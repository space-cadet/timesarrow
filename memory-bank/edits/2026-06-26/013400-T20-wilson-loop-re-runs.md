---
kind: edit_chunk
id: T20-wilson-loop-re-runs-20260626
created_at: 2026-06-26 01:34:00 IST
task_ids: [T20]
source_branch: main
source_commit: unknown
---

#### 01:34:00 IST - T20: Re-ran Phase 1 & 3 with Wilson loop measurements
- Modified `rust-lattice/src/lib.rs` - Added `wilson_loop_2d()`, `average_wilson_loop_2d()`, `wilson_loop_xy_3d()`, `average_wilson_loop_xy_3d()`, `measure_with_wilson_loops()`, `simulate_beta_with_wilson_loops()`
- Modified `rust-lattice/src/main.rs` - Added loop size parameter and Wilson loop JSON output
- Re-ran Phase 1 (2D, L=16): `numerics/output/t20-p1-L16-wilson-20250626.json` with loop sizes 1x1, 2x2, 4x4, 6x6, 8x8
- Re-ran Phase 3 (3D, L=8): `numerics/output/t20-p3-L8-3D-wilson-20250626.json` with loop sizes 1x1, 2x2, 3x3, 4x4
- Updated `memory-bank/tasks/T20.md` - Updated status to show Wilson loops now available
- Updated `memory-bank/progress.md` - Marked Wilson loops as complete
- Updated `memory-bank/tasks.md` - Updated T20 status
- Updated `memory-bank/session_cache.md` - Updated with completion of Wilson loop re-runs
