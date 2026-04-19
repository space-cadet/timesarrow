# 3D SPT Phases with Z₂ Time-Reversal Symmetry — Survey Needed

*Created: 2026-04-20*
*Status: 🔄 ACTIVE — tracked as `tasks/T15.md`; survey and matching to spin-network phase in progress*
*Related Task: [T15: 3D SPT Survey and Mapping](../tasks/T15.md)*

## Why This Is Needed

The paper's current M14 fix (spt-lqg-mapping.tex, subsection "The CZX SPT Phase as the Deconfined Phase") acknowledges the 2D/3D dimensional mismatch and defers a detailed matching to future work:

> "Three-dimensional bosonic SPT phases protected by Z₂ time-reversal symmetry have been classified [Vishwanath2013Physics, Kapustin2014Symmetry], and the deconfined phase of the 3D Z₂ gauge theory falls within this classification. A detailed matching of the 3D spin-network phase to the appropriate entry in this classification is left for future work."

This is honest but leaves an obvious referee question unanswered. A follow-up paper (or a more detailed appendix) should close this gap.

## What Needs To Be Done

1. **Survey the classification of 3D bosonic SPT phases with Z₂ᵀ symmetry.**
   - Key references: Vishwanath & Senthil 2013 (PRX 3, 011016; arXiv:1209.3003), Kapustin 2014 (arXiv:1403.1467), Freed & Hopkins 2021 (arXiv:1604.06527), Chen-Gu-Liu-Wen 2013 (arXiv:1106.4772)
   - How many distinct 3D Z₂ᵀ SPT phases are there? (Group cohomology gives H³(Z₂ᵀ, U(1)) = Z₂, so two phases: trivial and non-trivial)
   - What are the physical signatures of the non-trivial 3D Z₂ᵀ SPT? (Surface topological order, quantized magnetoelectric response, etc.)

2. **Identify which phase the deconfined Z₂ gauge theory on spin networks corresponds to.**
   - The deconfined phase of 3D Z₂ LGT = Z₂ toric code in 3+1d (Dennis et al. 2002, arXiv:quant-ph/0110143)
   - Is the 3+1d toric code the gauged version of the non-trivial 3D Z₂ᵀ SPT, or the trivial one?
   - Key: gauging the trivial SPT gives standard toric code; gauging the non-trivial SPT gives a twisted toric code with different anyon statistics (Levin & Gu 2012, arXiv:1202.3120)

3. **Determine which 3D SPT the spin-network state realizes.**
   - The CZX model in 2D is the non-trivial Z₂ SPT in 2D. Its 3D analogue is the non-trivial entry in H³(Z₂ᵀ, U(1)) = Z₂.
   - Does the spin-network intertwiner structure (4-valent vertex, j=1/2) match the non-trivial 3D SPT, or is a different vertex valence/spin needed?

4. **Check whether the edge modes (fermionic conjecture) are consistent with the 3D classification.**
   - The non-trivial 3D Z₂ᵀ SPT has surface states that are a topological insulator surface (gapless Dirac fermions protected by time-reversal). This would directly support the fermionic edge mode conjecture.
   - Reference: Vishwanath & Senthil 2013, Section III on surface states.

## Key Papers To Read

| Paper | arXiv | Relevance |
|-------|-------|-----------|
| Vishwanath & Senthil 2013 | 1209.3003 | 3D bosonic SPT classification; surface states |
| Kapustin 2014 | 1403.1467 | Cobordism classification beyond group cohomology |
| Freed & Hopkins 2021 | 1604.06527 | Invertible phases and cobordism |
| Levin & Gu 2012 | 1202.3120 | Gauging Z₂ SPT → twisted toric code |
| Chen-Gu-Liu-Wen 2013 | 1106.4772 | Group cohomology classification |
| Dennis et al. 2002 | quant-ph/0110143 | 3+1d toric code and QECC |
| Wang & Senthil 2013 | 1302.6234 | Boson topological insulators in 3D |

## Expected Outcome

A short appendix or follow-up paper establishing:
- The spin-network Z₂ᵀ SPT phase is the non-trivial element of H³(Z₂ᵀ, U(1)) = Z₂
- Its gauging gives the 3+1d toric code (deconfined Z₂ gauge theory)
- The surface states are gapless Dirac fermions, consistent with the fermionic edge mode conjecture

This would significantly strengthen the paper's central claim and close the dimensional-mismatch objection.
