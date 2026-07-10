# T32 Dashboard Asset and Timestamp Repair

**Timestamp:** 2026-07-10 19:05:00 IST
**Task:** T32 — Post-May Numerics Correction and Reproducibility Pass
**Type:** Numerics docs repair and deployment follow-up

## Summary

Repaired the numerics dashboard/gallery publication path, corrected stale page metadata, fixed the T20 Phase 3b figure paths, and redeployed the rendered numerics site.

## Findings

- The dashboard gallery built image URLs dynamically, so Quarto was not copying most of `numerics/docs/assets/` into `_site/assets/`.
- Several numerics pages had stale or invalid `date-modified` metadata that did not match the visible "Last updated" text.
- The T20 Phase 3b Ising FSS section still referenced the obsolete `../figures/t20d-ising/` path instead of the published `../assets/` files.
- The main numerics overview page did not expose task recency in the `Simulation Tasks` table.

## Files Updated

- `numerics/docs/_quarto.yml`
- `numerics/docs/dashboard.qmd`
- `numerics/docs/index.qmd`
- `numerics/docs/tasks/t20-z2-lgt.qmd`
- `numerics/docs/tasks/t22-spin-foam.qmd`
- `numerics/docs/tasks/t25-volume-operator.qmd`
- `numerics/docs/tasks/t31-signed-volume.qmd`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/edit_history.md`
- `memory-bank/edits/2026-07-10/190500-t32-dashboard-asset-fix.md`

## Deployment Notes

- Rendered `numerics/docs/` after adding `assets/**` as project resources.
- Deploy commit `21a496e`: restored dashboard assets and refreshed corrected timestamps on the public numerics pages.
- Deploy commit `efe6780`: fixed the T20 Phase 3b figure references and added the `Last Updated` column on the main numerics page.

## Remaining Work

- Rust 2024-compatible validation for the T31 gauge-invariance tests.
- T20d fine-scan reanalysis with autocorrelation-aware uncertainties.
- Artifact-policy cleanup and final T32 manuscript-gate closure.
