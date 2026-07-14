#!/usr/bin/env python3
"""
⚠️  SUPERCEDED — This script computes an FK/EPRL vertex amplitude estimate that was
mislabeled. The calculation is actually a normalized SU(2) four-leg group average.

See: numerics/scripts/su2-four-leg-group-average-multi-spin.py
     for the corrected implementation.

Original description (retained for provenance):
T22a Quick Estimate: FK Vertex Amplitude Suppression

Compute |A_v(j=1)|² / |A_v(j=½)|² for a single 4-valent FK vertex
using Monte Carlo integration over SU(2) with Haar measure.
"""

import numpy as np
from numpy import sin, cos, sqrt, pi

def sample_su2_haar(n_samples: int) -> np.ndarray:
    """
    Sample n points from SU(2) with Haar measure.
    
    SU(2) elements: h = cos(θ/2) I + i sin(θ/2) n̂·σ
    Haar measure: dμ(h) = (1/2π²) sin²(θ/2) dθ dΩ
    
    Returns θ values (the class angle). The Haar measure only depends on θ
    for class functions (functions of conjugacy class).
    """
    # For class functions f(h) = f(θ), we integrate:
    # ∫ f(h) dh = (2/π) ∫_0^π f(θ) sin²(θ/2) dθ
    # 
    # To sample θ with PDF ∝ sin²(θ/2):
    # CDF: F(θ) = (θ - sin(θ)) / π  for θ ∈ [0, π]
    # Actually, let's use rejection sampling for simplicity
    
    samples = []
    while len(samples) < n_samples:
        # Proposal: uniform on [0, π]
        theta_prop = np.random.uniform(0, pi, size=n_samples*2)
        # Acceptance probability ∝ sin²(θ/2)
        accept_prob = sin(theta_prop/2)**2
        accepted = theta_prop[np.random.uniform(size=len(theta_prop)) < accept_prob]
        samples.extend(accepted)
    
    return np.array(samples[:n_samples])

def character_su2(j: float, theta: np.ndarray) -> np.ndarray:
    """
    SU(2) character for spin j at class angle θ.
    
    χ^j(θ) = sin((2j+1)θ/2) / sin(θ/2)
    
    For j = 1/2: χ(θ) = 2 cos(θ/2)
    """
    # Handle θ=0 carefully
    result = np.zeros_like(theta)
    nonzero = np.abs(sin(theta/2)) > 1e-10
    
    result[nonzero] = sin((2*j + 1) * theta[nonzero] / 2) / sin(theta[nonzero] / 2)
    result[~nonzero] = 2*j + 1  # Limit as θ→0
    
    return result

def compute_vertex_amplitude_sq(j: float, n_samples: int = 1_000_000) -> tuple:
    """
    Compute |A_v(j)|² for a 4-valent vertex with uniform spin j.
    
    For simple intertwiners, the vertex amplitude is:
    A_v(j) = ∫_{SU(2)} dh [χ^j(h)]⁴ / (2j+1)³
    
    The factor (2j+1)^{-3} comes from normalizing the intertwiner.
    
    Returns: (mean, std_error)
    """
    theta_samples = sample_su2_haar(n_samples)
    
    # Compute characters
    chi = character_su2(j, theta_samples)
    
    # Integrand: [χ^j(h)]⁴
    integrand = chi**4
    
    # Monte Carlo estimate
    # The Haar measure normalization: (2/π) for θ ∈ [0, π]
    # But we sampled with PDF ∝ sin²(θ/2), so we need to weight by the measure
    # Actually, our samples are uniformly distributed on [0, π] after rejection
    # Wait — let me redo this more carefully
    
    mean_val = np.mean(integrand)
    std_val = np.std(integrand) / sqrt(n_samples)
    
    # Normalize by intertwiner factor
    normalization = (2*j + 1)**3
    
    amplitude = mean_val / normalization
    error = std_val / normalization
    
    return amplitude, error

def compute_vertex_amplitude_sq_v2(j: float, n_samples: int = 1_000_000) -> tuple:
    """
    Cleaner implementation using direct integration.
    
    For a 4-valent vertex with simple intertwiners:
    A_v(j) = (1/(2j+1)³) × (2/π) ∫_0^π dθ sin²(θ/2) [χ^j(θ)]⁴
    
    We compute the integral using Monte Carlo with uniform θ sampling
    and proper weighting.
    """
    # Sample θ uniformly on [0, π]
    theta = np.random.uniform(0, pi, n_samples)
    
    # Character values
    chi = character_su2(j, theta)
    
    # Integrand with Haar measure weight: sin²(θ/2) × [χ^j(θ)]⁴
    integrand = sin(theta/2)**2 * chi**4
    
    # Monte Carlo average
    mc_mean = np.mean(integrand)
    mc_std = np.std(integrand) / sqrt(n_samples)
    
    # Multiply by measure factor (2/π) and normalize
    measure_factor = 2.0 / pi
    normalization = (2*j + 1)**3
    
    amplitude = measure_factor * mc_mean / normalization
    error = measure_factor * mc_std / normalization
    
    return amplitude, error

def main():
    print("=" * 60)
    print("T22a: FK Vertex Amplitude — Quick Estimate")
    print("=" * 60)
    print()
    
    n_samples = 1_000_000
    print(f"Monte Carlo samples: {n_samples:,}")
    print()
    
    # Compute for j = 1/2
    print("Computing j = 1/2 ...")
    a_half, err_half = compute_vertex_amplitude_sq_v2(0.5, n_samples)
    print(f"  |A_v(j=1/2)|² = {a_half:.6e} ± {err_half:.6e}")
    print()
    
    # Compute for j = 1
    print("Computing j = 1 ...")
    a_one, err_one = compute_vertex_amplitude_sq_v2(1.0, n_samples)
    print(f"  |A_v(j=1)|²   = {a_one:.6e} ± {err_one:.6e}")
    print()
    
    # Ratio
    ratio = a_one / a_half
    ratio_err = ratio * sqrt((err_one/a_one)**2 + (err_half/a_half)**2)
    
    print("-" * 60)
    print("RESULTS:")
    print("-" * 60)
    print(f"  |A_v(j=1)|² / |A_v(j=1/2)|² = {ratio:.6f} ± {ratio_err:.6f}")
    
    if ratio > 0:
        log_ratio = -np.log10(ratio)
        log_err = ratio_err / (ratio * np.log(10))
        print(f"  Suppression factor: 10^(-{log_ratio:.2f} ± {log_err:.2f})")
    
    print()
    print("Interpretation:")
    if ratio < 0.01:
        print("  → Strong suppression: j=1/2 dominance well-justified")
    elif ratio < 0.1:
        print("  → Moderate suppression: j=1/2 favored but not overwhelmingly")
    else:
        print("  → Weak suppression: j=1/2 dominance needs additional arguments")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
