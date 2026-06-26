# T20-Phase3b: Critical Exponent Extraction from 3D Z₂ LGT

*Created: 2026-06-26*
*Status: 🔄 IN PROGRESS — Infrastructure ready, simulations pending*
*Last Updated: 2026-06-26*

## Session Update (2026-06-26 Morning)

**Contradiction resolved**: The claimed α = -3.084 was mixing 2D vs 3D physics. 3D Z₂ LGT is second-order (3D Ising universality, α ≈ 0.11), not first-order.

**Infrastructure created**: All 6 FSS blockers mapped and scripts generated:
- ✅ `t20-autocorr-v2.py` — Rust-based autocorrelation (8 workers, τ_int measured)
- ✅ `t20-sim-3d-fss.py` — Fine β grid near β_c
- ✅ `t20-multi-run.py` — Multiple independent runs with unique seeds
- ✅ `t20-fss-analysis.py` — 4 FSS methods with corrections-to-scaling

**Subagents completed**: `t20_fss_analysis` (13m36s), `t20_multi_run` (9m13s), `t20_fine_grid_l48` (8m17s), `t20_polyakov_loop` (done). `t20_autocorr` timed out but pipeline fixed with Rust `--raw-output` + worker threads.

**Estimated compute**: ~12–15 hours for full L=8→64 suite.

**Next**: Run simulations with proper CPU utilization.

## Objective

Extract critical exponents (ν, β, γ, α) from the 3D Z₂ LGT simulation data to confirm the universality class. This is a dedicated finite-size scaling study.

## Status Summary

| Blocker | Status |
|---------|--------|
| Polyakov loop implementation | 🟡 Script ready |
| Autocorrelation measurement | ✅ Script ready |
| Fine β grid near β_c | ✅ Script ready |
| L ≥ 48 lattices | ✅ Script ready |
| Multiple independent runs | ✅ Script ready |
| Corrections-to-scaling analysis | ✅ Script ready |

## Detailed Requirements

See [`implementation-details/t20-phase3b-requirements.md`](implementation-details/t20-phase3b-requirements.md) for full specifications including:
- Lattice size requirements (L = 8 → 64)
- β grid resolution (Δβ = 0.001–0.005)
- Sweeps and thermalization requirements
- Observables: Polyakov loop, Binder cumulant, correlation length
- 4 analysis methods (Binder crossing, scaling collapse, peak scaling, β_c shift)
- Corrections-to-scaling formulas
- Autocorrelation analysis implementation
- Estimated compute cost (~12–15 hours)
- References (Pelissetto & Vicari 2002, Creutz et al. 1979, etc.)

## Key Files

- `numerics/src/scripts/t20-autocorr-v2.py`
- `numerics/src/scripts/t20-sim-3d-fss.py`
- `numerics/src/scripts/t20-multi-run.py`
- `numerics/src/scripts/t20-fss-analysis.py`
- `rust-lattice/src/main.rs` (with `--raw-output` flag)
- `implementation-details/t20-phase3b-requirements.md`

