# Record Maintenance Heading Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the Appendix A section-numbering bug in Policy 1.6 (issue #56) by converting pseudo-list section labels to real Markdown headings, and clean up a related Google-Docs-export artifact file.

**Architecture:** This is a content/documentation fix, not code — there is no test suite. "Testing" means rendering each file with `quarto render` and inspecting the generated HTML with `grep`/`python` to confirm headings appear correctly and in sequence, exactly as done during the design review. Each task edits `.qmd` source, renders, verifies, then commits.

**Tech Stack:** Quarto (`quarto render`), Markdown, Pandoc (via Quarto).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-06-record-maintenance-heading-fix-design.md` — every task's requirements implicitly include this spec.
- Site config has `number-sections: false` (`_quarto.yml`), so heading numbers/letters are authored by hand in the heading text itself, matching the convention already used in `policies/1-corporate/1-9-data-privacy.qmd`.
- Preserve original heading text casing exactly as authored (the source uses ALL CAPS for Appendix A subsection titles — keep it).
- Do not touch the nested `1./2.` ordered lists under sections A, D, and E — those already render correctly and are out of scope.
- Do not modify any body paragraph content/wording — only the section-label lines (and the two new placeholder sections defined in Task 4).
- Branch: `56-fix-record-maintenance-appendix-a-numbering` (already checked out).
- `_book/` is gitignored — render output never needs to be staged or cleaned up.
- Quarto sometimes rewrites `.gitignore` (adding `/.quarto/`) as a side effect of `quarto render`. If you see `.gitignore` modified after rendering, run `git checkout -- .gitignore` before committing — it is not part of this work.

---

### Task 1: Convert top-matter sections 1–5 to real headings

**Files:**
- Modify: `policies/1-corporate/1-6-record-maintenance.qmd`

**Interfaces:** N/A — content-only change, no code.

- [ ] **Step 1: Render current state and confirm the pre-fix structure**

Run: `quarto render policies/1-corporate/1-6-record-maintenance.qmd`

Then inspect the relevant section:

```bash
python3 -c "
with open('_book/policies/1-corporate/1-6-record-maintenance.html') as f:
    c = f.read()
idx = c.find('id=\"quarto-document-content\"')
print(c[idx:idx+3000])
" | grep -n '<ol\|<h[1-6]'
```

Expected: you see `<ol type="1">` blocks for Purpose/Policy/Administration/etc — confirming these are currently list items, not headings.

- [ ] **Step 2: Convert the five section labels to headings**

In `policies/1-corporate/1-6-record-maintenance.qmd`, make these five replacements (exact text match, including the span wrapper being removed):

Replace:
```
1.  <span class="c10">Purpose</span>
```
With:
```
### 1. Purpose
```

Replace:
```
2.  <span class="c10">Policy</span>
```
With:
```
### 2. Policy
```

Replace:
```
3.  <span class="c10">Administration</span>
```
With:
```
### 3. Administration
```

Replace:
```
4.  <span class="c32 c63">Suspension of Record Disposal In Event of
    Litigation or Claims</span>
```
With:
```
### 4. Suspension of Record Disposal In Event of Litigation or Claims
```

Replace:
```
5.  <span class="c10">Applicability</span>
```
With:
```
### 5. Applicability
```

- [ ] **Step 3: Render and verify**

Run: `quarto render policies/1-corporate/1-6-record-maintenance.qmd`

```bash
python3 -c "
with open('_book/policies/1-corporate/1-6-record-maintenance.html') as f:
    c = f.read()
idx = c.find('id=\"quarto-document-content\"')
print(c[idx:idx+3000])
" | grep -n '<h3\|<ol type=\"1\"'
```

Expected: five `<h3>` elements containing "Purpose", "Policy", "Administration", "Suspension of Record Disposal...", "Applicability" — and no more `<ol type="1">` blocks for these five items.

- [ ] **Step 4: Commit**

```bash
git add policies/1-corporate/1-6-record-maintenance.qmd
git commit -m "Convert Policy 1.6 top-matter sections to real headings"
```

---

### Task 2: Convert Appendix A intro and section-topic index to headings/bullets

**Files:**
- Modify: `policies/1-corporate/1-6-record-maintenance.qmd`

**Interfaces:** N/A — content-only change, no code.

- [ ] **Step 1: Replace the Appendix A intro block and index list**

Replace this entire block (exact match):
```
<span class="c10">APPENDIX A  RECORD RETENTION SCHEDULE</span>

<span class="c1">The Record Retention Schedule is organized as
follows:</span>

<span class="c1"></span>

<span class="c10">SECTION TOPIC</span>

<span class="c1"></span>

A.  <span class="c1">Accounting and Finance</span>

B.  <span class="c1">Contracts</span>

C.  <span class="c1">Corporate Records</span>

D.  <span class="c1">Correspondence and Internal Memoranda</span>

E.  <span class="c1">Electronic Documents</span>

F.  <span class="c1">Grant Records </span>

G.  <span class="c1">Insurance Records</span>

H.  <span class="c1">Legal Files and Papers</span>

I.  <span class="c1">Miscellaneous</span>

J. <span class="c1">Payroll Documents</span>

K. <span class="c1">Pension Documents </span>

L. <span class="c1">Personnel Records</span>

M. <span class="c1">Property Records</span>

N. <span class="c1">Tax Records</span>

O. <span class="c1">Contribution Records</span>

P. <span class="c1">Programs & Services Records</span>

Q. <span class="c1">Fiscal Sponsor Project Records</span>
```

With:
```
### Appendix A: Record Retention Schedule

The Record Retention Schedule is organized as follows:

**Section Topic**

- A. Accounting and Finance
- B. Contracts
- C. Corporate Records
- D. Correspondence and Internal Memoranda
- E. Electronic Documents
- F. Grant Records
- G. Insurance Records
- H. Legal Files and Papers
- I. Miscellaneous
- J. Payroll Documents
- K. Pension Documents
- L. Personnel Records
- M. Property Records
- N. Tax Records
- O. Contribution Records
- P. Programs & Services Records
- Q. Fiscal Sponsor Project Records
```

- [ ] **Step 2: Render and verify**

Run: `quarto render policies/1-corporate/1-6-record-maintenance.qmd`

```bash
python3 -c "
with open('_book/policies/1-corporate/1-6-record-maintenance.html') as f:
    c = f.read()
idx = c.find('Appendix A')
print(c[idx-200:idx+2500])
" | grep -n '<h3\|<ul\|<li\|<ol'
```

Expected: one `<h3>` containing "Appendix A", followed by a `<ul>` (not `<ol>`) with 17 `<li>` entries, one per letter A–Q.

- [ ] **Step 3: Commit**

```bash
git add policies/1-corporate/1-6-record-maintenance.qmd
git commit -m "Convert Appendix A intro and section-topic index to heading and bullet list"
```

---

### Task 3: Convert body subsection headers A–L to real headings

**Files:**
- Modify: `policies/1-corporate/1-6-record-maintenance.qmd`

**Interfaces:** N/A — content-only change, no code. These 12 sections' content already matches their index position — only the label line changes, table/paragraph content underneath is untouched.

- [ ] **Step 1: Replace each of the 12 section label lines**

Make these 12 replacements (exact text match each; each occurs exactly once in the file):

Replace:
```
A.  <span class="c10">ACCOUNTING AND
FINANCE</span>
```
With:
```
#### A. ACCOUNTING AND FINANCE
```

Replace:
```
B.  <span class="c10">CONTRACTS</span>
```
With:
```
#### B. CONTRACTS
```

Replace:
```
C.  <span class="c10">CORPORATE RECORDS
</span>
```
With:
```
#### C. CORPORATE RECORDS
```

Replace:
```
D.  <span class="c10">CORRESPONDENCE AND INTERNAL MEMORANDA</span>
```
With:
```
#### D. CORRESPONDENCE AND INTERNAL MEMORANDA
```

Replace:
```
E.  <span class="c10">ELECTRONIC
    </span><span class="c10">DOCUMENTS</span>
```
With:
```
#### E. ELECTRONIC DOCUMENTS
```

Replace:
```
F.  <span class="c10">GRANT RECORDS
</span>
```
With:
```
#### F. GRANT RECORDS
```

Replace:
```
G.  <span class="c10">INSURANCE
RECORDS</span>
```
With:
```
#### G. INSURANCE RECORDS
```

Replace:
```
H.  <span class="c10">LEGAL FILES AND
PAPERS</span>
```
With:
```
#### H. LEGAL FILES AND PAPERS
```

Replace:
```
I.  <span class="c10">MISCELLANEOUS</span>
```
With:
```
#### I. MISCELLANEOUS
```

Replace:
```
J. <span class="c10">PAYROLL
DOCUMENTS</span>
```
With:
```
#### J. PAYROLL DOCUMENTS
```

Replace:
```
K. <span class="c10">PENSION DOCUMENTS AND SUPPORTING EMPLOYEE
    DATA</span>
```
With:
```
#### K. PENSION DOCUMENTS AND SUPPORTING EMPLOYEE DATA
```

Replace:
```
L. <span class="c10">PERSONNEL
RECORDS</span>
```
With:
```
#### L. PERSONNEL RECORDS
```

- [ ] **Step 2: Render and verify**

Run: `quarto render policies/1-corporate/1-6-record-maintenance.qmd`

```bash
grep -oE '<h4[^>]*>.*?</h4>' _book/policies/1-corporate/1-6-record-maintenance.html
```

Expected: 12 `<h4>` elements in order, text content: "A. ACCOUNTING AND FINANCE", "B. CONTRACTS", "C. CORPORATE RECORDS", "D. CORRESPONDENCE AND INTERNAL MEMORANDA", "E. ELECTRONIC DOCUMENTS", "F. GRANT RECORDS", "G. INSURANCE RECORDS", "H. LEGAL FILES AND PAPERS", "I. MISCELLANEOUS", "J. PAYROLL DOCUMENTS", "K. PENSION DOCUMENTS AND SUPPORTING EMPLOYEE DATA", "L. PERSONNEL RECORDS" — no gaps, no reset at I, J onward all present (this is the direct regression check for issue #56).

- [ ] **Step 3: Commit**

```bash
git add policies/1-corporate/1-6-record-maintenance.qmd
git commit -m "Convert Appendix A sections A-L to real headings"
```

---

### Task 4: Re-letter M/N/O to N/O/P and add placeholder sections M and Q

**Files:**
- Modify: `policies/1-corporate/1-6-record-maintenance.qmd`

**Interfaces:** N/A — content-only change, no code.

- [ ] **Step 1: Insert the Property Records placeholder and re-letter Tax Records**

Replace (exact match, occurs once):
```
M. <span class="c10">TAX RECORDS</span>
```
With:
```
#### M. PROPERTY RECORDS

*Content for this section has not yet been supplied. Contact the Policy Administrator to complete the Property Records retention schedule.*

#### N. TAX RECORDS
```

- [ ] **Step 2: Re-letter Contribution Records**

Replace (exact match, occurs once):
```
N. <span class="c10">CONTRIBUTION
RECORDS</span>
```
With:
```
#### O. CONTRIBUTION RECORDS
```

- [ ] **Step 3: Re-letter Program and Service Records**

Replace (exact match, occurs once):
```
O. <span class="c10">PROGRAM AND SERVICE
RECORDS</span>
```
With:
```
#### P. PROGRAM AND SERVICE RECORDS
```

- [ ] **Step 4: Insert the Fiscal Sponsor Project Records placeholder at the end of the document**

Replace (exact match — this exact wording occurs once; the file has a similarly-worded approval line near the top, but that one uses different markup and does not match this text exactly):
```
<span class="c1"></span>

<span class="c1"></span>

<span class="c51">This Policy was approved by the Board of Directors of
ESIP on October 17, 2017. </span>
```
With:
```
#### Q. FISCAL SPONSOR PROJECT RECORDS

*Content for this section has not yet been supplied. Contact the Policy Administrator to complete the Fiscal Sponsor Project Records retention schedule.*

This Policy was approved by the Board of Directors of ESIP on October 17, 2017.
```

- [ ] **Step 5: Full-document render and verification**

Run: `quarto render policies/1-corporate/1-6-record-maintenance.qmd`

```bash
grep -oE '<h3[^>]*>.*?</h3>|<h4[^>]*>.*?</h4>' _book/policies/1-corporate/1-6-record-maintenance.html
```

Expected: exactly 5 `<h3>` elements (Purpose, Policy, Administration, Suspension..., Applicability), one `<h3>` "Appendix A: Record Retention Schedule", and 17 `<h4>` elements in order A through Q (A. ACCOUNTING AND FINANCE ... Q. FISCAL SPONSOR PROJECT RECORDS), with M and Q present as the new placeholder sections. No duplicate letters, no gaps, no reset.

Also confirm the placeholder text renders as a paragraph under each of M and Q:

```bash
grep -A2 'PROPERTY RECORDS\|FISCAL SPONSOR PROJECT RECORDS' _book/policies/1-corporate/1-6-record-maintenance.html
```

- [ ] **Step 6: Commit**

```bash
git add policies/1-corporate/1-6-record-maintenance.qmd
git commit -m "Re-letter Appendix A sections M-O to N-P and add placeholders for missing M and Q sections"
```

---

### Task 5: Clean up leftover span markup in 3.3A FiCom Budget Cycle

**Files:**
- Modify: `policies/3-business-finance/3-3a-ficom-budget-cycle.qmd`

**Interfaces:** N/A — content-only change, no code.

- [ ] **Step 1: Read the current file**

Run: Read `policies/3-business-finance/3-3a-ficom-budget-cycle.qmd` to confirm current content before overwriting (required before using Write on an existing file).

- [ ] **Step 2: Rewrite the file with clean Markdown**

Overwrite `policies/3-business-finance/3-3a-ficom-budget-cycle.qmd` with:

```markdown
---
title: "3.3A FiCom Annual Budget Cycle"
date: 2024-04-02
---

| Task | Timeframe |
| --- | --- |
| Annual Committee and Working Group budgets | 4 months before beginning of fiscal year |
| Budget request for next fiscal year to Standing Committee and Working Group chairs | First week of June |
| Committee and Working Group budgets due to FiCom | First week of August |
| Committee and Working Group budget reviews complete and forwarded to Board for approval | First week of September |
| Committee and Working Group chairs notified of budget decisions | Second week of September |
| ESIP meeting travel funding requests (to be handled by Program Committee going forward) | tied to ESIP meeting planning schedule |
| Availability of travel funds announced | ESIP call for sessions |
| Travel budgets due to FiCom | Session proposal due date |
| Travel budget reviews complete and requestors notified | 2 weeks after budgets due |
| Special Project funding requests - workshops, etc. | As needed |
| Special Project request submitted (NOTE: Special Projects are those that don't fit into testbed, incubator, or other ESIP funding opportunities) | At least 2 months before funds needed |
| Special Project budget reviews complete and requestors notified | Within 1 month of request |
| Committee Membership Cycle | Nominal 1 year term |
```

- [ ] **Step 3: Render and verify**

Run: `quarto render policies/3-business-finance/3-3a-ficom-budget-cycle.qmd`

```bash
grep -c 'span class="c' _book/policies/3-business-finance/3-3a-ficom-budget-cycle.html
grep -c '<td>' _book/policies/3-business-finance/3-3a-ficom-budget-cycle.html
```

Expected: first command outputs `0` (no leftover span-class wrappers survived into the render — note the site's own CSS/JS may add unrelated `span` tags elsewhere in the page shell, so if this isn't exactly 0, open the file and confirm any matches are outside the table body, not leftover `cNN` artifacts); second command outputs `26` (13 data rows × 2 columns, confirming the table still has all its content).

- [ ] **Step 4: Commit**

```bash
git add policies/3-business-finance/3-3a-ficom-budget-cycle.qmd
git commit -m "Strip leftover Google-Docs span markup from FiCom budget cycle table"
```

---

### Task 6: Final full-book verification

**Files:** None modified — verification only.

**Interfaces:** N/A.

- [ ] **Step 1: Render the full book**

Run: `quarto render`

Expected: exits 0, no errors or warnings about the two files touched in this plan.

- [ ] **Step 2: Confirm the martha-maiden-award link still resolves**

This plan doesn't touch `procedures/martha-maiden-award.qmd`, but it's a good final sanity check that the site as a whole still builds correctly after these changes:

```bash
grep -o 'href="[^"]*2-2-conflict-of-interest[^"]*"' _book/procedures/martha-maiden-award.html
```

Expected: `../policies/2-ethics-conduct/2-2-conflict-of-interest.html` (unchanged from the earlier fix).

- [ ] **Step 3: Confirm no unintended `.gitignore` changes are staged**

```bash
git status --short
```

Expected: clean working tree (everything already committed in Tasks 1–5). If `.gitignore` shows as modified, run `git checkout -- .gitignore` — this is the known Quarto side effect described in Global Constraints, not part of this work.
