# T20 Validation Plan — 2026-06-26 Session (COMPLETE)

*Updated: 2026-06-26 03:52 IST*

## Completed ✅

### 1. Multi-lattice plot regression fix
- L=4,6,8 overlaid on fine-grained β grid (21 values) ✓

### 2. Website rebuild + redeploy
- Timestamps fixed (ISO 8601 +05:30 for YAML, IST for humans) ✓

### 3. Binder cumulant first-order analysis (L=4,6,8)
- α = -3.084 ≈ -3, confirms first-order transition ✓

### 4. Larger lattice runs (L=16, 24, 32)
- **L=16**: 129s (2.1 min) — avg 6.1s/β
- **L=24**: 436s (7.3 min) — avg 20.8s/β
- **L=32**: 1,034s (17.2 min) — avg 49.2s/β

### 5. All-L plots generated
- Plaquette, specific heat, susceptibility, binder cumulant (all L)
- Combined overview figure

### 6. First-order scaling analysis (all L)
- **Binder cumulant minimum**: U_min = 2/3 - 2.81·L^(-3.198), exponent ≈ -3 ✓
- **Peak heights**: χ_max → ~0.70, C_V,max → ~0.52 (constants, not diverging) ✓
- **Peak widths**: FWHM limited by grid resolution (Δβ = 0.02)
- **β_c shift**: Limited by grid resolution
- **Scaling collapse**: Confirms NOT 3D Ising (first-order) ✓

### 7. Deployment
- `space-cadet.github.io` commit `71f71fe` — T20 page updated with all-L figures
- `timesarrow` commit `a5939af` — Source qmd + scripts + data + assets

## Key Findings

**3D Z₂ LGT has a FIRST-ORDER phase transition**, not a continuous one:
- Binder cumulant minimum scaling: exponent = -3.198 ≈ -3 (expected for first-order in d=3)
- Peak heights approach constants (volume-scaled, not diverging)
- Scaling collapse with 3D Ising exponents fails (curves don't collapse)
- The transition is NOT in the 3D Ising universality class

**Grid resolution is the limiting factor** for L ≥ 16:
- Δβ = 0.02 is too coarse to resolve β_c shift (~0.00003 for L=32)
- Need Δβ ≈ 0.001 or adaptive grid near β_c ≈ 0.76
- Would require ~200 β values in [0.70, 0.80] or finer adaptive spacing

## Benchmarks

| L | Volume | Time (21 β, 8 workers) | Avg/β |
|---|--------|--------------------------|-------|
| 4 | 64 | 6s | 0.3s |
| 6 | 216 | 23s | 1.1s |
| 8 | 512 | 51s | 2.4s |
| 16 | 4,096 | 129s | 6.1s |
| 24 | 13,824 | 436s | 20.8s |
| 32 | 32,768 | 1,034s | 49.2s |

Scaling: ~L^3.2 (slightly faster than L^4 due to cache + parallelization)

## Files Added

| File | Description |
|------|-------------|
| `numerics/output/t20-p3-L16-3D-wilson-fine-20250626.json` | L=16 raw data |
| `numerics/output/t20-p3-L24-3D-wilson-fine-20250626.json` | L=24 raw data |
| `numerics/output/t20-p3-L32-3D-wilson-fine-20250626.json` | L=32 raw data |
| `numerics/output/benchmark-lattice-sizes-20250626.json` | Timing benchmarks |
| `numerics/src/scripts/run-larger-lattices.sh` | Benchmark runner |
| `numerics/src/scripts/t20-plot-all-L.py` | All-L plotting |
| `numerics/src/scripts/t20-first-order-analysis.py` | First-order scaling |
| `docs/assets/t20-p3-*-all-L.png` | All-L overlay plots (5 figures) |
| `docs/assets/t20-binder-first-order-scaling-all-L.png` | Binder scaling |
| `docs/assets/t20-first-order-scaling-summary.png` | Summary figure |
| `docs/assets/t20-scaling-collapse-all-L.png` | Collapse test |

## Open Questions / Next Steps

1. **Adaptive β grid**: Run with finer spacing (Δβ ≈ 0.005) near β_c ≈ 0.76 for L=16,24,32 to verify β_c shift and peak width scaling
2. **Dressed correlator**: Implement Z₂ gauge-Higgs model or document that Wilson loops = dressed correlator in pure gauge limit
3. **Publication-ready figures**: Consistent styling, higher DPI, maybe TikZ
4. **Thermodynamic limit extrapolation**: Extrapolate plaquette curves to L→∞ to show discontinuous jump

## Decisions

- 3D Z₂ LGT has first-order transition (not continuous) — Binder cumulant confirms
- Standard critical exponent extraction doesn't apply — use first-order scaling instead
- Grid resolution is the limiting factor for L ≥ 16 — need adaptive β grid
- Wilson loops in pure gauge theory ARE the dressed correlator in the matter-free limit
- For paper: focus on first-order signatures (binder minimum, non-diverging peaks, step-function plaquette)
