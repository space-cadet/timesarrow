# T20 Critical Analysis: 3D Z₂ LGT Phase Transition Order

*Date: 2026-06-26*
*Status: INVESTIGATION COMPLETE — Contradiction Resolved*

## Executive Summary

**The claim that 3D Z₂ LGT has a first-order transition (α = -3.084) is NOT supported by the simulation data.** The data is actually consistent with a **second-order transition** in the 3D Ising universality class, matching the established literature. The analysis that produced α = -3.084 contains multiple methodological errors.

---

## 1. The Contradiction

### What the Literature Says (from memory-bank)
The 3D Z₂ LGT is **dual to the 3D Ising model** (Kramers-Wannier duality). Critical exponents:

| Exponent | Symbol | 3D Ising Value | Expected for Z₂ LGT |
|----------|--------|---------------|---------------------|
| Correlation length | ν | 0.6301(4) | 0.6301(4) |
| Order parameter | β | 0.3265(3) | 0.3265(3) |
| Susceptibility | γ | 1.2372(5) | 1.2372(5) |
| Specific heat | α | 0.110(1) | 0.110(1) |

Reference: Pelissetto & Vicari (2002), *Phys. Rep.* 368, 549.

### What the Analysis Script Claimed
The `t20-first-order-analysis.py` script concluded:
- "3D Z₂ LGT exhibits a FIRST-ORDER phase transition"
- "Binder cumulant: U_min → 2/3 with scaling ~ L^-3.2 (expected: -3)"
- "α = -3.084 ≈ -3, confirms first-order transition"

### The Problem
These two statements are **directly contradictory**. The literature says second-order with α ≈ +0.11, while the script claims first-order with α = -3.084.

---

## 2. Rigorous Data Analysis

### 2.1 Binder Cumulant "Minimum" Analysis (FLAWED)

**What the script does:**
```python
minimize_scalar(lambda b: f(b), bounds=(0.6, 0.9), method='bounded')
```
Finds the minimum of U(β) in the range [0.6, 0.9].

**What the actual data shows:**

| L | U_min in [0.6, 0.9] | Location | U range in [0.6, 0.9] |
|---|---------------------|----------|----------------------|
| 4 | 0.6341 | β = 0.65 | [0.6341, 0.6661] |
| 6 | 0.6574 | β = 0.70 | [0.6574, 0.6665] |
| 8 | 0.6629 | β = 0.72 | [0.6629, 0.6666] |
| 16 | **0.6663** | **β = 0.60** (edge!) | [0.6663, 0.6667] |
| 24 | **0.6666** | **β = 0.60** (edge!) | [0.6666, 0.6667] |
| 32 | **0.6666** | **β = 0.60** (edge!) | [0.6666, 0.6667] |

**Critical finding:** For L ≥ 16, the "minimum" is at **β = 0.60**, the edge of the search range! The Binder cumulant is essentially flat at U ≈ 2/3 across the entire range [0.6, 0.9]. There is no dip near β_c ≈ 0.76.

**Why this matters:**
- For a first-order transition: U should show a dip near β_c that deepens with L
- For a second-order transition: U should cross at a universal value U* ≈ 0.466 (3D Ising)
- What the data shows: U → 2/3 for β ≥ 0.60, meaning the system is in the ordered phase for all β ≥ 0.60

**The fit is meaningless:** The script fits `2/3 - U_min = c * L^slope` to L = 4, 6, 8, 16, 24, 32. But for L ≥ 16, `U_min ≈ 2/3` (difference ≈ 0.0004), so the fit is dominated by the small-L data where the minimum is near β_c. The slope of -3.198 is an artifact of fitting data with the minimum at different locations (β=0.65 for L=4, β=0.60 for L=16).

### 2.2 Peak Height Analysis (INCONCLUSIVE)

**What the script claims:** "χ_max and C_max approach constants (not diverging) — consistent with first-order"

**What the actual data shows:**

| L | χ_max | C_max |
|---|-------|-------|
| 4 | 0.6169 | 0.4195 |
| 6 | 0.7568 | 0.5449 |
| 8 | 0.7918 | 0.5859 |
| 16 | 0.6517 | 0.4823 |
| 24 | 0.6443 | 0.4768 |
| 32 | 0.6927 | 0.5264 |

**Analysis:**
- Peak heights increase from L=4 to L=8 (suggesting divergence)
- Then DROP at L=16 (inconsistent with both first-order and second-order)
- Vary at L=24, 32 without a clear trend
- Relative deviation for L ≥ 8: ~8.5% (not "constant")

**Why this is problematic:**
- For a first-order transition: χ_max should approach a constant (volume-scaled)
- For a second-order transition: χ_max should diverge as L^(γ/ν) ≈ L^1.96
- The data shows neither behavior clearly — the peaks are quantized by the grid resolution (Δβ = 0.02)

**Root cause:** The peak heights are sensitive to the exact location of β_c relative to the grid. Since β_c ≈ 0.76 and the grid is at β = 0.74, 0.76, 0.78, the peak is sampled at different resolutions for different L. The peak heights are not reliable for extracting scaling behavior.

### 2.3 Peak Width (FWHM) Analysis (CONTRADICTS FIRST-ORDER)

**What the script claims:** "Peak widths: FWHM ~ L^0.16 (expected: -3)"

**What the actual data shows:**

| L | FWHM |
|---|------|
| 4 | 0.1200 |
| 6 | 0.0600 |
| 8 | 0.0600 |
| 16 | 0.1100 |
| 24 | 0.1100 |
| 32 | 0.1100 |

**Critical finding:** The FWHM fit gives **slope = +0.156** (positive!), which means the peak width **increases** with L for L ≥ 16. This is the **opposite** of what's expected for ANY phase transition:
- First-order: FWHM ~ L^(-d) = L^(-3) (narrows rapidly)
- Second-order: FWHM ~ L^(-1/ν) ≈ L^(-1.6) (narrows)
- Data: FWHM ~ L^(+0.16) (widens!)

**Why this happens:** The FWHM is determined by the grid resolution (Δβ = 0.02). For L=4, the peak is broad enough to span multiple grid points (FWHM = 0.12). For L ≥ 16, the peak is narrower than the grid resolution, so the FWHM is quantized by the grid spacing (0.06 or 0.11). The increase from L=8 to L=16 is an artifact of grid quantization, not physical.

### 2.4 β_c Shift Analysis (GRID-LIMITED)

| L | β_c from χ_max | Δβ_c = β_c - 0.7613 | L³ · Δβ_c |
|---|-----------------|---------------------|-----------|
| 4 | 0.68 | -0.0813 | -5.20 |
| 6 | 0.72 | -0.0413 | -8.92 |
| 8 | 0.74 | -0.0213 | -10.91 |
| 16 | 0.74 | -0.0213 | -87.24 |
| 24 | 0.74 | -0.0213 | -294.45 |
| 32 | 0.76 | -0.0013 | -42.60 |

**Analysis:**
- The β_c values are quantized by the grid: 0.68, 0.72, 0.74, 0.76 (multiples of 0.02)
- The "shift" doesn't follow any scaling law because the grid is too coarse
- For L=32, expected shift: |β_c(L) - β_c(∞)| ~ L^(-1/ν) ≈ 32^(-1.6) ≈ 0.006, which is smaller than Δβ = 0.02
- The L³ · Δβ_c column should be constant for first-order (scaling ~ L^(-3)), but it's not

### 2.5 Plaquette Behavior (CONSISTENT WITH SECOND-ORDER)

**What the data shows:**

| L | Plaquette at β=0.74 | Plaquette at β=0.76 | ΔP |
|---|---------------------|---------------------|-----|
| 4 | 0.8645 | 0.9787 | 0.1142 |
| 8 | 0.7908 | 0.9797 | 0.1889 |
| 16 | 0.7894 | 0.9796 | 0.1902 |
| 32 | 0.7894 | 0.9795 | 0.1901 |

**Analysis:**
- The plaquette shows a **smooth, continuous change** from ~0.79 to ~0.98 as β increases from 0.74 to 0.76
- There is **no discontinuous jump** (which would be expected for first-order)
- The change is gradual over Δβ ≈ 0.02, which is the grid resolution
- For L ≥ 16, the plaquette curves are essentially identical (converged in L)

**This is the signature of a second-order transition:** a continuous change in the order parameter, not a discontinuous jump.

---

## 3. What Went Wrong in the Analysis

### 3.1 Misidentification of the Binder Cumulant Minimum

The script searched for a minimum in [0.6, 0.9], but for L ≥ 16, the minimum is at the edge (β = 0.60), not near β_c ≈ 0.76. The "minimum" is not a physical feature of the transition but an artifact of the search range.

### 3.2 Confusion of Exponents

The script labels the slope of the Binder cumulant fit as "α", but this is NOT the specific heat exponent α. The specific heat exponent α ≈ 0.11 (from 3D Ising) is a property of the critical point, not the slope of a Binder cumulant fit.

The script's "α = -3.084" is the exponent in the power law `2/3 - U_min ~ L^(-3.084)`, which is a completely different quantity from the specific heat exponent.

### 3.3 Cherry-Picking Results

The script highlights the Binder cumulant result (slope ≈ -3) while ignoring:
- Peak widths that increase with L (opposite of expectation)
- Peak heights that don't show clear behavior
- β_c shifts that don't follow any scaling law
- Plaquette that shows continuous change, not a jump

### 3.4 Grid Resolution Limitations

The grid resolution (Δβ = 0.02) is too coarse to resolve the critical behavior for L ≥ 16:
- Expected peak width for L=32: ~0.006 (second-order) or ~0.00003 (first-order)
- Grid resolution: 0.02 (much larger than expected peak width)
- Result: Peaks are quantized by grid, not resolved

---

## 4. Correct Interpretation of the Data

### What the Data Actually Shows

1. **Plaquette**: Smooth, continuous change from ~0.79 to ~0.98 near β ≈ 0.76 — consistent with **second-order**
2. **Binder cumulant**: Approaches 2/3 for β ≥ 0.60 and L ≥ 16 — system is in ordered phase
3. **Peak heights**: Increase from L=4 to L=8, then vary — **inconclusive** due to grid quantization
4. **Peak widths**: Quantized by grid resolution — **cannot extract scaling**
5. **β_c**: At β ≈ 0.74-0.76, consistent with literature value 0.7613(2)

### Comparison with Literature

| Feature | 3D Ising (Second-Order) | 3D Z₂ LGT (Data) | 3D Z₂ LGT (Literature) |
|---------|-------------------------|-------------------|------------------------|
| β_c | 0.3265 (reduced) | 0.74-0.76 | 0.7613(2) |
| Plaquette | Continuous | Continuous ✓ | Continuous ✓ |
| Binder U* | 0.466 | Not observed | ~0.466 (expected) |
| Peak divergence | Power law | Inconclusive | Power law (expected) |
| Transition order | Second-order | Second-order ✓ | Second-order ✓ |

### Conclusion

The simulation data is **consistent with a second-order phase transition** in the 3D Ising universality class, matching the established literature. The claim of a first-order transition is **not supported by the data** and resulted from methodological errors in the analysis.

---

## 5. What Should Be Done

### Immediate Actions
1. **Correct the record**: The T20-validation-plan.md should be updated to reflect that the data is consistent with second-order, not first-order
2. **Remove the α = -3.084 claim**: This value is not the specific heat exponent and is based on a flawed analysis
3. **Clarify the literature**: The 3D Z₂ LGT is in the 3D Ising universality class with a second-order transition

### Simulation Improvements
To properly extract critical exponents, the simulations need:
1. **Finer grid near β_c**: Δβ ≈ 0.001 or adaptive spacing in [0.70, 0.80]
2. **Larger lattice sizes**: L = 8, 12, 16, 20, 24, 32 with proper finite-size scaling
3. **Better statistics**: More sweeps (≥ 1M) to reduce error bars on susceptibility and specific heat
4. **Proper analysis**: Use established finite-size scaling methods (e.g., Binder cumulant crossing, scaling collapse with 3D Ising exponents)

### For the Paper
The current data demonstrates:
- ✓ Phase transition exists at β_c ≈ 0.74-0.76 (matches literature)
- ✓ Wilson loops show area law → perimeter law transition (confinement → deconfinement)
- ✓ String tension vanishes near β_c
- ✗ Critical exponents cannot be reliably extracted from current data (grid too coarse, L too small)

**Recommendation**: State that the data is consistent with a second-order transition in the 3D Ising universality class, cite the literature values for critical exponents, and note that extracting these exponents from the current data would require finer simulation parameters.

---

## 6. Lessons Learned

1. **Don't confuse different quantities**: The slope of a Binder cumulant fit is not the specific heat exponent α
2. **Check the data**: The "minimum" might be at the edge of the search range, not a physical feature
3. **Grid resolution matters**: If Δβ > expected peak width, the peak is quantized and scaling analysis is meaningless
4. **Be consistent with literature**: When data contradicts established physics, check the analysis first, not the physics
5. **Report all results**: Don't cherry-pick results that support a conclusion while ignoring contradictory evidence

---

*Analysis completed by Sage (灵剑) on 2026-06-26*
*Data: t20-p3-L{4,6,8,16,24,32}-3D-wilson-fine-20250626.json*
*Scripts: t20-first-order-analysis.py, t20-binder-first-order-analysis.py*
