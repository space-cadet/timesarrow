#!/usr/bin/env python3
"""
Critical exponent extraction via finite-size scaling.

For 3D Ising universality (3D Z2 LGT dual):
- ν ≈ 0.630 (correlation length exponent)
- γ ≈ 1.237 (susceptibility exponent)
- β ≈ 0.327 (order parameter exponent) — note: this is the exponent, not the coupling

Method: Peak height scaling of susceptibility
  χ_max(L) ~ L^(γ/ν)

Also: specific heat peak scaling
  C_max(L) ~ L^(α/ν) where α = 2 - dν = 2 - 3*0.630 = 0.110

And: shift of critical coupling
  β_c(L) - β_c(∞) ~ L^(-1/ν)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.plotting import (
    load_run,
    extract_observables,
    save_publication,
    setup_grid,
    FIG_SIZES,
    PATHS,
)

import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

OUTPUT_DIR = PATHS['docs_assets']
RUNS = {
    8:  't20-p3b-L8-3D-fine-20260627',
    16: 't20d-L16-fine-20260629',
    24: 't20d-L24-fine-20260629',
    32: 't20-p3b-L32-lean-20260627',
}

# Literature values for 3D Ising
BETA_C_INF = 0.7613
GAMMA_ISING = 1.237
NU_ISING = 0.630
ALPHA_ISING = 2 - 3 * NU_ISING  # = 0.110

# ─────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────

data = {}
for L, run_id in RUNS.items():
    d = load_run(run_id)
    obs = extract_observables(d['results'])
    data[L] = obs
    print(f"  Loaded L={L}: {len(obs['betas'])} β values")

# ─────────────────────────────────────────────────────────────
# Extract peak values
# ─────────────────────────────────────────────────────────────

results = {}
for L, obs in data.items():
    # Peak of susceptibility
    peak_idx = np.argmax(obs['susceptibilities'])
    beta_peak_chi = obs['betas'][peak_idx]
    chi_max = obs['susceptibilities'][peak_idx]

    # Peak of specific heat
    peak_idx_c = np.argmax(obs['specific_heats'])
    beta_peak_c = obs['betas'][peak_idx_c]
    c_max = obs['specific_heats'][peak_idx_c]

    results[L] = {
        'beta_peak_chi': beta_peak_chi,
        'chi_max': chi_max,
        'beta_peak_c': beta_peak_c,
        'c_max': c_max,
    }

# ─────────────────────────────────────────────────────────────
# Print summary table
# ─────────────────────────────────────────────────────────────

print("=" * 60)
print("CRITICAL EXPONENT EXTRACTION")
print("3D Z2 LGT — Finite-size scaling")
print("=" * 60)
print(f"\n{'L':<6} {'β_c(χ)':<10} {'χ_max':<12} {'β_c(C)':<10} {'C_max':<12}")
print("-" * 60)
for L in sorted(results):
    r = results[L]
    print(f"{L:<6} {r['beta_peak_chi']:<10.4f} {r['chi_max']:<12.4f} {r['beta_peak_c']:<10.4f} {r['c_max']:<12.4f}")

# ─────────────────────────────────────────────────────────────
# Power-law fits
# ─────────────────────────────────────────────────────────────

L_vals = np.array(sorted(results), dtype=float)
chi_max_vals = np.array([results[L]['chi_max'] for L in sorted(results)])
c_max_vals = np.array([results[L]['c_max'] for L in sorted(results)])
beta_c_vals = np.array([results[L]['beta_peak_chi'] for L in sorted(results)])

log_L = np.log(L_vals)
log_chi = np.log(chi_max_vals)
log_c = np.log(c_max_vals)

# χ_max ~ L^(γ/ν)
coeffs_chi = np.polyfit(log_L, log_chi, 1)
gamma_over_nu = coeffs_chi[0]
chi_prefactor = np.exp(coeffs_chi[1])

# C_max ~ L^(α/ν)
coeffs_c = np.polyfit(log_L, log_c, 1)
alpha_over_nu = coeffs_c[0]
c_prefactor = np.exp(coeffs_c[1])

# β_c shift: β_c(L) - β_c(∞) ~ L^(-1/ν)
delta_beta = beta_c_vals - BETA_C_INF
coeffs_beta = np.polyfit(log_L, np.log(np.abs(delta_beta)), 1)
minus_one_over_nu = coeffs_beta[0]
nu_from_shift = -1 / minus_one_over_nu

# ─────────────────────────────────────────────────────────────
# Print fit results
# ─────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print("FINITE-SIZE SCALING FITS")
print(f"{'='*60}")
print(f"\nχ_max scaling: χ_max = {chi_prefactor:.3f} * L^{gamma_over_nu:.3f}")
print(f"  γ/ν (fitted) = {gamma_over_nu:.3f}")
print(f"  γ/ν (3D Ising) = {GAMMA_ISING/NU_ISING:.3f}")
print(f"  Deviation: {gamma_over_nu - GAMMA_ISING/NU_ISING:+.3f}")

print(f"\nC_max scaling: C_max = {c_prefactor:.3f} * L^{alpha_over_nu:.3f}")
print(f"  α/ν (fitted) = {alpha_over_nu:.3f}")
print(f"  α/ν (3D Ising, α=2-3ν) = {ALPHA_ISING/NU_ISING:.3f}")
print(f"  Deviation: {alpha_over_nu - ALPHA_ISING/NU_ISING:+.3f}")

print(f"\nβ_c shift: β_c(L) - β_c(∞) ~ L^{minus_one_over_nu:.3f}")
print(f"  -1/ν (fitted) = {minus_one_over_nu:.3f}")
print(f"  -1/ν (3D Ising, ν=0.630) = {-1/NU_ISING:.3f}")
print(f"  ν (from shift) = {nu_from_shift:.3f}")
print(f"  ν (3D Ising) = {NU_ISING}")
print(f"  Deviation: {nu_from_shift - NU_ISING:+.3f}")

# ─────────────────────────────────────────────────────────────
# Plot: Scaling fits
# ─────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=FIG_SIZES['wide'])

L_fit = np.linspace(3, 20, 100)

# χ_max vs L
ax = axes[0]
ax.plot(L_vals, chi_max_vals, 'ko', markersize=10, label='Data')
ax.plot(L_fit, chi_prefactor * L_fit**gamma_over_nu, 'r--', linewidth=1.5, alpha=0.7,
        label=f'Fit: χ ~ L^{gamma_over_nu:.2f}')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$\chi_{\max}(L)$', fontsize=12)
ax.set_title(r'Susceptibility peak scaling', fontsize=12)
setup_grid(ax)
ax.legend(fontsize=9)

# C_max vs L
ax = axes[1]
ax.plot(L_vals, c_max_vals, 'ko', markersize=10, label='Data')
ax.plot(L_fit, c_prefactor * L_fit**alpha_over_nu, 'r--', linewidth=1.5, alpha=0.7,
        label=f'Fit: C ~ L^{alpha_over_nu:.2f}')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$C_{V,\max}(L)$', fontsize=12)
ax.set_title(r'Specific heat peak scaling', fontsize=12)
setup_grid(ax)
ax.legend(fontsize=9)

# β_c(L) vs L
ax = axes[2]
ax.plot(L_vals, beta_c_vals, 'ko', markersize=10, label=r'$\beta_c$ from $\chi_{peak}$')
ax.axhline(BETA_C_INF, color='gray', linestyle=':', linewidth=2, alpha=0.7, label=f'β_c(∞) = {BETA_C_INF}')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$\beta_c(L)$', fontsize=12)
ax.set_title(r'Critical coupling shift', fontsize=12)
ax.set_ylim(0.70, 0.78)
setup_grid(ax)
ax.legend(fontsize=9)

plt.tight_layout()
save_publication(fig, 't20-critical-exponents', output_dir=OUTPUT_DIR)
plt.close()

print(f"\nFigure saved: t20-critical-exponents.png")

# ─────────────────────────────────────────────────────────────
# Consistency check
# ─────────────────────────────────────────────────────────────

nu_from_chi = GAMMA_ISING / gamma_over_nu

print(f"\n{'='*60}")
print("CONSISTENCY CHECK")
print(f"{'='*60}")
print(f"\nAssuming γ = {GAMMA_ISING} (3D Ising):")
print(f"  ν from χ scaling = γ / (γ/ν) = {nu_from_chi:.3f}")
print(f"  ν from β_c shift = {nu_from_shift:.3f}")
print(f"  ν (3D Ising) = {NU_ISING}")
print(f"  Consistency: |Δν| = {abs(nu_from_chi - nu_from_shift):.3f}")

if abs(nu_from_chi - nu_from_shift) < 0.1:
    print(f"  ✓ Exponents are consistent (|Δν| < 0.1)")
else:
    print(f"  ⚠ Exponents differ significantly — need larger L")
