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
| A-05 | fix | All readme files | All navigation links are hardcoded GitHub blob URLs (153 total across `Bylaws/readme.md` and `ESIP Policies and Procedures/readme.md`) — will break on repo rename/fork | Replaced by Quarto sidebar navigation during migration |
| A-06 | fix | `ESIP Policies and Procedures/readme.md` | `3.3F ESIP Committee Budget Request Policy.md` exists in repo but is absent from the P&P index | Add to navigation in `_quarto.yml` (same fix as A-02) |
| A-07 | fix | `ESIP Policies and Procedures/readme.md` line 57 | URL for 3.5B Complimentary Registration uses literal `&` instead of `%26` in filename (`ESIP P&P 3.5B...` vs `ESIP%20P%26P%203.5B...`) — malformed URL that may resolve incorrectly | Replaced by Quarto navigation; no separate fix needed if A-05 is resolved |
| A-08 | review | `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.0 Definitions.md` | `1.0 Definitions.md` exists in repo but is not linked from the P&P index (separate from its draft status in A-03) | Add to navigation in `_quarto.yml` if board approves the document (see A-03); otherwise remove or archive |
| A-09 | review | `README.md`, `Standing Committee and Cluster Policies and Procedures/Funding Friday Rules.md`, `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.1 Goals.md` | Multiple files link to `wiki.esipfed.org` — external wiki that may no longer be maintained | Review whether wiki links are still valid; update or remove stale references during migration |

## Orphaned files found

Files present in the repository but not linked from any index:

- `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.0 Definitions.md` — draft document, not in index (see A-03 and A-08)
- `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.10 Memoranda of Understanding.md` — file is present and correct, but the index link points to a fork (see A-01); effectively orphaned from the canonical index
- `ESIP Policies and Procedures/3.0 Business and Finance/ESIP P&P 3.3A FiCom annual budget cycle.md` — see A-02
- `ESIP Policies and Procedures/3.0 Business and Finance/ESIP P&P 3.3F ESIP Committee Budget Request Policy.md` — see A-06

## Step-by-step command results

**Step 1 — File count:** 123 total source files (expected ~80). The higher count is explained by the Bylaws directory containing 75 individual section files; the overall structure is as expected.

**Step 2 — Files missing from index:** The `comm` command matched against `blob/master` URLs, so the BenGalewsky fork link (1.10 MoU) also appeared as unmatched. Four files are genuinely absent from the index: `1.0 Definitions.md`, `1.10 Memoranda of Understanding.md` (via fork), `3.3A FiCom annual budget cycle.md`, and `3.3F ESIP Committee Budget Request Policy.md`.

**Step 3 — Broken fork links:** One confirmed hit: `ESIP Policies and Procedures/readme.md` line 29 links to `BenGalewsky/Governance` fork at a specific commit SHA (A-01).

**Step 4 — Draft/unapproved documents:** One confirmed hit: `ESIP Policies and Procedures/1.0 Corporate/ESIP P&P 1.0 Definitions.md` contains "not yet been approved by the Board of Directors of ESIP" (A-03).

**Step 5 — Hardcoded GitHub blob URLs:** The `grep -rn "github.com.*blob/master"` command returned 0 because the macOS BSD `grep` handles the dot-star pattern differently in recursive mode; direct file greps confirm 37 links in the P&P readme and 74 in the Bylaws readme, for **153 total** hardcoded GitHub blob/master links across the two index files. This exceeds the expected >50 and confirms A-05.

## Notes

- `Assembly Notes/ESIP Assembly 2017 Winter Notes` — UTF-8 text file with no extension; archive in place, do not migrate to Quarto web book
- `Standing Committee and Cluster Policies and Procedures/Template for new Policies` — no file extension; ASCII text; migrate content to `contributing/template.qmd`
- `README.md` (root) — references `wiki.esipfed.org` and a Zenodo DOI badge; update root README during migration to point to the new Quarto site
