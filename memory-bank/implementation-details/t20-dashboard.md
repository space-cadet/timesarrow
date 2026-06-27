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

## Known Issues (2026-06-26 → FIXED 2026-06-27)

### ✅ FIXED: Single-Quote JSON Parsing Error
**Problem**: Inline OJS `{ojs} new Date(registry.lastUpdated).toLocaleString('en-GB')}` used single quotes. Quarto base64-encodes OJS modules into JSON strings, but escapes single quotes as `\'` — which is **not a valid JSON escape sequence** (JSON only allows `\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, `\uXXXX`).

**Fix**: Changed `'en-GB'` to `"en-GB"` in both `docs/dashboard.qmd` and `pages/dashboard.qmd`.

**Commits**: `752449e` (timesarrow), `c29db61` (space-cadet.github.io)

### ✅ FIXED: Summary Cards Not Rendering
**Problem**: Inline OJS expressions like `{ojs} totalRuns` inside raw HTML blocks (`<div class="card"><h3>...</h3></div>`) were not processed by the OJS runtime. They remained as literal text `{ojs} totalRuns` instead of being replaced with values.

**Root Cause**: Quarto's OJS inline expression syntax `{ojs} expr` only works in **markdown text contexts**, not inside raw HTML blocks.

**Fix**: Replaced the grid of HTML cards with a single OJS cell using `html\`\` ` tagged template literal:
```ojs
html`<div class="row">
  ${[[totalRuns, "Total Runs"], ...].map(([value, label]) => html`
    <div class="col-3">...
  `)}
</div>`
```

**Commits**: `5167509` (timesarrow), `c2a95d9` (space-cadet.github.io)

### ✅ FIXED: Recent Activity Shows `[object HTMLSpanElement]`
**Problem**: Recent Activity used `htl.html` + `.join('')` which stringifies DOM nodes to `[object HTMLSpanElement]`.

**Fix**: Replaced with `html\`\` ` tagged template (no `.join()` needed):
```ojs
html`<div class="list-group">
  ${recentRuns.map(r => html`
    <div class="list-group-item">...</div>
  `)}
</div>`
```

**Commits**: `5167509` (timesarrow), `c2a95d9` (space-cadet.github.io)

## OJS Best Practices (Learned 2026-06-27)

| Pattern | Works? | Notes |
|---------|--------|-------|
| `{ojs} expr` in markdown text | ✅ Yes | Inline expression, processed by OJS runtime |
| `{ojs} expr` inside HTML blocks | ❌ No | Use pure OJS `html\`\` ` cell instead |
| `html\`\` ` tagged template | ✅ Yes | Generates proper DOM, use in OJS cells |
| `htl.html` + `.join('')` | ❌ No | Stringifies DOM nodes; use `html\`\` ` instead |
| Single quotes in inline OJS | ❌ No | JSON parse error; use double quotes |
| Double quotes in inline OJS | ✅ Yes | Safe for JSON encoding |

## Verification

Live dashboard confirmed working: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard.html?nocache=1

Snapshot shows:
- ✅ Summary callout (Project/Schema/Last Updated)
- ✅ Summary cards (33 Total Runs, 4 Tasks, 5 Phases, 33 Complete)
- ✅ Filters (Task/Phase/Search dropdowns)
- ✅ Runs table with all data
- ✅ Task Breakdown section
- ✅ Recent Activity list

## Future Improvements

1. **Auto-refresh**: GitHub Action to rebuild dashboard on registry update
2. **Plot integration**: Embed matplotlib plots directly in dashboard
3. **Run comparison**: Side-by-side comparison of two runs
4. **Export**: Download filtered data as CSV
