---
task_id: T20-Phase2
title: Sharp Phase Transition in Z₂ LGT — Multi-Lattice Finite-Size Scaling
created: 2026-06-24
status: planned
---

## Problem Statement

T20 Phase 1 produced simulation results for Z₂ LGT on a 2D square lattice (L=8). The figures (plaquette vs β, susceptibility) do **not** show a sharp phase transition. The plaquette smoothly increases from ~0 to ~1, and the susceptibility peak is broad and poorly resolved due to:

1. Only single lattice size (L=8)
2. Sparse β sampling (10 points, only 2–3 near βc)
3. Insufficient statistics near critical region (1000 thermal + 5000 measure sweeps)
4. Only ⟨P⟩ computed — no higher moments (P², P⁴) for susceptibility / Binder cumulant

## Physics Requirements

For a **second-order phase transition** (2D Z₂ Ising universality), the signatures are:

| Observable | Behavior | Finite-Size Scaling |
|-----------|----------|---------------------|
| Specific heat C = β²(⟨P²⟩ − ⟨P⟩²) | Peak height ∝ L^(α/ν) | Diverges at βc |
| Susceptibility χ = L²(⟨P²⟩ − ⟨P⟩²) | Peak height ∝ L^(γ/ν) | Diverges strongly |
| Binder cumulant U = 1 − ⟨P⁴⟩/(3⟨P²⟩²) | Curves for all L cross at βc | Universal crossing |

Critical exponents (2D Ising): α = 0, ν = 1, γ = 7/4

## Plan

### Phase 2A: Higher Observables + Dense β Grid (minutes)

**Simulation parameters:**
- Lattice sizes: L = 8, 16, 32
- β grid: 0.30–0.60 with Δβ = 0.02 (16 points)
- Sweeps: 100k thermal + 500k measure (standard)
- Near βc (0.40–0.50): additional Δβ = 0.01 (11 points)
- Measure every 10 sweeps
- Bin size: 100 for error analysis

**Parallelization:** Run 6–7 (β, L) combinations simultaneously across CPU cores.

**New observables to compute:**
- ⟨P⟩ — average plaquette (already have)
- ⟨P²⟩ — for susceptibility and specific heat
- ⟨P⁴⟩ — for Binder cumulant
- Specific heat C(β, L)
- Susceptibility χ(β, L)
- Binder cumulant U(β, L)
- Jackknife error estimates for all quantities

**Expected output:**
- Raw data JSON with all moments per sweep
- Summary statistics JSON with means and errors
- Plots:
  1. ⟨P⟩ vs β for all L (shows crossover sharpening)
  2. Susceptibility χ vs β for all L (peak grows with L)
  3. Binder cumulant U vs β for all L (crossing at βc)
  4. Specific heat C vs β for all L (peak grows with L)

### Phase 2B: Finite-Size Scaling Collapse (if needed)

**Scaling variables:**
- Horizontal: L^(1/ν)(β − βc) = L(β − 0.4407)
- Vertical susceptibility: L^(−γ/ν)χ = L^(−7/4)χ
- Vertical specific heat: L^(−α/ν)C = C (since α = 0)

**Result:** All curves for different L collapse onto a single universal scaling function.

**Required:** L = 8, 16, 32, 64, 128 with very dense β grid and long runs near βc.

### Phase 2C: Production Quality (if publishing)

- L = 64, 128, 256
- Near βc: 500k thermal + 2M measure sweeps
- Measure every L² sweeps (critical slowing down)
- Autocorrelation time analysis
- Full error budget with jackknife + binning

## GPU Assessment

**Verdict: Not needed for this project.**

| Factor | Assessment |
|--------|------------|
| M2 GPU | 8-core, ~2.6 TFLOPS, Metal framework |
| CUDA | Not available (Apple Silicon) |
| Z₂ Metropolis | Inherently sequential per sweep |
| Lattice size | Even L=128 = 16K sites — too small for GPU advantage |
| Kernel overhead | Would dominate for such small lattices |
| Best GPU use | Batch independent simulations (8 sims in parallel) — same as CPU parallelization |

**CPU parallelization is sufficient:** 6–7 cores running independent simulations gives ~6× speedup with zero complexity. This matches the batch GPU approach without any Metal/MLX bindings.

## Computational Estimates (M2 MacBook Air)

| Phase | L sizes | β points | Sweeps | Time per run | Parallel runs | Total time |
|-------|---------|----------|--------|--------------|---------------|------------|
| 2A | 8, 16, 32 | 27 | 100k + 500k | ~10s | 6 | ~3 min |
| 2B | 8–128 | 40+ | 500k + 2M | ~3 min | 6 | ~30 min |
| 2C | 64–256 | 80+ | 1M + 5M | ~15 min | 6 | ~3 hours |

## Code Changes Required

### ts-quantum (lattice module)

1. **`observables.ts`**: Add `averagePlaquetteMoments(field)` returning `{mean, meanSq, meanFourth}`
2. **`observables.ts`**: Add `binderCumulant(meanSq, meanFourth)` 
3. **`observables.ts`**: Add `specificHeat(mean, meanSq, beta, volume)`
4. **`observables.ts`**: Add `susceptibility(mean, meanSq, volume)`
5. **`monteCarlo.ts`**: Ensure `metropolisSweep` returns acceptance rate for monitoring

### timesarrow/numerics (scripts)

1. **`t20-z2-lgt-phase2.ts`**: Multi-lattice parameter sweep with CPU parallelization
2. **`analysis/plot-phase2.ts`**: Generate all four plots (P, χ, U, C vs β for multiple L)
3. **Update Quarto docs**: Add Phase 2 results to `tasks/t20-z2-lgt.qmd`

## Deliverables

- [ ] ts-quantum observables extended (P², P⁴, Binder, C, χ)
- [ ] Multi-lattice simulation script (L=8,16,32, CPU parallel)
- [ ] Simulation results JSON with all observables
- [ ] 4 plots showing sharp phase transition signatures
- [ ] Updated Quarto numerics page with Phase 2 results
- [ ] Deployed to space-cadet.github.io

## Dependencies

- ts-quantum lattice module (already implemented in Phase 1)
- Bun/Node.js runtime for parallel execution (`Promise.all()` or `Worker` threads)
- Python/matplotlib or Observable Plot for figure generation

## References

- Kogut, J. B. (1979). Rev. Mod. Phys. 51, 659.
- Balian, Drouffe, Itzykson (1975). Phys. Rev. D 11, 2104.
- Binder, K. (1981). Z. Phys. B 43, 119. (Binder cumulant)
- Cardy, J. L. (1988). *Finite-Size Scaling*. North-Holland.
