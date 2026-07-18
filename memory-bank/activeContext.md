# timesarrow — Active Context

*Updated: 2026-07-18*

## T33a Foundation Validated 🔄

The reusable Z₂ boundary-operator API and connected diamond 2-skeleton are built and tested. Diamond 3-cells and general-complex Monte Carlo integration remain open; see `implementation/T33a-cell-complex-api.md` for the exact boundary.

## T35a CZX Construction — Many-Body Results ✅

Explicit construction of the CZX SPT state completed on single plaquette and 2×2 torus (16 qubits). Key results:
- Single plaquette: $|\Psi\rangle = (|0000\rangle + |1111\rangle)/\sqrt2$ is exact +1 eigenvector of $U_{CZX}$
- Open plaquette: boundary signature shows relative sign ($\langle\Psi|U|\Psi\rangle = 0$)
- 2×2 torus: **global** $\prod_s U_{CZX,s}$ preserves state; single-site does NOT
- CZ cancellation on shared links is the mechanism (each link gets CZ twice)

Code: `numerics/scripts/t35a-czx-construction-verify.py` (numpy, exact state-vector).
Theory doc updated: `theory/docs/czx-intertwiner-analysis.md`.

**Open threads:** boundary MPUO / 3-cocycle, parent Hamiltonian, ts-quantum cross-check, 3D generalization.

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T35a** | Boundary MPUO + parent Hamiltonian | 🔄 | — |
| 2 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 3 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 4 | T32 | Rust 2024 reproducibility | 🔄 | — |
| 5 | T29 | Extensible schema design | ⏳ | T32 |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
