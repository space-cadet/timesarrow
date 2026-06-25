/**
 * Worker thread entry point for Z₂ LGT simulation
 * 
 * Receives a single β value and runs the full thermalization + measurement.
 * Posts result back to main thread when done.
 */

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

interface WorkerInput {
  beta: number;
  L: number;
  thermalSweeps: number;
  measureSweeps: number;
  measureEvery: number;
  binSize: number;
  seed?: number;
}

function runSimulation(params: WorkerInput) {
  const { beta, L, thermalSweeps, measureSweeps, measureEvery, binSize, seed } = params;
  
  // Optional seeding for reproducibility
  if (seed !== undefined) {
    // Simple seeded random - not cryptographically secure but deterministic
    let s = seed;
    const seededRandom = () => {
      s = (s * 16807 + 0) % 2147483647;
      return (s - 1) / 2147483646;
    };
    // Override Math.random for this worker
    (globalThis as any).Math = Object.create(Math);
    (globalThis as any).Math.random = seededRandom;
  }
  
  const startTime = Date.now();
  
  // Initialize lattice and field
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  
  // Thermalization
  thermalize(field, beta, thermalSweeps);
  
  // Measurement
  const measurements: number[] = [];
  for (let s = 0; s < measureSweeps; s++) {
    metropolisSweep(field, beta);
    if (s % measureEvery === 0) {
      measurements.push(averagePlaquette(field));
    }
  }
  
  // Analysis
  const binned = binData(measurements, binSize);
  const mean = binned.reduce((a, b) => a + b, 0) / binned.length;
  const error = jackknifeError(binned);
  const wallTime = Date.now() - startTime;
  
  return {
    beta,
    meanPlaquette: mean,
    errorPlaquette: error,
    numMeasurements: measurements.length,
    wallTimeMs: wallTime
  };
}

// If run as worker, listen for messages
if (parentPort) {
  parentPort.on('message', (params: WorkerInput) => {
    try {
      const result = runSimulation(params);
      parentPort!.postMessage({ type: 'result', data: result });
    } catch (error) {
      parentPort!.postMessage({ 
        type: 'error', 
        beta: params.beta,
        error: error instanceof Error ? error.message : String(error)
      });
    }
  });
}

// Export for testing
export { runSimulation };
export type { WorkerInput };
