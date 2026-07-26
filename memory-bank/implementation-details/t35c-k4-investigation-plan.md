# T35c Investigation Plan: K₄ Face-Qubit CZX

*Date: 2026-07-26*
*Author: Sage (recording Deepak's direction)*

---

## Objective

Determine whether the K₄ (all-to-all) connectivity of a tetrahedron-face model can realize a valid symmetry-protected topological (SPT) phase, and whether it is equivalent to or distinct from the standard C₄ CZX construction.

## Background

Following the July 21–22 dialog with Terra and Deepak, the T35b edge-qubit model was shown to fail at L≥3. Three candidate models remain:

| Model | Qubit Location | Connectivity | Status |
|-------|---------------|--------------|--------|
| Edge-qubit | Edge | N/A (singlet) | ❌ Obstructed |
| Terra's coarse-site | Vertex (4 modules) | C₄ ring by fiat | 🔄 Spec written |
| **Face-qubit** (this plan) | Tetrahedron face | K₄ intrinsic | ❓ **Under investigation** |

The face-qubit model places qubits on the 4 faces of each tetrahedron vertex. The intrinsic connectivity is K₄ (all pairs of faces share an edge). This is distinct from Terra's spec, which imposes C₄ connectivity by fiat on grouped intertwiner modules.

## The Core Questions

1. **Algebraic**: Does K₄ stabilize a valid SPT? (Same cohomology class as C₄?)
2. **Geometric**: Can K₄ be realized on the diamond lattice without frustration?
3. **Physical**: If frustration exists, does it destroy the SPT or merely make it non-commuting?

## Investigation Tracks

### Track 1: Numerical Investigation (Option 1)

**Goal**: Implement the K₄ Hamiltonian numerically and check for gap, uniqueness, and symmetry.

#### Phase 1a: Single-Site Verification (4 qubits)
- [ ] Implement K₄ operator: $U_{K_4} = X^{\otimes 4} \prod_{i<j} \text{CZ}_{ij}$
- [ ] Verify: $U_{K_4}^2 = I$
- [ ] Verify: $U_{K_4}|\text{GHZ}\rangle = |\text{GHZ}\rangle$
- [ ] Compute full spectrum (16×16 matrix)
- [ ] Compare eigenvalue distribution with C₄
- [ ] **Deliverable**: `rust-lattice/src/t35c_k4_single_site.rs`

#### Phase 1b: Two-Site Cluster (8 qubits)
- [ ] Two tetrahedra sharing a face/edge
- [ ] Define plaquette projectors $P_p$ for each tetrahedron
- [ ] Test: Do projectors commute? $[P_1, P_2] = 0$?
- [ ] If not commuting: implement full Hamiltonian $H = P_1 + P_2$
- [ ] Lanczos or dense ED on 256×256 matrix
- [ ] **Deliverable**: `rust-lattice/src/t35c_k4_two_sites.rs`

#### Phase 1c: Square Lattice Test (No Frustration)
- [ ] 2×2 square lattice with K₄ on each plaquette
- [ ] Qubits at vertices (4 per plaquette, no sharing)
- [ ] This is the **control test** — should work if K₄ is valid
- [ ] Check: commuting projectors, unique gapped ground state
- [ ] Compare with T35a C₄ results
- [ ] **Deliverable**: `rust-lattice/src/t35c_k4_square_lattice.rs`

#### Phase 1d: Diamond Cluster Test (With Frustration)
- [ ] Small diamond lattice cluster (L=2 or L=3)
- [ ] Face-qubits (4 per vertex)
- [ ] Hexagonal plaquettes (6 qubits each? Or redefined?)
- [ ] Full non-commuting Hamiltonian
- [ ] Lanczos on ~10³–10⁴ dimensional space
- [ ] Check: gap, ground state structure, symmetry
- [ ] **Deliverable**: `rust-lattice/src/t35c_k4_diamond.rs`

#### Phase 1e: Analysis
- [ ] If square lattice works but diamond doesn't → obstruction is geometric
- [ ] If neither works → obstruction is algebraic (K₄ ≠ C₄ as SPT)
- [ ] If both work → K₄ is a valid SPT, possibly in same phase as C₄
- [ ] **Deliverable**: `memory-bank/implementation/t35c-numerical-results.md`

### Track 2: Literature Search (Option 2)

**Goal**: Find prior work on SPTs with K₄ symmetry, diamond lattice SPTs, or related constructions.

#### Search Queries
- [ ] "symmetry protected topological diamond lattice"
- [ ] "tetrahedral symmetry protected topological"
- [ ] "K4 CZ gate" / "complete graph controlled-Z"
- [ ] "non-commuting projector Hamiltonian SPT"
- [ ] "face qubit lattice gauge theory"
- [ ] "SPT bipartite lattice obstruction"
- [ ] "3D Z2 SPT classification"
- [ ] "diamond lattice quantum information"

#### Target Venues
- [ ] arXiv (quant-ph, cond-mat.str-el, hep-th)
- [ ] Physical Review B / Letters
- [ ] Quantum Information & Computation
- [ ] Reviews of Modern Physics (review articles)

#### Key Questions
- [ ] Has anyone constructed an SPT on the diamond lattice?
- [ ] Are there known obstructions for SPTs on bipartite lattices?
- [ ] Is K₄ connectivity studied in quantum information?
- [ ] What is the 3D SPT classification for Z₂ on non-simple lattices?

#### Deliverable
- [ ] `memory-bank/implementation/t35c-literature-review.md`

### Track 3: Alternative Geometries (Rolled into Option 2)

**Goal**: Test whether K₄ works on simpler lattices where frustration is absent.

#### Geometries to Test
| Lattice | Plaquette | Qubits/site | Frustration? | Priority |
|---------|-----------|-------------|--------------|----------|
| **Square** | 4-cycle | 4 | ✅ None | High |
| **Cubic** | 4-cycle (face) | 4 | ✅ None | Medium |
| **Diamond** | 6-cycle | 4 | ❌ Yes | Already in Track 1 |

#### Deliverable
- [ ] Results integrated into Track 1 numerical results

## Timeline

| Phase | Track | Target | Effort |
|-------|-------|--------|--------|
| 1 | Track 1a | Single-site K₄ verification | 1 session |
| 2 | Track 1b | Two-site cluster | 1 session |
| 3 | Track 1c | Square lattice control test | 1–2 sessions |
| 4 | Track 2 | Literature search | Parallel, 1–2 sessions |
| 5 | Track 1d | Diamond cluster test | 2–3 sessions |
| 6 | Track 1e | Analysis and documentation | 1 session |

## Decision Gates

**Gate A (after Phase 1a–1b)**:
- If K₄ fails on single site or two sites → **STOP**. Algebraic obstruction. Document and pivot.
- If K₄ passes → proceed to Gate B.

**Gate B (after Phase 1c)**:
- If K₄ works on square lattice → **PROCEED** to diamond test.
- If K₄ fails on square lattice → **STOP**. K₄ is not a valid SPT. Document.

**Gate C (after Phase 1d–1e)**:
- If K₄ works on diamond → **SUCCESS**. Valid SPT, compare with C₄ phase.
- If K₄ fails on diamond but works on square → **PARTIAL**. Geometric obstruction on diamond only. Document.
- If K₄ fails everywhere → **NEGATIVE RESULT**. K₄ ≠ C₄ as SPT.

## Code Structure

```
rust-lattice/src/
├── t35c_k4_single_site.rs      # Phase 1a
├── t35c_k4_two_sites.rs        # Phase 1b
├── t35c_k4_square_lattice.rs   # Phase 1c
├── t35c_k4_diamond.rs          # Phase 1d
└── t35c_analysis.rs             # Phase 1e (shared utilities)
```

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Numerical cost too high | Medium | Delay | Start with small systems; use Lanczos |
| Negative result (K₄ invalid) | Medium | Disappointment | Document precisely; still valuable |
| Ambiguous results | Medium | Uncertainty | Multiple checks; cross-validate |
| Literature gap (no prior work) | Low | Reinventing wheel | Thorough search; cite if found |

## Relation to Other Tasks

- **T35a**: Provides C₄ baseline for comparison.
- **T35b**: Parallel track. If Terra's coarse-site works, compare phases.
- **T33a**: Diamond lattice cell-complex API (may be needed for Phase 1d).
- **T32**: Post-correction rigor standard applies — no claims without evidence.

## Acceptance Criteria

- [ ] Single-site K₄ algebra verified
- [ ] Numerical results documented with exact parameters
- [ ] Literature search completed (even if no relevant papers found)
- [ ] Clear conclusion: same phase / different phase / not an SPT / obstructed
- [ ] All code committed and pushed
- [ ] Memory bank updated with findings

## Notes

- Deepak's original Z₂ gauge theory numerics (T20/T31/T33) are **unaffected** — they used edge-qubits.
- The face-qubit model is a **new proposal** that needs independent validation.
- Terra's coarse-site spec (T35b) and the face-qubit model (T35c) should be tracked separately.
- If both succeed, a phase-comparison task (T35d?) may be needed.
