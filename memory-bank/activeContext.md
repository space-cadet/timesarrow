# timesarrow — Active Context

*Updated: 2026-07-18*

## T33a Foundation Validated 🔄

The reusable Z₂ boundary-operator API and connected diamond 2-skeleton are built and tested. Diamond 3-cells and general-complex Monte Carlo integration remain open; see `implementation/T33a-cell-complex-api.md` for the exact boundary.

## T35a Local CZX Audit Started 🔄

`ts-quantum` now contains a controlled-Z primitive and a local four-qubit CZX audit. The literal CZX on-site operator squares to identity but leaks out of the $SU(2)$ intertwiner subspace, confirming that the LQG-CZX relation remains structural rather than a literal operator action. The next T35a gate is a minimal many-vertex candidate state, not a toric-code projector.

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 2 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 3 | **T35a** | Microscopic construction audit | ⏳ | T33a |
| 4 | T32 | Rust 2024 reproducibility | 🔄 | — |
| 5 | T29 | Extensible schema design | ⏳ | T32 |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
