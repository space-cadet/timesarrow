# Active Context
*Last Updated: 2026-04-18 02:12:39 IST*

## Current Status
Three subagent audits completed (2026-04-18 night). Full findings recorded in T10, T11, T12.

## Audit Summary

### Agent A — Reference Verification
- 42/59 cited entries clean; 17 need fixes; 0 unverifiable
- Highest priority: Markopoulou2000Quantum (wrong journal: CMP→CQG 17, 2059)
- Full details and fix list: `tasks/T10.md`

### Agent B — Claim Audit + Recent Literature
- ~15 external attributions verified; no fabricated citations
- Two real errors: spin-foam "A_v ~ j^{-α}" overclaim; "first order in 3+1d" Z₂ LGT (should be second-order)
- ~20 recent papers (2018–2026) identified; 5 must-cite for reviewer protection
- Full details: `tasks/T12.md`

### Agent C — Manuscript Quality Audit
- 5 critical issues (block publication), 9 major issues, 9 minor issues
- Most critical: "We" glyph corruption in ~10 equations; Ψ₁/Ψ₂ central derivation internally inconsistent
- Full details: `tasks/T11.md` (critical) and `tasks/T12.md` (major)

## Active Tasks
- **T13**: Gemini 3 Flash - Create Accessible Web Presentation — 
- **T11**: Fix Critical Manuscript Errors — ⬜ CRITICAL
- **T10**: Fix 17 bib metadata errors — ⬜
- **T12**: Major issues + recent citations — ⬜
- **T7**: Trim MPS Pedagogy — still open, not yet started

## Implementation Docs Created (2026-04-18)
- `implementation-details/gemini-web-presentation-plan.md` — 9 groups/programs; Chirco-Colafranceschi-Oriti, Han, Qi, Swingle, HaPPY, Singh-McMahon etc.
- `implementation-details/arrow-of-time-survey.md` — 16 approaches surveyed with acceptance ratings
- `supplementary-calculations.tex` — **compiled cleanly (14pp PDF, verified)**; works out T11/C3, T12/M6, T12/M9

Key findings from supplementary calculations:
- Ψ₁ in manuscript is NOT a singlet; Ψ₂/2 = −Φ₁ is correct
- Time orientation = eigenvalue of signed Q̂ (not V̂, which is degenerate)
- U_CZX does not preserve the singlet subspace; LQG–CZX is structural correspondence
- j=1/2 thermal dominance holds for β > 2/κ; entropy claim needs replacing with BH entropy argument

## Recommended Next Session Order
1. **T11** first — "We" bug (easy) + D_e formula (easy) + gauge-invariance sentence (easy) = 3 of 5 criticals in minutes
2. **T11/C3** — use supplementary-calculations.tex as the derivation; replace Ψ₁/Ψ₂ with Φ₁/Φ₂ and reframe V̂ → Q̂
3. **T12/M6** — reframe LQG–CZX using Result 5 from supplementary doc
4. **T10** — bib metadata fixes (mechanical, batch in one pass)
5. **T12** — remaining major issues and new citations
6. **T7** — MPS trimming (lower priority)

## Open Author Decisions (unchanged from previous session)
- Appendix D: sub-sections labeled A/B/C/D shadow top-level appendix labels
- Abstract: SPT framing leads; confinement-deconfinement should lead per title
- New (from audit): add explicit "original contributions" paragraph at end of Sec 1

## Document Statistics
- Pages: 36
- LaTeX: builds cleanly
- Pending: T7 (trim), T10 (bib), T11 (critical fixes), T12 (major fixes + new cites)
