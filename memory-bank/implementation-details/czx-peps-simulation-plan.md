# Simulation Plan: CZX-Spin Network PEPS Ground State

*Created: 2026-06-24*
*Task: T21*

## Overview
Construct the ground state of the CZX-like spin-network state using PEPS in 3D, verifying the SPT structure that underlies the deconfined phase.

## PEPS Construction

### Local Tensor Structure

Each 4-valent spin-network vertex contributes a PEPS tensor with:
- 1 physical index: i ∈ {0,1} (intertwiner qubit)
- 4 virtual indices: u, d, l, r ∈ {0,1} (bond indices, matching j=1/2)
- Plaquette constraint: |0000⟩ + |1111⟩ on each face

### Intertwiner Basis

From supplementary calculations (T11/C3), the corrected singlet basis is:
```
|Φ₁⟩ = ½(|0101⟩ - |0110⟩ - |1001⟩ + |1010⟩)
|Φ₂⟩ = (1/√12)(2|0011⟩ - |0101⟩ - |0110⟩ - |1001⟩ - |1010⟩ + 2|1100⟩)
```

The CZX code subspace is span{|0000⟩, |1111⟩}. The correspondence is:
- |Φ₁⟩ ↔ effective |0⟩_code
- |Φ₂⟩ ↔ effective |1⟩_code

### Plaquette Projectors

The plaquette state (Eq. 64-65):
```
|ψ_p⟩ = |0000⟩_p + |1111⟩_p
```

This is enforced by a rank-2 projector P_p on each plaquette:
```
P_p = |ψ_p⟩⟨ψ_p| / ⟨ψ_p|ψ_p⟩
```

## Implementation Strategy

### Option A: Variational PEPS
1. Start with random PEPS tensor
2. Optimize using simple update or full update
3. Target: maximize overlap with CZX plaquette constraints

### Option B: Exact Construction
1. Build transfer operator from plaquette projectors
2. Find fixed point (dominant eigenvector)
3. Construct PEPS from fixed point

### Option C: Boundary MPS
1. Contract layer by layer
2. Approximate boundary with MPS
3. Use DMRG-like optimization

## Observables

### Gap Verification
- Compute energy spectrum via transfer operator
- Verify Δ = E₁ - E₀ > 0

### Entanglement Entropy
- S₂(A) for half-system bipartition
- Extract topological term γ

### String Order Parameter
- Non-local order parameter for SPT phases
- Should be non-zero in non-trivial SPT, zero in trivial phase

## Computational Considerations

3D PEPS is expensive. Strategies:
1. Start with 2D CZX as benchmark (well-understood)
2. Use small bond dimension D = 2, 4, 8
3. Employ GPU acceleration if available
4. Consider iTEBD for infinite systems

## Validation
1. Reproduce known 2D CZX results
2. Verify toric code equivalence in deconfined limit
3. Check topological entanglement entropy γ = log(2)

## Timeline
- 2D benchmark: 1-2 weeks
- 3D implementation: 3-4 weeks
- Analysis: 1-2 weeks
- Total: 1-2 months

## References
- Chen, Gu, Wen (2010, 2011): CZX model
- Verstraete, Murg, Cirac (2008): PEPS review
- Bridgeman, Chubb (2017): Tensor network review
- Schuch et al. (2011): PEPS classification
