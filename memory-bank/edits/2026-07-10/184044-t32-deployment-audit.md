# T32 Deployment Audit and Task Cleanup

**Timestamp:** 2026-07-10 18:40:44 IST
**Task:** T32 — Post-May Numerics Correction and Reproducibility Pass
**Type:** Memory-bank synchronization and deployment audit

## Summary

Clarified the remaining T32 work as executable memory-bank tasks and checked the local `space-cadet.github.io` deployment checkout against the corrected local Quarto render.

## Findings

- `memory-bank/tasks/T20d.md` already contains concrete remaining work for fine scans, autocorrelation-aware uncertainty handling, finite-size scaling, and dashboard updates.
- `memory-bank/tasks/T31.md` had stale checkbox state; source-level correction work is recorded as done, while Rust 2024 test execution, physical review, and production validation remain open.
- `memory-bank/tasks/T32.md` now explicitly tracks Rust validation, T20d reanalysis, artifact policy, deployment sync, and the manuscript gate.
- The local `numerics/docs/_site` render contains the corrected T20d, T22a, and T31 pages.
- The local `space-cadet.github.io` checkout is clean but stale for `projects/timesarrow/numerics/`; deployed `/tasks/` pages still contain withdrawn first-order, spin-foam dominance, and greedy-gauge wording.
- The deployed dashboard HTML differs from the corrected `_site` render; an older project-local deployment copy also still lists superseded first-order dashboard figure entries.

## Files Updated

- `memory-bank/tasks/T31.md`
- `memory-bank/tasks/T32.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/edit_history.md`
- `memory-bank/edits/2026-07-10/184044-t32-deployment-audit.md`

## Remaining Work

- Run Rust tests under a Rust 2024-compatible toolchain.
- Complete T20d fine-scan reanalysis with autocorrelation-aware uncertainties.
- Finish artifact-policy cleanup for superseded generated outputs and provenance-only scripts.

## Deployment Resolution

- 2026-07-10 18:45 IST: Mirrored corrected `numerics/docs/_site/` output into `/Users/deepak/code/space-cadet.github.io/projects/timesarrow/numerics/`.
- Removed stale deploy-only files in the numerics subtree via `rsync --delete`.
- Committed and pushed `space-cadet.github.io` commit `92d05cc` with message `docs: deploy corrected timesarrow numerics`.
