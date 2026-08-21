#!/usr/bin/env python3
"""Warn (non-blocking) on staged .qmd/.md prose lines over 80 columns that
could have been wrapped, per the convention set in commit 06815ad."""
import json
import re
import subprocess
import sys

LIMIT = 80


def staged_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, check=False,
    ).stdout.splitlines()
    return [f for f in out if f.endswith((".qmd", ".md"))]


def staged_lines(path):
    result = subprocess.run(
        ["git", "show", f":{path}"], capture_output=True, text=True, check=False
    )
    return result.stdout.splitlines()


def is_table_row(stripped):
    return stripped.startswith("|") or bool(re.fullmatch(r"[\s|:-]+", stripped))


def is_separator(stripped):
    return bool(re.fullmatch(r"(-{3,}|={3,}|_{3,})", stripped))


def is_breakable(line, limit):
    indent = len(line) - len(line.lstrip(" "))
    window = line[indent:limit]
    return " " in window.strip()


def check_file(path):
    violations = []
    in_front_matter = False
    in_code_block = False
    for i, line in enumerate(staged_lines(path), start=1):
        stripped = line.strip()
        if i == 1 and stripped == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if stripped == "---":
                in_front_matter = False
            continue
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if is_table_row(stripped) or is_separator(stripped):
            continue
        if len(line) > LIMIT and is_breakable(line, LIMIT):
            violations.append((i, len(line)))
    return violations


def main():
    sys.stdin.read()  # consume the hook payload; not otherwise needed
    findings = {}
    for path in staged_files():
        violations = check_file(path)
        if violations:
            findings[path] = violations

    if not findings:
        return 0

    lines = ["Prose line-wrap check (repo convention: ~80 cols, see commit 06815ad):"]
    for path, violations in findings.items():
        preview = ", ".join(f"L{n} ({length} chars)" for n, length in violations[:5])
        more = f", +{len(violations) - 5} more" if len(violations) > 5 else ""
        lines.append(f"  {path}: {preview}{more}")
    lines.append("Not blocking the commit -- review and rewrap if unintentional.")

    print(json.dumps({"systemMessage": "\n".join(lines)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
