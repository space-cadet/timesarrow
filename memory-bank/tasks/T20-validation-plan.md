# T20 Validation Plan — 2026-06-26 Session

*Recorded: 2026-06-26 03:10 IST*

## Completed
1. **Multi-lattice plot regression fix** — L=4,6,8 overlaid on fine-grained β grid
2. **Website rebuild + redeploy** — timestamps fixed (ISO 8601 +05:30 for YAML, IST for humans)
3. **Binder cumulant first-order analysis** — α = -3.084 ≈ -3, confirms first-order transition in 3D Z₂ LGT

## In Progress / Next
4. **Dressed correlator analysis** — measure C(r) = ⟨τ₀ ∏_{e∈γ} σ_e τ_r⟩ for various r
   - Confined phase (β < β_c): exponential decay with r
   - Deconfined phase (β > β_c): constant (order parameter)
   - Need to implement in Rust or compute from existing field data
5. **Critical exponent extraction** — fit χ peak heights → ν, γ via finite-size scaling
6. **Phase 2B scaling collapse** — L^(-γ/ν)χ vs L^(1/ν)(β-β_c)
7. **Publication-ready figure formatting** — consistent styling, higher DPI

## Decisions
- 3D Z₂ LGT has first-order transition (not continuous) — Binder cumulant minimum scaling confirms
- Thermodynamic limit: U_∞ = 2/3, β_c = 0.7613
- Dressed correlator is the physical order parameter for confinement
