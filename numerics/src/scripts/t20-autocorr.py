#!/usr/bin/env python3
"""
T20-Autocorr: Autocorrelation time measurement for Z2 lattice gauge theory.

This script computes integrated autocorrelation times (τ_int) for observables
in the 3D Z2 LGT simulation. Without autocorrelation correction, error bars
are underestimated by factor ~√τ_int.

Usage:
    python3 t20-autocorr.py

Outputs:
    - Autocorrelation times for plaquette, susceptibility, and energy
    - Effective independent sample sizes
    - Corrected error bars
    - JSON file with raw results

Note: Existing Phase 3 data files are binned and do NOT contain raw time series.
This script includes a lightweight Python simulation to generate raw data for
demonstration. For production analysis, the Rust simulation should be modified
to output raw measurements (unbinned).

Author: Sage (subagent for T20-Phase3b Blocker 4)
"""

import json
import math
import os
import random
import sys
import time
from pathlib import Path

import numpy as np

# ─── CONFIGURATION ───────────────────────────────────────────────────────────

OUTPUT_DIR = Path('/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output')
RESULTS_FILE = OUTPUT_DIR / 't20-autocorr-results.json'
RAW_DATA_FILE = OUTPUT_DIR / 't20-autocorr-raw-data.json'

# Lattice sizes and beta values near critical point (β_c ≈ 0.74-0.76 for 3D Z2 LGT)
LATTICE_SIZES = [8, 16, 32]
BETA_VALUES = {
    8: [0.74, 0.76],
    16: [0.74, 0.76],
    32: [0.74, 0.76],
}

# DEMONSTRATION parameters. Python is ~1000× slower than Rust.
# For production-quality τ_int, much longer runs are needed.
THERMAL_SWEEPS = {
    8: 5000,
    16: 1000,   # Very short for demo speed
    32: 200,    # Very short for demo speed
}
MEASURE_SWEEPS = {
    8: 10000,
    16: 2000,   # ~200 measurements
    32: 500,    # ~50 measurements
}
MEASURE_EVERY = 10
SEED = 42


# ─── AUTOCORRELATION FUNCTIONS ────────────────────────────────────────────

def autocorrelation_function(observable, max_lag=None):
    """
    Compute the normalized autocorrelation function C(t)/C(0) for t = 0..max_lag.

    Uses FFT-based convolution for O(N log N) speed when N is large,
    falling back to direct summation for small N.

    Args:
        observable: 1D array of measurements
        max_lag: maximum lag to compute (default: N//4, capped at 2000)

    Returns:
        lags: array of lag values
        rho: normalized autocorrelation values
    """
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

    # For small N, direct computation is fine
    if N <= 5000:
        rho = np.zeros(max_lag + 1)
        rho[0] = 1.0
        for t in range(1, max_lag + 1):
            rho[t] = np.dot(x_centered[:N-t], x_centered[t:]) / (N - t) / C0
        return np.arange(max_lag + 1), rho

    # For larger N, use FFT-based autocorrelation
    x_padded = np.concatenate([x_centered, np.zeros(N - 1)])
    Xf = np.fft.rfft(x_padded)
    corr = np.fft.irfft(Xf * np.conjugate(Xf))
    corr = corr[:max_lag + 1] / (N - np.arange(max_lag + 1))
    rho = corr / C0
    return np.arange(max_lag + 1), rho


def integrated_autocorrelation(observable, cutoff_method='standard'):
    """
    Compute integrated autocorrelation time τ_int.

    Standard formula: τ_int = 0.5 + Σ_{t=1}^{cutoff} C(t)/C(0)

    Cutoff methods:
        'standard': Cut when C(t) < 0 or C(t) < 2/√N (whichever comes first)
        'sokal': Sokal's adaptive cutoff (c = 6, window = c*τ_int)

    Args:
        observable: 1D array of measurements
        cutoff_method: 'standard' or 'sokal'

    Returns:
        tau_int: integrated autocorrelation time
        tau_int_err: error estimate on τ_int
        cutoff: lag at which summation was truncated
        rho: normalized autocorrelation function (full array, up to max_lag)
        lags: lag values
    """
    x = np.asarray(observable, dtype=np.float64)
    N = len(x)

    lags, rho = autocorrelation_function(x, max_lag=min(N // 4, 2000))

    if cutoff_method == 'standard':
        # Cut when C(t) < 0 or C(t) < 2/√N
        threshold = 2.0 / math.sqrt(N)
        cutoff = 0
        for t in range(1, len(rho)):
            if rho[t] < 0 or rho[t] < threshold:
                cutoff = max(0, t - 1)
                break
            cutoff = t

        tau_int = 0.5 + np.sum(rho[1:cutoff + 1])
        # Error estimate
        tau_int_err = math.sqrt(2 * (2 * cutoff + 1) * tau_int / N) * tau_int

    elif cutoff_method == 'sokal':
        # Sokal's adaptive cutoff method
        c = 6.0
        tau_int = 0.5
        M = 1
        max_iter = 50

        for _ in range(max_iter):
            M_new = max(1, int(c * tau_int))
            M_new = min(M_new, len(rho) - 1)
            if M_new == M:
                break
            M = M_new
            tau_int = 0.5 + np.sum(rho[1:M + 1])

        cutoff = M
        # Sokal's error estimate: sqrt(2*(2c+1)*tau_int/N) * tau_int
        tau_int_err = math.sqrt(2 * (2 * c + 1) * tau_int / N) * tau_int

    else:
        raise ValueError(f"Unknown cutoff_method: {cutoff_method}")

    return float(tau_int), float(tau_int_err), int(cutoff), rho, lags


def compute_corrected_error(observable, tau_int=None):
    """
    Compute corrected error bar accounting for autocorrelation.

    σ_corrected = σ_naive * √τ_int = σ / √(N_eff) where N_eff = N / τ_int

    Args:
        observable: 1D array of measurements
        tau_int: precomputed autocorrelation time (optional)

    Returns:
        mean, naive_error, corrected_error, tau_int, N_eff
    """
    x = np.asarray(observable, dtype=np.float64)
    N = len(x)
    mean = float(np.mean(x))
    variance = float(np.var(x, ddof=1))
    naive_error = math.sqrt(variance / N)

    if tau_int is None:
        tau_int, _, _, _, _ = integrated_autocorrelation(x, cutoff_method='standard')

    tau_int = max(float(tau_int), 0.5)
    N_eff = N / tau_int
    corrected_error = math.sqrt(variance / N_eff)

    return mean, naive_error, corrected_error, tau_int, N_eff


# ─── Z2 LGT SIMULATION (Python) ───────────────────────────────────────────

class Z2GaugeField3D:
    """
    Lightweight 3D Z2 lattice gauge field simulation in Python.
    Matches the Rust implementation's dynamics and sign conventions.

    NOTE: This is ~1000× slower than the Rust implementation.
    For production runs with L ≥ 16, use the Rust binary with raw output.
    """

    def __init__(self, L, seed=42):
        self.L = L
        self.rng = random.Random(seed)
        np.random.seed(seed)
        # links[x, y, z, dir] where dir = 0 (x), 1 (y), 2 (z)
        self.links = np.random.choice([-1, 1], size=(L, L, L, 3))

    def plaquette_xy(self, x, y, z):
        """XY plaquette at (x, y, z)."""
        L = self.L
        xp1 = (x + 1) % L
        yp1 = (y + 1) % L
        return (self.links[x, y, z, 0] * self.links[xp1, y, z, 1] *
                self.links[x, yp1, z, 0] * self.links[x, y, z, 1])

    def plaquette_yz(self, x, y, z):
        """YZ plaquette at (x, y, z)."""
        L = self.L
        yp1 = (y + 1) % L
        zp1 = (z + 1) % L
        return (self.links[x, y, z, 1] * self.links[x, yp1, z, 2] *
                self.links[x, y, zp1, 1] * self.links[x, y, z, 2])

    def plaquette_xz(self, x, y, z):
        """XZ plaquette at (x, y, z)."""
        L = self.L
        xp1 = (x + 1) % L
        zp1 = (z + 1) % L
        return (self.links[x, y, z, 0] * self.links[xp1, y, z, 2] *
                self.links[x, y, zp1, 0] * self.links[x, y, z, 2])

    def _delta_sum_x(self, x, y, z):
        """Sum of plaquettes containing x-link at (x,y,z)."""
        L = self.L
        ym = (y + L - 1) % L
        zm = (z + L - 1) % L
        return (self.plaquette_xy(x, y, z) +
                self.plaquette_xy(x, ym, z) +
                self.plaquette_xz(x, y, z) +
                self.plaquette_xz(x, y, zm))

    def _delta_sum_y(self, x, y, z):
        """Sum of plaquettes containing y-link at (x,y,z)."""
        L = self.L
        xm = (x + L - 1) % L
        zm = (z + L - 1) % L
        return (self.plaquette_xy(x, y, z) +
                self.plaquette_xy(xm, y, z) +
                self.plaquette_yz(x, y, z) +
                self.plaquette_yz(x, y, zm))

    def _delta_sum_z(self, x, y, z):
        """Sum of plaquettes containing z-link at (x,y,z)."""
        L = self.L
        xm = (x + L - 1) % L
        ym = (y + L - 1) % L
        return (self.plaquette_xz(x, y, z) +
                self.plaquette_xz(xm, y, z) +
                self.plaquette_yz(x, y, z) +
                self.plaquette_yz(x, ym, z))

    def sweep(self, beta):
        """One Metropolis sweep over all links. Returns acceptance count."""
        L = self.L
        accepted = 0
        beta2 = 2.0 * beta

        for z in range(L):
            for y in range(L):
                for x in range(L):
                    # x-link
                    delta_sum = self._delta_sum_x(x, y, z)
                    delta_e = -beta2 * float(delta_sum)
                    if delta_e <= 0.0 or self.rng.random() < math.exp(-delta_e):
                        self.links[x, y, z, 0] *= -1
                        accepted += 1

                    # y-link
                    delta_sum = self._delta_sum_y(x, y, z)
                    delta_e = -beta2 * float(delta_sum)
                    if delta_e <= 0.0 or self.rng.random() < math.exp(-delta_e):
                        self.links[x, y, z, 1] *= -1
                        accepted += 1

                    # z-link
                    delta_sum = self._delta_sum_z(x, y, z)
                    delta_e = -beta2 * float(delta_sum)
                    if delta_e <= 0.0 or self.rng.random() < math.exp(-delta_e):
                        self.links[x, y, z, 2] *= -1
                        accepted += 1

        return accepted

    def thermalize(self, beta, n_sweeps):
        """Thermalize the lattice."""
        for i in range(n_sweeps):
            self.sweep(beta)
            if (i + 1) % 1000 == 0 or n_sweeps < 1000:
                if n_sweeps >= 1000:
                    print(f"      Thermalization: {i+1}/{n_sweeps} sweeps...", end='\r', file=sys.stderr)
        print(file=sys.stderr)

    def measure_plaquette(self):
        """Mean plaquette (negated to match Rust convention)."""
        L = self.L
        total = 0
        for z in range(L):
            for y in range(L):
                for x in range(L):
                    xp = (x + 1) % L
                    yp = (y + 1) % L
                    zp = (z + 1) % L
                    total += (self.links[x, y, z, 0] * self.links[xp, y, z, 1] *
                              self.links[x, yp, z, 0] * self.links[x, y, z, 1])
                    total += (self.links[x, y, z, 1] * self.links[x, yp, z, 2] *
                              self.links[x, y, zp, 1] * self.links[x, y, z, 2])
                    total += (self.links[x, y, z, 0] * self.links[xp, y, z, 2] *
                              self.links[x, y, zp, 0] * self.links[x, y, z, 2])
        n_plaquettes = 3 * L * L * L
        return -float(total) / n_plaquettes

    def run_simulation(self, beta, thermal_sweeps, measure_sweeps, measure_every):
        """Run simulation and return time series of measurements."""
        self.thermalize(beta, thermal_sweeps)

        plaquettes = []
        print("      Measuring...", end='\r', file=sys.stderr)

        for sweep in range(measure_sweeps):
            self.sweep(beta)
            if sweep % measure_every == 0:
                p = self.measure_plaquette()
                plaquettes.append(p)
            if (sweep + 1) % 1000 == 0 or measure_sweeps < 1000:
                if measure_sweeps >= 1000:
                    pct = 100 * (sweep + 1) / measure_sweeps
                    print(f"      Measurement: {sweep+1}/{measure_sweeps} sweeps ({pct:.0f}%)...", end='\r', file=sys.stderr)
        print(file=sys.stderr)

        return np.array(plaquettes)


# ─── WRAPPER: RUN ANALYSIS ────────────────────────────────────────────────

def analyze_autocorrelation(L, beta, thermal_sweeps, measure_sweeps, measure_every, seed):
    """Run simulation and compute autocorrelation times for all observables."""
    print(f"\n{'='*60}")
    print(f"Running L={L}, β={beta:.2f}")
    print(f"  Thermalization: {thermal_sweeps:,} sweeps")
    print(f"  Measurement: {measure_sweeps:,} sweeps (every {measure_every})")
    print(f"  Expected measurements: {measure_sweeps // measure_every:,}")

    start = time.time()
    field = Z2GaugeField3D(L, seed=seed)
    plaquettes = field.run_simulation(
        beta, thermal_sweeps, measure_sweeps, measure_every
    )
    sim_time = time.time() - start
    print(f"  Simulation time: {sim_time:.1f}s")

    N = len(plaquettes)
    volume = L ** 3

    # For susceptibility, compute from block averages
    block_size = max(1, N // 100)
    n_blocks = N // block_size
    susceptibilities = []
    for i in range(n_blocks):
        block = plaquettes[i * block_size:(i + 1) * block_size]
        p_mean = np.mean(block)
        p_var = np.var(block, ddof=1)
        susceptibilities.append(volume * beta * p_var)
    susceptibilities = np.array(susceptibilities)

    # Energy density: -plaquette
    energies = -plaquettes

    results = {}

    # Analyze plaquette
    print(f"\n  Plaquette analysis (N={N}):")
    tau_std, tau_std_err, cutoff_std, rho, lags = integrated_autocorrelation(
        plaquettes, cutoff_method='standard'
    )
    tau_sokal, tau_sokal_err, cutoff_sokal, _, _ = integrated_autocorrelation(
        plaquettes, cutoff_method='sokal'
    )
    mean_p, naive_err, corr_err, tau_combined, N_eff = compute_corrected_error(
        plaquettes, tau_int=(tau_std + tau_sokal) / 2
    )

    print(f"    Mean: {mean_p:.6f} ± {naive_err:.6f} (naive)")
    print(f"    Corrected: {mean_p:.6f} ± {corr_err:.6f} (×{corr_err/naive_err:.2f} larger)")
    print(f"    τ_int (standard): {tau_std:.2f} ± {tau_std_err:.2f} (cutoff={cutoff_std})")
    print(f"    τ_int (Sokal):    {tau_sokal:.2f} ± {tau_sokal_err:.2f} (cutoff={cutoff_sokal})")
    print(f"    N_eff: {N_eff:.1f} (from {N} measurements)")

    results['plaquette'] = {
        'mean': float(mean_p),
        'naive_error': float(naive_err),
        'corrected_error': float(corr_err),
        'tau_int_standard': float(tau_std),
        'tau_int_standard_err': float(tau_std_err),
        'tau_int_sokal': float(tau_sokal),
        'tau_int_sokal_err': float(tau_sokal_err),
        'N_eff': float(N_eff),
    }

    # Analyze energy
    print(f"\n  Energy analysis:")
    tau_std_e, tau_std_err_e, cutoff_std_e, _, _ = integrated_autocorrelation(
        energies, cutoff_method='standard'
    )
    tau_sokal_e, tau_sokal_err_e, cutoff_sokal_e, _, _ = integrated_autocorrelation(
        energies, cutoff_method='sokal'
    )
    mean_e, naive_err_e, corr_err_e, tau_combined_e, N_eff_e = compute_corrected_error(
        energies, tau_int=(tau_std_e + tau_sokal_e) / 2
    )

    print(f"    Mean: {mean_e:.6f} ± {naive_err_e:.6f} (naive)")
    print(f"    Corrected: {mean_e:.6f} ± {corr_err_e:.6f} (×{corr_err_e/naive_err_e:.2f} larger)")
    print(f"    τ_int (standard): {tau_std_e:.2f} ± {tau_std_err_e:.2f}")
    print(f"    τ_int (Sokal):    {tau_sokal_e:.2f} ± {tau_sokal_err_e:.2f}")
    print(f"    N_eff: {N_eff_e:.1f}")

    results['energy'] = {
        'mean': float(mean_e),
        'naive_error': float(naive_err_e),
        'corrected_error': float(corr_err_e),
        'tau_int_standard': float(tau_std_e),
        'tau_int_standard_err': float(tau_std_err_e),
        'tau_int_sokal': float(tau_sokal_e),
        'tau_int_sokal_err': float(tau_sokal_err_e),
        'N_eff': float(N_eff_e),
    }

    # Analyze susceptibility (from block estimates)
    print(f"\n  Susceptibility analysis (N_blocks={len(susceptibilities)}):")
    tau_std_chi, tau_std_err_chi, cutoff_std_chi, _, _ = integrated_autocorrelation(
        susceptibilities, cutoff_method='standard'
    )
    tau_sokal_chi, tau_sokal_err_chi, cutoff_sokal_chi, _, _ = integrated_autocorrelation(
        susceptibilities, cutoff_method='sokal'
    )
    mean_chi, naive_err_chi, corr_err_chi, tau_combined_chi, N_eff_chi = compute_corrected_error(
        susceptibilities, tau_int=(tau_std_chi + tau_sokal_chi) / 2
    )

    print(f"    Mean: {mean_chi:.4f} ± {naive_err_chi:.4f} (naive)")
    print(f"    Corrected: {mean_chi:.4f} ± {corr_err_chi:.4f} (×{corr_err_chi/naive_err_chi:.2f} larger)")
    print(f"    τ_int (standard): {tau_std_chi:.2f} ± {tau_std_err_chi:.2f}")
    print(f"    τ_int (Sokal):    {tau_sokal_chi:.2f} ± {tau_sokal_err_chi:.2f}")
    print(f"    N_eff: {N_eff_chi:.1f}")

    results['susceptibility'] = {
        'mean': float(mean_chi),
        'naive_error': float(naive_err_chi),
        'corrected_error': float(corr_err_chi),
        'tau_int_standard': float(tau_std_chi),
        'tau_int_standard_err': float(tau_std_err_chi),
        'tau_int_sokal': float(tau_sokal_chi),
        'tau_int_sokal_err': float(tau_sokal_err_chi),
        'N_eff': float(N_eff_chi),
    }

    # Save autocorrelation function for plotting
    results['autocorr'] = {
        'lags': lags[:min(200, len(lags))].tolist(),
        'rho': rho[:min(200, len(rho))].tolist(),
    }

    # Save raw time series for potential re-analysis
    results['raw'] = {
        'plaquettes': plaquettes.tolist(),
    }

    return results


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    print("="*60)
    print("T20-Autocorr: Autocorrelation Time Measurement")
    print("3D Z2 Lattice Gauge Theory — Phase 3 Blocker 4")
    print("="*60)
    print()
    print("NOTE: This script uses a DEMONSTRATION Python simulation.")
    print("      For production, the Rust binary should be modified to output")
    print("      raw (unbinned) measurements per sweep.")
    print()
    print("      Parameters are REDUCED for demonstration speed.")
    print("      Expected τ_int near β_c: L=8 ~ O(10), L=16 ~ O(50), L=32 ~ O(200+)")
    print()

    all_results = {
        'metadata': {
            'description': 'Autocorrelation analysis for T20 Phase 3 data',
            'thermal_sweeps': THERMAL_SWEEPS,
            'measure_sweeps': MEASURE_SWEEPS,
            'measure_every': MEASURE_EVERY,
            'note': (
                'Raw time series generated by Python simulation for testing. '
                'Sweep counts are REDUCED for demonstration (Python ~1000x slower than Rust). '
                'For production: L=8 needs ~100k sweeps, L=16 needs ~200k, L=32 needs ~500k+.'
            ),
        },
        'results': []
    }

    for L in LATTICE_SIZES:
        for beta in BETA_VALUES[L]:
            seed = SEED + L + int(beta * 100)
            result = analyze_autocorrelation(
                L, beta,
                THERMAL_SWEEPS[L],
                MEASURE_SWEEPS[L],
                MEASURE_EVERY,
                seed
            )
            result['L'] = L
            result['beta'] = beta
            all_results['results'].append(result)

            # Save incremental results after each run
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(RESULTS_FILE, 'w') as f:
                json.dump(all_results, f, indent=2)

    # Also save raw time series separately
    raw_data = {
        'metadata': all_results['metadata'],
        'runs': [
            {
                'L': r['L'],
                'beta': r['beta'],
                'plaquettes': r['raw']['plaquettes'],
            }
            for r in all_results['results']
        ]
    }
    with open(RAW_DATA_FILE, 'w') as f:
        json.dump(raw_data, f, indent=2)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"\nResults saved to: {RESULTS_FILE}")
    print(f"Raw time series: {RAW_DATA_FILE}")
    print(f"\n{'L':>4} {'β':>6} {'Observable':>15} {'τ_int':>8} {'N_eff':>10} {'Error factor':>12}")
    print("-" * 60)

    for r in all_results['results']:
        L = r['L']
        beta = r['beta']
        for obs_name in ['plaquette', 'energy', 'susceptibility']:
            obs = r[obs_name]
            tau = obs['tau_int_standard']
            N_eff = obs['N_eff']
            factor = obs['corrected_error'] / obs['naive_error']
            print(f"{L:>4} {beta:>6.2f} {obs_name:>15} {tau:>8.1f} {N_eff:>10.1f} {factor:>12.2f}×")

    print(f"\n{'='*60}")
    print("KEY FINDINGS:")
    print(f"{'='*60}")

    # Find largest tau_int
    max_tau = 0
    max_entry = None
    for r in all_results['results']:
        for obs_name in ['plaquette', 'energy', 'susceptibility']:
            tau = r[obs_name]['tau_int_standard']
            if tau > max_tau:
                max_tau = tau
                max_entry = (r['L'], r['beta'], obs_name, tau)

    if max_entry:
        L, beta, obs, tau = max_entry
        print(f"\n  Largest measured τ_int: {tau:.1f} for {obs} at L={L}, β={beta:.2f}")
        print(f"  Error bars are underestimated by factor √{tau:.1f} = {math.sqrt(tau):.1f}")

    print(f"\n  {'='*60}")
    print("  CRITICAL SLOWING DOWN SCALING:")
    print(f"  {'='*60}")
    print("  For Metropolis algorithm in 3D Z2 LGT, τ_int ~ L^z with z ≈ 2.0")
    print("  Expected values near β_c:")
    print("    L=8:   τ_int ~ 10-30  sweeps  →  ~300-1000 independent samples from 10k meas")
    print("    L=16:  τ_int ~ 50-100 sweeps  →  ~100-200 independent samples from 10k meas")
    print("    L=32:  τ_int ~ 200-500 sweeps →  ~20-50 independent samples from 10k meas")
    print()
    print("  Current Phase 3 runs: 100k sweeps, measure every 10 → 10k measurements")
    print("  At L=32 near β_c with τ_int ~ 200 sweeps = 20 measurements:")
    print("    N_eff = 10000 / 20 = 500 independent samples")
    print("    Error bars are √20 ≈ 4.5× larger than currently reported")
    print()
    print("  RECOMMENDATIONS:")
    print("  1. For production: modify Rust simulation to output raw measurements")
    print("  2. Increase sweeps to at least 10× τ_int per measurement point")
    print("  3. For L=32 near β_c: need ~1M sweeps (100k measurements) for ~5k ind. samples")
    print("  4. Consider cluster/update algorithms (Swendsen-Wang, Wolff) to reduce z")
    print(f"  {'='*60}")


if __name__ == '__main__':
    main()
