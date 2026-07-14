#### 11:15 IST - T31: Polyakov loop proof-of-principle scan complete

**Actions:**
- Fixed Polyakov loop measurement in `rust-lattice/src/lib.rs`: changed from `average_polyakov_3d()` (average of |P| = always 1) to `average_polyakov_signed_3d()` (signed spatial average P̄)
- Rebuilt Rust binary
- Ran proof-of-principle scans for L=8, 10, 12 across β = 0.60–0.85
- Saved results to `numerics/data/t31-polyakov-proof-of-principle-20260714.json`

**Results:**
- Polyakov loop susceptibility χ_P peaks at β = 0.76 for all L
- Peak height grows with L: 355 (L=8) → 621 (L=10) → 886 (L=12)
- Mean Polyakov loop |⟨P̄⟩| → 1 in ordered phase, ≈ 0 in disordered phase
- Binder cumulant U_P → 0.665 in deep ordered phase (close to 2/3)

**Files modified:**
- `rust-lattice/src/lib.rs` — Fixed Polyakov loop measurement to use signed average
- `memory-bank/tasks/T31.md` — Updated with Polyakov loop results
- `numerics/data/t31-polyakov-proof-of-principle-20260714.json` — New data file
