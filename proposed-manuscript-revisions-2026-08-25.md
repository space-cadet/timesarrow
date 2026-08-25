# Proposed Manuscript Revisions

**Status:** Proposal for author review only

**Manuscript:** `timesarrow.tex`

**Prepared:** 2026-08-25

## How to Use This Document

This document separates proposed wording from the authoritative manuscript. Each entry contains:

1. the text in the checked-in manuscript before the proposed revision;
2. the proposed replacement;
3. the purpose and claim-level effect of the change.

The governing principle is to preserve the paper's spine: state the effective confinement--deconfinement proposal confidently, while marking the exact boundary between a result within the effective model and a microscopic derivation from LQG.

No proposal in this document should be treated as accepted until approved by the author.

---

## P1. Abstract

### Current checked-in text

> The question of the origin of time's arrow is a major outstanding problem in physics. Here we present a mechanism for the emergence of a coherent cosmological arrow of time from a confinement--deconfinement transition in a $Z_2$ lattice gauge theory living on the spin-network states of Loop Quantum Gravity. Following Chen and Vishwanath, who showed that time-reversal symmetry can be gauged on tensor network states, and using the spin-network/tensor-network correspondence, we identify a $Z_2$ link field on spin networks with the shared binary bond index carried by $j=1/2$ spin-network edges. The effective theory of this gauge field contains a confined phase -- corresponding to a pre-geometric ``quantum gravitational foam'' with no coherent time orientation -- and a deconfined phase -- corresponding to semiclassical spacetime with a uniform, transportable time orientation. In this work, ``arrow of time'' refers primarily to this cosmological time-orientation structure: a prerequisite for, but not by itself a complete derivation of, the thermodynamic arrow. The transition is detected by gauge-invariant non-local observables, in particular Wilson loops and, in finite-temperature lattice treatments, the Polyakov loop. The deconfined phase is argued to realize a gauged CZX-type tensor-network structure, whose topological order provides additional stability of the coherent arrow against local perturbations. We conjecture that protected surface excitations associated with this topological structure may give rise to fermionic matter degrees of freedom.

### Proposed replacement

> The question of how a coherent direction of time can be defined across a quantum spacetime is logically prior to the thermodynamic question of why entropy increases. We propose that this cosmological time orientation is an emergent gauge phenomenon. In a restricted four-valent $j=1/2$ spin-network sector, the binary tensor-network structure and the paired sectors of the signed volume operator motivate an effective $Z_2$ orientation variable on links. Adopting the minimal Wilson action for this variable gives a concrete mechanism: confinement obstructs long-distance comparison of local orientations, whereas deconfinement permits a coherent orientation to be transported across macroscopic distances. This is the central claim of the paper. It is an effective proposal, not a derivation of the $Z_2$ sector or its coupling from spin-foam dynamics, and it does not by itself derive semiclassical geometry or the thermodynamic arrow. Standard Wilson and Polyakov observables characterize the assumed gauge theory; bounded numerical checks reproduce its expected transition region and also show that a tested signed-volume dressing is not a viable phase diagnostic. The CZX model supplies a sharp tensor-network reference construction and a target for future microscopic work, rather than a completed LQG embedding.

### Purpose

Keep the central mechanism prominent while removing four stronger conclusions from the abstract: a completed microscopic link-field identification, automatic emergence of semiclassical spacetime, a completed gauged-CZX realization, and fermionic-matter emergence.

---

## P2. Main proposal in the Introduction

### Current checked-in text

> In this work we build upon these developments to present a mechanism for the origin of a coherent cosmological arrow of time by identifying a $Z_2$ link field representing local time-reversal symmetry on spin networks. We show that the effective theory of this gauge field is a $Z_2$ lattice gauge theory which admits a confinement-deconfinement transition. The confined phase corresponds to a pre-geometric state with no coherent arrow of time, while the deconfined phase corresponds to semiclassical spacetime with a uniform, transportable cosmological arrow. We further conjecture that protected surface excitations associated with the resulting topological structure may give rise to fermionic matter degrees of freedom. This microscopic approach is complemented by prior work which permits a macroscopic, continuum description of the $Z_2$ gauge field as a symmetry which changes the sign of the determinant of the tetrad field.

### Proposed replacement

> In this work we build upon these developments to propose that coherent cosmological time orientation is an emergent gauge phenomenon. We restrict attention to a four-valent $j=1/2$ spin-network sector on a chosen cellular complex and introduce an effective $Z_2$ link variable representing relative local orientation. We then adopt the minimal Wilson action compatible with that gauge structure and study its consequences. Within this effective theory, confinement prevents orientation from being compared coherently over long distances, while deconfinement permits a uniform, transportable cosmological orientation. The proposal is motivated by spin-network kinematics and by the continuum tetrad-orientation discussion; the microscopic derivation of the link field, its action, and its cosmological trajectory remains open.

### Purpose

State the mechanism as the paper's proposal, while distinguishing introduction of an effective field from its microscopic derivation.

---

## P3. Claimed original contributions

### Current checked-in claims

1. A local $Z_2$ link field is identified as the microscopic representation of time reversal in LQG, and its gauge theory is derived.
2. The cosmological arrow is identified with deconfinement, using Wilson loops and the dressed relative-orientation correlator.
3. A concrete CZX--intertwiner correspondence identifies the topological structure of the deconfined phase.
4. The LQG intertwiner qubit and CZX code subspace are identified as corresponding effective qubits.
5. Protected surface excitations are conjectured to produce fermionic matter.

### Proposed replacement

> The original contributions of this work are as follows. (i) We formulate a concrete effective $Z_2$ gauge proposal for coherent time orientation in a restricted spin-network sector and state its microscopic assumptions explicitly. (ii) We identify deconfinement as the phase in which relative orientation can be transported coherently over long distances, with Wilson and Polyakov observables providing the appropriate gauge-invariant diagnostics. (iii) We separate the robust tensor-network motivation from the unresolved microscopic embedding by using CZX as a reference construction and by exhibiting the operator-level obstruction to a literal identification with the $SU(2)$ intertwiner subspace. (iv) We provide bounded numerical controls of the assumed gauge theory and retain the failure of the tested signed-volume dressing as a useful negative result. Together these steps define a falsifiable research programme: derive, modify, or rule out the effective orientation sector from microscopic quantum-gravity dynamics.

### Purpose

Replace five escalating claims with four contributions that the manuscript and numerical evidence directly support.

---

## P4. Signed volume and binary bond structure

### Current checked-in text

> We wish to argue that the local action of time-reversal symmetry on a spin network leads to a change in the sign of the eigenvalues of the LQG volume operator acting in that region. At the kinematical level, the relevant $Z_2$ structure is already present in the binary bond indices of the $j=1/2$ tensor-network representation.

The checked-in discussion then says that the $pm q$ eigenstates correspond to the two possible time orientations and that the bond-level description is the natural home of the emergent field.

### Proposed replacement

> We now isolate the kinematical structure that motivates the effective proposal. Time reversal changes angular momentum, while the signed interior operator in the restricted four-valent sector has paired eigenvalues. Binary bond indices provide a natural language in which to represent a relative orientation variable. These observations motivate, but do not uniquely derive, the $Z_2$ link field; the continuum tetrad description supplies its intended spacetime interpretation.

For the paired eigenstates:

> These states are eigenvectors of the signed interior operator $\hat Q$ with eigenvalues $\pm q$. We interpret this paired sign as the local orientation datum relevant to the proposal. The standard volume operator $\hat V\propto\sqrt{|\hat Q|}$ is degenerate on the pair, so the interpretation depends on retaining the signed operator rather than ordinary volume alone.

For the bond data:

> Shared binary data live on connecting edges. This makes the bond description a natural candidate carrier for the effective $Z_2$ link field. It is not a basis-independent derivation of that field: the even-parity binary constraint is not the full $SU(2)$ Gauss constraint, and the map from bond data to the signed-volume sectors remains part of the required microscopic construction.

### Purpose

Preserve the physical motivation while avoiding an unproved identification among bond bits, the full Gauss constraint, signed volume, and time orientation.

---

## P5. Status of the $j=1/2$ sector

### Current checked-in position

The current discussion treats the $j=1/2$ sector as physically preferred and suggests that higher-spin sectors mainly renormalize the effective coupling without changing the mechanism.

### Proposed position

Describe $j=1/2$ as a controlled truncation selected because:

- it is the minimal nontrivial four-valent intertwiner sector;
- it has a two-dimensional invariant space;
- its signed-volume pair makes the proposed binary structure explicit;
- it permits analytic and numerical control.

Proposed limiting sentence:

> These considerations justify studying the $j=1/2$ sector as a controlled minimal model; they do not establish its dynamical dominance. Higher-spin sectors can introduce additional local states and relevant couplings, and their effect on the proposed orientation theory must be determined by coarse graining rather than assumed to be a renormalization of $K$ alone.

### Purpose

Retain a clean, tractable model without presenting the truncation as a derived feature of the physical regime.

---

## P6. CZX as a reference construction

### Current checked-in text

> In this section we establish the tensor-network correspondence between the CZX model and the spin-network states of Loop Quantum Gravity. This mapping is the bridge which allows us to use the technology of symmetry-protected topological phases in the quantum gravity setting.

The section further treats equality of local dimensions and a proposed GHZ plaquette pattern as establishing the relevant microscopic correspondence.

### Proposed replacement

> In this section we use the CZX model as a reference construction. It displays, in an exactly controlled setting, how a binary symmetry, multipartite entanglement, and a nontrivial boundary action can coexist. These ingredients motivate a possible microscopic realization of the effective orientation sector, but the spin-network state is not assumed to be a literal CZX ground state.

For the dimension comparison:

> A chosen two-dimensional CZX code space can be treated as an effective qubit, while the Gauss constraint selects a two-dimensional $SU(2)$-invariant intertwiner space. Equality of dimensions permits comparison of effective descriptions; it does not identify their projectors, symmetry operators, or many-body phases.

For the missing microscopic construction:

> A genuine spin-network analogue would have to specify which logical partons are owned by each coarse site, which plaquette or cell receives each parton, and how the resulting GHZ structure is mapped into the $SU(2)$-invariant recoupling basis. Those ownership, incidence, and isometry data have not yet been constructed.

### Purpose

Keep CZX as a powerful organizing model while incorporating the explicit Appendix F result that literal $U_{\mathrm{CZX}}$ does not preserve the full intertwiner subspace.

---

## P7. Matter and defect modes

### Current checked-in position

The manuscript conjectures that protected surface excitations of the proposed topological phase may give rise to fermionic matter, supported by CZX boundary behavior, projective time reversal, SPT classification, and related arguments.

### Proposed replacement

Rename the subsection to **Orientation Defects and Matter as an Open Direction** and replace the conclusion with:

> At present this is a question, not a result. The bulk SPT class of the proposed spin-network state has not been established; neither a physical boundary theory nor fermionic statistics has been derived. In particular, the gapless boundary of the two-dimensional CZX reference model does not determine the surface physics of a three-dimensional bosonic $Z_2^{\mathcal T}$ phase, and a projective action with $\mathcal T^2=-1$ is not by itself a derivation of propagating fermionic matter.
>
> A future microscopic theory would have to identify the defect Hilbert space, establish its statistics and dynamics, and recover an appropriate Dirac operator in a semiclassical limit. Orientation defects may provide a useful arena for that programme, but no matter-emergence claim is needed for the effective mechanism developed in this paper.

### Purpose

Prevent the speculative matter thread from competing with the paper's main contribution.

---

## P8. Definition of the effective $Z_2$ field

### Current checked-in text

> We now identify the local $Z_2$ link variable already present on the spin network and analyze its consequences. We will show that the effective theory of this $Z_2$ field is a lattice gauge theory whose phase structure naturally provides a mechanism for the emergence of the cosmological arrow of time.

The current section also states that $\sigma_e$ is not introduced by hand and includes the transformations

$$
\tilde E^a_i(e)\rightarrow\sigma_e\tilde E^a_i(e),
$$

$$
\det({}^3e)\rightarrow\sigma_e\det({}^3e),
$$

and a corresponding regional signed-volume transformation.

### Proposed replacement

> The preceding sections isolate two pieces of structure: binary edge data in the restricted tensor-network description and paired sectors of the signed volume operator. We now turn that kinematical motivation into the central effective proposal of this paper. We introduce a $Z_2$ link field for relative local orientation and adopt its minimal gauge-invariant dynamics. The resulting theory has a sharp physical consequence: only its deconfined phase permits orientation to be compared coherently over macroscopic distances.
>
> The restricted $j=1/2$ sector and chosen cellular complex define the setting; the identification of a binary link field with relative orientation and the Wilson action define the effective model. Neither the field nor its coupling has yet been derived from a spin-foam amplitude. Once these ingredients are adopted, however, the confinement--deconfinement mechanism and its gauge-invariant diagnostics follow.

Retain

$$
\sigma_e\in\{+1,-1\},
$$

and

$$
\sigma_e\rightarrow\tau_v\sigma_e\tau_{v'},
$$

as definitions of the effective link field and gauge redundancy.

Remove the three direct edge-to-continuum transformation equations. Replace them with:

> Reversing an oriented triad leaves the spatial metric unchanged while reversing orientation-sensitive cubic quantities. Likewise, time reversal exchanges the paired signs of the signed interior operator. We therefore read the gauge-invariant organization of $\sigma_e$ as the ability to compare local orientation conventions. This is a proposed effective identification, not an operator identity between a bond bit, the full $SU(2)$ Gauss constraint, and a continuum tetrad.

### Purpose

This is the main technical boundary: the link theory remains definite, but its microscopic encoding is presented as the central derivation target rather than as an accomplished result.

---

## P9. Wilson action and backreaction

### Current checked-in position

The Wilson plaquette action is described as the natural effective action of the field already identified in the spin network. The coupling $K$ is related qualitatively to aligned and anti-aligned neighboring orientations and expected to arise from spin-foam amplitudes.

### Proposed replacement

Retain the action

$$
S_{Z_2}[\sigma]=-K\sum_{p\in\Gamma^*}\prod_{e\in\partial p}\sigma_e,
$$

but introduce it as follows:

> For a $Z_2$ field on the links of a chosen cellular complex, the minimal local gauge-invariant dynamics is the Wilson plaquette action. We adopt this action. Here $K$ is an effective coupling controlling flux suppression. A microscopic completion would have to derive both the action and $K$ from coarse-grained spin-foam amplitudes; no formula equating $K$ with a presently computed LQG amplitude is assumed.

For the geometric factor in the partition function:

> The pure-gauge analysis is the controlled limit in which the geometric factor is taken to be constant. Nontrivial geometric backreaction can shift or alter the phase diagram and belongs to the microscopic extension of the model.

### Purpose

Make the Wilson theory an explicit modeling choice without weakening the consequences derived from it.

---

## P10. Physical meaning of confinement and deconfinement

### Current checked-in text

> The confined phase is the pre-geometric phase: a state of quantum gravitational foam in which smooth spacetime and time orientation do not exist.
>
> The deconfined phase corresponds to our observed semiclassical spacetime, in which cosmological time orientation is uniform.

### Proposed replacement

> **Confined phase:** Wilson loops obey an area law. Large flux fluctuations obstruct transport of a relative orientation convention over macroscopic distances. Within the effective model, coherent cosmological time orientation is therefore absent.
>
> **Deconfined phase:** Wilson loops obey a perimeter law. Large flux sheets are suppressed, so relative orientation can be transported coherently over macroscopic distances. This is the phase required by the proposal for a uniform cosmological time orientation. Identifying it with our semiclassical universe additionally requires a coarse-graining map to geometric observables.

### Purpose

Retain the sharp physical contrast while avoiding the unsupported equivalences “confinement = no geometry” and “deconfinement = observed semiclassical universe.”

---

## P11. Numerical controls

### Proposed new subsection

> **Bounded Numerical Controls.** Our simulations are controls of the adopted gauge model, not simulations of spin-foam dynamics. In the classical three-dimensional runs, the energy-like specific-heat maximum moves from $\beta\simeq0.735$ at $L=8$ to $0.752$, $0.756$, and $0.758$ at $L=16,24,32$, respectively. In the finite-temperature runs, the Polyakov susceptibility peaks in the interval $\beta=0.760$--$0.775$ for $L=8,10,12,16$. These finite-size signals locate the expected transition region and confirm that the code distinguishes the two regimes of the assumed theory. They are not precision critical-exponent estimates and do not validate the proposed LQG identification.
>
> The negative result is equally important. A tested gauge-invariant signed-volume dressing did not produce a stable phase discriminator. We therefore do not use it as evidence for deconfinement and do not claim that the numerical gauge transition already measures a geometric volume transition.

### Purpose

Use the numerical work as genuine evidence at the level it supports, including the negative result.

---

## P12. Cosmological trajectory

### Current checked-in text

The manuscript states that $K$ is small near the Big Bang, that expansion increases $K$, that increasing spin-network size lowers an effective gauge-theory temperature, and that the universe consequently crosses $K_c$ into the deconfined phase.

### Proposed replacement

Rename the subsection **The Cosmological Interpretation and Its Dynamical Bridge** and use:

> If the coarse-grained orientation sector of quantum geometry follows the effective theory above, and if cosmological evolution carries it from confinement into deconfinement, then that transition marks the emergence of a coherent cosmological time orientation. Before the transition, local future--past conventions cannot be compared over long distances; after it, they can.
>
> This statement deliberately separates mechanism from trajectory. The gauge theory supplies the mechanism and its observables. A spin-foam or cosmological calculation must still supply the trajectory: it must derive an effective $K$, show how it depends on coarse-graining or cosmological state, and establish that the physical history crosses the transition in the required direction. Expansion alone does not prove that $K$ grows, and the present paper does not assume a numerical relation between $K_c$ and a Planck temperature, cosmological constant, or epoch.

Proposed closing statement:

> The spine of the proposal is therefore simple and consequential: a cosmological time orientation need not be imposed as an independent global sign; it can arise as long-distance gauge coherence. In the effective model that coherence is created at deconfinement and diagnosed by standard non-local observables. Establishing that our universe followed such a trajectory is the next dynamical problem, not a premise disguised as a result.

### Purpose

Keep the cosmological ambition while removing an uncalculated evolution law for $K$.

---

## P13. Lapse, triads, and spatial spin networks

### Current checked-in position

The discussion says that flipping edge spins is equivalent to reversing the triad, that this reverses local spatial volume, and that the result is equivalent to changing the sign of the lapse.

### Proposed replacement

> The continuum motivation is that reversing an oriented triad changes the sign of its determinant while leaving the metric invariant. The quantum analogue available in the restricted vertex space is the sign of the cubic operator $\hat Q$. This makes $\operatorname{sgn}\hat Q$ a plausible local orientation label, but it does not make an independent sign flip on every spin-network edge identical to a continuum triad inversion.
>
> Nor does a spatial spin network contain the lapse. The relation $\det({}^4e)=N\det({}^3e)$ shows how spatial and temporal orientations combine once a four-dimensional tetrad history is supplied; it does not allow the lapse sign to be reconstructed from one spatial boundary state. The effective $Z_2$ sector should therefore be understood as a proposal for relational orientation data whose spacetime meaning must ultimately be tested in spin-foam histories.

### Purpose

Separate a continuum motivation from a claimed quantum operator equivalence.

---

## P14. Error correction and robustness

### Current checked-in position

The manuscript says that topological order automatically corrects local reversed-orientation errors and explains why macroscopic pockets of reversed time are not observed.

### Proposed replacement

Rename the subsection **Quantum Error Correction and Robust Orientation Transport** and use:

> The relation between deconfined $Z_2$ gauge theory and toric-code topological order provides a useful picture of robustness. In the corresponding quantum Hamiltonian setting, non-local information can be protected against local perturbations while the gap and phase persist. This statement concerns the effective gauge sector; it does not by itself establish that physical cosmological time orientation is a stored logical qubit or that a particular error threshold applies to spacetime.
>
> Translated into the language of the effective model, non-local orientation information is insensitive to sufficiently small local perturbations while the system remains in the deconfined phase. This is a useful robustness mechanism, but it is not yet an explanation of observational bounds on hypothetical regions of reversed time. Such a claim would require the semiclassical map, a defect production rate, and a cosmological history.

### Purpose

Retain the valuable topological-robustness intuition without turning it into an observational conclusion.

---

## P15. Consolidated scope statement

### Proposed new subsection

> **What the Proposal Claims---and What It Does Not.** The claim is that deconfinement supplies a concrete gauge mechanism for long-distance coherence of relative time orientation. It is stronger than an analogy: within the stated effective theory, the relevant phase distinction and non-local observables are fixed. It is narrower than a microscopic derivation: the paper does not derive the $Z_2$ link Hilbert space, the Wilson coupling, or a cosmological flow of $K$ from LQG amplitudes. It also does not derive semiclassical geometry, a low-entropy initial condition, irreversible dynamics, or matter. These are distinct bridges. Keeping them open makes the proposal testable: any microscopic completion must reproduce the effective sector and its phase structure, or explain why the mechanism fails.

### Purpose

Collect the scientific boundaries in one place so that the rest of the paper can speak directly rather than repeating qualifications in every paragraph.

---

## Recommended Author Decisions

The proposals can be reviewed independently rather than accepted as one block:

- **Core spine:** P1--P3, P8--P10, P12, and P15.
- **Microscopic calibration:** P4--P7 and P13.
- **Evidence integration:** P11.
- **Interpretive calibration:** P14.

For each proposal, the author can choose **accept**, **revise**, or **reject**. No manuscript change should be applied until those decisions are recorded.
