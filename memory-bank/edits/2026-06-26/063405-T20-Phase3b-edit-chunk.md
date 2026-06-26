# Edit Chunk: 2026-06-26 06:34:05 IST

## Task: T20-Phase3b

### Work Done

Finite-Size Scaling Analysis for 3D Z₂ LGT: Identified and resolved the α = -3.084 contradiction (mixing 2D vs 3D physics). Created infrastructure for rigorous FSS: 6 blockers mapped, all scripts generated, subagents completed. Simulations not yet run.

### Files Modified

- Created `numerics/src/scripts/t20-autocorr-v2.py` — Rust-based autocorrelation analysis with 8 worker threads, --raw-output flag, τ_int measurement
- Created `numerics/src/scripts/t20-sim-3d-fss.py` — Fine β grid (Δβ=0.001-0.005) near critical point for L=8,16,32,48,64
- Created `numerics/src/scripts/t20-multi-run.py` — Multiple independent runs with unique seeds per (L,β) configuration
- Created `numerics/src/scripts/t20-fss-analysis.py` — 4 FSS methods: Binder cumulant crossing, scaling collapse, peak height scaling, β_c shift with corrections-to-scaling
- Modified `rust-lattice/src/main.rs` — Added --raw-output flag for raw time series output (autocorrelation pipeline)
- Created `memory-bank/tasks/T20-Phase3b.md` — Full task specification: 6 blockers, requirements, estimated compute cost, analysis methods
- Modified `memory-bank/tasks/T20.md` — Updated gap analysis: Wilson loops implemented (2026-06-26 night), missing observables corrected
- Modified `memory-bank/activeContext.md` — Added T20-Phase3b status and next steps

