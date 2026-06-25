/**
 * TimesArrow-specific intertwiner utilities
 *
 * Imports general-purpose functions from ts-quantum and adds
 * domain-specific logic for the timesarrow paper.
 */
import { IntertwinerSpace } from 'ts-quantum';
/**
 * Build 4-valent intertwiner basis for j=1/2 (paper's central case)
 * Returns |Φ₁⟩, |Φ₂⟩ states with corrected normalization from supplementary
 */
export declare function build4ValentIntertwiners(j?: number): IntertwinerSpace;
/**
 * Compute volume spectrum for n-valent vertex and check Z₂ structure
 *
 * @param n Valence
 * @param j Edge spin
 * @returns Spectrum with Z₂ diagnostic
 */
export declare function analyzeVolumeSpectrum(n: number, j: number): {
    eigenvalues: number[];
    hasZ2Structure: boolean;
    dimension: number;
};
//# sourceMappingURL=intertwiner.d.ts.map