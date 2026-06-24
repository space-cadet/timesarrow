# Active Context
*Last Updated: 2026-06-24 09:35:00 IST*

## Current Status
**Numerics Package Initialized (2026-06-24):** A unified `timesarrow-numerics` package has been created under `numerics/` with TypeScript, ts-quantum integration, and Quarto docs. Seven beads tasks (T20-T26) are tracked in the workspace beads database with dependency chains. T25 and T22 are unblocked and ready to start; T20 is blocked on T25.

T18 (Manuscript Claim-Hardening) — **ACTIVE**. The reviewer-safe `sigma_e` / emergent-link clarification remains integrated into `timesarrow.tex`. T17 remains submitted to arXiv as `submit/7550944`; status on hold.

**Simulation Priority (Revised):**
1. **T25** (Volume Operator Extension) — 🟢 READY (no blockers, 3-5 days)
2. **T22** (Spin Foam Amplitudes) — 🟢 READY (no blockers, 2-4 weeks)
3. **T20** (Z₂ LGT Monte Carlo) — 🔴 BLOCKED on T25 (2-3 weeks)
4. **T23** (Entanglement Entropy) — 🔴 BLOCKED on T20 (1-2 weeks)
5. **T21** (CZX PEPS) — 🔴 BLOCKED on T22 (1-2 months)
6. **T24** (Domain Walls) — 🔴 BLOCKED on T20+T21 (1-2 months)
7. **T26** (Coupled Matter) — 🔴 BLOCKED on T20+T24 (2-3 months)

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
- **T25**: Volume Operator Extension — 🟢 **READY** (uses ts-quantum's `constructNValentBasis`, `computeVolumeSpectrum`)
- **T22**: Spin Foam Amplitudes — 🟢 **READY** (uses ts-quantum's Wigner 6j symbols)
- **T20**: Z₂ LGT Monte Carlo — 🔴 **BLOCKED** on T25
- **T23**: Entanglement Structure — 🔴 **BLOCKED** on T20
- **T21**: CZX PEPS Ground State — 🔴 **BLOCKED** on T22
- **T24**: Domain Wall Dynamics — 🔴 **BLOCKED** on T20+T21
- **T26**: Coupled Matter Simulation — 🔴 **BLOCKED** on T20+T24

## Completed Tasks (Current Session)
- **T18**: May 2026 reviewer-safety calibration integrated into the live manuscript and AI assistance disclosure; `timesarrow.pdf` rebuilt cleanly

## Recent Completed Tasks
- **T19**: Markdown-First Z2 Section Pilot — ✅ COMPLETED
- **T17**: arXiv Submission Preparation — ✅ COMPLETED & SUBMITTED (submit/7550944)

## Implementation Docs Created
- `implementation-details/z2-lgt-monte-carlo-plan.md` — T20: Detailed simulation plan for 3D Z₂ lattice gauge theory Monte Carlo
- `implementation-details/czx-peps-simulation-plan.md` — T21: PEPS construction plan for CZX-spin network ground state
- `implementation-details/spin-foam-amplitude-calculation.md` — T22: EPRL/FK vertex amplitude calculation plan
- `implementation-details/entanglement-structure-simulation.md` — T23: Topological entanglement entropy measurement plan
- `implementation-details/domain-wall-dynamics-plan.md` — T24: Domain wall dynamics and surface topological order simulation plan
- `implementation-details/volume-operator-extension.md` — T25: Extended volume operator diagonalization plan
- `implementation-details/coupled-matter-simulation-plan.md` — T26: Coupled spin network + scalar field simulation plan
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
1. **T25 implementation** — Start volume operator extension (3-5 days, no blockers, validates ts-quantum integration)
2. **T22 implementation** — Start spin foam amplitude calculation (2-4 weeks, no blockers, can run in parallel with T25)
3. **T20 implementation** — Begin Z₂ LGT Monte Carlo once T25 intertwiner framework is validated
4. **T23 entanglement entropy** — Run once T20 infrastructure is ready
5. **T21 PEPS construction** — Begin after T22 spin foam results are available
6. **T24 domain walls** — Most ambitious; tackle after T20 and T21
7. **T26 coupled matter** — Long-term; matter-selection of arrow
8. **T18 focused reading pass** — Review revised sections for flow and reviewer-safety
9. **T13** — Next.js interactive web presentation (can proceed in parallel)

## Open Author Decisions
- **Simulation priority and sequencing**: ✅ RESOLVED — T25 and T22 start first (parallel), then T20, T23, T21, T24, T26 in sequence. Beads tasks created with dependencies.
- **T20 code infrastructure**: ✅ DECIDED — Build unified `timesarrow-numerics` package using ts-quantum as base, Quarto docs for web output.
- **T21 computational strategy**: Whether to attempt full 3D PEPS or start with 2D CZX benchmark, then extrapolate. 3D PEPS is computationally expensive; may need GPU or cluster access.
- **T22 collaboration**: Whether to implement spin foam amplitudes from scratch or collaborate with spin-foam experts (e.g., Donà et al.) who have existing code.
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
