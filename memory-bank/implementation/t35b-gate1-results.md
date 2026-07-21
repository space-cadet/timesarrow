# T35b Gate 1 Results: Four-Valent Square-Lattice Test

*Date: 2026-07-21*
*Status: Gate 1 complete — intertwiner subspace preserved, but dimensionally small*

## Cluster Specification

- **Lattice:** Periodic $L=2$ square lattice (2×2 torus of vertices)
- **Vertices:** 4 (four-valent)
- **Edges (qubits):** 8
- **Hilbert space dimension:** $2^8 = 256$
- **Intertwiner subspace dimension:** **1**

## Degrees of Freedom

Qubits live on **edges**. Each vertex has 4 incident edges ordered counterclockwise from +x:

```
        e_{+y} (up)
            |
    e_{-x} — v — e_{+x}  (left/right)
            |
        e_{-y} (down)
```

## Intertwiner Projector

At each vertex $v$, the spin-1/2 four-valent singlet projector $P_v$ projects onto the 2-dimensional spin-0 subspace of $(\mathbb{C}^2)^{\otimes 4}$.

**Critical finding:** The vertex projectors $P_v$ do **not commute** when vertices share edges.

| Commutator | Norm |
|---|---|
| $[P_0, P_1]$ | 1.540 |
| $[P_0, P_2]$ | 1.540 |
| $[P_0, P_3]$ | 0.000 |
| $[P_1, P_2]$ | 0.000 |
| $[P_1, P_3]$ | 1.540 |
| $[P_2, P_3]$ | 1.540 |

This means $P_{\text{int}} \neq \prod_v P_v$. The correct global projector is onto the **intersection** of all vertex singlet subspaces, computed iteratively.

## Symmetry Operators Tested

### Candidate 1: $U = X^{\otimes 8} \cdot U_{CZ}$

Where $U_{CZ}$ applies CZ to all pairs of edges in each plaquette.

**Result:**
- $U^2 = I$ ✓
- Leakage: $\|(I - P_{\text{int}}) U P_{\text{int}}\| = 0$ ✓
- Commutator: $\|[U, P_{\text{int}}]\| = 0$ ✓
- Eigenvalue on intertwiner subspace: **+1** ✓

### Candidate 2: $U_X = X^{\otimes 8}$ (no CZ)

**Result:**
- Leakage: 0 ✓
- Commutator: 0 ✓
- Eigenvalue: **+1** ✓

## Interpretation

**Gate 1 passes** for the $L=2$ four-valent square lattice: the proposed symmetry preserves the intertwiner subspace.

However, the **intertwiner subspace is 1-dimensional** for $L=2$. This is unexpectedly small. Possible explanations:

1. The singlet constraint at each vertex is very restrictive when edges are shared.
2. The $L=2$ torus has nontrivial homology that further constrains the gauge-invariant subspace.
3. The edge-qubit model with strict intertwiner projectors may not be the right Hilbert space for the CZX construction.

**Important caveat:** Both $U$ (with CZ) and $U_X$ (without CZ) preserve the intertwiner subspace on $L=2$. The CZ structure is not probed by this test because the subspace is 1-dimensional. Larger clusters ($L=3, 4$) are needed to distinguish these operators.

## Comparison with T35a

T35a used a **plaquette model** where qubits live at plaquette corners (vertices of the dual lattice). The intertwiner structure was different — the CZX operator acted on plaquettes, not on vertex-edge incidence.

This test uses an **edge-qubit model** which is closer to the LQG/spin-network correspondence. The result suggests that a global $X$ operator is sufficient to preserve the intertwiner subspace, but the subspace itself is very small.

## Next Steps

Before proceeding to Gate 2 (diamond lattice), consider:

1. **Larger square lattices ($L=3, 4$):** Does the intertwiner subspace grow? Does the CZ part become necessary?
2. **Different Hilbert space placement:** What if qubits live on vertices instead of edges? Or on vertex-edge incidences?
3. **Relaxed constraints:** Instead of strict singlet projectors, use gauge-invariance constraints (star operators) which are less restrictive.

## Files

- Script: `numerics/scripts/t35b-gate1-square-lattice.py`
- Specification: `memory-bank/implementation/t35b-gate1-specification.md`
