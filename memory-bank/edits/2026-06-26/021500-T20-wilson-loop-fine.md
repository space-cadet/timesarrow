---
kind: edit_chunk
id: T20-wilson-loop-fine-20260626
created_at: 2026-06-26 02:15:00 IST
task_ids: [T20]
source_branch: main
source_commit: unknown
---

#### 02:15:00 IST - T20: Re-ran Phase 3 with fine-grained beta spacing for smoother transition plots
- Created `numerics/output/t20-p3-L8-3D-wilson-fine-20250626.json` - 21 beta values with fine spacing (0.30-1.20, concentrated around critical region 0.65-0.86)
- Created `numerics/src/scripts/t20-plot-wilson-fine.py` - Python matplotlib script for high-resolution plots
- Re-generated `numerics/docs/assets/t20-p3-string-tension.png` - Smoother σ(β) curve with 21 data points
- Re-generated `numerics/docs/assets/t20-p3-string-tension.svg` - Vector version
- Re-generated `numerics/docs/assets/t20-p3-wilson-loops.png` - Wilson loop curves with finer β resolution
- Re-generated `numerics/docs/assets/t20-p3-wilson-loops.svg` - Vector version
- Modified `numerics/docs/tasks/t20-z2-lgt.qmd` - Updated data file reference to fine-grained dataset
- Updated `space-cadet.github.io` repo - Deployed new plots and HTML (commits 3b3b767, 793bc47)
- Created `memory-bank/edits/2026-06-26/021500-T20-wilson-loop-fine.md` - Canonical edit chunk for fine-grained re-run
