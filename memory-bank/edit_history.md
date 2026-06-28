# Edit History

*Last Updated: 2026-06-27 17:40:00 IST*

---

## 2026-06-28

#### 05:35:00 IST - T22 Reorganization: Fixed ts-quantum DB workflow, renamed T22-core→T14, T22-ext→T15 for proper sequential naming
- Modified `memory-bank/tasks.md` - Updated T22 dependencies to reference T14 instead of T22-core
- Modified `memory-bank/tasks/T22.md` - Updated architecture section: Phase 1 = T14, Phase 2 = T15
- Modified `memory-bank/activeContext.md` - Updated What's Next table: T14 (implement core), T22 (application)
- Created `ts-quantum/memory-bank/tasks/T14.md` - SU(2) Haar Measure Sampling (Core) via `mb task create`
- Created `ts-quantum/memory-bank/tasks/T15.md` - Spin Foam Extension Package Design via `mb task create`
- Deleted `ts-quantum/memory-bank/tasks/T22-core.md` - Replaced by T14
- Deleted `ts-quantum/memory-bank/tasks/T22-ext.md` - Replaced by T15
- Modified `ts-quantum/memory-bank/activeContext.md` - Updated current focus to T14/T15
- Fixed ts-quantum DB schema: Added `updated` column to task_items table for regenerate compatibility

#### 17:40:00 IST - T20d: L=32 simulation verified complete, registry fixed. T28a: Dashboard v2 functional implementation complete with external JSON loading and GitHub raw fallback. T29: Extensible schema design task created.
- Modified `numerics/data/registry.json` - Fixed syntax error, added L=32 entry
- Created `space-cadet.github.io/projects/timesarrow/numerics/dashboard-v2.html` - Vanilla JS single-file dashboard
- Created `space-cadet.github.io/projects/timesarrow/numerics/data/dashboard-data.json` - 33 runs metadata
- Created `space-cadet.github.io/projects/timesarrow/numerics/data/dashboard-figures.json` - 6 FSS figure references
- Modified `memory-bank/tasks/T20.md` - Updated all phases complete, L=32 results
- Modified `memory-bank/tasks/T20d.md` - Updated L=32 completion status
- Modified `memory-bank/tasks/T28.md` - Marked complete, superseded by T28a
- Created `memory-bank/tasks/T28a.md` - Comprehensive task file for dashboard v2
- Created `memory-bank/tasks/T29.md` - Extensible schema design task
- Modified `memory-bank/tasks.md` - Updated registry statuses
- Modified `memory-bank/activeContext.md` - Updated session focus and T20 status
- Modified `memory-bank/progress.md` - Updated T20d, T28a, T29 progress
- Created `memory-bank/sessions/2026-06-27-evening.md` - Session record
- Modified `memory-bank/session_cache.md` - Updated session info
- Created `memory-bank/edits/2026-06-27/1740-T20-T28a-T29-edit-chunk.md` - Edit chunk Analyzed old dashboard UX issues (unclear Plot Gallery dropdown, overlapping sections). Proposed extensible schema design with base+extension architecture for general numerics dashboard.
- Created `space-cadet.github.io/projects/timesarrow/numerics/dashboard-prototype-static.html` - Created space-cadet.github.io/projects/timesarrow/numerics/dashboard-prototype-static.html
- Created `numerics/docs/dashboard-prototype.qmd` - Created numerics/docs/dashboard-prototype.qmd
- Created `memory-bank/implementation/dashboard-v2-implementation-plan.md` - Created memory-bank/implementation/dashboard-v2-implementation-plan.md

#### 12:41:54 IST - T20d: L=32 simulation running (PID 49975, ~2h elapsed, 690% CPU). Corrected timing estimate: ~6h total wall time for 21 betas x 2M sweeps. L=8 and L=16 complete. Monitoring via subagent.
- Modified `memory-bank/tasks/T20d.md` - Modified memory-bank/tasks/T20d.md
- Modified `memory-bank/activeContext.md` - Modified memory-bank/activeContext.md
- Modified `memory-bank/progress.md` - Modified memory-bank/progress.md

#### 12:41:46 IST - T28: Implemented Plot Gallery with 20 plots (category-filtered), Run Detail Browser with parameters/results/timing, performance scaling chart with Observable Plot, compact summary cards, test run indicators. Fixed key finding word wrap, Results card formatting, Vega-Lite→Observable Plot migration. Deployed 5 commits to GitHub Pages.
- Modified `numerics/docs/dashboard.qmd` - Modified numerics/docs/dashboard.qmd
- Modified `numerics/data/registry.schema.json` - Modified numerics/data/registry.schema.json
- Modified `numerics/src/scripts/collate-data.ts` - Modified numerics/src/scripts/collate-data.ts
- Modified `memory-bank/tasks/T28.md` - Modified memory-bank/tasks/T28.md

#### 11:12:34 IST - T28: Session end: T20d L=32 still running (~3.7h CPU). T28 dashboard v2 design complete, collate-data.ts v2 in progress. DB workflow fixed. All changes committed and pushed to GitHub.
- Modified `memory-bank/session_cache.md` - Modified memory-bank/session_cache.md

#### 10:51:10 IST - T28-db-fix: Fixed DB schema drift in timesarrow memory-bank: updated project-local JS files (inserts.js, workflow.js, regenerate.js) to match mb-core v1.1 schema (session_date→date, session_period→period, focus_task→focus). Migrated session_cache table schema. DB-native workflow now fully functional.
- Modified `memory-bank/database/lib/inserts.js` - Modified memory-bank/database/lib/inserts.js
- Modified `memory-bank/database/lib/workflow.js` - Modified memory-bank/database/lib/workflow.js
- Modified `memory-bank/database/lib/regenerate.js` - Modified memory-bank/database/lib/regenerate.js

#### 10:50:58 IST - T28: Design enhanced simulation dashboard v2: integrated within timesarrow (not standalone), adds performance metrics (wall time, CPU time, timestamps), data export (JSON/CSV), plot gallery, live progress monitoring, task pipeline visualization. Architecture: Quarto + OJS + static JSON (GitHub Pages compatible). Design spec written to memory-bank/implementation/dashboard-v2-design.md.
- Modified `memory-bank/tasks/T28.md` - Modified memory-bank/tasks/T28.md
- Created `memory-bank/implementation/dashboard-v2-design.md` - Created memory-bank/implementation/dashboard-v2-design.md
- Modified `memory-bank/tasks.md` - Modified memory-bank/tasks.md
- Modified `memory-bank/activeContext.md` - Modified memory-bank/activeContext.md
- Modified `memory-bank/session_cache.md` - Modified memory-bank/session_cache.md
- Created `memory-bank/edits/2026-06-27/1020-T28-dashboard-v2-design.md` - Created memory-bank/edits/2026-06-27/1020-T28-dashboard-v2-design.md

#### 10:46:33 IST - T28: Test DB workflow after full schema fix
- Modified `memory-bank/database/lib/inserts.js` - Modified memory-bank/database/lib/inserts.js
- Modified `memory-bank/database/lib/workflow.js` - Modified memory-bank/database/lib/workflow.js
- Modified `memory-bank/database/lib/regenerate.js` - Modified memory-bank/database/lib/regenerate.js


## ## 2026-06-26

#### 23:50:00 IST - T20/T20d: Memory-bank schema fix plan — diagnosed v1.0→v1.1 column name mismatch, committed rename files, planned database recreation from text

#### 11:33:34 IST - T20: Rust checkpointing, data collation fix, and simulation dashboard deployment
- Modified `rust-lattice/src/main.rs` - Added --checkpoint flag, mpsc streaming, atomic writes, resume support
- Modified `rust-lattice/Cargo.toml` - Added chrono dependency for timestamps
- Modified `numerics/src/scripts/t20-sim-3d-fss-v2.py` - Pass checkpoint path to Rust binary
- Modified `numerics/src/scripts/collate-data.ts` - Fixed ES module compatibility, updated regex for hyphen-date filenames
- Modified `numerics/data/registry.json` - Fixed syntax error, backfilled 22 missing June 26 runs (33 total)
- Modified `numerics/output/benchmark-lattice-sizes-20250626.json` - Reconstructed from corrupted file, added scaling analysis
- Created `numerics/docs/dashboard.qmd` - Interactive OJS dashboard for browsing simulation runs
- Modified `numerics/docs/_quarto.yml` - Added Dashboard to navbar and sidebar
- Created `numerics/docs/data-registry.json` - Registry snapshot for dashboard FileAttachment

#### 06:34:05 IST - T20d: Finite-Size Scaling Analysis for 3D Z₂ LGT: Identified and resolved the α = -3.084 contradiction (mixing 2D vs 3D physics). Created infrastructure for rigorous FSS: 6 blockers mapped, all scripts generated, subagents completed. Simulations not yet run.
- Created `numerics/src/scripts/t20-autocorr-v2.py` - Rust-based autocorrelation analysis with 8 worker threads, --raw-output flag, τ_int measurement
- Created `numerics/src/scripts/t20-sim-3d-fss.py` - Fine β grid (Δβ=0.001-0.005) near critical point for L=8,16,32,48,64
- Created `numerics/src/scripts/t20-multi-run.py` - Multiple independent runs with unique seeds per (L,β) configuration
- Created `numerics/src/scripts/t20-fss-analysis.py` - 4 FSS methods: Binder cumulant crossing, scaling collapse, peak height scaling, β_c shift with corrections-to-scaling
- Modified `rust-lattice/src/main.rs` - Added --raw-output flag for raw time series output (autocorrelation pipeline)
- Created `memory-bank/tasks/T20d.md` - Full task specification: 6 blockers, requirements, estimated compute cost, analysis methods
- Modified `memory-bank/tasks/T20.md` - Updated gap analysis: Wilson loops implemented (2026-06-26 night), missing observables corrected
- Modified `memory-bank/activeContext.md` - Added T20d status and next steps

#### 00:50:02 IST - T20: Gap analysis: identified missing Wilson loops, critical exponents, and Phase 2 plots across all T20 phases

#### 00:43:21 IST - T20: Gap analysis: identified missing Wilson loops, critical exponents, and Phase 2 plots across all T20 phases. See implementation-details/t20-missing-observables.md for full details.

#### 00:30:00 IST - T20: Gap analysis: identified missing Wilson loops, critical exponents, and Phase 2 plots across all T20 phases


## ## 2026-06-24

#### 09:30:00 IST - T20–T26: Numerical simulation tasks created


## ## 2026-05-20

#### 09:30:55 IST - T18: Reviewer-safety calibration recorded
- Modified `timesarrow.tex` - Clarified that the paper targets coherent cosmological time orientation rather than a complete thermodynamic-arrow derivation
- Modified `timesarrow.tex` - Added a gauge-invariant dressed relative-orientation correlator to complement the Wilson loop
- Modified `timesarrow.tex` - Calibrated the CZX/SPT framing toward a concrete tensor-network/bond-index correspondence with the Appendix F caveat preserved
- Modified `timesarrow.tex` - Softened the fermionic-matter discussion toward boundary/defect-surface conjecture language and added a co-emergence caveat for semiclassical geometry
- Modified `ai-assistance-statement.md` - Expanded the disclosure to cover the April-May 2026 reviewer-safety and claim-hardening pass
- Modified `timesarrow.pdf` - Rebuilt the 44-page manuscript PDF after the May 2026 claim-hardening updates
- Created `memory-bank/implementation-details/ai-reviews/gpt55-peer-review-2026-05-19.md` - Archived the full GPT 5.5 manuscript review and phase-interpretation discussion
- Created `memory-bank/implementation-details/ai-reviews/gpt55-response-to-kimi-comparison-2026-05-19.md` - Archived GPT 5.5 follow-up guidance on the Kimi comparison and dressed-correlator recommendation
- Created `memory-bank/implementation-details/ai-reviews/kimi-gpt55-synthesis-2026-05-19.md` - Archived the synthesized reviewer-facing revision targets from Kimi and GPT 5.5
- Created `memory-bank/sessions/2026-05-19-afternoon.md` - Logged the terminology clarification, Mikhail Q&A, and AI review archive session
- Updated `memory-bank/tasks/T18.md` - Recorded the May 2026 manuscript hardening pass, disclosure update, and new related review artifacts
- Updated `memory-bank/tasks.md` - Refreshed T18 last-active timestamp and related files
- Updated `memory-bank/activeContext.md` - Recorded the current reviewer-safe manuscript framing and new implementation docs
- Updated `memory-bank/session_cache.md` - Set the current session to the 2026-05-20 T18 calibration update and refreshed session history
- Created `memory-bank/sessions/2026-05-20-morning.md` - Logged the memory-bank update session for the May 2026 manuscript calibration
- Created `memory-bank/edits/2026-05-20/093055-T18.md` - Added the canonical edit chunk for the May 2026 manuscript and memory-bank updates
- Updated `memory-bank/edit_history.md` - Prepended the generated-view entry for the T18 calibration update


## ## 2026-05-12

#### 13:36:57 IST - T18: Z2 link-field origin integrated
- Modified `timesarrow.tex` - Identified `sigma_e` as the shared binary bond index on a `j=1/2` spin-network edge
- Modified `timesarrow.tex` - Distinguished effective `Z_2` bond/even-parity structure from the full `SU(2)` singlet projection
- Modified `timesarrow.tex` - Added local `Z_2` transformation law and referenced it in the plaquette-action discussion
- Modified `timesarrow.tex` - Reframed the Wilson plaquette action and coupling `K` as effective dynamics pending spin-foam derivation
- Modified `timesarrow.tex` - Tightened abstract and introduction wording from "introduce" to "identify" the `Z_2` link field
- Modified `timesarrow.pdf` - Rebuilt 44-page manuscript PDF after the `sigma_e` integration
- Updated `memory-bank/tasks/T18.md` - Recorded progress on the manuscript hardening task and remaining review state
- Updated `memory-bank/tasks.md` - Refreshed T18 last-active timestamp
- Updated `memory-bank/activeContext.md` - Recorded current T18 manuscript state and next review step
- Updated `memory-bank/session_cache.md` - Set current session to the 2026-05-12 T18 manuscript integration
- Created `memory-bank/sessions/2026-05-12-afternoon.md` - Logged the manuscript integration session
- Created `memory-bank/edits/2026-05-12/133025-T18.md` - Added canonical edit chunk for the manuscript and memory-bank updates
- Updated `memory-bank/edit_history.md` - Prepended the generated-view entry for the T18 integration


## ## 2026-05-09

#### 12:03:05 IST - T19: Markdown-first Z2 pilot recorded
- Modified `.gitignore` - Ignored `markdown-pilot/build/` artifacts for the standalone pilot workflow
- Created `markdown-pilot/README.md` - Documented the pilot structure, usage, and hybrid Markdown/LaTeX rationale
- Created `markdown-pilot/z2-action.md` - Added Markdown-first source for the manuscript's `Z_2` section
- Created `markdown-pilot/z2-pilot.tex` - Added standalone LaTeX wrapper for pilot compilation
- Created `markdown-pilot/scripts/render-z2-pilot.sh` - Added Pandoc render script for Markdown-to-LaTeX generation
- Created `markdown-pilot/scripts/build-z2-pilot.sh` - Added end-to-end standalone build script
- Created `markdown-pilot/scripts/normalize_inline_math.py` - Added preprocessor for the manuscript's spaced inline math style
- Updated `markdown-pilot/generated/z2-action.tex` - Generated final LaTeX output from the normalized Markdown source
- Created `markdown-pilot/build/z2-pilot.pdf` - Verified standalone PDF artifact for the Z2 pilot
- Deleted `markdown-pilot/pdflatex.out` - Removed temporary debug output from sandboxed LaTeX troubleshooting
- Created `memory-bank/tasks/T19.md` - Recorded the pilot as a completed manuscript-workflow task
- Created `memory-bank/implementation-details/markdown-first-z2-pilot-2026-05-09.md` - Documented artifacts, workflow decisions, verification, and next integration step
- Created `memory-bank/sessions/2026-05-09-afternoon.md` - Logged the Markdown pilot session and deferred integration decision
- Created `memory-bank/edits/2026-05-09/120305-T19.md` - Added canonical edit chunk covering source and memory-bank updates
- Updated `memory-bank/tasks.md` - Added T19 to the completed-task registry and refreshed timestamps
- Updated `memory-bank/activeContext.md` - Recorded the completed Markdown pilot and the next optional full-manuscript integration step
- Updated `memory-bank/session_cache.md` - Switched current session state to the 2026-05-09 afternoon Markdown pilot
- Updated `memory-bank/edit_history.md` - Prepended the generated-view entry for the T19 update


## ## 2026-05-06

#### 18:34:13 IST - T18: Second-opinion feasibility discussion recorded
- Updated `memory-bank/tasks/T18.md` - Added Sonnet 4.6 and GPT 5.5 model provenance, refined `Z_2` bond-index claim, and progress update
- Updated `memory-bank/implementation-details/manuscript-claim-hardening-proposal-2026-05-06.md` - Appended full second-opinion discussion and GPT 5.5 follow-up assessment
- Updated `memory-bank/sessions/2026-05-06-evening.md` - Added second-opinion discussion summary and key decisions
- Updated `memory-bank/tasks.md` - Refreshed T18 last-active timestamp
- Updated `memory-bank/activeContext.md` - Recorded refined T18 hardening path and subsection wording decision
- Updated `memory-bank/session_cache.md` - Recorded second-opinion status and next memo step
- Updated `memory-bank/edit_history.md` - Added generated-view entry for the second-opinion memory update

#### 17:26:52 IST - T18: Claim-hardening roadmap recorded
- Created `memory-bank/tasks/T18.md` - New task for manuscript claim-hardening and reviewer-response roadmap
- Created `memory-bank/implementation-details/manuscript-claim-hardening-proposal-2026-05-06.md` - Proposal capturing defensible claims map approach and technical gaps
- Created `memory-bank/sessions/2026-05-06-evening.md` - Session log for PDF review follow-up and memory-bank update
- Updated `memory-bank/tasks.md` - Added T18 active task and updated strict task registry table
- Updated `memory-bank/activeContext.md` - Set T18 as current manuscript follow-up focus and refreshed timestamp
- Updated `memory-bank/session_cache.md` - Recorded T18 in current session state and active task list
- Updated `memory-bank/edit_history.md` - Regenerated generated-view entry for the T18 update


## ## 2026-05-05

#### 02:42:04 IST - T17: arXiv Submission Uploaded
- Modified `arxiv_submission_v1/timesarrow.tex` - Restored full AI addendum (84 lines) accidentally stripped during peer-review fixes
- Modified `timesarrow.tex` - Restored full AI addendum at end of document
- Modified `arxiv-submission-v1.tar.gz` - Rebuilt with root-level files (no top-level directory)
- Updated `memory-bank/tasks/T17.md` - Added submission reference submit/7550944
- Updated `memory-bank/tasks.md` - Updated last-updated timestamp
- Updated `memory-bank/activeContext.md` - Marked T17 as submitted to arXiv
- Updated `memory-bank/session_cache.md` - Recorded submission status and reference
- Updated `memory-bank/sessions/2026-05-05-peer-review.md` - Added arXiv upload section

#### 02:13:32 IST - T17-ext: AI Peer Review — 9 Fixes Applied
- Modified `timesarrow.tex` - Fixed eqn:area-minimum: added missing pi factor (4√3 π γ lp²)
- Modified `timesarrow.tex` - Fixed eqn:vol-states basis consistency in Appendix F (manuscript basis, not supplementary basis)
- Modified `timesarrow.tex` - Clarified line 1437: SU(2) Gauss constraint reduces to effective Z₂ on j=1/2 intertwiner qubit
- Modified `timesarrow.tex` - Reframed Intro claim (iv): structural correspondence of Z₂-invariant effective qubits (not literal U_CZX action)
- Modified `timesarrow.tex` - Added regular-lattice dominance paragraph in Sec 6.3 justifying 2D CZX ↔ 3D spin-network mapping
- Modified `timesarrow.tex` - Added universality footnote at line 1084 distinguishing 3+1D quantum Ising from classical 3D→2D duality
- Modified `timesarrow.tex` - Made thermal argument dimensionally consistent: explicit Planck units with restoration at end
- Modified `timesarrow.tex` - Added MPS caveat: generic states require exponential bond dimension
- Modified `timesarrow.tex` - En-dash typography consistency in title and abstract
- Modified `arxiv_submission_v1/timesarrow.tex` - Synced from root manuscript after all fixes
- Modified `arxiv-submission-v1.tar.gz` - Rebuilt bundle (~1.5 MB)
- Created `memory-bank/implementation-details/ai-peer-review-2026-05-05.md` - Full 3-round peer review dialog with resolutions table
- Created `memory-bank/sessions/2026-05-05-peer-review.md` - Session record for peer review work

#### 01:23:22 IST - T17: arXiv Submission Preparation
- Created `arxiv_submission_v1/` - Clean submission folder with figures subdirectory
- Created `arxiv_submission_v1/timesarrow.tex` - Edited for arXiv (disabled todonotes, added `\pdfoutput=1`, cleaned template comments)
- Created `arxiv_submission_v1/SciPost.cls` - Document class file
- Created `arxiv_submission_v1/timesarrow.bbl` - Bibliography (biblatex format 3.3)
- Created `arxiv_submission_v1/timesarrow.bib` - BibTeX source
- Created `arxiv_submission_v1/figures/` - 34 referenced figure files
- Modified `arxiv_submission_v1/timesarrow.tex` - Added AI assistance statement addendum at end of document
- Modified `arxiv_submission_v1/timesarrow.tex` - Hyperlinked all commit IDs in addendum to GitHub repo
- Modified `arxiv_submission_v1/timesarrow.tex` - Updated "What the AI Did Not Do" to note Appendix F was AI-drafted
- Modified `arxiv_submission_v1/timesarrow.tex` - Changed "editor" analogy to "research assistant"
- Modified `arxiv_submission_v1/timesarrow.tex` - Added `\thanks` footnote with repo link on author line
- Created `arxiv-submission-v1.tar.gz` - Final submission bundle (1.4 MB)
- Created `memory-bank/tasks/T17.md` - Task documentation
- Created `memory-bank/sessions/2026-05-05-early.md` - Session log


## ## 2026-04-29

#### 22:27:33 IST - T16: Submission Documentation
- Created `cover-letter.md` - SciPost Physics submission cover letter with manuscript summary, original contributions, relation to literature, suitability justification, AI assistance note, and suggested referees from LQG, topological phases, and quantum information communities
- Created `ai-assistance-statement.md` - Detailed AI assistance disclosure documenting author's original work (2016-2018) vs AI-assisted revision (April 2026), with git commit references for auditability
- Created `memory-bank/project_contributions.md` - Contribution record delineating author vs AI contributions with boundary principles for intellectual ownership
- Modified `timesarrow.tex` - Added AI assistance acknowledgment in acknowledgements section referencing separate AI assistance statement document
- Modified `timesarrow.pdf` - Regenerated PDF with AI assistance acknowledgment update
- Modified `memory-bank/activeContext.md` - Updated Last Updated timestamp to 2026-04-29 22:27:33 IST, updated current status to reflect T16 completion, added T16 to completed tasks, added project_contributions.md to implementation docs
- Created `memory-bank/tasks/T16.md` - Task file documenting submission documentation work
- Modified `memory-bank/tasks.md` - Updated Last Updated timestamp to 2026-04-29 22:27:33 IST, added T16 to Completed Tasks table
- Created `memory-bank/sessions/2026-04-29-evening.md` - New session file documenting T16 submission documentation work
- Modified `memory-bank/session_cache.md` - Updated Last Updated timestamp to 2026-04-29 22:27:33 IST, updated current session to evening with T16 focus, updated session history to include new evening session

#### 22:14:09 IST - T14: Static web presentation implementation complete
- Created `web-static/index.html` - 34 KB single-page HTML, 6 sections, 4 inline SVG illustrations, 5 KaTeX equations
- Created `web-static/css/style.css` - dark quantum theme with CSS variables and mobile breakpoints at 700px
- Created `web-static/js/katex-loader.js` - KaTeX CDN auto-render with diagnostic console logging
- Created `web-static/figures/spin-net-vertex.svg` - copied from figures/
- Created `web-static/figures/czx-vertex.svg` - copied from figures/czx_vertex.svg
- Created `web-static/figures/local-symmetry-flux.png` - copied from figures/
- Created `web-static/figures/czx-lattice.png` - copied from figures/
- Updated `memory-bank/tasks/T14.md` - status completed, acceptance criteria updated, progress log added
- Updated `memory-bank/tasks.md` - T14 status to completed, row added to completed table
- Created `memory-bank/sessions/2026-04-29-evening.md` - session file
- Updated `memory-bank/session_cache.md` - current session and T14 status
- Updated `memory-bank/activeContext.md` - current status and next steps
- Created `memory-bank/edits/2026-04-29/221409-T14.md` - edit chunk


## ## 2026-04-20

#### 12:36:54 IST - T15: 3D SPT Survey Completion and Manuscript Finalization
- Modified `timesarrow.tex` - M9 refinement: replaced "exponentially more states" with defensible arguments (thermal Boltzmann suppression β > 2/κ, Bekenstein-Hawking black hole entropy); SciPost template cleanup: updated affiliation to "Independent Researcher", removed TODO comments; acknowledgements rewrite to reflect 2018 Visiting Associateship; gapless/gapped terminology resolution throughout (abstract, introduction, contributions, Sec 7.3, future directions); Sec 7.3 dimensional paragraph: added explicit 3D SPT classification H⁴(Z₂ᵀ, U(1)_𝒯) ≅ ℤ₂
- Modified `timesarrow.bib` - Added Meissner2004Black-hole and Domagala2004Black-hole citations for M9 refinement
- Modified `memory-bank/tasks/T15.md` - Marked status as COMPLETED, updated completion timestamp to 2026-04-20 12:36:54 IST, marked final acceptance criterion as complete
- Modified `memory-bank/tasks.md` - Moved T15 from Active Tasks to Completed Tasks table, updated Last Updated timestamp to 2026-04-20 12:36:54 IST
- Modified `memory-bank/tasks/T12.md` - Updated Last Updated timestamp to 2026-04-20 12:36:54 IST, added M9 refinement note with defensible arguments (Boltzmann suppression, Bekenstein-Hawking entropy) and new citations (Meissner2004Black-hole, Domagala2004Black-hole)
- Created `memory-bank/implementation-details/biber-infrastructure-fix.md` - Documented Apple Silicon biber infrastructure fix (removed MiKTeX x86_64 symlink, allowing homebrew arm64 biber to take precedence)
- Created `memory-bank/sessions/2026-04-20-afternoon.md` - New session file documenting T15 completion, M9 refinement, template cleanup, acknowledgements update, gapless/gapped terminology resolution, Sec 7.3 classification result, and biber infrastructure fix
- Modified `memory-bank/activeContext.md` - Updated Last Updated timestamp to 2026-04-20 12:36:54 IST, updated current status to reflect T15 completion and manuscript ready for submission, removed T15 from active tasks, added T15 and T12 to completed tasks, updated implementation docs list, updated recommended next session order, updated document statistics
- Modified `memory-bank/session_cache.md` - Updated Last Updated timestamp to 2026-04-20 12:36:54 IST, updated current session to afternoon with T15 completion focus, updated active task count to 2 (T13, T14), removed T15 and T15.1 from active tasks, updated session history to include new afternoon session

#### 11:09:51 IST - T15: Memory bank update for survey completion and integration phase
- Updated `memory-bank/tasks/T15.md` - Marked survey criteria complete, updated progress tracking, added subtask T15.1 delegation
- Created `memory-bank/implementation-details/fermionic-matter-emergence.md` - Documented all-fermion toric code surface order decision
- Updated `memory-bank/tasks.md` - Updated Last Updated timestamp
- Updated `memory-bank/session_cache.md` - Updated current session info, task registry, and active tasks section
- Created `memory-bank/sessions/2026-04-20-morning.md` - Created new session file for morning work
- Created `memory-bank/edits/2026-04-20/110951-t15-integration.md` - Edit chunk file documenting this memory bank update

#### 04:07:00 IST - T11, T7, T12: Verification and Completion

#### 02:50:00 IST - T12: Major Issues M7/M9/M10/M13/M14 Fixed; T15 Created
- Modified `spt-lqg-mapping.tex` - M14: Added cohomological rationale for fermionic edge modes (H²(Z₂ᵀ,U(1)ₜ)); cite Kapustin2014Symmetry
- Modified `timesarrow.tex` - M7: Added Jahn2021Holographic, Steinberg2023Holographic citations to QECC section; M10: Added Dittrich2016Coarse to Future Work; M13: Added Cao2018Bulk, Hohn2021The-Trinity to Future Work
- Modified `z2-action-derivation.tex` - M13: Specified 3D toric code (not 2D) in topological protection discussion
- Modified `timesarrow.bib` - Added Dittrich2016Coarse, Cao2018Bulk, Hohn2021The-Trinity, Jahn2021Holographic, Steinberg2023Holographic, Baytas2018Gluing, Bianchi2018Intertwiner entries
- Created `memory-bank/tasks/T15.md` - New task for 3D SPT classification survey to resolve 2D/3D mismatch
- Created `memory-bank/implementation-details/3d-spt-survey-needed.md` - Survey requirements doc linked to T15
- Modified `memory-bank/tasks/T12.md` - Updated progress: M7, M9, M10, M13, M14 completed
- Modified `memory-bank/tasks.md` - Added T15 to active tasks, updated T12 status, moved T10 to completed
- Modified `memory-bank/activeContext.md` - Updated audit summary and recommended next session order
- Modified `memory-bank/session_cache.md` - Updated current session and task registry
- Created `memory-bank/sessions/2026-04-20-dawn.md` - Session record for this work
- Created `memory-bank/edits/2026-04-20/025000-T15-T12-sync.md` - Edit chunk for T12 completion and T15 creation


## ## 2026-04-18

#### 04:30:37 IST - T10: BibTeX Mismatches Fixed; T12: Reference Cleanup Partial
- Modified `timesarrow.tex` - Fixed 11 BibTeX key mismatches (Zeh, Goold, Barbour, Vaid, Christodoulou, Perez, Kogut, Mildenberger, Ashtekar), fixed index notation (We->I, we->I), added new citations
- Modified `spt-lqg-mapping.tex` - Fixed Perez2013Spin -> Perez2013The-Spin-Foam
- Modified `z2-action-derivation.tex` - Fixed Kogut1979Introduction -> Kogut1979An-introduction, Perez2013Spin -> Perez2013The-Spin-Foam, added Dona2020Numerical, Dona2022Asymptotics, fixed M12 universality class statement
- Modified `supplementary-calculations.tex` - Fixed Perez2013Spin -> Perez2013The-Spin-Foam
- Modified `timesarrow.bib` - Changed Kogut1979Introduction -> Kogut1979An-introduction, Perez2013Spin -> Perez2013The-Spin-Foam, added 7 new entries (Colafranceschi2021Holographic, Chirco2022Quantum, Colafranceschi2022Holographic, Dona2020Numerical, Dona2022Asymptotics, Mildenberger2024Probing, Homeier2023Quantum)
- Modified `memory-bank/tasks/T10.md` - Updated status to completed, marked all criteria as done
- Modified `memory-bank/tasks/T12.md` - Updated status to in progress, updated progress section
- Modified `memory-bank/tasks.md` - Moved T10 to completed tasks, updated T12 to in progress, updated timestamps
- Modified `memory-bank/session_cache.md` - Updated task registry, marked T10 completed, T12 in progress
- Modified `memory-bank/sessions/2026-04-18-night.md` - Added T10 completion and T12 partial progress
- Created `memory-bank/edits/2026-04-18/043037-T10-T12.md` - Edit chunk for T10 and T12 work

#### 03:00:00 IST - T14: Kimi K2.5 Minimal Web Presentation
- Created `memory-bank/tasks/T14.md` - Task definition for static HTML web presentation
- Created `memory-bank/implementation-details/kimi-k25-web-minimal-plan.md` - Detailed plan with ASCII layout diagrams
- Created `memory-bank/sessions/2026-04-18-kimi-web.md` - Session tracking file
- Modified `memory-bank/tasks.md` - Added T14 to active tasks table
- Modified `memory-bank/session_cache.md` - Updated current session and task registry
- Created `memory-bank/edits/2026-04-18/030000-T14.md` - Edit chunk for T14 work

#### 02:32:38 IST - T11/T12: Implementation Docs Created
- Created `memory-bank/implementation-details/holography-lqg-survey.md` - LQG holography survey (9 groups, 2015–2026)
- Created `memory-bank/implementation-details/arrow-of-time-survey.md` - Arrow of time approaches survey (16 approaches)
- Created `supplementary-calculations.tex` - Full calculations for T11/C3, T12/M6, T12/M9; compiles to 14pp PDF
- Updated `memory-bank/sessions/2026-04-18-night.md` - Added implementation doc records
- Updated `memory-bank/activeContext.md` - Added impl docs section and revised next session order
- Created `memory-bank/edits/2026-04-18/023238-impl-docs.md` - Edit chunk for implementation docs

#### 02:12:39 IST - T10/T11/T12: Subagent Audit Tasks Created
- Created `memory-bank/tasks/T10.md` - New task: fix 17 bibliography metadata errors
- Created `memory-bank/tasks/T11.md` - New task: fix 5 critical manuscript errors
- Created `memory-bank/tasks/T12.md` - New task: address 9 major issues + add recent citations
- Updated `memory-bank/tasks.md` - Added T10, T11, T12 to active tasks registry
- Updated `memory-bank/activeContext.md` - Recorded audit findings; recommended next session order
- Updated `memory-bank/session_cache.md` - New session; T10/T11/T12 registered as active
- Created `memory-bank/sessions/2026-04-18-night.md` - Session record for audit work
- Updated `memory-bank/progress.md` - Work in progress and remaining tasks updated
- Created `memory-bank/edits/2026-04-18/021239-T10T11T12.md` - Edit chunk for audit tasks


## ## 2026-04-17

#### 02:29:00 IST - T9: Create missing figure for Sec 3.5
- Created `figures/tns-matrix-insertion-2d.tex` - TikZ 4×4 TNS grid showing M/M⁻¹ insertion on subregion bonds with interior cancellation and boundary survival labels
- Created `figures/tns-matrix-insertion-2d.pdf` - Compiled standalone figure
- Modified `timesarrow.tex` - Replaced \todo{Insert figure...} with figure environment, \autoref, and caption in Sec 3.5

#### 02:29:00 IST - T8: Fix typos and structural errors
- Modified `timesarrow.tex` - Moved \label{fig:czx-entangled} inside figure float; changed \captionof to \caption
- Modified `timesarrow.tex` - Removed duplicate \usepackage{todonotes}; converted p.1 \todo to LaTeX comment
- Modified `timesarrow.tex` - Fixed "two region", "a a single", "Legende", "othogonal", "Succintly", "difference representations", "Schrodinger" (×3)
- Modified `timesarrow.bib` - Fixed doubled arXiv: prefix in Van Raamsdonk entry
- Created `memory-bank/sessions/2026-04-17-night.md` - Session file for 2026-04-17 night
- Created `memory-bank/tasks/T9.md` - Task file for missing figure creation
- Modified `memory-bank/tasks/T8.md` - Updated to completed status with full fix log
- Modified `memory-bank/tasks.md` - Added T9, moved T8 to completed, updated timestamps
- Modified `memory-bank/activeContext.md` - Updated current status and next steps
- Modified `memory-bank/session_cache.md` - Populated with current session and history
- Created `memory-bank/edits/2026-04-17/022900-T8-T9.md` - Edit chunk for T8 and T9


## ## 2026-04-16

#### 23:25:00 IST - T3, T4, T5, T6: Major Manuscript Rewrite and Expansion

#### 20:27:00 IST - T1, T2: Memory Bank Documentation

#### 20:25:00 IST - T1: Initial Memory Bank Population

#### 20:22:00 IST - T2: Analyze Manuscript Gaps

