# timesarrow — Active Context

*Updated: 2026-06-27 12:30:00 IST*

## Current Session — 2026-06-27 Afternoon

### T28: Dashboard v2 — UX ANALYSIS + PROTOTYPE ✅

**User Feedback on Old Dashboard:**
- Plot Gallery dropdown options unclear ("Core" vs "Finite-Size Scaling" — same data, different aggregation)
- Three overlapping sections confuse users (All Runs, Plot Gallery, Run Detail Browser)
- Run Detail Browser has no link to selected run

**Prototype Built:** `dashboard-prototype-static.html`
- ✅ Unified "Runs & Results" (table + detail panel in one section)
- ✅ Figure Archive with orthogonal filters (Task × Dimension × Type)
- ✅ Figure cards grouped by type with colored badges (FSS/Raw/Analysis)
- ✅ Static HTML/CSS, single file, no dependencies
- ❌ Not yet functional (filters don't filter, rows don't click, figures are placeholders)

**Architecture Decision:** Abandoned OJS/Quarto approach (fragile on static hosting). Adopted vanilla JS + static HTML.

**Live URL**: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard-prototype-static.html

### T28a: Dashboard v2 — Functional JS Implementation (NEW)
- Status: pending
- Goal: Make prototype interactive (filtering, row selection, figure loading, data export)
- Est. time: ~1.25 hours
- See: `dashboard-v2-implementation-plan.md`

### T29: Extensible Numerics Schema Design (NEW)
- Status: pending
- Goal: Design base+extension schema for general numerics dashboard (not LGT-specific)
- Key idea: Physics-agnostic base schema + extension namespaces (`lgt`, `dmrg`, etc.)
- See: `extensible-schema-design.md`

### T20d: L=32 Simulation — STILL RUNNING
- **PID 49975**: Started 10:31 IST
- **Status**: ~2h elapsed at session start, still running
- **No checkpoint yet** — first checkpoint expected in ~15-20 min
- **Total estimate**: ~6 hours wall time

---

## T20 — Status (Updated 2026-06-27)

| Phase | Description | Data Status | Analysis Status | Key Missing |
|-------|-------------|-------------|-----------------|-------------|
| T20a | 2D square, L=16 | ✅ Data collected | ✅ Wilson loops complete | Critical exponents |
| T20b | 2D finite-size scaling | ✅ Data collected | 🔄 Missing analysis | Scaling collapse, Binder crossing, ξ |
| T20c | 3D cubic lattice | ✅ Data collected | ✅ Wilson loops & string tension complete | Critical exponents |
| T20d | FSS critical exponent extraction | ✅ L=8,16 complete, L=32 running | 🔄 Scripts ready | L=32,48,64 completion |

### Critical Finding (2026-06-26)

**Wilson loops and string tension**: ✅ COMPLETE
**First-order transition**: Evidence from Binder cumulant scaling (exponent ≈ -3)

**Remaining work**: Complete L=32,48,64 fine-grid runs; critical exponent fitting; thermodynamic limit extrapolation

---

## What's Next (Updated 2026-06-27)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T20d** | **Monitor L=32 simulation** | — |
| 2 | **T28a** | **Functional JS dashboard** | — |
| 3 | **T29** | **Extensible schema design** | — |
| 4 | T20d | Start L=48/64 when L=32 completes | L=32 |
| 5 | T20d | Critical exponent fitting (ν, γ, β, α) | L=32,48,64 |
| 6 | T20b | Scaling collapse plots (existing data) | — |
| 7 | T22 | Spin Foam Amplitudes — single vertex computation | T20 |
| 8 | T23 | Entanglement entropy — needs T22 completion | T22 |

**Key decision**: T20d L=32 is running. T28a and T29 can proceed in parallel.
