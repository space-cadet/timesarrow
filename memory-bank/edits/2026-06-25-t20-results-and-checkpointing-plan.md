---

## Session Update — 2026-06-25

### Completed Work

**T20 Phase 1 — Production Run (L=16)**
- Status: ✅ COMPLETE
- Full-scale simulation with 18 β values, 100k measurement sweeps
- Error bars ~0.0005 (6× improvement over L=8 fast run)
- Results saved: `numerics/output/t20-phase1-square-lattice.json`
- Numerics page updated with chronological log format

**Results Summary**:
- Critical region clearly identified at β ≈ 0.44-0.46
- ⟨P⟩ ranges from 0.10 (β=0.1, confined) to 0.96 (β=2.0, deconfined)
- All 18 β values completed successfully with excellent statistics

### New Task: T21 — Worker Threads + Checkpointing

**Status**: 🔄 Planning → Implementation

**Motivation**: Current simulations are single-threaded and not checkpointable. Long runs (L=32, 3D cubic) risk losing hours of work if interrupted.

**Implementation Plan**:

1. **Worker Threads Architecture**
   - Main thread: orchestrates β values, collects results, handles I/O
   - Worker threads: one per CPU core, each runs independent β simulation
   - Communication: MessageChannel for state transfer

2. **Checkpointing Strategy**
   
   **Coarse-grained** (implement first):
   - Save after each β value completes
   - Track completed β values in JSON manifest
   - On resume: skip already-completed β values
   - Simple, robust, covers 90% of use cases
   
   **Fine-grained** (implement if needed):
   - Save Z2GaugeField state + sweep counter every N sweeps
   - Required for very large lattices where single β takes hours
   - More complex: need to serialize worker state, handle partial bins

3. **Files to Create**
   - `numerics/src/utils/checkpoint.ts` — save/resume logic
   - `numerics/src/scripts/t20-z2-lgt-phase1-worker.ts` — worker entry point
   - `numerics/src/scripts/t20-z2-lgt-phase1-main.ts` — main orchestrator

**Decision**: Start with coarse-grained checkpointing. Fine-grained only if L≥32 simulations show need.

**Next Steps**:
1. Implement checkpoint.ts module
2. Refactor phase1 script to worker_threads pattern
3. Test with small L=8 run
4. Run L=16 validation to ensure results match single-threaded

### Decisions

- **Coarse checkpointing first**: Per-β completion tracking is sufficient for current lattice sizes
- **Keep single-threaded version**: As fallback for debugging and comparison
- **Z2GaugeField.toJSON() already exists**: Checkpoint serialization is half-done
- **No GPU needed**: CPU parallelization across β values is optimal for this workload
