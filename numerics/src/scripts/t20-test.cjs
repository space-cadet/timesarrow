/**
 * T20 Phase 1: Quick test run for Z₂ LGT on 2D Square Lattice
 */

const {
  createSquareLattice,
  Z2GaugeField,
  averagePlaquette,
  metropolisSweep,
  thermalize
} = require('../../../../ts-quantum/dist/index.js');

console.log('=== T20 Phase 1: Quick Test ===');

const L = 8;
const betaValues = [0.2, 0.44, 1.0];

for (const beta of betaValues) {
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  
  // Quick thermalization
  thermalize(field, beta, 1000);
  
  // Quick measurement
  const measurements = [];
  for (let s = 0; s < 1000; s++) {
    metropolisSweep(field, beta);
    if (s % 10 === 0) {
      measurements.push(averagePlaquette(field));
    }
  }
  
  const mean = measurements.reduce((a, b) => a + b, 0) / measurements.length;
  console.log(`β = ${beta.toFixed(2)}: ⟨P⟩ = ${mean.toFixed(4)}`);
}

console.log('\nTest complete.');
