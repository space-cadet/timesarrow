# Edit History

*Last Updated: 2026-07-10 19:05 IST*

---

## 2026-07-10

#### 18:40:44 IST - T32: Clarified remaining correction tasks and recorded stale GitHub Pages numerics deployment.
- Modified `memory-bank/tasks/T31.md` - Updated T31 correction checklist to match resolved source-level work and remaining validation blockers.
- Modified `memory-bank/tasks/T32.md` - Expanded T32 acceptance criteria, including deployment synchronization.
- Modified `memory-bank/activeContext.md` - Added deployment audit finding and next-session priority.
- Modified `memory-bank/progress.md` - Recorded that local `_site` is corrected but `space-cadet.github.io` deployment is stale.
- Created `memory-bank/edits/2026-07-10/184044-t32-deployment-audit.md` - Added edit chunk for this bookkeeping pass.

#### 18:45:55 IST - T32: Deployed corrected numerics pages to `space-cadet.github.io`.
- Modified `memory-bank/tasks/T32.md` - Marked deployment synchronization complete and recorded deploy commit `92d05cc`.
- Modified `memory-bank/activeContext.md` - Added deployment sync record and updated next-session priorities.
- Modified `memory-bank/progress.md` - Recorded the successful deploy push.
- Modified `memory-bank/edits/2026-07-10/184044-t32-deployment-audit.md` - Added deployment resolution note.

#### 19:05:00 IST - T32: Fixed dashboard asset publishing, T20 Phase 3b figure paths, and main-page task timestamps.
- Modified `numerics/docs/_quarto.yml` - Added `assets/**` so Quarto copies dashboard gallery figures into `_site/assets/`.
- Modified `numerics/docs/dashboard.qmd` - Updated dashboard timestamps.
- Modified `numerics/docs/index.qmd` - Updated timestamps and added `Last Updated` column to the `Simulation Tasks` table.
- Modified `numerics/docs/tasks/t20-z2-lgt.qmd` - Switched Phase 3b Ising FSS figures to published `../assets/` paths and updated timestamps.
- Modified `numerics/docs/tasks/t22-spin-foam.qmd` - Updated timestamps.
- Modified `numerics/docs/tasks/t25-volume-operator.qmd` - Corrected `date-modified` to match the visible update date.
- Modified `numerics/docs/tasks/t31-signed-volume.qmd` - Updated timestamps.
- Re-rendered `numerics/docs/_site/` - Refreshed published HTML, search metadata, and copied figure assets.
- Deployed `space-cadet.github.io` commit `21a496e` - Restored dashboard assets and refreshed timestamps.
- Deployed `space-cadet.github.io` commit `efe6780` - Fixed T20 Phase 3b figure references and main numerics task table.
- Created `memory-bank/edits/2026-07-10/190500-t32-dashboard-asset-fix.md` - Added edit chunk for the dashboard/timestamp repair.

---

## 2026-07-08

#### 15:49:26 IST - T32: Deployed updated task pages and figures to GitHub Pages. Deleted stale gh-pages branch. Updated space-cadet.github.io repo from origin (5 commits). Copied v2 dashboard source to timesarrow repo. Synced 54 files (task pages + figures) from timesarrow main to .github.io repo. Fixed timestamps on index, T20, T31 pages. All changes pushed to origin/main.
- Deleted `gh-pages branch` - Deleted gh-pages branch
- Modified `space-cadet.github.io/projects/timesarrow/numerics/index.html` - Modified space-cadet.github.io/projects/timesarrow/numerics/index.html
- Modified `space-cadet.github.io/projects/timesarrow/numerics/tasks/t20-z2-lgt.html` - Modified space-cadet.github.io/projects/timesarrow/numerics/tasks/t20-z2-lgt.html
- Modified `space-cadet.github.io/projects/timesarrow/numerics/tasks/t31-signed-volume.html` - Modified space-cadet.github.io/projects/timesarrow/numerics/tasks/t31-signed-volume.html
- Created `numerics/pages/dashboard-v2.html` - Created numerics/pages/dashboard-v2.html


## 2026-07-02

#### 21:29:17 IST - T31: Completed 3D signed volume simulations for L=8,10,12. Added --signed-volume CLI flag. Created task page and deployed to numerics website. Identified gauge-dependence issue requiring iterative gauge-fixing.
- Modified `rust-lattice/src/lib.rs` - Modified rust-lattice/src/lib.rs
- Modified `rust-lattice/src/main.rs` - Modified rust-lattice/src/main.rs
- Created `rust-lattice/scripts/run-signed-volume.sh` - Created rust-lattice/scripts/run-signed-volume.sh
- Created `docs/tasks/t31-signed-volume.qmd` - Created docs/tasks/t31-signed-volume.qmd
- Modified `data/registry.json` - Modified data/registry.json
- Modified `docs/_quarto.yml` - Modified docs/_quarto.yml
