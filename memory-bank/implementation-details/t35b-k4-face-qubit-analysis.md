# T35b/T35c: K₄ vs C₄ On-Site Symmetry Comparison

*Date: 2026-07-26*
*Context: Deepak, Sage discussion following July 21–22 dialog compilation with Terra*

---

## The Core Question

Can the all-to-all connectivity (K₄) of a tetrahedron-face model realize the same on-site symmetry as the ring connectivity (C₄) of the standard CZX construction?

## The Operators

**Standard CZX (C₄ ring):**

$$U_{C_4} = X^{\otimes 4} \cdot \text{CZ}_{12}\text{CZ}_{23}\text{CZ}_{34}\text{CZ}_{41}$$

**Tetrahedron-face (K₄ all-to-all):**

$$U_{K_4} = X^{\otimes 4} \cdot \prod_{i<j} \text{CZ}_{ij} = X^{\otimes 4} \cdot \text{CZ}_{12}\text{CZ}_{13}\text{CZ}_{14}\text{CZ}_{23}\text{CZ}_{24}\text{CZ}_{34}$$

## Algebraic Properties

| Property | C₄ | K₄ |
|----------|-----|-----|
| $U^2$ | $I$ ✅ | $I$ ✅ |
| $U\|\text{GHZ}\rangle$ | $\|\text{GHZ}\rangle$ ✅ | $\|\text{GHZ}\rangle$ ✅ |
| Eigenvalues on basis | $\pm 1$ | $\pm 1$ |
| Support | 4 edges (ring) | 6 edges (complete) |
| Locality | 2-body max | 2-body max |

## Critical Difference: Action on Non-GHZ States

On $|1110\rangle$:
- **C₄**: eigenvalue **+1** (4 adjacent pairs of |11⟩: $(-1)^4 = +1$)
- **K₄**: eigenvalue **−1** (3 pairs of |11⟩ among first 3 qubits: $(-1)^3 = -1$)

The operators differ on the orthogonal complement of the GHZ state.

## SPT Phase Equivalence?

For $\mathbb{Z}_2$ in 2D: $H^3(\mathbb{Z}_2, U(1)) = \mathbb{Z}_2$ — only one nontrivial SPT.

Both operators:
1. Square to identity (generate $\mathbb{Z}_2$)
2. Stabilize the GHZ state
3. Are supported on a 4-qubit site

**Possibility 1**: K₄ and C₄ realize the **same SPT phase** (same cohomology class) despite different on-site representatives.

**Possibility 2**: K₄ realizes a **different phase** (or no SPT at all) due to different edge action.

**Test**: Check the boundary 't Hooft anomaly. If identical, the bulk phases are equivalent.

## Geometric Frustration on Diamond Lattice

For the **face-qubit model** (qubits on tetrahedron faces, 4 per vertex):

- Diamond lattice: each vertex is 4-valent
- Elementary cycles: hexagons (6-cycles)
- **6 hexagons pass through each vertex**
- But only **4 face qubits** exist per vertex
- → Hexagons **must share qubits** at vertices

### Commuting Projector Obstruction

For $H = \sum_p h_p$ with $h_p = I - P_p$ (projector onto +1 eigenspace of $U_p$):

Overlapping plaquettes sharing qubits → $[h_p, h_{p'}] \neq 0$ in general.

**Result**: A commuting projector parent Hamiltonian appears **geometrically obstructed** for the face-qubit model on the diamond lattice with hexagonal plaquettes.

### Contrast with C₄ Square Lattice

The C₄ model works because:
- Qubits on **vertices** (not faces)
- Each plaquette involves 4 **corner** qubits
- Neighboring plaquettes share **edges**, not corners
- No qubit sharing → projectors commute

The diamond lattice with face-qubits breaks this pattern.

## Three Candidate Models (Summary)

| Model | Qubit Location | CZ Connectivity | Status |
|-------|---------------|-----------------|--------|
| **Edge-qubit** (T35b old) | Edge | N/A (singlet constraints) | ❌ Obstructed at L=3 |
| **Intertwiner coarse-site** (Terra) | Vertex — 4 modules grouped | C₄ ring by fiat | 🔄 Spec written, Gate 0 open |
| **Face-qubit** (Deepak's picture) | Tetrahedron face | K₄ intrinsic | ❓ Geometric frustration; needs investigation |

## Investigation Options

### Option 1: Numerical Test (Empirical)

Implement the frustrated Hamiltonian directly:

$$H = \sum_p (I - P_p) \quad \text{(non-commuting terms)}$$

Run Lanczos on L=2, L=3 clusters. Check:
- Does a gap exist?
- Is the ground state unique?
- Does it have the right symmetry?
- Phase transition as function of parameter?

**Pros**: Definitive answer.
**Cons**: Expensive; might be negative.

### Option 2: Literature Search

Search for:
- SPTs on diamond lattice
- Tetrahedral symmetry protected topological phases
- K₄ vs C₄ in quantum information
- Non-commuting projector Hamiltonians

**Known**: Diamond lattice is bipartite. Bipartite lattices often have SPT obstructions due to symmetry fractionalization constraints.

**Unknown**: Whether any SPT exists on diamond with face degrees of freedom.

### Option 3: Alternative Geometries

Test K₄ on lattices where plaquettes don't overlap:
- **Square lattice**: 4-cycles, no frustration
- **Cubic lattice**: 4-cycles (faces), no frustration
- **Coarse-grained diamond**: Define non-overlapping super-plaquettes

## Conclusion

The K₄ operator is algebraically valid (stabilizes GHZ, generates $\mathbb{Z}_2$) but its lattice realization on the diamond lattice with face-qubits faces **geometric frustration**. Whether this frustration destroys the SPT or merely makes it non-commuting is the open question.

The face-qubit model and Terra's coarse-site model are **distinct physical constructions** that should be investigated separately.

---

## Related Files

- `memory-bank/implementation/t35b-encoded-tetrahedral-czx-spec.md` — Terra's coarse-site spec
- `memory-bank/implementation/t35b-gate1-results.md` — Edge-qubit negative result
- `memory-bank/implementation-details/t35b-dialog-compilation.md` — Full July 21–22 dialog

## Next Steps

See `memory-bank/implementation-details/t35c-k4-investigation-plan.md` for the investigation plan.
