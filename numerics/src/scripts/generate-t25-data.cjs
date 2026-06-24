/**
 * T25 Data Generation Script
 * 
 * Run after building ts-quantum: node generate-t25-data.cjs
 */

const fs = require('fs');
const path = require('path');

const tsQuantumPath = path.resolve(__dirname, '..', '..', '..', 'ts-quantum', 'dist');
const { constructNValentBasis, computeVolumeSpectrum } = require(tsQuantumPath);

const outputDir = path.join(__dirname, '..', '..', 'output');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const results = [];

// 4-valent j=1/2
console.log('Computing 4-valent j=1/2...');
const space4 = constructNValentBasis(4, 0.5);
const spectrum4 = computeVolumeSpectrum(space4);
results.push({
  n: 4,
  j: 0.5,
  dimension: space4.dimension,
  eigenvalues: spectrum4.eigenvalues,
  hasZ2Structure: spectrum4.hasZ2Structure,
  note: 'Analytical result: eigenvalues = ±8√3/9 ≈ ±1.5396'
});

// 5-valent j=1/2
console.log('Computing 5-valent j=1/2...');
const space5 = constructNValentBasis(5, 0.5);
results.push({
  n: 5,
  j: 0.5,
  dimension: space5.dimension,
  eigenvalues: [],
  hasZ2Structure: true,
  note: 'No singlet subspace: odd number of half-integer spins cannot couple to J=0'
});

// 6-valent j=1/2
console.log('Computing 6-valent j=1/2...');
const space6 = constructNValentBasis(6, 0.5);
const spectrum6 = computeVolumeSpectrum(space6);
results.push({
  n: 6,
  j: 0.5,
  dimension: space6.dimension,
  eigenvalues: spectrum6.eigenvalues,
  hasZ2Structure: spectrum6.hasZ2Structure,
  note: 'Volume operator matrix not yet implemented for 6-valent'
});

// Save results
const outputPath = path.join(outputDir, 't25-spectrum.json');
fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));

console.log(`\nResults saved to: ${outputPath}`);
console.log('\nSummary:');
for (const r of results) {
  console.log(`  n=${r.n}, j=${r.j}: dim=${r.dimension}, Z₂=${r.hasZ2Structure}`);
}
