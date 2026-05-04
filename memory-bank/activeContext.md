# Active Context
*Last Updated: 2026-05-05 01:23:22 IST*

## Current Status
T17 (arXiv Submission Preparation) completed. `arxiv_submission_v1/` created with clean `timesarrow.tex` (44 pages), `SciPost.cls`, `timesarrow.bbl`, 34 figure files. AI assistance statement added as end addendum with hyperlinked git commits and verified dates. Build clean. Tarball `arxiv-submission-v1.tar.gz` (1.4 MB) ready. User will do one final pass in new session before upload.

## Audit Summary (Updated)

### Agent A — Reference Verification
- ✅ T10 Completed: 17 bib metadata errors fixed; all keys verified and building.

### Agent B — Claim Audit + Recent Literature
- ✅ T12 Completed: 20 recent papers (2018–2026) added; "first order" error fixed; "SSB" language corrected; M9 refined with defensible arguments and new citations.
- ✅ T15 Completed: Addressed M14 (2D/3D mismatch) via detailed 3D SPT survey; Sec 7.3 integration complete; gapless/gapped terminology resolved.

### Agent C — Manuscript Quality Audit
- ✅ T11 Completed: All 5 critical errors fixed (C1-C5).
- ✅ T12 Completed: All 9 major issues addressed; M6 resolved by C3 correction.

### Agent D — arXiv Submission Preparation
- ✅ T17 Completed: Clean submission bundle created, build verified, tarball ready.

## Active Tasks
- **T13**: Gemini 3 Flash - Web Presentation — 🔄 IN PROGRESS

## Completed Tasks (This Session)
- **T17**: arXiv Submission Preparation — ✅ COMPLETED

## Implementation Docs Created
- `implementation-details/gemini-web-presentation-plan.md`
- `implementation-details/arrow-of-time-survey.md`
- `implementation-details/3d-spt-survey-needed.md` — 3D SPT classification survey requirements
- `implementation-details/3d-spt-survey-results.md` — Survey findings and appendix outline
- `implementation-details/biber-infrastructure-fix.md` — Apple Silicon biber fix documentation
- `supplementary-calculations.tex` — Verified; contains T11/C3 derivations
- `project_contributions.md` — Author vs AI contribution delineation for submission

## Recommended Next Session Order
1. **Final arXiv pass** — User will review submission bundle in new session.
2. **T13** — Next.js interactive web presentation (remaining open task).
3. **Deploy T14** — Netlify drop-in deployment of `/web-static/` when deploy tool is available.

## Open Author Decisions
- ~~Appendix D sub-label shadowing~~ ✅ RESOLVED
- ~~Abstract emphasis ordering~~ ✅ RESOLVED
- ~~"Original contributions" paragraph~~ ✅ RESOLVED
- ~~Front-page repo link footnote~~ 🔄 ATTEMPTED: `\thanks` added but may not render correctly in SciPost class

## Document Statistics
- Pages: 44
- LaTeX: builds cleanly
- Status: Ready for arXiv submission (pending final user review)
- Pending: T13 (web presentation), final submission upload
