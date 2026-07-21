# Encoded Tetrahedral CZX Specification

*Created: 2026-07-22 03:15 IST*  
*Status: Specification — not yet tested*  
*Replaces: T35b Gate 1 (edge-qubit model)*  
*Related: T35a (CZX microscopic construction), T33a (diamond cell-complex API)*

---

## 1. Scope and Non-Claims

This document specifies a **spin-network-compatible CZX construction** where the physical degrees of freedom are intertwiner qubits living at the vertices of a lattice, and the symmetry acts on encoded logical operators. It replaces the failed T35b edge-qubit model.

**What this is:** A testable candidate for an SPT state on a tensor network with SU(2) gauge invariance built in at the virtual level.

**What this is not:** A proof that the CZX SPT order survives in a spin-network setting. That requires passing all hard gates below.

---

## 2. Hilbert Space Structure

### 2.1 Single Vertex (Tetrahedron)

Each vertex $v$ of the lattice is a 4-valent node. Associate a **tetrahedron** to $v$ with four faces labeled by a cyclic order $(1,2,3,4)$ around $v$.

- **Virtual space**: $\mathcal{H}_v^{\text{virt}} = (\mathbb{C}^2)^{\otimes 4}$ — four spin-$\tfrac12$ indices.
- **Physical space**: The $SU(2)$-invariant (intertwiner) subspace:
  $$
  \mathcal{H}_v^{\text{phys}} = \operatorname{Inv}_{SU(2)}\big[ (\mathbb{C}^2)^{\otimes 4} \big] \cong \mathbb{C}^2
  $$
  This is a **single qubit** — the intertwiner qubit.

- **Dimension**: $\dim \mathcal{H}_v^{\text{virt}} = 16$, $\dim \mathcal{H}_v^{\text{phys}} = 2$.

### 2.2 Encoding Map

Fix a basis $\{ |0\rangle_v, |1\rangle_v \}$ for $\mathcal{H}_v^{\text{phys}}$. The **encoding map** is an isometry:

$$
W_v : \mathbb{C}^2 \longrightarrow \mathcal{H}_v^{\text{virt}}, \qquad W_v^\dagger W_v = I_{2}
$$

The projector onto the code space at $v$ is:

$$
P_v = W_v W_v^\dagger, \qquad P_v^2 = P_v = P_v^\dagger, \quad \operatorname{rank}(P_v) = 2
$$

**Note**: The choice of intertwiner basis is a convention. Different choices give different encoded operators. The basis must be fixed and recorded before any test.

### 2.3 Gluing: Edge Singlet Contraction

For an edge $e = (v,w)$ connecting vertices $v$ and $w$, the two tetrahedra share a face. Let the face index at $v$ be $i$ and at $w$ be $j$.

The **gluing tensor** is the $SU(2)$ singlet pairing:

$$
\epsilon_{mn} = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}
$$

**Orientation convention**: Fix an orientation for each edge (e.g., $v \to w$). If the edge is traversed in the opposite direction, use $-\epsilon_{mn}$ (since $\epsilon^T = -\epsilon$). Record all edge orientations explicitly.

The gluing projects the virtual tensor product onto a gauge-invariant subspace. The **full physical Hilbert space** on a lattice with $N_v$ vertices is the subspace of $\bigotimes_v \mathcal{H}_v^{\text{virt}}$ where all edge singlet constraints are satisfied:

$$
\mathcal{H}^{\text{phys}}_{\text{total}} = \Big( \bigotimes_v \mathcal{H}_v^{\text{virt}} \Big) \Big/ \sim_{\text{edges}}
$$

where $\sim_{\text{edges}}$ denotes contraction with $\epsilon$ on every edge.

**Critical distinction**: The edge carries **no independent physical qubit**. The only physical degrees of freedom are the intertwiner qubits at vertices. The virtual legs are contracted away.

---

## 3. Encoded Operators

Given a logical operator $O$ on $\mathbb{C}^2$, its **encoded lift** to $\mathcal{H}_v^{\text{virt}}$ is:

$$
\bar{O}_v = W_v O W_v^\dagger + (I_{16} - P_v)
$$

This acts as $O$ on the code space $\operatorname{im}(P_v)$ and as identity on the orthogonal complement. It is unitary if $O$ is unitary.

### 3.1 Single-Qubit Encoded Operators

For the logical Pauli operators $X, Z$ on $\mathbb{C}^2$:

$$
\bar{X}_v = W_v X W_v^\dagger + (I_{16} - P_v), \qquad
\bar{Z}_v = W_v Z W_v^\dagger + (I_{16} - P_v)
$$

### 3.2 Two-Qubit Encoded Operator

For a logical CZ on $\mathbb{C}^2 \otimes \mathbb{C}^2$, the encoded lift to $\mathcal{H}_v^{\text{virt}} \otimes \mathcal{H}_w^{\text{virt}}$ is:

$$
\overline{\mathrm{CZ}}_{vw} = (W_v \otimes W_w) \, \mathrm{CZ} \, (W_v^\dagger \otimes W_w^\dagger) + (I_{256} - P_v \otimes P_w)
$$

where $\mathrm{CZ} = \operatorname{diag}(1,1,1,-1)$ in the computational basis.

### 3.3 CZX Cell Operator

A **CZX cell** is a set $\mathcal{C} = \{v_1, v_2, v_3, v_4\}$ of four intertwiner qubits arranged in a plaquette (2D) or equivalent local cluster (3D).

The encoded CZX operator on the cell is:

$$
\bar{U}_{\mathcal{C}} = \Big( \prod_{v \in \mathcal{C}} \bar{X}_v \Big) \Big( \prod_{(v,w) \in \partial \mathcal{C}} \overline{\mathrm{CZ}}_{vw} \Big)
$$

where $\partial \mathcal{C}$ denotes the edges of the cell.

**Note**: Code-space preservation at each vertex is automatic by construction. The non-trivial test is whether $\bar{U}_{\mathcal{C}}$ commutes with the **edge singlet constraints** (see Gate B below).

---

## 4. Tensor Network State

### 4.1 Single-Vertex State

A logical single-qubit state $|\psi\rangle \in \mathbb{C}^2$ at vertex $v$ is encoded as:

$$
|\Psi_v\rangle = W_v |\psi\rangle \in \mathcal{H}_v^{\text{virt}}
$$

### 4.2 Product State (No Gluing)

On $N_v$ vertices with no edge gluing:

$$
|\Psi_{\text{prod}}\rangle = \bigotimes_v W_v |\psi_v\rangle = \bigotimes_v |\Psi_v\rangle
$$

### 4.3 Gauge-Invariant Tensor Network State

The **physical state** is obtained by contracting all virtual legs with $\epsilon$:

$$
|\Psi_{\text{phys}}\rangle = \Big( \prod_{e=(v,w)} \epsilon_{m_e n_e} \Big) \bigotimes_v |\Psi_v\rangle
$$

This is a **projected entangled pair state (PEPS)** with bond dimension 2. The state lives in the gauge-invariant subspace by construction.

For a plaquette product state where each $|\psi_v\rangle = |+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$, the physical state is:

$$
|\Psi_{\text{GHZ}}\rangle \propto \text{(contraction of four } W_v |+\rangle \text{ with edge } \epsilon \text{'s)}
$$

This should reduce to the plaquette GHZ state in an appropriate basis.

---

## 5. CZX Cell Geometry

### 5.1 2D Square Lattice (Gate 1 Test)

On a square lattice with vertices at integer coordinates $(i,j)$:

- Each vertex is 4-valent (N, E, S, W faces).
- A **plaquette** at $(i+\tfrac12, j+\tfrac12)$ has four corner vertices: $(i,j), (i+1,j), (i+1,j+1), (i,j+1)$.
- The **CZX cell** $\mathcal{C}$ is exactly these four vertices.
- CZ edges: the four edges of the plaquette.

This is the 2D test case that must pass before any 3D construction.

### 5.2 3D Diamond Lattice (Gate 2 Test)

On the diamond lattice (bipartite, 4-valent):

- Each vertex is a tetrahedron with 4 triangular faces.
- The "plaquettes" are hexagons in the dual lattice.
- A CZX cell must be a set of 4 tetrahedra that are mutually adjacent in a geometrically local pattern.

**Open question**: What is the natural CZX cell on the diamond lattice? Four tetrahedra sharing a common edge? Four tetrahedra around a vertex? The geometry must be specified explicitly before testing.

**T33a provides**: The connected diamond 2-skeleton with validated hexagonal plaquettes. This is sufficient for defining the incidence structure, but the CZX cell geometry requires additional specification.

---

## 6. Hard Gates (Tests)

### Gate A: Intertwiner Basis and Encoding Map

**Requirement**: Fix an explicit orthonormal basis $\{|0\rangle, |1\rangle\}$ for $\operatorname{Inv}_{SU(2)}[(\mathbb{C}^2)^{\otimes 4}]$ and write down $W_v$ as a $16 \times 2$ matrix.

**Why**: The encoded operators depend on this choice. Without an explicit basis, the tests are not reproducible.

**Suggested basis**: Use the recoupling scheme with intermediate angular momenta. For 4 spin-$\tfrac12$, couple legs $(1,2)$ to total $j_{12} \in \{0,1\}$ and legs $(3,4)$ to $j_{34} \in \{0,1\}$. The singlets are the states with total $J=0$:
- $|0\rangle = |j_{12}=0, j_{34}=0; J=0, M=0\rangle$
- $|1\rangle = |j_{12}=1, j_{34}=1; J=0, M=0\rangle$

These are orthonormal and span the intertwiner space.

**Deliverable**: Matrix elements $\langle m_1 m_2 m_3 m_4 | W_v | \alpha \rangle$ for $\alpha \in \{0,1\}$.

---

### Gate B: Locality and Gluing Compatibility

**Requirement**: Verify that $\bar{U}_{\mathcal{C}}$ commutes with the edge singlet constraints.

**Test**: For each edge $e = (v,w)$ shared by two CZX cells (or within one cell), compute:

$$
\big[ \bar{U}_{\mathcal{C}}, \, \epsilon_{m_e n_e} \big] \stackrel{?}{=} 0
$$

on the virtual space. More precisely: after contracting the virtual legs of $v$ and $w$ with $\epsilon$, does the action of $\bar{U}_{\mathcal{C}}$ factor through the contraction?

**Pass condition**: The operator $\bar{U}_{\mathcal{C}}$ descends to a well-defined operator on the gauge-invariant subspace (the physical Hilbert space).

**Fail condition**: $\bar{U}_{\mathcal{C}}$ mixes gauge-invariant states with non-gauge-invariant states. This would mean the CZX symmetry is not compatible with the SU(2) gauge structure.

**Why this matters**: Code-space preservation at each vertex (automatic) is not enough. The gauge-invariant subspace is a proper subspace of the tensor product of individual code spaces. The symmetry must respect the gluing constraints.

---

### Gate C: Global Symmetry on a Small Closed Patch

**Requirement**: On a finite periodic cluster (e.g., $2 \times 2$ torus in 2D, or minimal periodic diamond cluster in 3D), define the global symmetry:

$$
\bar{U}_{\text{global}} = \prod_{\mathcal{C}} \bar{U}_{\mathcal{C}}
$$

and test whether a candidate state $|\Psi\rangle$ is invariant:

$$
\bar{U}_{\text{global}} |\Psi\rangle \stackrel{?}{=} |\Psi\rangle
$$

**State candidate**: The tensor network state where each vertex is in $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$ in the intertwiner basis, with all virtual legs contracted via $\epsilon$.

**Test**: Compute $\langle \Psi | \bar{U}_{\text{global}} | \Psi \rangle$. Pass if $= 1$ (or $|\langle \Psi | \bar{U}_{\text{global}} | \Psi \rangle| = 1$ up to numerical precision).

---

### Gate D: Parent Hamiltonian

**Requirement**: Construct local parent terms $\bar{h}_p$ such that $|\Psi\rangle$ is the unique ground state of $\bar{H} = \sum_p \bar{h}_p$ with a nonzero gap.

**Approach**: If $|\Psi\rangle$ is a product of plaquette GHZ states in the intertwiner basis, the parent Hamiltonian from T35a should lift naturally:

$$
\bar{h}_p = \frac{1}{2}\Big[ (I - \bar{X}_1 \bar{X}_2 \bar{X}_3 \bar{X}_4) + \sum_{\text{edges}} (I - \bar{Z}_i \bar{Z}_j) \Big]
$$

**Tests**:
1. $\bar{H} |\Psi\rangle = 0$
2. Gap $\Delta E > 0$
3. Local terms commute $[\bar{h}_p, \bar{h}_{p'}] = 0$ (frustration-free)

---

### Gate E: Boundary Anomaly / MPUO

**Requirement**: Cut the torus open to a cylinder or slab. Extract the effective boundary symmetry operator. Test whether it is:
- (a) On-site (trivial SPT)
- (b) Non-on-site but can be made on-site with extra ancillas (group cohomology classification)
- (c) Genuinely anomalous (nontrivial SPT)

**Method**: Compute the 3-cocycle (in 2D) or the boundary projective representation. Compare with the known CZX classification.

**Caution**: This gate should only be attempted after Gates A–D pass. Until then, the state is not established as a valid CZX candidate.

---

## 7. Evidence Standard and Permitted Conclusions

| Outcome | Minimum Evidence | Permitted Conclusion |
|---------|------------------|----------------------|
| **Compatible candidate** | Gates A–D pass with explicit basis, explicit cell geometry, and reproducible numerics | A microscopic encoded CZX candidate exists on the tested lattice. |
| **Partial construction** | Gates A–B pass, C or D fails with documented leakage | The construction preserves gauge invariance but may not realize the CZX phase. |
| **Obstruction** | Gate B fails (gluing incompatibility) | The encoded CZX is incompatible with SU(2) singlet gluing on this lattice. |
| **Not yet decided** | Any gate answered with "not computed" | No conclusion permitted. The claim stays tentative. |

---

## 8. Implementation Notes

### 8.1 Numerical Strategy

For Gate A (2D square lattice, $2 \times 2$ torus):
- 4 vertices → 4 intertwiner qubits → physical Hilbert space dimension = $2^4 = 16$ (before gluing)
- After gluing (4 plaquette edges + 2 periodic wrap edges), the gauge-invariant subspace dimension is smaller.
- The virtual space is $16^4 = 65536$-dimensional, but we work in the encoded (physical) space.
- Exact diagonalization is feasible.

For Gate A (3D diamond lattice, minimal cluster):
- Need to determine the minimal periodic cluster from T33a.
- Dimension depends on the number of vertices and the gluing topology.

### 8.2 Code Structure

Suggested Rust implementation:
```
rust-lattice/src/
  t35b_encoded/
    mod.rs           — shared types and W_v
    intertwiner.rs   — explicit basis for Inv[(C^2)^{⊗4}]
    gluing.rs        — ε contraction with orientation
    cell2d.rs        — 2D square lattice CZX cell
    cell3d.rs        — 3D diamond lattice CZX cell (T33a integration)
    gates.rs         — test implementations for Gates A–E
```

### 8.3 Relation to Prior Work

- **T35a**: The original CZX on raw qubits. This spec encodes that construction into intertwiner qubits.
- **T35b (old)**: Edge-qubit model with shared physical qubits — failed at $L=3$ due to over-constraint.
- **T35b (new)**: This spec. The failure of the old model motivated the virtual-leg / encoded-operator approach.
- **T33a**: Provides the diamond lattice 2-skeleton for Gate C (3D).

---

## 9. Open Questions

1. **Intertwiner basis choice**: The recoupling basis $|j_{12}=0, j_{34}=0; J=0\rangle$ vs. $|j_{12}=1, j_{34}=1; J=0\rangle$ is natural for a square, but is it the right basis for the tetrahedral geometry? A tetrahedron has no preferred pairing of faces.

2. **3D CZX cell geometry**: On the diamond lattice, what is the analog of a plaquette? Hexagons have 6 vertices, not 4. A CZX cell needs 4 qubits. Is the cell 4 tetrahedra sharing an edge? Or something else?

3. **Encoded CZ on non-nearest-neighbors**: In the diamond lattice, the natural 4-qubit cell may not have the same edge structure as the square plaquette. The CZ pattern may need to be rederived.

4. **Relation to LQG volume operator**: The intertwiner qubit is formally similar to the LQG shape qubit. Can the volume operator sign be expressed in this basis? This connects to the original Time's Arrow conjecture.

---

## 10. Next Immediate Step

**Write down $W_v$ explicitly** in the recoupling basis and verify numerically that:
1. $W_v^\dagger W_v = I_2$
2. The two basis states are SU(2) invariant
3. They are orthonormal

This is Gate A. Until this is done, no other gate can proceed.
