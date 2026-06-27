# timesarrow — Active Context

*Updated: 2026-06-27 17:40:00 IST*

## Current Session — 2026-06-27 Evening

### T28a: Dashboard v2 — FUNCTIONAL ✅ COMPLETE

**What was built:**
- Full vanilla JS dashboard with 3 tabs: Runs & Results, Figure Archive, Performance
- 14 runs loaded from external JSON (with GitHub raw fallback for immediate availability)
- Filterable, sortable runs table with row selection and detail panel
- Detail panel: Parameters, Results, Key Findings, Timing, Export (JSON/CSV)
- 6 FSS figures with thumbnails, click-to-zoom modal, orthogonal filters
- Performance chart: SVG log-log scatter plot (Wall time vs Lattice Size)
- Dark mode via `prefers-color-scheme`, mobile responsive

**Deployment:**
- URL: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard-v2.html
- Repo: space-cadet.github.io (GitHub Pages)
- Commit: `db2bfef`

**Architecture decisions:**
- External JSON files instead of inline data (235KB blob caused syntax errors)
- GitHub raw fallback for data files (GitHub Pages cache delay ~5min)
- Vanilla JS over React: faster iteration, no build step, sufficient for current features

### T20d: L=32 Simulation — COMPLETE ✅
- **Run ID:** `t20-p3b-L32-lean-20260627`
- **Status:** Complete, data committed to `numerics/data/fss/`
- **Results:** Peak χ=1.3704 at β=0.758, Peak C=1.0388 at β=0.758, Binder U≈0.666
- **Plaquette:** First-order jump from ~0.88 to ~0.96 at β≈0.758
- **Wall time:** ~6h total (distributed across 8 workers)

### T29: Extensible Schema Design — PENDING ⬜
- Status: Pending, not started
- Goal: Physics-agnostic base schema + extension namespaces for any simulation domain
- Key idea: `extensions: { lgt: {...}, dmrg: {...} }` in base schema
- See: `memory-bank/implementation/extensible-schema-design.md`

---

## T20 — Status (Updated 2026-06-27)

| Phase | Description | Data Status | Analysis Status | Key Missing |
|-------|-------------|-------------|-----------------|-------------|
| T20a | 2D square, L=16 | ✅ Data collected | ✅ Wilson loops complete | Critical exponents |
| T20b | 2D finite-size scaling | ✅ Data collected | 🔄 Missing analysis | Scaling collapse, Binder crossing, ξ |
| T20c | 3D cubic lattice | ✅ Data collected | ✅ Wilson loops & string tension complete | Critical exponents |
| T20d | FSS critical exponent extraction | ✅ L=8,16,32 complete | 🔄 Scripts ready | L=48,64; FSS plots; exponent fitting |

### Critical Finding (2026-06-27)

**3D Z₂ LGT first-order transition CONFIRMED:**
- L=32 plaquette jumps from 0.878 to 0.965 at β≈0.758 (Δβ≈0.001)
- Binder cumulant converges to 2/3 (3D Ising universal value)
- Peak susceptibility χ=1.3704 at β=0.758
- Critical βₑ ≈ 0.758 ± 0.002

**Remaining work:** 
- Generate FSS comparison plots (L=8,16,32 overlay)
- Extract critical exponents (ν, γ, α) from scaling
- Start L=48/64 if needed for thermodynamic limit

---

## What's Next (Updated 2026-06-27)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T20d** | **Generate FSS plots (L=8,16,32 overlay)** | L=32 completion |
| 2 | **T20d** | **Critical exponent fitting (ν, γ, β, α)** | FSS plots |
| 3 | **T29** | **Extensible schema design** | — |
| 4 | T20d | Start L=48/64 if needed for better extrapolation | L=32 analysis |
| 5 | T20b | Scaling collapse plots (existing 2D data) | — |
| 6 | T22 | Spin Foam Amplitudes — single vertex computation | T20 |
| 7 | T23 | Entanglement entropy — needs T22 completion | T22 |

**Key decision:** T28a complete. T20d L=32 complete. Next priority is FSS analysis and exponent extraction, then T29 schema work when user prioritizes it.
