# T35b Gate 1: Four-Valent Square-Lattice Specification

*Draft: 2026-07-21*
*Status: Specification in progress — not yet a construction claim*

## 1. Degrees of Freedom

**Placement:** Qubits live on **edges** of the square lattice.

**Rationale:** In the LQG/spin-network correspondence, holonomies live on edges and intertwiners live at vertices. The CZX construction must respect this if it is to realize the structural correspondence claimed in T35a.

**Local Hilbert space at vertex v:**
- Four edges meet at each vertex: $e_1, e_2, e_3, e_4$ (ordered counterclockwise).
- Local space: $\mathcal{H}_v = \mathbb{C}^2_{e_1} \otimes \mathbb{C}^2_{e_2} \otimes \mathbb{C}^2_{e_3} \otimes \mathbb{C}^2_{e_4}$
- Dimension: 16.

**Global Hilbert space (finite cluster):**
- $N_V$ vertices, $N_E$ edges.
- For a periodic $L \times L$ square lattice: $N_V = L^2$, $N_E = 2L^2$.
- Each edge is shared by 2 vertices → each edge-qubit appears in exactly 2 local vertex spaces.
- The global space is the tensor product over all edge-qubits: $\mathcal{H} = (\mathbb{C}^2)^{\otimes N_E}$.

## 2. Incidence Map

For a periodic $L \times L$ square lattice with vertices at integer coordinates $(x, y)$:

**Vertices:** $V = \{(x, y) : x, y \in \{0, \dots, L-1\}\}$ (with periodic boundaries).

**Edges:** Two sets:
- Horizontal edges: $E_h = \{((x,y), (x+1,y)) : x, y \in \mathbb{Z}_L\}$
- Vertical edges: $E_v = \{((x,y), (x,y+1)) : x, y \in \mathbb{Z}_L\}$

**Edge-qubit indexing:**
- Each edge $e$ gets a unique index $i(e) \in \{0, \dots, N_E - 1\}$.
- Convention: horizontal edges first, then vertical, row-major order.

**Vertex-edge incidence:**
- For each vertex $v = (x, y)$, the four incident edges (in counterclockwise order starting from +x):
  1. $e_{+x}$: horizontal edge to $(x+1, y)$
  2. $e_{+y}$: vertical edge to $(x, y+1)$
  3. $e_{-x}$: horizontal edge from $(x-1, y)$
  4. $e_{-y}$: vertical edge from $(x, y-1)$

**Shared degrees of freedom:**
- Edge $e = ((x,y), (x+1,y))$ is incident to vertices $v_1 = (x,y)$ and $v_2 = (x+1, y)$.
- The qubit on edge $e$ appears in both $\mathcal{H}_{v_1}$ and $\mathcal{H}_{v_2}$.
- The global state must be consistent: tracing over all but one vertex must give the same reduced density matrix for shared edge-qubits.

## 3. Local Convention: Four-Leg Ordering

At each vertex $v = (x, y)$, the four incident edges are ordered **counterclockwise from +x**:

```
        e_{+y} (up)
            |
    e_{-x} — v — e_{+x}  (left/right)
            |
        e_{-y} (down)
```

**Ordering:** $(e_{+x}, e_{+y}, e_{-x}, e_{-y}) \leftrightarrow (1, 2, 3, 4)$.

This is reproducible and respects the planar embedding. For a periodic torus, the ordering is well-defined at every vertex.

## 4. Intertwiner Projector

At each vertex $v$, the **spin-1/2 four-valent singlet projector** is:

$$P_v = \text{projector onto } \text{Inv}_{SU(2)}\left(\frac{1}{2}^{\otimes 4}\right)$$

The tensor product of four spin-1/2 representations decomposes as:
$$\frac{1}{2} \otimes \frac{1}{2} \otimes \frac{1}{2} \otimes \frac{1}{2} = \mathbf{0} \oplus \mathbf{0} \oplus \mathbf{1} \oplus \mathbf{1} \oplus \mathbf{1} \oplus \mathbf{2}$$

The spin-0 (singlet) subspace is **2-dimensional**.

**Explicit construction of $P_v$:**

The singlet subspace is spanned by two orthogonal states. A standard basis:

$$|s_1\rangle = \frac{1}{\sqrt{2}}(|0011\rangle - |1100\rangle)$$
$$|s_2\rangle = \frac{1}{\sqrt{12}}(2|0101\rangle - 2|1010\rangle - |0011\rangle + |1100\rangle)$$

(using the ordering convention above, and $|0\rangle = |\uparrow\rangle, |1\rangle = |\downarrow\rangle$).

Then:
$$P_v = |s_1\rangle\langle s_1| + |s_2\rangle\langle s_2|$$

**Global intertwiner projector:**
$$P_{\text{int}} = \prod_v P_v$$

This is a projector onto the gauge-invariant subspace where every vertex is in a singlet configuration.

## 5. Symmetry Operator

**Question:** What is the global $\mathbb{Z}_2$ symmetry $U$ on this Hilbert space?

**Candidate (from T35a analogy):**
On the plaquette model, $U_{CZX} = X^{\otimes 4} \cdot \prod_{\text{edges}} CZ$.

For the vertex/edge model, a natural candidate acts on **vertices**:
- At each vertex $v$: apply $X$ to all four incident edge-qubits.
- Apply $CZ$ on pairs of edge-qubits that share a plaquette.

But this needs careful definition because edge-qubits are shared between vertices.

**Alternative candidate:**
The global symmetry is a **product over vertices** of local operators:
$$U = \prod_v U_v$$

where $U_v$ acts on the four edge-qubits incident to $v$.

If $U_v = X^{\otimes 4}$ (flip all four edges), then $U = X^{\otimes N_E}$ (flip all edges globally).

If $U_v = X^{\otimes 4} \cdot CZ_{\text{pairs}}$, the $CZ$ factors may cancel or double on shared edges.

**T35a lesson:** The global operator is a dressed product. Single-vertex operators do not preserve the state.

## 6. Gate 1 Test: Projector / Leakage

For a minimal cluster (e.g., $L=2$ periodic, 4 vertices, 8 edges), compute:

1. **Intertwiner dimension:** $\text{tr}(P_{\text{int}}) = 2^{N_V}$ (each vertex contributes 2 singlet states).
   - For $L=2$: $\text{tr}(P_{\text{int}}) = 2^4 = 16$.

2. **Symmetry action on intertwiner subspace:**
   $$M = P_{\text{int}} \cdot U \cdot P_{\text{int}}$$
   
   - If $U$ preserves the intertwiner subspace: $M = P_{\text{int}} \cdot U \cdot P_{\text{int}}$ is unitary on the 16-dimensional subspace.
   - Compute eigenvalues of $M$ (should be $\pm 1$ if $U^2 = I$).

3. **Leakage:**
   $$L = (I - P_{\text{int}}) \cdot U \cdot P_{\text{int}}$$
   
   - If $L \neq 0$: $U$ leaks out of the intertwiner subspace.
   - Report $\|L\|$ and the leakage pattern.

4. **Commutator:**
   $$[U, P_{\text{int}}] = U P_{\text{int}} - P_{\text{int}} U$$
   
   - If $[U, P_{\text{int}}] = 0$: $U$ preserves the intertwiner subspace exactly.

## 7. Finite-Cluster Specification for Implementation

**Cluster:** $L=2$ periodic square lattice (2×2 torus of vertices).

**Vertices:** $V = \{(0,0), (1,0), (0,1), (1,1)\}$ (with periodic identifications).

**Edges:** 8 edges total.
- Horizontal: $h_0 = ((0,0),(1,0))$, $h_1 = ((1,0),(0,0))$ (periodic), $h_2 = ((0,1),(1,1))$, $h_3 = ((1,1),(0,1))$
- Vertical: $v_0 = ((0,0),(0,1))$, $v_1 = ((0,1),(0,0))$, $v_2 = ((1,0),(1,1))$, $v_3 = ((1,1),(1,0))$

**Qubit indices:**
- Horizontal: $h_0 \to 0$, $h_1 \to 1$, $h_2 \to 2$, $h_3 \to 3$
- Vertical: $v_0 \to 4$, $v_1 \to 5$, $v_2 \to 6$, $v_3 \to 7$

**Vertex-edge map:**
- $v_{00}$: edges $(0, 4, 1, 5)$ — $(+x, +y, -x, -y)$
- $v_{10}$: edges $(1, 6, 0, 7)$ — $(+x, +y, -x, -y)$
- $v_{01}$: edges $(2, 5, 3, 4)$ — $(+x, +y, -x, -y)$
- $v_{11}$: edges $(3, 7, 2, 6)$ — $(+x, +y, -x, -y)$

**Note:** On $L=2$, $+x$ and $-x$ are the same edge (traversed opposite directions), and similarly for $+y$ and $-y$.

This is a **toy model** for the four-valent test. The actual diamond lattice (Gate 2) has hexagonal plaquettes and a more complex incidence map.

## 8. Implementation Notes

- Use numpy for exact arithmetic (sparse matrices acceptable for $P_v$).
- The global projector $P_{\text{int}} = \bigotimes_v P_v$ is a product of commuting projectors (they act on different qubits... wait, no: edge-qubits are shared, so $P_v$ and $P_{v'}$ do not commute in general if they share an edge).
- Actually: $P_v$ acts on the 4 edge-qubits incident to $v$. If two vertices share an edge, their projectors both act on that edge-qubit, so $[P_v, P_{v'}] \neq 0$ in general.
- The correct global projector is the product, but it may not be a projector if the $P_v$ don't commute. Need to verify $P_{\text{int}}^2 = P_{\text{int}}$.
- Alternative: The gauge-invariant subspace is the intersection of the ranges of all $P_v$. This is the subspace where every vertex is in a singlet. The projector onto this intersection is well-defined but may not be simply $\prod_v P_v$.

## 9. Evidence Standard

| Outcome | Condition | Conclusion |
|---|---|---|
| Pass | $[U, P_{\text{int}}] = 0$ and $U$ has eigenvalue +1 on a nonzero subspace | A compatible candidate exists on the tested cluster. |
| Partial | $U$ defined but $[U, P_{\text{int}}] \neq 0$ with computable leakage | Construction is incomplete; try modified $U$. |
| Obstruction | Leakage is total or $U^2 \neq I$ on intertwiner subspace | This realization fails; the structural correspondence may remain. |
