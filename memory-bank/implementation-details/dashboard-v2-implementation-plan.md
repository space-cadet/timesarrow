# Dashboard v2 Implementation Plan

*Created: 2026-06-27*
*Updated: 2026-06-27 (post-prototype)*
*Based on: v2 Design Specification + Current Dashboard Analysis*
*Tasks: T28 (Dashboard), T28a (Functional JS Implementation)*

## Current State

### Old Dashboard (`dashboard.html` — preserved)
- ✅ Summary cards, filters, runs table, task breakdown, recent activity
- ❌ Three overlapping sections confuse users (All Runs, Plot Gallery, Run Detail Browser)
- ❌ Plot Gallery dropdown unclear ("Core" vs "Finite-Size Scaling" — same data, different aggregation)
- ❌ Run Detail Browser has no link to selected run
- ❌ No expandable rows, no live monitoring, no data export

### Prototype Built (`dashboard-prototype-static.html`)
- ✅ Unified "Runs & Results" section (table + detail panel)
- ✅ Figure Archive with orthogonal filters (Task × Dimension × Type)
- ✅ Figure cards grouped by type with colored badges (FSS/Raw/Analysis)
- ✅ Summary cards with "Figures" count
- ❌ Static only — no interactivity (filters don't filter, rows don't click, figures show placeholders)

## Architecture Decision: Vanilla JS + Static HTML

**Abandoned:** OJS + Quarto approach
- OJS cells rendered as raw code on GitHub Pages
- Runtime loading is fragile and hard to debug
- Quarto build step adds complexity

**Adopted:** Single `.html` file with embedded JSON data + vanilla JavaScript
- No build step, no dependencies
- Works on any static host (GitHub Pages, Netlify, etc.)
- Easy to debug and extend
- Data embedded as JSON blob or fetched from `data-registry.json`

## Prioritized Implementation Plan

### Phase 1: Functional JS Core (~30 min)
**Goal:** Make the prototype interactive.

**Changes to `dashboard-prototype-static.html` → `dashboard-v2.html`:**

1. **Embed or fetch registry data**
   - Option A: Inline JSON blob (works offline, single file)
   - Option B: `fetch('data-registry.json')` (smaller file, auto-updates)
   - Hybrid: Try fetch, fallback to inline

2. **Table filtering**
   - Task dropdown filters rows
   - Phase dropdown filters rows
   - Search box filters by runId, description, or key finding
   - Real-time update (no page reload)

3. **Row selection → Detail Panel**
   - Click row → highlight, show detail panel
   - Detail panel populates from selected run's data
   - Shows: parameters, results, timing, figure links

4. **Figure filtering**
   - Checkboxes filter figures by Task, Dimension, Type
   - Figure cards show actual images (fix paths to deployed PNGs)
   - "Source: N runs" dynamically computed

### Phase 2: Data Export + Performance (~20 min)
**Goal:** Enable data download and scaling visualization.

5. **Download buttons**
   - Per-run: "Download JSON" (raw data), "Download CSV" (per-β table)
   - Uses `Blob` + `URL.createObjectURL`

6. **Performance chart**
   - Simple canvas or SVG scatter plot: L vs wallTime (log-log)
   - Color by dimension
   - No heavy charting library needed for a scatter plot

### Phase 3: Polish (~15 min)
**Goal:** Make it feel finished.

7. **Tab switching** (Runs Table ↔ Detail Panel)
   - Mobile-friendly: tabs instead of side-by-side

8. **Loading states**
   - "Loading..." while fetching registry
   - Image placeholders while figures load

9. **Dark mode**
   - CSS `prefers-color-scheme` support

## File Locations

| File | Purpose | Status |
|------|---------|--------|
| `dashboard.html` | Old dashboard (preserved) | ✅ Live |
| `dashboard-prototype-static.html` | Static layout mockup | ✅ Deployed |
| `dashboard-v2.html` | Functional JS version (target) | ⬜ Phase 1 |
| `data-registry.json` | Data source | ✅ Exists |
| `figures/*.png` | Generated plots | ✅ Deployed |

## Registry Updates Needed

1. **Add figure references** to runs that generated figures
2. **Add missing runs:** L=8 fine (complete), L=16 fine (partial), L=32 lean (when complete)
3. **Ensure all runs have** `wallTimeMs`, `sweepsPerSecond` for performance chart

## Implementation Order

| Step | Task | Est. Time | Depends On |
|------|------|-----------|------------|
| 1 | Embed/fetch registry data in HTML | 5 min | — |
| 2 | Implement table filtering (Task/Phase/Search) | 10 min | Step 1 |
| 3 | Implement row selection + detail panel | 10 min | Step 1 |
| 4 | Implement figure filtering | 10 min | Step 1 |
| 5 | Fix figure paths to deployed PNGs | 5 min | — |
| 6 | Add download buttons | 10 min | Step 3 |
| 7 | Add performance chart | 10 min | Step 1 |
| 8 | Polish: tabs, loading, dark mode | 15 min | — |
| **Total** | | **~1.25 hours** | |

## Recommended Next Steps

1. **Immediate:** Implement Phase 1 (functional JS core) — makes prototype fully usable
2. **Next session:** Phase 2 (export + performance chart)
3. **When ready:** Replace `dashboard.html` with `dashboard-v2.html` (or keep both, link from nav)
4. **Parallel:** T29 — Extensible Schema Design (separate track, see `extensible-schema-design.md`)

## Notes

- Old dashboard stays live at `dashboard.html` until v2 is tested and approved
- No Quarto dependency for v2 — pure static HTML
- Migration to standalone app later is straightforward: extract HTML + JS, add backend
