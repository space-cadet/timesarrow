# CZX-Intertwiner Compatibility Analysis

**Date:** 2026-07-18  
**Task:** T35a  
**Status:** Active — Partial Results (2D toy model complete, correct 2D pending, 3D blocked)

## Question

Can the CZX symmetry (an SPT-protected order) coexist with the gauge-invariant intertwiner subspace (spin-network structure)? In other words: is the CZX +1 eigenspace compatible with the space of states where each 4-valent vertex is in an intertwiner (singlet) state?

## Background

### CZX Symmetry
The CZX operator is defined on a square plaquette (4 vertices, 4 edges) as:

$$U_{CZX} = X_1 X_2 X_3 X_4 \cdot CZ_{12} CZ_{23} CZ_{34} CZ_{41}$$

where $X_i$ is the Pauli-X operator on vertex $i$ and $CZ_{ij}$ is the controlled-Z between adjacent vertices $i$ and $j$.

This is the SPT symmetry of a 2D cluster state. It has:
- 8 eigenvectors with eigenvalue +1
- 8 eigenvectors with eigenvalue -1

### Intertwiner Subspace
In loop quantum gravity / spin-network theory, each vertex is a 4-valent node with 4 incident edges (spin-1/2 representations). The gauge-invariant subspace at each vertex is the **intertwiner space** — the space of states invariant under the gauge group action.

For a 4-valent vertex with spin-1/2 edges, the intertwiner space is **2-dimensional** (the space of singlets formed by pairing the 4 spins). The basis is typically:
- $|I_1\rangle$ = singlet on edges (1,2) × singlet on edges (3,4)
- $|I_2\rangle$ = singlet on edges (1,3) × singlet on edges (2,4)

A gauge-invariant state on the lattice is a tensor product of intertwiners at each vertex, with edge states identified (summed over).

## 2D Square Plaquette Test

### Setup

We tested a **square plaquette** with 4 vertices and 4 edges. Each vertex is 4-valent, but we initially made an error: we used a **2-valent toy model** where each vertex has only 2 edges, making the intertwiner space 1-dimensional.

In the toy model (2-valent vertices):
- Hilbert space: $2^4 = 16$ (4 edge qubits)
- Intertwiner space per vertex: 1D (single singlet state)
- Gauge-invariant state: $|0101\rangle + |1010\rangle$ / √2

### Toy Model Result: POSITIVE ✅

The gauge-invariant state **is** a CZX +1 eigenvector:

| CZX +1 Eigenstate | Overlap with Gauge-Invariant |
|-------------------|------------------------------|
| $\|0011\rangle - \|1100\rangle$ | 0 |
| $\|0110\rangle - \|1001\rangle$ | 0 |
| $\|0111\rangle + \|1000\rangle$ | 0 |
| **$\|0101\rangle + \|1010\rangle$** | **1.000** ✅ |
| $\|0100\rangle + \|1011\rangle$ | 0 |
| $\|0010\rangle + \|1101\rangle$ | 0 |
| $\|0001\rangle + \|1110\rangle$ | 0 |
| $\|0000\rangle + \|1111\rangle$ | 0 |

### Why This Result is Misleading

The toy model used **2-valent vertices**, which is not the correct geometry for a 2D square lattice. In the proper 2D square lattice:
- Each vertex has **4 edges** (4-valent)
- Intertwiner space is **2-dimensional** per vertex
- Full Hilbert space: $2^{16} = 65536$ (16 qubits for 4 vertices with 4 qubits each)

The toy model result is therefore **not directly applicable** to the physical question.

## Correct 2D Analysis (Pending)

For the proper 2D square lattice with 4-valent vertices:

1. **Vertex-qubit picture:** Each vertex has 4 qubits (one per edge). The CZX operator acts on the 4 vertex-qubits of the plaquette.
2. **Edge-qubit picture:** Each edge is a qubit shared by 2 vertices. The gauge-invariant state is a tensor product of intertwiners.
3. **Mapping:** The relationship between the CZX (vertex-qubit) picture and the intertwiner (edge-qubit) picture is non-trivial and requires careful analysis.

The key question: does the CZX +1 eigenspace in the **vertex-qubit picture** map to the gauge-invariant subspace in the **edge-qubit picture**?

## 3D Diamond Lattice (Blocked)

In 3D, the geometry is more complex:
- **Diamond lattice:** Each vertex is 4-valent
- **Hexagonal plaquettes:** Each plaquette has 6 edges and 6 vertices
- **CZX on hexagon:** Product of X on 6 vertices × CZ on 6 edges
- **Full Hilbert space:** $2^{24} = 16,777,216$ (24 qubits for 6 vertices with 4 qubits each)

This is computationally tractable but requires the correct 2D analysis first.

## Scripts and Files

| Script | Description | Status |
|--------|-------------|--------|
| `t35a-square-plaquette.cjs` | CZX operator on 4 qubits (vertex picture) | ✅ Working |
| `t35a-square-plaquette-intertwiner.cjs` | Gauge-invariant state in edge picture (2-valent) | ⚠️ Toy model only |
| `t35a-czx-product-test.cjs` | Product state test for CZX eigenvectors | ✅ Working |
| `t35a-czx-intertwiner-overlap.cjs` | Overlap between CZX +1 and gauge-invariant | ⚠️ Toy model result |
| `t35a-many-vertex-state.cjs` | Multi-vertex intertwiner construction (abandoned) | ❌ Wrong geometry |

## Key Learnings

1. **CZX is a plaquette operator, not a vertex operator** — must be defined on faces, not vertices
2. **The 2-valent toy model is misleading** — the intertwiner structure is fundamentally different for 4-valent vertices
3. **The mapping between vertex-qubit and edge-qubit pictures is non-trivial** — this is the core of the problem
4. **In 2D, the gauge-invariant state is a CZX eigenstate** — but only in the toy model; the full 4-valent case is pending


## Explicit Construction Results (2026-07-18 Session)

### Single Plaquette

The state $|\Psi\rangle_{\rm plaq} = \tfrac{1}{\sqrt2}(|0000\rangle + |1111\rangle)$ is an exact +1 eigenvector of $U_{CZX} = X^{\otimes 4} \prod CZ$:

| Check | Result |
|---|---|
| $\langle\Psi|U_{CZX}|\Psi\rangle$ | $= 1$ |
| $\|U_{CZX}|\Psi\rangle - |\Psi\rangle\|$ | $= 0$ |
| $U_{CZX}^2 = \mathbb{1}$, Hermitian | True |

**Mechanism:**
1. $U_{CZ}$ is diagonal — contributes $(-1)$ only when both neighbors are $|1\rangle$.
   - $|0000\rangle$: phase $(-1)^0 = +1$
   - $|1111\rangle$: all 4 edges active → phase $(-1)^4 = +1$ (even count essential)
2. $U_X = X^{\otimes 4}$ swaps the two GHZ components.
3. Net: $U_{CZX}|\Psi\rangle = |\Psi\rangle$.

### Open Plaquette (Boundary Signature)

With 3 edges (dangling ends), the symmetry is **broken**:
$$U_{CZX}^{\rm open}|\Psi\rangle = \tfrac{1}{\sqrt2}(-|0000\rangle + |1111\rangle) \perp |\Psi\rangle, \qquad \langle\Psi|U|\Psi\rangle = 0$$

The $|1111\rangle$ component gets $(-1)^3 = -1$ vs $+1$ for $|0000\rangle$ — a **relative sign**. This is the single-cell shadow of the non-on-site edge MPUO and the nontrivial 3-cocycle.

### 2×2 Torus (16 Qubits)

**Setup:** qubit $(p,s)$ = spin of site $s$ in plaquette $p$. On the 2×2 torus every plaquette touches all four sites.
$$|\Psi\rangle = \bigotimes_{p=0}^{3}\tfrac{1}{\sqrt2}\big(|0000\rangle_p + |1111\rangle_p\big)$$

**Critical finding:** the symmetry is the **global** operator $U_{CZX} = \prod_s U_{CZX,s}$. A single-site $U_{CZX,s}$ alone does **not** preserve the state.

| Operation | Result |
|---|---|
| Single-site $U_{CZX,s}$ | maps $|\Psi\rangle$ to an **orthogonal** state ($\|U_s|\Psi\rangle - |\Psi\rangle\| = \sqrt2$) |
| Global $\prod_s U_{CZX,s}$ | **invariant** ($\langle\Psi|U|\Psi\rangle = 1$, difference norm $= 0$) |
| Global $U_X$ alone | invariant (flips all 4 corners of each plaquette) |
| Global $U_{CZ}$ alone | invariant (each shared link gets CZ twice — cancels) |

**CZ cancellation mechanism:** Between every two neighboring plaquettes, CZ is applied twice (once at each end of the shared link). Since spins within a plaquette are perfectly correlated, the two CZ's cancel. Only the **dressed global product** is the symmetry — which is exactly what makes the SPT nontrivial: the state looks like a trivial product of plaquettes, but the symmetry cannot be disentangled on-site, and the CZ-pair cancellation fails at boundaries.

### Code

The exact numerical verification is in `numerics/scripts/t35a-czx-construction-verify.py` (numpy, exact state-vector arithmetic).

## Updated Status

- ✅ Single plaquette: explicit construction and verification
- ✅ 2×2 torus: global symmetry verified, single-site obstruction confirmed
- ✅ Boundary signature: open plaquette shows relative sign
- ⬜ Boundary MPUO: cut torus open, extract $\tilde U_{CZX}$, show non-on-site, compute 3-cocycle
- ⬜ Parent Hamiltonian: build commuting terms, verify unique gapped ground state
- ⬜ ts-quantum cross-check: compare gate-by-gate with `src/models/czx.ts`

## Next Steps (Revised)

1. **Boundary MPUO** — cut the torus open, extract effective edge symmetry, show it cannot be factored on-site; compute the 3-cocycle of $H^3(\mathbb{Z}_2, U(1)) = \mathbb{Z}_2$ explicitly.
2. **Parent Hamiltonian** — build local commuting projector terms that stabilize the CZX state; verify unique gapped ground state by exact diagonalization on small lattices.
3. **3D generalization** — once the 2D boundary physics is understood, extend to the diamond lattice (hexagonal plaquettes, 6 vertices).

## Open Questions

- Is the CZX +1 eigenspace a subspace of the gauge-invariant space, or vice versa?
- Do the CZX constraints and gauge constraints commute?
- What is the physical interpretation of a state that is both CZX-symmetric and gauge-invariant?
- Can this construction be extended to higher spins or different gauge groups?
