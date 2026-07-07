#!/usr/bin/env python3
"""
SU(2) Four-Leg Group Average — Multi-Spin Scan

Computes the normalized SU(2) Haar integral of four characters
for spins j = 1/2 to 3. Analytic result is primary; Monte Carlo
is used only as validation.

WARNING: This is a group-average toy calculation, NOT a complete
FK/EPRL spin-foam vertex amplitude. It does NOT establish j=1/2
dominance for any physical model.
"""

import numpy as np
from numpy import sin, sqrt
import json
from pathlib import Path
from datetime import datetime, timezone

def character_su2(j: float, theta: np.ndarray) -> np.ndarray:
    """SU(2) character for spin j at class angle θ."""
    result = np.zeros_like(theta)
    nonzero = np.abs(sin(theta/2)) > 1e-10
    result[nonzero] = sin((2*j + 1) * theta[nonzero] / 2) / sin(theta[nonzero] / 2)
    result[~nonzero] = 2*j + 1
    return result

def analytic_integral(j: float) -> float:
    """Exact unnormalized integral: I(j) = ∫ dh [χ^j(h)]^4 = 2j + 1."""
    return 2*j + 1

def normalized_group_average(j: float) -> float:
    """Exact normalized value: G(j) = I(j) / (2j+1)^3 = 1/(2j+1)^2."""
    return 1.0 / (2*j + 1)**2

def monte_carlo_check(j: float, n_samples: int = 2_000_000, seed: int = 42) -> dict:
    """
    Monte Carlo validation against the exact analytic result.
    
    Samples θ uniformly on [0, π] and integrates with the Haar measure
    weight sin²(θ/2). The exact integral is 2 × E[sin²(θ/2) [χ^j]⁴].
    """
    np.random.seed(seed)
    theta = np.random.uniform(0, np.pi, n_samples)
    chi = character_su2(j, theta)
    integrand = sin(theta/2)**2 * chi**4
    
    mc_mean = np.mean(integrand)
    mc_std = np.std(integrand) / sqrt(n_samples)
    
    # For uniform sampling on [0,π]: true integral = 2 × E[integrand]
    I_mc = 2.0 * mc_mean
    I_err = 2.0 * mc_std
    
    normalization = (2*j + 1)**3
    G_mc = I_mc / normalization
    G_err = I_err / normalization
    
    G_exact = normalized_group_average(j)
    rel_err = abs(G_mc - G_exact) / G_exact
    
    return {
        "j": j,
        "analytic": float(G_exact),
        "mc_estimate": float(G_mc),
        "mc_error": float(G_err),
        "relative_error": float(rel_err),
        "n_samples": n_samples,
        "seed": seed
    }

def main():
    print("=" * 70)
    print("SU(2) Four-Leg Group Average — Multi-Spin Scan")
    print("=" * 70)
    print()
    print("WARNING: This is a TOY group-average calculation.")
    print("It is NOT a complete FK/EPRL spin-foam vertex amplitude.")
    print()
    
    spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    n_samples = 2_000_000
    
    print(f"Spins: {spins}")
    print(f"Samples per spin: {n_samples:,}")
    print()
    
    results = []
    baseline = None
    
    for j in spins:
        print(f"Computing j = {j} ...", end=" ")
        res = monte_carlo_check(j, n_samples)
        results.append(res)
        
        if j == 0.5:
            baseline = res["analytic"]
        
        ratio = res["analytic"] / baseline
        print(f"G_exact = {res['analytic']:.6f}, MC = {res['mc_estimate']:.6f} "
              f"± {res['mc_error']:.2e}, R = {ratio:.4f}")
    
    print()
    print("-" * 70)
    print("SUMMARY")
    print("-" * 70)
    
    baseline_val = results[0]["analytic"]
    for res in results:
        j = res["j"]
        G_exact = res["analytic"]
        G_mc = res["mc_estimate"]
        G_err = res["mc_error"]
        ratio = G_exact / baseline_val
        ratio_err = ratio * sqrt((G_err/G_mc)**2 + (results[0]["mc_error"]/results[0]["mc_estimate"])**2)
        
        print(f"  j = {j:>4.1f}: G_exact = {G_exact:.6f}, "
              f"MC = {G_mc:.6f} ± {G_err:.2e},  R = {ratio:.4f} ± {ratio_err:.4f}")
    
    print()
    
    # Fit power law: G(j) ~ j^{-alpha} for j >= 1
    js = np.array([r["j"] for r in results[1:]])
    Gs = np.array([r["analytic"] for r in results[1:]])
    log_js = np.log(js)
    log_Gs = np.log(Gs)
    
    coeffs = np.polyfit(log_js, log_Gs, 1)
    alpha = -coeffs[0]
    c = coeffs[1]
    
    print(f"Power law fit (j >= 1): G(j) ~ j^(-{alpha:.2f})")
    print(f"  (Exact: G(j) = 1/(2j+1)^2 ~ 1/(4j^2) = 0.25 j^{-2} for large j)")
    print()
    
    # --- Save data ---
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    run_id = "su2-four-leg-group-average-multi-spin-20260708"
    
    data = {
        "taskId": "T22a-reclassified",
        "runId": run_id,
        "description": "SU(2) four-leg group average G(j) = (2j+1)^{-3} ∫ dh [χ^j(h)]^4 = 1/(2j+1)^2 for spins j=1/2 to 3. Analytic result primary; MC validation only.",
        "warning": "This is a TOY group-average calculation, NOT a complete FK/EPRL spin-foam vertex amplitude. It does NOT establish j=1/2 dominance.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "calculation_type": "SU(2) four-leg group average (normalized)",
        "parameters": {
            "n_samples": n_samples,
            "spins": spins,
            "seed": 42
        },
        "analytic_result": {
            "formula": "G(j) = 1 / (2j+1)^2",
            "derivation": "∫ dh [χ^j]^4 = 2j+1 via Clebsch-Gordan; normalize by (2j+1)^3"
        },
        "results": results,
        "analysis": {
            "baseline_j": 0.5,
            "exact_ratio_j1_to_j_half": float(normalized_group_average(1.0) / normalized_group_average(0.5)),
            "power_law_fit": {
                "valid_for": "j >= 1",
                "exponent_alpha": float(alpha),
                "prefactor_log_c": float(c),
                "formula": f"G(j) ~ {np.exp(c):.4e} * j^(-{alpha:.2f})"
            },
            "key_findings": [
                f"Exact j=1/2: G = {results[0]['analytic']:.6f}",
                f"Exact j=1: G = {results[1]['analytic']:.6f}",
                f"Exact ratio j=1/j=1/2 = 4/9 = {results[1]['analytic']/results[0]['analytic']:.6f}",
                f"Asymptotic: G(j) ~ 1/(4j^2) for large j"
            ]
        }
    }
    
    output_path = output_dir / f"{run_id}.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to: {output_path}")
    print()
    print("=" * 70)
    
    return data

if __name__ == "__main__":
    main()
