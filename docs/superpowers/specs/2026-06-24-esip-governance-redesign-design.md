# ESIP Governance Repository Redesign — Design Spec

**Date:** 2026-06-24
**Author:** Aaron Friesz (amfriesz)
**Status:** Approved — ready for implementation planning

---

## Overview

The ESIP Governance repository holds all bylaws, policies, procedures, and position descriptions for the Foundation for Earth Science Information Partners. The primary users are ESIP Staff and Board Members. The core problem is findability: documents are hard to locate, links are fragile, and there is no searchable web-facing interface.

This spec covers five sequential phases:

1. **Content audit** — systematic review of all documents for discrepancies, broken links, and gaps
2. **Repository reorganization** — restructure files and folders for clean URLs and logical grouping
3. **Quarto web book** — configure the book, navigation, theme, and search
4. **Deployment** — GitHub Actions CI/CD pipeline publishing to GitHub Pages automatically on merge
5. **Contribution workflow** — documented paths for staff and board members to propose and review changes

---

## Phase 1: Content Audit

### Goal

Produce an `audit-report.md` that documents every issue found across all repository files before any reorganization begins. This file is excluded from the Quarto web book — it is a staff working document.

### What the audit checks

| Category | What to look for |
|---|---|
| Broken links | Hardcoded GitHub URLs pointing to forks, renamed files, or raw blob paths |
| Index gaps | Files that exist in the repo but are absent from any readme or navigation |
| Draft / unapproved documents | Content explicitly flagged as not board-approved |
| Cross-document conflicts | Same term defined differently across Bylaws and P&P |
| Stale dates | Approval or revision dates inconsistent with recent git history |
| Numbering inconsistencies | Section references that don't match the actual file structure |
| Orphaned files | Files with no inbound links from any index or nav |
| Formatting inconsistencies | Mixed bold/header conventions, inconsistent title casing |

### Issues already identified

The following issues were found during the design phase and should be addressed in the audit report:

| Severity | Location | Issue |
|---|---|---|
| `fix` | `ESIP Policies and Procedures/readme.md` | Link to P&P 1.10 MoU points to `BenGalewsky/Governance` fork, not the canonical `ESIPFed/Governance` repo |
| `fix` | `ESIP Policies and Procedures/readme.md` | `3.3A FiCom annual budget cycle.md` exists in the repo but is missing from the P&P index |
| `review` | `ESIP P&P 1.0 Definitions.md` | Document explicitly states "not yet approved by the Board of Directors of ESIP" — needs board decision on status |
| `note` | `Bylaws/readme.md` | States "Restated as of December 02, 2016" with no subsequent amendment dates noted |
| `fix` | All readme files | All navigation links are hardcoded GitHub blob URLs that will break if the repo is renamed or moved |

### Audit report format

Each finding is recorded with:
- **Severity:** `fix` (address during implementation), `review` (needs staff/board decision), or `note` (informational)
- **Location:** file path
- **Issue:** plain-language description
- **Recommended action:** what to do

The audit runs as a distinct step before any files are renamed or moved.

---

## Phase 2: Repository Reorganization

### Design approach (Option B — Moderate restructure)

Consolidate the Bylaws from ~70 tiny per-section files into 11 article files. Rename all folders to lowercase-with-hyphens for clean URLs. Add YAML frontmatter to every document. Fix all issues identified in the audit.

### Target file structure

```
Governance/
├── _quarto.yml                    ← Quarto config + navigation
├── index.qmd                      ← Landing page (replaces README as entry point)
├── README.md                      ← Short GitHub landing page linking to web book
├── .gitignore                     ← Excludes .superpowers/, docs/ (generated output)
├── docs/                          ← Quarto build output (served by GitHub Pages)
│
├── bylaws/
│   ├── index.qmd                  ← Bylaws overview + amendment history
│   ├── article-01-offices.qmd
│   ├── article-02-purposes.qmd
│   ├── article-03-members.qmd
│   ├── article-04-directors.qmd
│   ├── article-05-director-conduct.qmd
│   ├── article-06-board-meetings.qmd
│   ├── article-07-officers.qmd
│   ├── article-08-committees.qmd
│   ├── article-09-instruments.qmd
│   ├── article-10-records.qmd
│   └── article-11-miscellaneous.qmd
│
├── policies/
│   ├── index.qmd                  ← P&P overview
│   ├── 1-corporate/
│   │   ├── 1-0-definitions.qmd
│   │   ├── 1-1-goals.qmd
│   │   ├── 1-2-partners.qmd
│   │   ├── 1-2a-nonvoting-associates.qmd
│   │   ├── 1-3-corporate-organization.qmd
│   │   ├── 1-3a-board-participation.qmd
│   │   ├── 1-4-policy-approval.qmd
│   │   ├── 1-5-equal-opportunity.qmd
│   │   ├── 1-6-record-maintenance.qmd
│   │   ├── 1-7-endorsements.qmd
│   │   ├── 1-8-logo-use.qmd
│   │   ├── 1-9-data-privacy.qmd
│   │   └── 1-10-memoranda-of-understanding.qmd
│   ├── 2-ethics-conduct/
│   │   ├── 2-1-community-participation-guidelines.qmd
│   │   ├── 2-2-conflict-of-interest.qmd
│   │   ├── 2-3-gift-acceptance.qmd
│   │   ├── 2-4-fundraising.qmd
│   │   └── 2-5-whistleblower.qmd
│   ├── 3-business-finance/
│   │   ├── 3-1-accounting.qmd
│   │   ├── 3-2-internal-controls.qmd
│   │   ├── 3-3-financial-planning.qmd
│   │   ├── 3-3a-ficom-budget-cycle.qmd
│   │   ├── 3-3f-committee-budget-request.qmd
│   │   ├── 3-4-revenue-accounts-receivable.qmd
│   │   ├── 3-5-expenses-accounts-payable.qmd
│   │   ├── 3-5a-travel-expense.qmd
│   │   ├── 3-5b-complimentary-registration.qmd
│   │   ├── 3-5c-credit-card-points.qmd
│   │   ├── 3-6-asset-management.qmd
│   │   ├── 3-7-pass-through-funding.qmd
│   │   ├── 3-8-gift-issuance.qmd
│   │   └── 3-9-procurement.qmd
│   └── 4-human-resources/
│       ├── 4-1-employee-handbook.qmd
│       ├── 4-2-personnel-records.qmd
│       ├── 4-3-employee-search-selection.qmd
│       └── 4-4-executive-director-evaluation.qmd
│
├── procedures/
│   ├── index.qmd
│   ├── funding-friday.qmd
│   ├── raskin-scholarship.qmd
│   ├── martha-maiden-award.qmd
│   └── cpg-reporting.qmd
│
├── positions/
│   └── executive-director.qmd
│
└── contributing/
    ├── index.qmd                  ← How to propose changes (two paths)
    ├── deployment.qmd             ← How publishing works (plain-language CI/CD explanation)
    └── template.qmd               ← Policy/procedure template
```

### Key reorganization decisions

- **Bylaws consolidate** from ~70 individual section files into 11 article files (one per Article). Each article file contains all its sections. This preserves the full content while making navigation manageable.
- **Folder names** use lowercase-with-hyphens. No spaces in paths = clean, stable URLs.
- **`.qmd` extension** replaces `.md`. Content is identical; the extension signals Quarto-awareness and enables YAML frontmatter processing.
- **`procedures/`** replaces `Standing Committee and Cluster Policies and Procedures/` — shorter, accurate, URL-safe.
- **`contributing/`** is new — houses the contribution guide, deployment documentation, and policy template.
- **`3.3A FiCom budget cycle`** is added to the navigation (currently orphaned — missing from the P&P index).
- **Old folder structure** is removed after content migration is verified. Git history preserves the full record.

### YAML frontmatter standard

Every `.qmd` file gets consistent frontmatter:

```yaml
---
title: "3.1 Accounting Policies and Procedures"
date: 2024-03-15        # last board approval date
---
```

---

## Phase 3: Quarto Web Book

### Configuration (`_quarto.yml`)

```yaml
project:
  type: book
  output-dir: docs

book:
  title: "ESIP Governance"
  sidebar:
    style: "docked"
    collapse-level: 1        # increase to 2 later to enable section collapsing
  search: true
  repo-url: https://github.com/ESIPFed/Governance
  repo-actions: [edit, issue]

format:
  html:
    theme: [cosmo, custom.scss]
    toc: true
```

### Navigation layout

Always-expanded full outline (Option B). All sections visible in the sidebar without clicking to expand. The `collapse-level: 1` setting can be changed to `2` in a single line to enable collapsible sections if the board requests it later.

### Theme and branding

Base theme: `cosmo` (clean, professional, readable). ESIP brand colors are applied via `custom.scss`:

```scss
/*-- scss:defaults --*/
$primary:    #XXXXXX;   /* extract from esipfed.org via browser DevTools */
$link-color: #XXXXXX;
$body-bg:    #FFFFFF;
```

**Implementation task:** Open [esipfed.org](https://www.esipfed.org) in a browser, open DevTools (right-click → Inspect → Elements), and look for CSS color variables at the `:root` level. Copy hex values into `custom.scss`. The web book is functional with `cosmo` defaults from day one and can be branded once colors are confirmed.

### Key features

- **Full-text search** — Quarto builds a search index at render time. Users can search any term (e.g., "conflict of interest", "quorum") and land directly on the right section. No external service required.
- **"Edit this page" button** — every page has a link that opens the source file in GitHub's web editor. Primary contribution path for board members who don't know Git.
- **"Report an issue" button** — every page has a link that opens a pre-filled GitHub Issue. For flagging problems without making edits.
- **Per-page table of contents** — right-side TOC on each page for long documents (articles, policies).

---

## Phase 4: Deployment (GitHub Pages + GitHub Actions)

### How publishing works

Every merge to `master` triggers an automated build and deploy. No manual steps required after setup.

```
Contributor edits a .qmd file on GitHub
        ↓
Opens a Pull Request
        ↓
Staff/board reviews and merges to master
        ↓
GitHub Actions triggers automatically
        ↓
Quarto renders all .qmd files → outputs HTML to docs/
        ↓
GitHub Pages pushes output to gh-pages branch
        ↓
Live site updates within ~2 minutes of merge
```

### GitHub Actions workflow (`.github/workflows/publish.yml`)

```yaml
on:
  push:
    branches: [master]

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - run: quarto render
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

### One-time GitHub Pages setup

In the repository Settings → Pages:
- Source: `Deploy from a branch`
- Branch: `gh-pages`, folder: `/ (root)`

The `GITHUB_TOKEN` is automatically provided by GitHub — no secrets to configure manually.

### Deployment documentation

`contributing/deployment.qmd` documents this process in plain language for non-engineers, covering:
- What happens automatically when a PR is merged
- How to check if a build succeeded (GitHub Actions tab)
- What to do if a build fails
- How to preview changes locally (optional, for staff with Quarto installed)

---

## Phase 5: Contribution Workflow

### Two paths for contributors

**Path 1 — "Edit this page" (recommended for board members)**

1. Click "Edit this page" on any web book page
2. GitHub opens the source `.qmd` file in its web editor
3. Make edits in the browser — no Git knowledge needed
4. Click "Propose changes" → GitHub creates a Pull Request automatically
5. Staff review and merge

**Path 2 — Pull Request (for staff)**

Standard GitHub workflow: branch → edit → open PR → review → merge. Used for larger changes such as restructuring sections or adding new policies.

### Review and approval rules

| Change type | Who can approve |
|---|---|
| Typo, formatting, broken link | Staff (single reviewer) |
| Wording clarification, date update | Staff (single reviewer) |
| Policy content change | Board approval required before merge |
| New policy or procedure | Board approval required before merge |
| Structural or navigation changes | Staff lead + one other reviewer |

### Issue reporting

Board members who spot something wrong but don't want to make an edit can click "Report an issue" on any page. This opens a pre-filled GitHub Issue that staff triage and resolve.

### Documentation

`contributing/index.qmd` — published in the web book, explains both paths and the review rules in plain language.

`contributing/deployment.qmd` — explains the CI/CD pipeline, how to verify a successful build, and how to preview locally.

`contributing/template.qmd` — blank template for drafting new policies or procedures.

---

## Out of scope

- Editorial review of policy substance (content conflicts flagged as `review` items are for the governance committee to resolve)
- ESIP wiki migration (the wiki at wiki.esipfed.org is a separate system)
- Cross-linking between related policies (deferred to a future iteration — tracked as Option C for later consideration)
- Assembly Notes (single non-markdown file; archive it in place, do not migrate to Quarto)
