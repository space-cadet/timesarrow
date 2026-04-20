# T15 Resolution Summary: 3D SPT Classification Survey Complete

**Status**: ✅ COMPLETE - Ready for appendix drafting  
**Date**: 2026-04-20  
**Output Document**: `3d-spt-survey-results.md` (468 lines, 26 KB)

---

## The Problem (T15)

The paper defers matching the 2D CZX SPT model to a 3D classification:

> "Three-dimensional bosonic SPT phases protected by Z₂ time-reversal symmetry have been classified [Vishwanath & Senthil 2013, Kapustin 2014], and the deconfined phase of the 3D Z₂ gauge theory falls within this classification. A detailed matching of the 3D spin-network phase to the appropriate entry in this classification is left for future work."

---

## The Solution (Resolved via Literature Survey)

### Key Finding 1: Classification
- **H⁴(Z₂ᵀ, U(1)_T) = Z₂** → exactly **2 distinct 3D bosonic SPT phases**
- Both group cohomology and cobordism agree (no exotic phases)
- Trivial and non-trivial classes

### Key Finding 2: Gauging Rules
- **Trivial 3D Z₂ᵀ SPT → gauged to standard 3+1d toric code** (Dennis et al. 2002)
- Non-trivial 3D Z₂ᵀ SPT → twisted toric code (modified anyon statistics)
- Levin-Gu (2012) precedent in 2D extends to 3D

### Key Finding 3: Spin-Network Phase Identity
- Deconfined Z₂ gauge theory on spin networks = **standard 3+1d toric code** ✓
- By reverse-engineering: ungauged phase = **TRIVIAL 3D Z₂ᵀ SPT**
- NOT the non-trivial phase

### Key Finding 4: Surface States (CRITICAL!)
- **Non-trivial 3D Z₂ᵀ SPT surface**: Gapped all-fermion toric code (Vishwanath-Senthil 2013)
- NOT gapless Dirac fermions (that's fermionic topological insulator)
- Trivial 3D Z₂ᵀ SPT surface: No protected SPT modes

### Key Finding 5: Edge Mode Inconsistency (⚠️ IMPORTANT)
- **Paper's conjecture**: "gapless edge modes of this SPT phase give rise to fermionic matter"
- **Classification says**: Trivial SPT has no protected gapless boundary modes
- **Implication**: Fermionic matter must arise from **different mechanism** (e.g., domain walls, lapse sign change)
- **Action needed**: Revise or separate the SPT story from fermion origin story

---

## What This Means for the Paper

### ✅ Can Assert Firmly
1. "The deconfined phase = standard 3+1d toric code"
2. "This is classified within H⁴(Z₂ᵀ, U(1)_T) = Z₂"
3. "Spin-network structure matches CZX on-site Hilbert space"
4. "Z₂ gauge theory provides topological stability to time orientation"

### ⚠️ Must Revise
1. The fermionic edge mode conjecture (not supported by 3D SPT surface structure)
2. May need to decouple SPT stability (which is solid) from fermion origin (which is open)

### 📝 Can Acknowledge Openly
1. "Explicit 3D lattice model combining SPT + spin-network geometry remains open"
2. "Whether fermions arise from SPT surface order or domain wall physics requires further analysis"
3. "Non-trivial 3D Z₂ᵀ SPT may have future role in LQG framework"

---

## Appendix Drafting Checklist

- [ ] **Section A** (Review 3D Z₂ᵀ SPT classification)
  - H⁴(Z₂ᵀ, U(1)_T) = Z₂
  - Cite Vishwanath-Senthil, Chen-Gu-Liu-Wen, Kapustin
  - 1-2 pages

- [ ] **Section B** (Gauging procedure)
  - Explain 2D precedent (Levin-Gu 2012)
  - Extend to 3D: trivial → standard toric code
  - Conclude: deconfined phase = gauged trivial SPT
  - 1-2 pages

- [ ] **Section C** (Surface states and signatures)
  - Non-trivial phase: all-fermion toric code (GAPPED, not Dirac fermions)
  - Contrast with fermionic topological insulator
  - Quantized magnetoelectric response
  - 1-2 pages

- [ ] **Section D** (Spin-network matching)
  - 4-valent j=1/2 = CZX on-site Hilbert space
  - Deconfined = standard toric code = gauged trivial SPT
  - Open problem: explicit 3D lattice model
  - 1 page

- [ ] **Section E** (Open questions)
  - 3D lattice model construction
  - Role of non-trivial phase
  - Domain wall gravity effects
  - 0.5 page

---

## Key Papers (Quick Reference)

| Code | Paper | arXiv | Key Point |
|------|-------|-------|-----------|
| VS13 | Vishwanath & Senthil 2013 | 1209.3003 | 3D bosonic SPT classification; surface = all-fermion toric code |
| K14 | Kapustin 2014 | 1403.1467 | Cobordism = cohomology for Z₂ᵀ in d≤3 |
| LG12 | Levin & Gu 2012 | 1202.3120 | 2D precedent: trivial SPT → toric code |
| CGLW13 | Chen-Gu-Liu-Wen 2013 | 1106.4772 | Group cohomology formula H^{1+d} |
| D02 | Dennis et al. 2002 | quant-ph/0110143 | 3+1d toric code (standard) |
| WS13 | Wang & Senthil 2013 | 1302.6234 | 3D boson topological insulators |
| CV15 | Chen & Vishwanath 2015 | 1401.3736 | Gauging time-reversal on tensor networks |

---

## Document Structure (3d-spt-survey-results.md)

1. **Executive Summary** — 6 main findings
2. **Classification Summary** — H⁴ = Z₂, group cohomology vs cobordism
3. **Physical Signatures** — surface states, magnetoelectric response
4. **Gauging Rules** — which SPT → which gauge theory
5. **3D CZX Analogue** — existing constructions and gaps
6. **Spin-Network Matching** — which phase is realized?
7. **Edge Modes Consistency** — CRITICAL ISSUE identified
8. **Appendix Structure** — detailed outline for paper revision
9. **Firm vs. Soft Claims** — guidance on what to assert vs. revise
10. **Key Citations** — full reference table
11. **Reframing Guidance** — three revised versions of central claim
12. **Final Checkpoints** — verification checklist

---

## Next Steps

1. **Read** `3d-spt-survey-results.md` thoroughly (especially Sections 3, 6, 7, 8)
2. **Decide** on which reframing option (Section 10) best fits the paper
3. **Draft appendix** using Section 7 outline
4. **Test claims** against the 9 citations in Section 9
5. **Revise** paper text to separate SPT stability story from fermion origin story
6. **Optional**: Explore whether non-trivial 3D Z₂ᵀ SPT has any LQG application

---

## Critical Points for Reviewer Argument

✅ **Strong position**: "The deconfined phase of our Z₂ gauge theory is the standard 3+1d toric code, which falls within the established 3D Z₂ time-reversal SPT classification (H⁴ = Z₂). This provides topological protection for the cosmological arrow of time."

⚠️ **Honest position on fermions**: "The origin of fermionic matter from SPT structure is an open question. The 3D classification suggests that if the ungauged phase is the trivial SPT (as indicated by our toric code result), then fermionic degrees of freedom must arise from a complementary mechanism—such as the interaction of the SPT structure with spacetime domain walls where the lapse function changes sign. We leave a complete analysis for future work."

📝 **Gap acknowledgment**: "An explicit 3D lattice model realizing both the Z₂ᵀ SPT structure and the 4-valent spin-network geometry remains a valuable open problem for future research."

---

*Document prepared: 2026-04-20 by comprehensive literature survey*  
*Status: Ready for appendix drafting and paper revision*
