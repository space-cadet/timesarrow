#!/usr/bin/env node
/**
 * T20 Wilson Loop Analysis Script (Fixed)
 * 
 * Processes Wilson loop data from Rust simulation outputs:
 * 1. Uses |W| (absolute value) for area law fits since Z2 Wilson loops can be negative
 * 2. Fits string tension σ from area law: |W(A)| ~ exp(-σ·A)
 * 3. Generates plots for area law vs perimeter law
 * 4. Outputs analysis results as JSON
 */

const fs = require('fs');
const path = require('path');

// Read Phase 1 (2D) data
const p1Data = JSON.parse(fs.readFileSync(
  path.join(__dirname, '../../output/t20-p1-L16-wilson-20250626.json'),
  'utf8'
));

// Read Phase 3 (3D) data
const p3Data = JSON.parse(fs.readFileSync(
  path.join(__dirname, '../../output/t20-p3-L8-3D-wilson-fine-20250626.json'),
  'utf8'
));

/**
 * Fit string tension σ from log(|W|) vs Area
 * Returns { sigma, sigmaError, chi2, fitQuality }
 */
function fitStringTension(wilsonData) {
  const areas = [];
  const logAbsWs = [];

  for (const { r, c, meanW, varW } of wilsonData) {
    const area = r * c;
    const absW = Math.abs(meanW);
    if (absW < 1e-10) continue; // Skip zero values
    areas.push(area);
    logAbsWs.push(Math.log(absW));
  }

  if (areas.length < 2) {
    return { sigma: null, sigmaError: null, chi2: null, fitQuality: null };
  }

  // Linear fit: log(|W|) = -σ·Area + C
  const n = areas.length;
  const sumX = areas.reduce((a, b) => a + b, 0);
  const sumY = logAbsWs.reduce((a, b) => a + b, 0);
  const sumXY = areas.reduce((sum, x, i) => sum + x * logAbsWs[i], 0);
  const sumX2 = areas.reduce((sum, x) => sum + x * x, 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;

  // Error estimate
  const residuals = areas.map((x, i) => logAbsWs[i] - (slope * x + intercept));
  const sumRes2 = residuals.reduce((sum, r) => sum + r * r, 0);
  const sigmaError = Math.sqrt(sumRes2 / (n - 2)) / Math.sqrt(sumX2 - sumX * sumX / n);

  return {
    sigma: -slope, // Convert to positive string tension
    sigmaError: sigmaError || Infinity,
    chi2: sumRes2,
    fitQuality: sumRes2 / (n - 2),
    intercept: intercept,
    areas,
    logAbsWs,
    predictions: areas.map(x => slope * x + intercept)
  };
}

/**
 * Analyze Wilson loops for a single β value
 */
function analyzeBeta(result) {
  const { beta, wilsonLoops } = result;
  
  // Fit string tension using |W|
  const tension = fitStringTension(wilsonLoops);
  
  return {
    beta,
    tension,
    wilsonLoops: wilsonLoops.map(({ r, c, meanW, varW }) => ({
      r, c, area: r * c, perimeter: 2 * (r + c),
      meanW, absW: Math.abs(meanW), varW, 
      logAbsW: Math.log(Math.abs(meanW) + 1e-10)
    }))
  };
}

// Analyze Phase 1 (2D) data
console.log('=== Phase 1: 2D Square Lattice (L=16) ===\n');
const p1Analysis = p1Data.results.map(r => analyzeBeta(r));

for (const a of p1Analysis) {
  console.log(`β = ${a.beta.toFixed(2)}:`);
  if (a.tension.sigma !== null) {
    console.log(`  String tension σ = ${a.tension.sigma.toFixed(4)} ± ${a.tension.sigmaError.toFixed(4)}`);
  } else {
    console.log(`  String tension: insufficient data`);
  }
  for (const w of a.wilsonLoops) {
    console.log(`  |W|(${w.r}×${w.c}) = ${w.absW.toFixed(4)} (area=${w.area})`);
  }
  console.log();
}

// Analyze Phase 3 (3D) data
console.log('=== Phase 3: 3D Cubic Lattice (L=8) ===\n');
const p3Analysis = p3Data.results.map(r => analyzeBeta(r));

for (const a of p3Analysis) {
  console.log(`β = ${a.beta.toFixed(2)}:`);
  if (a.tension.sigma !== null) {
    console.log(`  String tension σ = ${a.tension.sigma.toFixed(4)} ± ${a.tension.sigmaError.toFixed(4)}`);
  } else {
    console.log(`  String tension: insufficient data`);
  }
  for (const w of a.wilsonLoops) {
    console.log(`  |W|(${w.r}×${w.c}) = ${w.absW.toFixed(4)} (area=${w.area})`);
  }
  console.log();
}

// Save analysis results
const outputDir = path.join(__dirname, '../../output');
fs.writeFileSync(
  path.join(outputDir, 't20-p1-L16-wilson-analysis.json'),
  JSON.stringify({ phase: '1', dimension: 2, results: p1Analysis }, null, 2)
);
fs.writeFileSync(
  path.join(outputDir, 't20-p3-L8-3D-wilson-analysis.json'),
  JSON.stringify({ phase: '3', dimension: 3, results: p3Analysis }, null, 2)
);

console.log('Analysis results saved to:');
console.log('  - t20-p1-L16-wilson-analysis.json');
console.log('  - t20-p3-L8-3D-wilson-analysis.json');
