# Statement of AI Assistance

**Manuscript**: Gauging Time Reversal Symmetry in Quantum Gravity: Arrow of Time from a Confinement-Deconfinement Transition  
**Author**: Deepak Vaid  
**Date**: April-May 2026
**Public repository**: https://github.com/space-cadet/timesarrow

---

## Summary

The original manuscript was written entirely by the author between 2016 and 2018. In April-May 2026, the author used AI systems as technical writing and review assistants to prepare and refine the manuscript. These included Claude (Anthropic, model claude-sonnet-4-6), GPT-5.5, Kimi, and Codex. The AI's role was limited to formalization, error correction, bibliography management, LaTeX editing, critical review, and reviewer-safety calibration. All physical ideas, arguments, and conclusions originate with the author.

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

## AI-Assisted Claim Hardening (May 2026)

After the initial arXiv submission, the author used AI systems for a focused reviewer-safety pass on the manuscript's central chain of reasoning. The author directed the questions, evaluated the responses, and approved the resulting changes.

### Z₂ link-field origin clarification

- AI-assisted review identified the lack of a sufficiently explicit origin for the `Z₂` link field as the main technical vulnerability.
- The author clarified the intended construction: the `Z₂` variable is not added by hand, but is the shared binary bond index already present on `j=1/2` spin-network edges in the tensor-network/intertwiner representation.
- AI-assisted drafting helped integrate this clarification into the manuscript: `sigma_e` is now identified as the shared edge bond index; the local vertex flip gives the usual `Z₂` gauge transformation; and the effective `Z₂` even-parity structure is distinguished from the full `SU(2)` singlet projection.
- The Wilson plaquette action and coupling `K` were reframed as minimal effective dynamics consistent with the emergent gauge structure, not as quantities derived from spin-foam amplitudes.

### Referee-facing calibration

- GPT-5.5 and Kimi were used for independent critical discussion of the manuscript's interpretation of confinement/deconfinement, Wilson loops, and coherent time orientation.
- Codex was used to apply targeted LaTeX edits that distinguish coherent cosmological time orientation from a complete derivation of the thermodynamic arrow of time.
- A gauge-invariant dressed relative-orientation correlator was added to complement the Wilson loop and make the long-distance coherence claim operational.
- The CZX/SPT language was calibrated to present a concrete tensor-network/bond-index correspondence, while preserving the Appendix F caveat that the projected LQG volume-qubit basis and the CZX code-space basis require careful operator-level matching.
- The fermionic matter discussion was calibrated as a conjectural boundary/defect-surface mechanism rather than an established derivation.

---

## What the AI Did Not Do

- Propose the central physical mechanism or hypothesis
- Identify the relevant condensed matter models (CZX, toric code) — these were the author's choices
- Select the research question or the LQG framework
- Generate any figures other than the one noted above
- Write any of the appendices (all pre-existing author work)
- Decide the physical interpretation of the `Z₂` bond index; the author supplied and approved this interpretation

---

## Author Responsibility

The author reviewed all AI-generated content, approved all changes, and takes full scientific responsibility for the manuscript. The AI was used as a writing, review, and formalization tool, functioning in a role analogous to a technically knowledgeable research assistant working under the author's direct supervision.
