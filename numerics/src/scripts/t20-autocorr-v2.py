#!/usr/bin/env python3
"""
T20-Autocorr-v2: Autocorrelation time measurement using Rust binary with worker threads.

This script runs the Rust simulation with --raw-output to get raw time series,
then computes integrated autocorrelation times (τ_int) for the plaquette observable.

Uses the Rust binary with worker threads for proper CPU parallelism.

Usage:
    python3 t20-autocorr-v2.py

Outputs:
    - JSON with autocorrelation times per (L, β)
    - Figures showing autocorrelation functions
"""

import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

# ─── CONFIGURATION ───────────────────────────────────────────────────────────

RUST_BINARY = Path('/Users/sage/.openclaw/workspace/code/timesarrow/rust-lattice/target/release/z2-lattice-gauge')
OUTPUT_DIR = Path('/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output')
RESULTS_FILE = OUTPUT_DIR / 't20-autocorr-v2-results.json'
FIGURES_DIR = OUTPUT_DIR / 'figures'

# Lattice sizes and beta values near critical point (β_c ≈ 0.74-0.76 for 3D Z2 LGT)
LATTICE_SIZES = [8, 16, 24, 32]
BETA_VALUES = [0.70, 0.72, 0.74, 0.76, 0.78, 0.80]

# Simulation parameters
THERMAL_SWEEPS = 10000
MEASURE_SWEEPS = 100000
MEASURE_EVERY = 10
WORKERS = 8  # Use all cores

# ─── RUN RUST SIMULATION ───────────────────────────────────────────────────

def run_simulation_raw(L, beta, thermal, measure, workers, seed=42):
    """Run Rust binary with --raw-output and return raw plaquette measurements."""
    cmd = [
        str(RUST_BINARY),
        str(L), '3',
        str(measure), str(thermal),
        str(workers),
        '1x1',
        str(beta),
        '--raw-output',
        '--seed', str(seed)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: Rust binary failed for L={L}, β={beta}")
        print(f"  stderr: {result.stderr[:500]}")
        return None
    
    try:
        data = json.loads(result.stdout)
        # Extract raw plaquette measurements from first (and only) result entry
        raw = data['results'][0]['rawPlaquettes']
        return np.array(raw, dtype=np.float64)
    except Exception as e:
        print(f"  ERROR parsing JSON for L={L}, β={beta}: {e}")
        return None

# ─── AUTOCORRELATION ANALYSIS ──────────────────────────────────────────────

def autocorrelation_function(observable, max_lag=None):
    """Compute normalized autocorrelation function C(t)/C(0)."""
    x = np.asarray(observable, dtype=np.float64)
    N = len(x)
    if max_lag is None:
        max_lag = min(N // 4, 2000)
    max_lag = min(max_lag, N - 1)

    x_mean = np.mean(x)
    x_centered = x - x_mean
    C0 = np.dot(x_centered, x_centered) / N
    if C0 == 0:
        return np.arange(max_lag + 1), np.zeros(max_lag + 1)

    rho = np.zeros(max_lag + 1)
    rho[0] = 1.0
    for t in range(1, max_lag + 1):
        rho[t] = np.dot(x_centered[:N-t], x_centered[t:]) / (N - t) / C0
    return np.arange(max_lag + 1), rho


def integrated_autocorrelation(observable, cutoff_method='standard'):
    """Compute integrated autocorrelation time τ_int."""
    x = np.asarray(observable, dtype=np.float64)
    N = len(x)
    lags, rho = autocorrelation_function(x, max_lag=min(N // 4, 2000))

    if cutoff_method == 'standard':
        threshold = 2.0 / math.sqrt(N)
        cutoff = 0
        for t in range(1, len(rho)):
            if rho[t] < 0 or rho[t] < threshold:
                cutoff = max(0, t - 1)
                break
            cutoff = t
        tau_int = 0.5 + np.sum(rho[1:cutoff + 1])
        tau_int_err = tau_int * math.sqrt(2 * (2 * cutoff + 1) / N)
    elif cutoff_method == 'sokal':
        c = 6.0
        tau_int = 0.5
        cutoff = 0
        for t in range(1, len(rho)):
            if t > c * tau_int:
                cutoff = t - 1
                break
            tau_int += rho[t]
            cutoff = t
        tau_int = 0.5 + np.sum(rho[1:cutoff + 1])
        tau_int_err = tau_int * math.sqrt(2 * (2 * cutoff + 1) / N)
    else:
        raise ValueError(f"Unknown cutoff method: {cutoff_method}")

    return tau_int, tau_int_err, cutoff, rho, lags

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("T20-Autocorr-v2: Raw time series autocorrelation analysis")
    print("Using Rust binary with worker threads for simulation")
    print("=" * 60)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for L in LATTICE_SIZES:
        print(f"\n--- L = {L} ---")
        for beta in BETA_VALUES:
            print(f"  β = {beta:.2f} ...", end=" ", flush=True)
            start = time.time()
            
            raw = run_simulation_raw(L, beta, THERMAL_SWEEPS, MEASURE_SWEEPS, WORKERS, seed=42)
            if raw is None:
                continue
            
            tau_std, err_std, cut_std, rho_std, lags_std = integrated_autocorrelation(raw, 'standard')
            tau_sokal, err_sokal, cut_sokal, rho_sokal, lags_sokal = integrated_autocorrelation(raw, 'sokal')
            
            N_eff_std = len(raw) / (2 * tau_std)
            N_eff_sokal = len(raw) / (2 * tau_sokal)
            
            elapsed = time.time() - start
            print(f"done ({elapsed:.1f}s). τ_int = {tau_std:.2f} ± {err_std:.2f} (std), {tau_sokal:.2f} ± {err_sokal:.2f} (sokal)")
            
            results.append({
                'L': L,
                'beta': beta,
                'N_measurements': len(raw),
                'tau_int_standard': tau_std,
                'tau_int_standard_err': err_std,
                'tau_int_sokal': tau_sokal,
                'tau_int_sokal_err': err_sokal,
                'cutoff_standard': cut_std,
                'cutoff_sokal': cut_sokal,
                'N_eff_standard': N_eff_std,
                'N_eff_sokal': N_eff_sokal,
                'mean_plaquette': float(np.mean(raw)),
                'std_plaquette': float(np.std(raw)),
            })
    
    # Save results
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to {RESULTS_FILE}")
    
    # Summary table
    print("\n" + "=" * 60)
    print("SUMMARY: Autocorrelation times τ_int")
    print("=" * 60)
    print(f"{'L':>3} {'β':>5} {'τ_int(std)':>10} {'err':>8} {'τ_int(sokal)':>12} {'err':>8} {'N_eff':>8}")
    print("-" * 60)
    for r in results:
        print(f"{r['L']:>3} {r['beta']:>5.2f} {r['tau_int_standard']:>10.2f} {r['tau_int_standard_err']:>8.2f} "
              f"{r['tau_int_sokal']:>12.2f} {r['tau_int_sokal_err']:>8.2f} {r['N_eff_standard']:>8.0f}")
    
    print("\n" + "=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)
    
    # Find max tau_int
    max_tau = max(results, key=lambda r: r['tau_int_standard'])
    print(f"Maximum τ_int: {max_tau['tau_int_standard']:.2f} ± {max_tau['tau_int_standard_err']:.2f} "
          f"at L={max_tau['L']}, β={max_tau['beta']:.2f}")
    
    # Estimate required sweeps
    print(f"\nRecommended minimum sweeps for reliable statistics:")
    print(f"  Conservative (10 × τ_int × measure_every): {10 * max_tau['tau_int_standard'] * MEASURE_EVERY:.0f} sweeps")
    print(f"  Aggressive (5 × τ_int × measure_every):   {5 * max_tau['tau_int_standard'] * MEASURE_EVERY:.0f} sweeps")
    
    return results

if __name__ == '__main__':
    main()
