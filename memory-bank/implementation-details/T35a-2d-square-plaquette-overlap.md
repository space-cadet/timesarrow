# T35a: 2D Square Plaquette CZX-Intertwiner Overlap Test

*Created: 2026-07-18*  
*Updated: 2026-07-18*  
*Status: ⚠️ Partial — Toy model complete, correct geometry pending*

## Purpose

Test whether the CZX symmetry on a 2D square plaquette is compatible with the gauge-invariant intertwiner subspace. Specifically: is there a state that is both (a) an eigenvector of the CZX operator with eigenvalue +1, and (b) in the intertwiner (gauge-invariant) subspace where each vertex is in a singlet state?

## Geometry and Setup

### Correct Geometry: 4-Valent Vertices

In a 2D square lattice, each vertex is **4-valent** (4 edges meet). The CZX operator is defined on a **square plaquette** (4 vertices, 4 edges forming a loop).

- **Vertex-qubit picture:** Each vertex has 4 qubits (one per edge). The CZX operator acts on the 4 vertex-qubits.
- **Edge-qubit picture:** Each edge is a qubit shared by 2 vertices. The gauge-invariant state is a tensor product of intertwiners.

The intertwiner space at a 4-valent vertex with spin-1/2 edges is **2-dimensional**.

### What We Actually Tested (Incorrectly)

Due to a conceptual error, the first test used a **2-valent toy model**:
- Each vertex has only 2 edges (not 4)
- Hilbert space: $2^4 = 16$ (4 edge qubits)
- Intertwiner space per vertex: 1-dimensional (only one singlet: $|01\rangle - |10\rangle$ / √2)
- This is NOT the correct geometry for a 2D square lattice

## Scripts and Results

### Script 1: `t35a-square-plaquette.cjs` — CZX Operator Construction

Builds the CZX operator on a square plaquette in the **vertex-qubit picture** (4 qubits, one per vertex):

$$U_{CZX} = X_1 X_2 X_3 X_4 \cdot CZ_{12} CZ_{23} CZ_{34} CZ_{41}$$

- Dimension: 16 ($2^4$)
- Eigenvalues: ±1 (8 each)
- Verified: $U_{CZX}^2 = I$ (identity)

**Result:** ✅ CZX operator correctly constructed and unitary.

### Script 2: `t35a-square-plaquette-intertwiner.cjs` — Gauge-Invariant State

Constructs the gauge-invariant state in the **edge-qubit picture** with **2-valent vertices**:
- Vertices: 4, each with 2 edges
- Gauge-invariant state: $|0101\rangle + |1010\rangle$ / √2
- Tested against plaquette B-operator (product of σz on edges)
- Result: B|ψ⟩ = |ψ⟩ (eigenvalue +1)

**Result:** ⚠️ This is the **toy model** (2-valent), not the correct 4-valent geometry.

### Script 3: `t35a-czx-product-test.cjs` — CZX Eigenvector Analysis

Extracts all 8 CZX +1 eigenvectors and tests whether they are product states.

**CZX +1 eigenvectors (in vertex-qubit picture):**

| Eigenvector | Configuration | Product State? |
|-------------|---------------|----------------|
| 1 | \|0011⟩ - \|1100⟩ | No (entangled) |
| 2 | \|0110⟩ - \|1001⟩ | No (entangled) |
| 3 | \|0111⟩ + \|1000⟩ | No (entangled) |
| 4 | **\|0101⟩ + \|1010⟩** | No (entangled) |
| 5 | \|0100⟩ + \|1011⟩ | No (entangled) |
| 6 | \|0010⟩ + \|1101⟩ | No (entangled) |
| 7 | \|0001⟩ + \|1110⟩ | No (entangled) |
| 8 | \|0000⟩ + \|1111⟩ | No (entangled) |

**Result:** All CZX +1 eigenvectors are **entangled** (not product states). This is expected for a plaquette operator.

### Script 4: `t35a-czx-intertwiner-overlap.cjs` — Overlap Test

Computes the overlap between each CZX +1 eigenvector and the gauge-invariant state from the toy model.

**Result:**

| CZX +1 Eigenvector | Overlap with Gauge-Invariant |
|--------------------|------------------------------|
| \|0011⟩ - \|1100⟩ | 0.000 |
| \|0110⟩ - \|1001⟩ | 0.000 |
| \|0111⟩ + \|1000⟩ | 0.000 |
| **\|0101⟩ + \|1010⟩** | **1.000** ✅ |
| \|0100⟩ + \|1011⟩ | 0.000 |
| \|0010⟩ + \|1101⟩ | 0.000 |
| \|0001⟩ + \|1110⟩ | 0.000 |
| \|0000⟩ + \|1111⟩ | 0.000 |

**Result:** The gauge-invariant state (toy model) **is** a CZX +1 eigenvector. But this is **not physically meaningful** because the geometry is wrong.

## The Critical Error

### What We Did Wrong

The test used **2-valent vertices** (2 edges per vertex) instead of the correct **4-valent vertices** (4 edges per vertex) of a 2D square lattice.

| | Correct 2D Square Lattice | Toy Model (What We Used) |
|---|---------------------------|--------------------------|
| Vertex valence | 4-valent | 2-valent |
| Qubits per vertex | 4 | 2 |
| Intertwiner dimension | 2-dimensional | 1-dimensional |
| Full plaquette Hilbert space | $2^{16} = 65,536$ | $2^4 = 16$ |
| CZX operator | Acts on 4 vertex-qubits | Same (but wrong geometry) |
| Gauge-invariant state | Tensor product of 2D intertwiners | Product of 1D intertwiners |

### Why the Error Happened

The CZX operator is naturally defined in the **vertex-qubit picture** (one qubit per vertex, with CZ between adjacent vertices). But the gauge-invariant (intertwiner) condition is naturally defined in the **edge-qubit picture** (one qubit per edge, with vertices imposing constraints).

The mapping between these two pictures is **non-trivial** for 4-valent vertices. To avoid this complexity, the first test used a simplified edge-qubit picture with 2-valent vertices, which accidentally mapped the problem to a different (easier) geometry.

### What the Toy Model Result Actually Means

In the toy model (2-valent vertices on a square loop):
- The "intertwiner" at each vertex is just the singlet $|01\rangle - |10\rangle$ / √2
- The gauge-invariant state is a product of these singlets on the 4 edges
- This state happens to be a CZX +1 eigenvector in the **vertex-qubit picture**

But in the **correct** geometry (4-valent vertices):
- Each vertex has a 2-dimensional intertwiner space
- The gauge-invariant state is a superposition of many configurations
- The CZX operator acts on vertex-qubits, not edge-qubits
- The relationship is not a simple overlap calculation

## Correct 2D Analysis (Pending)

For the **proper** 2D square lattice with 4-valent vertices:

### Step 1: Define the Hilbert Space
- 4 vertices, each with 4 qubits (one per edge)
- Total Hilbert space: $2^{16} = 65,536$
- But the CZX operator acts on 4 "vertex-qubits" (one per vertex), not 16 edge qubits

### Step 2: Map Between Pictures
The vertex-qubit picture and edge-qubit picture are related by:
- In the vertex-qubit picture, each vertex has 1 qubit (not 4)
- The CZX operator is defined on these 4 vertex-qubits
- But the gauge-invariant condition requires the full 4-qubit state at each vertex to be in the intertwiner subspace

This mapping is **non-trivial** and requires:
- Either: working entirely in the edge-qubit picture and expressing CZX in terms of edge operators
- Or: working in the vertex-qubit picture and defining the gauge constraint appropriately

### Step 3: Key Question
The correct question is:

> In the **vertex-qubit picture** (4 qubits), what is the subspace of states that are **both** (a) CZX +1 eigenvectors and (b) gauge-invariant (in the appropriate sense)?

Or equivalently:

> In the **edge-qubit picture** (16 qubits), what is the subspace of states that are **both** (a) in the intertwiner product space and (b) mapped to CZX +1 eigenvectors under the appropriate mapping?

## 3D Generalization (Blocked)

In 3D (diamond lattice):
- Vertices are 4-valent
- Plaquettes are hexagonal (6 edges, 6 vertices)
- CZX operator: product of X on 6 vertices × CZ on 6 edges
- Full Hilbert space: $2^{24} = 16,777,216$ (6 vertices × 4 qubits each)
- This is computationally tractable but requires the correct 2D analysis first

## Scripts Reference

| Script | Description | Status | Notes |
|--------|-------------|--------|-------|
| `t35a-square-plaquette.cjs` | CZX operator on 4 qubits | ✅ Working | Vertex-qubit picture |
| `t35a-square-plaquette-intertwiner.cjs` | Gauge-invariant state (2-valent) | ⚠️ Toy model | Edge-qubit picture, wrong geometry |
| `t35a-czx-product-test.cjs` | CZX eigenvector analysis | ✅ Working | All +1 eigenvectors are entangled |
| `t35a-czx-intertwiner-overlap.cjs` | Overlap test | ⚠️ Toy model result | Positive overlap, but geometry is wrong |
| `t35a-many-vertex-state.cjs` | Multi-vertex intertwiner (abandoned) | ❌ Abandoned | Wrong approach — CZX is plaquette, not vertex |
| `t35a-many-vertex-state.ts` | TypeScript version (abandoned) | ❌ Abandoned | Same issue |

## Theory Documentation

- `theory/docs/czx-intertwiner-analysis.md` — High-level analysis and question framing
- `theory/docs/index.md` — Theory index
- `theory/pages/dashboard.html` — Theory dashboard (vanilla JS)

## Key Learnings

1. **CZX is a plaquette operator, not a vertex operator.** It must be defined on faces (squares in 2D, hexagons in 3D), not at vertices.
2. **The vertex-qubit and edge-qubit pictures are non-trivially related.** A state that is simple in one picture may be complex in the other.
3. **2-valent toy models are misleading.** The 1-dimensional intertwiner space at a 2-valent vertex is not representative of the 2-dimensional space at a 4-valent vertex.
4. **The gauge-invariant state in the toy model is a CZX +1 eigenvector.** This is a mathematical fact about the toy model, but it does not answer the physical question.

## Next Steps

1. **Clarify the vertex-qubit / edge-qubit mapping.** How does the CZX operator (defined on vertex qubits) relate to the gauge constraint (defined on edge qubits)?
2. **Redo the 2D analysis with correct 4-valent vertices.** The full Hilbert space is $2^{16} = 65,536$, which is manageable.
3. **Test 3D hexagonal plaquette** once the 2D picture is understood.

## Open Questions

- Is the CZX +1 eigenspace a subspace of the gauge-invariant space, or vice versa?
- Do the CZX constraints and gauge constraints commute?
- What is the physical interpretation of a state that is both CZX-symmetric and gauge-invariant?
- Can this construction be extended to higher spins or different gauge groups?
