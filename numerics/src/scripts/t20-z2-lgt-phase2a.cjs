const { createSquareLattice, Z2GaugeField, averagePlaquetteMoments, metropolisSweep, thermalize, jackknifeError, binData, susceptibility, plaquetteSpecificHeat, binderCumulant } = require('ts-quantum');
const fs = require('fs');
const path = require('path');

// ─── PRODUCTION PARAMETERS ───
const LATTICE_SIZES = [8, 16, 32];

// Dense β grid: 0.30–0.60 with Δβ = 0.02
// Plus extra-fine near β_c (0.40–0.50): Δβ = 0.01
const BETA_COARSE = Array.from({ length: 16 }, (_, i) => 0.30 + i * 0.02);
const BETA_FINE = Array.from({ length: 11 }, (_, i) => 0.40 + i * 0.01);
const BETA_VALUES = [...new Set([...BETA_COARSE, ...BETA_FINE])].sort((a, b) => a - b);

const THERMAL_SWEEPS = 100000;
const MEASURE_SWEEPS = 500000;
const MEASURE_EVERY = 10;
const BIN_SIZE = 100;
const MAX_PARALLEL = 6;

function formatTime(ms) {
  const totalSec = Math.floor(ms / 1000);
  const min = Math.floor(totalSec / 60);
  const sec = totalSec % 60;
  return `${min}m${sec}s`;
}

function runSimulation(L, beta) {
  const lattice = createSquareLattice(L);
  const field = new Z2GaugeField(lattice, 'random');
  const volume = L * L;
  
  // Thermalize
  const thermalRates = thermalize(field, beta, THERMAL_SWEEPS);
  const meanThermalRate = thermalRates.reduce((a, b) => a + b, 0) / thermalRates.length;
  
  // Measure
  const measurements = [];
  for (let s = 0; s < MEASURE_SWEEPS; s++) {
    metropolisSweep(field, beta);
    if (s % MEASURE_EVERY === 0) {
      const moments = averagePlaquetteMoments(field);
      measurements.push({ p: moments.mean, p2: moments.meanSq, p4: moments.meanFourth });
    }
  }
  
  // Extract and bin
  const pValues = measurements.map(m => m.p);
  const p2Values = measurements.map(m => m.p2);
  const p4Values = measurements.map(m => m.p4);
  
  const pBinned = binData(pValues, BIN_SIZE);
  const p2Binned = binData(p2Values, BIN_SIZE);
  const p4Binned = binData(p4Values, BIN_SIZE);
  
  // Statistics
  const meanP = pBinned.reduce((a, b) => a + b, 0) / pBinned.length;
  const meanP2 = p2Binned.reduce((a, b) => a + b, 0) / p2Binned.length;
  const meanP4 = p4Binned.reduce((a, b) => a + b, 0) / p4Binned.length;
  
  const errorP = jackknifeError(pBinned);
  const errorP2 = jackknifeError(p2Binned);
  const errorP4 = jackknifeError(p4Binned);
  
  // Derived observables
  const chiValues = pBinned.map((p, i) => susceptibility(p, p2Binned[i], volume));
  const cValues = pBinned.map((p, i) => plaquetteSpecificHeat(p, p2Binned[i], beta));
  const uValues = p4Binned.map((p4, i) => 1 - p4 / (3 * p2Binned[i] * p2Binned[i]));
  
  const chi = chiValues.reduce((a, b) => a + b, 0) / chiValues.length;
  const c = cValues.reduce((a, b) => a + b, 0) / cValues.length;
  const u = uValues.reduce((a, b) => a + b, 0) / uValues.length;
  
  const errorChi = jackknifeError(chiValues);
  const errorC = jackknifeError(cValues);
  const errorU = jackknifeError(uValues);
  
  return {
    L, beta,
    meanPlaquette: meanP, errorPlaquette: errorP,
    meanPlaquetteSq: meanP2, errorPlaquetteSq: errorP2,
    meanPlaquetteFourth: meanP4, errorPlaquetteFourth: errorP4,
    susceptibility: chi, errorSusceptibility: errorChi,
    specificHeat: c, errorSpecificHeat: errorC,
    binderCumulant: u, errorBinderCumulant: errorU,
    numMeasurements: measurements.length,
    numBinned: pBinned.length,
    acceptanceRate: meanThermalRate
  };
}

async function main() {
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║  T20 Phase 2A: Z₂ LGT Multi-Lattice Finite-Size Scaling     ║');
  console.log('║  PRODUCTION RUN                                              ║');
  console.log('╚══════════════════════════════════════════════════════════════╝');
  console.log('');
  console.log('Parameters:');
  console.log(`  Lattice sizes: ${LATTICE_SIZES.join(', ')}`);
  console.log(`  β values: ${BETA_VALUES.length} points (${BETA_VALUES[0].toFixed(2)} to ${BETA_VALUES[BETA_VALUES.length-1].toFixed(2)})`);
  console.log(`  Thermalization: ${THERMAL_SWEEPS.toLocaleString()} sweeps`);
  console.log(`  Measurement: ${MEASURE_SWEEPS.toLocaleString()} sweeps (every ${MEASURE_EVERY})`);
  console.log(`  Parallel runs: ${MAX_PARALLEL}`);
  console.log(`  Total simulations: ${LATTICE_SIZES.length * BETA_VALUES.length}`);
  console.log('');
  
  const allParams = [];
  for (const L of LATTICE_SIZES) {
    for (const beta of BETA_VALUES) {
      allParams.push({ L, beta });
    }
  }
  
  const results = [];
  const startTime = Date.now();
  
  for (let i = 0; i < allParams.length; i += MAX_PARALLEL) {
    const batch = allParams.slice(i, i + MAX_PARALLEL);
    const batchNum = Math.floor(i / MAX_PARALLEL) + 1;
    const totalBatches = Math.ceil(allParams.length / MAX_PARALLEL);
    const batchStart = Date.now();
    
    console.log(`[Batch ${batchNum}/${totalBatches}] L=[${batch.map(p => p.L).join(',')}], β=[${batch.map(p => p.beta.toFixed(2)).join(',')}]`);
    
    const batchResults = await Promise.all(
      batch.map(params => Promise.resolve(runSimulation(params.L, params.beta)))
    );
    
    const batchElapsed = Date.now() - batchStart;
    const totalElapsed = Date.now() - startTime;
    const avgPerSim = totalElapsed / (i + batch.length);
    const remaining = avgPerSim * (allParams.length - i - batch.length);
    
    for (const r of batchResults) {
      console.log(`  L=${r.L} β=${r.beta.toFixed(2)}: ⟨P⟩=${r.meanPlaquette.toFixed(4)}±${r.errorPlaquette.toFixed(4)} χ=${r.susceptibility.toFixed(2)}±${r.errorSusceptibility.toFixed(2)} U=${r.binderCumulant.toFixed(4)}±${r.errorBinderCumulant.toFixed(4)}`);
    }
    
    console.log(`  Batch time: ${formatTime(batchElapsed)} | Total: ${formatTime(totalElapsed)} | Est. remaining: ${formatTime(remaining)}`);
    console.log('');
    
    results.push(...batchResults);
  }
  
  const elapsed = Date.now() - startTime;
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log(`║  COMPLETED ${results.length} simulations in ${formatTime(elapsed)}                    ║`);
  console.log('╚══════════════════════════════════════════════════════════════╝');
  
  // Save results
  const outputDir = path.join(__dirname, '..', '..', 'output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const outputPath = path.join(outputDir, 't20-phase2a-finite-size.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    parameters: {
      LATTICE_SIZES, BETA_VALUES, THERMAL_SWEEPS, MEASURE_SWEEPS, MEASURE_EVERY, BIN_SIZE, MAX_PARALLEL
    },
    results
  }, null, 2));
  
  console.log(`\nResults saved to: ${outputPath}`);
  
  // Summary tables
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('SUSCEPTIBILITY PEAKS');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  for (const L of LATTICE_SIZES) {
    const lResults = results.filter(r => r.L === L);
    const maxChi = lResults.reduce((max, r) => r.susceptibility > max.susceptibility ? r : max, lResults[0]);
    console.log(`L=${L.toString().padEnd(2)}: χ_max=${maxChi.susceptibility.toFixed(2).padStart(8)}±${maxChi.errorSusceptibility.toFixed(2).padEnd(6)} at β=${maxChi.beta.toFixed(2)}`);
  }
  
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('BINDER CUMULANT NEAR β≈0.44');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  for (const L of LATTICE_SIZES) {
    const lResults = results.filter(r => r.L === L && Math.abs(r.beta - 0.44) < 0.02);
    for (const r of lResults) {
      console.log(`L=${L.toString().padEnd(2)} β=${r.beta.toFixed(2)}: U=${r.binderCumulant.toFixed(4)}±${r.errorBinderCumulant.toFixed(4)}`);
    }
  }
  
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('PLAQUETTE ⟨P⟩ CROSSOVER');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  for (const L of LATTICE_SIZES) {
    const lResults = results.filter(r => r.L === L && r.beta >= 0.40 && r.beta <= 0.50);
    console.log(`\nL=${L}:`);
    for (const r of lResults) {
      console.log(`  β=${r.beta.toFixed(2)}: ⟨P⟩=${r.meanPlaquette.toFixed(4)}±${r.errorPlaquette.toFixed(4)}`);
    }
  }
  
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('FINITE-SIZE SCALING ANALYSIS');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('Expected for 2D Ising universality class:');
  console.log('  • χ_peak ~ L^(γ/ν) = L^(7/4) ≈ L^1.75');
  console.log('  • U_L(β_c) → universal value (≈ 0.61 for 2D Ising)');
  console.log('  • β_c(L) from χ_max or U crossing');
  console.log('');
  
  // Extract χ_peak vs L for scaling analysis
  const chiPeaks = [];
  for (const L of LATTICE_SIZES) {
    const lResults = results.filter(r => r.L === L);
    const maxChi = lResults.reduce((max, r) => r.susceptibility > max.susceptibility ? r : max, lResults[0]);
    chiPeaks.push({ L, chiMax: maxChi.susceptibility, betaAtMax: maxChi.beta });
  }
  
  console.log('χ_max vs L:');
  for (const cp of chiPeaks) {
    console.log(`  L=${cp.L.toString().padEnd(2)}: χ_max=${cp.chiMax.toFixed(2).padStart(8)} at β=${cp.betaAtMax.toFixed(2)}`);
  }
  
  // Power law fit log(χ_max) = a + b*log(L)
  const logL = chiPeaks.map(cp => Math.log(cp.L));
  const logChi = chiPeaks.map(cp => Math.log(cp.chiMax));
  const n = logL.length;
  const sumLogL = logL.reduce((a, b) => a + b, 0);
  const sumLogChi = logChi.reduce((a, b) => a + b, 0);
  const sumLogLLogChi = logL.reduce((sum, l, i) => sum + l * logChi[i], 0);
  const sumLogLSq = logL.reduce((sum, l) => sum + l * l, 0);
  
  const b = (n * sumLogLLogChi - sumLogL * sumLogChi) / (n * sumLogLSq - sumLogL * sumLogL);
  const a = (sumLogChi - b * sumLogL) / n;
  
  console.log(`\nPower-law fit: χ_max ∝ L^b`);
  console.log(`  Fitted exponent: b = ${b.toFixed(3)}`);
  console.log(`  Theoretical (2D Ising): γ/ν = 7/4 = 1.750`);
  console.log(`  Agreement: ${(Math.abs(b - 1.75) / 1.75 * 100).toFixed(1)}% deviation`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
