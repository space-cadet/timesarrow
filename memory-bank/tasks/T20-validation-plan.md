# T20 Validation Plan — 2026-06-26 Session

*Updated: 2026-06-26 03:12 IST*

## Completed ✅

1. **Multi-lattice plot regression fix** — L=4,6,8 overlaid on fine-grained β grid (21 values)
2. **Website rebuild + redeploy** — timestamps fixed (ISO 8601 +05:30 for YAML, IST for humans)
3. **Binder cumulant first-order analysis** — α = -3.084 ≈ -3, confirms first-order transition in 3D Z₂ LGT. U_∞ = 0.6697 within 0.5% of 2/3.
4. **Critical exponent extraction (preliminary)** — Attempted with L=4,6,8; all exponents off due to small L. Documented as limitation.
5. **Scaling collapse test** — Used literature 3D Ising exponents (ν=0.630, γ=1.237); poor collapse with L=4,6,8 confirms need for larger lattices.

## Deployed

- `space-cadet.github.io` commit `adf8829` — T20 page updated with new sections
- `timesarrow` commit `6c0a9f2` — Source qmd + scripts + assets

## Next Steps (Need L ≥ 16)

6. **Critical exponents (proper)** — Run L=16, 24, 32 in Rust (~seconds each), then re-fit
7. **Scaling collapse (proper)** — With L=16, 24, 32, test if curves collapse onto universal function
8. **Dressed correlator** — Option A: Document that Wilson loops = dressed correlator in pure gauge limit. Option B: Implement Z₂ gauge-Higgs model with matter fields τ.

## Decisions

- 3D Z₂ LGT has first-order transition (not continuous) — Binder cumulant minimum scaling confirms with α = -3.084 ≈ -3
- Thermodynamic limit: U_∞ = 2/3, β_c = 0.7613
- L=4,6,8 insufficient for critical exponent extraction — need L ≥ 16 for asymptotic finite-size scaling
- Wilson loops in pure gauge theory ARE the dressed correlator in the matter-free limit
- Dressed correlator with matter fields (τ) requires extending to Z₂ gauge-Higgs model

## Files Added

| File | Description |
|------|-------------|
| `numerics/src/scripts/t20-binder-first-order-analysis.py` | Binder minimum + scaling analysis |
| `numerics/src/scripts/t20-binder-crossing-analysis.py` | First attempt (crossing, not applicable) |
| `numerics/src/scripts/t20-critical-exponents.py` | Peak height fitting (preliminary) |
| `numerics/src/scripts/t20-scaling-collapse.py` | Universality class test |
| `docs/assets/t20-binder-first-order.png` | Annotated binder plot |
| `docs/assets/t20-binder-first-order-scaling.png` | Log-log scaling plot |
| `docs/assets/t20-critical-exponents.png` | Exponent fits |
| `docs/assets/t20-scaling-collapse.png` | Collapse test |

## Open Questions

- Should we implement the Z₂ gauge-Higgs model (with matter fields τ) for the dressed correlator?
- Or document that Wilson loops suffice for the pure gauge theory paper?
- Larger lattices (L=16, 24, 32) — run now or defer to next session?
