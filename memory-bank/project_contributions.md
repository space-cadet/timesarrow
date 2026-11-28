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
- **Qualification (2026-11-26):** the first principle above no longer holds without exception. The author has accepted that AI-originated analysis now contributes to the physics claims; see "AI Contributions to the Physics Claims" below.

---

## For Future Reference (AI Disclosure)

If journal disclosure of AI assistance is required, the scope is: manuscript editing, bibliography management, LaTeX typesetting, and formalization of author-provided physics arguments. Through August 2026, the AI did not originate physical claims or perform novel calculations independently. From November 2026 this is no longer true: see the next section, which any disclosure must reflect for items adopted into the manuscript.

---

## AI Contributions to the Physics Claims (November 2026)

*Recorded: 2026-11-26, at the author's request.*

### Which AI system

- **This session (2026-11-26):** a Claude Code cloud session, https://claude.ai/code/session_01CWn2ur3JafUyRYvG8QKQYC. Model and effort level: **[to be entered by the author]**.
- This is a **different AI system** from the one used for the preceding AI-assisted work. According to the author, the earlier work was done with GPT; see the AI assistance statement for the systems named for April–May 2026. Contributions in this section must not be attributed to those earlier systems, and earlier contributions must not be attributed to this one.

### What remains the author's

The following is explicitly the author's, and none of it is claimed here:
- The Chen–Vishwanath gauging of local time reversal on the spin-network tensor network as the origin of the $Z_2$ field. This has been in the manuscript since v1 (abstract and §9.1) and dates to the 2016–2018 draft.
- The sign of the signed volume operator $\hat Q$ as the local time-orientation datum (§6).
- The framing that the local orientation is a degree of freedom already present in the system but overlooked until now.

### AI-originated contributions

None of these has been applied to the manuscript yet. Each needs the author's decision before it enters v2.

1. **$Z_2$ gauge–Higgs extension: the $J$ term.** *Accepted by the author as an AI addition.*
   - **The coupling:** treat the orientation labels $\tau_v$ (e.g. $\tau_v = \operatorname{sgn}\hat Q_v$) as dynamical, and couple them to the connection through the minimal gauge-invariant term, giving $S = -K\sum_p\prod_{e\in\partial p}\sigma_e - J\sum_{e=(vv')}\tau_v\sigma_e\tau_{v'}$.
   - **Phase-diagram consequences** (from the literature): Fradkin–Shenker, i.e. the confined and Higgs regimes are one connected phase, and only the deconfined phase is sharply separated. This supports identifying coherent time orientation with deconfinement specifically.
   - **Diagnostics:** for $J>0$ the Wilson loop no longer discriminates phases (string breaking), so the Fredenhagen–Marcu order parameter is the sharp test.
   - **Sources:** values taken from Tupitsyn, Kitaev, Prokof'ev & Stamp, PRB 82, 085114 (2010), and Somoza, Serna & Nahum, PRX 11, 041008 (2021), and checked against those papers.
   - **Status:** proposal only; there are no $J>0$ simulations.
2. **The bond-index flip does not reverse orientation.**
   - **The calculation:** on a 4-valent $j=1/2$ vertex, $\sigma_x^{\otimes4}$ acts as the identity on the two-dimensional singlet space and commutes with $\hat Q$, because $\sigma_x$ is an $SU(2)$ element up to a phase. The antiunitary time reversal $T=\sigma_y^{\otimes4}K$ does satisfy $T\hat Q T^{-1}=-\hat Q$, with eigenvalues $\pm0.433$ in units where $\hat J=\sigma/2$.
   - **Consequence:** the May 2026 identification of $\sigma_e$ with the shared bond index, with the vertex gauge transformation acting by flipping bond indices (`timesarrow.tex` line 1028 as of 2026-11-26; line 1057 after the 2026-11-27 merge), fails as written. The author's original Chen–Vishwanath construction does not have this problem.
   - **Cross-check (2026-11-28):** the eigenvalues $\pm\sqrt3/4$ and the antiunitary exchange $\Theta|\pm\rangle=|\mp\rangle$ agree with the independently derived new Appendix F (Sol 6.1 Medium, 2026-11-27). The bond-flip result itself is not in Appendix F.
3. **Dimension and universality correction.**
   - A quantum $Z_2$ gauge theory on 3D spatial slices corresponds to a 4D classical lattice. There the pure-gauge transition is first order, at $K_c=\tfrac12\ln(1+\sqrt2)\approx0.4407$ (Creutz, Jacobs & Rebbi 1979), not Ising.
   - The 3D classical theory is dual to the 3D Ising model, not the 2D one.
   - This corrects the universality footnote in §9, and also the April 2026 AI change recorded under T12 ("first order" → "second order").
   - The T20d/T31 numerics are 3D classical, i.e. the (2+1)D model.
4. **The T31 "dressed correlator" is a Wilson-loop average.**
   - In `rust-lattice/src/lib.rs`, the site labels $s(r)$ are themselves link products from the origin. So $C(r_1,r_2)=s(r_1)W(r_1\to r_2)s(r_2)$ is the product of $\sigma$ around a closed loop.
   - The observable is therefore an average of large Wilson loops, suppressed in both phases. It does not test an independent orientation variable.
   - The code comment claiming $C\approx+1$ in the deconfined phase neglects perimeter-law decay.

### Supporting (non-physics) work in the same session

- An audit of the arXiv v1 → current manuscript diff against the Path A claims map.
- Two figures: (a) peak locations from the T20d/T31 data versus $1/L$; (b) a literature schematic of the gauge–Higgs phase diagram, static and interactive. They are not yet committed to the repository.
- Removal of the OpenClaw template files (commit `72ebbf6`).

---

## Single-node derivation and presentation — November 2026

Deepak Vaid proposed the connection to a string worldsheet, recalled the spinor-polynomial construction, selected a common basis, reviewed exact replacements one passage at a time, requested the exchange-operator explanation and named AI credit, authorized implementation, and required the complete calculation in the manuscript itself.

Sol 6.1 Medium assembled the pedagogical calculation from established identities, performed explicit algebraic checks, identified the bare coefficient and constraint-count errors, and drafted the approved passages. The pair-Casimir commutator is credited to Brunnemann–Thiemann, and the spin-exchange identity is standard. New or substantively revised manuscript text carries visible model-named markers. The shared Appendix F derivation and `ai-assistance-statement.md` record these contributions. Scientific responsibility remains with the author.

[Session](sessions/2026-11-27-intertwiner-orientation.md).
