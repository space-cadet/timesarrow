# Calculation Plan: Spin Foam Amplitude for j=1/2 Dominance

*Created: 2026-06-24*
*Updated: 2026-06-28*
*Task: T22*

## Overview

Numerically evaluate EPRL/FK spin foam vertex amplitudes to verify j=1/2 dominance, addressing the key weakness identified in peer review.

## Background

The paper assumes j=1/2 edges dominate at the Planck scale. Three arguments are given:
1. Amplitude suppression in spin foam models
2. Entropy counting (combinatorial dominance)
3. Black hole entropy matching

The GPT 5.5 review found argument 2 weak and argument 3 context-specific. A direct spin-foam calculation is needed.

## Why j=1/2 Dominance Is NOT a Given

### The Naive Argument
One might think j=1/2 dominance is obvious because:
- The Wilson action S_W = -β ∑_p Re[U_p] naturally emerges from j=1/2 characters (χ_{1/2}(U_p) = 2 cos θ_p)
- In the Ponzano-Regge / asymptotic limit, higher spins are suppressed by 1/j
- For simple coherent intertwiners, the peakedness favors small spins

### Why It's Actually Nontrivial

**1. FK Vertex Structure**

The Freidel-Krasnov vertex amplitude involves a nontrivial kernel:

```
A_v^{FK}(j₁,j₂,j₃,j₄) = ∫_{SU(2)} ∏_{i=1}^4 dh_i δ(∏_i h_i) ∏_{i=1}^4 D^{j_i}(h_i)
```

The kernel K_j(g₁,g₂,g₃,g₄) depends on:
- The spins j_i
- The Barbero-Immirzi parameter γ
- The intertwiner state (simple vs coherent)

The suppression isn't purely dimensional — it's geometric. The integral over SU(2) elements couples the spins nontrivially.

**2. Intertwiner Multiplicity**

While individual matrix elements scale as ~1/√(2j+1), the number of intertwiners grows with j. For a 4-valent vertex with spin j, the number of intertwiners is:

```
dim(Inv(j⊗j⊗j⊗j)) = Σ_{k=0}^{2j} (2k+1) × {j j k; j j k}
```

This multiplicity factor partially compensates for the per-state suppression.

**3. Coherent State Widths**

Livine-Speziale coherent states have widths that scale as σ ~ j^{-1/2}. For the integral:

```
∫ dg exp(-j (θ - θ₀)² / 2) × D^j(g)
```

The Gaussian width competes with the oscillatory D^j(g), and the net scaling depends on the stationary phase point.

**4. EPRL vs FK Distinction**

The EPRL vertex (which maps SU(2) to SL(2,C)) has different asymptotics:

```
A_v^{EPRL} ~ j^{-3/2} exp(i S_{Regge}[j])   [EPRL]
A_v^{FK} ~ j^{-3/2} exp(i S_{Regge}[j])      [FK, Euclidean]
```

But the prefactors and the effective γ-dependence differ. If the manuscript relies on a specific embedding, the suppression factor matters quantitatively.

**5. Compounding in the Full Path Integral**

A single vertex suppression of 10⁻² becomes 10^{-2N} for N vertices. But:
- The partition function sums over ALL spin assignments
- Entropy factors (number of configurations) compete with amplitude suppression
- The net effect requires careful balance analysis

### What a Single-Vertex Estimate Actually Gives

Even a single-vertex computation provides:
- **Conservative bound:** If one vertex suppresses higher spins by factor X, the full lattice suppresses by at least X^N
- **Order-of-magnitude guidance:** Is the suppression 10⁻¹ (weak) or 10⁻⁴ (strong)?
- **Model discrimination:** EPRL vs FK may give different suppression patterns

## Two-Path Strategy

### Path 1: Quick Estimate (1-2 days)

**Scope:** Single 4-valent vertex, j=1/2 vs j=1, one model (FK)

**Method:**
1. Write down FK vertex formula explicitly
2. Monte Carlo over SU(2) with ~10⁶ samples
3. Compare |A_v(½,½,½,½)|² vs |A_v(1,1,1,1)|²
4. Compute ratio with error bars

**Expected precision:** ~10% statistical error
**Deliverable:** "|A_v(j=1)|² / |A_v(j=½)|² ≈ 10^{-α±Δα}"

**When sufficient:** If the manuscript presents the Wilson action as an approximation ("in the j=1/2 sector...")

### Path 2: Full Systematic Study (1-2 weeks)

**Scope:** Multiple spins, both models, γ-dependence, asymptotic verification

**Method:**
1. Cross-repo implementation (ts-quantum core → spin-foam extension)
2. Systematic scan: j = ½, 1, 3/2, 2, 5/2, 3
3. Both FK and EPRL vertices
4. Multiple γ values (0.1, 0.237, 0.5, 1.0)
5. Asymptotic formula verification against Donà et al. (2022)

**Expected precision:** <1% statistical error
**Deliverable:** Full parameter scan with plots, exponent extraction, model comparison

**When needed:** If the manuscript claims the Wilson action emerges *uniquely* from LQG without truncation

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

**Path 1 (Quick Estimate):**
- Implementation: 1 day
- Calculation: 2-4 hours (Monte Carlo)
- Analysis: 2-3 hours
- Total: 1-2 days

**Path 2 (Full Study):**
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
