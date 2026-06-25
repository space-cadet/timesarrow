# Session Cache: T20 Phase 1 + T27 Rust Framework
*Updated: 2026-06-25 14:45 IST*

## Current Session
**Started**: 2026-06-25 12:45 IST
**Ended**: 2026-06-25 14:45 IST
**Focus**: T20 Phase 1 completion + T27 Rust validation
**Status**: ✅ All objectives met

## Task Registry
- T20: Z₂ LGT Phase 1 (2D square lattice) — ✅ COMPLETE
- T21: Worker threads + checkpointing — ✅ COMPLETE
- T27: Rust Z₂ lattice gauge framework — ✅ COMPLETE
- T20-Phase2: Sharp phase transition — ⬜ PENDING (next session)
- T20-Phase3: 3D cubic lattice — ⬜ PENDING

## Completed Work

### T20 Phase 1 Production Run (L=16, 100k sweeps, 3 workers)
**Status**: ✅ COMPLETE
**Wall time**: ~2h 11m
**Results**: 11 β values (0.1–2.0), all match critical coupling β_c ≈ 0.44
**Output**: `numerics/output/t20-phase1-worker-L16.json`

### T27 Rust Framework Validation
**Status**: ✅ COMPLETE — Validated against TypeScript
**Performance**: 3.0s for L=16, 100k sweeps, 11 β values
**Speedup**: ~2,500–3,000× vs TypeScript
**Bug fixes**: Plaquette geometry (wrong link indices), sign convention (negate output layer only)
**Output**: `numerics/output/t27-rust-benchmark-L16-final.json`

## Validation Summary
| Metric | TypeScript | Rust | Ratio |
|--------|-----------|------|-------|
| Wall time (11 β) | ~2h 11m | 3.0s | ~2,600× |
| Accuracy | Statistical errors | Deterministic | Match within tolerance |
| Code size | ~4k lines TS | ~400 lines Rust | — |

## Next Session Priorities
1. T20 Phase 2: Finite-size scaling (L=8,12,16,20,24) — Rust-based
2. T20 Phase 3: 3D cubic lattice — Rust-based
3. Higher statistics: 1M sweeps (now practical with Rust speed)

## Files
- `memory-bank/tasks/T20.md` — Updated with Phase 1 results
- `memory-bank/tasks/T27.md` — Created with Rust validation data
- `numerics/docs/tasks/t20-z2-lgt.qmd` — Updated with Rust comparison
- `numerics/docs/implementation/t20-z2-lgt.md` — Updated with architecture
- `rust-lattice/src/lib.rs` — Z2GaugeField implementation
- `rust-lattice/src/main.rs` — CLI with rayon parallel sweeps

## Session End
Session closed by user request. All memory banks updated. Git commits pushed to:
- `space-cadet/timesarrow` (main): T20+T27 code + docs
- `space-cadet/space-cadet.github.io` (main): Updated T20 page
