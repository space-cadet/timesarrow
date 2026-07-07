# Calculation Plan: Volume Operator Extension

*Created: 2026-06-24*
*Task: T25*

## Overview
Extend volume operator diagonalization to higher-valence vertices, verifying whether the Z₂ sign-flip structure is generic or specific to 4-valent j=1/2.

## Background

The signed volume operator at a vertex v:
```
Q̂_v = Σ_{I<J<K} ε^{ijk} Ĵ_i^{(I)} Ĵ_j^{(J)} Ĵ_k^{(K)}
```

where I, J, K label triples of edges meeting at v, and Ĵ_i^{(I)} are SU(2) generators on edge I.

For 4-valent j=1/2, the singlet subspace is 2-dimensional, spanned by |Φ₁⟩, |Φ₂⟩ with eigenvalues ±q₀.

## Cases to Study

### Case 1: 4-valent, j=1/2 (Verification)
- Matrix size: 16 × 16 (full), 2 × 2 (singlet)
- Expected: eigenvalues ±q₀
- Purpose: Verify supplementary calculations

### Case 2: 4-valent, j=1
- Matrix size: 81 × 81 (full)
- Singlet subspace dimension: ? (need CG decomposition)
- Question: Does ± degeneracy persist?

### Case 3: 5-valent, j=1/2
- Matrix size: 32 × 32 (full)
- Need to impose Gauss constraint Σ_{e∈v} Ĵ_e = 0
- Question: Is the invariant subspace 2-dimensional?

### Case 4: 6-valent, j=1/2
- Matrix size: 64 × 64 (full)
- Similar to 5-valent but more edges

### Case 5: Mixed j
- Example: two j=1/2 edges, two j=1 edges
- Tests whether algebraic ± spectral reflection symmetry requires uniform j

## Method

### Step 1: Build Angular Momentum Operators
For each edge I:
```
Ĵ_i^{(I)} = 1_{2j_1+1} ⊗ ... ⊗ J_i^{(j_I)} ⊗ ... ⊗ 1_{2j_n+1}
```

### Step 2: Construct Q̂_v
Sum over all triples of edges:
```
Q̂_v = Σ_{I<J<K} ε^{ijk} Ĵ_i^{(I)} Ĵ_j^{(J)} Ĵ_k^{(K)}
```

### Step 3: Project to Invariant Subspace
Build Gauss constraint projector:
```
P_0 = δ(Σ_{e∈v} Ĵ_e)
```
and project Q̂_v to this subspace.

### Step 4: Diagonalize
Use NumPy/SciPy for exact diagonalization.

## Implementation

```python
import numpy as np
from numpy.linalg import eigh

# SU(2) generators for spin j
def su2_generators(j):
    # Returns Jx, Jy, Jz as (2j+1) x (2j+1) matrices
    ...

# Build volume operator for n-valent vertex
def volume_operator(j_list):
    n = len(j_list)
    dims = [int(2*j + 1) for j in j_list]
    total_dim = np.prod(dims)
    
    Q = np.zeros((total_dim, total_dim))
    for I in range(n):
        for J in range(I+1, n):
            for K in range(J+1, n):
                # Add ε^{ijk} J_i^I J_j^J J_k^K
                ...
    return Q

# Main calculation
for n in [4, 5, 6]:
    for j in [0.5, 1.0, 1.5]:
        Q = volume_operator([j]*n)
        # Project, diagonalize, analyze spectrum
```

## Expected Outcomes

### Scenario A: Universal ± Structure (Algebraic)
- All cases show two-fold degeneracy with ± eigenvalues.
- This establishes an **algebraic spectral reflection symmetry** of the volume operator.
- Demonstrating that this algebraic symmetry corresponds to a **physical $Z_2$ time-orientation symmetry** would require constructing an explicit symmetry generator and verifying it commutes with the Hamiltonian while acting as $q \to -q$ on eigenstates.

### Scenario B: j=1/2 is Special
- Only j=1/2 shows ± structure
- Higher spins have more complex spectra
- Justifies j=1/2 restriction as physically meaningful

### Scenario C: Valence-Dependent
- 4-valent: ± structure
- 5+ valent: different structure
- Suggests 4-valent vertices are special (consistent with simplicial decomposition)

## Code Structure

```
code/simulations/volume-operator/
├── src/
│   ├── su2.py             # SU(2) representation matrices
│   ├── volume.py          # Volume operator construction
│   ├── invariant.py       # Gauss constraint projection
│   └── analyze.py         # Spectrum analysis
├── run_volume.py
└── results/
```

## Validation
1. Reproduce 4-valent j=1/2 results from supplementary calculations
2. Check hermiticity of Q̂_v
3. Verify Gauss constraint commutation [Q̂_v, ΣĴ_e] = 0

## Timeline
- Implementation: 2-3 days
- Calculations: 1-2 days
- Analysis: 1 day
- Total: 3-5 days

## References
- Brunnemann & Thiemann (2006): Volume operator simplification
- Borissenko & Ivanov (2021): 4-valent volume eigenvalues
- Rovelli & Smolin (1995): Discreteness of area and volume
