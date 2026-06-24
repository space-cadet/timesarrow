# T21 — Worker Threads + Checkpointing

**Status**: 🔄 Ready to implement
**Created**: 2026-06-25
**Priority**: High (blocks T20 Phase 2 and 3)

## Objective

Add worker thread parallelization and checkpointing to Monte Carlo simulations. Enable:
1. Parallel β sweeps across CPU cores
2. Resumable simulations (no lost work on interruption)
3. Efficient use of M2 Air 8-core architecture

## Background

Current simulations are single-threaded. The T20 Phase 1 production run (L=16, 18 β values, 100k sweeps) took significant wall-clock time. Moving to larger lattices (L=32) and 3D cubic will make this untenable without parallelization.

## Implementation Plan

### Phase 1: Coarse Checkpointing

**What**: Save progress after each β value completes.

**Files**:
- `numerics/src/utils/checkpoint.ts`

**Interface**:
```typescript
interface CheckpointManifest {
  simulationId: string;
  parameters: SimulationParameters;
  completed: number[];  // β values done
  results: BetaResult[];
  timestamp: string;
}

function saveCheckpoint(manifest: CheckpointManifest): void;
function loadCheckpoint(simulationId: string): CheckpointManifest | null;
function resumeSimulation(manifest: CheckpointManifest): number[];  // β values still needed
```

**Logic**:
1. Before starting: check for existing checkpoint
2. If found: load completed β values, skip them
3. After each β: append result, save manifest
4. On interrupt: manifest already saved, resume finds it

### Phase 2: Worker Thread Orchestration

**Architecture**:
```
Main Thread                    Workers (1 per core)
     |                              |
     ├── assign β=0.1 ───────────→ Worker 1
     ├── assign β=0.2 ───────────→ Worker 2
     ├── assign β=0.3 ───────────→ Worker 3
     │         ...                      |
     ←── result ─────────────────── Worker 1 (done)
     ├── assign β=0.4 ───────────→ Worker 1
     │         ...                      |
     ←── all done ──────────────────────|
```

**Files**:
- `numerics/src/scripts/t20-z2-lgt-phase1-main.ts` — Main orchestrator
- `numerics/src/scripts/t20-z2-lgt-phase1-worker.ts` — Worker entry point

**Worker interface**:
```typescript
// worker.ts
import { parentPort, workerData } from 'worker_threads';

interface WorkerData {
  beta: number;
  L: number;
  thermalSweeps: number;
  measureSweeps: number;
  measureEvery: number;
}

// Run simulation for single β
// Post result back to main thread
```

### Phase 3: Fine-Grained Checkpointing (Conditional)

**Trigger**: Only if L≥32 or 3D simulations show single β takes >30 minutes.

**What**: Save Z2GaugeField state + sweep counter mid-simulation.

**Files**: Extend `checkpoint.ts` with:
```typescript
interface FineCheckpoint {
  beta: number;
  sweep: number;
  field: Z2GaugeField;  // serialized
  measurements: number[];
}
```

**Decision**: Defer until needed. Coarse checkpointing handles current use cases.

## Acceptance Criteria

- [ ] `checkpoint.ts` module with save/load/resume
- [ ] Worker thread scripts for T20 Phase 1
- [ ] Validation: L=8 results match single-threaded version exactly
- [ ] Performance: 6-8× speedup on 8-core M2 Air for multi-β sweeps
- [ ] Numerics page updated with new architecture

## Dependencies

- `ts-quantum` ≥ 0.x (Z2GaugeField, lattice, Metropolis)
- Node.js ≥ 14 (worker_threads)

## Related

- T20-Phase1: Results validated, ready for parallelization
- T20-Phase2: Blocked until T21 complete
- T20-Phase3: Blocked until T21 complete
