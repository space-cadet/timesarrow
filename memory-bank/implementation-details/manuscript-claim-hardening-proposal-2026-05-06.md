# Manuscript Claim-Hardening Proposal
*Created: 2026-05-06 17:26:52 IST*
*Last Updated: 2026-05-06 17:26:52 IST*
*Related Task: T18*

## Purpose
Record the proposed follow-up after a fresh read of `timesarrow.pdf`: build a reviewer-facing technical memo before editing the manuscript. The memo should distinguish derivable claims from conjectures and make the central argument more defensible.

## Starting Point
The manuscript has a strong conceptual spine: local time-reversal twists in tensor networks, spin networks as tensor-network-like states, oriented volume/tetrad sign sectors in LQG, and a `Z_2` confinement-deconfinement mechanism for coherent time orientation.

The current risk is overclaiming. Several links in the argument are plausible but not yet derived at the level a serious reviewer will expect:
- spin-network local time reversal to a dynamical `Z_2` gauge field
- graph/dual-complex structure to plaquette Wilson action
- deconfined `Z_2` phase to cosmological arrow rather than coherent time orientation
- CZX structural correspondence to direct phase identification
- SPT/domain-wall structure to fermionic matter

## Proposed Work Order
1. Create a defensible claims map.
2. Define the exact `Z_2` gauge system: graph, dual complex, plaquettes, gauge transformations, Wilson loops, and allowed observables.
3. Derive or explicitly model the effective plaquette action and coupling `K` from a toy spin-network/spin-foam sector.
4. Repair the CZX argument by preserving the existing structural-correspondence decision and avoiding literal operator claims.
5. Tighten `j = 1/2` and regular-lattice dominance as controlled assumptions or toy-sector restrictions.
6. Reframe the arrow claim as emergence of coherent time orientation unless a thermodynamic-arrow bridge is actually supplied.
7. Reassess the fermion conjecture against the T15 3D SPT survey and separate topological stability from matter emergence where needed.

## High-Priority Technical Gaps
- The effective action in section 8 is currently motivated as the natural `Z_2` lattice gauge action; it should either be derived in a controlled toy model or explicitly labeled as the assumed effective theory.
- Spin networks need a specified cellular/dual complex before plaquettes and Wilson-loop area laws are well-defined.
- The CZX map should be framed as a correspondence of local Hilbert-space structure and `Z_2` effective qubits, not proof that the spin-network state is literally a CZX phase.
- The fermion story is the most fragile because prior memory-bank survey results indicate standard deconfined `3+1d Z_2` gauge theory corresponds to standard toric code/gauged trivial SPT, while the all-fermion surface story belongs to a non-trivial or twisted setting.

## Recommended Next Artifact
A technical memo with this schema:
- Claim
- Current manuscript support
- Gap or reviewer risk
- Repair path
- Proposed replacement wording
- Status: derivable, model assumption, conjecture, or future work

## Boundary
No manuscript edits should be made as part of this proposal step. The first deliverable should be a roadmap or reviewer-response memo that the user can accept, reject, or narrow.
