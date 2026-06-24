# Simulation Plan: Coupled Spin Network + Matter

*Created: 2026-06-24*
*Task: T26*

## Overview
Couple the Z₂ gauge field to a scalar field on vertices and study whether matter coupling can spontaneously select a global arrow of time from the deconfined phase.

## Motivation

The paper currently explains "time-orientability" (a globally consistent choice of future/past), not a true "arrow of time" (a preferred direction). Matter coupling is a plausible mechanism for selection:

1. Deconfined phase: Z₂ flux is ordered → time is orientable
2. Matter couples to orientation: λ Σ_v ϕ_v τ_v
3. If ⟨ϕ⟩ ≠ 0: matter "picks" a direction → arrow of time emerges

## Model

### Action
```
S = S_Z₂[σ] + S_ϕ[ϕ] + S_int[ϕ, τ]
```

where:
- S_Z₂ = -K Σ_p ∏_{e∈∂p} σ_e (gauge field)
- S_ϕ = Σ_v [½(∇_μ ϕ_v)² + V(ϕ_v)] (scalar field)
- S_int = λ Σ_v ϕ_v τ_v (coupling)

### Scalar Potential
```
V(ϕ) = ½ m² ϕ² + ¼ g ϕ⁴
```

Cases:
- m² > 0, g = 0: free field
- m² < 0, g > 0: double-well (symmetry-breaking potential)

### Vertex Variable τ_v
```
τ_v = ∏_{e∋v} σ_e^{orientation}
```

This is gauge-invariant (transforms as τ_v → τ_v under Z₂ gauge transformation).

## Algorithm

### Coupled Metropolis
1. Update σ_e using standard Metropolis (as in T20)
2. Update ϕ_v using Gaussian or heat-bath proposal
3. Both updates respect detailed balance for the joint action

### Observables

#### 1. Scalar Field Expectation Value
```
⟨ϕ⟩ = (1/L³) Σ_v ⟨ϕ_v⟩
```

- ⟨ϕ⟩ = 0: Z₂ × matter symmetry unbroken
- ⟨ϕ⟩ ≠ 0: symmetry broken, arrow selected

#### 2. Dressed Correlator with Matter
```
C_matter(r) = ⟨ϕ_v τ_v ∏_{e∈γ_{vw}} σ_e τ_w ϕ_w⟩
```

This measures whether matter and orientation are correlated.

#### 3. Susceptibility
```
χ = L³ (⟨ϕ²⟩ - ⟨ϕ⟩²)
```

Diverges at phase transition.

#### 4. Binder Cumulant
```
U = 1 - ⟨ϕ⁴⟩ / (3⟨ϕ²⟩²)
```

Crossing of U_L for different L locates critical point.

## Phase Diagram

Explore (K, λ) plane:

### Region I: K < K_c, any λ
- Confined phase
- No time orientability
- ⟨ϕ⟩ = 0

### Region II: K > K_c, λ < λ_c
- Deconfined, matter-decoupled
- Orientability exists but no arrow selected
- ⟨ϕ⟩ = 0

### Region III: K > K_c, λ > λ_c
- Deconfined, matter-coupled
- Arrow selected
- ⟨ϕ⟩ ≠ 0, correlated with τ_v

### Region IV: K ≈ K_c, λ large
- Competition between gauge and matter transitions
- Complex critical behavior

## Implementation

### Reuse T20 Infrastructure
- Same Z₂ LGT Monte Carlo code
- Add scalar field update and measurements

### Scalar Field Update
```python
# Heat-bath for ϕ_v (Gaussian approximation)
def update_phi(phi, sigma, lambda_coupling, m2, g):
    tau_v = compute_tau(sigma, v)
    force = lambda_coupling * tau_v - m2 * phi[v] - g * phi[v]**3
    # Langevin or Metropolis step
    ...
```

## Expected Results

### If Symmetry Breaking Occurs
- ⟨ϕ⟩ ≠ 0 for K > K_c and λ > λ_c
- C_matter(r) → constant as r → ∞
- Phase diagram with critical line λ_c(K)

### If No Symmetry Breaking
- ⟨ϕ⟩ = 0 for all λ (Mermin-Wagner theorem in 2D, but 3D allows SSB)
- Matter couples but doesn't select arrow
- Paper's scope should remain "orientability"

## Code Structure

```
code/simulations/coupled-matter/
├── src/
│   ├── scalar_field.py    # ϕ field update and measurements
│   ├── coupling.py        # τ_v computation and S_int
│   └── phase_diagram.py   # Scan (K, λ) plane
├── run_coupled.py
└── figures/
    ├── phase_diagram.pdf
    ├── phi_vs_lambda.pdf
    └── correlator_matter.pdf
```

## Validation
1. Recover pure Z₂ LGT results when λ = 0
2. Recover free scalar field when K = 0
3. Check detailed balance for coupled updates

## Timeline
- Implementation: 2-3 weeks (builds on T20)
- Phase diagram scan: 2-3 weeks
- Analysis: 1-2 weeks
- Total: 2-3 months

## References
- Langguth, Münster, Weisz (1986): Higgs model on lattice
- Fradkin & Shenker (1979): Phase diagrams in lattice gauge theories with Higgs fields
- Kogut (1983): Review of lattice gauge theory with matter
