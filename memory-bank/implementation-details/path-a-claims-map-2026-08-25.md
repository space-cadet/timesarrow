# Path A Manuscript Claims Map

*Created: 2026-08-25 14:50:52 IST*
*Related Tasks: T18, T36*
*Status: Approved in principle 2026-08-25 15:05:57 IST; apply with the spine-and-guardrails principle below*

## Purpose

This document fixes the evidential status and permitted wording of the manuscript's central argument. It is the reviewer-safety contract for the Path A revision. Current line references point to `timesarrow.tex` before that revision and may move later.

## Guiding Principle: Preserve the Spine

The claims map is a set of scientific guardrails, not the voice of the paper. The revision must remain confident, purposeful, and recognizably committed to its central proposal. Caution should prevent category errors; it should not dissolve the thesis into a sequence of weak possibilities.

The manuscript should therefore:

- state the effective proposal directly and derive its consequences decisively within the assumed model;
- distinguish the proposal from its missing microscopic derivation once, clearly, rather than repeating defensive caveats in every paragraph;
- concentrate assumptions and limitations in dedicated passages so the main argument remains readable and forceful;
- use “we propose,” “within the effective theory,” and “the model implies” where justified, rather than mechanically replacing every claim with “may,” “might,” or “could”; and
- preserve the paper's central spine: coherent cosmological time orientation can be formulated as an emergent $Z_2$ gauge phenomenon, with deconfinement providing the organizing mechanism for long-distance orientation coherence.

The target tone is **bold proposal, exact boundaries**.

## Classification

- **Established result**: a standard result from the cited literature or an exact statement verified within its stated mathematical scope.
- **Numerical control**: a check that the implementation reproduces expected behavior; it is not evidence for the proposed LQG interpretation.
- **Modeling assumption**: an input adopted to define the effective model, not a result derived from LQG or spin foams.
- **Physical interpretation**: a proposed meaning assigned to the effective model once its assumptions are granted.
- **Conjecture**: a plausible extension without a completed derivation.
- **Open problem**: a missing construction or calculation that the paper must identify explicitly.

## Governing Claim

**Classification:** Modeling assumption plus conditional physical interpretation.

**Permitted central claim:**

> If a suitable spin-network sector admits an effective $Z_2$ variable representing relative local time orientation, and if its leading dynamics is described by a Wilson-type $Z_2$ gauge action, then the confined and deconfined phases provide a candidate mechanism for the absence or presence of long-distance coherent time orientation.

The manuscript may study the consequences and internal consistency of this conditional model. It must not state that the $Z_2$ sector, Wilson coupling, cosmological trajectory, microscopic CZX state, semiclassical geometry, thermodynamic arrow, or fermionic matter has been derived from LQG.

## C1. The $j=1/2$ sector

**Current locations:** Abstract and contributions (`timesarrow.tex:217-219`, `247-251`); volume discussion (`747-765`); $j=1/2$ subsection (`932-946`).

**Classification:** Established kinematics within the restricted sector; modeling assumption for dominance.

**Support:**

- A four-valent vertex with four $j=1/2$ legs has a two-dimensional $SU(2)$-invariant intertwiner space.
- $j=1/2$ supplies the smallest nonzero area eigenvalue in the stated LQG kinematics.
- The signed interior operator has paired eigenvalues in the tested truncations; this is algebraic background only.

**Missing derivation or risk:**

- No spin-foam calculation in this project establishes that $j=1/2$ configurations dominate the relevant state sum.
- T22a is a normalized four-leg $SU(2)$ group average, not an FK/EPRL vertex amplitude and not evidence for $j=1/2$ dominance.
- Treating area as a single-edge thermal energy and deriving a Planck-temperature crossover is an additional model assumption, not an LQG result.
- Higher-spin sectors need not be harmless corrections, and their universality-class effect has not been established.

**Permitted wording:**

> We restrict attention to a four-valent $j=1/2$ sector because it is the smallest nontrivial sector with a two-dimensional intertwiner space. This is a controlled truncation used to formulate the effective proposal; dominance of this sector in spin-foam dynamics is not established here.

**Prohibited wording:**

- “The spin-network partition function is dominated by $j=1/2$.”
- “Higher spins only renormalize $K$ and cannot change the universality class.”
- Any Planck-temperature crossover presented as a derived physical result.

**Revision action:** Replace the dominance argument in `timesarrow.tex:934-946` with the controlled-truncation statement. Remove or quarantine the unsupported thermal calculation and demote black-hole counting and large-spin asymptotics to motivation with explicit limits.

## C2. Regular-lattice and plaquette structure

**Current locations:** CZX/dimensional discussion (`timesarrow.tex:970-972`); Wilson action (`1052-1056`).

**Classification:** Modeling assumption and open problem.

**Support:**

- A cellular complex with edges, faces, and closed loops is sufficient to define the standard $Z_2$ Wilson action and Wilson loops.
- The numerical controls use explicit regular cubic lattices.
- T33a supplies a tested connected diamond 2-skeleton and hexagon enumeration within its bounded implementation scope.

**Missing derivation or risk:**

- No gravitational path-integral argument establishes that cubic, diamond, four-valent, homogeneous, or other regular graphs dominate.
- “Minimizing vertex-valency entropy” and “maximizing homogeneity” are not derived selection principles in the present work.
- Results on the cubic numerical lattice do not automatically transfer to an arbitrary spin network or to the diamond construction.

**Permitted wording:**

> We formulate the effective model on a chosen regular cellular complex so that faces and Wilson loops are unambiguous. Extending the construction to generic spin networks, and deriving which complexes dominate the underlying dynamics, are separate open problems.

**Prohibited wording:**

- “Regular lattices dominate the gravitational path integral.”
- “Graph defects or higher valence cannot change the effective phase structure.”
- Treating cubic-lattice controls as validation of a diamond or generic LQG geometry.

**Revision action:** Replace `timesarrow.tex:972` with an explicit geometry assumption. Define the graph, dual complex, plaquettes, and dimensional convention before writing the effective action.

## C3. The $Z_2$ bond field and signed orientation

**Current locations:** Abstract and contributions (`timesarrow.tex:217-219`, `247-251`); volume section (`710`, `763-765`); link-field section (`1022-1048`).

**Classification:** Established binary and intertwiner kinematics; proposed effective identification; open microscopic derivation.

**Support:**

- A $j=1/2$ representation has a two-valued magnetic basis index, and a fixed four-leg tensor representation has binary leg indices.
- The projected four-leg singlet space is two-dimensional.
- The signed interior operator separates paired orientation sectors in the selected truncation.
- The standard transformation law $sigma_e \mapsto \tau_v\sigma_e\tau_{v'}$ defines a consistent $Z_2$ lattice gauge field once $sigma_e$ is adopted.

**Missing derivation or risk:**

- A binary $SU(2)$ representation index is not by itself a derived, basis-independent physical $Z_2$ gauge field.
- The manuscript has not constructed a map showing that the bond index survives the full $SU(2)$ projection as an independent orientation link variable with the asserted local gauge action.
- Algebraic $\pm q$ pairing does not establish the physical time-reversal operator or its dynamics.
- A sign attached to one edge cannot directly multiply an entire triad or regional determinant without a defined coarse-graining map.

**Permitted wording:**

> Motivated by the binary indices in the restricted tensor-network representation and the paired signed-volume sectors, we propose an effective link variable $\sigma_e\in\{\pm1\}$ for relative orientation. We impose the standard local $Z_2$ transformation law as part of the effective model. A basis-independent derivation from the projected LQG Hilbert space remains open.

**Prohibited wording:**

- “The $Z_2$ link field is already present in LQG and is not added by hand.”
- “The full $SU(2)$ Gauss constraint is the $Z_2$ even-parity constraint.”
- “The signed-volume spectrum proves a physical time-reversal symmetry.”
- Directly identifying an edge sign with the sign of a regional triad determinant as a derived microscopic result.

**Revision action:** Recast `timesarrow.tex:1024-1048` as the definition and motivation of an effective variable. Separate the established intertwiner facts from the proposed orientation interpretation and move the missing operator/coarse-graining construction to Limitations.

## C4. Wilson dynamics and the effective coupling $K$

**Current locations:** Effective-action subsection (`timesarrow.tex:1050-1064`); contributions and AI disclosure (`249`, `1640-1647`).

**Classification:** Established gauge-theory dynamics after adoption; modeling assumption for the spin-network system; microscopic derivation open.

**Support:**

- The plaquette Wilson action is the standard minimal local action for a pure $Z_2$ gauge field on a specified cellular complex.
- Its gauge invariance and confinement--deconfinement phase structure are established properties of that effective model.

**Missing derivation or risk:**

- No spin-foam amplitude, coarse-graining calculation, or integration over geometric degrees of freedom derives the Wilson term or its coefficient.
- Additional allowed effective interactions and coupling to geometry have not been excluded.
- The approximate factorization of $\mathcal Z_{\mathrm{geom}}[\sigma]$ in `timesarrow.tex:1060-1064` is an assumption.

**Permitted wording:**

> We adopt the pure Wilson action as the leading minimal effective model consistent with the proposed $Z_2$ gauge symmetry. The action, the neglect of geometric backreaction, and the value of $K$ are assumptions whose derivation from spin-foam dynamics is left open.

**Prohibited wording:**

- “We show that the effective theory is the $Z_2$ Wilson theory.”
- “The Wilson action follows from the spin-network bond indices.”
- Any value or physical interpretation of $K$ presented as microscopically derived.

**Revision action:** Retain the standard action and its gauge-invariance derivation, but label the action, truncation, and factorization assumptions before the equation.

## C5. Cosmological evolution of $K$

**Current locations:** Cosmological transition (`timesarrow.tex:1097-1117`), especially `1101-1103`; future work (`1174-1177`).

**Classification:** Conjecture and open problem.

**Support:** None from the current LQG or numerical work. The effective gauge model only describes its phases as a function of $K$.

**Missing derivation or risk:**

- No calculation shows that the early universe begins at small $K$, that expansion increases $K$, or that graph growth corresponds to cooling of this effective gauge system.
- No mapping relates $K$ or $K_c$ to cosmological time, temperature, scale factor, or a spin-foam coupling.

**Permitted wording:**

> For the proposal to describe a cosmological transition, the coarse-grained effective trajectory would have to cross the confinement--deconfinement boundary. Determining whether spin-foam dynamics produces such a trajectory, and in which direction, is an open requirement.

**Prohibited wording:**

- “Near the Big Bang $K$ is small.”
- “As the universe expands, $K$ grows.”
- “The transition occurs at a particular cosmological epoch.”

**Revision action:** Replace `timesarrow.tex:1101-1103` with the conditional coarse-graining requirement. Do not assign a cosmological history to $K$.

## C6. Gauge-transition diagnostics and numerical evidence

**Current locations:** Abstract and contributions (`timesarrow.tex:217-219`, `249`); phase structure (`1066-1093`); summary (`1117`).

**Classification:** Established background plus bounded numerical controls and one negative result.

**Support:**

- Wilson area/perimeter laws are standard diagnostics in the assumed pure gauge model.
- T20d finite-size plaquette and selected loop results vary in the established transition region and are consistent with the known continuous transition.
- T31 Polyakov scans provide a gauge-invariant implementation control near the expected region.
- The raw signed-volume observable is gauge-dependent, and the particular tested dressed correlator fails to discriminate phases.

**Missing derivation or risk:**

- The controls do not establish the proposed LQG interpretation, coherent physical orientation, a new critical point, precision exponents, or cosmological emergence.
- Canonical datasets, figures, uncertainty language, doctests, and artifact policy remain under T32.

**Permitted wording:**

> Numerical checks of the assumed pure $Z_2$ model reproduce qualitative finite-size behavior in the established transition region. They validate the implementation as a control, not the microscopic LQG origin or physical time-orientation interpretation. The signed-volume study supplies a negative result for the tested observables.

**Prohibited wording:**

- A new precision determination of $K_c$ or critical exponents.
- First-order behavior, latent heat, phase coexistence, or plaquette-Binder order claims.
- Calling the failed dressed correlator a successful order parameter.
- Treating Polyakov or Wilson data as evidence that LQG orientation orders.

**Revision action:** Remove the dressed correlator from the abstract, contribution list, and positive summary. Integrate only T32-approved T20d/T31 controls and retain the signed-volume failure with its bounded scope.

## C7. CZX and the microscopic spin-network construction

**Current locations:** Abstract (`timesarrow.tex:217-219`); contributions (`249`); CZX/LQG mapping (`902-970`); Appendix F (`1518-1565`).

**Classification:** Established reference-model checks; structural motivation; open microscopic construction.

**Support:**

- T35a reproduces the reference two-dimensional CZX plaquette state, global symmetry on a $2\times2$ torus, boundary obstruction, and a gapped commuting-projector parent Hamiltonian.
- The four-$j=1/2$ leg Hilbert space and the four-qubit CZX site have the same dimension before projection.
- The LQG intertwiner multiplicity space and a chosen CZX code space are both two-dimensional effective spaces.

**Missing derivation or risk:**

- The literal $U_{\mathrm{CZX}}$ operator leaks out of the $SU(2)$ intertwiner subspace.
- A single tetrahedral intertwiner module supplies one logical qubit, not the four owned partons required by a CZX site.
- T35b Gate 0 and Gate A are open: no bounded four-module coarse site, non-overlapping GHZ incidence map, or recoupling isometry has been constructed on the diamond lattice.
- The shared-edge model fails beyond its special small case; the $K_4$ cluster-graph route is ruled out only within its bounded framework.
- No result identifies the spin-network deconfined phase with a gauged CZX phase or fixes the relevant three-dimensional SPT class.

**Permitted wording:**

> CZX is used as a reference tensor-network construction illustrating how a global symmetry, entangled partons, and a boundary obstruction can coexist. The shared low-dimensional structure motivates a possible spin-network realization, but the required microscopic embedding has not been constructed.

**Prohibited wording:**

- “We establish the CZX/intertwiner mapping.”
- “The deconfined spin-network phase is gauged CZX or a toric-code phase because of this mapping.”
- “The CZX ground state supplies the entanglement required for semiclassical geometry.”
- “The $\hat Q$ sign flip corresponds to the on-site $U_{\mathrm{CZX}}$ action.”

**Revision action:** Recast `timesarrow.tex:902-970` as motivation and reference validation. State the operator-leakage result and the missing coarse-site/incidence/isometry gates prominently. Move detailed speculative matching to an outlook or limitations appendix.

## C8. Deconfinement, coherent time orientation, and semiclassical geometry

**Current locations:** Abstract and introduction (`timesarrow.tex:217-219`, `241`, `247-251`); phase interpretation (`1075-1082`); cosmological transition and summary (`1099-1117`).

**Classification:** Established gauge-theory phase distinction; proposed physical interpretation; semiclassical and thermodynamic emergence open.

**Support:**

- In the assumed effective model, deconfinement suppresses large flux sheets and permits long-distance gauge coherence diagnosed by nonlocal observables.
- The manuscript already distinguishes coherent cosmological time orientation from the thermodynamic arrow at `timesarrow.tex:241`.

**Missing derivation or risk:**

- No coarse-graining map shows that gauge coherence becomes a tetrad time orientation in a semiclassical spacetime.
- Deconfinement does not by itself generate smooth geometry, a lapse field, locality, the low-entropy initial condition, entropy growth, or irreversibility.
- The confined phase has not been shown to be pre-geometric foam, and the deconfined phase has not been shown to be our observed universe.

**Permitted wording:**

> Within the effective interpretation, deconfinement is a candidate condition for coherent comparison of local orientation across long distances. Establishing its relation to a semiclassical tetrad geometry or the thermodynamic arrow requires additional dynamics not supplied here.

**Prohibited wording:**

- “The confined phase is pre-geometric quantum foam.”
- “The deconfined phase is semiclassical spacetime or our observed universe.”
- “The confinement transition explains the thermodynamic arrow.”
- “Topological error correction automatically stabilizes the physical arrow of time.”

**Revision action:** Use “candidate mechanism for coherent orientation” consistently. Remove equivalence language and add a dedicated Limitations section separating gauge coherence, semiclassical geometry, and thermodynamic irreversibility.

## C9. Fermionic matter

**Current locations:** Abstract and contributions (`timesarrow.tex:217-219`, `247-251`); edge modes (`974-988`); future work (`1176`).

**Classification:** Speculative outlook and open problem.

**Support:** General analogies exist between topological boundary/defect structure and exotic excitations in other models.

**Missing derivation or risk:**

- The project has not established the spin-network SPT class, a corresponding physical boundary theory, fermionic statistics, a Dirac operator, a semiclassical limit, or four-dimensional propagating matter.
- The two-dimensional CZX boundary does not determine the boundary of a three-dimensional spin-network phase.
- The 3D SPT survey found that the earlier gapless-Dirac analogy is not available for a bosonic $Z_2^{\mathcal T}$ SPT; even an all-fermion surface-order argument would require first establishing the nontrivial bulk class.
- $\mathcal T^2=-1$ or a projective representation alone is not a derivation of physical fermions in this model.

**Permitted wording:**

> Possible matter-like degrees of freedom on orientation defects are an open direction. Their statistics, dynamics, dimensional interpretation, and relation to physical fermions have not been derived.

**Prohibited wording:**

- “Protected surface excitations give rise to fermionic matter.”
- “The model predicts all-fermion toric-code surface order.”
- “The defect modes satisfy the Dirac equation” or “$\mathcal T^2=-1$ proves fermionic matter.”

**Revision action:** Remove fermionic matter from the abstract and original-contributions list. Retain at most one short, explicitly speculative outlook paragraph.

## Manuscript-Wide Required Changes

1. Rewrite the abstract around the conditional effective mechanism.
2. Replace the five current “original contributions” with bounded contributions: definition of the proposal, analysis of its consequences, reference-model checks, numerical controls, and explicit negative results.
3. Add a “Scope, assumptions, and limitations” section before or at the start of the effective-action section.
4. Use “coherent time orientation” rather than “arrow of time” whenever the thermodynamic arrow is not being discussed.
5. Distinguish the standard gauge-theory result from its proposed LQG interpretation in every phase-structure paragraph.
6. Remove claims contradicted by T31, especially positive use of the dressed orientation correlator.
7. Keep numerical claims gated by T32 until canonical artifacts and the validation path are approved.
8. Update the AI disclosure so it does not preserve claims that the Path A revision withdraws.

## Author Approval Record

The author accepted these decisions in principle on 2026-08-25, with the explicit requirement that conservative calibration must not reduce the paper to a claimless or soulless work. The guiding principle above controls their application during revision.

- [x] The paper is a conditional effective proposal, not a microscopic derivation.
- [x] $j=1/2$ and regular geometry are explicit controlled assumptions.
- [x] The $Z_2$ orientation field and Wilson action are model inputs motivated by restricted kinematics.
- [x] No cosmological evolution of $K$ is asserted.
- [x] CZX is a reference model and open microscopic target, not an established LQG phase.
- [x] Deconfinement is interpreted only as a candidate for long-distance orientation coherence.
- [x] T20d/T31 appear only as bounded controls; the signed-volume failure is retained.
- [x] Fermionic matter is removed from the paper's claims and retained, if at all, as a short speculative outlook.

## Next Gate After Approval

T32 must select the canonical numerical artifacts, repair the normal Rust validation path, include doctests, quarantine superseded material, and approve the numerical evidence matrix before numerical results enter `timesarrow.tex`.
