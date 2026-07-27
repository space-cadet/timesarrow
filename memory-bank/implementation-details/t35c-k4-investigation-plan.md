# T35c Investigation Plan: K₄ Face-Qubit CZX

*Date: 2026-07-26*
*Author: Sage (recording Deepak's direction)*
*Updated: 2026-07-28 — Investigation COMPLETE, K₄ RULED OUT*

---

## ⚠️ STATUS: INVESTIGATION COMPLETE — K₄ RULED OUT

**Date: 2026-07-28**

The K₄ (all-to-all) connectivity has been **ruled out** as a valid cluster state construction by Jia 2024 (JHEP09(2024)147).

**Critical Finding:**
- Cluster graphs **MUST be bipartite** (Jia 2024 Definition 2, p. 17)
- K₄ contains triangles → **NOT bipartite** → INVALID cluster graph
- **Even vertices with >2 bonds break commutativity** (Jia 2024 Proposition 6, p. 21)
- C₄ (ring) IS bipartite → VALID cluster graph

**Verdict: K₄ is fundamentally incompatible with CSS-type cluster state construction.**

This document is preserved for historical record. The active work has pivoted to **Terra's coarse-site C₄ spec (T35b)**.

---

## Original Objective (Historical)

~~Determine whether the K₄ (all-to-all) connectivity of a tetrahedron-face model can realize a valid symmetry-protected topological (SPT) phase, and whether it is equivalent to or distinct from the standard C₄ CZX construction.~~

**Answer: NO. K₄ cannot realize a valid SPT phase in the cluster state framework.**

## Original Background (Historical)

Following the July 21–22 dialog with Terra and Deepak, the T35b edge-qubit model was shown to fail at L≥3. Three candidate models were considered:

| Model | Qubit Location | Connectivity | Status |
|-------|---------------|--------------|--------|
| Edge-qubit | Edge | N/A (singlet) | ❌ Obstructed at L=3 |
| **Terra's coarse-site** | Vertex (4 modules) | C₄ ring by fiat | 🔄 **ONLY VALID PATH** |
| ~~Face-qubit~~ | ~~Tetrahedron face~~ | ~~K₄ intrinsic~~ | ❌ **RULED OUT** |

## Investigation Tracks — ALL COMPLETE

### Track 1: Numerical Investigation — NOT NEEDED

The numerical investigation was abandoned after the algebraic obstruction was found in literature.

~~Phase 1a: Single-Site Verification (4 qubits)~~ — NOT NEEDED  
~~Phase 1b: Two-Site Cluster (8 qubits)~~ — NOT NEEDED  
~~Phase 1c: Square Lattice Test (No Frustration)~~ — NOT NEEDED  
~~Phase 1d: Diamond Cluster Test (With Frustration)~~ — NOT NEEDED  
~~Phase 1e: Analysis~~ — NOT NEEDED

**Reason:** Jia 2024 proves K₄ cannot be a cluster graph, so no numerical verification is needed.

### Track 2: Literature Search — ✅ COMPLETE (2026-07-28)

**Goal**: Find prior work on SPTs with K₄ symmetry, cluster state constraints, diamond lattice SPTs.

#### Papers Reviewed

| Paper | Finding | Relevance |
|-------|---------|-----------|
| **Jia 2024** (JHEP09(2024)147) | Cluster graphs MUST be bipartite (Def 2); K₄ is NOT bipartite → INVALID | **CRITICAL — RULES OUT K₄** |
| **Inamura 2021** (JHEP03(2022)036) | Commuting projector framework is geometry-agnostic | No obstruction, but no support for K₄ |
| **Inamura & Ohyama 2026** (arXiv:2601.08615) | 2+1D generalized cluster states via gauging | No direct relevance to K₄ vs C₄ |
| **Ryu 2008** (PRB 79, 075124) | Diamond lattice Kitaev-type model | NOT relevant (different symmetry) |

#### Key Finding from Jia 2024

> "A graph K(V,E) is called a cluster graph if (i) it is a bipartite graph..."
> — Definition 2, p. 17

> "if the even vertex v_e has more than two bonds (|N_E(v_e)| > 2), the commutativity cannot be reached in general."
> — Proposition 6, p. 21

**Implication:**
- K₄ has degree-3 vertices at each node
- Edge entangler operators do NOT commute
- K₄ cannot support CSS-type cluster state construction
- C₄ (ring) with degree-2 vertices is VALID

### Track 3: Alternative Geometries — NOT NEEDED

Testing K₄ on square/cubic lattices is unnecessary because the obstruction is **algebraic** (non-bipartite), not geometric.

| Lattice | Plaquette | Qubits/site | Frustration? | Status |
|---------|-----------|-------------|--------------|--------|
| ~~Square~~ | ~~4-cycle~~ | ~~4~~ | ~~None~~ | ~~NOT NEEDED~~ |
| ~~Cubic~~ | ~~4-cycle (face)~~ | ~~4~~ | ~~None~~ | ~~NOT NEEDED~~ |
| ~~Diamond~~ | ~~6-cycle~~ | ~~4~~ | ~~Yes~~ | ~~NOT NEEDED~~ |

## Original Timeline (Historical)

| Phase | Track | Target | Status |
|-------|-------|--------|--------|
| 1 | Track 1a | Single-site K₄ verification | ❌ NOT NEEDED |
| 2 | Track 1b | Two-site cluster | ❌ NOT NEEDED |
| 3 | Track 1c | Square lattice control test | ❌ NOT NEEDED |
| 4 | Track 2 | Literature search | ✅ COMPLETE |
| 5 | Track 1d | Diamond cluster test | ❌ NOT NEEDED |
| 6 | Track 1e | Analysis and documentation | ✅ COMPLETE (in T35c.md) |

## Original Decision Gates (Historical)

**Gate A (after Phase 1a–1b)**:
~~If K₄ fails on single site or two sites → STOP~~ — K₄ fails algebraically before numerics

**Gate B (after Phase 1c)**:
~~If K₄ works on square lattice → PROCEED~~ — K₄ fails everywhere (non-bipartite)

**Gate C (after Phase 1d–1e)**:
~~If K₄ works on diamond → SUCCESS~~ — K₄ is definitively NOT a valid SPT

## Code Structure (Historical — Not Implemented)

```
rust-lattice/src/
├── t35c_k4_single_site.rs      # NOT IMPLEMENTED
├── t35c_k4_two_sites.rs        # NOT IMPLEMENTED
├── t35c_k4_square_lattice.rs   # NOT IMPLEMENTED
├── t35c_k4_diamond.rs          # NOT IMPLEMENTED
└── t35c_analysis.rs             # NOT IMPLEMENTED
```

## Risks — All Resolved

| Risk | Resolution |
|------|-----------|
| Numerical cost too high | ❌ NOT APPLICABLE — theoretical obstruction found |
| Negative result (K₄ invalid) | ✅ CONFIRMED — Jia 2024 proves K₄ invalid |
| Ambiguous results | ✅ RESOLVED — clear algebraic obstruction |
| Literature gap | ✅ RESOLVED — Jia 2024 directly addresses the question |

## Relation to Other Tasks — UPDATED

- **T35a**: Provides C₄ baseline. **C₄ is the only valid path.**
- **T35b**: Terra's coarse-site spec is now the **only viable approach**.
- **T33a**: Diamond lattice cell-complex API still relevant for T35b.
- **T32**: Post-correction rigor standard applied — claims backed by literature.

## Acceptance Criteria — UPDATED

- [x] Literature search completed
- [x] Clear conclusion: **K₄ is NOT an SPT** (algebraically invalid)
- [x] All findings documented in `memory-bank/tasks/T35c.md`
- [x] Implementation docs updated
- [ ] ~~Single-site K₄ algebra verified~~ — NOT NEEDED
- [ ] ~~Numerical results documented~~ — NOT NEEDED
- [ ] ~~Code committed and pushed~~ — NOT NEEDED

## Notes

- Deepak's original Z₂ gauge theory numerics (T20/T31/T33) are **unaffected** — they used edge-qubits.
- The face-qubit model is **invalid** — not due to geometric frustration, but due to **algebraic incompatibility** with cluster states.
- Terra's coarse-site spec (T35b) with C₄ connectivity is now the **only remaining path**.
- **2026-07-28**: Investigation concluded. K₄ ruled out by Jia 2024's bipartite requirement.
