/**
 * T25 Data Generation Script
 * 
 * Computes volume operator spectrum for n=4,5,6 valent intertwiners
 * and saves results to JSON.
 */

import { 
  constructNValentBasis, 
  computeVolumeSpectrum,
  buildGeneric6ValentEmbedding
} from 'ts-quantum';
import * as fs from 'fs';
import * as path from 'path';

const outputDir = path.join(__dirname, '..', 'output');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const results: Array<{
  n: number;
  j: number;
  dimension: number;
  eigenvalues: number[];
  hasZ2Structure: boolean;
  note?: string;
}> = [];

// 4-valent j=1/2
console.log('Computing 4-valent j=1/2...');
const space4 = constructNValentBasis(4, 0.5);
const spec4 = computeVolumeSpectrum(space4);
results.push({
  n: 4,
  j: 0.5,
  dimension: space4.dimension,
  eigenvalues: spec4.eigenvalues,
  hasZ2Structure: spec4.hasZ2Structure,
  note: 'Analytical result: ±8√3/9 ≈ ±1.5396'
});

// 5-valent j=1/2 (trivially excluded)
console.log('Computing 5-valent j=1/2...');
const space5 = constructNValentBasis(5, 0.5);
results.push({
  n: 5,
  j: 0.5,
  dimension: space5.dimension,
  eigenvalues: [],
  hasZ2Structure: true,
  note: 'Odd number of half-integer spins cannot couple to J=0 (singlet subspace dimension = 0)'
});

// 6-valent j=1/2 with generic geometric embedding
console.log('Computing 6-valent j=1/2 with generic embedding...');
const embedding = buildGeneric6ValentEmbedding();
const space6 = constructNValentBasis(6, 0.5);
const spec6 = computeVolumeSpectrum(space6, embedding);
results.push({
  n: 6,
  j: 0.5,
  dimension: space6.dimension,
  eigenvalues: spec6.eigenvalues,
  hasZ2Structure: spec6.hasZ2Structure,
  note: 'Singlet subspace dimension = 5. Generic geometric embedding (triangular prism). Eigenvalues: ±2.291, ±0.866, 0'
});

// Save results
const outputPath = path.join(outputDir, 't25-volume-operator-spectrum.json');
fs.writeFileSync(outputPath, JSON.stringify({
  timestamp: new Date().toISOString(),
  description: 'Volume operator spectrum for n=4,5,6 valent intertwiners with j=1/2',
  results
}, null, 2));

console.log(`\nResults saved to ${outputPath}`);
console.log('\nSummary:');
for (const r of results) {
  console.log(`  n=${r.n}: dim=${r.dimension}, eigenvalues=[${r.eigenvalues.map(x => x.toFixed(4)).join(', ')}], Z₂=${r.hasZ2Structure}`);
}
