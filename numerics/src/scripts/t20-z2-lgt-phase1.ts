/**
 * T20 Phase 1: Z₂ LGT Monte Carlo on 2D Square Lattice
 * 
 * Parameter sweep to locate critical coupling β_c ≈ 0.4407
 */

import {
  createSquareLattice,
  Z2GaugeField,
  averagePlaquette,
  metropolisSweep,
  thermalize,
  jackknifeError,
  binData
} from 'ts-quantum';

import * as fs from 'fs';
import * as path from 'path';

// Simulation parameters
const L = 16;                    // Lattice size
const thermalSweeps = 10000;     // Thermalization sweeps
const measureSweeps = 100000;    // Measurement sweeps
const measureEvery = 10;         // Measure every N sweeps
const binSize = 100;             // Bin size for error analysis

// β values to simulate (around critical β_c ≈ 0.4407)
const betaValues = [
  0.1, 0.2, 0.3, 0.35, 0.38, 0.40, 0.42, 0.44, 0.45,
  0.46, 0.48, 0.50, 0.55, 0.60, 0.80, 1.0, 1.5, 2.0
];

console.log('=== T20 Phase 1: Z₂ LGT on 2D Square Lattice ===');
console.log('Lattice size:', L, 'x', L);
console.log('Thermalization:', thermalSweeps, 'sweeps');
console.log('Measurement:', measureSweeps, 'sweeps (every', measureEvery, ')');
console.log('β values:', betaValues.length, 'points');
console.log('');

const results = [];

for (const beta of betaValues) {
  process.stdout.write(`β = ${beta.toFixed(2)} ... `);
  
  // Create lattice and field
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  
  // Thermalize
  thermalize(field, beta, thermalSweeps);
  
  // Measure
  const measurements: number[] = [];
  for (let s = 0; s < measureSweeps; s++) {
    metropolisSweep(field, beta);
    if (s % measureEvery === 0) {
      measurements.push(averagePlaquette(field));
    }
  }
  
  // Bin data to reduce autocorrelation
  const binned = binData(measurements, binSize);
  
  // Compute statistics
  const mean = binned.reduce((a, b) => a + b, 0) / binned.length;
  const error = jackknifeError(binned);
  
  process.stdout.write(`⟨P⟩ = ${mean.toFixed(4)} ± ${error.toFixed(4)}\n`);
  
  results.push({
    beta,
    meanPlaquette: mean,
    errorPlaquette: error,
    numMeasurements: measurements.length,
    numBinned: binned.length
  });
}

console.log('\n=== Results ===');
console.log('β\t\t⟨P⟩\t\tError');
console.log('—'.repeat(40));
for (const r of results) {
  console.log(`${r.beta.toFixed(2)}\t\t${r.meanPlaquette.toFixed(4)}\t\t${r.errorPlaquette.toFixed(4)}`);
}

// Save results
const outputDir = path.join(__dirname, '..', '..', 'output');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const outputPath = path.join(outputDir, 't20-phase1-square-lattice.json');
fs.writeFileSync(outputPath, JSON.stringify({
  timestamp: new Date().toISOString(),
  parameters: {
    L,
    thermalSweeps,
    measureSweeps,
    measureEvery,
    binSize
  },
  results
}, null, 2));

console.log(`\nResults saved to ${outputPath}`);
