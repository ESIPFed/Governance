# ESIP Governance Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the ESIP Governance repository into a searchable, navigable Quarto web book hosted on GitHub Pages, with a clean file structure and a documented contribution workflow for staff and board members.

**Architecture:** Five sequential phases — (1) content audit producing a findings report, (2) repository reorganization consolidating Bylaws files and renaming folders, (3) Quarto web book configuration with full-text search and sidebar navigation, (4) GitHub Actions CI/CD deploying to GitHub Pages on every merge, (5) contribution workflow documentation published in the book itself.

**Tech Stack:** Quarto (≥ 1.4), GitHub Actions, GitHub Pages, SCSS, Markdown/QMD

> **Output directory note:** The spec listed `output-dir: docs` but `docs/` already contains committed planning files. This plan uses `_book/` (Quarto's default for book projects) instead, added to `.gitignore`. The live site always comes from the `gh-pages` branch via Actions — `_book/` is local-only.

---

## File Map

### New files (create)
- `_quarto.yml` — full project config and chapter list
- `custom.scss` — ESIP brand color overrides
- `index.qmd` — landing page
- `bylaws/index.qmd` — bylaws overview
- `bylaws/article-01-offices.qmd` — consolidated from 2 section files
- `bylaws/article-02-purposes.qmd` — consolidated from 1 section file
- `bylaws/article-03-members.qmd` — consolidated from 19 section files
- `bylaws/article-04-directors.qmd` — consolidated from 6 section files
- `bylaws/article-05-director-conduct.qmd` — consolidated from 9 section files
- `bylaws/article-06-board-meetings.qmd` — consolidated from 11 section files
- `bylaws/article-07-officers.qmd` — consolidated from 10 section files
- `bylaws/article-08-committees.qmd` — consolidated from 3 section files
- `bylaws/article-09-instruments.qmd` — consolidated from 5 section files
- `bylaws/article-10-records.qmd` — consolidated from 5 section files
- `bylaws/article-11-miscellaneous.qmd` — consolidated from 4 section files
- `policies/index.qmd` — P&P overview
- `policies/1-corporate/1-0-definitions.qmd`
- `policies/1-corporate/1-1-goals.qmd`
- `policies/1-corporate/1-2-partners.qmd`
- `policies/1-corporate/1-2a-nonvoting-associates.qmd`
- `policies/1-corporate/1-3-corporate-organization.qmd`
- `policies/1-corporate/1-3a-board-participation.qmd`
- `policies/1-corporate/1-4-policy-approval.qmd`
- `policies/1-corporate/1-5-equal-opportunity.qmd`
- `policies/1-corporate/1-6-record-maintenance.qmd`
- `policies/1-corporate/1-7-endorsements.qmd`
- `policies/1-corporate/1-8-logo-use.qmd`
- `policies/1-corporate/1-9-data-privacy.qmd`
- `policies/1-corporate/1-10-memoranda-of-understanding.qmd`
- `policies/2-ethics-conduct/2-1-community-participation-guidelines.qmd`
- `policies/2-ethics-conduct/2-2-conflict-of-interest.qmd`
- `policies/2-ethics-conduct/2-3-gift-acceptance.qmd`
- `policies/2-ethics-conduct/2-4-fundraising.qmd`
- `policies/2-ethics-conduct/2-5-whistleblower.qmd`
- `policies/3-business-finance/3-1-accounting.qmd`
- `policies/3-business-finance/3-2-internal-controls.qmd`
- `policies/3-business-finance/3-3-financial-planning.qmd`
- `policies/3-business-finance/3-3a-ficom-budget-cycle.qmd`
- `policies/3-business-finance/3-3f-committee-budget-request.qmd`
- `policies/3-business-finance/3-4-revenue-accounts-receivable.qmd`
- `policies/3-business-finance/3-5-expenses-accounts-payable.qmd`
- `policies/3-business-finance/3-5a-travel-expense.qmd`
- `policies/3-business-finance/3-5b-complimentary-registration.qmd`
- `policies/3-business-finance/3-5c-credit-card-points.qmd`
- `policies/3-business-finance/3-6-asset-management.qmd`
- `policies/3-business-finance/3-7-pass-through-funding.qmd`
- `policies/3-business-finance/3-8-gift-issuance.qmd`
- `policies/3-business-finance/3-9-procurement.qmd`
- `policies/4-human-resources/4-1-employee-handbook.qmd`
- `policies/4-human-resources/4-2-personnel-records.qmd`
- `policies/4-human-resources/4-3-employee-search-selection.qmd`
- `policies/4-human-resources/4-4-executive-director-evaluation.qmd`
- `procedures/index.qmd`
- `procedures/funding-friday.qmd`
- `procedures/raskin-scholarship.qmd`
- `procedures/martha-maiden-award.qmd`
- `procedures/cpg-reporting.qmd`
- `positions/executive-director.qmd`
- `contributing/index.qmd`
- `contributing/deployment.qmd`
- `contributing/template.qmd`
- `.github/workflows/publish.yml`
- `audit-report.md`

### Modified files
- `.gitignore` — add `_book/`
- `README.md` — replace content with short landing linking to web book

### Deleted after migration verified
- `Bylaws/` directory (all contents)
- `ESIP Policies and Procedures/` directory (all contents)
- `Standing Committee and Cluster Policies and Procedures/` directory (all contents)
- `Position Descriptions/` directory (all contents)

---

## Task 1: Run Content Audit

**Files:**
- Create: `audit-report.md`

- [ ] **Step 1: Enumerate all source files**

```bash
find . -not -path './.git/*' -not -path './docs/*' -not -path './.superpowers/*' \
  -type f | sort
```

Expected: ~80 files across Bylaws/, ESIP Policies and Procedures/, Standing Committee..., Position Descriptions/, Assembly Notes/

- [ ] **Step 2: Find files missing from any index**

```bash
# Files in repo not linked from either readme
comm -23 \
  <(find "ESIP Policies and Procedures" -name "*.md" | sort) \
  <(grep -oP '(?<=blob/master/).*\.md' "ESIP Policies and Procedures/readme.md" \
      | python3 -c "import sys,urllib.parse; [print(urllib.parse.unquote(l.strip())) for l in sys.stdin]" \
      | sort)
```

Expected output includes: `ESIP Policies and Procedures/3.0 Business and Finance/ESIP P&P 3.3A FiCom annual budget cycle.md`

- [ ] **Step 3: Find broken fork links**

```bash
grep -rn "BenGalewsky" . --include="*.md"
```

Expected output: one hit in `ESIP Policies and Procedures/readme.md` for the 1.10 MoU link

- [ ] **Step 4: Find draft/unapproved documents**

```bash
grep -rln "not yet been approved\|not yet approved\|pending approval" . --include="*.md"
```

Expected output: `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.0 Definitions.md`

- [ ] **Step 5: Find hardcoded GitHub blob URLs**

```bash
grep -rn "github.com.*blob/master" . --include="*.md" | grep -v ".git" | wc -l
```

Expected: > 50 (all readme navigation links are hardcoded blob URLs)

- [ ] **Step 6: Write audit-report.md**

Create `audit-report.md` in the repo root with the following structure. Fill in the complete findings from steps 1–5. The pre-identified issues below are confirmed starting points:

```markdown
# ESIP Governance Content Audit Report

**Date:** 2026-06-25
**Status:** Working document — not published to web book

This report documents all findings from the pre-reorganization content audit.
Fix items are addressed during implementation. Review items require staff or
board decision before changes are made.

## Findings

| ID | Severity | Location | Issue | Recommended Action |
|----|----------|----------|-------|--------------------|
| A-01 | fix | `ESIP Policies and Procedures/readme.md` | Link for P&P 1.10 MoU points to `BenGalewsky/Governance` fork instead of `ESIPFed/Governance` | Update URL to canonical repo during migration |
| A-02 | fix | `ESIP Policies and Procedures/readme.md` | `3.3A FiCom annual budget cycle.md` exists in repo but is absent from the P&P index | Add to navigation in `_quarto.yml` |
| A-03 | review | `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.0 Definitions.md` | Document states "not yet approved by the Board of Directors of ESIP" | Flag for board — add callout box noting draft status during migration; board to decide whether to approve or remove |
| A-04 | note | `Bylaws/readme.md` | Header states "Restated as of December 02, 2016" with no subsequent amendment dates | Record in bylaws/index.qmd; governance committee to maintain |
| A-05 | fix | All readme files | All navigation links are hardcoded GitHub blob URLs — will break on repo rename/fork | Replaced by Quarto sidebar navigation during migration |
| A-06 | [add further findings from steps 1-5 here] | | | |

## Orphaned files found
[List any files found in step 2 not already listed above]

## Notes
- `Assembly Notes/ESIP Assembly 2017 Winter Notes` — single non-markdown file, archive in place, do not migrate
- `Standing Committee and Cluster Policies and Procedures/Template for new Policies` — no file extension; migrate content to `contributing/template.qmd`
```

- [ ] **Step 7: Commit audit report**

```bash
git add audit-report.md
git commit -m "Add pre-migration content audit report"
```

---

## Task 2: Verify Quarto Installation

**Files:** none (environment check)

- [ ] **Step 1: Check if Quarto is installed**

```bash
quarto --version
```

Expected: a version string like `1.4.x` or higher. If command not found, install:

```bash
# macOS with Homebrew:
brew install quarto

# Or download installer from https://quarto.org/docs/get-started/
```

- [ ] **Step 2: Verify version is 1.4 or higher**

```bash
quarto --version | awk -F. '{if ($1 >= 1 && $2 >= 4) print "OK"; else print "UPGRADE NEEDED"}'
```

Expected: `OK`

---

## Task 3: Create Quarto Project Scaffold

**Files:**
- Create: `_quarto.yml`
- Create: `custom.scss`
- Create: `index.qmd`
- Modify: `.gitignore`

- [ ] **Step 1: Create `_quarto.yml`**

```yaml
project:
  type: book
  output-dir: _book

book:
  title: "ESIP Governance"
  author: "Earth Science Information Partners"
  description: "Official bylaws, policies, and procedures of the Foundation for Earth Science Information Partners."
  sidebar:
    style: "docked"
    collapse-level: 1
  search: true
  repo-url: https://github.com/ESIPFed/Governance
  repo-actions: [edit, issue]
  chapters:
    - index.qmd
    - part: "Bylaws"
      chapters:
        - bylaws/index.qmd
        - bylaws/article-01-offices.qmd
        - bylaws/article-02-purposes.qmd
        - bylaws/article-03-members.qmd
        - bylaws/article-04-directors.qmd
        - bylaws/article-05-director-conduct.qmd
        - bylaws/article-06-board-meetings.qmd
        - bylaws/article-07-officers.qmd
        - bylaws/article-08-committees.qmd
        - bylaws/article-09-instruments.qmd
        - bylaws/article-10-records.qmd
        - bylaws/article-11-miscellaneous.qmd
    - part: "Corporate Policies"
      chapters:
        - policies/index.qmd
        - policies/1-corporate/1-0-definitions.qmd
        - policies/1-corporate/1-1-goals.qmd
        - policies/1-corporate/1-2-partners.qmd
        - policies/1-corporate/1-2a-nonvoting-associates.qmd
        - policies/1-corporate/1-3-corporate-organization.qmd
        - policies/1-corporate/1-3a-board-participation.qmd
        - policies/1-corporate/1-4-policy-approval.qmd
        - policies/1-corporate/1-5-equal-opportunity.qmd
        - policies/1-corporate/1-6-record-maintenance.qmd
        - policies/1-corporate/1-7-endorsements.qmd
        - policies/1-corporate/1-8-logo-use.qmd
        - policies/1-corporate/1-9-data-privacy.qmd
        - policies/1-corporate/1-10-memoranda-of-understanding.qmd
    - part: "Ethics & Conduct"
      chapters:
        - policies/2-ethics-conduct/2-1-community-participation-guidelines.qmd
        - policies/2-ethics-conduct/2-2-conflict-of-interest.qmd
        - policies/2-ethics-conduct/2-3-gift-acceptance.qmd
        - policies/2-ethics-conduct/2-4-fundraising.qmd
        - policies/2-ethics-conduct/2-5-whistleblower.qmd
    - part: "Business & Finance"
      chapters:
        - policies/3-business-finance/3-1-accounting.qmd
        - policies/3-business-finance/3-2-internal-controls.qmd
        - policies/3-business-finance/3-3-financial-planning.qmd
        - policies/3-business-finance/3-3a-ficom-budget-cycle.qmd
        - policies/3-business-finance/3-3f-committee-budget-request.qmd
        - policies/3-business-finance/3-4-revenue-accounts-receivable.qmd
        - policies/3-business-finance/3-5-expenses-accounts-payable.qmd
        - policies/3-business-finance/3-5a-travel-expense.qmd
        - policies/3-business-finance/3-5b-complimentary-registration.qmd
        - policies/3-business-finance/3-5c-credit-card-points.qmd
        - policies/3-business-finance/3-6-asset-management.qmd
        - policies/3-business-finance/3-7-pass-through-funding.qmd
        - policies/3-business-finance/3-8-gift-issuance.qmd
        - policies/3-business-finance/3-9-procurement.qmd
    - part: "Human Resources"
      chapters:
        - policies/4-human-resources/4-1-employee-handbook.qmd
        - policies/4-human-resources/4-2-personnel-records.qmd
        - policies/4-human-resources/4-3-employee-search-selection.qmd
        - policies/4-human-resources/4-4-executive-director-evaluation.qmd
    - part: "Committee Procedures"
      chapters:
        - procedures/index.qmd
        - procedures/funding-friday.qmd
        - procedures/raskin-scholarship.qmd
        - procedures/martha-maiden-award.qmd
        - procedures/cpg-reporting.qmd
    - part: "Position Descriptions"
      chapters:
        - positions/executive-director.qmd
    - part: "Contributing"
      chapters:
        - contributing/index.qmd
        - contributing/deployment.qmd
        - contributing/template.qmd

format:
  html:
    theme: [cosmo, custom.scss]
    toc: true
```

- [ ] **Step 2: Create `custom.scss`**

```scss
/*-- scss:defaults --*/

/*
 * ESIP brand colors — extract from esipfed.org:
 *   1. Open https://www.esipfed.org in a browser
 *   2. Right-click → Inspect → Elements tab
 *   3. Look for :root { } block with CSS custom properties
 *   4. Replace the placeholder values below
 */

$primary:    #2c7be5;   /* placeholder — replace with ESIP primary brand color */
$link-color: #2c7be5;   /* placeholder — replace with ESIP link color */
$body-bg:    #ffffff;

/*-- scss:rules --*/
.sidebar-title {
  font-weight: 700;
}
```

- [ ] **Step 3: Create `index.qmd`**

```markdown
---
title: "ESIP Governance"
---

This resource contains the official governance documents for the Foundation for
Earth Science Information Partners (ESIP), including the bylaws, policies and
procedures, committee procedures, and position descriptions.

## How to use this resource

**Finding a document:** Use the sidebar on the left to browse by section, or use
the **search bar** (top-right) to search by keyword across all documents.

**Proposing a change:** See [How to Contribute](contributing/index.qmd) for how
to suggest edits or report issues — no Git knowledge required.

## Document sections

| Section | Description |
|---|---|
| [Bylaws](bylaws/index.qmd) | The foundational legal governing document of ESIP, restated December 2016 |
| [Corporate Policies](policies/index.qmd) | Organizational policies covering membership, structure, and operations |
| [Ethics & Conduct](policies/2-ethics-conduct/2-1-community-participation-guidelines.qmd) | Community guidelines, conflict of interest, and whistleblower policies |
| [Business & Finance](policies/3-business-finance/3-1-accounting.qmd) | Financial policies, accounting, procurement, and expense reimbursement |
| [Human Resources](policies/4-human-resources/4-1-employee-handbook.qmd) | HR policies including the employee handbook and search procedures |
| [Committee Procedures](procedures/index.qmd) | Award procedures and committee-specific rules |
| [Contributing](contributing/index.qmd) | How to propose changes or report issues |

## About this resource

This web book is maintained by the ESIP Governance Committee. To reach the
committee, email [governance@esipfed.org](mailto:governance@esipfed.org) or
[open an issue](https://github.com/ESIPFed/Governance/issues/new) on GitHub.
```

- [ ] **Step 4: Update `.gitignore`**

Open `.gitignore` and add `_book/` so local Quarto renders are not committed:

```
.superpowers/
_book/
```

- [ ] **Step 5: Verify Quarto config is valid**

```bash
quarto check
```

Expected: warnings about missing chapter files (those come in later tasks), but no fatal errors about the YAML structure itself. If you see a YAML parse error, fix the indentation in `_quarto.yml`.

- [ ] **Step 6: Commit scaffold**

```bash
git add _quarto.yml custom.scss index.qmd .gitignore
git commit -m "Add Quarto project scaffold (config, theme, landing page)"
```

---

## Task 4: Create Bylaws Directory and Index

**Files:**
- Create: `bylaws/index.qmd`

- [ ] **Step 1: Create bylaws/ directory and index**

```markdown
---
title: "Bylaws"
---

# Amended and Restated Bylaws of the Foundation for Earth Science Information Partners

**Restated as of December 2, 2016**

These bylaws govern the Foundation for Earth Science Information Partners (ESIP).
They are organized into eleven articles covering offices, purposes, membership,
directors, conduct, meetings, officers, committees, instruments, records, and
miscellaneous provisions.

Amendments to the bylaws require a two-thirds vote of the entire membership
present at a duly called meeting (see [Article 11.2](article-11-miscellaneous.qmd)).

## Articles

| Article | Title |
|---------|-------|
| [1](article-01-offices.qmd) | Offices |
| [2](article-02-purposes.qmd) | Purposes |
| [3](article-03-members.qmd) | Members |
| [4](article-04-directors.qmd) | Directors, Election and Removal |
| [5](article-05-director-conduct.qmd) | Director Duty of Care and Conduct |
| [6](article-06-board-meetings.qmd) | Meetings of the Board |
| [7](article-07-officers.qmd) | Officers |
| [8](article-08-committees.qmd) | Committees |
| [9](article-09-instruments.qmd) | Execution of Instruments, Deposits and Funds |
| [10](article-10-records.qmd) | Corporate Records, Reports and Seal |
| [11](article-11-miscellaneous.qmd) | Miscellaneous Provisions |
```

- [ ] **Step 2: Commit**

```bash
git add bylaws/index.qmd
git commit -m "Add bylaws section index"
```

---

## Task 5: Consolidate Bylaws Articles 1–4

**Files:**
- Create: `bylaws/article-01-offices.qmd`
- Create: `bylaws/article-02-purposes.qmd`
- Create: `bylaws/article-03-members.qmd`
- Create: `bylaws/article-04-directors.qmd`

The pattern for every bylaws article is identical: write a frontmatter header, then concatenate the source section files in numeric order. The source files use `## **section.number - TITLE**` headings — keep them exactly as-is.

- [ ] **Step 1: Consolidate Article 1 — Offices (2 sections)**

```bash
printf -- '---\ntitle: "Article 1: Offices"\n---\n\n' > bylaws/article-01-offices.qmd
cat "Bylaws/Article 01 Offices/1.01 Principal Office.md" >> bylaws/article-01-offices.qmd
printf '\n\n' >> bylaws/article-01-offices.qmd
cat "Bylaws/Article 01 Offices/1.02 Other Offices.md" >> bylaws/article-01-offices.qmd
```

- [ ] **Step 2: Verify Article 1**

```bash
head -5 bylaws/article-01-offices.qmd
grep -c "^##" bylaws/article-01-offices.qmd
```

Expected: frontmatter at top, count of `2`

- [ ] **Step 3: Consolidate Article 2 — Purposes (1 section)**

```bash
printf -- '---\ntitle: "Article 2: Purposes"\n---\n\n' > bylaws/article-02-purposes.qmd
cat "Bylaws/Article 02 Purposes/2.01 Objectives and Purposes.md" >> bylaws/article-02-purposes.qmd
```

- [ ] **Step 4: Consolidate Article 3 — Members (19 sections)**

```bash
printf -- '---\ntitle: "Article 3: Members"\n---\n\n' > bylaws/article-03-members.qmd
for f in "Bylaws/Article 03 Members/"*.md; do
  cat "$f" >> bylaws/article-03-members.qmd
  printf '\n\n' >> bylaws/article-03-members.qmd
done
```

- [ ] **Step 5: Verify Article 3**

```bash
grep -c "^##" bylaws/article-03-members.qmd
```

Expected: `19`

- [ ] **Step 6: Consolidate Article 4 — Directors (6 sections)**

```bash
printf -- '---\ntitle: "Article 4: Directors, Election and Removal"\n---\n\n' > bylaws/article-04-directors.qmd
for f in "Bylaws/Article 04 Directors Election and removal/"*.md; do
  cat "$f" >> bylaws/article-04-directors.qmd
  printf '\n\n' >> bylaws/article-04-directors.qmd
done
```

- [ ] **Step 7: Verify Article 4**

```bash
grep -c "^##" bylaws/article-04-directors.qmd
```

Expected: `6`

- [ ] **Step 8: Commit**

```bash
git add bylaws/article-01-offices.qmd bylaws/article-02-purposes.qmd \
        bylaws/article-03-members.qmd bylaws/article-04-directors.qmd
git commit -m "Consolidate bylaws articles 1-4"
```

---

## Task 6: Consolidate Bylaws Articles 5–11

**Files:**
- Create: `bylaws/article-05-director-conduct.qmd`
- Create: `bylaws/article-06-board-meetings.qmd`
- Create: `bylaws/article-07-officers.qmd`
- Create: `bylaws/article-08-committees.qmd`
- Create: `bylaws/article-09-instruments.qmd`
- Create: `bylaws/article-10-records.qmd`
- Create: `bylaws/article-11-miscellaneous.qmd`

- [ ] **Step 1: Consolidate Articles 5–11**

```bash
# Article 5 — Director Duty of Care and Conduct (9 sections)
printf -- '---\ntitle: "Article 5: Director Duty of Care and Conduct"\n---\n\n' \
  > bylaws/article-05-director-conduct.qmd
for f in "Bylaws/Article 05 Director duty of care and conduct/"*.md; do
  cat "$f" >> bylaws/article-05-director-conduct.qmd; printf '\n\n' >> bylaws/article-05-director-conduct.qmd
done

# Article 6 — Meetings of the Board (11 sections)
printf -- '---\ntitle: "Article 6: Meetings of the Board"\n---\n\n' \
  > bylaws/article-06-board-meetings.qmd
for f in "Bylaws/Article 06 Meetings of the Board/"*.md; do
  cat "$f" >> bylaws/article-06-board-meetings.qmd; printf '\n\n' >> bylaws/article-06-board-meetings.qmd
done

# Article 7 — Officers (10 sections)
printf -- '---\ntitle: "Article 7: Officers"\n---\n\n' \
  > bylaws/article-07-officers.qmd
for f in "Bylaws/Article 07 Officers/"*.md; do
  cat "$f" >> bylaws/article-07-officers.qmd; printf '\n\n' >> bylaws/article-07-officers.qmd
done

# Article 8 — Committees (3 sections)
printf -- '---\ntitle: "Article 8: Committees"\n---\n\n' \
  > bylaws/article-08-committees.qmd
for f in "Bylaws/Article 08 Committees/"*.md; do
  cat "$f" >> bylaws/article-08-committees.qmd; printf '\n\n' >> bylaws/article-08-committees.qmd
done

# Article 9 — Instruments (5 sections)
printf -- '---\ntitle: "Article 9: Execution of Instruments, Deposits and Funds"\n---\n\n' \
  > bylaws/article-09-instruments.qmd
for f in "Bylaws/Article 09 Execution of instruments, deposits and funds/"*.md; do
  cat "$f" >> bylaws/article-09-instruments.qmd; printf '\n\n' >> bylaws/article-09-instruments.qmd
done

# Article 10 — Records (5 sections)
printf -- '---\ntitle: "Article 10: Corporate Records, Reports and Seal"\n---\n\n' \
  > bylaws/article-10-records.qmd
for f in "Bylaws/Article 10 Corporate records, reports and seal/"*.md; do
  cat "$f" >> bylaws/article-10-records.qmd; printf '\n\n' >> bylaws/article-10-records.qmd
done

# Article 11 — Miscellaneous (4 sections)
printf -- '---\ntitle: "Article 11: Miscellaneous Provisions"\n---\n\n' \
  > bylaws/article-11-miscellaneous.qmd
for f in "Bylaws/Article 11 Miscellaneous provisions/"*.md; do
  cat "$f" >> bylaws/article-11-miscellaneous.qmd; printf '\n\n' >> bylaws/article-11-miscellaneous.qmd
done
```

- [ ] **Step 2: Verify section counts**

```bash
grep -c "^##" bylaws/article-05-director-conduct.qmd   # expect 9
grep -c "^##" bylaws/article-06-board-meetings.qmd      # expect 11
grep -c "^##" bylaws/article-07-officers.qmd            # expect 10
grep -c "^##" bylaws/article-08-committees.qmd          # expect 3
grep -c "^##" bylaws/article-09-instruments.qmd         # expect 5
grep -c "^##" bylaws/article-10-records.qmd             # expect 5
grep -c "^##" bylaws/article-11-miscellaneous.qmd       # expect 4
```

- [ ] **Step 3: Commit**

```bash
git add bylaws/
git commit -m "Consolidate bylaws articles 5-11 (75 files → 11)"
```

---

## Task 7: Migrate Policies — 1 Corporate

**Files:** Create 14 files in `policies/1-corporate/`

The migration pattern for every policy file is:
1. Write YAML frontmatter (`title`, `date`)
2. Append the source file content verbatim
3. For the `date` field: check the source file for an explicit approval date (e.g., "approved by the Board... on October 17, 2017"). If none found, use the file's last git commit date: `git log -1 --format="%as" -- "<source-file>"`

- [ ] **Step 1: Create policies/ directories**

```bash
mkdir -p policies/1-corporate policies/2-ethics-conduct \
         policies/3-business-finance policies/4-human-resources
```

- [ ] **Step 2: Migrate 1.0 Definitions**

The Definitions file is a draft (audit finding A-03). Add a callout box noting the draft status.

```bash
cat > policies/1-corporate/1-0-definitions.qmd << 'EOF'
---
title: "1.0 Definitions"
---

::: {.callout-warning}
This document has not yet been approved by the Board of Directors of ESIP. It is included here for reference. Contact [governance@esipfed.org](mailto:governance@esipfed.org) for the current status.
:::

EOF
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.0 Definitions.md" \
  >> policies/1-corporate/1-0-definitions.qmd
```

- [ ] **Step 3: Migrate remaining Corporate policies**

For each file below, run the same two-step pattern (write frontmatter, append source). Fill in the `date` from the source file or git log.

```bash
# 1.1 Goals — approved October 17, 2017
printf -- '---\ntitle: "1.1 Goals"\ndate: 2017-10-17\n---\n\n' \
  > policies/1-corporate/1-1-goals.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.1 Goals.md" \
  >> policies/1-corporate/1-1-goals.qmd

# 1.2 Partners and Partner Organizations
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.2 Partners and Partner Organizations.md")
printf -- "---\ntitle: \"1.2 Partners and Partner Organizations\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-2-partners.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.2 Partners and Partner Organizations.md" \
  >> policies/1-corporate/1-2-partners.qmd

# 1.2A Nonvoting Associates
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.2A Nonvoting Associates.md")
printf -- "---\ntitle: \"1.2A Nonvoting Associates\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-2a-nonvoting-associates.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.2A Nonvoting Associates.md" \
  >> policies/1-corporate/1-2a-nonvoting-associates.qmd

# 1.3 Corporate Organization
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.3 Corporate Organization.md")
printf -- "---\ntitle: \"1.3 Corporate Organization\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-3-corporate-organization.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.3 Corporate Organization.md" \
  >> policies/1-corporate/1-3-corporate-organization.qmd

# 1.3A Board and Program Committee Participation and Attendance
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.3A Board and Program Committee  Participation and Attendance.md")
printf -- "---\ntitle: \"1.3A Board and Program Committee Participation and Attendance\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-3a-board-participation.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.3A Board and Program Committee  Participation and Attendance.md" \
  >> policies/1-corporate/1-3a-board-participation.qmd

# 1.4 Policy Approval, Amendments, Administration and Compliance
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.4 Policy Approval, Amendments, Administration and Compliance.md")
printf -- "---\ntitle: \"1.4 Policy Approval, Amendments, Administration and Compliance\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-4-policy-approval.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.4 Policy Approval, Amendments, Administration and Compliance.md" \
  >> policies/1-corporate/1-4-policy-approval.qmd

# 1.5 Equal Opportunity
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.5 Equal Opportunity.md")
printf -- "---\ntitle: \"1.5 Equal Employment and Volunteer Opportunity\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-5-equal-opportunity.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.5 Equal Opportunity.md" \
  >> policies/1-corporate/1-5-equal-opportunity.qmd

# 1.6 Record Maintenance
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.6 Record Maintenance Policy.md")
printf -- "---\ntitle: \"1.6 Record Maintenance\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-6-record-maintenance.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.6 Record Maintenance Policy.md" \
  >> policies/1-corporate/1-6-record-maintenance.qmd

# 1.7 Endorsements
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.7 Endorsements.md")
printf -- "---\ntitle: \"1.7 Endorsements\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-7-endorsements.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.7 Endorsements.md" \
  >> policies/1-corporate/1-7-endorsements.qmd

# 1.8 Use of the ESIP Logo
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.8 Use of the ESIP Logo.md")
printf -- "---\ntitle: \"1.8 Use of the ESIP Logo\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-8-logo-use.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.8 Use of the ESIP Logo.md" \
  >> policies/1-corporate/1-8-logo-use.qmd

# 1.9 Data Privacy
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.9 Data Privacy Policy.md")
printf -- "---\ntitle: \"1.9 Data Privacy Policy\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-9-data-privacy.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.9 Data Privacy Policy.md" \
  >> policies/1-corporate/1-9-data-privacy.qmd

# 1.10 Memoranda of Understanding
DATE=$(git log -1 --format="%as" -- "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.10 Memoranda of Understanding.md")
printf -- "---\ntitle: \"1.10 Memoranda of Understanding\"\ndate: $DATE\n---\n\n" \
  > policies/1-corporate/1-10-memoranda-of-understanding.qmd
cat "ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.10 Memoranda of Understanding.md" \
  >> policies/1-corporate/1-10-memoranda-of-understanding.qmd
```

- [ ] **Step 4: Verify file count**

```bash
ls policies/1-corporate/ | wc -l
```

Expected: `14`

- [ ] **Step 5: Commit**

```bash
git add policies/1-corporate/
git commit -m "Migrate 1.0 Corporate policies (14 files)"
```

---

## Task 8: Migrate Policies — 2 Ethics & Conduct, 3 Business & Finance, 4 Human Resources

**Files:** Create 5 + 14 + 4 = 23 files

- [ ] **Step 1: Migrate 2.0 Ethics & Conduct (5 files)**

```bash
for pair in \
  "2-1-community-participation-guidelines.qmd|2.0 Ethics and Conduct/ESIP P&P 2.1 Community Participation Guidelines.md|2.1 Community Participation Guidelines" \
  "2-2-conflict-of-interest.qmd|2.0 Ethics and Conduct/ESIP P&P 2.2 Conflict Of Interest.md|2.2 Conflict of Interest" \
  "2-3-gift-acceptance.qmd|2.0 Ethics and Conduct/ESIP P&P 2.3 Gift Acceptance Policy.md|2.3 Gift Acceptance Policy" \
  "2-4-fundraising.qmd|2.0 Ethics and Conduct/ESIP P&P 2.4 Fundraising and Proposal Development Policy.md|2.4 Fundraising and Proposal Development" \
  "2-5-whistleblower.qmd|2.0 Ethics and Conduct/ESIP P&P 2.5 Whistleblower Policy.md|2.5 Whistleblower Policy"
do
  dest=$(echo "$pair" | cut -d'|' -f1)
  src="ESIP Policies and Procedures/$(echo "$pair" | cut -d'|' -f2)"
  title=$(echo "$pair" | cut -d'|' -f3)
  date=$(git log -1 --format="%as" -- "$src")
  printf -- "---\ntitle: \"$title\"\ndate: $date\n---\n\n" > "policies/2-ethics-conduct/$dest"
  cat "$src" >> "policies/2-ethics-conduct/$dest"
done
```

- [ ] **Step 2: Verify**

```bash
ls policies/2-ethics-conduct/ | wc -l
```

Expected: `5`

- [ ] **Step 3: Migrate 3.0 Business & Finance (14 files)**

```bash
BASE="ESIP Policies and Procedures/3.0 Business and Finance"

for pair in \
  "3-1-accounting.qmd|ESIP P&P 3.1 Accounting Policies and Procedures.md|3.1 Accounting Policies and Procedures" \
  "3-2-internal-controls.qmd|ESIP P&P 3.2 Internal Control Policies and Procedures.md|3.2 Internal Control Policies and Procedures" \
  "3-3-financial-planning.qmd|ESIP P&P 3.3 Financial Planning and Reporting Policies.md|3.3 Financial Planning and Reporting" \
  "3-3a-ficom-budget-cycle.qmd|ESIP P&P 3.3A FiCom annual budget cycle.md|3.3A FiCom Annual Budget Cycle" \
  "3-3f-committee-budget-request.qmd|ESIP P&P 3.3F ESIP Committee Budget Request Policy.md|3.3F Committee Budget Request Policy" \
  "3-4-revenue-accounts-receivable.qmd|ESIP P&P 3.4 Revenue and Accounts Receivables Policies.md|3.4 Revenue and Accounts Receivable" \
  "3-5-expenses-accounts-payable.qmd|ESIP P&P 3.5 Expenses and Accounts Payable Policies.md|3.5 Expenses and Accounts Payable" \
  "3-5a-travel-expense.qmd|ESIP P&P 3.5A Travel and Expense Reimbursement Policy.md|3.5A Travel and Expense Reimbursement" \
  "3-5b-complimentary-registration.qmd|ESIP P&P 3.5B Complimentary Registration Fee Policy.md|3.5B Complimentary Meeting Registration" \
  "3-5c-credit-card-points.qmd|ESIP P&P 3.5C Use of Credit Card Points.md|3.5C Use of Credit Card Points" \
  "3-6-asset-management.qmd|ESIP P&P 3.6 Asset Management Policies.md|3.6 Asset Management" \
  "3-7-pass-through-funding.qmd|ESIP P&P 3.7 Pass-Through Funding.md|3.7 Pass-Through Funding" \
  "3-8-gift-issuance.qmd|ESIP P&P 3.8 Gift Issuance.md|3.8 Gift Issuance" \
  "3-9-procurement.qmd|ESIP P&P 3.9 Procurement Policies and Procedures.md|3.9 Procurement Policies and Procedures"
do
  dest=$(echo "$pair" | cut -d'|' -f1)
  src="$BASE/$(echo "$pair" | cut -d'|' -f2)"
  title=$(echo "$pair" | cut -d'|' -f3)
  date=$(git log -1 --format="%as" -- "$src")
  printf -- "---\ntitle: \"$title\"\ndate: $date\n---\n\n" > "policies/3-business-finance/$dest"
  cat "$src" >> "policies/3-business-finance/$dest"
done
```

- [ ] **Step 4: Verify**

```bash
ls policies/3-business-finance/ | wc -l
```

Expected: `14`

- [ ] **Step 5: Migrate 4.0 Human Resources (4 files)**

```bash
BASE="ESIP Policies and Procedures/4.0 Human Resources"

for pair in \
  "4-1-employee-handbook.qmd|ESIP P&P 4.1 Employee Handbook.md|4.1 Employee Handbook" \
  "4-2-personnel-records.qmd|ESIP P&P 4.2 Handling of Employee and Volunteer Records Policy.md|4.2 Handling of Employee and Volunteer Personnel Records" \
  "4-3-employee-search-selection.qmd|ESIP P&P 4.3 Employee Search and Selection Policy.md|4.3 Employee Search and Selection" \
  "4-4-executive-director-evaluation.qmd|ESIP P&P 4.4 Executive Director Evaluation Policy.md|4.4 Executive Director Evaluation"
do
  dest=$(echo "$pair" | cut -d'|' -f1)
  src="$BASE/$(echo "$pair" | cut -d'|' -f2)"
  title=$(echo "$pair" | cut -d'|' -f3)
  date=$(git log -1 --format="%as" -- "$src")
  printf -- "---\ntitle: \"$title\"\ndate: $date\n---\n\n" > "policies/4-human-resources/$dest"
  cat "$src" >> "policies/4-human-resources/$dest"
done
```

- [ ] **Step 6: Verify**

```bash
ls policies/4-human-resources/ | wc -l
```

Expected: `4`

- [ ] **Step 7: Create policies/index.qmd**

```markdown
---
title: "Policies & Procedures"
---

# ESIP Policies and Procedures

**Approved by the ESIP Board, October 2017. Last updated April 2025.**

These policies and procedures govern ESIP's organizational operations across four
areas. Use the sidebar or the table below to navigate to a specific policy.

| Section | Policies |
|---------|---------|
| [1. Corporate](1-corporate/1-1-goals.qmd) | Goals, membership, corporate organization, record maintenance, privacy |
| [2. Ethics & Conduct](2-ethics-conduct/2-1-community-participation-guidelines.qmd) | Community guidelines, conflict of interest, gift acceptance, whistleblower |
| [3. Business & Finance](3-business-finance/3-1-accounting.qmd) | Accounting, financial planning, expense reimbursement, procurement |
| [4. Human Resources](4-human-resources/4-1-employee-handbook.qmd) | Employee handbook, personnel records, search and selection |
```

- [ ] **Step 8: Commit**

```bash
git add policies/
git commit -m "Migrate all Policies & Procedures (33 files)"
```

---

## Task 9: Migrate Procedures and Positions

**Files:**
- Create: `procedures/index.qmd`
- Create: `procedures/funding-friday.qmd`
- Create: `procedures/raskin-scholarship.qmd`
- Create: `procedures/martha-maiden-award.qmd`
- Create: `procedures/cpg-reporting.qmd`
- Create: `positions/executive-director.qmd`

- [ ] **Step 1: Create procedures/ directory and files**

```bash
mkdir -p procedures positions

# procedures/index.qmd
cat > procedures/index.qmd << 'EOF'
---
title: "Committee Procedures"
---

These procedures govern ESIP standing committees, awards, and community
participation processes.

| Procedure | Description |
|-----------|-------------|
| [FUNding Friday Rules](funding-friday.qmd) | Annual mini-grant competition rules |
| [Raskin Scholarship](raskin-scholarship.qmd) | Student scholarship procedures |
| [Martha Maiden Award](martha-maiden-award.qmd) | Annual recognition award procedures |
| [CPG Reporting](cpg-reporting.qmd) | Community Participation Guidelines reporting guidance |
EOF

# Migrate the four procedure files
for pair in \
  "funding-friday.qmd|Standing Committee and Cluster Policies and Procedures/Funding Friday Rules.md|FUNding Friday Rules" \
  "raskin-scholarship.qmd|Standing Committee and Cluster Policies and Procedures/Raskin Scholarship Procedure.md|Raskin Scholarship Procedure" \
  "martha-maiden-award.qmd|Standing Committee and Cluster Policies and Procedures/Martha Maiden Award Procedures.md|Martha Maiden Award Procedures" \
  "cpg-reporting.qmd|Standing Committee and Cluster Policies and Procedures/Community Participation Guidelines (CPG) Reporting - Additional Information.md|CPG Reporting — Additional Information"
do
  dest=$(echo "$pair" | cut -d'|' -f1)
  src=$(echo "$pair" | cut -d'|' -f2)
  title=$(echo "$pair" | cut -d'|' -f3)
  date=$(git log -1 --format="%as" -- "$src")
  printf -- "---\ntitle: \"$title\"\ndate: $date\n---\n\n" > "procedures/$dest"
  cat "$src" >> "procedures/$dest"
done
```

- [ ] **Step 2: Verify procedures**

```bash
ls procedures/
```

Expected: `cpg-reporting.qmd  funding-friday.qmd  index.qmd  martha-maiden-award.qmd  raskin-scholarship.qmd`

- [ ] **Step 3: Migrate position description**

```bash
DATE=$(git log -1 --format="%as" -- "Position Descriptions/ESIP Executive Director Position Description.md")
printf -- "---\ntitle: \"Executive Director Position Description\"\ndate: $DATE\n---\n\n" \
  > positions/executive-director.qmd
cat "Position Descriptions/ESIP Executive Director Position Description.md" \
  >> positions/executive-director.qmd
```

- [ ] **Step 4: Commit**

```bash
git add procedures/ positions/
git commit -m "Migrate committee procedures and position descriptions"
```

---

## Task 10: Create Contributing Section

**Files:**
- Create: `contributing/index.qmd`
- Create: `contributing/deployment.qmd`
- Create: `contributing/template.qmd`

- [ ] **Step 1: Create `contributing/index.qmd`**

```bash
mkdir -p contributing
cat > contributing/index.qmd << 'EOF'
---
title: "How to Contribute"
---

Changes to ESIP governance documents are proposed through GitHub. There are two
paths depending on your comfort with GitHub.

## Path 1 — Edit in the browser (recommended for board members)

No GitHub account setup or Git knowledge required.

1. Find the page you want to edit in the web book.
2. Click **Edit this page** (top-right corner of every page).
3. GitHub opens the source file in its web editor.
4. Make your changes directly in the browser.
5. Scroll down and click **Propose changes**.
6. GitHub creates a pull request automatically — staff will review and merge it.

## Path 2 — Pull request (for staff)

Standard GitHub workflow for larger changes:

1. Create a branch from `master`.
2. Edit `.qmd` files locally or in the GitHub interface.
3. Open a pull request with a description of what changed and why.
4. A reviewer merges after approval.

## Review and approval rules

| Change type | Who can approve |
|---|---|
| Typo, formatting, broken link | Staff (single reviewer) |
| Wording clarification, date update | Staff (single reviewer) |
| Policy content change | Board approval required before merge |
| New policy or procedure | Board approval required before merge |
| Structural or navigation changes | Staff lead + one other reviewer |

## Reporting an issue without editing

Click **Report an issue** (top-right on any page) to open a pre-filled GitHub
Issue. Staff will triage and make the fix. No edits required on your part.

## Questions

Email [governance@esipfed.org](mailto:governance@esipfed.org) or
[open an issue](https://github.com/ESIPFed/Governance/issues/new).
EOF
```

- [ ] **Step 2: Create `contributing/deployment.qmd`**

```bash
cat > contributing/deployment.qmd << 'EOF'
---
title: "How Publishing Works"
---

This page explains what happens automatically when a change is merged into the
`master` branch of the repository.

## The publishing pipeline

Every merge to `master` triggers the following sequence automatically — no one
needs to run any commands:

1. **GitHub receives the merge.** The push to `master` triggers a GitHub Actions
   workflow defined in `.github/workflows/publish.yml`.

2. **A virtual machine starts.** GitHub spins up a fresh Ubuntu environment in
   the cloud. This takes about 30 seconds.

3. **Quarto is installed on the VM.** The workflow installs Quarto automatically.
   This happens every run — the VM starts fresh each time.

4. **`quarto render` runs.** Quarto reads `_quarto.yml`, processes all `.qmd`
   files listed under `book.chapters`, and generates HTML output.

5. **The output is published to the `gh-pages` branch.** The rendered site is
   pushed to a special `gh-pages` branch in this repository. Only the built
   output lives there — not the source files.

6. **GitHub Pages serves the updated site.** GitHub detects the push to
   `gh-pages` and updates the live site, usually within 60 seconds.

The full pipeline takes about 2–3 minutes from merge to live.

## Checking if a build succeeded

1. Go to the repository on GitHub.
2. Click the **Actions** tab.
3. Find the most recent workflow run ("Quarto Publish").
4. A green checkmark means the site updated successfully.
5. A red X means something failed — click the run to see the error log.

## What to do if a build fails

1. Click the failed run in the Actions tab to read the error.
2. Common causes: a `.qmd` file listed in `_quarto.yml` doesn't exist yet, or
   there's a YAML syntax error in frontmatter.
3. Fix the issue in a new commit — the workflow re-runs automatically on push.
4. If you can't diagnose the error, email
   [governance@esipfed.org](mailto:governance@esipfed.org).

## Previewing changes locally (optional)

If you have Quarto installed on your machine, you can preview changes before
opening a pull request:

```bash
# Install Quarto: https://quarto.org/docs/get-started/
quarto preview
```

This opens a live-reloading browser preview at `http://localhost:4567`. Changes
you save to any `.qmd` file appear in the browser immediately.
EOF
```

- [ ] **Step 3: Create `contributing/template.qmd`**

```bash
cat > contributing/template.qmd << 'EOF'
---
title: "Policy/Procedure Template"
---

*This is a blank template for drafting new ESIP policies or procedures.
Copy this file, fill in the sections, and open a pull request.*

---

**Policy and Procedure X.X — [Policy Title]**

**Proposed by:** [Name / Committee]
**Date proposed:** [YYYY-MM-DD]
**Status:** Draft — pending board approval

---

## Section 1 — Purpose

[Describe the purpose of this policy in one to three sentences.]

## Section 2 — Scope

[Describe who this policy applies to.]

## Section 3 — Policy

[State the policy requirements clearly, using numbered subsections (3.1, 3.2, …).]

3.1 [First requirement.]

3.2 [Second requirement.]

## Section 4 — Procedures

[Optional: describe step-by-step procedures for implementing the policy.]

## Section 5 — Exceptions

[Optional: describe any exceptions to the policy.]

---

*This policy was approved by the ESIP Board of Directors on [date].*
EOF
```

- [ ] **Step 4: Commit**

```bash
git add contributing/
git commit -m "Add contributing section (how-to guide, deployment docs, template)"
```

---

## Task 11: Set Up GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/publish.yml`

- [ ] **Step 1: Create workflow directory and file**

```bash
mkdir -p .github/workflows
cat > .github/workflows/publish.yml << 'EOF'
name: Quarto Publish

on:
  push:
    branches: [master]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render and publish to GitHub Pages
        uses: quarto-dev/quarto-actions/publish@v2
        with:
          target: gh-pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF
```

- [ ] **Step 2: Commit workflow**

```bash
git add .github/workflows/publish.yml
git commit -m "Add GitHub Actions workflow for Quarto publish to GitHub Pages"
```

---

## Task 12: First Render Verification

**Files:** none (verification only)

- [ ] **Step 1: Run local render**

```bash
quarto render
```

Expected: Quarto processes all chapters, outputs HTML to `_book/`. Watch for any errors — the most common are missing files (chapter listed in `_quarto.yml` but not yet created) or frontmatter YAML syntax errors.

- [ ] **Step 2: Verify output exists**

```bash
ls _book/
```

Expected: `index.html`, `search.json`, `bylaws/`, `policies/`, `procedures/`, `positions/`, `contributing/`, and supporting assets.

- [ ] **Step 3: Spot-check a rendered page**

```bash
open _book/index.html
# or: python3 -m http.server 8000 -d _book/
```

Verify: landing page loads, sidebar shows all sections, search bar is visible, "Edit this page" link appears on each content page.

- [ ] **Step 4: Check that _book/ is gitignored**

```bash
git status
```

Confirm `_book/` does NOT appear in the output. If it does, verify `.gitignore` contains `_book/`.

- [ ] **Step 5: Commit any render fixes**

If any chapters were missing or had frontmatter errors, fix them and commit:

```bash
git add [fixed files]
git commit -m "Fix render errors found in first local build"
```

---

## Task 13: Update README and Clean Up Old Structure

**Files:**
- Modify: `README.md`
- Delete: `Bylaws/` directory
- Delete: `ESIP Policies and Procedures/` directory
- Delete: `Standing Committee and Cluster Policies and Procedures/` directory
- Delete: `Position Descriptions/` directory

- [ ] **Step 1: Update README.md**

Replace the entire contents of `README.md`:

```markdown
# ESIP Governance

Official governance documents for the [Earth Science Information Partners](https://www.esipfed.org) (ESIP).

**→ [Browse the Governance Web Book](https://esipfed.github.io/Governance/)**

The web book includes the ESIP Bylaws, all Policies & Procedures, committee procedures,
and position descriptions — with full-text search and an "Edit this page" link on every page.

## Contributing

To propose a change or report an issue, see the
[Contributing guide](https://esipfed.github.io/Governance/contributing/index.html)
in the web book. No Git knowledge required for simple edits.

## Repository maintenance

Questions? Email [governance@esipfed.org](mailto:governance@esipfed.org) or
[open an issue](https://github.com/ESIPFed/Governance/issues/new).

[![DOI](https://zenodo.org/badge/41741549.svg)](https://zenodo.org/badge/latestdoi/41741549)
```

- [ ] **Step 2: Verify all content has been migrated before deleting**

```bash
# Count source files remaining vs. migrated files
find "Bylaws" "ESIP Policies and Procedures" \
     "Standing Committee and Cluster Policies and Procedures" \
     "Position Descriptions" -name "*.md" 2>/dev/null | wc -l

find bylaws policies procedures positions -name "*.qmd" | wc -l
```

The second count should equal or exceed the first (allowing for consolidations). If the first number is unexpectedly high, investigate before deleting.

- [ ] **Step 3: Remove old directory structure**

```bash
git rm -r "Bylaws/" \
          "ESIP Policies and Procedures/" \
          "Standing Committee and Cluster Policies and Procedures/" \
          "Position Descriptions/"
```

- [ ] **Step 4: Verify only expected files remain untracked**

```bash
git status
```

Expected: only `Assembly Notes/` remains untouched (it contains a single non-markdown archive file and is out of scope).

- [ ] **Step 5: Commit cleanup**

```bash
git add README.md
git commit -m "Remove legacy directory structure; update README to point to web book"
```

---

## Task 14: Enable GitHub Pages and Verify Deployment

**Files:** none (GitHub settings + push verification)

- [ ] **Step 1: Push all commits to remote**

```bash
git push origin master
```

- [ ] **Step 2: Watch the Actions run**

1. Go to `https://github.com/ESIPFed/Governance/actions`
2. Find the "Quarto Publish" workflow run triggered by the push
3. Wait for it to complete (typically 2–4 minutes)
4. Confirm green checkmark

- [ ] **Step 3: Enable GitHub Pages (one-time setup, requires admin access)**

1. Go to `https://github.com/ESIPFed/Governance/settings/pages`
2. Under "Source", select **Deploy from a branch**
3. Branch: `gh-pages`, Folder: `/ (root)`
4. Click **Save**

This step only needs to be done once. After the first successful Actions run, the `gh-pages` branch exists and Pages can be pointed at it.

- [ ] **Step 4: Verify the live site**

Visit `https://esipfed.github.io/Governance/` (allow ~2 minutes after Pages is enabled for the first deploy).

Verify:
- Landing page loads
- Sidebar shows all sections (Bylaws, Corporate Policies, Ethics & Conduct, Business & Finance, Human Resources, Committee Procedures, Position Descriptions, Contributing)
- Search bar works — type "conflict of interest" and verify it finds the right policy
- "Edit this page" link on any page opens the correct `.qmd` file in GitHub's editor
- "Report an issue" link opens a new GitHub issue

- [ ] **Step 5: Apply ESIP brand colors to `custom.scss`**

Open `https://www.esipfed.org` in a browser. Open DevTools (right-click → Inspect → Elements). Look for `:root { }` CSS variables. Update `custom.scss`:

```scss
/*-- scss:defaults --*/
$primary:    #ACTUAL_HEX;   /* replace with ESIP primary brand color */
$link-color: #ACTUAL_HEX;   /* replace with ESIP link color */
$body-bg:    #ffffff;
```

Commit and push to trigger a rebuild:

```bash
git add custom.scss
git commit -m "Apply ESIP brand colors"
git push origin master
```

---

## Self-Review

### Spec coverage check

| Spec requirement | Covered by task |
|---|---|
| Content audit with audit-report.md | Task 1 |
| All audit findings addressed (broken MoU link, missing 3.3A, draft definition flag) | Tasks 1, 7, 8 |
| Bylaws consolidated from ~70 files to 11 | Tasks 5, 6 |
| Folders renamed to lowercase-with-hyphens | Tasks 5–9 |
| YAML frontmatter on every .qmd file | Tasks 5–10 |
| `_quarto.yml` with always-expanded sidebar | Task 3 |
| Full-text search | Task 3 (`search: true`) |
| "Edit this page" and "Report an issue" buttons | Task 3 (`repo-actions`) |
| cosmo theme + custom.scss for ESIP branding | Tasks 3, 14 |
| GitHub Actions publish workflow | Task 11 |
| GitHub Pages one-time setup documented | Task 14 |
| contributing/index.qmd with two paths | Task 10 |
| contributing/deployment.qmd plain-language CI/CD explanation | Task 10 |
| contributing/template.qmd | Task 10 |
| Review/approval rules table | Task 10 |
| Old structure removed after migration | Task 13 |
| README updated to point to web book | Task 13 |
| Assembly Notes left in place (out of scope) | Task 13 |
| output-dir conflict with docs/ resolved using _book/ | Tasks 3, 12 |

All spec requirements are covered. No gaps found.
