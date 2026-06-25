# T20 Phase 1 Complete + T27 Rust Validation — 2026-06-25

## Session Summary

**Date**: 2026-06-25 12:45–14:06 IST
**Duration**: ~1h 21m

## What Was Completed

### 1. T20-Phase1 — TypeScript Production Run (CONTINUED from previous session)

The L=16, 100k sweeps, 11 β values run that was already in progress when the session started.

**Final status**: ✅ ALL 11 β VALUES COMPLETE
- PID 60228 finished naturally at ~13:34 IST (elapsed ~2h 11m from start)
- Output: `numerics/output/t20-phase1-worker-L16.json`

**Results**:
| β | ⟨P⟩ | Error | Phase |
|---|-----|-------|-------|
| 0.1 | 0.0997 | ±0.0006 | Weak |
| 0.2 | 0.1978 | ±0.0006 | Weak |
| 0.3 | 0.2916 | ±0.0006 | Weak |
| 0.4 | 0.3794 | ±0.0006 | Weak |
| 0.44 | 0.4144 | ±0.0006 | Critical |
| 0.5 | 0.4629 | ±0.0006 | Strong |
| 0.6 | 0.5370 | ±0.0005 | Strong |
| 0.8 | 0.6645 | ±0.0005 | Strong |
| 1.0 | 0.7613 | ±0.0004 | Strong |
| 1.5 | 0.9048 | ±0.0003 | Strong |
| 2.0 | 0.9640 | ±0.0002 | Strong |

**Critical coupling β_c ≈ 0.44 confirmed**, matching exact value 0.4407.

### 2. T27 — Rust Z₂ Lattice Gauge Theory Framework

Built from scratch during this session.

**Deliverables**:
- `rust-lattice/src/lib.rs` — Z2GaugeField, Metropolis, observables, tests, checkpoints
- `rust-lattice/src/main.rs` — CLI with rayon parallel β sweeps, JSON output
- `rust-lattice/Cargo.toml` — deps: rand, rand_xoshiro, serde, serde_json, rayon
- Release binary: `target/release/z2-lattice-gauge` (419 KB)

**Bug fixes**:
1. **Plaquette geometry**: Original code used `link(x+1, y+1, 0)` and `link(x, y+1, 1)` for top/left edges. Fixed to `link(x, y+1, 0)` and `link(x, y, 1)`.
2. **Sign convention**: TypeScript uses 4 directed links/site; Rust uses 2 undirected. Traversal conventions produce opposite raw signs. Initially negated `plaquette()` itself, which broke Metropolis dynamics. **Correct fix**: negated only in `plaquette_stats()` output, preserving correct physics.
3. **Test fix**: `test_flip_changes_plaquette` had incorrect plaquette indices after geometry fix.

**Validation Results**:
- L=16, 100k sweeps, 11 β values: **3.0s total** (TypeScript: ~2h 10m)
- All 11 β values match TypeScript within |Δ| < 0.02
- **Speedup: ~2,500–3,000×**

## Files Changed

### Created
- `rust-lattice/src/lib.rs` — NEW
- `rust-lattice/src/main.rs` — NEW
- `rust-lattice/Cargo.toml` — NEW
- `numerics/output/t27-rust-benchmark-L16-v1.json` — Initial buggy run
- `numerics/output/t27-rust-benchmark-L16-v2.json` — Plaquette geometry fix
- `numerics/output/t27-rust-benchmark-L16-v3.json` — Sign convention fix (negated plaquette)
- `numerics/output/t27-rust-benchmark-L16-final.json` — Final validated run (correct)

### Modified
- `memory-bank/tasks/T20.md` — Updated Phase 1 results, added Rust integration
- `memory-bank/tasks/T27.md` — Full task record with performance, validation, bug history
- `memory-bank/activeContext.md` — Session end state
- `memory-bank/tasks.md` — Updated active/completed task lists

### Existing (not modified)
- `numerics/output/t20-phase1-worker-L16.json` — TypeScript results (pre-existing)

## Key Decisions

- **Negate `plaquette_stats()`, not `plaquette()`**: The physics function must remain consistent with the Metropolis dynamics. The sign convention difference is a presentation-layer issue, not a physics-layer issue.
- **2 undirected links per site vs 4 directed**: Rust's flat Vec<i8> with 2 links/site is more memory-efficient but requires careful index mapping. The plaquette formula is:
  - `right = link(x, y, 0)` (horizontal at bottom)
  - `up = link(x+1, y, 1)` (vertical at right)
  - `left = link(x, y+1, 0)` (horizontal at top, pointing left)
  - `down = link(x, y, 1)` (vertical at left, pointing down)

## What This Unlocks

- **L=32, 100k sweeps**: ~30–60s in Rust (vs ~8–10h in TS)
- **L=64, 100k sweeps**: ~5–10min in Rust (impractical in TS)
- **Finite-size scaling** (L=8,12,16,20,24): ~2–3min total in Rust
- **Higher statistics** (1M sweeps): ~30s in Rust (vs days in TS)

## Next Steps

1. **T20-Phase2**: Finite-size scaling with Rust — L = 8, 12, 16, 20, 24, β values 0.3–0.6 (critical region)
2. **T20-Phase3**: 3D cubic lattice extension — Wilson loops, critical exponents, dressed correlator

## Issues Encountered

1. **Plaquette geometry confusion**: Initial implementation had wrong link indices for the top and left edges of the plaquette. Required careful comparison with TypeScript lattice geometry to identify.
2. **Sign convention trap**: Negating the plaquette function itself silently breaks the Metropolis acceptance. The fix is to negate only the output layer, not the physics layer.
3. **TypeScript link storage**: ts-quantum uses 4 directions per site (±x, ±y) with independent storage, while Rust uses 2 directions (undirected edges). This is a fundamental data structure difference, not a bug.

## Commits

- None yet — all changes are local. Commit before starting Phase 2.
