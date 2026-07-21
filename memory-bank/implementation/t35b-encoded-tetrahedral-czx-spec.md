# Encoded Tetrahedral CZX Specification

*Created: 2026-07-22 03:15 IST*
*Last Updated: 2026-07-22 03:27:10 IST*
*Status: Specification — not yet tested*
*Replaces: T35b Gate 1 (edge-qubit model)*
*Related: T35a (CZX microscopic construction), T33a (diamond cell-complex API)*

---

## 1. Scope and Non-Claims

This document specifies the kinematics required for a **candidate encoded CZX construction** with spin-network intertwiners. It replaces the failed shared-edge-qubit model, but does not yet define a CZX phase on the diamond lattice.

**What this is:** A testable tensor-network candidate with $SU(2)$ gauge invariance built into its local intertwiner tensors.

**What this is not:** A proof that CZX SPT order survives in a spin-network setting. In particular, one intertwiner qubit per lattice vertex is insufficient to reproduce the four distinct partons at a CZX site; the coarse CZX site and its incidence map must be defined below before any symmetry claim.

---

## 2. Hilbert Space Structure

### 2.1 Single Vertex (Tetrahedron)

Each vertex $v$ of the lattice is a 4-valent node. Associate a **tetrahedron** to $v$ with four faces labelled $(1,2,3,4)$. A cyclic order is additional framing data, not intrinsic tetrahedral data, and must be fixed consistently before defining any CZX ring.

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

The pairing is a **tensor contraction**, not a projector or an additional Hilbert-space constraint. In the fixed-spin-$\tfrac12$ truncation, the physical multiplicity space is

$$
\mathcal{H}_{\mathrm{int}}=\bigotimes_v
\operatorname{Inv}_{SU(2)}[(\mathbb{C}^2)^{\otimes4}]
\cong(\mathbb{C}^2)^{\otimes N_v}.
$$

The $\epsilon$ tensors supply spin-network amplitudes between these local intertwiner labels. If link holonomies or unfixed representation labels are intended as physical degrees of freedom, they must be added explicitly; this specification does not include them.

**Critical distinction**: the virtual half-edge indices are contracted in a tensor network. They are not identified as one shared edge qubit and they do not reduce $\mathcal{H}_{\mathrm{int}}$ by a further singlet constraint.

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

### 3.3 Coarse CZX Site

A literal CZX site has **four distinct qubits that it owns**. Therefore a coarse site $s$ in this candidate must contain four independent intertwiner modules, labelled $r\in\{1,2,3,4\}$:

$$
\mathcal H_s=\bigotimes_{r=1}^{4}\mathcal I_{s,r},\qquad
\mathcal I_{s,r}\cong\operatorname{Inv}_{SU(2)}[(\mathbb C^2)^{\otimes4}].
$$

Each module has its own encoding $W_{s,r}$. A single tetrahedron provides one such module, not the complete four-qubit CZX site. The construction must therefore specify a local four-tetrahedron block or another local four-mode realization before it is implemented.

### 3.4 Encoded On-Site CZX Operator

With a fixed cyclic order of the four **internal** labels $r$, define

$$
\bar U_s=
\left(\prod_{r=1}^{4}\bar X_{s,r}\right)
\overline{\mathrm{CZ}}_{(s,1)(s,2)}
\overline{\mathrm{CZ}}_{(s,2)(s,3)}
\overline{\mathrm{CZ}}_{(s,3)(s,4)}
\overline{\mathrm{CZ}}_{(s,4)(s,1)}.
$$

Different sites have disjoint logical support, so $\bar U_{\mathrm{global}}=\prod_s\bar U_s$ is an unambiguous on-site $\mathbb Z_2$ candidate. Four neighbouring lattice vertices must **not** be substituted for these four internal qubits: overlapping plaquette operators would not reproduce the CZX symmetry.

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

### 4.3 Spin-Network Amplitude

Contraction must retain the logical basis kets. For a graph with one virtual leg $m_{ve}$ at each end of edge $e=(v,w)$, the tensor network defines

$$
|\Phi\rangle=\sum_{\{\alpha_v\}}
\left[\sum_{\{m_{ve}\}}
\prod_v W^{\alpha_v}_{\{m_{ve}\}}
\prod_{e=(v,w)}\epsilon_{m_{ve}m_{we}}
\right]|\{\alpha_v\}\rangle .
$$

The bracket is an amplitude in $\mathcal H_{\mathrm{int}}$, not a state obtained by quotienting the virtual space. It must be evaluated explicitly on the finite test cluster.

### 4.4 Encoded CZX State

The CZX fixed-point candidate is defined independently on the logical partons. For every coarse plaquette $p$ with corner sites $s_1,\ldots,s_4$, choose one distinct internal label $r_i(p)$ at each corner and set

$$
|\Psi_{\mathrm{CZX}}\rangle=
\bigotimes_p\frac{|0000\rangle_{p}+|1111\rangle_{p}}{\sqrt2}.
$$

The site--plaquette incidence map $r_i(p)$ must use each internal parton once. The spin-network amplitude may decorate this state, but it does not automatically turn a logical $|+\rangle$ product into a GHZ product.

---

## 5. CZX Cell Geometry

### 5.1 2D Square Lattice (Reference Test)

On a square lattice with vertices at integer coordinates $(i,j)$:

- Each coarse site has four internal intertwiner qubits, one for each adjacent plaquette.
- A plaquette at $(i+\tfrac12,j+\tfrac12)$ selects one different internal qubit from each of its four corner sites for its GHZ factor.
- $\bar U_s$ acts only on the four internal qubits owned by site $s$, with its CZ ring internal to the site.

This matches the CZX ownership structure. It is not equivalent to applying a four-qubit operator to the four shared corner qubits of every plaquette.

### 5.2 3D Diamond Lattice (Gate 2 Test)

On the diamond lattice (bipartite, 4-valent):

- Each four-valent vertex supplies one tetrahedral intertwiner module.
- T33a supplies hexagonal 2-cells, not a preferred four-parton CZX site or a square CZX cell.
- A diamond construction must first define a bounded coarse site containing four modules and a local incidence map between those partons and the chosen GHZ cells.

**Open question**: Which coarse block and which cellulation preserve locality while supplying four owned partons per CZX site? Four tetrahedra sharing an edge or an arbitrary four-vertex cluster is not a CZX site until this ownership and incidence data are given.

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

### Gate B: Coarse-Site Incidence and Local Symmetry

**Requirement**: Define the four owned partons at every coarse CZX site, the site--plaquette incidence map, and a bounded geometric realization of the four intertwiner modules.

**Tests**:
1. Every internal parton belongs to exactly one GHZ cell.
2. Different $\bar U_s$ have disjoint logical support, commute, and satisfy $\bar U_s^2=I$.
3. The lifted one-site operators act within the local intertwiner multiplicity space; this follows from $W_{s,r}$ being an intertwiner and is a convention check, not a separate $[\bar U,\epsilon]$ constraint.

**Pass condition**: The CZX state and its on-site symmetry are fully specified on a finite square-lattice reference cluster.

**Fail condition**: The proposed coarse block is nonlocal, overlaps logical partons between sites, or leaves any parton without a unique GHZ-cell assignment.

---

### Gate C: Global Symmetry on a Small Closed Patch

**Requirement**: On a finite periodic cluster, use the disjoint-site symmetry

$$
\bar{U}_{\text{global}} = \prod_s \bar{U}_s
$$

and test whether a candidate state $|\Psi\rangle$ is invariant:

$$
\bar{U}_{\text{global}} |\Psi\rangle \stackrel{?}{=} |\Psi\rangle
$$

**State candidate**: The encoded plaquette-GHZ state of Section 4.4, optionally decorated by the explicitly evaluated spin-network amplitude of Section 4.3.

**Test**: Compute $\langle \Psi | \bar{U}_{\text{global}} | \Psi \rangle$. Pass if $= 1$ (or $|\langle \Psi | \bar{U}_{\text{global}} | \Psi \rangle| = 1$ up to numerical precision).

---

### Gate D: Parent Hamiltonian

**Requirement**: Construct local parent terms $\bar{h}_p$ such that $|\Psi\rangle$ is the unique ground state of $\bar{H} = \sum_p \bar{h}_p$ with a nonzero gap.

**Approach**: Only after Gates A--C establish the four-parton ownership and the encoded GHZ state, lift the T35a stabilizers onto the corresponding distinct logical partons:

$$
\bar{h}_p = \frac{1}{2}\Big[ (I - \bar{X}_{p,1}\bar{X}_{p,2}\bar{X}_{p,3}\bar{X}_{p,4}) + \sum_{\langle i,j\rangle\subset p}(I-\bar{Z}_{p,i}\bar{Z}_{p,j})\Big].
$$

**Tests**:
1. $\bar{H} |\Psi\rangle = 0$
2. Gap $\Delta E > 0$
3. Local terms commute $[\bar{h}_p, \bar{h}_{p'}] = 0$ (frustration-free)

No parent-Hamiltonian conclusion is permitted for the one-intertwiner-per-vertex model.

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
| **Compatible candidate** | Gates A–D pass with a local four-parton site, explicit incidence, and reproducible numerics | A microscopic encoded CZX candidate exists on the tested lattice. |
| **Partial construction** | Gates A–B pass, C or D fails with documented cause | The kinematics are defined but the candidate does not yet realize the CZX phase. |
| **Obstruction** | No bounded, disjoint four-parton coarse-site realization exists on the chosen lattice | This encoded CZX realization fails on that lattice; the virtual-leg kinematics remain valid. |
| **Not yet decided** | Any gate answered with "not computed" | No conclusion permitted. The claim stays tentative. |

---

## 8. Implementation Notes

### 8.1 Numerical Strategy

For the 2D square reference cluster:
- Four coarse sites contain sixteen logical intertwiner qubits, so the CZX logical Hilbert space has dimension $2^{16}$.
- The fixed-spin intertwiner space is not reduced after $\epsilon$ contraction; the contraction supplies tensor amplitudes.
- Gate A can be tested on one module (a $16\times2$ isometry); Gates B--D require the full sixteen-parton reference cluster.
- Exact state-vector checks are feasible at this reference size.

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

- **T35a**: The raw-qubit CZX reference. This spec seeks an encoded analogue only after reproducing its four-parton site ownership.
- **T35b (old)**: Edge-qubit model with shared physical qubits — failed at $L=3$ due to over-constraint.
- **T35b (new)**: This spec. The failure of the old model motivated the virtual-leg / encoded-operator approach.
- **T33a**: Provides the diamond 2-skeleton for testing a separately specified coarse-site incidence map; it does not yet supply that map.

---

## 9. Open Questions

1. **Intertwiner basis choice**: The recoupling basis $|j_{12}=0, j_{34}=0; J=0\rangle$ vs. $|j_{12}=1, j_{34}=1; J=0\rangle$ is natural for a square, but is it the right basis for the tetrahedral geometry? A tetrahedron has no preferred pairing of faces.

2. **3D coarse-site geometry**: Can a bounded diamond-lattice block supply four owned intertwiner modules and a non-overlapping GHZ-cell incidence map? Hexagons alone do not answer this.

3. **Encoded CZ locality**: Once a coarse site is selected, can its internal CZ ring be realized by bounded gauge-invariant operators without arbitrary long-range couplings?

4. **Relation to LQG volume operator**: The intertwiner qubit is formally similar to the LQG shape qubit. Can the volume operator sign be expressed in this basis? This connects to the original Time's Arrow conjecture.

---

## 10. Next Immediate Step

**Gate 0: define the coarse CZX site and incidence map** for the square reference lattice, then state the required analogue on diamond. After that, write down $W_v$ explicitly in the recoupling basis and verify that:
1. $W_v^\dagger W_v = I_2$
2. The two basis states are SU(2) invariant
3. They are orthonormal

Gate A is a safe independent convention check, but Gates B--E must not start until Gate 0 fixes the four-parton ownership structure.
