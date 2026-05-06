# Active Context
*Last Updated: 2026-05-06 18:34:13 IST*

## Current Status
T18 (Manuscript Claim-Hardening and Reviewer-Response Roadmap) — **ACTIVE**. Fresh PDF review and Sonnet 4.6 (Medium) second opinion identified a refined hardening path: `sigma_e` should be described as the shared binary bond index on a spin-network edge, with the full `SU(2)` intertwiner projection leading to signed-volume orientation sectors. T17 remains submitted to arXiv as `submit/7550944`; status on hold.

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
- **T18**: Manuscript Claim-Hardening and Reviewer-Response Roadmap — 🔄 IN PROGRESS
- **T13**: Gemini 3 Flash - Web Presentation — 🔄 IN PROGRESS

## Completed Tasks (Current Session)
- None. T18 planning task is active; no manuscript edits made.

## Recent Completed Tasks
- **T17**: arXiv Submission Preparation — ✅ COMPLETED & SUBMITTED (submit/7550944)

## Implementation Docs Created
- `implementation-details/manuscript-claim-hardening-proposal-2026-05-06.md` — T18 proposal: defensible claims map, derivation targets, and reframe points
- `implementation-details/gemini-web-presentation-plan.md`
- `implementation-details/arrow-of-time-survey.md`
- `implementation-details/3d-spt-survey-needed.md` — 3D SPT classification survey requirements
- `implementation-details/3d-spt-survey-results.md` — Survey findings and appendix outline
- `implementation-details/biber-infrastructure-fix.md` — Apple Silicon biber fix documentation
- `supplementary-calculations.tex` — Verified; contains T11/C3 derivations
- `project_contributions.md` — Author vs AI contribution delineation for submission
- `implementation-details/ai-peer-review-2026-05-05.md` — Full dialog of final peer review: reviewer claims, author responses, admitted errors, and resolutions

## Recommended Next Session Order
1. **T18 technical memo** — Build claim/support/gap/repair/proposed wording map before manuscript edits.
2. **Final arXiv pass** — User may review submission bundle while arXiv status remains on hold.
3. **T13** — Next.js interactive web presentation.
4. **Deploy T14** — Netlify drop-in deployment of `/web-static/` when deploy tool is available.

## Open Author Decisions
- T18 memo scope: whether to focus first on `Z_2` gauge derivation, CZX/SPT framing, fermion conjecture, or all claims in one pass.
- T18 wording choice: new subsection should likely be "From Intertwiner Bond Indices to a `Z_2` Link Field" rather than half-edge comparison language.
- ~~Appendix D sub-label shadowing~~ ✅ RESOLVED
- ~~Abstract emphasis ordering~~ ✅ RESOLVED
- ~~"Original contributions" paragraph~~ ✅ RESOLVED
- ~~Front-page repo link footnote~~ 🔄 ATTEMPTED: `\thanks` added but may not render correctly in SciPost class

## Document Statistics
- Pages: 44
- LaTeX: builds cleanly
- Status: Submitted to arXiv (submit/7550944, on hold)
- Pending: T18 technical memo, T13 web presentation, arXiv moderation decision
