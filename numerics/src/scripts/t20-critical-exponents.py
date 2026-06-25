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

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar
import os

out_dir = '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets'
os.makedirs(out_dir, exist_ok=True)

# Load data
lattices = {
    'L=4': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L4-3D-wilson-fine-20250626.json',
    'L=6': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L6-3D-wilson-fine-20250626.json',
    'L=8': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L8-3D-wilson-fine-20250626.json',
}

colors = {'L=4': '#E94F37', 'L=6': '#2E86AB', 'L=8': '#2ECC40'}

# Parse data
data = {}
for label, path in lattices.items():
    with open(path) as f:
        d = json.load(f)
    results = d['results']
    data[label] = {
        'betas': np.array([r['beta'] for r in results]),
        'plaquettes': np.array([r['meanPlaquette'] for r in results]),
        'suscepts': np.array([r['susceptibility'] for r in results]),
        'specific_heats': np.array([r['specificHeat'] for r in results]),
    }

# Extract peak values for each L
results = {}
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    L = int(label.split('=')[1])
    
    # Find peak of susceptibility
    peak_idx = np.argmax(d['suscepts'])
    beta_peak_chi = d['betas'][peak_idx]
    chi_max = d['suscepts'][peak_idx]
    
    # Find peak of specific heat
    peak_idx_c = np.argmax(d['specific_heats'])
    beta_peak_c = d['betas'][peak_idx_c]
    c_max = d['specific_heats'][peak_idx_c]
    
    results[L] = {
        'beta_peak_chi': beta_peak_chi,
        'chi_max': chi_max,
        'beta_peak_c': beta_peak_c,
        'c_max': c_max,
    }

print("=" * 60)
print("CRITICAL EXPONENT EXTRACTION")
print("3D Z2 LGT — Finite-size scaling")
print("=" * 60)
print(f"\n{'L':<6} {'β_c(χ)':<10} {'χ_max':<12} {'β_c(C)':<10} {'C_max':<12}")
print("-" * 60)
for L in [4, 6, 8]:
    r = results[L]
    print(f"{L:<6} {r['beta_peak_chi']:<10.4f} {r['chi_max']:<12.4f} {r['beta_peak_c']:<10.4f} {r['c_max']:<12.4f}")

# --- Fit χ_max ~ L^(γ/ν) ---
L_vals = np.array([4, 6, 8], dtype=float)
chi_max_vals = np.array([results[L]['chi_max'] for L in [4, 6, 8]])
c_max_vals = np.array([results[L]['c_max'] for L in [4, 6, 8]])
beta_c_vals = np.array([results[L]['beta_peak_chi'] for L in [4, 6, 8]])

log_L = np.log(L_vals)
log_chi = np.log(chi_max_vals)
log_c = np.log(c_max_vals)

# Linear fit: log(χ_max) = a + (γ/ν)*log(L)
coeffs_chi = np.polyfit(log_L, log_chi, 1)
gamma_over_nu = coeffs_chi[0]
chi_prefactor = np.exp(coeffs_chi[1])

# For specific heat: C_max ~ L^(α/ν) where α = 2 - dν
coeffs_c = np.polyfit(log_L, log_c, 1)
alpha_over_nu = coeffs_c[0]
c_prefactor = np.exp(coeffs_c[1])

# β_c shift: β_c(L) - β_c(∞) ~ L^(-1/ν)
# We need β_c(∞) from literature: 0.7613
beta_c_inf = 0.7613
delta_beta = beta_c_vals - beta_c_inf
coeffs_beta = np.polyfit(log_L, np.log(np.abs(delta_beta)), 1)
minus_one_over_nu = coeffs_beta[0]
nu_from_shift = -1 / minus_one_over_nu

print(f"\n{'='*60}")
print("FINITE-SIZE SCALING FITS")
print(f"{'='*60}")
print(f"\nχ_max scaling: χ_max = {chi_prefactor:.3f} * L^{gamma_over_nu:.3f}")
print(f"  γ/ν (fitted) = {gamma_over_nu:.3f}")
print(f"  γ/ν (3D Ising) = {1.237/0.630:.3f}")
print(f"  Deviation: {gamma_over_nu - 1.237/0.630:+.3f}")

print(f"\nC_max scaling: C_max = {c_prefactor:.3f} * L^{alpha_over_nu:.3f}")
print(f"  α/ν (fitted) = {alpha_over_nu:.3f}")
print(f"  α/ν (3D Ising, α=2-3ν) = {(2-3*0.630)/0.630:.3f}")
print(f"  Deviation: {alpha_over_nu - (2-3*0.630)/0.630:+.3f}")

print(f"\nβ_c shift: β_c(L) - β_c(∞) ~ L^{minus_one_over_nu:.3f}")
print(f"  -1/ν (fitted) = {minus_one_over_nu:.3f}")
print(f"  -1/ν (3D Ising, ν=0.630) = {-1/0.630:.3f}")
print(f"  ν (from shift) = {nu_from_shift:.3f}")
print(f"  ν (3D Ising) = 0.630")
print(f"  Deviation: {nu_from_shift - 0.630:+.3f}")

# --- Plot: Scaling fits ---
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# χ_max vs L
ax = axes[0]
L_fit = np.linspace(3, 20, 100)
ax.plot(L_vals, chi_max_vals, 'ko', markersize=10, label='Data')
ax.plot(L_fit, chi_prefactor * L_fit**gamma_over_nu, 'r--', linewidth=1.5, alpha=0.7,
        label=f'Fit: χ ~ L^{gamma_over_nu:.2f}')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$\chi_{\max}(L)$', fontsize=12)
ax.set_title(r'Susceptibility peak scaling', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)

# C_max vs L
ax = axes[1]
ax.plot(L_vals, c_max_vals, 'ko', markersize=10, label='Data')
ax.plot(L_fit, c_prefactor * L_fit**alpha_over_nu, 'r--', linewidth=1.5, alpha=0.7,
        label=f'Fit: C ~ L^{alpha_over_nu:.2f}')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$C_{V,\max}(L)$', fontsize=12)
ax.set_title(r'Specific heat peak scaling', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)

# β_c(L) vs L
ax = axes[2]
ax.plot(L_vals, beta_c_vals, 'ko', markersize=10, label='β_c from χ_peak')
ax.axhline(beta_c_inf, color='gray', linestyle=':', linewidth=2, alpha=0.7, label='β_c(∞) = 0.7613')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$\beta_c(L)$', fontsize=12)
ax.set_title(r'Critical coupling shift', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)
ax.set_ylim(0.70, 0.78)

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-critical-exponents.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-critical-exponents.svg', bbox_inches='tight')
plt.close()

print(f"\nFigure saved: t20-critical-exponents.png")

# --- Estimate ν from γ/ν and γ ---
# If we assume γ = 1.237 (3D Ising), then ν = γ / (γ/ν)
nu_from_chi = 1.237 / gamma_over_nu
print(f"\n{'='*60}")
print("CONSISTENCY CHECK")
print(f"{'='*60}")
print(f"\nAssuming γ = 1.237 (3D Ising):")
print(f"  ν from χ scaling = γ / (γ/ν) = {nu_from_chi:.3f}")
print(f"  ν from β_c shift = {nu_from_shift:.3f}")
print(f"  ν (3D Ising) = 0.630")
print(f"  Consistency: |Δν| = {abs(nu_from_chi - nu_from_shift):.3f}")

if abs(nu_from_chi - nu_from_shift) < 0.1:
    print(f"  ✓ Exponents are consistent (|Δν| < 0.1)")
else:
    print(f"  ⚠ Exponents differ significantly — need larger L")
