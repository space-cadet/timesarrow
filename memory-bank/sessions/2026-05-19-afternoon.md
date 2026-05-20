---
source_branch: main
source_commit: 89816d1a9be1060870f068c509ca9ce0429b1014
---

# Session 2026-05-19 - Afternoon
*Created: 2026-05-19 15:35:00 IST*
*Last Updated: 2026-05-19 15:35:00 IST*

## Focus Task
T18: Manuscript Clarification - Confinement-Deconfinement Terminology and Mikhail Q&A
**Status**: Discussion recorded for future manuscript revision

## Context
User continued a stale session from May 12. After clarifying the current date/time, discussion shifted to the timesarrow paper. User had received questions from colleague Mikhail and wanted to verify paper content. A significant terminology discussion ensued regarding confinement-deconfinement conventions, which resolved in favor of the paper's existing mapping but identified a need for a clarifying footnote.

## Dialog Summary

### Part 1: Locating the Paper and arXiv Moderation

User asked about the timesarrow paper location. Paper was found at arXiv:2605.16316, repo at github.com/space-cadet/timesarrow, local clone at ~/code/timesarrow/ (empty, needs population from remote).

Discussion of arXiv moderation:
- Paper was held for two weeks then placed in general-physics
- User believes they are on a moderation "list" due to prior criticism of arXiv
- User was quoted in Indian Express / Scientific American article about arXiv moderation problems
- Quoted as saying: "They are taking actions which seem to go against what the role of a preprint server should be" and "inconsistent moderation and a lack of transparency"
- User suspects hep-th moderators (string theory community) resist LQG-related work in hep-th
- Paper was intentionally submitted to hep-th because it uses hep-th methods (Wilson loops, confinement-deconfinement, SPT phases, topological order) even though the substrate is spin networks

### Part 2: Mikhail's Questions and Answers

Mikhail (via image attachment) asked two questions about the paper:

**Q1: Why should Phi_1 and Phi_2 be orthogonal? Why can't they be totally symmetric vectors?**

Answer:
- Orthogonality is convenient but not crucial
- The crucial requirement is that states are SU(2) singlets (total angular momentum zero), demanded by the Gauss constraint
- Eq. (31) gives the orthonormal singlet basis; Supplementary Calculations give the full Clebsch-Gordan derivation
- Totally symmetric vectors live in the j=2 (5-dimensional) symmetric subspace, which is orthogonal to the singlet subspace
- Therefore totally symmetric vectors cannot be singlets
- Phi_1 and Phi_2 happen to be orthonormal because they are eigenvectors of the signed volume operator Q-hat with eigenvalues plus/minus q
- Any basis of the 2D singlet subspace would work mathematically

**Q2: Why n=4? Where does time live on the spin network? Is there a space-time symmetry?**

Answer:
- n=4: A vertex with n edges represents an n-faced quantum polyhedron in 3D space. A 4-valent vertex is a quantum tetrahedron -- the simplest case. j=1/2, n=4 chosen for calculational tractability. Higher valence is noted as perturbations that do not change the universality class.
- Time lives NOWHERE on the spin network. The spin network is purely spatial.
- Time enters externally through the tetrad formalism. Eq. (35) shows flipping the triad sign changes the local 3D volume determinant det(3e). Since det(4e) = N(t) * det(3e), this is equivalent to flipping the lapse sign.
- No space-time symmetry. The Z_2 action flips time orientation (lapse sign / volume sign) but does not touch spatial directions. The paper is explicit about this in the Discussion (Section 9, "Time Reversal in Spin Networks").

Key references identified:
- Eq. (31) and surrounding text (Section 5)
- Supplementary Calculations (Appendix/Supplementary, Section 1)
- Eq. (28) for the decomposition
- Discussion Section 9, around Eq. (35)
- Lines 1108-1112: explicit statement that spin networks are spatial with no knowledge of lapse

### Part 3: Search Engine Discoverability

Tested whether the paper appears in generic searches:
- With user name + topic: Yes, prominently
- With specific technical terms (confinement-deconfinement, spin network, Z2 gauge): Yes, first result
- With truly generic terms (origin arrow of time quantum gravity): No, does not appear

Conclusion: The paper is findable by specialists who know the keywords, but invisible to broad discoverability. The general-physics placement does hurt visibility.

### Part 4: Confinement-Deconfinement Terminology Crisis

User expressed concern that the confinement-deconfinement mapping in the paper might be backwards.

User's initial concern: In QCD, the deconfining phase is the high-temperature phase where quarks are free, and the confining phase is the low-temperature phase where they are bound. This seems opposite to the paper's mapping.

Resolution:
- QCD is a THERMAL phase transition at finite temperature
- The paper uses QUANTUM phase transition at T=0, driven by coupling K
- The paper follows the standard Z_2 lattice gauge theory / toric code convention (Kogut-Susskind / Wen):
  - Deconfined = perimeter law = topological ordered vacuum = toric code ground state = ordered
  - Confined = area law = trivial disordered vacuum = product state
- This convention is established in literature cited by the paper: Levin 2012, Haegeman 2015, Chen-Vishwanath
- Verified against multiple external sources:
  - arXiv:2601.16776: "Wilson loops obey perimeter law and area law in the deconfined and confined phases respectively"
  - PRX Quantum 2022: "deconfined (small h) to confinement (large h)"
  - Shankar QFT textbook: "area or perimeter law (corresponding to confined or deconfined phases)"

User's panic was justified by the QCD intuition but resolved by recognizing the different physical context. The paper is correct as written.

### Part 5: Two Different "Area" Concepts

User raised a subtle question:
- In the deconfined phase, Wilson loops follow perimeter law
- But semiclassical geometry should have non-zero area for 2-surfaces
- Would this not correspond to the confined phase with area law for Wilson loops?

Resolution:
- These are two COMPLETELY different "area" concepts:
  1. Wilson loop "area law" = decay rate of Z_2 flux correlations proportional to lattice plaquettes enclosed
  2. LQG area operator = eigenvalue of geometric area from SU(2) spin labels
- The Z_2 gauge theory does NOT destroy geometric area
- Even in the confined phase, j=1/2 edges still carry non-zero area eigenvalues
- What Z_2 disorder destroys is the COHERENCE of time orientation across the network
- Locally, geometry exists in both phases. Globally, only the deconfined phase has uniform time orientation.

Analogy: Confined phase = pile of tetrahedra with randomly flipped time orientations. Each has volume and area, but no consistent "future" direction globally.

### Part 6: Recommendation for Paper Revision

Identified need for a clarifying footnote or paragraph in the paper to address the QCD vs Z_2 convention confusion. Proposed text and full discussion archived in implementation docs.

**Note:** Full GPT 5.5 peer review, GPT 5.5's response to Kimi comparison, and the synthesis of both discussions are archived in:
- `memory-bank/implementation-details/ai-reviews/gpt55-peer-review-2026-05-19.md`
- `memory-bank/implementation-details/ai-reviews/gpt55-response-to-kimi-comparison-2026-05-19.md`
- `memory-bank/implementation-details/ai-reviews/kimi-gpt55-synthesis-2026-05-19.md`

## Decisions Made
- Paper's confinement-deconfinement mapping is CORRECT as written
- Need to add a footnote clarifying the QCD vs Z_2 convention difference
- Mikhail's questions were answered with specific equation and section references
- User has citations ready to send to Mikhail

## Next Steps
- User may add the proposed footnote to timesarrow.tex
- User may send citation-rich reply to Mikhail
- No structural changes needed to the paper's physics claims

## References Used
- timesarrow.tex (local repo ~/code/timesarrow/)
- supplementary-calculations.tex
- External literature verification:
  - arXiv:2601.16776 (Z_2 LGT on non-trivial topology)
  - arXiv:1701.00762 (X-cube duality)
  - arXiv:2012.05232 (gauge equivariant networks)
  - PRX Quantum 3, 020320 (2022) (VQE for Z_2 LGT)
  - Shankar, QFT and Condensed Matter
  - arXiv:1506.01247 (dissipationless cosmology arrow of time)
  - arXiv:0910.5836 (Kiefer quantum cosmology arrow)
  - Various arXiv moderation articles (Indian Express, Scientific American)
