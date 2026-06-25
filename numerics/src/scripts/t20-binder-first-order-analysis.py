#!/usr/bin/env python3
"""
Binder cumulant analysis for 3D Z2 LGT — FIRST-ORDER transition signature.

For a first-order transition, the Binder cumulant U_L(β) shows:
1. A minimum (dip) at β_c that deepens with increasing L
2. U → 2/3 in the ordered phase (β > β_c) as L → ∞

This is distinct from a second-order transition where curves cross at U*.

3D Z2 LGT has a first-order transition (related to 3D Ising but with different observable mapping).
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
markers = {'L=4': 'o', 'L=6': 's', 'L=8': '^'}

# Parse data
data = {}
for label, path in lattices.items():
    with open(path) as f:
        d = json.load(f)
    results = d['results']
    data[label] = {
        'betas': np.array([r['beta'] for r in results]),
        'binders': np.array([r['binderCumulant'] for r in results]),
    }

# --- Find minimum of U_L(β) for each L ---
print("=" * 60)
print("BINDER CUMULANT MINIMUM ANALYSIS")
print("3D Z2 LGT — First-order transition signature")
print("=" * 60)
print(f"\n{'L':<6} {'β_min':<10} {'U_min':<12} {'U_min - 2/3':<15}")
print("-" * 60)

minima = {}
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    f = interp1d(d['betas'], d['binders'], kind='cubic', bounds_error=False, fill_value='extrapolate')
    
    # Find minimum in [0.6, 0.9]
    result = minimize_scalar(lambda b: f(b), bounds=(0.6, 0.9), method='bounded')
    beta_min = result.x
    U_min = result.fun
    
    L = int(label.split('=')[1])
    minima[L] = (beta_min, U_min)
    print(f"{L:<6} {beta_min:.4f}    {U_min:.4f}      {U_min - 2/3:+.4f}")

# --- Scaling of minimum depth with L ---
L_vals = np.array([4, 6, 8])
U_mins = np.array([minima[L][1] for L in L_vals])

# For first-order: U_min ~ 2/3 - c * L^(-d) where d = dimension = 3
# Or equivalently: (2/3 - U_min) ~ L^(-3)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: U_min vs L
ax = axes[0]
ax.plot(L_vals, U_mins, 'ko-', markersize=10, linewidth=2, label='U_min(L)')
ax.axhline(2/3, color='gray', linestyle=':', linewidth=2, alpha=0.7, label='U = 2/3 (thermodynamic)')

# Fit U_min = 2/3 - c * L^(-3)
# At L → ∞, U_min → 2/3
delta_U = 2/3 - U_mins
log_L = np.log(L_vals)
log_delta = np.log(delta_U)

# Linear fit in log-log: log(delta_U) = log(c) - 3*log(L)
# If slope ≈ -3, confirms first-order scaling
coeffs = np.polyfit(log_L, log_delta, 1)
slope = coeffs[0]
intercept = coeffs[1]
c = np.exp(intercept)

L_fit = np.linspace(3, 20, 100)
U_fit = 2/3 - c * L_fit**(-3)
ax.plot(L_fit, U_fit, 'r--', linewidth=1.5, alpha=0.7, 
        label=f'Fit: U = 2/3 - {c:.2e}·L^{{{slope:.2f}}}')

ax.set_xlabel(r'Lattice size $L$', fontsize=13)
ax.set_ylabel(r'$U_{\min}(L)$', fontsize=13)
ax.set_title(r'Binder Minimum Depth vs $L$ (first-order scaling)', fontsize=13)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_xlim(0, 20)

# Right: log-log plot
ax = axes[1]
ax.loglog(L_vals, delta_U, 'ko', markersize=10, label='Data')
L_fit_log = np.linspace(3, 20, 100)
ax.loglog(L_fit_log, c * L_fit_log**slope, 'r--', linewidth=1.5, alpha=0.7,
          label=f'Fit: slope = {slope:.2f}')
ax.set_xlabel(r'$L$', fontsize=13)
ax.set_ylabel(r'$2/3 - U_{\min}(L)$', fontsize=13)
ax.set_title(r'Log-log: First-order scaling $\sim L^{-d}$', fontsize=13)
ax.grid(True, alpha=0.3, which='both')
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-binder-first-order-scaling.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-binder-first-order-scaling.svg', bbox_inches='tight')
plt.close()

print(f"\n{'='*60}")
print("FIRST-ORDER SCALING ANALYSIS")
print(f"{'='*60}")
print(f"\nFit: U_min(L) = 2/3 - c·L^α")
print(f"  α = {slope:.3f} (expected: -3 for d=3 first-order)")
print(f"  c = {c:.2e}")
print(f"\nAt L = 8: delta_U = {2/3 - U_mins[-1]:.4f}")
print(f"At L = 16 (predicted): delta_U = {c * 16**slope:.4f}")
print(f"At L = 32 (predicted): delta_U = {c * 32**slope:.4f}")

# --- Summary plot: Full Binder with annotations ---
fig, ax = plt.subplots(figsize=(10, 6))

for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    ax.plot(d['betas'], d['binders'], markers[label]+'-', color=colors[label], 
            linewidth=2, markersize=6, label=label, alpha=0.8)

# Mark minima
for label in ['L=4', 'L=6', 'L=8']:
    L = int(label.split('=')[1])
    beta_min, U_min = minima[L]
    ax.plot(beta_min, U_min, 'k*', markersize=15, zorder=5)
    ax.annotate(f'L={L}\nβ={beta_min:.3f}\nU={U_min:.3f}', 
               xy=(beta_min, U_min), 
               xytext=(beta_min-0.05 if L==4 else beta_min+0.03, U_min-0.08),
               fontsize=9, ha='center',
               arrowprops=dict(arrowstyle='->', color='gray', lw=0.5),
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))

ax.axhline(2/3, color='gray', linestyle=':', linewidth=2, alpha=0.7, label=r'$U = 2/3$ (ordered phase)')
ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'Lit. $\beta_c = 0.7613$')

ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Binder cumulant $U_L(\beta)$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Binder Cumulant (First-Order Transition)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='lower right')
ax.set_xlim(0.65, 0.85)
ax.set_ylim(0.35, 0.72)

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-binder-first-order.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-binder-first-order.svg', bbox_inches='tight')
plt.close()

print(f"\nFigures saved:")
print(f"  - t20-binder-first-order.png (annotated)")
print(f"  - t20-binder-first-order-scaling.png (scaling analysis)")
