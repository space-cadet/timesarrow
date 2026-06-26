# T20: Simulation Dashboard

*Date: 2026-06-26*
*Applies to: numerics/docs/dashboard.qmd, space-cadet.github.io deployment*

## Purpose

Interactive web dashboard for browsing all TimesArrow simulation runs. Deployed at:
https://space-cadet.github.io/projects/timesarrow/numerics/dashboard.html

## Technology

- **Quarto** for static site generation
- **Observable JS (OJS)** for reactive filtering and tables
- **Bootstrap** for styling (cards, badges, tables)
- **GitHub Pages** for hosting

## Architecture

```
timesarrow/numerics/docs/dashboard.qmd
    → FileAttachment("data-registry.json")  [OJS runtime loads data]
    → Observable Inputs (filters)
    → Observable Inputs.table (display)
    → _site/dashboard.html
    → space-cadet.github.io/projects/timesarrow/numerics/dashboard.html
```

## Data Flow

1. **Source of truth**: `numerics/data/registry.json` (updated by collate script)
2. **Snapshot for build**: `numerics/docs/data-registry.json` (copied from source)
3. **Dashboard loads**: `FileAttachment("data-registry.json")` — relative path from `.qmd` location

## Features

### Summary Cards
- Total runs count
- Number of distinct tasks
- Number of distinct phases
- Completion status count

### Interactive Filters
- **Task dropdown**: All, T20, T25, T27, ...
- **Phase dropdown**: All, phase1, phase2, phase3, phase3b
- **Search box**: Filters by runId, description, or keyFinding

### Runs Table
Columns: Run ID, Task, Phase, L, β Range, Date, Status, Key Finding, Output

### Task Breakdown
Per-task summary with phase list and completion counts.

### Recent Activity
Last 10 runs chronologically.

## Build & Deploy Workflow

```bash
# 1. Update registry
cd numerics
npx ts-node --esm src/scripts/collate-data.ts

# 2. Copy snapshot for dashboard build
cp data/registry.json docs/data-registry.json

# 3. Render dashboard
quarto render docs/dashboard.qmd --to html

# 4. Copy to deployment
cp docs/dashboard.html ../space-cadet.github.io/projects/timesarrow/numerics/
cp docs/dashboard_files/* ../space-cadet.github.io/projects/timesarrow/numerics/dashboard_files/
cp docs/data-registry.json ../space-cadet.github.io/projects/timesarrow/numerics/

# 5. Commit and push both repos
git add -A && git commit -m "deploy: Update dashboard" && git push
```

## Known Issues (2026-06-26)

⚠️ **Dashboard rendering broken on live site.** The OJS runtime files (`dashboard_files/libs/quarto-ojs/`) were not copied in the initial deployment. Fixed by copying `dashboard_files/` directory, but the page may still have loading issues. Needs verification.

### OJS Runtime Loading

The dashboard requires these JS files to be served alongside `dashboard.html`:
- `dashboard_files/libs/quarto-ojs/quarto-ojs-runtime.js`
- `dashboard_files/libs/bootstrap/bootstrap.min.css`
- `dashboard_files/libs/observablehq/`

If these return 404, the dashboard shows a blank page.

## Future Improvements

1. **Auto-refresh**: GitHub Action to rebuild dashboard on registry update
2. **Plot integration**: Embed matplotlib plots directly in dashboard
3. **Run comparison**: Side-by-side comparison of two runs
4. **Export**: Download filtered data as CSV
