# Development Branch Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Push the completed Quarto redesign from this fork's `main` branch to `ESIPFed/Governance` as a `development` branch, and get GitHub Pages serving its build output — the repo's first working live deployment.

**Architecture:** No new code. This is a config + git-remote + CI-trigger change: fix two config values (`_quarto.yml` repo pointers, workflow trigger branch), push existing history to a new upstream branch, let the existing (already-proven) Actions workflow render and publish to a `gh-pages` branch, then point upstream Pages settings at that branch.

**Tech Stack:** Quarto, GitHub Actions (`quarto-actions/publish@v2`), GitHub Pages, `gh` CLI, git.

## Global Constraints

- Do not modify `master` on `ESIPFed/Governance` in any way (per spec — content, history, and its Pages association are left untouched until a future, separate merge decision).
- Do not open a tracking PR (explicitly declined in the design spec).
- The final Pages-settings cutover (Task 6) requires explicit user go-ahead in chat immediately before it's executed — it's a settings change on a shared org repo, distinct from earlier approval of this plan.
- All upstream-repo commands target `ESIPFed/Governance`; all fork commands target `amfriesz/Governance` (`origin`).

Reference: [docs/superpowers/specs/2026-07-02-development-branch-deployment-design.md](../specs/2026-07-02-development-branch-deployment-design.md)

---

### Task 1: Fix `_quarto.yml` repo pointers

**Files:**
- Modify: `_quarto.yml:13`

**Interfaces:**
- Produces: `book.repo-url` = `https://github.com/ESIPFed/Governance`, `book.repo-branch` = `development`. Later tasks (verification in Task 5) rely on these values to confirm "Edit this page" links resolve correctly.

- [ ] **Step 1: Edit `repo-url` and add `repo-branch`**

In `_quarto.yml`, change line 13 from:

```yaml
  repo-url: https://github.com/amfriesz/Governance
```

to:

```yaml
  repo-url: https://github.com/ESIPFed/Governance
  repo-branch: development
```

- [ ] **Step 2: Verify the change**

Run: `grep -n "repo-url\|repo-branch" _quarto.yml`
Expected output:
```
13:  repo-url: https://github.com/ESIPFed/Governance
14:  repo-branch: development
```

- [ ] **Step 3: Render locally to confirm no config errors**

Run: `quarto render index.qmd --to html -o /tmp/quarto-check 2>&1 | tail -20`
Expected: renders without YAML/config errors (content warnings about other files are unrelated and fine — this only smoke-tests the `book:` config parses).

- [ ] **Step 4: Commit**

```bash
git add _quarto.yml
git commit -m "Point repo-url and repo-branch at ESIPFed/Governance development branch"
```

---

### Task 2: Fix workflow trigger branch

**Files:**
- Modify: `.github/workflows/publish.yml:4`

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces: workflow now triggers on push to `development`. Task 4 (push to upstream) relies on this trigger existing before the push happens.

- [ ] **Step 1: Edit the trigger**

In `.github/workflows/publish.yml`, change:

```yaml
on:
  push:
    branches: [master]
  workflow_dispatch:
```

to:

```yaml
on:
  push:
    branches: [development]
  workflow_dispatch:
```

- [ ] **Step 2: Verify the change**

Run: `grep -A2 "^on:" .github/workflows/publish.yml`
Expected output:
```
on:
  push:
    branches: [development]
  workflow_dispatch:
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "Trigger publish workflow on push to development branch"
```

---

### Task 3: Add upstream remote

**Files:** none (git config only)

**Interfaces:**
- Produces: a git remote named `upstream` pointing at `https://github.com/ESIPFed/Governance.git`. Task 4 pushes through this remote.

- [ ] **Step 1: Add the remote**

```bash
git remote add upstream https://github.com/ESIPFed/Governance.git
```

- [ ] **Step 2: Verify**

Run: `git remote -v`
Expected: includes
```
upstream	https://github.com/ESIPFed/Governance.git (fetch)
upstream	https://github.com/ESIPFed/Governance.git (push)
```
alongside the existing `origin` (amfriesz/Governance) entries.

---

### Task 4: Push `main` to upstream `development`

**Files:** none

**Interfaces:**
- Consumes: `upstream` remote from Task 3; committed changes from Tasks 1–2.
- Produces: `development` branch on `ESIPFed/Governance`, matching local `main` at push time. Task 5 verifies the resulting Action run.

- [ ] **Step 1: Push**

```bash
git push upstream main:development
```

Expected: push succeeds (this is a new branch on upstream, not a force-push — should be a plain fast-forward-style branch creation since upstream and the fork share history).

- [ ] **Step 2: Verify the branch exists on upstream**

Run: `gh api repos/ESIPFed/Governance/branches/development --jq '.name'`
Expected output: `development`

---

### Task 5: Verify the Action run and `gh-pages` branch

**Files:** none

**Interfaces:**
- Consumes: the push from Task 4, which triggers `.github/workflows/publish.yml` on upstream.
- Produces: a confirmed-good `gh-pages` branch on `ESIPFed/Governance`. Task 6 (cutover) depends on this existing and being correct before touching Pages settings.

- [ ] **Step 1: Watch the workflow run**

```bash
gh run watch --repo ESIPFed/Governance $(gh run list --repo ESIPFed/Governance --branch development --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: run completes with conclusion `success`. If it fails, read the failed step's log via `gh run view --repo ESIPFed/Governance --log-failed` before proceeding — do not continue to Task 6 on a failed run.

- [ ] **Step 2: Confirm `gh-pages` branch was created/updated**

Run: `gh api repos/ESIPFed/Governance/branches/gh-pages --jq '{name, commit: .commit.sha}'`
Expected: returns a branch object with a recent commit SHA (matching the timestamp of the run in Step 1).

- [ ] **Step 3: Spot-check rendered content**

Run: `gh api repos/ESIPFed/Governance/contents/index.html --ref gh-pages --jq '.name'`
Expected output: `index.html` — confirms the book actually rendered into the branch, not just an empty/failed publish.

---

### Task 6: Cutover — point Pages at `gh-pages`

**Files:** none (GitHub repo settings only)

**Interfaces:**
- Consumes: verified `gh-pages` branch from Task 5.
- Produces: a live site at `https://esipfed.github.io/Governance/`.

**This task requires explicit user go-ahead in chat immediately before Step 1** — it changes Pages settings on the shared `ESIPFed/Governance` org repo. Do not run Step 1 as part of an unattended batch; stop and ask first even if earlier tasks were approved to run inline.

- [ ] **Step 1: Update Pages source (after explicit go-ahead)**

```bash
gh api -X PUT repos/ESIPFed/Governance/pages \
  -f "build_type=legacy" \
  -f "source[branch]=gh-pages" \
  -f "source[path]=/"
```

- [ ] **Step 2: Verify the settings changed**

Run: `gh api repos/ESIPFed/Governance/pages --jq '{build_type, source}'`
Expected output:
```json
{"build_type": "legacy", "source": {"branch": "gh-pages", "path": "/"}}
```

- [ ] **Step 3: Verify the live site**

Run: `curl -s -o /dev/null -w "%{http_code}\n" https://esipfed.github.io/Governance/`
Expected: `200` (allow up to ~2 minutes after Step 1 for Pages to rebuild from the new source; retry if it still shows 404 immediately after the settings change).

Then open `https://esipfed.github.io/Governance/` and confirm:
- Landing page loads with the ESIP Governance title and sidebar
- Sidebar shows Bylaws, Corporate Policies, Ethics & Conduct, Business & Finance, Human Resources, Committee Procedures, Position Descriptions, Contributing
- Search works (try "conflict of interest")
- "Edit this page" link on any content page opens the file at `github.com/ESIPFed/Governance/edit/development/...` (confirms `repo-branch: development` from Task 1 took effect)

---

## Self-Review

### Spec coverage check

| Spec requirement | Covered by task |
|---|---|
| Revert `repo-url` to ESIPFed/Governance | Task 1 |
| Add `repo-branch: development` | Task 1 |
| Workflow trigger on `development` instead of `master` | Task 2 |
| Add `upstream` remote | Task 3 |
| Push `main` → upstream `development` (no rewrite) | Task 4 |
| Verify Action renders and publishes to `gh-pages` before touching Pages settings | Task 5 |
| Explicit confirmation checkpoint before cutover | Task 6 |
| Switch Pages source `master` → `gh-pages` | Task 6 |
| Verify live site content and "Edit this page" links | Task 6, Step 3 |
| `master` left untouched | No task modifies `master` — satisfied by omission |
| No tracking PR opened | No task opens a PR — satisfied by omission |

All spec requirements are covered. No gaps found.

### Placeholder scan

No TBD/TODO markers; every step has exact commands or exact YAML diffs.

### Type/name consistency

- `repo-branch: development` (Task 1) matches the branch name used in Tasks 2–6 throughout.
- `upstream` remote name (Task 3) is used consistently in Task 4's push command.
- `gh-pages` branch name is consistent across Tasks 2 (workflow `target: gh-pages`, pre-existing/unchanged), 5, and 6.
