# timesarrow — Active Context

*Updated: 2026-06-25 15:45 IST*

## Session End — 2026-06-25

**TypeScript run (T20-Phase1):** ✅ COMPLETE.
**Rust framework (T27):** ✅ COMPLETE.
**T20-Phase2 (finite-size scaling):** ✅ COMPLETE — All 5 lattice sizes (L=8,12,16,20,24) simulated.

---

## Current State

### T20 — Z₂ LGT Monte Carlo

**Phase 1 Status**: ✅ COMPLETE
**Phase 2 Status**: ✅ COMPLETE
**Phase 3 Status**: 🟡 PENDING (3D cubic lattice)

#### Phase 2 Results: Finite-Size Scaling

All 5 lattice sizes run with Rust implementation, 200k sweeps each:

| L | Wall Time | ⟨P⟩ at β=0.44 | Binder U at β=0.44 |
|---|-----------|---------------|-------------------|
| 8 | 1.6s | 0.4076(8) | 0.579 |
| 12 | 3.9s | 0.4148(5) | 0.625 |
| 16 | 7.4s | 0.4132(5) | 0.640 |
| 20 | 11.6s | 0.4127(3) | 0.651 |
| 24 | 15.5s | 0.4132(3) | 0.656 |

**Key findings**:
- Plaquette expectation converges to ⟨P⟩ ≈ 0.413 at β_c ≈ 0.44
- Binder cumulant approaches U* ≈ 0.66 (2D Ising universal value) as L → ∞
- Total time for complete finite-size scaling study: ~40 seconds

#### Data Collation System

New systematic approach for organizing simulation data:
- `numerics/data/registry.json` — Central registry of all runs
- `numerics/data/registry.schema.json` — Schema definition
- `numerics/src/scripts/collate-data.ts` — Automated collation script
- Each run tracked with: runId, parameters, results, output files, status

### T27 — Rust Framework

**Status**: ✅ COMPLETE. Production-ready.

---

## Unblocked Tasks

| Task | Previously Blocked By | Status |
|------|----------------------|--------|
| T20-Phase3 (3D cubic) | T20-Phase2 | 🟡 Ready to start |
| T22 (Spin Foam) | T20-Phase2 | 🟡 Ready to start |
| T23 (Entanglement) | T20 | 🔴 Blocked (needs T20-Phase3) |

## What's Next

1. **T20-Phase3**: 3D cubic lattice extension
   - Wilson loop measurements (area vs perimeter law)
   - Critical exponents: ν ≈ 0.63, β ≈ 0.33 (3D Ising universality)
   - Dressed correlator C(r) = ⟨τ_0 ∏_{e∈γ} σ_e τ_r⟩

2. **T22**: 2D Spin Foam Amplitudes
   - Single vertex (L=1) amplitude computation
   - Ready to start

---

*See `memory-bank/tasks/T20.md` for full results and planning.*
*See `memory-bank/tasks/T27.md` for Rust framework details.*
