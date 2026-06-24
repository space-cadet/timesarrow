# timesarrow Project Memory Bank

## Project Overview

Timesarrow — quantum gravity simulation and visualization project. Monte Carlo simulations of lattice gauge theory, spin networks, and related quantum geometry systems.

## Active Tasks

| ID | Task | Status | Next |
|----|------|--------|------|
| T20-Phase1 | Z₂ LGT 2D square lattice | ✅ Complete | Results documented, numerics page updated |
| T21 | Worker threads + checkpointing | 🔄 Ready to implement | Start with checkpoint.ts module |
| T20-Phase2 | Sharp phase transition figures | ⏳ Pending T21 | Multi-lattice sweep with worker threads |
| T20-Phase3 | 3D cubic lattice | ⏳ Pending | Paper target |
| T25 | Volume operator eigenvalues | ✅ Complete | — |

## Completed Tasks

### T20-Phase1 — Z₂ LGT 2D Square Lattice

**Completed**: 2026-06-24
**Results**: L=16, 18 β values, 100k sweeps, errors ~0.0005
**Files**:
- `numerics/output/t20-phase1-square-lattice.json`
- `numerics/output/t20-phase1-run.log`
- `numerics/docs/tasks/t20-z2-lgt.qmd` (updated with chronological log)

**Key Results**:
| β | ⟨P⟩ | Phase |
|---|-----|-------|
| 0.44 | 0.4134 ± 0.0006 | Critical |
| 0.45 | 0.4224 ± 0.0006 | Critical |
| 0.46 | 0.4306 ± 0.0005 | Critical |

Critical coupling β_c ≈ 0.44 confirmed, matching exact value 0.4407.

## In Progress

### T21 — Worker Threads + Checkpointing

**Status**: 🔄 Planning complete, ready to implement
**Priority**: High (blocks Phase 2 and 3)

**Plan**:
1. Coarse-grained checkpointing (per-β completion tracking)
2. Fine-grained checkpointing (mid-simulation state save) — if needed for L≥32
3. Worker thread orchestration for parallel β sweeps

**Files to create**:
- `numerics/src/utils/checkpoint.ts`
- `numerics/src/scripts/t20-z2-lgt-phase1-worker.ts`
- `numerics/src/scripts/t20-z2-lgt-phase1-main.ts`

**Decision log**: See `memory-bank/edits/2026-06-25-t20-results-and-checkpointing-plan.md`

- General lattice tools → `ts-quantum` package
- Simulation scripts + analysis → `timesarrow/numerics/`
- CPU parallelization preferred over GPU for this workload (Z₂ Metropolis is sequential per config, but independent sweeps parallelize across cores)

## Key Files

| Type | Location |
|------|----------|
| Simulation code | `numerics/src/scripts/` |
| Quarto docs | `numerics/docs/` |
| Output/plots | `numerics/output/` + `numerics/docs/assets/` |
| Implementation notes | `numerics/docs/implementation/` |

## Resources

- M2 MacBook Air: 8 cores, 16GB RAM
- ts-quantum package: lattice module with Z₂ gauge field, Metropolis, observables

---

*Memory bank format: v6.12*
