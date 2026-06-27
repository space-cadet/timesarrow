# Session: 2026-05-05 Peer-review

**Started**: -
**Focus Task**: None
**Status**: ✅ PEER REVIEW COMPLETE; FIXES APPLIED AND COPIED TO SUBMISSION BUNDLE

## Work Done

---
source_branch: main
source_commit: 89816d1a9be1060870f068c509ca9ce0429b1014
---

# Session 2026-05-05 — AI Peer Review (Final Manuscript Pass)
*Created: 2026-05-05 01:31 IST*
*Last Updated: 2026-05-05 02:42 IST*

## Focus Task
T17: arXiv Submission Preparation — Final peer review before upload
**Status**: ✅ Peer review complete; fixes applied and copied to submission bundle

## Session Type
AI Peer Review / Pre-submission audit

## Issues Identified and Resolved

### 🔴 Critical
| # | Issue | Status | Resolution |
|---|-------|--------|------------|
| 1 | Appendix F (`subsec:czx-intertwiner`) computed $U_{CZ}|\Phi_1\rangle$ using supplementary-calculations basis while claiming to use manuscript `eqn:vol-states` basis | ✅ Fixed | Updated computation to use manuscript basis; added note that $U_{CZ}|\Phi_2\rangle = -|\Phi_2\rangle$ (singlet) but $U_{CZ}$ does not preserve the **full** 2D subspace |
| 2 | Line 1437 conflated $SU(2)$ Gauss constraint with $Z_2$ gauge parameter $\tau_v$ | ✅ Fixed | Rewrote to clarify: $SU(2)$ Gauss constraint $\sum \vec{J}_i = 0$ reduces to effective discrete $Z_2$ on $j=1/2$ intertwiner qubit; $\tau_v^2=1$ is the generator of that discrete symmetry |

### 🟠 Major
| # | Issue | Status | Resolution |
|---|-------|--------|------------|
| 3 | $A_{\min} = 4\sqrt{3}\,\gamma\,l_p^2$ missing factor of $\pi$ | ✅ Fixed | Corrected to $4\sqrt{3}\,\pi\,\gamma\,l_p^2$ |
| 4 | Universality class claim "3d $Z_2$ gauge theory = 3d Ising" ambiguous | ✅ Fixed | Added footnote distinguishing $T=0$ quantum transition in $3+1$D (3D quantum Ising) from classical 3D treatment (2D classical Ising via duality) |
| 5 | Introduction claim (iv) overstated literal $U_{CZX}$ action on intertwiner subspace | ✅ Fixed | Reframed as structural correspondence of $Z_2$-invariant effective qubits |
| 6 | 2D CZX vs 3D spin-network correspondence lacked justification for restricting to regular graphs | ✅ Fixed | Added paragraph arguing regular spatial lattices dominate partition function at low energy, analogous to $j=1/2$ dominance |

### 🟡 Moderate
| # | Issue | Status | Resolution |
|---|-------|--------|------------|
| 7 | Thermal suppression argument dimensionally inconsistent ($\beta$ vs energy units) | ✅ Fixed | Explicitly stated Planck units ($\hbar=c=G=1$) for the argument; restored dimensions for $T_c$ at the end |
| 8 | MPS universality statement misleading about required bond dimension | ✅ Fixed | Added caveat: generic states require exponential bond dimension; MPS efficient only for area-law states |
| 9 | Abstract hyphen/en-dash inconsistency with title | ✅ Fixed | Changed title and abstract to use `--` (en-dash) for "confinement–deconfinement" |

## Author Responses and Clarifications

- **Singlet basis (#1)**: Author confirmed manuscript states are valid orthonormal singlets in a different basis from supplementary calculations (related by basis rotation). The AI initially reached a false negative due to a computational error mixing up $S^+$ and $S^-$ actions. Author's physics is correct.
- **$Z_2$ reduction (#2)**: Author clarified that $Z_2$ emerges as the effective discrete symmetry when $SU(2)$ is restricted to the $j=1/2$ intertwiner qubit — the continuous symmetry "reduces to" the discrete one in this context.
- **Universality class (#4)**: Author accepted the footnote hedge as the safest approach.
- **Regular graphs (#6)**: Author endorsed the "regular-lattice dominance" paragraph and noted a systematic derivation from spin-foam dynamics remains an open problem.

## Files Modified
- `timesarrow.tex` — 9 edits applied
- `arxiv_submission_v1/timesarrow.tex` — copied from root

## Build Verification
- `pdflatex` + `biber` + `pdflatex` × 2: clean, 42 pages, stable output

## arXiv Upload
- **Time**: 2026-05-05 02:42 IST
- **Reference**: `submit/7550944`
- **Status**: On hold (arXiv standard review queue)
- **Bundle**: `arxiv-submission-v1.tar.gz` (files at root level, no top-level directory)
- **Addendum**: Full AI assistance statement restored and included

## Next Steps
- Wait for arXiv moderation decision
- T13 (web presentation) remains active task


