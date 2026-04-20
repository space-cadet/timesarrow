---
source_branch: master
source_commit: ca78bc5804f479d9227d2071db3310ae42ef4247
---

# Session 2026-04-20 - Afternoon
*Created: 2026-04-20 12:36:54 IST*
*Last Updated: 2026-04-20 12:36:54 IST*

## Focus Task
T15: 3D SPT Survey and Mapping - Final Completion
**Status**: ✅ (Completed)

## Active Tasks
### T15: 3D SPT Survey and Mapping
**Status**: ✅ (Completed)
**Progress**:
1. ✅ Survey classification of 3D bosonic SPT phases (H⁴(Z₂ᵀ, U(1)_T) = Z₂)
2. ✅ Identify non-trivial SPT phase (twisted 3+1d toric code)
3. ✅ Revise fermionic edge mode conjecture (gapless → gapped all-fermion toric code)
4. ✅ Document findings in implementation detail docs
5. ✅ Integrate Sec 7.3/7.4 edits into main manuscript (timesarrow.tex)
6. ⬜ Verify 3D spin-network anyon statistics (delegated to T15.1)

### T13: Gemini 3 Flash - Web Presentation
**Status**: 🔄 (In Progress)
**Progress**:
1. ✅ Implementation plan drafted
2. ⬜ Initialize Next.js scaffold

### T14: Kimi K2.5 - Minimal Web Presentation
**Status**: 🔄 (In Progress)
**Progress**:
1. ✅ Implementation plan drafted with ASCII diagrams
2. ⬜ Initialize `/web-static/` directory

## Context and Working State
This session completed the final manuscript corrections and infrastructure fixes:

### Manuscript Corrections
- **M9 (j=1/2 dominance)**: Replaced invalid "exponentially more states / combinatorial dominance" argument with two defensible ones: (i) thermal Boltzmann suppression below Planck temperature (β > 2/κ), and (ii) Bekenstein-Hawking black hole entropy argument. Added citations Meissner2004Black-hole and Domagala2004Black-hole to timesarrow.bib.
- **SciPost template fields**: Replaced stale NITK/IUCAA affiliation with "Independent Researcher"; cleaned up template TODO comments.
- **Acknowledgements**: Rewritten to reflect past 2018 Visiting Associateship at IUCAA rather than current support.
- **"gapless/gapped" inconsistency**: Resolved throughout — abstract, introduction, contributions paragraph, Sec 7.3 bullet, and future directions. The ungauged CZX has gapless modes; the gauged/deconfined phase has gapped surface order (all-fermion toric code). Language updated to "topologically protected surface excitations" everywhere the conjecture is stated.
- **Sec 7.3 dimensional paragraph**: The 3D SPT classification result H⁴(Z₂ᵀ, U(1)_𝒯) ≅ ℤ₂ now stated explicitly before deferring the detailed matching.

### Infrastructure Fix
- **Empty .bbl bug**: MiKTeX's x86_64 biber symlink at `/usr/local/bin/biber` was crashing silently under Rosetta on Apple Silicon, producing an empty `.bbl`. Fix: removed the MiKTeX symlink, allowing the homebrew arm64 biber at `/opt/homebrew/bin/biber` to take precedence. Documented in implementation-details/biber-infrastructure-fix.md.

### Status Verification
- Confirmed T15 (3D SPT survey) was already complete in the manuscript.
- Confirmed C3a/C3b/M6a/M6b corrections from supplementary calculations were already applied.
- Confirmed original contributions paragraph, Appendix D sub-labels, and \wrt macro all correctly in place from prior sessions.

The manuscript builds cleanly and is ready for submission.

## Critical Files
- `timesarrow.tex`: Main manuscript (all corrections applied)
- `timesarrow.bib`: Updated with Meissner2004Black-hole and Domagala2004Black-hole citations
- `memory-bank/tasks/T15.md`: Marked as completed
- `memory-bank/tasks/T12.md`: Updated with M9 refinement notes
- `memory-bank/implementation-details/biber-infrastructure-fix.md`: Infrastructure fix documentation

## Session Notes
- T15 is now complete. All manuscript work is done.
- Only web presentation tasks (T13, T14) remain active.
- Manuscript is ready for submission to SciPost.
