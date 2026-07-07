#!/usr/bin/env python3
"""
SU(2) Four-Leg Group-Average Calculation

Computes the normalized SU(2) Haar integral of a product of four characters
for identical spin-j representations. This is a group-average toy calculation,
NOT a complete FK/EPRL spin-foam vertex amplitude.

Analytic result (primary method):
    I(j) = ∫_{SU(2)} dh [χ^j(h)]^4 = 2j + 1

    Normalized: I_norm(j) = I(j) / (2j+1)^3 = 1 / (2j+1)^2

    Ratio j=1 / j=1/2 = (2/3)^2 = 4/9 ≈ 0.444...

Monte Carlo is used only as a validation check against the exact analytic result.
"""

import numpy as np
from numpy import sin, sqrt, pi

def character_su2(j: float, theta: np.ndarray) -> np.ndarray:
    """SU(2) character for spin j at class angle θ.
    
    χ^j(θ) = sin((2j+1)θ/2) / sin(θ/2)    for θ ≠ 0
    χ^j(0) = 2j + 1                         (dimension)
    """
    result = np.zeros_like(theta)
    nonzero = np.abs(sin(theta/2)) > 1e-10
    result[nonzero] = sin((2*j + 1) * theta[nonzero] / 2) / sin(theta[nonzero] / 2)
    result[~nonzero] = 2*j + 1
    return result

def analytic_integral(j: float) -> float:
    """
    Analytic result for the unnormalized SU(2) character integral.
    
    Using the Clebsch-Gordan series:
        χ^j(h)^2 = Σ_{J=0}^{2j} χ^J(h)
    
    Therefore:
        χ^j(h)^4 = [Σ_{J=0}^{2j} χ^J(h)] [Σ_{K=0}^{2j} χ^K(h)]
                 = Σ_{J,K=0}^{2j} χ^J(h) χ^K(h)
    
    By orthogonality of characters:
        ∫_{SU(2)} dh χ^J(h) χ^K(h) = δ_{JK}
    
    Hence:
        I(j) = ∫_{SU(2)} dh [χ^j(h)]^4 = Σ_{J=0}^{2j} 1 = 2j + 1
    
    Returns the unnormalized integral I(j).
    """
    return 2*j + 1

def normalized_group_average(j: float) -> float:
    """
    Normalized group average with the (2j+1)^{-3} factor.
    
    This is the factor that would appear in a simple-intertwiner
    normalization, included here for consistency with the original
    Monte Carlo estimate. The normalized value is:
    
        G(j) = I(j) / (2j+1)^3 = 1 / (2j+1)^2
    
    Returns the exact normalized value.
    """
    return 1.0 / (2*j + 1)**2

def monte_carlo_check(j: float, n_samples: int = 1_000_000, seed: int = 42) -> tuple:
    """
    Monte Carlo validation of the analytic result.
    
    Samples θ uniformly on [0, π] and integrates with the Haar measure
    weight sin²(θ/2).
    
    Returns: (mc_estimate, mc_error, exact_value, relative_error)
    """
    np.random.seed(seed)
    theta = np.random.uniform(0, pi, n_samples)
    chi = character_su2(j, theta)
    
    # Integrand with Haar measure weight: sin²(θ/2) [χ^j(θ)]^4
    integrand = sin(theta/2)**2 * chi**4
    
    mc_mean = np.mean(integrand)
    mc_std = np.std(integrand) / sqrt(n_samples)
    
    # For uniform sampling on [0,π]:
    #   E[sin²(θ/2) χ^4] = (1/π) ∫_0^π sin²(θ/2) [χ]^4 dθ
    #   True integral = (2/π) ∫_0^π sin²(θ/2) [χ]^4 dθ = 2 × E[sin²(θ/2) χ^4]
    measure_factor = 2.0
    
    # Unnormalized integral estimate
    I_mc = measure_factor * mc_mean
    I_err = measure_factor * mc_std
    
    # Normalized value
    normalization = (2*j + 1)**3
    G_mc = I_mc / normalization
    G_err = I_err / normalization
    
    # Exact values for comparison
    I_exact = analytic_integral(j)
    G_exact = normalized_group_average(j)
    
    rel_err_I = abs(I_mc - I_exact) / I_exact
    rel_err_G = abs(G_mc - G_exact) / G_exact
    
    return G_mc, G_err, G_exact, rel_err_G

def main():
    print("=" * 70)
    print("SU(2) Four-Leg Group-Average Calculation")
    print("=" * 70)
    print()
    print("WARNING: This is a TOY calculation — a normalized group average.")
    print("It is NOT a complete FK/EPRL spin-foam vertex amplitude.")
    print("It does NOT establish j=1/2 dominance for any physical model.")
    print()
    print("-" * 70)
    print("Analytic Derivation")
    print("-" * 70)
    print()
    print("For identical spin-j irreps, the SU(2) Haar integral of four")
    print("characters reduces via Clebsch-Gordan decomposition:")
    print()
    print("  χ^j(h)^2 = Σ_{J=0}^{2j} χ^J(h)")
    print()
    print("  I(j) = ∫ dh [χ^j(h)]^4")
    print("       = Σ_{J,K=0}^{2j} ∫ dh χ^J(h) χ^K(h)")
    print("       = Σ_{J=0}^{2j} 1          (by orthogonality)")
    print("       = 2j + 1")
    print()
    print("With (2j+1)^{-3} normalization:")
    print("  G(j) = I(j) / (2j+1)^3 = 1 / (2j+1)^2")
    print()
    print("-" * 70)
    print("Exact Results")
    print("-" * 70)
    print()
    
    spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    for j in spins:
        I = analytic_integral(j)
        G = normalized_group_average(j)
        print(f"  j = {j:>4.1f}:  I(j) = {I:>6.1f},  G(j) = 1/(2j+1)² = {G:.6f}")
    
    print()
    print("-" * 70)
    print("Monte Carlo Validation (1M samples)")
    print("-" * 70)
    print()
    
    n_samples = 1_000_000
    for j in spins:
        G_mc, G_err, G_exact, rel_err = monte_carlo_check(j, n_samples)
        print(f"  j = {j:>4.1f}:  MC = {G_mc:.6f} ± {G_err:.6f},  "
              f"exact = {G_exact:.6f},  rel_err = {rel_err:.4%}")
    
    print()
    print("-" * 70)
    print("Key Ratio: j=1 / j=1/2")
    print("-" * 70)
    print()
    
    R_exact = normalized_group_average(1.0) / normalized_group_average(0.5)
    print(f"  Exact:  R = (1/9) / (1/4) = 4/9 = {R_exact:.6f}")
    print()
    
    G1_mc, G1_err, _, _ = monte_carlo_check(1.0, n_samples)
    Gh_mc, Gh_err, _, _ = monte_carlo_check(0.5, n_samples)
    R_mc = G1_mc / Gh_mc
    R_err = R_mc * sqrt((G1_err/G1_mc)**2 + (Gh_err/Gh_mc)**2)
    print(f"  MC:     R = {R_mc:.6f} ± {R_err:.6f}")
    print()
    
    print("=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print()
    print("This script computes a normalized SU(2) group average:")
    print("  G(j) = (2j+1)^{-3} ∫_{SU(2)} dh [χ^j(h)]^4 = 1/(2j+1)^2")
    print()
    print("The ratio R = G(1)/G(1/2) = 4/9 ≈ 0.444 is the CORRECT output.")
    print("There is NO extra squaring step. The ~0.45 ratio is exact.")
    print()
    print("This is a useful code check and analytic exercise, but it is NOT:")
    print("  - A complete FK or EPRL spin-foam vertex amplitude")
    print("  - Evidence for j=1/2 dominance in a physical model")
    print("  - A substitute for the full intertwiner, Immirzi, and")
    print("    face-amplitude structure of a real spin-foam model")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
