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

## SPT Phase Equivalence? — **ANSWERED: K₄ is NOT a valid cluster state**

For $\mathbb{Z}_2$ in 2D: $H^3(\mathbb{Z}_2, U(1)) = \mathbb{Z}_2$ — only one nontrivial SPT.

Both operators:
1. Square to identity (generate $\mathbb{Z}_2$)
2. Stabilize the GHZ state
3. Are supported on a 4-qubit site

**Critical Finding from Jia 2024 (JHEP09(2024)147):**
- Cluster graphs **MUST be bipartite** (Definition 2, p. 17)
- K₄ contains triangles → **NOT bipartite** → INVALID cluster graph
- C₄ (ring) IS bipartite → VALID cluster graph
- **Even vertices with >2 bonds break commutativity** (Proposition 6, p. 21)

**Verdict: K₄ and C₄ are NOT in the same SPT phase. K₄ cannot support a CSS-type cluster state construction.**

~~Possibility 1~~: K₄ and C₄ realize the **same SPT phase** — ❌ RULED OUT
~~Possibility 2~~: K₄ realizes a **different phase** — Not applicable; K₄ is not a valid SPT at all

**Test**: ~~Check the boundary 't Hooft anomaly~~ — Not needed; algebraic obstruction found.

## Geometric Frustration on Diamond Lattice — **Moot Point**

The geometric frustration discussion assumes K₄ is a valid starting point. Since K₄ is **algebraically invalid** (not bipartite), the geometric question is moot.

For reference, the original concern was:
- Diamond lattice: each vertex is 4-valent
- Elementary cycles: hexagons (6-cycles)
- **6 hexagons pass through each vertex**
- But only **4 face qubits** exist per vertex
- → Hexagons **must share qubits** at vertices

But this doesn't matter because K₄ cannot be used in the first place.

### Contrast with C₄ Square Lattice

The C₄ model works because:
- Qubits on **vertices** (not faces)
- Each plaquette involves 4 **corner** qubits
- Neighboring plaquettes share **edges**, not corners
- No qubit sharing → projectors commute
- **AND**: The underlying graph (C₄ ring) is **bipartite** ✅

## Three Candidate Models (Summary) — **UPDATED 2026-07-28**

| Model | Qubit Location | CZ Connectivity | Status |
|-------|---------------|-----------------|--------|
| **Edge-qubit** (T35b old) | Edge | N/A (singlet constraints) | ❌ Obstructed at L=3 — **NOW UNDERSTOOD: K₄ incompatibility** |
| **Intertwiner coarse-site** (Terra) | Vertex — 4 modules grouped | C₄ ring by fiat | 🔄 Spec written, Gate 0 open — **ONLY VALID PATH** |
| **Face-qubit** (Deepak's picture) | Tetrahedron face | K₄ intrinsic | ❌ **RULED OUT by Jia 2024** (not bipartite) |

## Investigation Options — **Track 2 COMPLETE, K₄ RULED OUT**

### ~~Option 1: Numerical Test (Empirical)~~ — NOT NEEDED

~~Implement the frustrated Hamiltonian directly~~ → K₄ is algebraically invalid.

### ~~Option 2: Literature Search~~ — ✅ COMPLETE (2026-07-28)

**Key finding:**
- **Jia 2024**: Cluster graphs MUST be bipartite. K₄ is NOT bipartite → INVALID
- **Inamura 2021**: No obstruction, but framework is geometry-agnostic
- **Inamura & Ohyama 2026**: No direct relevance (gauging construction)

**Verdict: K₄ is fundamentally incompatible with cluster state framework.**

### ~~Option 3: Alternative Geometries~~ — NOT NEEDED

~~Test K₄ on lattices where plaquettes don't overlap~~ → K₄ fails everywhere (algebraic, not geometric).

## Conclusion — **UPDATED 2026-07-28**

The K₄ operator is algebraically valid (stabilizes GHZ, generates $\mathbb{Z}_2$) but **it is NOT a valid cluster state** because K₄ is not bipartite (Jia 2024 Definition 2).

**The face-qubit model is invalid. The only remaining path is Terra's coarse-site spec with C₄ connectivity.**

The original question about geometric frustration on the diamond lattice is **moot** — the obstruction is algebraic, not geometric.

---

## Related Files

- `memory-bank/implementation/t35b-encoded-tetrahedral-czx-spec.md` — Terra's coarse-site spec (C₄) — **NOW THE ONLY VALID PATH**
- `memory-bank/implementation/t35b-gate1-results.md` — Edge-qubit negative result
- `memory-bank/implementation-details/t35b-dialog-compilation.md` — Full July 21–22 dialog

## Next Steps

**Abandon K₄. Focus exclusively on Terra's coarse-site C₄ spec (T35b).**

See `memory-bank/tasks/T35c.md` for the full investigation record.
