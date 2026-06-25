# T20 Missing Observables Gap Analysis

*Created: 2026-06-26 00:30:00 IST*
*Last Updated: 2026-06-26 01:21:00 IST*

## Context

T20 (Z₂ Lattice Gauge Theory Monte Carlo Simulation) was marked COMPLETE on 2026-06-25 after data collection for all three phases. However, a gap analysis on 2026-06-26 revealed that key physics observables necessary to demonstrate the confinement-deconfinement transition were never computed.

## Data Collection Status

| Phase | Lattice | L values | Sweeps | Status |
|-------|---------|----------|--------|--------|
| Phase 1 | 2D square | L=16 | 100k | ✅ Data collected |
| Phase 2 | 2D square | L=8,12,16,20,24 | 200k | ✅ Data collected |
| Phase 3 | 3D cubic | L=4,6,8 | 100k | ✅ Data collected |

## Missing Observables by Phase

### Phase 1 (2D Square Lattice, L=16)

**Raw data**: `numerics/output/t20-phase1-worker-L16.json` (11 β values, ⟨P⟩, χ, C, U)

**Missing**:
1. **Wilson loop W(γ)** for loop sizes L = 4, 6, 8, 10, 12
   - Need: W(γ) as function of loop perimeter/area for each β
   - Physics: Demonstrates perimeter law (weak coupling) vs area law (strong coupling)
   
2. **Critical exponents** (ν ≈ 1, γ ≈ 1.75 for 2D Ising)
   - Need: Fit χ ~ |β - β_c|^(-γ) near critical point
   - Need: Finite-size scaling analysis

3. **Publication-ready figures**

### Phase 2 (Finite-Size Scaling, L=8,12,16,20,24)

**Raw data**: `numerics/output/t20-p2-L*.json` (5 files, dense β grid)

**Missing**:
1. **Scaling collapse plot**
   - Need: L^(-γ/ν) χ vs L^(1/ν)(β - β_c) for all L on single curve
   - Need: Determine optimal β_c, γ, ν via data collapse

2. **Binder cumulant crossing**
   - Need: U_L(β) vs β for all L, identify crossing point β_c(L)
   - Need: Extrapolate β_c(L) → β_c(∞)

3. **Correlation length ξ vs L at β_c**
   - Need: Extract ξ from correlation function or second-moment method

### Phase 3 (3D Cubic Lattice, L=4,6,8)

**Raw data**: `numerics/output/t20-p3-L*.json` (3 files, 10 β values)

**Missing**:
1. **Wilson loops** (area law vs perimeter law)
   - Need: W(γ) for rectangular loops of size R×R and R×T
   - Need: log W vs area (strong coupling) and log W vs perimeter (weak coupling)

2. **String tension σ(L)**
   - Need: Extract from W(γ) ~ exp(-σ · Area) at strong coupling
   - Need: σ(β) as function of β, show vanishing at β_c

3. **Critical exponents** (ν ≈ 0.63, β ≈ 0.33 for 3D Ising)
   - Need: Finite-size scaling analysis with limited L values

### Implementation Notes (CORRECTED 2026-06-26)

**Wilson loop computation**:
- ts-quantum has `wilsonLoop()` and `averageWilsonLoop()` in `src/lattice/observables.ts`
- **CRITICAL: Rust code (`rust-lattice/src/lib.rs`) has NO Wilson loop implementation**
- **CRITICAL: Simulation outputs only contain plaquette averages, NOT raw link configurations**
- Raw configurations were NOT saved during simulation runs
- **Therefore: Cannot compute Wilson loops from existing data — MUST re-run simulations**
- **Step 1**: Add `wilson_loop()` and `average_wilson_loop()` to `rust-lattice/src/lib.rs`
- **Step 2**: Modify `measure()` to track W(γ) for multiple loop sizes during measurement sweeps
- **Step 3**: Re-run Phase 1 (2D) and Phase 3 (3D) simulations with Wilson loop measurements

**Estimated time for Rust implementation + re-runs**: ~2-3 hours

**Critical exponents**:
- Need fitting scripts (Python or TypeScript) to extract exponents from scaling behavior
- Can use existing Phase 2 data — no new simulation needed for exponent extraction
- **However**: Wilson loops must be computed first for complete analysis

**Scaling plots**:
- Phase 2 data is complete for scaling collapse plots
- Need plotting and fitting scripts only

## Why This Matters

## Why This Matters

The central claim of the paper is that the arrow of time emerges from a confinement-deconfinement transition in Z₂ gauge theory. Without Wilson loops:
- We cannot demonstrate area law (signature of confinement)
- We cannot demonstrate perimeter law (signature of deconfinement)
- We cannot extract string tension σ as an order parameter

The raw data exists. The missing piece is analysis code to compute these observables from the existing configurations.

## Next Steps

Priority order:
1. Wilson loop measurement for Phase 3 (3D — most critical for confinement claim)
2. Wilson loop measurement for Phase 1 (2D — validate methodology)
3. Critical exponent extraction (Phase 2 and Phase 3)
4. Scaling collapse plots (Phase 2)
5. String tension analysis (Phase 3)

## Dependencies

- ts-quantum: `wilsonLoop()`, `averageWilsonLoop()` functions available
- Raw data: All phases have complete data files
- Analysis: Need to write scripts (no new simulation needed)

## References

- `timesarrow.tex`: Eq. 48 (Z₂ gauge action), Sec 8.3 (phase structure)
- `memory-bank/tasks/T20.md`: Full task description
- `numerics/output/`: Raw data files
- `ts-quantum/src/lattice/observables.ts`: Wilson loop implementation
