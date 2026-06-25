/**
 * TimesArrow-specific intertwiner utilities
 *
 * Imports general-purpose functions from ts-quantum and adds
 * domain-specific logic for the timesarrow paper.
 */
import { constructNValentBasis, computeVolumeSpectrum } from 'ts-quantum';
/**
 * Build 4-valent intertwiner basis for j=1/2 (paper's central case)
 * Returns |Φ₁⟩, |Φ₂⟩ states with corrected normalization from supplementary
 */
export function build4ValentIntertwiners(j = 0.5) {
    return constructNValentBasis(4, j);
}
/**
 * Compute volume spectrum for n-valent vertex and check Z₂ structure
 *
 * @param n Valence
 * @param j Edge spin
 * @returns Spectrum with Z₂ diagnostic
 */
export function analyzeVolumeSpectrum(n, j) {
    const space = constructNValentBasis(n, j);
    const { eigenvalues, hasZ2Structure, dimension } = computeVolumeSpectrum(space);
    return { eigenvalues, hasZ2Structure, dimension };
}
//# sourceMappingURL=intertwiner.js.map