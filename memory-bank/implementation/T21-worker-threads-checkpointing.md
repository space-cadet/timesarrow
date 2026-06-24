# T21 — Worker Threads + Checkpointing Implementation

**Updated**: 2026-06-25
**Status**: Planning complete, implementation pending

## Architecture

### Coarse Checkpointing (Phase 1)

```typescript
// checkpoint.ts
import * as fs from 'fs';
import * as path from 'path';

const CHECKPOINT_DIR = './output/checkpoints';

export interface CheckpointManifest {
  simulationId: string;
  parameters: {
    L: number;
    thermalSweeps: number;
    measureSweeps: number;
    measureEvery: number;
    binSize: number;
  };
  completed: number[];      // β values completed
  results: Array<{
    beta: number;
    meanPlaquette: number;
    errorPlaquette: number;
    numMeasurements: number;
  }>;
  timestamp: string;
  version: '1.0';
}

export function saveCheckpoint(manifest: CheckpointManifest): void {
  const filepath = path.join(CHECKPOINT_DIR, `${manifest.simulationId}.json`);
  if (!fs.existsSync(CHECKPOINT_DIR)) {
    fs.mkdirSync(CHECKPOINT_DIR, { recursive: true });
  }
  fs.writeFileSync(filepath, JSON.stringify(manifest, null, 2));
}

export function loadCheckpoint(simulationId: string): CheckpointManifest | null {
  const filepath = path.join(CHECKPOINT_DIR, `${simulationId}.json`);
  if (!fs.existsSync(filepath)) return null;
  return JSON.parse(fs.readFileSync(filepath, 'utf-8'));
}

export function getRemainingBetas(
  allBetas: number[],
  manifest: CheckpointManifest | null
): number[] {
  if (!manifest) return allBetas;
  return allBetas.filter(b => !manifest.completed.includes(b));
}
```

### Worker Thread Pattern

```typescript
// t20-z2-lgt-phase1-main.ts
import { Worker } from 'worker_threads';
import * as os from 'os';
import { saveCheckpoint, loadCheckpoint, getRemainingBetas } from '../utils/checkpoint';

const NUM_WORKERS = os.cpus().length;  // 8 on M2 Air

interface BetaResult {
  beta: number;
  meanPlaquette: number;
  errorPlaquette: number;
  numMeasurements: number;
}

async function runParallelSweeps(params: SimulationParams): Promise<void> {
  const simulationId = `t20-phase1-L${params.L}-${Date.now()}`;
  
  // Check for existing checkpoint
  const checkpoint = loadCheckpoint(simulationId);
  const betas = getRemainingBetas(params.betaValues, checkpoint);
  
  const results: BetaResult[] = checkpoint?.results || [];
  const completed: number[] = checkpoint?.completed || [];
  
  // Worker pool
  const workers: Worker[] = [];
  const queue: number[] = [...betas];
  
  return new Promise((resolve, reject) => {
    let activeWorkers = 0;
    
    for (let i = 0; i < NUM_WORKERS; i++) {
      const worker = new Worker('./t20-z2-lgt-phase1-worker.js');
      workers.push(worker);
      
      worker.on('message', (result: BetaResult) => {
        results.push(result);
        completed.push(result.beta);
        
        // Save checkpoint after each β
        saveCheckpoint({
          simulationId,
          parameters: params,
          completed,
          results,
          timestamp: new Date().toISOString(),
          version: '1.0'
        });
        
        // Assign next β
        if (queue.length > 0) {
          const nextBeta = queue.shift()!;
          worker.postMessage({ ...params, beta: nextBeta });
        } else {
          activeWorkers--;
          if (activeWorkers === 0) {
            // All done
            workers.forEach(w => w.terminate());
            resolve();
          }
        }
      });
      
      worker.on('error', reject);
      
      // Start first batch
      if (queue.length > 0) {
        const beta = queue.shift()!;
        worker.postMessage({ ...params, beta });
        activeWorkers++;
      }
    }
  });
}
```

```typescript
// t20-z2-lgt-phase1-worker.ts
import { parentPort, workerData } from 'worker_threads';
import {
  createSquareLattice,
  Z2GaugeField,
  averagePlaquette,
  metropolisSweep,
  thermalize,
  jackknifeError,
  binData
} from 'ts-quantum';

parentPort?.on('message', (params) => {
  const { beta, L, thermalSweeps, measureSweeps, measureEvery, binSize } = params;
  
  // Run simulation
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  
  thermalize(field, beta, thermalSweeps);
  
  const measurements: number[] = [];
  for (let s = 0; s < measureSweeps; s++) {
    metropolisSweep(field, beta);
    if (s % measureEvery === 0) {
      measurements.push(averagePlaquette(field));
    }
  }
  
  const binned = binData(measurements, binSize);
  const mean = binned.reduce((a, b) => a + b, 0) / binned.length;
  const error = jackknifeError(binned);
  
  // Return result
  parentPort?.postMessage({
    beta,
    meanPlaquette: mean,
    errorPlaquette: error,
    numMeasurements: measurements.length
  });
});
```

## Key Decisions

1. **Coarse checkpointing first**: Per-β completion tracking is simple and sufficient for L≤16.
2. **Fine-grained deferred**: Only implement if single β simulation exceeds 30 minutes.
3. **JSON manifest**: Human-readable, easy to inspect and resume manually if needed.
4. **Worker per core**: Optimal for independent β sweeps (no communication between workers).

## Testing Plan

1. **Correctness**: Run L=8 with workers, compare to single-threaded results — should match exactly.
2. **Checkpoint resume**: Interrupt mid-run, verify resume skips completed β values.
3. **Performance**: Measure wall-clock time for 18 β values vs single-threaded.

## Open Questions

- Should we implement fine-grained checkpointing now or wait for L=32 need?
- Should checkpoint files include full RNG state for reproducibility?
- How to handle worker crashes? (retry logic, fallback to main thread)
