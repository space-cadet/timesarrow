# timesarrow — Progress Tracker

*Updated: 2026-06-27 12:30:00 IST*

## Active Tasks

### T20: Z₂ Lattice Gauge Theory — Phase 3 (3D) + Phase 3b (FSS)

| Sub-task | Status | Completion |
|----------|--------|------------|
| T20a (2D, L=16) | ✅ Complete | Wilson loops, string tension |
| T20b (2D FSS) | 🔄 Partial | Data collected, analysis pending |
| T20c (3D, L=8-24) | ✅ Complete | Wilson loops, string tension, first-order analysis |
| T20d (3D FSS, fine β) | 🔄 In Progress | L=8,16 done, L=32 running, L=48/64 pending |

**T20d Progress:**
- L=8: ✅ 25 β values, 0.70–0.82, Δβ=0.005, 1M sweeps
- L=16: ✅ 27 β values, 0.72–0.80, Δβ=0.003, 1.5M sweeps
- L=32: 🔄 21 β values, 0.74–0.78, Δβ=0.002, 2M sweeps, ~4h remaining
- L=48: ⏳ Pending (β=0.75–0.77, Δβ=0.0015, 2M sweeps)
- L=64: ⏳ Pending (β=0.75–0.77, Δβ=0.001, 3M sweeps)

**T20 Key Results:**
- β_c (3D) ≈ 0.7613(2) — matches Creutz et al. (1979)
- First-order transition confirmed (Binder cumulant exponent ≈ -3)
- String tension σ vanishes at β_c

### T28: Simulation Dashboard

| Feature | Status | Notes |
|---------|--------|-------|
| v1 (basic) | ✅ Complete | Summary, filters, table, task breakdown |
| v2 Phase 1 (data model) | ✅ Complete | Schema v2.0.0, timing fields, 25 runs |
| v2 Phase 2 (UI) | 🔄 Nearly Complete | Gallery, detail browser, charts, cards |
| v2 Phase 3 (deploy) | ✅ Complete | Live on GitHub Pages |

**v2 Remaining:**
- Expandable rows with per-β details
- Data Export buttons (CSV/JSON)
- Live Monitor for running simulations
- Task Pipeline flowchart

---

## Blockers

1. **T20d L=32**: ~4 hours remaining — no action needed, just wait
2. **T28**: None — can continue implementing remaining features

---

## Recent Commits

### timesarrow repo
- `7f4f77a` — fix(dashboard): Observable Plot instead of Vega-Lite
- `6fb8f5e` — fix(dashboard): word wrap for key finding
- `e4a0b15` — feat(dashboard): Plot Gallery + Run Detail Browser
- `b2c5d39` — fix(dashboard): Results card formatting
- `e9d57f7` — fix(dashboard): named function for formatValue

### space-cadet.github.io repo
- `e9d57f7` — Dashboard v2 deployed (same commits as above, copied)
