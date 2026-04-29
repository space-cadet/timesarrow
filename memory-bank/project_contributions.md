---
name: Contribution Record
description: Delineation of Deepak Vaid (author) vs. AI assistant contributions to the manuscript
type: project
---
# Contribution Record: Author vs. AI Assistant

*Created: 2026-04-20*

## Summary

The manuscript has two clearly separable layers of origin: the **original intellectual content** (Deepak Vaid, 2018 and prior) and **revision/formalization work** done collaboratively in April 2026 (AI-assisted sessions).

---

## Deepak Vaid's Contributions (pre-April 2026)

Everything present in git through commit `4914a21` (2018-09-10) is entirely the author's original work. This includes:

**Core physics ideas** — all original to the author:

- The central proposal: Z₂ gauge field on spin networks as local time-reversal symmetry
- Identification of the cosmological arrow of time with a phase transition
- The LQG–tensor network correspondence as the substrate
- The CZX model as the relevant SPT phase
- The conjecture that edge modes yield fermionic matter
- The tetrad determinant as the macroscopic manifestation of Z₂ symmetry

**Manuscript structure** — written by the author:

- Introduction and motivation (Sec 1)
- Topological order and spacetime geometry (Sec 2)
- MPS/TNS pedagogy (Sec 3)
- Spin networks section (Sec 4)
- Volume operator and Z₂ symmetry (Sec 5)
- CZX state description (Sec 6, original version)
- All appendices (time reversal, ADM/tetrads, GR time reversal, quantum geometry, invariant tensors)
- Original bibliography (~100 entries)
- All figures (TikZ, Draw.io, PNG)

**Stubs present in 2018** (ideas present but underdeveloped):

- `spt-lqg-mapping.tex` — 14 lines, placeholder
- `z2-action-derivation.tex` — 18 lines, placeholder

---

## AI Assistant Contributions (April 2026 sessions)

The AI assistant's role was **formalization, gap-filling, error-correction, and literature updating** — not originating the physics. Specifically:

**Rewrites of underdeveloped sections** (commits `be14b55`, `09dfd48`):

- `spt-lqg-mapping.tex` — expanded from 14-line stub to full section with 4 subsections: CZX-intertwiner correspondence, j=1/2 justification, SPT=deconfined identification, edge modes conjecture. The *ideas* were the author's; the *formalization and prose* are AI-drafted.
- `z2-action-derivation.tex` — expanded from 18-line stub to full section: Z₂ field definition, effective action derivation, phase structure with Wilson loop, cosmological transition. Same caveat: physics is the author's; derivation write-up is AI-drafted.
- Discussion subsections on Elitzur's theorem, QECC stability, Hopf algebras — AI-drafted based on author direction.
- Title change to "...Confinement-Deconfinement Transition" — proposed by AI, accepted by author.
- Abstract rewrite — AI-drafted with author approval.
- "Original contributions" paragraph (line 247) — AI-drafted.

**Error correction** (commits `ca78bc5`, `f5ef5cc`, `41d6178`, `808a710`):

- 17 BibTeX metadata errors fixed (T10)
- 5 critical manuscript errors fixed (T11): gauge invariance sentence, U_CZX framing correction, supplementary calculations
- `supplementary-calculations.tex` — entirely AI-drafted (calculations for C3/M6/M9)
- Missing figure `figures/tns-matrix-insertion-2d.tex` — AI-drafted TikZ (T9)
- Typo/structural fixes (T8)

**Literature updating** (commits `829c42b`, `f5ef5cc`):

- ~20 new bibliography entries added (2018–2026 literature)
- Citation calls inserted at appropriate manuscript locations

**3D SPT survey and Sec 7.3 revision** (commits `2a5fd1e`, `509fb79`):

- 3D SPT classification result H⁴(Z₂ᵀ, U(1)_𝒯) ≅ ℤ₂ integrated into manuscript
- Gapped all-fermion toric code replacing "gapless Dirac fermions" — AI-proposed correction, accepted by author
- Gapless/gapped terminology resolved throughout

**Infrastructure and documentation**:

- Memory bank system — entirely AI-created
- All session/task tracking files

---

## Boundary Principles

- **Physics originates with the author.** No AI contribution introduced a new physical claim not already latent in the author's 2018 draft or not explicitly directed by the author in session.
- **Formalization is shared.** The derivations in the expanded sections were written by the AI but based on the author's conceptual framework.
- **Error corrections are AI-identified but author-approved.** Every fix (C1–C5, M6–M14) was made with the author's knowledge and acceptance.
- The author retains full intellectual ownership of all scientific content.

---

## For Future Reference (AI Disclosure)

If journal disclosure of AI assistance is required, the scope is: manuscript editing, bibliography management, LaTeX typesetting, and formalization of author-provided physics arguments. The AI did not originate physical claims or perform novel calculations independently.
