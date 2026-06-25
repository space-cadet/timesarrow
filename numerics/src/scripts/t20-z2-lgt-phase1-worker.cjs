/**
 * Worker thread entry point for Z₂ LGT simulation
 * 
 * Uses CommonJS require for compatibility with ts-quantum's CJS build.
 */

const { parentPort } = require('worker_threads');

const {
  createSquareLattice,
  Z2GaugeField,
  averagePlaquette,
  metropolisSweep,
  thermalize,
  jackknifeError,
  binData
} = require('ts-quantum');

function runSimulation(params) {
  const { beta, L, thermalSweeps, measureSweeps, measureEvery, binSize } = params;
  
  const startTime = Date.now();
  
  // Initialize lattice and field
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  
  // Thermalization
  thermalize(field, beta, thermalSweeps);
  
  // Measurement
  const measurements = [];
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

// Listen for messages from main thread
if (parentPort) {
  parentPort.on('message', (params) => {
    console.log(`[WORKER] Starting β=${params.beta}, sweeps=${params.measureSweeps}`);
    try {
      const result = runSimulation(params);
      console.log(`[WORKER] Done β=${params.beta}, P=${result.meanPlaquette.toFixed(4)}`);
      parentPort.postMessage({ type: 'result', data: result });
    } catch (error) {
      console.error(`[WORKER] Error β=${params.beta}:`, error.message);
      parentPort.postMessage({ 
        type: 'error', 
        beta: params.beta,
        error: error.message || String(error)
      });
    }
  });
}

module.exports = { runSimulation };
