# timesarrow — Active Context

*Updated: 2026-06-25 05:30 IST*

## Current Focus

**T21 — Worker Threads + Checkpointing**

**Status**: ✅ IMPLEMENTATION COMPLETE. T20 Phase 1 complete, results validated.

**Results**:
- Checkpoint module (`ts-quantum/src/lattice/checkpoint.ts`): ✅ Working
- Worker thread scripts: ✅ Working
- Validation (L=8): ✅ Results match single-threaded
- Performance: 2.7× speedup (L=8), expected 6-8× (L=16)
- Checkpoint resume: ✅ Tested and working

## Completed This Session

### T21 — Worker Threads + Checkpointing
- ✅ `ts-quantum/src/lattice/checkpoint.ts` — Save/resume module
- ✅ `numerics/src/scripts/t20-z2-lgt-phase1-worker.cjs` — Worker entry point
- ✅ `numerics/src/scripts/t20-z2-lgt-phase1-main.cjs` — Main orchestrator
- ✅ Fixed `jackknifeError()` edge case (n ≤ 1)
- ✅ L=8 validation: results match single-threaded
- ✅ Checkpoint resume: correctly skips completed β values

### T20 Phase 1 — Production Run (from previous session)
- ✅ L=16, 18 β values, 100k sweeps completed
- ✅ Results saved and documented
- ✅ Numerics page updated with chronological log
- ✅ Error bars ~0.0005 (excellent statistics)

**Key finding**: Critical coupling β_c ≈ 0.44-0.46 confirmed, matching exact value 0.4407.

## Key Decisions (this session)

- **Coarse checkpointing first**: Per-β tracking sufficient for current lattice sizes (L≤16)
- **Fine-grained deferred**: Only implement if L≥32 simulations require it
- **Z2GaugeField.toJSON() reusable**: Serialization already implemented
- **Keep single-threaded fallback**: For debugging and validation
- **Worker threads over Rust/WASM**: For T21, Node.js worker threads are sufficient
- **CommonJS for worker scripts**: ESM build of ts-quantum has issues, CJS works

## Unblocked Tasks

| Task | Previously Blocked By | Status |
|------|----------------------|--------|
| T20-Phase2 (finite-size scaling) | T21 | 🔄 Ready to start |
| T20-Phase3 (3D cubic) | T21 | ⏳ After Phase 2 |

## Files in Play

| File | Role | Status |
|------|------|--------|
| `ts-quantum/src/lattice/checkpoint.ts` | Checkpoint save/resume | ✅ Implemented |
| `ts-quantum/src/lattice/observables.ts` | Jackknife error fix | ✅ Fixed |
| `numerics/src/scripts/t20-z2-lgt-phase1-worker.cjs` | Worker thread | ✅ Implemented |
| `numerics/src/scripts/t20-z2-lgt-phase1-main.cjs` | Main orchestrator | ✅ Implemented |
| `numerics/output/t20-phase1-worker-L8.json` | Validation results | ✅ Generated |

## What's Next

1. **Run** L=16 production run with worker threads
2. **Compare** to previous single-threaded L=16 results
3. **Update** numerics pages with T21 implementation details
4. **Start** T20-Phase2 (finite-size scaling) with worker threads

---

*See `memory-bank/tasks/T21-worker-threads-checkpointing.md` for detailed plan.*
*See `memory-bank/edits/2026-06-25-t21-implementation-complete.md` for implementation details.*
