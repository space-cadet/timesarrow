# Simulation Plan: Domain Wall Dynamics

*Created: 2026-06-24*
*Task: T24*

## Overview
Simulate domain walls between regions of opposite Z₂ time orientation and test the conjecture that they host all-fermion toric code surface states.

## Domain Wall Setup

### Initial Configuration
- 3D cubic lattice, size L × L × 2L
- Fixed boundary conditions:
  - z < L: σ_e = +1 ("future" orientation)
  - z > L: σ_e = -1 ("past" orientation)
- Domain wall at z = L (initially flat)

### Equilibration
- Run Metropolis at fixed K > K_c
- Allow domain wall to thermalize and fluctuate
- Measure after 10⁴ sweeps

## Observables

### 1. Domain Wall Tension
```
σ_DW = (E[with wall] - E[bulk]) / (L × L)
```

Expected scaling near criticality:
```
σ_DW ~ (K - K_c)^μ
```
with μ ≈ 1 (mean-field) or μ ≈ 1.26 (3D Ising surface tension exponent).

### 2. Surface Wilson Loops
On the domain wall plane (z = L):
```
W_surface(γ) = ⟨∏_{e∈γ} σ_e⟩
```

Expected:
- Perimeter law in deconfined phase (surface is topologically ordered)
- Measures surface anyon condensation

### 3. Anyon Statistics

#### String Operators
Create anyons by open string operators on the surface:
- e-particle: electric string (σ_e product)
- m-particle: magnetic string (dual variable)
- ε = e × m: fermionic composite

#### Braiding Phases
Compute mutual statistics via:
```
θ_{ab} = ⟨W_a W_b⟩ / (⟨W_a⟩⟨W_b⟩)
```

Expected for all-fermion toric code:
- θ_{ee} = θ_{mm} = θ_{εε} = π (all fermions)
- θ_{em} = π/2 (semionic mutual statistics)

**Note:** Computing braiding phases numerically is non-trivial. Alternative: use topological ground state degeneracy on torus as proxy.

### 4. Surface Gap
- Measure correlation length on domain wall
- Verify gapped spectrum (no gapless modes)

## Computational Approach

### Surface-Restricted Simulation
Instead of full 3D, simulate effective 2D theory on domain wall:
1. Extract surface configuration from 3D equilibration
2. Build effective Hamiltonian for surface degrees of freedom
3. Use 2D DMRG or exact diagonalization for small systems

### Full 3D Simulation
- More faithful to paper's framework
- Expensive but straightforward extension of T20

## Expected Results

### Scenario A: All-Fermion Toric Code (Paper's Conjecture)
- All anyons have fermionic self-statistics
- Surface is gapped
- Strong support for fermionic matter emergence

### Scenario B: Standard Toric Code
- Only ε is fermionic, e and m are bosons
- Still gapped
- Partial support; paper's conjecture needs refinement

### Scenario C: No Topological Order
- Surface is trivial or gapless
- Contradicts SPT prediction; paper's conjecture is wrong

## Code Structure

```
code/simulations/domain-wall/
├── src/
│   ├── wall_setup.py      # Domain wall initial configuration
│   ├── surface_ops.py     # Surface Wilson loops and string operators
│   ├── anyons.py          # Anyon creation and braiding
│   └── gap.py             # Surface correlation length
├── run_domain_wall.py
└── analysis/
```

## Validation
1. Reproduce standard Z₂ gauge theory bulk results (T20)
2. Check domain wall tension against theoretical predictions
3. Verify surface topological order using known results

## Timeline
- Implementation: 2-3 weeks (builds on T20)
- Production runs: 2-3 weeks
- Analysis: 1-2 weeks
- Total: 1-2 months

## References
- Vishwanath & Senthil (2013): All-fermion toric code
- Burnell et al.: Exactly solvable models of SPT surfaces
- Wang & Senthil (2013): Boson topological insulators
- Levin & Gu (2012): Braiding statistics of SPT phases
