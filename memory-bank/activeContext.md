# Active Context
*Last Updated: 2026-05-20 09:30:55 IST*

## Current Status
T18 (Manuscript Claim-Hardening and Reviewer-Response Roadmap) — **ACTIVE**. The reviewer-safe `sigma_e` / emergent-link clarification remains integrated into `timesarrow.tex`, and the May 2026 review pass has now hardened the broader framing: the manuscript explicitly distinguishes coherent cosmological time orientation from a full thermodynamic-arrow derivation, adds a gauge-invariant dressed relative-orientation correlator alongside the Wilson loop, presents the CZX discussion as a concrete tensor-network/bond-index correspondence with the Appendix F caveat intact, and softens the fermionic-matter story toward boundary/defect-surface conjecture language. `ai-assistance-statement.md` was updated in parallel to cover the April-May 2026 reviewer-safety pass, and `timesarrow.pdf` rebuilt cleanly. T19 (Markdown-First Z2 Section Pilot) — **COMPLETED** and remains isolated. T17 remains submitted to arXiv as `submit/7550944`; status on hold.

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
- **T18**: May 2026 reviewer-safety calibration integrated into the live manuscript and AI assistance disclosure; `timesarrow.pdf` rebuilt cleanly

## Recent Completed Tasks
- **T19**: Markdown-First Z2 Section Pilot — ✅ COMPLETED
- **T17**: arXiv Submission Preparation — ✅ COMPLETED & SUBMITTED (submit/7550944)

## Implementation Docs Created
- `implementation-details/markdown-first-z2-pilot-2026-05-09.md` — T19 pilot artifacts, workflow decisions, verification notes, and recommended full-manuscript integration test
- `implementation-details/manuscript-claim-hardening-proposal-2026-05-06.md` — T18 proposal: defensible claims map, derivation targets, and reframe points
- `implementation-details/ai-reviews/gpt55-peer-review-2026-05-19.md` — GPT 5.5 review of the manuscript's central claims and phase interpretation
- `implementation-details/ai-reviews/gpt55-response-to-kimi-comparison-2026-05-19.md` — GPT 5.5 follow-up on the Kimi comparison, including the dressed-correlator recommendation
- `implementation-details/ai-reviews/kimi-gpt55-synthesis-2026-05-19.md` — Synthesized reviewer-facing revision targets from Kimi and GPT 5.5
- `implementation-details/gemini-web-presentation-plan.md`
- `implementation-details/arrow-of-time-survey.md`
- `implementation-details/3d-spt-survey-needed.md` — 3D SPT classification survey requirements
- `implementation-details/3d-spt-survey-results.md` — Survey findings and appendix outline
- `implementation-details/biber-infrastructure-fix.md` — Apple Silicon biber fix documentation
- `supplementary-calculations.tex` — Verified; contains T11/C3 derivations
- `project_contributions.md` — Author vs AI contribution delineation for submission
- `implementation-details/ai-peer-review-2026-05-05.md` — Full dialog of final peer review: reviewer claims, author responses, admitted errors, and resolutions

## Recommended Next Session Order
1. **T18 focused reading pass** — Review the revised `Volume Operator`, `SPT-LQG`, `Z_2 Action`, and discussion chain for flow and reviewer-safety after the May 2026 calibration.
2. **T19 integration test** — If the Markdown route resumes, wire `markdown-pilot/generated/z2-action.tex` into the full SciPost manuscript and compare the output.
3. **Final arXiv pass** — User may review submission bundle while arXiv status remains on hold.
4. **T13** — Next.js interactive web presentation.

## Open Author Decisions
- T19 integration choice: keep the Markdown pilot isolated, or replace the live `Z_2` section via `\input{markdown-pilot/generated/z2-action.tex}` for a full-manuscript test.
- T18 reading result: whether the integrated `sigma_e` origin plus the new time-orientation/discussion wording now flows well enough, or whether the `Z_2` section still needs a dedicated subsection title such as "From Intertwiner Bond Indices to a `Z_2` Link Field."
- T18 remaining scope: whether to next harden `j=1/2` / regular-lattice assumptions, or revisit the fermion conjecture with the boundary/defect-surface framing now in place.
- ~~Appendix D sub-label shadowing~~ ✅ RESOLVED
- ~~Abstract emphasis ordering~~ ✅ RESOLVED
- ~~"Original contributions" paragraph~~ ✅ RESOLVED
- ~~Front-page repo link footnote~~ 🔄 ATTEMPTED: `\thanks` added but may not render correctly in SciPost class

## Document Statistics
- Pages: 44
- LaTeX: builds cleanly after the 2026-05-20 reviewer-safety calibration
- Markdown pilot: `markdown-pilot/build/z2-pilot.pdf` verified as a 7-page standalone artifact
- Status: Submitted to arXiv (submit/7550944, on hold)
- Pending: T18 focused reading pass, T19 full-manuscript integration decision, T13 web presentation, arXiv moderation decision
