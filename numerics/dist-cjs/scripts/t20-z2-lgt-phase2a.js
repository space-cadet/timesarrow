"use strict";
/**
 * T20 Phase 2A: Sharp Phase Transition via Multi-Lattice Finite-Size Scaling
 *
 * Simulates Z₂ LGT on multiple lattice sizes (L=8,16,32) with dense β grid
 * to show clear phase transition signatures:
 * - ⟨P⟩ vs β: crossover sharpens with L
 * - χ vs β: peak grows with L (diverges in thermodynamic limit)
 * - U vs β: curves cross at β_c ( Binder cumulant crossing)
 * - C vs β: peak behavior near β_c
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const ts_quantum_1 = require("ts-quantum");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// ─── Simulation Parameters ───
const LATTICE_SIZES = [8, 16, 32];
// Dense β grid: 0.30–0.60 with Δβ = 0.02
// Plus extra-fine near β_c (0.40–0.50): Δβ = 0.01
const BETA_COARSE = Array.from({ length: 16 }, (_, i) => 0.30 + i * 0.02); // 0.30, 0.32, ..., 0.60
const BETA_FINE = Array.from({ length: 11 }, (_, i) => 0.40 + i * 0.01); // 0.40, 0.41, ..., 0.50
// Merge and deduplicate
const BETA_VALUES = [...new Set([...BETA_COARSE, ...BETA_FINE])].sort((a, b) => a - b);
const THERMAL_SWEEPS = 100000;
const MEASURE_SWEEPS = 500000;
const MEASURE_EVERY = 10;
const BIN_SIZE = 100;
// Number of parallel simulations (M2 Air has 8 cores, use 6-7)
const MAX_PARALLEL = 6;
// ─── Run a single simulation ───
function runSimulation(params) {
    const { L, beta, thermalSweeps, measureSweeps, measureEvery, binSize } = params;
    const lattice = (0, ts_quantum_1.createSquareLattice)(L);
    const field = new ts_quantum_1.Z2GaugeField(lattice, 'random');
    const volume = L * L;
    // Thermalize
    const thermalRates = (0, ts_quantum_1.thermalize)(field, beta, thermalSweeps);
    const meanThermalRate = thermalRates.reduce((a, b) => a + b, 0) / thermalRates.length;
    // Measure: collect all moments per measurement
    const measurements = [];
    for (let s = 0; s < measureSweeps; s++) {
        (0, ts_quantum_1.metropolisSweep)(field, beta);
        if (s % measureEvery === 0) {
            const moments = (0, ts_quantum_1.averagePlaquetteMoments)(field);
            measurements.push({
                p: moments.mean,
                p2: moments.meanSq,
                p4: moments.meanFourth
            });
        }
    }
    // Extract arrays for binning
    const pValues = measurements.map(m => m.p);
    const p2Values = measurements.map(m => m.p2);
    const p4Values = measurements.map(m => m.p4);
    // Bin data to reduce autocorrelation
    const pBinned = (0, ts_quantum_1.binData)(pValues, binSize);
    const p2Binned = (0, ts_quantum_1.binData)(p2Values, binSize);
    const p4Binned = (0, ts_quantum_1.binData)(p4Values, binSize);
    // Compute means and jackknife errors from binned data
    const meanP = pBinned.reduce((a, b) => a + b, 0) / pBinned.length;
    const meanP2 = p2Binned.reduce((a, b) => a + b, 0) / p2Binned.length;
    const meanP4 = p4Binned.reduce((a, b) => a + b, 0) / p4Binned.length;
    const errorP = (0, ts_quantum_1.jackknifeError)(pBinned);
    const errorP2 = (0, ts_quantum_1.jackknifeError)(p2Binned);
    const errorP4 = (0, ts_quantum_1.jackknifeError)(p4Binned);
    // Compute derived observables for each bin (to get error estimates)
    const chiBinned = pBinned.map((p, i) => (0, ts_quantum_1.susceptibility)(p, p2Binned[i], volume));
    const cBinned = pBinned.map((p, i) => (0, ts_quantum_1.plaquetteSpecificHeat)(p, p2Binned[i], beta));
    const uBinned = pBinned.map((_, i) => (0, ts_quantum_1.binderCumulant)(Array(pBinned.length).fill(0).map((_, j) => j === i ? pBinned[j] : pBinned[j]) // hacky - need raw values
    ));
    // Better: compute χ, C, U from the binned P and P² values
    const chiValues = pBinned.map((p, i) => (0, ts_quantum_1.susceptibility)(p, p2Binned[i], volume));
    const cValues = pBinned.map((p, i) => (0, ts_quantum_1.plaquetteSpecificHeat)(p, p2Binned[i], beta));
    // For Binder cumulant, we need ⟨P⁴⟩ and ⟨P²⟩ per bin
    const uValues = p4Binned.map((p4, i) => 1 - p4 / (3 * p2Binned[i] * p2Binned[i]));
    const chi = chiValues.reduce((a, b) => a + b, 0) / chiValues.length;
    const c = cValues.reduce((a, b) => a + b, 0) / cValues.length;
    const u = uValues.reduce((a, b) => a + b, 0) / uValues.length;
    const errorChi = (0, ts_quantum_1.jackknifeError)(chiValues);
    const errorC = (0, ts_quantum_1.jackknifeError)(cValues);
    const errorU = (0, ts_quantum_1.jackknifeError)(uValues);
    return {
        L,
        beta,
        meanPlaquette: meanP,
        errorPlaquette: errorP,
        meanPlaquetteSq: meanP2,
        errorPlaquetteSq: errorP2,
        meanPlaquetteFourth: meanP4,
        errorPlaquetteFourth: errorP4,
        susceptibility: chi,
        errorSusceptibility: errorChi,
        specificHeat: c,
        errorSpecificHeat: errorC,
        binderCumulant: u,
        errorBinderCumulant: errorU,
        numMeasurements: measurements.length,
        numBinned: pBinned.length,
        acceptanceRate: meanThermalRate
    };
}
// ─── Main ───
async function main() {
    console.log('=== T20 Phase 2A: Z₂ LGT Multi-Lattice Finite-Size Scaling ===');
    console.log('Lattice sizes:', LATTICE_SIZES.join(', '));
    console.log('β values:', BETA_VALUES.length, 'points');
    console.log('β range:', BETA_VALUES[0].toFixed(2), 'to', BETA_VALUES[BETA_VALUES.length - 1].toFixed(2));
    console.log('Thermalization:', THERMAL_SWEEPS, 'sweeps');
    console.log('Measurement:', MEASURE_SWEEPS, 'sweeps (every', MEASURE_EVERY, ')');
    console.log('Parallel runs:', MAX_PARALLEL);
    console.log('');
    // Build all parameter combinations
    const allParams = [];
    for (const L of LATTICE_SIZES) {
        for (const beta of BETA_VALUES) {
            allParams.push({
                L,
                beta,
                thermalSweeps: THERMAL_SWEEPS,
                measureSweeps: MEASURE_SWEEPS,
                measureEvery: MEASURE_EVERY,
                binSize: BIN_SIZE
            });
        }
    }
    console.log(`Total simulations: ${allParams.length}`);
    console.log('');
    // Run in batches of MAX_PARALLEL
    const results = [];
    const startTime = Date.now();
    for (let i = 0; i < allParams.length; i += MAX_PARALLEL) {
        const batch = allParams.slice(i, i + MAX_PARALLEL);
        const batchNum = Math.floor(i / MAX_PARALLEL) + 1;
        const totalBatches = Math.ceil(allParams.length / MAX_PARALLEL);
        console.log(`Batch ${batchNum}/${totalBatches}: L=[${batch.map(p => p.L).join(',')}], β=[${batch.map(p => p.beta.toFixed(2)).join(',')}]`);
        // Run batch in parallel
        const batchResults = await Promise.all(batch.map(params => runSimulation(params)));
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
    const outputPath = path.join(outputDir, 't20-phase2a-finite-size.json');
    fs.writeFileSync(outputPath, JSON.stringify({
        timestamp: new Date().toISOString(),
        parameters: {
            LATTICE_SIZES,
            BETA_VALUES,
            THERMAL_SWEEPS,
            MEASURE_SWEEPS,
            MEASURE_EVERY,
            BIN_SIZE,
            MAX_PARALLEL
        },
        results
    }, null, 2));
    console.log(`Results saved to ${outputPath}`);
    // Print summary table
    console.log('\n=== Summary: Susceptibility Peaks ===');
    for (const L of LATTICE_SIZES) {
        const lResults = results.filter(r => r.L === L);
        const maxChi = lResults.reduce((max, r) => r.susceptibility > max.susceptibility ? r : max, lResults[0]);
        console.log(`L=${L}: χ_max=${maxChi.susceptibility.toFixed(2)}±${maxChi.errorSusceptibility.toFixed(2)} at β=${maxChi.beta.toFixed(2)}`);
    }
    console.log('\n=== Summary: Binder Cumulant at β≈0.44 ===');
    for (const L of LATTICE_SIZES) {
        const lResults = results.filter(r => r.L === L && Math.abs(r.beta - 0.44) < 0.02);
        for (const r of lResults) {
            console.log(`L=${L} β=${r.beta.toFixed(2)}: U=${r.binderCumulant.toFixed(4)}±${r.errorBinderCumulant.toFixed(4)}`);
        }
    }
}
main().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
//# sourceMappingURL=t20-z2-lgt-phase2a.js.map