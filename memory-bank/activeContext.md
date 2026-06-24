# timesarrow — Active Context

*Updated: 2026-06-24*

## Current Focus

**T20-Phase2**: Making the Z₂ LGT phase transition sharp in figures.

Phase 1 is complete (single L=8 lattice, basic ⟨P⟩ vs β plot). The transition is visible but smooth — expected for a second-order transition on a small lattice. Phase 2 will show it clearly via:

- Multi-lattice finite-size scaling (L=8, 16, 32)
- Higher-order observables (susceptibility, Binder cumulant, specific heat)
- Dense β sampling near βc = 0.4407
- CPU parallelization across 6 cores

## Immediate Next Step

Implement the observables extensions in `ts-quantum` and run the multi-lattice sweep. Estimated time: 3 minutes for Phase 2A.

## Blockers

None. All dependencies (ts-quantum lattice module, simulation scripts) are in place.

## Key Decisions (this session)

- **GPU not needed**: CPU parallelization of independent simulations gives same speedup with zero complexity.
- **Phase 2A first**: L=8,16,32 with 100k+500k sweeps. If peaks sharpen clearly, proceed to 2B/2C as needed.
- **Observable priority**: Binder cumulant crossing is the most visually convincing signature.

## Files in Play

| File | Role |
|------|------|
| `ts-quantum/src/lattice/observables.ts` | Add P², P⁴, Binder, C, χ |
| `numerics/src/scripts/t20-phase2.ts` | Multi-lattice parallel sweep |
| `numerics/docs/tasks/t20-z2-lgt.qmd` | Update with Phase 2 results |
| `numerics/docs/assets/t20-*.png` | New plots (4 figures) |

---

*See `memory-bank/tasks/T20-Phase2-sharp-transition.md` for full plan.*
