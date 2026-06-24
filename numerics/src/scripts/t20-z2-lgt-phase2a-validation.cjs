const { createSquareLattice, Z2GaugeField, averagePlaquetteMoments, metropolisSweep, thermalize, jackknifeError, binData, susceptibility, plaquetteSpecificHeat, binderCumulant } = require('ts-quantum');
const fs = require('fs');
const path = require('path');

// ─── FAST VALIDATION PARAMETERS ───
const LATTICE_SIZES = [8, 16, 32];

// Reduced β grid for quick validation
const BETA_VALUES = [0.30, 0.35, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.55, 0.60];

const THERMAL_SWEEPS = 10000;   // Reduced from 100k
const MEASURE_SWEEPS = 50000;    // Reduced from 500k
const MEASURE_EVERY = 10;
const BIN_SIZE = 50;
const MAX_PARALLEL = 6;

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
  
  // Compute statistics
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
  console.log('=== T20 Phase 2A VALIDATION RUN (Fast Parameters) ===');
  console.log('Lattice sizes:', LATTICE_SIZES.join(', '));
  console.log('β values:', BETA_VALUES.length, 'points');
  console.log('Thermalization:', THERMAL_SWEEPS, 'sweeps');
  console.log('Measurement:', MEASURE_SWEEPS, 'sweeps (every', MEASURE_EVERY, ')');
  console.log('WARNING: Reduced statistics for quick validation only!');
  console.log('');
  
  const allParams = [];
  for (const L of LATTICE_SIZES) {
    for (const beta of BETA_VALUES) {
      allParams.push({ L, beta });
    }
  }
  
  console.log(`Total simulations: ${allParams.length}`);
  console.log('');
  
  const results = [];
  const startTime = Date.now();
  
  for (let i = 0; i < allParams.length; i += MAX_PARALLEL) {
    const batch = allParams.slice(i, i + MAX_PARALLEL);
    const batchNum = Math.floor(i / MAX_PARALLEL) + 1;
    const totalBatches = Math.ceil(allParams.length / MAX_PARALLEL);
    
    console.log(`Batch ${batchNum}/${totalBatches}: L=[${batch.map(p => p.L).join(',')}], β=[${batch.map(p => p.beta.toFixed(2)).join(',')}]`);
    
    const batchResults = await Promise.all(
      batch.map(params => Promise.resolve(runSimulation(params.L, params.beta)))
    );
    
    for (const r of batchResults) {
      console.log(`  L=${r.L} β=${r.beta.toFixed(2)}: ⟨P⟩=${r.meanPlaquette.toFixed(4)}±${r.errorPlaquette.toFixed(4)} χ=${r.susceptibility.toFixed(2)}±${r.errorSusceptibility.toFixed(2)} U=${r.binderCumulant.toFixed(4)}±${r.errorBinderCumulant.toFixed(4)}`);
    }
    
    results.push(...batchResults);
  }
  
  const elapsed = (Date.now() - startTime) / 1000;
  console.log(`\n=== Completed ${results.length} simulations in ${elapsed.toFixed(1)}s ===`);
  
  // Save results
  const outputDir = path.join(__dirname, '..', '..', 'output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const outputPath = path.join(outputDir, 't20-phase2a-validation.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    parameters: {
      LATTICE_SIZES, BETA_VALUES, THERMAL_SWEEPS, MEASURE_SWEEPS, MEASURE_EVERY, BIN_SIZE, MAX_PARALLEL
    },
    results
  }, null, 2));
  
  console.log(`Results saved to ${outputPath}`);
  
  // Summary table
  console.log('\n=== Summary: Susceptibility Peaks ===');
  for (const L of LATTICE_SIZES) {
    const lResults = results.filter(r => r.L === L);
    const maxChi = lResults.reduce((max, r) => r.susceptibility > max.susceptibility ? r : max, lResults[0]);
    console.log(`L=${L}: χ_max=${maxChi.susceptibility.toFixed(2)}±${maxChi.errorSusceptibility.toFixed(2)} at β=${maxChi.beta.toFixed(2)}`);
  }
  
  console.log('\n=== Summary: Binder Cumulant near β≈0.44 ===');
  for (const L of LATTICE_SIZES) {
    const lResults = results.filter(r => r.L === L && Math.abs(r.beta - 0.44) < 0.02);
    for (const r of lResults) {
      console.log(`L=${L} β=${r.beta.toFixed(2)}: U=${r.binderCumulant.toFixed(4)}±${r.errorBinderCumulant.toFixed(4)}`);
    }
  }
  
  console.log('\n=== EXPECTED BEHAVIOR (for validation) ===');
  console.log('1. ⟨P⟩ should increase from ~0 to ~1 as β increases');
  console.log('2. χ peak should grow with L (roughly L^(7/4) for 2D Ising)');
  console.log('3. U curves should approach each other near β≈0.44');
  console.log('4. For VALIDATION: errors will be large due to reduced statistics');
  console.log('   Run full simulation (100k+500k sweeps) for production results');
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
