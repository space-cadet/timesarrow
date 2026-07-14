#### 10:45 IST - T31: Gauge-invariant signed volume FAILED validation — pivot to Polyakov loop

**Actions:**
- Implemented `simulate_beta_with_wilson_and_gauge_invariant_signed_volume()` in `rust-lattice/src/lib.rs`
- Added `--gauge-invariant-signed-volume` CLI flag in `rust-lattice/src/main.rs`
- Fixed bug: `gauge_invariant_signed_volume_3d()` was using `path_product_zyx_3d()` for W(r1→r2) while using `path_product_xyz_3d()` for s(r) — changed to use `path_product_xyz_3d()` for both
- Ran test simulations: L=6 (5k+5k sweeps) and L=8 (10k+10k sweeps)

**Results:**
- Cold start: Q_GI = 1.000 ✓
- L=6 thermalized: Q_GI ≈ 0.02–0.08 (weak trend with β)
- L=8 thermalized: Q_GI ≈ 0.01 (flat across all β, no phase discrimination)

**Root cause:** Elitzur's theorem — individual link variables are random ±1 in any thermalized state, so path products are ±1 with equal probability. The triple product averages to ~0 regardless of phase.

**Decision:** Abandon signed volume as an order parameter. Pivot to Polyakov loop (already implemented, standard deconfinement diagnostic).

**Files modified:**
- `rust-lattice/src/lib.rs` — Added `simulate_beta_with_wilson_and_gauge_invariant_signed_volume()`, fixed path convention in `gauge_invariant_signed_volume_3d()`
- `rust-lattice/src/main.rs` — Added `--gauge-invariant-signed-volume` flag
- `memory-bank/tasks/T31.md` — Recorded pivot decision
- `memory-bank/implementation-details/signed-volume-observable.md` — Documented Elitzur theorem obstruction
- `memory-bank/activeContext.md` — Updated T31 status
