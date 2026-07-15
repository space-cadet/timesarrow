# T31 Signed-Volume Provenance Salvage

**Timestamp:** 2026-07-15 18:35:42 IST
**Task:** T31 — Signed Volume Observable
**Type:** Provenance salvage and negative-result archive

## Summary

Recovered an unpushed pre-pivot T31 calibration branch and preserved only the pieces that still fit the current repository story: additional signed-volume calibration artifacts, cold-start support for archived gauge-invariant runs, and memory-bank notes clarifying that these results strengthen the existing Polyakov-loop pivot rather than reopening signed volume as the active deconfinement diagnostic.

## Findings

- Additional `L=4` and `L=6` hot-start/cold-start signed-volume calibration files were preserved under `numerics/data/signed-volume/`.
- The archived runs are consistent with the existing negative result: plaquette and Wilson-loop observables order strongly at high `β`, while the dressed signed-volume correlator stays non-monotone and sector-sensitive.
- `--cold-start` is now available for provenance-only gauge-invariant signed-volume calibration runs.
- Signed-volume JSON output is now explicitly labeled with `signedVolumeKind` and `initialState` so archived artifacts remain self-describing.

## Files Updated

- `rust-lattice/src/main.rs`
- `rust-lattice/src/lib.rs`
- `memory-bank/tasks/T31.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/tasks.md`
- `memory-bank/edit_history.md`

## Data Artifacts

- `numerics/data/signed-volume/t31-gi-L4-calibration-20260714.json`
- `numerics/data/signed-volume/t31-gi-L4-cold-calibration-20260714.json`
- `numerics/data/signed-volume/t31-gi-L6-calibration-20260714.json`
- `numerics/data/signed-volume/t31-gi-L6-cold-calibration-20260714.json`
- `numerics/data/signed-volume/t31-gi-L6-beta1-seed42-20260714.json`
- `numerics/data/signed-volume/t31-gi-L6-beta1-seed43-20260714.json`
- `numerics/data/signed-volume/t31-gi-L6-beta1-seed44-20260714.json`

## Remaining Work

- Keep the signed-volume calibration artifacts as provenance-only evidence for the obstruction.
- Continue active T31 deconfinement work through the Polyakov-loop path on `origin/main`.
