# T35c Literature Review: K₄ Face-Qubit CZX Investigation

*Date: 2026-07-26*
*Status: IN PROGRESS*

---

## Search Queries Executed

1. `symmetry protected topological diamond lattice` — 11 results
2. `3D SPT Z2 diamond lattice` — 0 results
3. `SPT non-commuting projector` — 4 results
4. `cluster state SPT phase` — 35 results
5. `complete graph controlled-Z` — 5 results
6. `graph state SPT equivalence` — 1 result

---

## Relevant Papers Found

## 1. Diamond Lattice Topological Phases

### arXiv:0811.2036 — Shinsei Ryu, *"Three-dimensional topological phase on the diamond lattice"* (2008)
**Journal**: Phys. Rev. B 79, 075124 (2009) | **Relevance**: ⭐⭐⭐⭐⭐

**Deep Read Summary (Sage, 2026-07-26)**:

**Model**: Kitaev-type interacting bosonic model on the 3D diamond lattice. Each site has a **4D Hilbert space** (spin-3/2, or equivalently two spin-1/2 degrees of freedom σ ⊗ τ). The Hamiltonian is:

```
H = Σ_µ Σ_<jk>_µ  Jµ (αⱼ^µ αₖ^µ + ζⱼ^µ ζₖ^µ)
```

where α^µ and ζ^µ are two sets of Dirac gamma matrices acting on the local 4D Hilbert space. Four bond types µ=0,1,2,3 correspond to the four edge orientations of the diamond lattice.

**Symmetry**: The model has:
- Time-reversal T (T² = +1) and T′ (T′⁴ = 1, exchanges α ↔ ζ)
- A discrete rotation R (π/2 around τᵧ)
- A continuous U(1) symmetry for rotation around τᵧ axis
- **The topological phase is protected by a combination of time-reversal and four-fold discrete rotation**

**Solution method**: Exact solution via Majorana fermion representation. Six Majorana fermions λ₀...₅ per site. The Hamiltonian reduces to a Majorana hopping problem with a Z₂ gauge field uⱼₖ = ±1 on each link. By Lieb's theorem, the ground state is in the vortex-free sector (uⱼₖ = +1 for all links).

**Two phases**:
1. **Weak pairing phase**: Non-zero winding number ν ≠ 0. Topological superconductor in class DIII (3D analogue of Moore-Read Pfaffian). Has gapless surface Majorana fermion modes.
2. **Strong pairing phase**: ν = 0. Trivial phase. No surface states.

**Key distinction**: This is NOT an SPT phase — it's a **topological superconductor** (class DIII) with emergent Majorana fermions. The ground state is obtained by projection from a fermionic state, not by applying CZ gates to a product state.

**Critical insight for T35c**: The diamond lattice **CAN support topological phases**. The 4D Hilbert space per site is essential. However, this model's topological character is protected by **time-reversal + discrete rotation**, not by a simple Z₂ on-site symmetry like the CZX construction.

**Relevance to K₄ vs C₄ question**: This paper shows that:
- The diamond lattice geometry is NOT an obstruction
- A 4D Hilbert space per site is natural on the diamond lattice
- Different symmetries (T′ + rotation vs Z₂) protect different topological phases
- The Majorana construction is fundamentally different from the cluster-state SPT construction

**Gap for T35c**: Does NOT address:
- Cluster states or CZ-based constructions
- SPT phases with Z₂ symmetry
- Whether K₄ connectivity preserves the same symmetry as C₄
- Whether a commuting projector Hamiltonian exists for face-qubits

---

### 2. Cluster States and SPT Phases

**arXiv:2405.09277** — Jia, *"Generalized cluster states from Hopf algebras: non-invertible symmetry and Hopf tensor network representation"* (2024)
- **Journal**: JHEP 2024, 147 (2024)
- **Relevance**: ⭐⭐⭐⭐⭐ Most relevant to our cluster-state/SPT question
- **Key finding**: Generalized cluster states can be constructed from Hopf algebras, with non-invertible symmetries.
- **Connection to T35c**: Provides a framework for understanding when different graph states are in the same SPT phase. The Hopf algebra structure may relate to our K₄ vs C₄ question.
- **Gap**: Does not specifically address K₄ connectivity or diamond lattice.

**arXiv:2601.10817** — Inamura & Ohyama, *"Generalized cluster states in 2+1d: non-invertible symmetries, interfaces, and parameterized families"* (2026)
- **Relevance**: ⭐⭐⭐⭐⭐ Highly relevant
- **Key finding**: 2+1D lattice models of SPT phases with non-invertible symmetries, constructed by gauging. Generalized cluster models.
- **Connection to T35c**: Shows that different cluster-state constructions can be related by gauging. May provide a path to understand if K₄ and C₄ are equivalent.

**arXiv:2505.01978** — Jiang et al., *"Generation of 95-qubit genuine entanglement and verification of symmetry-protected topological phases"* (2025)
- **Journal**: Nat. Phys. 22, 430-438 (2026)
- **Relevance**: ⭐⭐⭐ Experimental verification of SPT phases
- **Connection to T35c**: Shows that SPT phases can be experimentally verified, but doesn't address our theoretical question.

### 3. Commuting Projector Models

**arXiv:2110.12882** — Inamura, *"On lattice models of gapped phases with fusion category symmetries"* (2021)
- **Journal**: JHEP 2022, 036 (2022)
- **Relevance**: ⭐⭐⭐⭐ Commuting projector Hamiltonians for SPT phases
- **Key finding**: Construction of TQFTs and commuting projector Hamiltonians for 1+1D gapped phases with fusion category symmetries.
- **Connection to T35c**: The commuting projector framework is exactly what we need. If K₄ on diamond lattice cannot be written as commuting projectors, this paper's techniques might explain why.

**arXiv:2006.00159** — Kobayashi, *"Commuting projector models for (3+1)d topological superconductors via string net of (1+1)d topological superconductors"* (2020)
- **Journal**: Phys. Rev. B 102, 075135 (2020)
- **Relevance**: ⭐⭐⭐⭐ 3+1D commuting projector models
- **Key finding**: Construction of 3+1D topological superconductors using string nets.
- **Connection to T35c**: Techniques for higher-dimensional commuting projector models.

**arXiv:2002.01639** — Horinouchi, *"Solvable lattice model for (2+1)D bosonic topological insulator"* (2020)
- **Relevance**: ⭐⭐⭐⭐ Exactly solvable commuting projector for SPT
- **Key finding**: Commuting projector Hamiltonian for 2+1D bosonic topological insulator (U(1) × Z₂^T symmetry).
- **Connection to T35c**: Shows that commuting projector constructions exist for SPTs, but specific to U(1) × time-reversal symmetry.

### 4. Complete Graph States

**arXiv:2401.01986** — Li et al., *"Generation of complete graph states in a spin-1/2 Heisenberg chain with a globally optimized magnetic field"* (2024)
- **Journal**: Phys. Rev. A 109, 042604 (2024)
- **Relevance**: ⭐⭐⭐ Complete graph states (K₄ = complete graph on 4 vertices)
- **Key finding**: Complete graph states can be generated in spin chains.
- **Connection to T35c**: Complete graph states are exactly the K₄ states we need! But this paper is about generation, not SPT classification.

**arXiv:2601.19857** — de Jesus et al., *"Symmetric and Antisymmetric Quantum States from Graph Structure and Orientation"* (2026)
- **Journal**: Entropy 28(4), 386 (2026)
- **Relevance**: ⭐⭐⭐ Graph states from CZ interactions
- **Key finding**: Graph states encode symmetric exchange properties based on graph structure.
- **Connection to T35c**: Graph state formalism may help compare K₄ and C₄.

---

## Key Insights from Literature (Updated after Deep Read of Ryu 2008)

### 1. Diamond Lattice CAN Support Topological Phases ✅

Ryu (2008) proved that the diamond lattice supports a 3D **topological superconducting phase** (class DIII, weak pairing phase with ν ≠ 0). This is NOT an SPT, but it shows the lattice itself is not an obstruction.

**Critical detail**: The model uses a **4D Hilbert space per site** — naturally described as two spin-1/2 degrees of freedom (σ ⊗ τ) or a spin-3/2. This is the same dimensionality as Deepak's face-qubit model (4 qubits = 2⁴ = 16D Hilbert space... wait, that's different. Let me check: 4 qubits per vertex = 2⁴ = 16D Hilbert space. Ryu's model has 4D per site = spin-3/2. These are different.)

**Correction**: Deepak's face-qubit model has **4 qubits per vertex** (16D Hilbert space), while Ryu's model has a **4D Hilbert space per site** (spin-3/2 or two spin-1/2s). These are different scales. However, both use the diamond lattice's 4-valent structure.

### 2. Symmetry Protection is Different

Ryu's topological phase is protected by **time-reversal + four-fold discrete rotation** (T′ symmetry, where T′⁴ = 1). This is fundamentally different from the **Z₂ on-site symmetry** of the CZX construction.

**Implication**: Even if the diamond lattice supports topological phases, the specific symmetry that protects them matters. The CZX SPT requires a specific Z₂ symmetry; Ryu's model uses a different symmetry.

### 3. Exact Solvability via Majorana Fermions

Ryu's model is solvable by mapping to Majorana fermions. The CZX cluster-state SPT is constructed by applying CZ gates to a product state. These are **different construction methods**:
- Majorana: Interacting bosonic model → fermionization → projection
- CZX: Product state → CZ gates → cluster state

**Question**: Can the CZX construction be fermionized? Or is it inherently bosonic?

### 4. Commuting Projectors vs Majorana Hopping

Ryu's Hamiltonian is NOT a commuting projector model. It's an interacting bosonic model that maps to a free Majorana hopping problem. The CZX parent Hamiltonian IS a commuting projector model.

**Implication**: If K₄ on diamond lattice with face-qubits cannot be written as commuting projectors, it may still be a valid topological phase (like Ryu's model), but in a different universality class.

---

---

## Gaps in Literature

| Question | Literature Coverage |
|----------|---------------------|
| K₄ vs C₄ SPT equivalence | ❌ NOT addressed directly |
| SPT on diamond lattice with face DOF | ❌ NOT addressed |
| Non-commuting Hamiltonians for SPT | ⚠️ Partial (commuting projectors preferred) |
| Frustration in SPT parent Hamiltonians | ⚠️ Limited |
| 3D Z₂ SPT on non-simple lattices | ⚠️ Some (Ryu 2008), but not SPT |

## Most Relevant Papers for Further Reading

1. **Jia (2024)** — Generalized cluster states from Hopf algebras. Most likely to contain tools for comparing K₄ and C₄.
2. **Inamura & Ohyama (2026)** — 2+1D generalized cluster models with non-invertible symmetries.
3. **Inamura (2021)** — Commuting projector models for fusion category symmetries.
4. **Ryu (2008)** — Diamond lattice topological phase (for lattice-specific context).

## Next Steps for Literature Search

- [ ] Read Jia (2024) in detail — check if Hopf algebra framework can compare K₄ and C₄
- [ ] Search for "bipartite lattice SPT obstruction" specifically
- [ ] Search for "frustrated SPT" or "non-commuting SPT"
- [ ] Check if K₄ complete graph state has been studied as an SPT ground state
- [ ] Look for papers on "graph state equivalence under local complementation" (may relate to K₄ ↔ C₄)

## Preliminary Conclusion

**The literature does not directly answer whether K₄ and C₄ are in the same SPT phase.** However:

1. The diamond lattice supports topological phases (Ryu 2008)
2. Complete graph states are valid quantum states (Li 2024)
3. Different cluster states can be related by gauging (Jia 2024, Inamura 2026)
4. Commuting projector models are the standard but not the only possibility

**This suggests the numerical investigation (Track 1) is necessary and worthwhile.** The literature provides tools but not the answer.

---

*Last updated: 2026-07-26*
*Next update: After detailed reading of top-priority papers*
