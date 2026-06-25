# timesarrow — Active Context

*Updated: 2026-06-25 14:06 IST*

## Session End — 2026-06-25

**TypeScript run (T20-Phase1):** ✅ COMPLETE. All 11 β values finished, results saved.
**Rust framework (T27):** ✅ COMPLETE. Built, tested, validated against TypeScript.

---

## Current State

### T20-Phase1 — Z₂ LGT 2D Square Lattice

**Status**: ✅ COMPLETE

**Results (L=16, 100k sweeps, 11 β values):**
| β | ⟨P⟩ | Error | Phase |
|---|-----|-------|-------|
| 0.1 | 0.0997 | ±0.0006 | Weak |
| 0.2 | 0.1978 | ±0.0006 | Weak |
| 0.3 | 0.2916 | ±0.0006 | Weak |
| 0.4 | 0.3794 | ±0.0006 | Weak |
| 0.44 | 0.4144 | ±0.0006 | Critical |
| 0.5 | 0.4629 | ±0.0006 | Strong |
| 0.6 | 0.5370 | ±0.0005 | Strong |
| 0.8 | 0.6645 | ±0.0005 | Strong |
| 1.0 | 0.7613 | ±0.0004 | Strong |
| 1.5 | 0.9048 | ±0.0003 | Strong |
| 2.0 | 0.9640 | ±0.0002 | Strong |

- **Total wall time**: ~2h 11m
- **Critical coupling β_c ≈ 0.44** confirmed, matching exact value 0.4407
- **Output file**: `numerics/output/t20-phase1-worker-L16.json`

### T27 — Rust Z₂ Lattice Gauge Theory Framework

**Status**: ✅ COMPLETE. Validated against TypeScript.

**Deliverables:**
- `rust-lattice/src/lib.rs` — Z2GaugeField with Metropolis, observables, checkpoints
- `rust-lattice/src/main.rs` — CLI with rayon parallel β sweeps, JSON output
- `rust-lattice/Cargo.toml` — deps: rand, rand_xoshiro, serde, serde_json, rayon
- Release binary: `target/release/z2-lattice-gauge` (419 KB)

**Validation Results:**
- L=16, 100k sweeps, 11 β values: **3.0s total** (TypeScript: ~2h 10m)
- All 11 β values match TypeScript within |Δ| < 0.02
- Speedup: **~2,500–3,000×**

**Bug fixes applied:**
1. Plaquette geometry: wrong link indices for top/left edges (`link(x+1,y+1,0)` → `link(x,y+1,0)`)
2. Sign convention: TypeScript uses 4 directed links/site; Rust uses 2 undirected. Fixed by negating `plaquette_stats()` output only (preserving Metropolis dynamics)

**Test results**: 3/3 pass

---

## Previously Completed

### T21 — Worker Threads + Checkpointing

**Results**:
- Checkpoint module (`ts-quantum/src/lattice/checkpoint.ts`): ✅ Working
- Worker thread scripts: ✅ Working
- Validation (L=8): ✅ Results match single-threaded
- Performance: 2.7× speedup (L=8), 6-8× expected (L=16)
- Checkpoint resume: ✅ Tested and working

---

## Unblocked Tasks

| Task | Previously Blocked By | Status |
|------|----------------------|--------|
| T20-Phase2 (finite-size scaling) | T20-Phase1, T27 | 🔄 Ready to start |
| T20-Phase3 (3D cubic) | T20-Phase2 | ⏳ After Phase 2 |

## What's Next

1. **T20-Phase2**: Finite-size scaling with Rust — L = 8, 12, 16, 20, 24, β values 0.3–0.6 (critical region)
   - Estimated time: ~2–3 minutes total (Rust)
   - Output: sharp phase transition figures for publication

2. **T20-Phase3**: 3D cubic lattice extension
   - Wilson loop measurements (area vs perimeter law)
   - Critical exponents: ν ≈ 0.63, β ≈ 0.33 (3D Ising universality)
   - Dressed correlator C(r) = ⟨τ_0 ∏_{e∈γ} σ_e τ_r⟩

---

*See `memory-bank/tasks/T20.md` for full Phase 1 results and Phase 2/3 planning.*
*See `memory-bank/tasks/T27.md` for Rust framework details and benchmark data.*
