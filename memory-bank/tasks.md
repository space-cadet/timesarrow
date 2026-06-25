# timesarrow Project Memory Bank

## Project Overview

Timesarrow — quantum gravity simulation and visualization project. Monte Carlo simulations of lattice gauge theory, spin networks, and related quantum geometry systems.

## Active Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T27 | Rust Z₂ LGT framework | ✅ Complete | MEDIUM | 2026-06-25 | — | [Details](tasks/T27.md) |
| T20-Phase1 | Z₂ LGT 2D square lattice | 🔄 IN PROGRESS | HIGH | 2026-06-24 | T27 | [Details](tasks/T20.md) |
| T21 | Worker threads + checkpointing | ✅ Complete | MEDIUM | 2026-06-25 | — | [Details](tasks/T21.md) |
| T20-Phase2 | Sharp phase transition figures | 🔄 IN PROGRESS | HIGH | 2026-06-25 | T20-Phase1 | [Details](tasks/T20.md) |
| T20-Phase3 | 3D cubic lattice | 🔄 IN PROGRESS | HIGH | 2026-06-25 | T20-Phase1 | [Details](tasks/T20.md) |
| T20-Phase3b | Critical exponents (3D Z₂ LGT) | 🔴 NOT STARTED | HIGH | — | T20-Phase3 | [Details](tasks/T20-Phase3b.md) |
| T25 | Volume operator eigenvalues | ✅ Complete | MEDIUM | 2026-06-24 | — | [Details](tasks/T25.md) |
| **T22** | **Spin Foam Amplitudes** | **🟡 Ready** | **HIGH** | **2026-06-25** | **T20-Phase3** | **[Details](tasks/T22.md)** |

## Completed Tasks

### T20-Phase1 — Z₂ LGT 2D Square Lattice

**Data Collection**: 2026-06-25 (COMPLETE)
**Gap Analysis**: 2026-06-26 (IN PROGRESS — missing observables)
**Results**: L=16, 11 β values, 100k sweeps, errors ~0.0005
**Files**:
- `numerics/output/t20-phase1-worker-L16.json`
- `numerics/output/t27-rust-benchmark-L16-final.json` (Rust validation)
- `memory-bank/tasks/T20.md`
- `memory-bank/tasks/T27.md`

**Missing observables**:
- [ ] Wilson loop W(γ) for L = 4, 6, 8, 10, 12
- [ ] Critical exponents (ν ≈ 1, γ ≈ 1.75 for 2D Ising)
- [ ] Publication-ready figures

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

### T20-Phase2 — Finite-Size Scaling

**Data Collection**: 2026-06-25 (COMPLETE)
**Gap Analysis**: 2026-06-26 (IN PROGRESS — missing plots and analysis)
**Results**: L=8,12,16,20,24, 200k sweeps each, dense β grid
**Files**:
- `numerics/output/t20-p2-L*.json` (5 files)
- `numerics/data/registry.json`

**Missing observables**:
- [ ] Scaling collapse plot: L^(-γ/ν)χ vs L^(1/ν)(β-βc)
- [ ] Binder cumulant crossing analysis
- [ ] Correlation length ξ vs L at βc

**Key Results**:
- Binder cumulant approaches U* ≈ 0.66 (2D Ising)
- Plaquette converges to ⟨P⟩ ≈ 0.413 at β_c ≈ 0.44
- Total time: ~40 seconds (Rust, 4 workers)

### T20-Phase3 — 3D Cubic Lattice

**Data Collection**: 2026-06-25 (COMPLETE)
**Gap Analysis**: 2026-06-26 (IN PROGRESS — missing observables)
**Results**: L=4,6,8, 100k sweeps each, 10 β values
**Files**:
- `numerics/output/t20-p3-L4-3D-20250625.json`
- `numerics/output/t20-p3-L6-3D-20250625.json`
- `numerics/output/t20-p3-L8-3D-20250625.json`
- `numerics/docs/assets/t20-p3-*.png` (5 figures)

**Missing observables**:
- [ ] Wilson loops (area law vs perimeter law)
- [ ] String tension σ(L) from W(γ) ~ exp(-σ·Area)
- [ ] Critical exponents (ν ≈ 0.63, β ≈ 0.33 for 3D Ising)
- [ ] Finite-size scaling analysis

**Key Results**:
- Critical β ≈ 0.75 (L=8), converging to β_c ≈ 0.76
- Sharp first-order transition (plaquette jump Δβ ≈ 0.05)
- Binder cumulant U ≈ 0.666 (3D Ising)

## In Progress

### T20 (All Phases) — Missing Observables

**Status**: 🔄 IN PROGRESS (Gap analysis complete — missing observables identified)
**Identified**: 2026-06-26

**Missing observables by phase:**
- **Phase 1**: Wilson loops W(γ) — **NEEDS RE-RUN** (Rust code missing Wilson loop implementation, configs not saved), critical exponents (ν, γ)
- **Phase 2**: Scaling collapse plots, Binder crossing, correlation length ξ — can use existing data
- **Phase 3**: Wilson loops (area vs perimeter law) — **NEEDS RE-RUN**, string tension σ — **NEEDS RE-RUN**, critical exponents (ν, β)

**Corrected understanding (2026-06-26 night session):**
- Rust code (`rust-lattice/src/lib.rs`) has NO Wilson loop implementation
- Raw link configurations were NOT saved during simulation runs
- Existing JSON outputs contain only plaquette averages — cannot compute W(γ) retrospectively
- Must add Wilson loop to Rust code and re-run Phase 1 & 3 simulations
- ts-quantum has `wilsonLoop()` ready in `src/lattice/observables.ts` — logic can be ported to Rust
- Estimated Rust implementation + re-run time: ~2-3 hours

**Impact**: Without Wilson loops, cannot demonstrate area law (confinement) vs perimeter law (deconfinement). This is the central physics claim of the paper.

**Next**: Compute missing observables or proceed to T22 (Spin Foam).

---

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
*Last updated: 2026-06-26 04:55 IST*