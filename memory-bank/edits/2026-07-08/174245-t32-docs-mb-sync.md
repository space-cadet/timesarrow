# T32 Docs and Memory Synchronization

**Timestamp:** 2026-07-08 17:42:45 IST
**Task:** T32 — Post-May Numerics Correction and Reproducibility Pass
**Type:** Documentation and memory-bank synchronization

## Summary

Synchronized the correction documentation, rendered numerics docs, and memory-bank records after auditing which T32 issues have been resolved and which remain open.

## Files Updated

- `memory-bank/implementation-details/post-may-numerics-correction-plan.md`
- `memory-bank/tasks/T31.md`
- `memory-bank/tasks/T32.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/implementation-details/signed-volume-observable.md`
- `memory-bank/session_cache.md`
- `memory-bank/tasks.md`
- `memory-bank/sessions/2026-07-05-night.md`
- `memory-bank/sessions/2026-07-02-evening.md`
- `memory-bank/edit_history.md`
- `numerics/docs/dashboard.qmd`
- `numerics/docs/dashboard-prototype.qmd`
- `numerics/docs/tasks/t31-signed-volume.qmd`
- `numerics/docs/_site/` rendered Quarto output

## Changes

- Recorded resolved-vs-remaining status for each T32 error class.
- Marked T22a and T25 source corrections as resolved.
- Marked T31 design/test correction as partially resolved: old $|Q|/N$ data are exploratory, greedy gauge fixing is withdrawn, and the candidate gauge-invariant dressed correlator is documented.
- Cleaned stale historical T22a/T31 wording so search results point to superseded provenance rather than current guidance.
- Marked the 2026-07-02 iterative-gauge-fixing next steps as superseded by T32.
- Removed duplicated unmarked first-order T20 figure entries from the dashboard source.
- Replaced the stale first-order prototype dashboard entry with a T20d Ising correction entry.
- Rebuilt the Quarto site into `_site` using the current `output-dir: _site` configuration.

## Remaining Work

- Run the Rust and TypeScript validation path with a Rust 2024-compatible toolchain.
- Physically review and production-test the T31 dressed correlator.
- Complete T20d autocorrelation-aware numerical reanalysis.
- Finish artifact-policy cleanup for superseded figures, old scripts, logs, and generated outputs.
