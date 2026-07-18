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

## Next Steps

1. **Redo 2D with proper 4-valent vertices** — construct the full intertwiner space (2D per vertex) and test overlap with CZX +1 eigenspace
2. **Clarify the mapping** — how does the vertex-qubit CZX relate to the edge-qubit gauge constraints?
3. **3D hexagonal plaquette** — once 2D is understood, generalize to 3D diamond lattice

## Open Questions

- Is the CZX +1 eigenspace a subspace of the gauge-invariant space, or vice versa?
- Do the CZX constraints and gauge constraints commute?
- What is the physical interpretation of a state that is both CZX-symmetric and gauge-invariant?
- Can this construction be extended to higher spins or different gauge groups?
