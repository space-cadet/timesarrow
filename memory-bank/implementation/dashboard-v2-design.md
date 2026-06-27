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

## Implementation Plan

### Phase 1: Data Model (30 min)
1. Update `collate-data.ts` to extract timing from output JSON
2. Update `registry.schema.json` with new fields
3. Regenerate `data/registry.json` with enhanced fields
4. Sync to `docs/data-registry.json`

### Phase 2: Dashboard UI (60 min)
1. Rewrite `dashboard.qmd` with new sections
2. Create `dashboard-detail.js` OJS module
3. Implement expandable rows for runs table
4. Implement performance chart (Vega-Lite)
5. Add download buttons (JSON/CSV)
6. Implement plot gallery discovery

### Phase 3: Polish & Deploy (30 min)
1. Test with T20d data (L=8, 16, 32)
2. Quarto render to HTML
3. Copy to space-cadet.github.io
4. Commit and push
5. Verify live deployment

## File Inventory

| File | Purpose | Status |
|------|---------|--------|
| `numerics/docs/dashboard.qmd` | Main dashboard | 🔄 Rewrite needed |
| `numerics/docs/data-registry.json` | Synced data | 🔄 Auto-generated |
| `numerics/data/registry.json` | Canonical registry | 🔄 Update schema |
| `numerics/data/registry.schema.json` | Schema validation | 🔄 Add fields |
| `numerics/src/scripts/collate-data.ts` | Data extraction | 🔄 Add timing |
| `numerics/src/scripts/figure-discovery.ts` | Plot discovery | ⬜ Create new |
| `memory-bank/implementation/dashboard-v2-design.md` | This document | ✅ Created |

## Dependencies
- No new dependencies
- Uses existing: Quarto, OJS, Vega-Lite, htl
- Browser-native: Fetch API, Blob for downloads

## Future Extraction Path
If needed for ts-quantum or other projects:
1. Extract `dashboard.qmd` → standalone repo
2. Generalize registry schema (remove physics-specific fields)
3. Make task pipeline configurable
4. Keep same OJS + Vega-Lite stack
