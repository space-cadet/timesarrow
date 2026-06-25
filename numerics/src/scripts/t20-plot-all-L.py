#!/usr/bin/env python3
"""
Regenerate all Phase 3 plots with ALL lattice sizes: L=4, 6, 8, 16, 24, 32
Fine-grained β grid (21 values), 3D cubic Z2 LGT
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar, brentq
import os

out_dir = '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets'
os.makedirs(out_dir, exist_ok=True)

# Load data for ALL lattice sizes
lattices = {
    'L=4': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L4-3D-wilson-fine-20250626.json',
    'L=6': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L6-3D-wilson-fine-20250626.json',
    'L=8': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L8-3D-wilson-fine-20250626.json',
    'L=16': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L16-3D-wilson-fine-20250626.json',
    'L=24': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L24-3D-wilson-fine-20250626.json',
    'L=32': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L32-3D-wilson-fine-20250626.json',
}

# Colors for each lattice (diverging from red to blue, larger = darker)
colors = {
    'L=4': '#E94F37',   # Red
    'L=6': '#F39C12',   # Orange
    'L=8': '#2ECC40',   # Green
    'L=16': '#1ABC9C',  # Teal
    'L=24': '#3498DB',  # Blue
    'L=32': '#9B59B6',  # Purple
}
markers = {
    'L=4': 'o', 'L=6': 's', 'L=8': '^',
    'L=16': 'v', 'L=24': 'D', 'L=32': '*',
}

# Parse data
data = {}
for label, path in lattices.items():
    with open(path) as f:
        d = json.load(f)
    results = d['results']
    data[label] = {
        'betas': np.array([r['beta'] for r in results]),
        'plaquettes': np.array([r['meanPlaquette'] for r in results]),
        'plaquette_errs': np.array([r['errorPlaquette'] for r in results]),
        'suscepts': np.array([r['susceptibility'] for r in results]),
        'specific_heats': np.array([r['specificHeat'] for r in results]),
        'binders': np.array([r['binderCumulant'] for r in results]),
    }

print("Data loaded for:", list(data.keys()))

# --- Plot 1: Plaquette vs Beta (ALL L) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    ax.errorbar(d['betas'], d['plaquettes'], yerr=d['plaquette_errs'], 
                fmt=markers[label]+'-', color=colors[label], label=label,
                ecolor=colors[label], capsize=2, capthick=1, linewidth=1.5, markersize=4, alpha=0.8)
ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'Lit. $\beta_c = 0.7613$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Average plaquette $\langle P \rangle$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Plaquette vs $\beta$ (all $L$, fine-grained)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='lower right', ncol=2)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-plaquette-vs-beta-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-plaquette-vs-beta-all-L.svg', bbox_inches='tight')
plt.close()

# --- Plot 2: Specific Heat vs Beta (ALL L) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    ax.plot(d['betas'], d['specific_heats'], markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=4, label=label, alpha=0.8)
ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'Lit. $\beta_c = 0.7613$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Specific heat $C_V$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Specific heat vs $\beta$ (all $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='upper right', ncol=2)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-specific-heat-vs-beta-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-specific-heat-vs-beta-all-L.svg', bbox_inches='tight')
plt.close()

# --- Plot 3: Susceptibility vs Beta (ALL L) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    ax.plot(d['betas'], d['suscepts'], markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=4, label=label, alpha=0.8)
ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'Lit. $\beta_c = 0.7613$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Susceptibility $\chi$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Susceptibility vs $\beta$ (all $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='upper right', ncol=2)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-susceptibility-vs-beta-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-susceptibility-vs-beta-all-L.svg', bbox_inches='tight')
plt.close()

# --- Plot 4: Binder Cumulant vs Beta (ALL L) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    ax.plot(d['betas'], d['binders'], markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=4, label=label, alpha=0.8)
ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'Lit. $\beta_c = 0.7613$')
ax.axhline(2/3, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=r'$U = 2/3$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Binder cumulant $U$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Binder cumulant vs $\beta$ (all $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='lower right', ncol=2)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-binder-vs-beta-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-binder-vs-beta-all-L.svg', bbox_inches='tight')
plt.close()

# --- Plot 5: Combined Overview (ALL L) ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    # Plaquette
    axes[0,0].errorbar(d['betas'], d['plaquettes'], yerr=d['plaquette_errs'], 
                       fmt=markers[label]+'-', color=colors[label], capsize=2, linewidth=1, markersize=3, label=label)
    # Specific heat
    axes[0,1].plot(d['betas'], d['specific_heats'], markers[label]+'-', color=colors[label], linewidth=1, markersize=3, label=label)
    # Susceptibility
    axes[1,0].plot(d['betas'], d['suscepts'], markers[label]+'-', color=colors[label], linewidth=1, markersize=3, label=label)
    # Binder cumulant
    axes[1,1].plot(d['betas'], d['binders'], markers[label]+'-', color=colors[label], linewidth=1, markersize=3, label=label)

for ax in axes.flat:
    ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc='best', ncol=2)

axes[0,0].set_ylabel(r'$\langle P \rangle$', fontsize=12)
axes[0,0].set_title('Plaquette', fontsize=12)
axes[0,1].set_ylabel(r'$C_V$', fontsize=12)
axes[0,1].set_title('Specific heat', fontsize=12)
axes[1,0].set_xlabel(r'$\beta$', fontsize=12)
axes[1,0].set_ylabel(r'$\chi$', fontsize=12)
axes[1,0].set_title('Susceptibility', fontsize=12)
axes[1,1].axhline(2/3, color='gray', linestyle=':', linewidth=1, alpha=0.5)
axes[1,1].set_xlabel(r'$\beta$', fontsize=12)
axes[1,1].set_ylabel(r'$U$', fontsize=12)
axes[1,1].set_title('Binder cumulant', fontsize=12)

fig.suptitle(r'3D Z$_2$ LGT: Observables overview (all $L$, 21 $\beta$ values)', fontsize=14)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-combined-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-combined-all-L.svg', bbox_inches='tight')
plt.close()

print("\nAll lattice size plots generated:")
print(f"  - t20-p3-plaquette-vs-beta-all-L.png")
print(f"  - t20-p3-specific-heat-vs-beta-all-L.png")
print(f"  - t20-p3-susceptibility-vs-beta-all-L.png")
print(f"  - t20-p3-binder-vs-beta-all-L.png")
print(f"  - t20-p3-combined-all-L.png")

# --- Critical Exponent Extraction (with larger L) ---
print("\n" + "=" * 60)
print("CRITICAL EXPONENT EXTRACTION (ALL LATTICE SIZES)")
print("=" * 60)

# Extract peak values for each L
results = {}
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
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
    
    # Find minimum of binder cumulant
    f = interp1d(d['betas'], d['binders'], kind='cubic', bounds_error=False, fill_value='extrapolate')
    result = minimize_scalar(lambda b: f(b), bounds=(0.6, 0.9), method='bounded')
    beta_min = result.x
    U_min = result.fun
    
    results[L] = {
        'beta_peak_chi': beta_peak_chi,
        'chi_max': chi_max,
        'beta_peak_c': beta_peak_c,
        'c_max': c_max,
        'beta_min': beta_min,
        'U_min': U_min,
    }

print(f"\n{'L':<6} {'β_c(χ)':<10} {'χ_max':<12} {'β_c(C)':<10} {'C_max':<12} {'β_min(U)':<10} {'U_min':<10}")
print("-" * 80)
for L in [4, 6, 8, 16, 24, 32]:
    r = results[L]
    print(f"{L:<6} {r['beta_peak_chi']:<10.4f} {r['chi_max']:<12.4f} {r['beta_peak_c']:<10.4f} {r['c_max']:<12.4f} {r['beta_min']:<10.4f} {r['U_min']:<10.4f}")

# --- Fit χ_max ~ L^(γ/ν) ---
L_vals = np.array([4, 6, 8, 16, 24, 32], dtype=float)
chi_max_vals = np.array([results[L]['chi_max'] for L in [4, 6, 8, 16, 24, 32]])
c_max_vals = np.array([results[L]['c_max'] for L in [4, 6, 8, 16, 24, 32]])
beta_c_vals = np.array([results[L]['beta_peak_chi'] for L in [4, 6, 8, 16, 24, 32]])
U_min_vals = np.array([results[L]['U_min'] for L in [4, 6, 8, 16, 24, 32]])

log_L = np.log(L_vals)
log_chi = np.log(chi_max_vals)
log_c = np.log(c_max_vals)

# Linear fit: log(χ_max) = a + (γ/ν)*log(L)
coeffs_chi = np.polyfit(log_L, log_chi, 1)
gamma_over_nu = coeffs_chi[0]
chi_prefactor = np.exp(coeffs_chi[1])

# For specific heat: C_max ~ L^(α/ν)
coeffs_c = np.polyfit(log_L, log_c, 1)
alpha_over_nu = coeffs_c[0]
c_prefactor = np.exp(coeffs_c[1])

# β_c shift: β_c(L) - β_c(∞) ~ L^(-1/ν)
beta_c_inf = 0.7613
delta_beta = beta_c_vals - beta_c_inf
# Only fit for L >= 8 (small L have strong corrections)
L_fit = L_vals[L_vals >= 8]
delta_beta_fit = delta_beta[L_vals >= 8]
coeffs_beta = np.polyfit(np.log(L_fit), np.log(np.abs(delta_beta_fit)), 1)
minus_one_over_nu = coeffs_beta[0]
nu_from_shift = -1 / minus_one_over_nu

print(f"\n{'='*60}")
print("FINITE-SIZE SCALING FITS (ALL L)")
print(f"{'='*60}")
print(f"\nχ_max scaling: χ_max = {chi_prefactor:.3f} * L^{gamma_over_nu:.3f}")
print(f"  γ/ν (fitted) = {gamma_over_nu:.3f}")
print(f"  γ/ν (3D Ising) = {1.237/0.630:.3f}")
print(f"  Deviation: {gamma_over_nu - 1.237/0.630:+.3f}")

print(f"\nC_max scaling: C_max = {c_prefactor:.3f} * L^{alpha_over_nu:.3f}")
print(f"  α/ν (fitted) = {alpha_over_nu:.3f}")
print(f"  α/ν (3D Ising, α=2-3ν) = {(2-3*0.630)/0.630:.3f}")
print(f"  Deviation: {alpha_over_nu - (2-3*0.630)/0.630:+.3f}")

print(f"\nβ_c shift (L>=8): β_c(L) - β_c(∞) ~ L^{minus_one_over_nu:.3f}")
print(f"  -1/ν (fitted) = {minus_one_over_nu:.3f}")
print(f"  -1/ν (3D Ising, ν=0.630) = {-1/0.630:.3f}")
print(f"  ν (from shift) = {nu_from_shift:.3f}")
print(f"  ν (3D Ising) = 0.630")
print(f"  Deviation: {nu_from_shift - 0.630:+.3f}")

# --- Estimate ν from γ/ν and γ ---
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

# --- Plot: Scaling fits (ALL L) ---
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# χ_max vs L
ax = axes[0]
L_fit = np.linspace(3, 40, 100)
ax.plot(L_vals, chi_max_vals, 'ko', markersize=10, label='Data')
ax.plot(L_fit, chi_prefactor * L_fit**gamma_over_nu, 'r--', linewidth=1.5, alpha=0.7,
        label=f'Fit: χ ~ L^{gamma_over_nu:.2f}')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$\chi_{\max}(L)$', fontsize=12)
ax.set_title(r'Susceptibility peak scaling', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)
ax.set_xscale('log')
ax.set_yscale('log')

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
ax.set_xscale('log')
ax.set_yscale('log')

# β_c(L) vs L
ax = axes[2]
ax.plot(L_vals, beta_c_vals, 'ko', markersize=10, label='β_c from χ_peak')
ax.axhline(beta_c_inf, color='gray', linestyle=':', linewidth=2, alpha=0.7, label='β_c(∞) = 0.7613')
ax.set_xlabel(r'$L$', fontsize=12)
ax.set_ylabel(r'$\beta_c(L)$', fontsize=12)
ax.set_title(r'Critical coupling shift', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)
ax.set_xlim(0, 40)
ax.set_ylim(0.70, 0.78)

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-critical-exponents-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-critical-exponents-all-L.svg', bbox_inches='tight')
plt.close()

print(f"\nFigure saved: t20-critical-exponents-all-L.png")

# --- Scaling Collapse Test (ALL L) ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

nu = 0.630
gamma = 1.237
beta_c = 0.7613
beta_exp = 0.327

# Susceptibility collapse
ax = axes[0]
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    L = int(label.split('=')[1])
    
    x = L**(1/nu) * (d['betas'] - beta_c)
    y = L**(-gamma/nu) * d['suscepts']
    
    ax.plot(x, y, markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=4, label=label, alpha=0.8)

ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(r'$L^{1/\nu}(\beta - \beta_c)$', fontsize=12)
ax.set_ylabel(r'$L^{-\gamma/\nu} \chi$', fontsize=12)
ax.set_title(r'Susceptibility scaling collapse', fontsize=13)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9, ncol=2)
ax.set_xlim(-3, 3)

# Order parameter collapse
ax = axes[1]
for label in ['L=4', 'L=6', 'L=8', 'L=16', 'L=24', 'L=32']:
    d = data[label]
    L = int(label.split('=')[1])
    
    x = L**(1/nu) * (d['betas'] - beta_c)
    y = L**(beta_exp/nu) * d['plaquettes']
    
    ax.plot(x, y, markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=4, label=label, alpha=0.8)

ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(r'$L^{1/\nu}(\beta - \beta_c)$', fontsize=12)
ax.set_ylabel(r'$L^{\beta/\nu} \langle P \rangle$', fontsize=12)
ax.set_title(r'Order parameter scaling collapse', fontsize=13)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9, ncol=2)
ax.set_xlim(-3, 3)

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-scaling-collapse-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-scaling-collapse-all-L.svg', bbox_inches='tight')
plt.close()

print(f"Figure saved: t20-scaling-collapse-all-L.png")

print(f"\n{'='*60}")
print("BINDER CUMULANT MINIMUM SCALING (ALL L)")
print(f"{'='*60}")
print(f"\n{'L':<6} {'β_min':<10} {'U_min':<12} {'2/3 − U_min':<15}")
print("-" * 50)
for L in [4, 6, 8, 16, 24, 32]:
    r = results[L]
    print(f"{L:<6} {r['beta_min']:<10.4f} {r['U_min']:<12.4f} {2/3 - r['U_min']:<15.4f}")

# Fit U_min = 2/3 - c * L^(-d)
delta_U = 2/3 - U_min_vals
log_L_all = np.log(L_vals)
log_delta_all = np.log(delta_U)

coeffs_U = np.polyfit(log_L_all, log_delta_all, 1)
slope_U = coeffs_U[0]
intercept_U = coeffs_U[1]
c_U = np.exp(intercept_U)

print(f"\nFit: U_min(L) = 2/3 - {c_U:.2e} * L^{slope_U:.3f}")
print(f"  Exponent: {slope_U:.3f} (expected: -3 for d=3 first-order)")
print(f"  Deviation: {slope_U + 3:+.3f}")

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.loglog(L_vals, delta_U, 'ko', markersize=10, label='Data')
L_fit = np.linspace(3, 40, 100)
ax.loglog(L_fit, c_U * L_fit**slope_U, 'r--', linewidth=1.5, alpha=0.7,
          label=f'Fit: slope = {slope_U:.2f}')
ax.set_xlabel(r'$L$', fontsize=13)
ax.set_ylabel(r'$2/3 - U_{\min}(L)$', fontsize=13)
ax.set_title(r'Binder Cumulant Minimum Scaling (first-order, all $L$)', fontsize=14)
ax.grid(True, alpha=0.3, which='both')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-binder-first-order-scaling-all-L.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-binder-first-order-scaling-all-L.svg', bbox_inches='tight')
plt.close()

print(f"Figure saved: t20-binder-first-order-scaling-all-L.png")

print("\nAll plots generated successfully!")
