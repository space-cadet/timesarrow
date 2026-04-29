# Statement of AI Assistance

**Manuscript**: Gauging Time Reversal Symmetry in Quantum Gravity: Arrow of Time from a Confinement-Deconfinement Transition  
**Author**: Deepak Vaid  
**Date**: April 2026  
**Public repository**: https://github.com/space-cadet/timesarrow

---

## Summary

The original manuscript was written entirely by the author between 2016 and 2018. In April 2026, the author used Claude (Anthropic, model claude-sonnet-4-6) as an AI writing assistant to prepare the manuscript for submission. The AI's role was limited to formalization, error correction, bibliography management, and LaTeX editing. All physical ideas, arguments, and conclusions originate with the author.

The complete revision history is publicly auditable via the git repository linked above.

---

## Author's Original Work (2016–2018)

Commits `a62f261` through `4914a21` (September 2018) represent the author's sole work. These establish:

- The central physical proposal: a local Z₂ gauge field on spin networks as the microscopic representation of time-reversal symmetry in Loop Quantum Gravity
- Identification of the cosmological arrow of time with a phase transition of this gauge field
- The LQG–tensor network correspondence as the substrate for the construction
- The CZX model as the relevant symmetry-protected topological (SPT) phase
- The conjecture that topologically protected edge modes yield fermionic matter degrees of freedom
- The connection between Z₂ symmetry breaking and the sign of the tetrad determinant
- All manuscript sections, appendices, figures, and the original bibliography (~100 entries)

Two section files (`spt-lqg-mapping.tex`, `z2-action-derivation.tex`) existed as short stubs (14 and 18 lines respectively), containing the author's conceptual outline but lacking full derivations.

---

## AI-Assisted Revision (April 2026)

Commits `09dfd48` through `509fb79` (April 2026) represent work done with AI assistance. The author directed all tasks; the AI executed them. Specific contributions by category:

### Formalization of author-outlined arguments

- **`spt-lqg-mapping.tex`** (commit `be14b55`): Expanded from 14-line stub to a full section with four subsections — CZX-intertwiner structural correspondence, j=1/2 sector justification, SPT=deconfined phase identification, and edge modes conjecture. The physical content was the author's; the derivations and prose were AI-drafted under author direction.
- **`z2-action-derivation.tex`** (commit `be14b55`): Expanded from 18-line stub to a full section — Z₂ gauge field definition, effective Ising action derivation, phase structure analysis with Wilson loop order parameter, and cosmological transition. Same provenance as above.
- **Discussion subsections** on Elitzur's theorem, QECC stability, and Hopf algebras (commit `be14b55`): AI-drafted based on author direction.
- **Abstract and title** (commit `be14b55`): Rewritten by AI, reviewed and approved by author.
- **"Original contributions" paragraph** in Sec. 1 (commit `41d6178`): AI-drafted.

### Error correction

- **T10** (commit `f5ef5cc`): 17 BibTeX metadata errors corrected (wrong keys, wrong journals, missing DOIs).
- **T11** (commits `808a710`, `41d6178`): Five critical errors fixed, including a gauge invariance argument (τ²=1 vertex cancellation), correction of the U_CZX operator framing, and an internally inconsistent basis calculation. Supplementary calculations document (`supplementary-calculations.tex`) drafted by AI to record these fixes.
- **T12** (commits `829c42b`, `41d6178`): Nine major issues addressed, including terminology corrections (SSB→confinement-deconfinement language, "first order"→"second order" universality class), clarification of the edge-mode T²=−1 argument, and dimensional mismatch resolution.
- **T8** (commit `ca78bc5`): Typographic and structural fixes throughout.

### Literature updating

- **~20 new bibliography entries** added (commits `f5ef5cc`, `829c42b`), covering 2018–2026 literature on holographic spin networks, Z₂ lattice gauge theory, SPT classification, and intertwiner entanglement.

### 3D SPT classification

- **Sec. 7.3 revision** (commits `2a5fd1e`, `509fb79`): AI surveyed the classification of 3D bosonic SPT phases with Z₂ᵀ symmetry (H⁴(Z₂ᵀ, U(1)_𝒯) ≅ ℤ₂) and integrated the result into the manuscript, resolving a dimensional mismatch noted in peer review preparation. The identification of the non-trivial SPT class with the spin-network state was made by the author; the survey and write-up were AI-executed.

### New figure

- **`figures/tns-matrix-insertion-2d.tex`** (commit `ca78bc5`): TikZ figure showing M/M⁻¹ matrix insertion on a 2D tensor network subregion, replacing a `\todo` placeholder. Drafted by AI to author's specification.

---

## What the AI Did Not Do

- Propose any new physical mechanism or hypothesis
- Identify the relevant condensed matter models (CZX, toric code) — these were the author's choices
- Select the research question or the LQG framework
- Generate any figures other than the one noted above
- Write any of the appendices (all pre-existing author work)

---

## Author Responsibility

The author reviewed all AI-generated content, approved all changes, and takes full scientific responsibility for the manuscript as submitted. The AI was used as a writing and formalization tool, analogous to a technically knowledgeable editor.
