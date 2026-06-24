# timesarrow — Active Context

*Updated: 2026-06-25 04:12 IST*

## Current Focus

**T21 — Worker Threads + Checkpointing**

**Status**: 🔄 Ready to implement. T20 Phase 1 complete, results validated.

**Plan**: Implement coarse-grained checkpointing first, then worker thread orchestration.

**Decision**: Start implementation immediately. Physics is validated (β_c ≈ 0.44 confirmed).

## Completed This Session

### T20 Phase 1 — Production Run
- ✅ L=16, 18 β values, 100k sweeps completed
- ✅ Results saved and documented
- ✅ Numerics page updated with chronological log
- ✅ Error bars ~0.0005 (excellent statistics)

**Key finding**: Critical coupling β_c ≈ 0.44-0.46 confirmed, matching exact value 0.4407.

## T21 — Worker Threads + Checkpointing (In Progress)

**Status**: 🔄 Planning complete, implementation starting

**Scope**:
1. **Coarse checkpointing** (per-β completion tracking) — implement first
2. **Fine-grained checkpointing** (mid-simulation state) — if needed for L≥32
3. **Worker thread orchestration** — parallel β sweeps across CPU cores

**Architecture**:
- Main thread: distributes β values, collects results, handles I/O
- Workers: one per core, independent simulations
- Checkpoints: JSON manifest tracking completed β values

**Files to create**:
| File | Purpose |
|------|---------|
| `numerics/src/utils/checkpoint.ts` | Save/resume logic |
| `numerics/src/scripts/t20-z2-lgt-phase1-worker.ts` | Worker entry point |
| `numerics/src/scripts/t20-z2-lgt-phase1-main.ts` | Main orchestrator |

## Key Decisions (this session)

- **Coarse checkpointing first**: Per-β tracking sufficient for current lattice sizes (L≤16)
- **Fine-grained deferred**: Only implement if L≥32 simulations require it
- **Z2GaugeField.toJSON() reusable**: Serialization already implemented
- **Keep single-threaded fallback**: For debugging and validation
- **Worker threads over Rust/WASM**: For T21, Node.js worker threads are sufficient (parallel β sweeps, not inner loop optimization)

## Blocked Tasks

| Task | Blocked By | When Unblocked |
|------|-----------|---------------|
| T20-Phase2 (finite-size scaling) | T21 | After worker threads + checkpointing ready |
| T20-Phase3 (3D cubic) | T21 | After Phase 2 |

## Files in Play

| File | Role | Status |
|------|------|--------|
| `ts-quantum/src/lattice/gaugeField.ts` | Z2GaugeField with toJSON/fromJSON | ✅ Ready |
| `numerics/output/t20-phase1-square-lattice.json` | Production results | ✅ Complete |
| `numerics/docs/tasks/t20-z2-lgt.qmd` | Numerics page with chronological log | ✅ Updated |
| `memory-bank/edits/2026-06-25-t20-results-and-checkpointing-plan.md` | This session's work log | ✅ Created |

## What's Next

1. **Implement** `checkpoint.ts` module
2. **Create** worker thread scripts
3. **Test** with L=8 validation run
4. **Verify** results match single-threaded version
5. **Document** in numerics pages

---

*See `memory-bank/tasks/T21-worker-threads-checkpointing.md` for detailed plan.*
