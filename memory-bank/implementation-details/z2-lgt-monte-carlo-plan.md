# Simulation Plan: 3D Z₂ Lattice Gauge Theory Monte Carlo

*Created: 2026-06-24*
*Task: T20*

## Overview
This document details the implementation plan for Monte Carlo simulation of the 3D Z₂ lattice gauge theory that underpins the arrow-of-time mechanism in the manuscript.

## Model

The effective action (Eq. 48 in timesarrow.tex):
```
S[σ] = -K Σ_p ∏_{e∈∂p} σ_e
```

where:
- σ_e ∈ {+1, -1} on each edge of a cubic lattice
- p labels plaquettes (square faces)
- ∂p is the boundary of plaquette p (4 edges)
- K is the dimensionless coupling

## Algorithm

### Standard Metropolis
1. Visit each edge sequentially
2. Propose flip: σ_e → -σ_e
3. Compute ΔS = S[new] - S[old]
4. Accept with probability min(1, exp(-ΔS))

### Observables

**Wilson Loop:**
```
W(γ) = ⟨∏_{e∈γ} σ_e⟩
```
for rectangular loops of size R × T.

**Dressed Correlator:**
```
C(r) = ⟨τ_0 ∏_{e∈γ_{0r}} σ_e τ_r⟩
```
where τ_v ∈ {+1, -1} are auxiliary vertex variables.

**Specific Heat:**
```
C_v = (⟨S²⟩ - ⟨S⟩²) / L³
```

**Binder Cumulant:**
```
U_L = 1 - ⟨W⁴⟩ / (3⟨W²⟩²)
```
for crossing determination.

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Lattice sizes | L = 8, 12, 16, 20 | Finite-size scaling |
| Thermalization | 10⁴ sweeps | Discard |
| Measurements | 10⁵ sweeps | With binning |
| Couplings | K ∈ [0.3, 0.6] | Around expected K_c ≈ 0.44 |
| Bin size | 100 sweeps | Autocorrelation analysis |

## Expected Results

### Phase Transition
- Critical coupling: K_c ≈ 0.44 (3D Ising gauge theory)
- Universality class: 3D Ising (ν ≈ 0.62997, β ≈ 0.32642)

### Wilson Loop Scaling
- K < K_c: ln W(L) ~ -c L² (area law)
- K > K_c: ln W(L) ~ -c' L (perimeter law)
- K = K_c: ln W(L) ~ -c'' L^θ with θ ≈ 1 (rough)

### Dressed Correlator
- Confined: C(r) ~ exp(-r/ξ) with ξ ~ few lattice spacings
- Deconfined: C(r) → constant as r → ∞ (long-range order)

## Code Structure

```
code/simulations/z2-lgt/
├── src/
│   ├── lattice.py        # 3D cubic lattice geometry
│   ├── monte_carlo.py    # Metropolis algorithm
│   ├── observables.py    # Wilson loop, correlator measurements
│   └── analysis.py       # Finite-size scaling, critical exponents
├── run_simulation.py     # Main driver
├── analyze_results.py    # Post-processing
└── figures/              # Output plots
```

## Dependencies
- Python 3.9+
- NumPy, SciPy
- Matplotlib (plotting)
- tqdm (progress bars)

## Validation
1. Reproduce known 3D Ising gauge theory results from literature
2. Check detailed balance and ergodicity
3. Verify autocorrelation times are properly handled

## Timeline
- Implementation: 1 week
- Production runs: 1 week
- Analysis and figures: 1 week
- Total: 2-3 weeks

## References
- Wegner (1971): Original Z₂ gauge theory
- Kogut (1979): Review of lattice gauge theory
- Fradkin & Susskind (1979): Phase structure
- Balian et al. (1975): Gauge fixing and observables
