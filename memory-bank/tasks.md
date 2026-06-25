# timesarrow Project Memory Bank

## Project Overview

Timesarrow — quantum gravity simulation and visualization project. Monte Carlo simulations of lattice gauge theory, spin networks, and related quantum geometry systems.

## Active Tasks

| ID | Task | Status | Next |
|----|------|--------|------|
| T27 | Rust Z₂ LGT framework | ✅ Complete | Benchmark vs TypeScript |
| T20-Phase1 | Z₂ LGT 2D square lattice | ✅ Complete | Results documented, numerics page updated |
| T21 | Worker threads + checkpointing | 🔄 Ready to implement | Start with checkpoint.ts module |
| T20-Phase2 | Sharp phase transition figures | ✅ Complete | Results in numerics page, data registry created |
| T20-Phase3 | 3D cubic lattice | ✅ Complete | L=4,6,8 simulated, β_c ≈ 0.75 |
| T25 | Volume operator eigenvalues | ✅ Complete | — |

## Completed Tasks

### T20-Phase1 — Z₂ LGT 2D Square Lattice

**Completed**: 2026-06-25
**Results**: L=16, 11 β values, 100k sweeps, errors ~0.0005
**Files**:
- `numerics/output/t20-phase1-worker-L16.json`
- `numerics/output/t27-rust-benchmark-L16-final.json` (Rust validation)
- `memory-bank/tasks/T20.md`
- `memory-bank/tasks/T27.md`

**Key Results**:
| β | ⟨P⟩ | Error | Phase |
|---|-----|-------|-------|
| 0.44 | 0.4144 ± 0.0006 | Critical |
| 0.5 | 0.4629 ± 0.0006 | Strong |
| 1.0 | 0.7613 ± 0.0004 | Strong |

Critical coupling β_c ≈ 0.44 confirmed, matching exact value 0.4407.
**Rust speedup**: ~2,500–3,000× validated against TypeScript.

### T27 — Rust Z₂ LGT Framework

**Completed**: 2026-06-25
**Results**: L=16, 100k sweeps, 11 β values in 3.0s
**Files**:
- `rust-lattice/src/lib.rs`
- `rust-lattice/src/main.rs`
- `rust-lattice/Cargo.toml`
- `rust-lattice/target/release/z2-lattice-gauge`

**Validation**: All 11 β values match TypeScript within |Δ| < 0.02.
**Bug fixes**: Plaquette geometry (link indices), sign convention (directed vs undirected links).

## Active Tasks

| ID | Task | Status | Next |
|----|------|--------|------|
| T20-Phase2 | Sharp phase transition figures | ⏳ Pending | Run Rust with L = 8,12,16,20,24 |
| T20-Phase3 | 3D cubic lattice | ⏳ Pending | After Phase 2 |
| T21 | Worker threads + checkpointing | ✅ Complete | — |
| T27 | Rust Z₂ LGT framework | ✅ Complete | — |

## In Progress

None — session ended. Next session: T20-Phase2 or Phase 3.
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
