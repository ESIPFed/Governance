# Deploy Redesigned Site from a `development` Branch — Design Spec

**Date:** 2026-07-02
**Author:** Aaron Friesz (amfriesz)
**Status:** Approved — ready for implementation planning

---

## Overview

The Quarto-based governance redesign (content audit, repo restructure, web book — see
[2026-06-24-esip-governance-redesign-design.md](2026-06-24-esip-governance-redesign-design.md))
is feature-complete in this fork, on the local `main` branch.

The upstream repository, `ESIPFed/Governance`, has GitHub Pages nominally enabled
(`Settings → Pages` shows source = `Deploy from branch: master, path /`), but
`https://esipfed.github.io/Governance/` currently returns a **404** — there is no working
live site today. Nothing is being replaced; this is the first functioning deployment.

This spec covers pushing the redesign to upstream as a `development` branch and pointing
Pages at its build output, so ESIP staff/board can review the real, rendered result —
without altering `master` or its history.

---

## Current state (verified against upstream)

- Upstream default branch: `master`. No `development`, `main`, or `gh-pages` branch exists there yet.
- Upstream Pages: nominally enabled, source = `Deploy from branch: master, path /`, but
  `https://esipfed.github.io/Governance/` returns a 404. Confirmed via `gh api repos/ESIPFed/Governance/pages`
  and a direct `curl` of the URL. No working site exists today.
- Upstream has no `.github/workflows` directory — no CI currently configured.
- Local fork (`amfriesz/Governance`) already proved the build mechanism: `main` → Action renders
  the book → `quarto-actions/publish@v2` (target `gh-pages`) pushes rendered output to a `gh-pages`
  branch. That branch already exists and builds successfully in the fork.
- Local `_quarto.yml` has `repo-url: https://github.com/amfriesz/Governance` — a leftover from
  fork testing (commit "Point repo-url to amfriesz/Governance for fork demo") that must be
  reverted before pushing upstream.
- The author has direct write access to `ESIPFed/Governance`.

---

## Changes

### 1. `_quarto.yml`

- Revert `repo-url` to `https://github.com/ESIPFed/Governance`.
- Add `repo-branch: development` under `book:`. Quarto's "Edit this page" / "Report an issue"
  links resolve against the repo's default branch unless `repo-branch` is set explicitly. Since
  the `.qmd` source files only exist on `development` (not `master`, the upstream default), every
  such link would otherwise point at a branch with no matching file and 404.

### 2. `.github/workflows/publish.yml`

- Change the trigger from `branches: [master]` to `branches: [development]`. Building against
  `master` isn't viable anyway — it has no `.qmd` files yet. Everything else in the workflow
  (Quarto setup, render, `quarto-actions/publish@v2` targeting `gh-pages`) is unchanged; it's
  already proven to work via the fork's existing `gh-pages` branch.

### 3. Push to upstream

- Add a local git remote `upstream` → `https://github.com/ESIPFed/Governance.git`.
- Push local `main` to upstream as `development`: `git push upstream main:development`.
- Upstream and the fork share common history (same original repo), so this is a normal branch
  push — not a rewrite or force-push.
- Pushing alone does not change the Pages source. It triggers the Action, which renders the book
  and pushes the result to a new `gh-pages` branch on the upstream repo. `esipfed.github.io/Governance/`
  keeps returning 404 until step 4.

### 4. Cutover

- After the Action run from step 3 completes and `gh-pages` exists on upstream with the rendered
  site, change upstream **Settings → Pages** source from `Deploy from branch: master /(root)` to
  `Deploy from branch: gh-pages /(root)`.
- This is the step that makes the URL serve real content for the first time. It's still an org-repo
  settings change, so it will be done last, with explicit confirmation immediately beforehand.
- `master` is not modified in any way — its content and history are left intact. If the Pages source
  ever needs to be reverted, pointing it back to `master` restores exactly today's state (a 404,
  since master has no working Pages output either).

---

## Sequencing

```
Fix _quarto.yml + workflow trigger (local)
        ↓
Commit changes on main
        ↓
Add `upstream` remote, push main → upstream development
        ↓
Action runs on upstream: render → publish to upstream gh-pages branch
        ↓
Verify upstream gh-pages branch + rendered output look correct
        ↓
[Explicit confirmation checkpoint]
        ↓
Switch upstream Pages source: master → gh-pages
        ↓
Verify https://esipfed.github.io/Governance/ now serves the new book
```

---

## Out of scope

- Merging `development` into `master`.
- Opening a tracking PR from `development` to `master` (explicitly declined for now — can be
  opened later when ready to merge).
- Renaming branches, changing the upstream default branch.
- ESIP brand colors / `custom.scss` — already handled by the prior redesign plan.
- Any change to the fork (`amfriesz/Governance`) itself — it is already in the desired state.
