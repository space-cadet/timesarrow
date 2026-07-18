# timesarrow — Active Context

*Updated: 2026-07-18*

## T33a Foundation Validated 🔄

The reusable Z₂ boundary-operator API and connected diamond 2-skeleton are built and tested. Diamond 3-cells and general-complex Monte Carlo integration remain open; see `implementation/T33a-cell-complex-api.md` for the exact boundary.

## T35a Local CZX Audit — Partial Results ⚠️

`ts-quantum` contains a controlled-Z primitive and a local four-qubit CZX audit. The literal CZX on-site operator squares to identity but leaks out of the SU(2) intertwiner subspace, confirming the operator-level obstruction.

**New finding (2D toy model):** A 2-valent toy model (not the correct 4-valent geometry) shows that the gauge-invariant state IS a CZX +1 eigenvector. However, this result is not physically applicable because the proper 2D square lattice requires 4-valent vertices with 2D intertwiner spaces. The correct 4-valent analysis is pending.

**Theory docs created:**
- `theory/docs/czx-intertwiner-analysis.md` — Detailed analysis
- `theory/docs/index.md` — Theory index
- `theory/pages/dashboard.html` — Theory dashboard

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T35a** | Correct 4-valent 2D analysis | 🔄 | — |
| 2 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 3 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 4 | T32 | Rust 2024 reproducibility | 🔄 | — |
| 5 | T29 | Extensible schema design | ⏳ | T32 |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
