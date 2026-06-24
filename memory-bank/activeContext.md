# Active Context
*Last Updated: 2026-06-24 09:35:00 IST*

## Current Status
T18 (Manuscript Claim-Hardening and Reviewer-Response Roadmap) — **ACTIVE**. The reviewer-safe `sigma_e` / emergent-link clarification remains integrated into `timesarrow.tex`, and the May 2026 review pass has now hardened the broader framing: the manuscript explicitly distinguishes coherent cosmological time orientation from a full thermodynamic-arrow derivation, adds a gauge-invariant dressed relative-orientation correlator alongside the Wilson loop, presents the CZX discussion as a concrete tensor-network/bond-index correspondence with the Appendix F caveat intact, and softens the fermionic-matter story toward boundary/defect-surface conjecture language. `ai-assistance-statement.md` was updated in parallel to cover the April-May 2026 reviewer-safety pass, and `timesarrow.pdf` rebuilt cleanly. T19 (Markdown-First Z2 Section Pilot) — **COMPLETED** and remains isolated. T17 remains submitted to arXiv as `submit/7550944`; status on hold.

**NEW (2026-06-24):** Seven numerical simulation tasks (T20–T26) have been created to back up the theoretical work, following a comprehensive review of the manuscript and GPT 5.5 peer-review critique. The simulation program is designed to address the three main weaknesses identified: (1) the Z₂ gauge action is "posited, not derived" → T22 (spin foam amplitudes) addresses this; (2) the CZX/SPT correspondence is "overstated" → T21 (PEPS ground state) addresses this; (3) the fermion conjecture is "very speculative" → T24 (domain wall dynamics) addresses this. T20 (Z₂ LGT Monte Carlo) is the foundational simulation validating the core confinement-deconfinement claim.

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
- **T20**: 3D Z₂ Lattice Gauge Theory Monte Carlo — 🔄 ACTIVE (CRITICAL)
- **T21**: CZX-Spin Network PEPS Ground State — 🔄 ACTIVE (HIGH)
- **T22**: Spin Foam Amplitude for j=1/2 Dominance — 🔄 ACTIVE (HIGH)
- **T23**: Entanglement Structure of Deconfined Phase — 🔄 ACTIVE (MEDIUM)
- **T24**: Domain Wall Dynamics and Surface Topological Order — 🔄 ACTIVE (MEDIUM)
- **T25**: Volume Operator Eigenvalue Distribution (Extended) — 🔄 ACTIVE (LOW, quick win)
- **T26**: Coupled Spin Network + Matter Simulation — 🔄 ACTIVE (LOW, long-term)

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
1. **T20 implementation** — Begin the Z₂ LGT Monte Carlo simulation (foundational; validates core claim).
2. **T22 spin foam amplitudes** — Start EPRL/FK vertex amplitude calculation (addresses j=1/2 weakness; can run in parallel with T20).
3. **T25 quick win** — Extend volume operator diagonalization (3-5 days; strengthens j=1/2 argument).
4. **T18 focused reading pass** — Review the revised `Volume Operator`, `SPT-LQG`, `Z_2 Action`, and discussion chain for flow and reviewer-safety after the May 2026 calibration.
5. **T21 PEPS construction** — Begin after T20 is running; build CZX ground state in 2D first, then 3D.
6. **T23 entanglement entropy** — Run once T20 infrastructure is ready; topological entanglement entropy is the smoking gun.
7. **T24 domain walls** — Most ambitious; tackle after T20 and T21 are producing results.
8. **T26 coupled matter** — Long-term; matter-selection of arrow is the conceptual gap to bridge.
9. **T13** — Next.js interactive web presentation (can proceed in parallel with simulations).

## Open Author Decisions
- **Simulation priority and sequencing**: Which of T20–T26 to start first, and whether to run multiple simulations in parallel. T20 and T22 are recommended as parallel starting points; T25 is a quick win that can be done immediately.
- **T20 code infrastructure**: Whether to build from scratch or adapt existing open-source Z₂ LGT code (e.g., from lattice QCD community).
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
