---
kind: edit_chunk
id: 180915-t20d-ising-reanalysis
created_at: 2026-07-08 18:09:15 IST
task_ids: [T20d, T32]
source_commit: cd1f380
---

#### 18:09:15 IST - T20d: Completed Ising reanalysis of existing 3D Z₂ data
- Created `numerics/src/scripts/t20d-ising-reanalysis.py` — Python reanalysis script using 3D Ising universality assumptions
- Modified `numerics/output/t20d-ising-reanalysis.json` — Summary JSON with extracted (limited) results
- Created figures in `numerics/output/figures/`:
  - `t20d-ising-string-tension.png` — Wilson loop area-law string tension vs β
  - `t20d-ising-perimeter-coeff.png` — Perimeter-law coefficient vs β
  - `t20d-ising-peak-scaling.png` — Susceptibility/specific-heat peak scaling (flagged unreliable)
  - `t20d-ising-binder-crossing.png` — Binder cumulant vs β (flat, no crossing resolved)
  - `t20d-ising-beta-c-extrapolation.png` — Critical β_c extrapolation from peak shift
  - `t20d-ising-data-collapse.png` — Data collapse attempt (blocked by coarse spacing)
  - `t20d-ising-plaquette-smooth.png` — Plaquette vs β showing smooth transition

## Key Findings

1. **Plaquette transition is SMOOTH** — no discontinuity or bimodality. Consistent with continuous (not first-order) transition.

2. **Binder cumulant is FLAT** (~0.666) for L ≥ 16 with no visible crossing. The critical drop to Ising universal value ~0.47 is NOT resolved with 0.02 β spacing.

3. **Peak shifts toward β ≈ 0.76** with increasing L:
   - L=8,16,24: peak at β ≈ 0.74
   - L=32: peak at β ≈ 0.76
   - This shift is consistent with finite-size scaling toward β_c ≈ 0.761

4. **β_c(∞) estimate: 0.750 ± 0.008** — close to literature 0.761 but low. Large uncertainty from coarse spacing.

5. **String tension decreases** approaching critical region, consistent with confinement → deconfinement transition.

## Critical Limitation

The fine-scan data has only **7 β points in [0.70, 0.82] with 0.02 spacing**. This is **too coarse for reliable finite-size scaling exponent extraction**:
- χ_max is NOT monotonic in L (should grow as L^(γ/ν))
- Peak locations are poorly resolved (often stuck at same β value)
- Binder cumulant crossing cannot be identified
- Data collapse fails

## Recommendations for Next Steps

1. **Re-run simulations** with β spacing ≤ 0.005 in [0.74, 0.78] (critical region)
2. **Include L = 48, 64** for better asymptotic scaling
3. **Increase thermalization/measurement** for better statistics at each β
4. **Add larger Wilson loops** (r × c up to L/2) for proper area-law fits
5. **Measure time-series** for autocorrelation analysis

## Conclusion

The existing data is **consistent with a continuous 3D Ising-universality transition** but **cannot reliably extract critical exponents**. The first-order classification was incorrect, but the correction requires new simulations with finer resolution. The manuscript should **not** cite specific exponent values from this dataset.
