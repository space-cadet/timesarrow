# timesarrow Project Memory Bank

## Project Overview

Timesarrow — quantum gravity simulation and visualization project. Monte Carlo simulations of lattice gauge theory, spin networks, and related quantum geometry systems.

## Active Tasks

| ID | Task | Status | Next |
|----|------|--------|------|
| T20-Phase1 | Z₂ LGT 2D square lattice | ✅ Complete | Phase 2 |
| T20-Phase2 | Sharp phase transition figures | 🔄 In Progress | Multi-lattice sweep |
| T25 | Volume operator eigenvalues | ✅ Complete | — |

## Decisions

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
