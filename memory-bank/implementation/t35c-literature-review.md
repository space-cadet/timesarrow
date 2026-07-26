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

### 1. Diamond Lattice Topological Phases

**arXiv:0811.2036** — Shinsei Ryu, *"Three-dimensional topological phase on the diamond lattice"* (2008)
- **Journal**: Phys. Rev. B 79, 075124 (2009)
- **Relevance**: ⭐⭐⭐⭐⭐ Directly addresses topological phases on the diamond lattice
- **Model**: Kitaev-type interacting bosonic model
- **Key finding**: Two phases ("weak" and "strong" pairing) on the diamond lattice. The weak pairing phase is a topological superconducting phase characterized by non-zero winding number, protected by discrete symmetry.
- **Connection to T35c**: Shows that non-trivial topological phases CAN exist on the diamond lattice, but this is a Majorana/superconducting model, not an SPT.
- **Gap**: Does not address SPT phases or cluster-state constructions.

**arXiv:2212.06190** — Shang et al., *"IrF4: From Tetrahedral Compass Model to Topological Semimetal"* (2022)
- **Journal**: Phys. Rev. B 107, 125111 (2023)
- **Relevance**: ⭐⭐⭐ Uses tetrahedral geometry
- **Model**: Tetrahedral compass model → topological semimetal
- **Connection to T35c**: Tetrahedral symmetry appears in material contexts, but this is about semimetals, not SPTs.

**arXiv:1612.02614** — Takahashi et al., *"Edge states of mechanical diamond and its topological origin"* (2016)
- **Journal**: New J. Phys. 19, 035003 (2017)
- **Relevance**: ⭐⭐⭐ Mechanical (classical) topological model on diamond lattice
- **Connection to T35c**: Shows topological edge states can exist on diamond lattice, but in a classical spring-mass model.

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

## Key Insights from Literature

### 1. Diamond Lattice CAN Support Topological Phases

Ryu (2008) proved that the diamond lattice supports a 3D topological superconducting phase. This is not an SPT, but it shows the lattice itself is not an obstruction.

**Implication for T35c**: The diamond lattice geometry alone does not prevent topological order. The question is whether an SPT (specifically a cluster-state SPT) can exist.

### 2. Commuting Projector Models Are Well-Studied

Multiple papers (Inamura 2021, Kobayashi 2020, Horinouchi 2020) construct commuting projector Hamiltonians for SPTs in various dimensions and symmetries. The key requirement is that the projectors commute.

**Implication for T35c**: If K₄ on diamond lattice with face-qubits cannot be written as commuting projectors, it may still be a valid SPT but with a non-commuting Hamiltonian. This would be a different class of model.

### 3. Generalized Cluster States and Equivalence

Jia (2024) and Inamura & Ohyama (2026) show that different cluster-state constructions can be related through:
- Gauging subgroups
- Hopf algebra structures
- Non-invertible symmetries

**Implication for T35c**: There may be a formal way to determine if K₄ and C₄ are in the same SPT phase, even if they look different locally.

### 4. Complete Graph States Exist

Li et al. (2024) generate complete graph states (K₄) experimentally. The K₄ state is a valid quantum state.

**Implication for T35c**: The K₄ operator is not algebraically invalid. The question is only whether it can be assembled into a lattice SPT.

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
