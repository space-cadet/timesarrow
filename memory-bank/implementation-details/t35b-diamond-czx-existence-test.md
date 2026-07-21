# T35b: Diamond-Lattice CZX Existence Test

*Created: 2026-07-21 14:56:49 IST*
*Status: 🔄 Specification ready; no construction claim*
*Related task: [T35b](../tasks/T35b.md)*

## Question

Can a CZX-inspired state and global symmetry be defined on a four-valent diamond lattice such that the symmetry preserves the intended $SU(2)$ intertwiner subspace? A positive answer additionally needs a nontriviality test; global invariance alone is not enough.

## Scope and Non-Claims

This task concerns an explicit microscopic construction or obstruction. It does not infer CZX order from Polyakov loops, flux-loop statistics, or a toric-code projector. It also does not assume that a hexagon GHZ product is well-defined when neighboring hexagons share local degrees of freedom.

## Required Specification

Before any numerical search, write down all of the following.

1. **Degrees of freedom:** state whether qubits live on vertices, edges, or vertex--hexagon incidences, and state the physical Hilbert space on a finite cluster.
2. **Incidence map:** identify which local qubit belongs to each hexagon corner and how shared degrees of freedom are identified.
3. **Local convention:** fix a reproducible ordering or branching for the four legs of every tetrahedrally coordinated vertex.
4. **Symmetry:** define a global $\mathbb{Z}_2$ operator and its local factors on that same Hilbert space. Check that the factors define the claimed global action.
5. **Gauge/intertwiner projector:** define $P_{\mathrm{int}}=\prod_v P_v$, with $P_v$ the two-dimensional spin-$1/2$ four-valent singlet projector.

This specification is the first implementation deliverable. Do not write a state-construction or exact-diagonalization script until it is fixed and reviewable.

## Gate 1: Correct Four-Valent Square Test

The current two-valent square-loop result is not a prerequisite result. On a correct four-valent square cluster, construct the vertex/edge map explicitly and calculate

$$
P_{\mathrm{int}} U P_{\mathrm{int}}, \qquad
(1-P_{\mathrm{int}}) U P_{\mathrm{int}}.
$$

Pass condition: the proposed symmetry preserves a nonzero intended intertwiner subspace. Failure condition: report the leakage, the convention used, and whether a different local symmetry could still be tested. Do not advance a literal operator that fails this gate as an intertwiner realization.

## Gate 2: Minimal Periodic Diamond Cluster

Use the T33a connected periodic diamond 2-skeleton and enumerated hexagons. Choose the smallest cluster that realizes the proposed incidence map without duplicate or ambiguous hexagon assignments. For a candidate state $|\Psi\rangle$, test:

$$
\langle\Psi|\Psi\rangle=1, \qquad
U|\Psi\rangle=|\Psi\rangle, \qquad
P_{\mathrm{int}}|\Psi\rangle=|\Psi\rangle.
$$

Also report commutators required by the construction, especially $[U,P_{\mathrm{int}}]$, and any finite-size or boundary conventions. A state that is invariant only in the full qubit Hilbert space does not pass.

## Gate 3: Physical Interpretation

If Gates 1--2 pass, derive candidate local parent terms and test them on the smallest cluster. Separately determine the appropriate three-dimensional SPT classification for the exact protecting symmetry. Only then design the open-boundary test: derive the induced surface symmetry and test whether it is anomalous/non-on-site. The existing 2D boundary MPUO and 3-cocycle calculation are useful preparation but do not by themselves establish a 3D bulk invariant.

## Infrastructure Boundary

T33a currently provides a connected four-valent diamond 2-skeleton with validated hexagonal plaquettes. It does not yet provide diamond 3-cells. That is sufficient for Gates 1--2, but a chosen 3-cell completion and nonempty $d_3$ are required before claims about a closed 3-manifold, 3D homology, or bulk Bianchi structure.

## Evidence Standard and Outcomes

| Outcome | Minimum evidence | Permitted conclusion |
|---|---|---|
| Compatible candidate | Gates 1--2 pass with reproducible conventions | A microscopic candidate exists on the tested finite complex. |
| Partial construction | State and global action defined, but a listed gate remains untested | Construction is incomplete; no SPT claim. |
| Obstruction | Explicit leakage, incompatibility, or inconsistent incidence relation | The tested realization fails; the structural correspondence may remain. |

## Immediate Deliverables

1. A machine-readable finite-cluster incidence specification.
2. A four-valent square-lattice projector/leakage test with exact small-system output.
3. A diamond-cluster construction notebook or script only after the square test passes.
4. A separate classification note for the exact symmetry group before any 3D SPT language is used.
