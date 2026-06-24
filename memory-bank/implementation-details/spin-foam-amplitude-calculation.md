# Calculation Plan: Spin Foam Amplitude for j=1/2 Dominance

*Created: 2026-06-24*
*Task: T22*

## Overview
Numerically evaluate EPRL/FK spin foam vertex amplitudes to verify j=1/2 dominance, addressing the key weakness identified in peer review.

## Background

The paper assumes j=1/2 edges dominate at the Planck scale. Three arguments are given:
1. Amplitude suppression in spin foam models
2. Entropy counting (combinatorial dominance)
3. Black hole entropy matching

The GPT 5.5 review found argument 2 weak and argument 3 context-specific. A direct spin-foam calculation is needed.

## Spin Foam Vertex Amplitude

### EPRL Vertex
```
A_v^{EPRL}(j₁, j₂, j₃, j₄) = ∫_{SL(2,C)} ∏_{i=1}^4 dg_i δ(∏_i g_i) ∏_{i=1}^4 D^{(γj_i, j_i)}(g_i)
```

where D^{(γj, j)} is the SL(2,C) representation matrix in the principal series.

### FK Vertex (Euclidean)
```
A_v^{FK}(j₁, j₂, j₃, j₄) = ∫_{SU(2)} ∏_{i=1}^4 dh_i δ(∏_i h_i) ∏_{i=1}^4 D^{j_i}(h_i)
```

### Asymptotic Formula (Large j)

From Donà et al. (2022):
```
A_v ~ j^{-α} exp(i S_{Regge}[j])
```

where α depends on the model and vertex geometry.

## Implementation

### Method 1: Numerical Integration (Small j)
- Monte Carlo integration over SU(2) or SL(2,C)
- Compute for j = 1/2, 1, 3/2, 2, 5/2, 3
- Use coherent state boundary conditions

### Method 2: Asymptotic Formula (Large j)
- Use stationary phase approximation
- Extract exponent α from numerical fit
- Valid for j ≳ 2

### Method 3: Direct Comparison
- Compute |A_v|² for various (j₁, j₂, j₃, j₄) combinations
- Plot relative weights
- Check if j=1/2 configurations dominate partition function

## Key Configurations

1. **Uniform:** j₁ = j₂ = j₃ = j₄ = j
2. **Mixed low:** three j=1/2, one j=1
3. **Mixed high:** three j=1/2, one j=3/2
4. **Checkerboard:** alternating j=1/2 and j=1 on lattice

## Parameters
- Immirzi parameter γ = 0.237 (black hole entropy matching)
- Boundary states: Livine-Speziale coherent states with spread parameter

## Expected Outcomes

### Scenario A: Strong Suppression (α ≳ 2)
j=1/2 dominance is robust. Update manuscript to include numerical evidence.

### Scenario B: Weak Suppression (α < 1)
j=1/2 dominance is not guaranteed by amplitudes alone. Rely on thermal argument or acknowledge assumption more explicitly.

### Scenario C: Model-Dependent
EPRL and FK give different α. Document model-dependence in manuscript.

## Code Structure

```
code/simulations/spin-foam/
├── src/
│   ├── eprl_vertex.py     # EPRL amplitude calculation
│   ├── fk_vertex.py       # FK amplitude calculation
│   ├── coherent_states.py # Livine-Speziale states
│   └── asymptotics.py     # Large-j asymptotic formulas
├── run_calculation.py
└── analysis/
```

## Validation
1. Reproduce known results from Donà et al. (2020, 2022)
2. Check unitarity and gauge invariance
3. Verify asymptotic formula against exact integration for intermediate j

## Timeline
- Implementation: 1-2 weeks
- Calculations: 1-2 weeks
- Analysis: 1 week
- Total: 2-4 weeks

## References
- Donà, Fanizza, Sarno (2020): Numerical evaluation of spinfoam amplitudes
- Donà et al. (2022): Asymptotics of Lorentzian spinfoam amplitudes
- Perez (2013): The Spin-Foam Approach to Quantum Gravity (review)
- Engle, Pereira, Rovelli, Livine (EPRL, 2008)
- Freidel, Krasnov (FK, 2008)
