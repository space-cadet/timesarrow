# T32 Proof-of-Principle Reanalysis Update

**Timestamp:** 2026-07-14 04:55:00 IST
**Task:** T32 — Post-May Numerics Correction and Reproducibility Pass
**Type:** Memory-bank synchronization after completed L16/L32 reruns and updated T20d reanalysis

## Summary

Recorded the completed `L=16` and `L=32` production reruns, the updated `T20d` reanalysis outcome, and the shift in emphasis from precision critical exponents to proof-of-principle support for the corrected continuous-transition interpretation.

## Findings

- `scripts/validate.sh` now passes locally, so the T32 reproducibility item is no longer blocked by the shell environment.
- Fresh `L=16` and `L=32` fine scans were completed and saved under `numerics/data/fss/`.
- The updated `T20d` reanalysis uses the current `L = 8, 16, 24, 32` fine-scan artifacts.
- The clearest finite-size signal is the upward drift and sharpening of the susceptibility/specific-heat peaks:
  - `L=16`: peak near `β≈0.752`
  - `L=24`: peak near `β≈0.756`
  - `L=32`: peak near `β≈0.758`
- The corrected numerics are now strong enough for proof of principle, while autocorrelation-aware precision exponent extraction remains explicitly deferred.

## Files Updated

- `memory-bank/tasks/T20d.md`
- `memory-bank/tasks/T32.md`
- `memory-bank/tasks.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/session_cache.md`
- `memory-bank/sessions/2026-07-14-night.md`
- `memory-bank/edit_history.md`

## Remaining Work

- Correct the dashboard text and retire any lingering misleading `T20d` figure references.
- Finalize the T32 artifact-policy/manuscript-gate bookkeeping.
- Return attention to the more central volume-operator and related calculations rather than pursuing precision exponents immediately.
