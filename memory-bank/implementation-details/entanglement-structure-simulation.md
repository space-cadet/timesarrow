# Simulation Plan: Entanglement Structure of Deconfined Phase

*Created: 2026-06-24*
*Task: T23*

## Overview
Compute topological entanglement entropy in the 3D Z₂ gauge theory to provide smoking-gun evidence for topological order in the deconfined phase.

## Theory

For a topologically ordered system, the entanglement entropy has the form:
```
S(A) = α|∂A| - γ + ...
```

where:
- α: non-universal coefficient (depends on microscopic details)
- γ: topological entanglement entropy (universal)
- |∂A|: area of the boundary of region A

For Z₂ gauge theory:
- Deconfined phase: γ = log(2) (D = 2, total quantum dimension)
- Confined phase: γ = 0 (no topological order)

## Method: Swap Operator

The second Rényi entropy:
```
S₂(A) = -ln ⟨Swap_A⟩
```

where Swap_A exchanges the configuration in region A between two independent copies of the system.

### Algorithm
1. Run two independent Monte Carlo simulations
2. Every N sweeps, attempt a swap of region A between the two copies
3. Measure acceptance probability
4. S₂(A) = -ln(P_accept)

### Subtraction Scheme (Kitaev-Preskill)

To isolate γ, use:
```
γ = S(A) + S(B) - S(A∪B) - S(A∩B)
```

for appropriately chosen regions A, B.

## Implementation

### Reuse T20 Infrastructure
- Same lattice and Monte Carlo code
- Add swap operation and second-copy management

### Regions
1. **Cylinder:** A = [0,L_x] × [0,L_y] × [0,ℓ]
2. **Sphere:** radius R centered in lattice
3. **Annulus:** for Kitaev-Preskill subtraction

### Parameters
- Same as T20: L = 8, 12, 16, 20
- Swap interval: every 10 sweeps (after thermalization)
- Statistics: 10⁵ measurements per coupling

## Expected Results

### Confined Phase (K < K_c)
- S₂(A) = α|∂A| + O(1/|∂A|)
- γ = 0 (no topological term)

### Deconfined Phase (K > K_c)
- S₂(A) = α|∂A| - log(2) + ...
- γ = log(2) (topological order confirmed)

### Near Criticality (K ≈ K_c)
- Crossover behavior
- γ may show finite-size effects

## Code Structure

```
code/simulations/z2-lgt/
├── src/
│   ├── entanglement.py    # Swap operator and Rényi entropy
│   └── subtraction.py     # Kitaev-Preskill scheme
├── run_entanglement.py
└── figures/
    ├── s2_vs_area.pdf
    └── gamma_vs_k.pdf
```

## Validation
1. Reproduce toric code result γ = log(2) at strong coupling
2. Verify γ = 0 at weak coupling
3. Check finite-size scaling of γ near K_c

## Timeline
- Implementation: 3-5 days (builds on T20)
- Production runs: 1-2 weeks
- Analysis: 3-5 days
- Total: 2-3 weeks (parallel with T20 analysis)

## References
- Kitaev & Preskill (2006): Topological entanglement entropy
- Levin & Wen (2006): Detecting topological order
- Isakov et al. (2011): Topological entanglement entropy of a Bose-Hubbard spin liquid
