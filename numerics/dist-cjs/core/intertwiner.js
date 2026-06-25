"use strict";
/**
 * TimesArrow-specific intertwiner utilities
 *
 * Imports general-purpose functions from ts-quantum and adds
 * domain-specific logic for the timesarrow paper.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.build4ValentIntertwiners = build4ValentIntertwiners;
exports.analyzeVolumeSpectrum = analyzeVolumeSpectrum;
const ts_quantum_1 = require("ts-quantum");
/**
 * Build 4-valent intertwiner basis for j=1/2 (paper's central case)
 * Returns |Φ₁⟩, |Φ₂⟩ states with corrected normalization from supplementary
 */
function build4ValentIntertwiners(j = 0.5) {
    return (0, ts_quantum_1.constructNValentBasis)(4, j);
}
/**
 * Compute volume spectrum for n-valent vertex and check Z₂ structure
 *
 * @param n Valence
 * @param j Edge spin
 * @returns Spectrum with Z₂ diagnostic
 */
function analyzeVolumeSpectrum(n, j) {
    const space = (0, ts_quantum_1.constructNValentBasis)(n, j);
    const { eigenvalues, hasZ2Structure, dimension } = (0, ts_quantum_1.computeVolumeSpectrum)(space);
    return { eigenvalues, hasZ2Structure, dimension };
}
//# sourceMappingURL=intertwiner.js.map