"use strict";
/**
 * T25 Data Generation Script
 *
 * Computes volume operator spectrum for n=4,5,6 valent intertwiners
 * and saves results to JSON.
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
const outputDir = path.join(__dirname, '..', 'output');
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}
const results = [];
// 4-valent j=1/2
console.log('Computing 4-valent j=1/2...');
const space4 = (0, ts_quantum_1.constructNValentBasis)(4, 0.5);
const spec4 = (0, ts_quantum_1.computeVolumeSpectrum)(space4);
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
const space5 = (0, ts_quantum_1.constructNValentBasis)(5, 0.5);
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
const embedding = (0, ts_quantum_1.buildGeneric6ValentEmbedding)();
const space6 = (0, ts_quantum_1.constructNValentBasis)(6, 0.5);
const spec6 = (0, ts_quantum_1.computeVolumeSpectrum)(space6, embedding);
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
//# sourceMappingURL=generate-t25-data.js.map