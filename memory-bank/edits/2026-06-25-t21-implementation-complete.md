# T21 Implementation Complete — 2026-06-25

## What Was Implemented

### ts-quantum Library
- **New file**: `src/lattice/checkpoint.ts`
  - `CheckpointManifest` interface
  - `saveCheckpoint()` / `loadCheckpoint()` / `hasCheckpoint()`
  - `getRemainingBetas()` — filters out completed β values
  - `createSimulationId()` — generates unique simulation IDs
  - `listCheckpoints()` / `deleteCheckpoint()` — management utilities
- **Updated**: `src/lattice/index.ts` — exports checkpoint module
- **Updated**: `src/lattice/observables.ts` — fixed `jackknifeError()` to return 0 for n ≤ 1

### timesarrow Numerics
- **New file**: `src/scripts/t20-z2-lgt-phase1-worker.cjs`
  - Worker thread entry point using CommonJS `require()`
  - Runs single β simulation and posts result back to main thread
- **New file**: `src/scripts/t20-z2-lgt-phase1-main.cjs`
  - Main orchestrator with worker pool
  - Assigns β values to workers dynamically
  - Saves checkpoint after each β completes
  - Resumes from checkpoint on restart
  - CLI entry point with L, measureSweeps, thermalSweeps arguments

## Validation Results

### Correctness Test (L=8, 1000 sweeps, 11 β values)
Worker thread results match single-threaded within statistical errors:

| β | Single-Threaded | Worker Thread | Match |
|---|-----------------|---------------|-------|
| 0.1 | 0.1041 ± 0.0127 | 0.0956 ± 0.0077 | ✅ |
| 0.2 | 0.2062 ± 0.0108 | 0.1988 ± 0.0100 | ✅ |
| 0.3 | 0.2703 ± 0.0119 | 0.2841 ± 0.0078 | ✅ |
| 0.4 | 0.3741 ± 0.0129 | 0.3753 ± 0.0125 | ✅ |
| 0.44 | 0.4228 ± 0.0075 | 0.4381 ± 0.0101 | ✅ |
| 0.5 | 0.4756 ± 0.0132 | 0.4769 ± 0.0128 | ✅ |

### Performance Test (L=8, 5000 sweeps, 11 β values)

| Mode | Wall-Clock Time | Speedup |
|------|-----------------|---------|
| Single-threaded | 28.5s | 1.0× |
| Worker threads (8 cores) | 10.7s | 2.7× |

**Note**: Speedup is limited because each β is quick (~2-3s). For larger L=16 simulations, expected speedup approaches 6-8×.

### Checkpoint Resume Test
- ✅ Checkpoint saved after each β completes
- ✅ Resume correctly skips already-completed β values
- ✅ Multiple runs with same simulation ID don't re-run completed β values

## Files Changed

### ts-quantum
- `src/lattice/checkpoint.ts` — NEW
- `src/lattice/index.ts` — Added checkpoint export
- `src/lattice/observables.ts` — Fixed jackknifeError edge case

### timesarrow
- `src/scripts/t20-z2-lgt-phase1-worker.cjs` — NEW
- `src/scripts/t20-z2-lgt-phase1-main.cjs` — NEW

## Next Steps

1. Run full L=16 production run with worker threads
2. Compare to previous single-threaded L=16 results
3. Update numerics pages with worker thread documentation
4. Implement fine-grained checkpointing if needed for L=32

## Issues Encountered

1. **ESM/CJS module mismatch**: ts-quantum's ESM build has issues, so worker scripts use CommonJS `require()`
2. **Jackknife edge case**: Returns NaN for single-bin data — fixed to return 0
3. **Worker overhead**: For small L=8 simulations, worker creation overhead limits speedup

## Commits

- ts-quantum: TBD (checkpoint module + jackknife fix)
- timesarrow: TBD (worker scripts)
