"use strict";
/**
 * T20 Phase 1: Z₂ LGT Monte Carlo on 2D Square Lattice
 *
 * Parameter sweep to locate critical coupling β_c ≈ 0.4407
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
// Simulation parameters
const L = 16; // Lattice size
const thermalSweeps = 10000; // Thermalization sweeps
const measureSweeps = 100000; // Measurement sweeps
const measureEvery = 10; // Measure every N sweeps
const binSize = 100; // Bin size for error analysis
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
    const lattice = (0, ts_quantum_1.createSquareLattice)(L);
    const field = new ts_quantum_1.Z2GaugeField(lattice, 'random');
    // Thermalize
    (0, ts_quantum_1.thermalize)(field, beta, thermalSweeps);
    // Measure
    const measurements = [];
    for (let s = 0; s < measureSweeps; s++) {
        (0, ts_quantum_1.metropolisSweep)(field, beta);
        if (s % measureEvery === 0) {
            measurements.push((0, ts_quantum_1.averagePlaquette)(field));
        }
    }
    // Bin data to reduce autocorrelation
    const binned = (0, ts_quantum_1.binData)(measurements, binSize);
    // Compute statistics
    const mean = binned.reduce((a, b) => a + b, 0) / binned.length;
    const error = (0, ts_quantum_1.jackknifeError)(binned);
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
//# sourceMappingURL=t20-z2-lgt-phase1.js.map