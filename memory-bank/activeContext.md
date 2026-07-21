# timesarrow — Active Context

*Updated: 2026-07-21 14:56:49 IST*

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

## T35b Diamond-Lattice Existence Test 🔄

T35b now makes the 3D construction question explicit. It first requires a correct four-valent square-lattice vertex/edge mapping and intertwiner-preservation test, then a minimal periodic diamond-cluster test. The diamond 2-skeleton is sufficient for these first gates; missing 3-cells block bulk-topology claims.

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T35b** | Diamond CZX existence test | 🔄 | T33a, T35a |
| 2 | **T35a** | Boundary MPUO + parent Hamiltonian | 🔄 | — |
| 3 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 4 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 5 | T32 | Rust 2024 reproducibility | 🔄 | — |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
