#!/usr/bin/env python3
"""
T22a Quick Estimate: FK Vertex Amplitude Suppression — Multi-Spin

Compute |A_v(j)|² for j = 1/2, 1, 3/2, 2, 5/2, 3
and save results in timesarrow data format.
"""

import numpy as np
from numpy import sin, cos, sqrt, pi
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

def compute_vertex_amplitude_sq(j: float, n_samples: int = 1_000_000, seed: int = 42) -> dict:
    """
    Compute |A_v(j)|² for a 4-valent vertex with uniform spin j.
    
    A_v(j) = (2/π) ∫_0^π dθ sin²(θ/2) [χ^j(θ)]⁴ / (2j+1)³
    """
    np.random.seed(seed)
    theta = np.random.uniform(0, pi, n_samples)
    chi = character_su2(j, theta)
    integrand = sin(theta/2)**2 * chi**4
    
    mc_mean = np.mean(integrand)
    mc_std = np.std(integrand) / sqrt(n_samples)
    
    measure_factor = 2.0 / pi
    normalization = (2*j + 1)**3
    
    amplitude = measure_factor * mc_mean / normalization
    error = measure_factor * mc_std / normalization
    
    return {
        "j": j,
        "amplitude_sq": float(amplitude),
        "error": float(error),
        "n_samples": n_samples,
        "seed": seed
    }

def main():
    print("=" * 70)
    print("T22a: FK Vertex Amplitude — Multi-Spin Scan")
    print("=" * 70)
    print()
    
    spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    n_samples = 2_000_000  # More samples for better precision
    
    print(f"Spins: {spins}")
    print(f"Samples per spin: {n_samples:,}")
    print()
    
    results = []
    baseline = None
    
    for j in spins:
        print(f"Computing j = {j} ...", end=" ")
        res = compute_vertex_amplitude_sq(j, n_samples)
        results.append(res)
        
        if j == 0.5:
            baseline = res["amplitude_sq"]
        
        ratio = res["amplitude_sq"] / baseline if baseline else 1.0
        print(f"|A_v|² = {res['amplitude_sq']:.4e}, ratio_to_j_half = {ratio:.4f}")
    
    print()
    print("-" * 70)
    print("SUMMARY")
    print("-" * 70)
    
    # Ratios relative to j=1/2
    baseline_val = results[0]["amplitude_sq"]
    for res in results:
        j = res["j"]
        a = res["amplitude_sq"]
        err = res["error"]
        ratio = a / baseline_val
        ratio_err = ratio * sqrt((err/a)**2 + (results[0]["error"]/baseline_val)**2)
        
        if ratio > 0:
            log_sup = -np.log10(ratio)
            print(f"  j = {j:>4.1f}: |A_v|² = {a:.4e} ± {err:.2e},  R = {ratio:.4f} ± {ratio_err:.4f},  10^(-{log_sup:.2f})")
        else:
            print(f"  j = {j:>4.1f}: |A_v|² = {a:.4e} ± {err:.2e},  R = {ratio:.4f}")
    
    print()
    
    # Fit power law: A_v ~ j^{-alpha} for j >= 1
    js = np.array([r["j"] for r in results[1:]])  # exclude j=1/2
    amps = np.array([r["amplitude_sq"] for r in results[1:]])
    log_js = np.log(js)
    log_amps = np.log(amps)
    
    # Linear fit: log(A) = c - alpha * log(j)
    coeffs = np.polyfit(log_js, log_amps, 1)
    alpha = -coeffs[0]
    c = coeffs[1]
    
    print(f"Power law fit (j >= 1): A_v ~ j^(-{alpha:.2f})")
    print()
    
    # --- Save data in timesarrow format ---
    
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    run_id = "t22a-fk-vertex-multi-spin-20260628"
    
    data = {
        "taskId": "T22a",
        "runId": run_id,
        "description": "FK vertex amplitude |A_v(j)|² for spins j=1/2 to 3, 4-valent vertex, simple intertwiners",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": "FK",
        "vertex": "4-valent",
        "intertwiner": "simple",
        "parameters": {
            "n_samples": n_samples,
            "spins": spins,
            "seed": 42
        },
        "results": results,
        "analysis": {
            "baseline_j": 0.5,
            "power_law_fit": {
                "valid_for": "j >= 1",
                "exponent_alpha": float(alpha),
                "prefactor_log_c": float(c),
                "formula": f"|A_v(j)|² ~ {np.exp(c):.4e} * j^(-{alpha:.2f})"
            },
            "key_findings": [
                f"j=1/2 amplitude: {results[0]['amplitude_sq']:.4e}",
                f"j=1 amplitude: {results[1]['amplitude_sq']:.4e}",
                f"Suppression j=1 vs j=1/2: {results[1]['amplitude_sq']/results[0]['amplitude_sq']:.4f}",
                f"Asymptotic scaling: A_v ~ j^(-{alpha:.2f})"
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
