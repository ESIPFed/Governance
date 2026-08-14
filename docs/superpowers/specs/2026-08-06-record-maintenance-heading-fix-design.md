# Design: Fix Appendix A Section Numbering in Policy 1.6 (Record Maintenance)

**Date:** 2026-08-06
**Related issue:** [ESIPFed/Governance#56](https://github.com/ESIPFed/Governance/issues/56)
**Branch:** `56-fix-record-maintenance-appendix-a-numbering`

## Problem

In `policies/1-corporate/1-6-record-maintenance.qmd`, Appendix A's section
labels (`A.` through `Q.`) are written as literal text formatted to look
like Pandoc ordered-list markers, rather than as real Markdown headings.
This is fragile by construction, and breaks in two independent ways in the
current rendered output:

1. **Roman/alpha ambiguity.** A lone `I.` marker is ambiguous between the
   9th letter of an alpha list and the roman numeral for 1. Pandoc resolves
   this by starting a new roman-numbered list at `I.`, which visually reads
   almost identically to `1.` in the rendered font — so the index and the
   actual section heading disagree (index says "9", heading renders as
   "I."/"1.").
2. **Single vs. double space after the marker.** Pandoc requires two spaces
   after a lone-letter ordered-list marker (`A.  `) to avoid misreading
   prose initials (e.g. "J. Smith") as list markers. Sections A–I use two
   spaces and are recognized as list items; sections J–Q use one space and
   are never recognized as list items at all — they render as plain
   paragraph text, which is why the issue reports "J–Q keep their original
   letters."

Root cause: these are semantically section headings, not list items. Ordered
list markers were never the right tool for this content, and the failure
modes above are inherent to that mismatch, not a one-off typo.

Same root problem also affects the top-matter sections (`1. Purpose`,
`2. Policy`, etc.) structurally, though they don't currently exhibit a
visible bug since decimal numbering doesn't have the alpha/roman ambiguity.

Separately, `policies/3-business-finance/3-3a-ficom-budget-cycle.qmd` was
found to share the same Google-Docs-export origin but *not* the same bug —
it has no headings or lists, just a table wrapped in meaningless leftover
`<span class="cNN">` styling artifacts with no corresponding CSS. It's
included here as a light, low-risk cleanup since it was already surfaced
during this review.

### Pre-existing content gap (independent of the rendering bug)

Comparing the "SECTION TOPIC" index (17 items, A–Q) against the Appendix A
body by subject rather than by letter turned up a second, unrelated problem
that would keep the index and the body disagreeing even after the Pandoc
bug is fixed:

| Index position | Index says | Body has |
| --- | --- | --- |
| 1–12 (A–L) | Accounting and Finance → Personnel Records | Matches correctly, letter and content agree |
| 13 (M) | Property Records | **No corresponding body section exists** |
| 14 (N) | Tax Records | Present in body, but currently labeled `M.` |
| 15 (O) | Contribution Records | Present in body, but currently labeled `N.` |
| 16 (P) | Programs & Services Records | Present in body, but currently labeled `O.` |
| 17 (Q) | Fiscal Sponsor Project Records | **No corresponding body section exists — document ends after "Program and Service Records"** |

This is a pre-existing gap in the source document (not introduced by the
Markdown conversion): two whole topics have no body content, and the three
sections after the gap are each one letter off from what the index claims.
Decision: keep all 17 index items and add explicit placeholder headings in
the body for the two missing sections (`M. Property Records` and
`Q. Fiscal Sponsor Project Records`), each with a short note that content
needs to be supplied, and re-letter the existing `M.`/`N.`/`O.` body
sections to `N.`/`O.`/`P.` so every body heading matches its actual index
position and content.

## Fix

### 1. `policies/1-corporate/1-6-record-maintenance.qmd`

Convert all pseudo-list section labels to real Markdown headings, matching
the convention already established elsewhere in the repo (e.g.
`policies/1-corporate/1-9-data-privacy.qmd`, which uses manually-numbered
headings like `### 1. OVERVIEW`, `#### 2.1. INDIVIDUAL INFORMATION` — the
site has `number-sections: false`, so numbers are authored by hand, not
auto-generated):

- Top-matter sections 1–5 → `### 1. Purpose`, `### 2. Policy`,
  `### 3. Administration`, `### 4. Suspension of Record Disposal In Event of
  Litigation or Claims`, `### 5. Applicability`
- `APPENDIX A RECORD RETENTION SCHEDULE` → `### Appendix A: Record Retention
  Schedule`
- Each lettered subsection A–L → `#### A. Accounting and Finance`,
  `#### B. Contracts`, ... `#### L. Personnel Records` (unchanged letters,
  content already matches the index)
- The existing `M.`/`N.`/`O.` body sections (Tax Records, Contribution
  Records, Program and Service Records) are re-lettered to `N.`/`O.`/`P.`
  to match their actual index position
- Two new placeholder headings are added to restore the missing index
  items, each with a single sentence of placeholder body text flagging
  that content is needed:
  - `#### M. Property Records` — placeholder text: "*Content for this
    section has not yet been supplied. Contact the Policy Administrator to
    complete the Property Records retention schedule.*"
  - `#### Q. Fiscal Sponsor Project Records` — placeholder text: "*Content
    for this section has not yet been supplied. Contact the Policy
    Administrator to complete the Fiscal Sponsor Project Records retention
    schedule.*"
  - `M.` is inserted immediately before the re-lettered `N.` (Tax Records);
    `Q.` is appended after the re-lettered `P.` (Program and Service
    Records), since the document currently ends there

Headings sidestep the bug entirely: no list-marker ambiguity, no
continuation tracking across intervening tables/paragraphs, and Quarto's
sidebar TOC picks them up automatically.

Genuinely-enumerated content that already renders correctly (the nested
`1./2.` ordered lists under sections A, D, and E — e.g. "Credit card record
retention and destruction") is **not** part of this fix and stays as-is.

The "SECTION TOPIC" index list at the top of Appendix A becomes a plain
unordered Markdown list (`-` bullets), not an ordered/lettered list and not
anchor-linked:

```markdown
- A. Accounting and Finance
- B. Contracts
- C. Corporate Records
...
- Q. Fiscal Sponsor Project Records
```

Plain bullets keep this preview list visually distinct from the real
headings below and avoid re-triggering the same marker-ambiguity class of
bug. No links are added since Quarto's auto-generated sidebar TOC already
provides in-page navigation once the sections below are real headings.

### 2. `policies/3-business-finance/3-3a-ficom-budget-cycle.qmd`

Strip the leftover `<span class="cNN">` / `<span id="t...">` wrapper markup
from the table cells and surrounding empty spans. Purely a source-legibility
cleanup — no rendered behavior change, since these classes have no matching
CSS in the site.

## Guideline for future conversions

Documents originally authored in Google Docs and exported to Markdown can
carry over numbered/lettered labels as literal marker-style text (`A.`,
`1.`) instead of real headings. **Numbered or lettered section labels must
be authored as real Markdown headings (`#`/`##`/`###`/etc.), never as bare
`A.`/`1.` text meant to visually resemble a list marker.** Pandoc's ordered-
list parsing has marker-ambiguity edge cases (notably single-letter roman
numerals, and spacing requirements to disambiguate from prose initials)
that make bare-text pseudo-headers fragile in ways that are easy to miss
during conversion and hard to spot without rendering the output.

## Verification

For both files, run `quarto render` and inspect the rendered HTML:

- `1-6-record-maintenance.qmd`: confirm all Appendix A sections A–Q render
  as real `<h4>` elements in correct sequence (all 17 letters present, no
  reset/break at `I`, `M` and `Q` present as placeholders), and that the
  top-matter sections 1–5 render as `<h3>` elements.
- `3-3a-ficom-budget-cycle.qmd`: confirm the table renders with clean `<td>`
  content and no leftover `<span class="cNN">` wrappers.

## Out of scope

- Converting the nested `1./2.` enumerations under sections A, D, and E
  (e.g. "Electronic Mail" / "Electronic Documents" under section E) into
  sub-headings. These currently render correctly as ordered lists; changing
  their semantic role is a judgment call left for a future pass if desired,
  not required to fix issue #56.
- Any other Google-Docs-export artifacts elsewhere in the repo beyond the
  two files identified during this review.
- Writing the actual Property Records / Fiscal Sponsor Project Records
  retention policy content. This fix only adds placeholder headings with a
  note that content is needed — supplying the real retention schedule is a
  policy decision for the Policy Administrator, not a documentation-tooling
  task.
