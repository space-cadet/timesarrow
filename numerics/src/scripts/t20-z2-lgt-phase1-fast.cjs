/**
 * T20 Phase 1: Z₂ LGT Monte Carlo on 2D Square Lattice (Fast Version)
 * 
 * Reduced parameters for quick demonstration
 */

const {
  createSquareLattice,
  Z2GaugeField,
  averagePlaquette,
  metropolisSweep,
  thermalize,
  jackknifeError,
  binData
} = require('../../../../ts-quantum/dist/index.js');

const fs = require('fs');
const path = require('path');

// Fast simulation parameters
const L = 8;
const thermalSweeps = 1000;
const measureSweeps = 5000;
const measureEvery = 5;
const binSize = 20;

const betaValues = [0.1, 0.2, 0.3, 0.4, 0.44, 0.5, 0.6, 0.8, 1.0, 1.5];

console.log('=== T20 Phase 1: Z₂ LGT on 2D Square Lattice (Fast) ===');
console.log('Lattice size:', L, 'x', L);
console.log('Thermalization:', thermalSweeps, 'sweeps');
console.log('Measurement:', measureSweeps, 'sweeps (every', measureEvery, ')');
console.log('');

const results = [];

for (const beta of betaValues) {
  process.stdout.write(`β = ${beta.toFixed(2)} ... `);
  
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  
  thermalize(field, beta, thermalSweeps);
  
  const measurements = [];
  for (let s = 0; s < measureSweeps; s++) {
    metropolisSweep(field, beta);
    if (s % measureEvery === 0) {
      measurements.push(averagePlaquette(field));
    }
  }
  
  const binned = binData(measurements, binSize);
  const mean = binned.reduce((a, b) => a + b, 0) / binned.length;
  const error = jackknifeError(binned);
  
  process.stdout.write(`⟨P⟩ = ${mean.toFixed(4)} ± ${error.toFixed(4)}\n`);
  
  results.push({ beta, meanPlaquette: mean, errorPlaquette: error });
}

console.log('\n=== Results ===');
console.log('β\t\t⟨P⟩\t\tError');
console.log('—'.repeat(40));
for (const r of results) {
  console.log(`${r.beta.toFixed(2)}\t\t${r.meanPlaquette.toFixed(4)}\t\t${r.errorPlaquette.toFixed(4)}`);
}

const outputDir = path.join(__dirname, '..', '..', 'output');
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

const outputPath = path.join(outputDir, 't20-phase1-fast.json');
fs.writeFileSync(outputPath, JSON.stringify({
  timestamp: new Date().toISOString(),
  parameters: { L, thermalSweeps, measureSweeps, measureEvery, binSize },
  results
}, null, 2));

console.log(`\nResults saved to ${outputPath}`);
