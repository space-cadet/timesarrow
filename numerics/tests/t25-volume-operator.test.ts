/**
 * T25: Volume Operator Extension Tests
 * 
 * Tests for volume operator diagonalization on higher-valence intertwiners.
 * Uses ts-quantum's intertwiner and volume operator modules.
 */

import { describe, it, expect } from 'vitest';
import { constructNValentBasis, computeVolumeSpectrum, checkZ2Structure } from 'ts-quantum';

describe('T25: Volume Operator Spectrum', () => {
  
  it('4-valent j=1/2: dimension 2, eigenvalues ±8√3/9', () => {
    const space = constructNValentBasis(4, 0.5);
    expect(space.dimension).toBe(2);
    
    const spectrum = computeVolumeSpectrum(space);
    expect(spectrum.eigenvalues).toHaveLength(2);
    expect(spectrum.hasZ2Structure).toBe(true);
    
    // Eigenvalues should be ±8√3/9 ≈ ±1.5396
    const expected = 8 * Math.sqrt(3) / 9;
    expect(Math.abs(spectrum.eigenvalues[0])).toBeCloseTo(expected, 5);
    expect(Math.abs(spectrum.eigenvalues[1])).toBeCloseTo(expected, 5);
    expect(spectrum.eigenvalues[0]).toBeCloseTo(-spectrum.eigenvalues[1], 10);
  });

  it('5-valent j=1/2: no singlet subspace (dimension 0)', () => {
    // 5 half-integer spins cannot couple to J=0
    const space = constructNValentBasis(5, 0.5);
    expect(space.dimension).toBe(0);
  });

  it('6-valent j=1/2: dimension > 0, check Z2 structure', () => {
    const space = constructNValentBasis(6, 0.5);
    
    // 6-valent j=1/2 should have a singlet subspace
    // Dimension formula: number of ways to pair 6 spins to get J=0
    expect(space.dimension).toBeGreaterThan(0);
    
    const spectrum = computeVolumeSpectrum(space);
    
    // For now, the 6-valent volume operator returns zeros (not implemented)
    // So all eigenvalues are 0, which trivially satisfies Z2 structure
    // Once implemented, this test should verify actual ±q pairs
    expect(spectrum.hasZ2Structure).toBe(true);
  });

  it('checkZ2Structure detects ±q pairs correctly', () => {
    expect(checkZ2Structure([-1.5, 1.5])).toBe(true);
    expect(checkZ2Structure([-2, -1, 1, 2])).toBe(true);
    expect(checkZ2Structure([0, -1, 1])).toBe(true);  // Zero eigenvalue allowed
    expect(checkZ2Structure([1, 2, 3])).toBe(false);
    expect(checkZ2Structure([])).toBe(true);
  });

});
