# Edit Chunk — 2026-06-27 Dashboard Fix

#### 06:12 IST — T28: Dashboard JSON Parsing & Rendering Fix

**Files Modified:**
- `numerics/docs/dashboard.qmd` — Fixed inline OJS single quotes, converted summary cards to pure OJS cell
- `numerics/pages/dashboard.qmd` — Fixed inline OJS single quotes, converted summary cards and recent activity to pure OJS cells
- `numerics/docs/dashboard.html` — Re-rendered
- `numerics/pages/dashboard.html` — Re-rendered
- `space-cadet.github.io/projects/timesarrow/numerics/dashboard.html` — Deployed fix

**Changes:**
1. **Single quotes → double quotes**: Inline OJS `{ojs} new Date(...).toLocaleString('en-GB')` caused JSON parse error because `\'` is not a valid JSON escape sequence. Changed to `"en-GB"`.
2. **Summary cards**: Inline OJS inside HTML blocks (`<div class="card"><h3>{ojs} totalRuns</h3>`) doesn't work — OJS runtime doesn't process expressions inside raw HTML. Converted to a single OJS `html\`\` ` cell that generates the entire card grid.
3. **Recent Activity**: `htl.html` + `.join('')` stringifies DOM nodes to `[object HTMLSpanElement]`. Changed to `html\`\` ` tagged template which properly renders DOM.

**Commits:**
- `timesarrow`: `752449e`, `5167509`
- `space-cadet.github.io`: `c29db61`, `c2a95d9`

**Verification:** Dashboard renders correctly with 33 total runs, 4 tasks, 5 phases, 33 complete.
