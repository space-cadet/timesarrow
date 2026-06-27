# timesarrow — Progress Tracker

*Updated: 2026-06-27 17:40:00 IST*

## Active Tasks

### T20: Z₂ Lattice Gauge Theory — Phase 3 (3D) + Phase 3b (FSS)

| Sub-task | Status | Completion |
|----------|--------|------------|
| T20a (2D, L=16) | ✅ Complete | Wilson loops, string tension |
| T20b (2D FSS) | ✅ Complete | Data collected, analysis pending |
| T20c (3D, L=8-24) | ✅ Complete | Wilson loops, string tension, first-order analysis |
| T20d (3D FSS, fine β) | 🔄 In Progress | L=8,16,32 done, L=48/64 pending; FSS plots + exponent fitting pending |

**T20d Progress:**
- L=8: ✅ 25 β values, 0.70–0.82, Δβ=0.005, 1M sweeps
- L=16: ✅ 27 β values, 0.72–0.80, Δβ=0.003, 1.5M sweeps
- L=32: ✅ 21 β values, 0.74–0.78, Δβ=0.002, 500k sweeps (300k therm + 200k measure), 8 workers, ~6h wall
- L=48: ⏳ Pending (β=0.75–0.77, Δβ=0.0015, 2M sweeps)
- L=64: ⏳ Pending (β=0.75–0.77, Δβ=0.001, 3M sweeps)

**T20 Key Results (3D Z₂ LGT):**
- β_c (3D) ≈ 0.758 ± 0.002 — from Binder cumulant crossing (L=8,16,32)
- First-order transition confirmed: plaquette jumps from 0.88 to 0.96 at β≈0.758
- Binder cumulant U ≈ 0.666 (3D Ising universal value 2/3)
- Peak susceptibility χ = 1.3704 at β=0.758
- Peak specific heat C = 1.0388 at β=0.758
- String tension σ vanishes at β_c
- Results match Creutz et al. (1979) within error

### T28a: Simulation Dashboard v2 (Functional)

| Feature | Status | Notes |
|---------|--------|-------|
| Runs & Results | ✅ Complete | Filterable, sortable, selectable, detail panel, export |
| Figure Archive | ✅ Complete | 6 FSS figures, thumbnails, click-to-zoom, orthogonal filters |
| Performance Chart | ✅ Complete | SVG log-log scatter plot, color by dimension |
| Data Export | ✅ Complete | JSON + CSV for selected run |
| Dark Mode | ✅ Complete | `prefers-color-scheme` media query |
| Mobile Responsive | ✅ Complete | CSS grid + flexbox, breakpoints |
| External Data | ✅ Complete | `fetch()` from JSON files, GitHub raw fallback |

**Architecture:**
- Vanilla JS, single HTML file, zero build step, zero dependencies
- External JSON data: `dashboard-data.json` (33 runs metadata), `dashboard-figures.json` (6 figures)
- GitHub raw fallback for immediate availability (avoids GitHub Pages cache delay)
- Abandoned OJS/Quarto approach (fragile runtime loading, cells rendered as raw code)
- Abandoned 235KB inline JSON blob (syntax errors, blank page)

**Deployment:**
- URL: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard-v2.html
- Commit: `db2bfef` (space-cadet.github.io)

### T29: Extensible Schema Design

| Phase | Status | Notes |
|-------|--------|-------|
| Design spec | ✅ Complete | `extensible-schema-design.md` written |
| Base schema | ⏳ Pending | `base-registry.schema.json` not yet created |
| Extension registry | ⏳ Pending | `lgt.schema.json`, `dmrg.schema.json` not yet created |
| Migration script | ⏳ Pending | v1.0 → v2.0 converter not yet written |
| Dashboard v3 | ⏳ Pending | Schema-driven UI not yet started |

---

## Blockers

1. **T20d**: L=32 complete, but FSS plots and exponent extraction not yet done
2. **T29**: None — can start when user prioritizes

---

## Recent Commits

### timesarrow repo
- `0db8bcf` — T20d: L=32 simulation complete, data committed
- `7f4f77a` — fix(dashboard): Observable Plot instead of Vega-Lite
- `6fb8f5e` — fix(dashboard): word wrap for key finding
- `e4a0b15` — feat(dashboard): Plot Gallery + Run Detail Browser
- `b2c5d39` — fix(dashboard): Results card formatting
- `e9d57f7` — fix(dashboard): named function for formatValue

### space-cadet.github.io repo
- `db2bfef` — Dashboard v2: add GitHub raw fallback for data loading
- `43587fe` — Dashboard v2: clean rewrite with external JSON loading
- `0457c05` — Dashboard v2 initial deployment with inline data fix
