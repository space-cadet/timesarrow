# T20-Phase3b: Critical Exponent Extraction from 3D Z₂ LGT

*Created: 2026-06-26*
*Status: 🔴 NOT STARTED — Blocked by implementation requirements*

## Objective

Extract critical exponents (ν, β, γ, α) from the 3D Z₂ LGT simulation data to confirm the universality class. This is a dedicated finite-size scaling study that requires substantially finer simulation parameters than the current T20-Phase3 data collection.

## Background

T20-Phase3 collected data at L = 4, 6, 8, 16, 24, 32 with Δβ = 0.02 spacing. This data is sufficient to demonstrate:
- ✓ Phase transition exists at β_c ≈ 0.74–0.76
- ✓ Wilson loops show area law → perimeter law transition
- ✓ String tension vanishes near β_c

But **insufficient** to extract critical exponents because:
- Grid resolution (Δβ = 0.02) is much larger than the peak width (~0.006 for L=32)
- Peak heights are quantized by grid, not resolved
- Only 3 sizes (L=4,6,8) have well-resolved peaks; L≥16 peaks are at the same grid points
- No measurement of autocorrelation time (error bars unreliable)
- Order parameter is plaquette (not Polyakov loop)

## Requirements (Minimum vs Ideal)

### 1. Lattice Sizes

| Level | Sizes | Purpose | Status |
|-------|-------|---------|--------|
| **Minimum** | L = 8, 12, 16, 20, 24, 32 | FSS power law fit with 6 points | 🔴 Not run |
| **Ideal** | L = 8, 12, 16, 20, 24, 32, 48, 64 | FSS with corrections to scaling | 🔴 Not run |
| **Current** | L = 4, 6, 8, 16, 24, 32 | Insufficient for exponent extraction | ✅ Done |

**Why L ≥ 48:** Corrections to scaling (ω ≈ 0.8) are significant for L < 32. Without L ≥ 48, fitting ν gives ~0.55 instead of ~0.63.

### 2. β Grid Near β_c

| L | Current Δβ | Needed Δβ | β Range | Points |
|---|------------|-----------|---------|--------|
| 8 | 0.02 | 0.005 | [0.70, 0.82] | 25 |
| 16 | 0.02 | 0.003 | [0.72, 0.80] | 27 |
| 32 | 0.02 | 0.002 | [0.74, 0.78] | 21 |
| 48 | — | 0.0015 | [0.75, 0.77] | 14 |
| 64 | — | 0.001 | [0.75, 0.77] | 21 |

**Why finer grid:** Expected peak width for L=32 is ~L^(-1/ν) ≈ 32^(-1.6) ≈ 0.006. Current Δβ = 0.02 is **3× wider** than the peak. The peak is sampled at only 2-3 points, making height and position unreliable.

### 3. Sweeps per β Configuration

| Phase | Thermalization | Measurement | Total | Independent Samples (τ ≈ L²) |
|-------|-------------|-------------|-------|-------------------------------|
| **Current** | 100k | 100k | 200k | ~200 (L=8), ~30 (L=32) |
| **Minimum** | 500k | 1M | 1.5M | ~1,500 (L=8), ~250 (L=32) |
| **Ideal** | 1M | 5M | 6M | ~6,000 (L=8), ~1,000 (L=32) |

**Why more sweeps:** Near β_c, autocorrelation time τ_int ~ L^z with z ≈ 2.0 (Metropolis). Error on susceptibility scales as 1/√(N_sweeps/τ_int). With 100k sweeps at L=32, you have only ~30 independent samples → ~18% error. Need ≥250 independent samples for <6% error.

### 4. Independent Runs

| Level | Runs per (L, β) | Purpose |
|-------|----------------|---------|
| **Current** | 1 | No error estimate on peaks |
| **Minimum** | 3 | Estimate variance of χ_max, β_c |
| **Ideal** | 5 | Reliable Jackknife/bootstrap error bars |

**Why multiple runs:** Each run is a Markov chain with different random seed. Variance across runs gives true error, not just the statistical error from a single chain.

### 5. Observables to Measure

#### Current (Plaquette-based)
- Plaquette ⟨P⟩
- Susceptibility: χ = L³ (⟨P²⟩ - ⟨P⟩²) — this is "energy" susceptibility, not order parameter susceptibility
- Specific heat: C = L³ (⟨E²⟩ - ⟨E⟩²) — energy fluctuations
- Binder cumulant: U = 1 - ⟨P⁴⟩/(3⟨P²⟩²) — plaquette-based, not standard for deconfinement

#### Needed (Polyakov loop-based)
- **Polyakov loop P(L)**: ⟨∏_links U⟩ along a closed temporal loop — true order parameter for deconfinement
- **Order parameter susceptibility**: χ_P = L³ (⟨P²⟩ - ⟨P⟩²)
- **Binder cumulant**: U_P = 1 - ⟨P⁴⟩/(3⟨P²⟩²) — standard for deconfinement transition
- **Correlation length**: ξ from ⟨P(0)P(r)⟩ decay — extract ν directly
- **String tension σ**: From Wilson loops W(γ) ~ exp(-σ·Area) — independent check

**Why Polyakov loop:** The plaquette is not the order parameter for the deconfinement transition. The Polyakov loop is the standard order parameter for Z_N gauge theories. The susceptibility from plaquette variance is not the same as the order parameter susceptibility.

#### Implementation in Rust
```rust
// Add to rust-lattice/src/lib.rs

/// Polyakov loop: product of temporal links along a closed loop
pub fn polyakov_loop(&self, x: usize, y: usize, z: usize) -> i8 {
    let mut product = 1i8;
    for t in 0..self.L {
        let idx = self.link_index(x, y, z, t, 3); // temporal direction = 3
        product *= self.links[idx];
    }
    product
}

/// Average Polyakov loop magnitude (order parameter)
pub fn average_polyakov(&self) -> f64 {
    let mut sum = 0.0;
    for x in 0..self.L {
        for y in 0..self.L {
            for z in 0..self.L {
                sum += self.polyakov_loop(x, y, z).abs() as f64;
            }
        }
    }
    sum / (self.L * self.L * self.L) as f64
}
```

### 6. Analysis Methods

#### Method A: Binder Cumulant Crossing (Primary)
1. Compute U_L(β) for each L
2. Find crossing point U* where U_L(β) = U_L'(β) for different L, L'
3. For 3D Ising: U* ≈ 0.466
4. Fit U_L(β_c) - U* ~ L^(-1/ν) to extract ν

**Expected result:** If ν = 0.630, then U_L(β_c) - U* should scale as L^(-1/0.630) ≈ L^(-1.59)

#### Method B: Scaling Collapse (Cross-check)
1. Plot L^(-β/ν) ⟨P⟩ vs L^(1/ν)(β - β_c) for trial ν, β values
2. Find the collapse that gives the straightest lines (minimize χ²)
3. For 3D Ising: β ≈ 0.326, ν ≈ 0.63

**Expected result:** If correct exponents are used, all L curves collapse onto a single universal function.

#### Method C: Peak Height Scaling (Cross-check)
1. χ_max ~ L^(γ/ν) → log χ_max vs log L has slope γ/ν
2. C_max ~ L^(α/ν) → log C_max vs log L has slope α/ν
3. Need: γ/ν ≈ 1.237/0.630 ≈ 1.96, α/ν ≈ 0.110/0.630 ≈ 0.17

**Expected result:** For 3D Ising, χ_max should increase as L^1.96, C_max should increase weakly as L^0.17.

#### Method D: β_c Shift (Cross-check)
1. β_c(L) - β_c(∞) ~ L^(-1/ν)
2. Fit β_c from peak position vs L
3. Extract ν and β_c(∞)

**Expected result:** β_c(∞) ≈ 0.7613, slope gives 1/ν ≈ 1.59.

### 7. Corrections to Scaling

For L < 32, **leading corrections** to scaling are significant:
- χ_max = a·L^(γ/ν) · (1 + b·L^(-ω) + ...)
- ω ≈ 0.8 (correction exponent for 3D Ising)

**Without corrections:** Fitting L = 8, 16, 32 gives ν ≈ 0.55 (wrong by 13%)
**With corrections:** Fitting L = 8, 16, 32, 48, 64 gives ν ≈ 0.63 (correct)

**Implementation:** Use 3-parameter fit:
```python
def fit_with_corrections(L, chi_max, gamma_over_nu, omega, a, b):
    return a * L**gamma_over_nu * (1 + b * L**(-omega))
```

### 8. Autocorrelation Analysis

**Current:** Not measured. Error bars are σ/√N where N is total sweeps, not independent samples.

**Needed:** Measure integrated autocorrelation time τ_int for:
- Plaquette (or Polyakov loop)
- Susceptibility
- Energy

**Implementation:**
```python
def integrated_autocorrelation(observable):
    """
    Compute τ_int = 0.5 + Σ C(t)/C(0) from t=1 to t_cutoff
    where C(t) = <O(0)O(t)> - <O>^2
    """
    n = len(observable)
    mean = np.mean(observable)
    
    # Compute autocorrelation
    C = np.correlate(observable - mean, observable - mean, mode='full')
    C = C[n-1:] / n  # Keep only t ≥ 0
    C = C / C[0]  # Normalize
    
    # Find cutoff where C(t) < 0 or C(t) < 2/√n
    cutoff = np.where((C < 0) | (C < 2/np.sqrt(n)))[0]
    if len(cutoff) > 0:
        t_cut = cutoff[0]
    else:
        t_cut = n // 4
    
    # Compute τ_int
    tau_int = 0.5 + np.sum(C[1:t_cut])
    return tau_int

# Effective independent samples
N_eff = N_sweeps / tau_int
error = np.std(observable) / np.sqrt(N_eff)
```

**Why this matters:** If you report χ_max = 0.7918 ± 0.0005 but the true error is ±0.05 (because τ_int = 1000 and you only have 100 independent samples), the error bar is meaningless.

## Estimated Compute Cost

| Task | Current | Minimum | Ideal |
|------|---------|---------|-------|
| L=8, fine grid | 10 min | 10 min | 20 min |
| L=16, fine grid | 30 min | 30 min | 60 min |
| L=32, fine grid + more sweeps | 60 min | 60 min | 120 min |
| L=48, fine grid | — | 90 min | 180 min |
| L=64, fine grid | — | — | 300 min |
| Multiple runs (×3) | — | ×3 | ×5 |
| Analysis | — | 2 hours | 4 hours |
| **Total per config** | 17 min | 6-8 hours | 20+ hours |

**Note:** All runs are embarrassingly parallel. With 8 cores, you can run all β points simultaneously. The actual wall-clock time is roughly the time for a single β point.

## Deliverables

1. **Critical exponents table:**
| Exponent | Value | Error | Literature | Agreement |
|----------|-------|-------|------------|-----------|
| ν | ? | ? | 0.6301(4) | ? |
| β | ? | ? | 0.3265(3) | ? |
| γ | ? | ? | 1.2372(5) | ? |
| α | ? | ? | 0.110(1) | ? |
| η | ? | ? | 0.0364(5) | ? |

2. **Scaling collapse plots:** All L curves collapse onto single universal function
3. **Binder cumulant crossing plot:** U_L(β) for all L showing crossing at U* ≈ 0.466
4. **Peak scaling plots:** χ_max, C_max vs L with power law fits
5. **β_c convergence plot:** β_c(L) vs L with L^(-1/ν) fit
6. **Autocorrelation time plot:** τ_int vs L showing τ_int ~ L^z
7. **Comparison table:** Our values vs. literature (Pelissetto & Vicari 2002, Creutz et al. 1979)

## Blockers

| Blocker | Impact | Resolution |
|---------|--------|------------|
| No Polyakov loop in Rust code | Cannot measure true order parameter | Add to rust-lattice/src/lib.rs |
| No autocorrelation measurement | Error bars unreliable | Add to analysis script |
| No fine β grid | Peaks quantized, exponents unreliable | Re-run with Δβ = 0.001-0.005 |
| No L ≥ 48 | Corrections to scaling significant | Add L=48, 64 (if memory allows) |
| No multiple independent runs | No variance estimate | Run 3× per (L, β) |
| No corrections-to-scaling fit | ν biased low | Implement 3-parameter fit |

## Recommended Next Steps

1. **Add Polyakov loop to Rust code** (~1 hour)
2. **Add autocorrelation measurement** (~1 hour)
3. **Run L=8, 16, 32 with fine grid and more sweeps** (~3 hours wall-clock with 8 cores)
4. **Run L=48, 64 if possible** (~2-3 hours additional)
5. **Implement 4 analysis methods** (~2 hours)
6. **Extract exponents and compare with literature** (~1 hour)
7. **Generate publication-ready figures** (~2 hours)

**Total estimated time:** ~12-15 hours of work (much of it parallelizable compute)

## References

- Pelissetto, A. & Vicari, E. (2002). "Critical Phenomena and Renormalization-Group Theory." *Phys. Rep.* 368, 549.
- Creutz, M., Jacobs, L., & Rebbi, C. (1979). "Monte Carlo Computations in Lattice Gauge Theories." *Phys. Rev. D* 20, 1915.
- Ferrenberg, A. M. & Landau, D. P. (1991). "Critical behavior of the three-dimensional Ising model: A high-resolution Monte Carlo study." *Phys. Rev. B* 44, 5081.
- Hasenbusch, M. (2010). "Finite size scaling study of lattice models in the three-dimensional Ising universality class." *Phys. Rev. B* 82, 174433.

## Decision Log

**2026-06-26:** Current T20-Phase3 data is sufficient for demonstrating the phase transition and Wilson loop behavior, but insufficient for critical exponent extraction. A dedicated FSS study is needed if we want to confirm the universality class from first principles. For the paper, citing literature values and stating consistency is the pragmatic approach.

---

*Task created by Sage (灵剑) on 2026-06-26*
*Based on critical analysis in t20-critical-analysis.md*