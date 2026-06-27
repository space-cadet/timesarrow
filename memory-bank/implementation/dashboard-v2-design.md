# Dashboard v2 Design Specification

*Created: 2026-06-27 10:20:00 IST*
*Status: Design Complete | Implementation Pending*

## Overview

Enhanced simulation dashboard for TimesArrow numerics. Transforms the basic run listing into a full "one-stop simulation library" with performance metrics, data export, plot visualization, and live monitoring.

## Design Decisions

### Architecture: Integrated (Not Standalone)
- Dashboard lives within `timesarrow/numerics/docs/dashboard.qmd`
- Same Quarto + OJS + static JSON architecture as v1
- Modularity designed for future extraction if needed
- No backend server — GitHub Pages compatible

### Data Flow
```
Simulation Output (.json)
    ↓
collate-data.ts (extracts timing, performance, figures)
    ↓
registry.json (canonical)
    ↓
cp to docs/data-registry.json (synced for OJS FileAttachment)
    ↓
OJS dashboard (reactive, client-side rendering)
    ↓
Quarto render → HTML → GitHub Pages
```

## Enhanced Data Model

### Registry Run Fields (New)

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `wallTimeMs` | number | Total wall-clock time | `totalWallTimeMs` from Rust output |
| `cpuTimeMs` | number | CPU time (if available) | OS process accounting |
| `startTime` | ISO string | Actual run start | Python wrapper records |
| `endTime` | ISO string | Run completion | Python wrapper records |
| `betasCompleted` | number | β values done | `results.length` |
| `totalBetas` | number | Total β values | `parameters.betaValues.length` |
| `sweepsPerSecond` | number | Performance metric | `measureSweeps * betas / wallTime` |
| `figures` | string[] | Generated plot filenames | Scan `figures/` for `runId` prefix |
| `dataUrl` | string | Raw JSON path | `data/fss/<filename>.json` |

### Performance Object (New)
```json
{
  "benchmarks": {
    "L8": { "wallTime": 14.5, "sweepsPerSec": 1748 },
    "L16": { "wallTime": 83.9, "sweepsPerSec": 321 },
    "L32": { "wallTime": 540.0, "sweepsPerSec": 58 }
  }
}
```

## Dashboard Sections

### 1. Summary Cards (Enhanced)
- Total compute time (sum of all wall times)
- Average sweeps/sec
- Active runs count
- Tasks completed / total

### 2. Performance Chart (New)
- **Vega-Lite**: L vs wallTime (log-log scale)
- Shows scaling behavior: O(L^3) for 3D
- Color-coded by task
- Tooltip: exact wall time, sweeps/sec

### 3. Runs Table v2 (Enhanced)
- **Sortable columns**: task, runId, L, β, status, wallTime, date
- **Expandable rows**: Click → expand to show:
  - Full parameters (β range, sweeps, thermalization)
  - Per-β results table (β, plaquette, χ, Cv, U)
  - Performance metrics
  - Timestamps
- **Action buttons**: Download JSON, Download CSV, View Plots

### 4. Run Detail Modal (New)
```
┌─────────────────────────────────────────┐
│ Run: t20-p3b-L8-3D-fine-20260627       │
│ Status: ✅ Complete | Duration: 14m 35s  │
│ CPU: 23m 52s | β: 25/25 | Sweeps: 1M   │
├─────────────────────────────────────────┤
│ Timeline: [=======|----------] 14:35     │
│                                         │
│ Per-β Results (table):                  │
│ β     Plaquette   χ     Cᵥ    U         │
│ 0.70  0.5234      0.12  0.45  0.667    │
│ ...                                     │
│                                         │
│ [📥 Download JSON] [📥 Download CSV]    │
│ [🖼 View Plots] [📄 Open Task Page]     │
└─────────────────────────────────────────┘
```

### 5. Plot Gallery (New)
- Auto-discover PNG/SVG from `figures/` directory
- Match by runId prefix
- Inline thumbnails in modal
- Click → full-size view

### 6. Live Monitor (New)
- For currently running simulations
- Progress bar: `completed_betas / total_betas`
- ETA: `(elapsed / completed) * remaining`
- Elapsed wall time (auto-updating)
- Status: 🔄 Running | ⏸️ Paused | ✅ Complete

### 7. Task Pipeline (New)
- Visual flowchart: T20a → T20b → T20c → T20d
- Each node shows status emoji
- Arrows show dependencies
- Click node → filter runs to that task

## Session 2026-06-27: Prototype & Design Decisions

### What Was Built
1. **Static HTML Prototype** — `dashboard-prototype-static.html`
   - Unified "Runs & Results" section (table + detail panel in one place)
   - Figure Archive with orthogonal checkbox filters (Task × Dimension × Type)
   - Figure cards grouped by type (FSS/Raw/Analysis) with colored badges
   - Summary cards including new "Figures" count
   - No OJS — pure HTML/CSS, single file, works on GitHub Pages

2. **UX Analysis of Old Dashboard**
   - Three overlapping sections (All Runs, Plot Gallery, Run Detail Browser) confused users
   - Plot Gallery dropdown options were unclear ("Core" vs "Finite-Size Scaling" — same data, different aggregation)
   - Run Detail Browser had no direct link to which run you were viewing
   - Figure Archive was separate from runs — hard to trace provenance

### Key Design Decisions
- **Abandoned OJS/Vega-Lite approach** — OJS cells rendered as raw code on GitHub Pages, runtime loading is fragile
- **Adopted vanilla JS + static HTML** — single file, no build step, no dependencies, reliable
- **Data embedded as JSON blob** — fetch or inline `data-registry.json`
- **Old dashboard preserved** — `dashboard.html` untouched, no links to prototype

### What Comes Next
See `dashboard-v2-implementation-plan.md` for full plan.

