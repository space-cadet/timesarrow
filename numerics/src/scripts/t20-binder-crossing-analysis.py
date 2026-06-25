#!/usr/bin/env python3
"""
Binder cumulant crossing analysis for 3D Z2 LGT finite-size scaling.

The Binder cumulant U_L(β) = 1 - <P^4>/(3<P^2>^2) should cross at a 
universal value U* for different L at the critical point β_c.
For 3D Ising universality: U* ≈ 0.623 (periodic b.c.) or 0.465 (fixed b.c.)
We use periodic b.c. → U* ≈ 0.623.

This script:
1. Loads L=4,6,8 data from fine-grained β runs
2. Finds where U_L curves for different L pairs cross
3. Estimates β_c and U* from crossings
4. Checks convergence with L
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import brentq
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

# --- Find crossing points between pairs ---
def find_crossing(betas1, u1, betas2, u2, beta_min=0.65, beta_max=0.85):
    """Find β where U_L1(β) = U_L2(β) using interpolation."""
    # Create smooth interpolations
    f1 = interp1d(betas1, u1, kind='cubic', bounds_error=False, fill_value='extrapolate')
    f2 = interp1d(betas2, u2, kind='cubic', bounds_error=False, fill_value='extrapolate')
    
    # Difference function
    def diff(beta):
        return f1(beta) - f2(beta)
    
    # Check if there's a sign change in [beta_min, beta_max]
    try:
        d_min = diff(beta_min)
        d_max = diff(beta_max)
        if d_min * d_max < 0:  # Sign change → crossing
            beta_cross = brentq(diff, beta_min, beta_max)
            u_cross = f1(beta_cross)
            return beta_cross, u_cross
    except ValueError:
        pass
    return None, None

pairs = [('L=4', 'L=6'), ('L=6', 'L=8'), ('L=4', 'L=8')]
crossings = {}

for l1, l2 in pairs:
    d1 = data[l1]
    d2 = data[l2]
    beta_c, u_star = find_crossing(d1['betas'], d1['binders'], d2['betas'], d2['binders'])
    crossings[f"{l1} × {l2}"] = (beta_c, u_star)

# --- Print results ---
print("=" * 60)
print("BINDER CUMULANT CROSSING ANALYSIS")
print("3D Z2 LGT — Fine-grained β grid (21 values)")
print("=" * 60)
print(f"\n{'Pair':<12} {'β_c (crossing)':<18} {'U* (crossing)':<18} {'U* - U_Ising':<15}")
print("-" * 60)

U_ising = 0.623  # 3D Ising periodic b.c. from literature
for pair, (beta_c, u_star) in crossings.items():
    if beta_c is not None:
        diff = u_star - U_ising if u_star else None
        print(f"{pair:<12} {beta_c:.4f}            {u_star:.4f}            {diff:+.4f}")
    else:
        print(f"{pair:<12} No crossing found")

# Average crossing
valid = [(bc, us) for bc, us in crossings.values() if bc is not None]
if valid:
    avg_beta_c = np.mean([bc for bc, _ in valid])
    avg_u_star = np.mean([us for _, us in valid])
    print(f"\n{'Average':<12} {avg_beta_c:.4f}            {avg_u_star:.4f}")
    print(f"\nLiterature β_c (Creutz et al. 1979): 0.7613")
    print(f"Deviation: {avg_beta_c - 0.7613:+.4f}")

# --- Plot 1: Binder cumulant vs β with crossings ---
fig, ax = plt.subplots(figsize=(10, 6))

for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    ax.plot(d['betas'], d['binders'], markers[label]+'-', color=colors[label], 
            linewidth=2, markersize=6, label=label, alpha=0.8)

# Mark crossings
for pair, (beta_c, u_star) in crossings.items():
    if beta_c is not None:
        ax.plot(beta_c, u_star, 'k*', markersize=15, zorder=5)
        ax.annotate(f'{pair}\nβ_c={beta_c:.3f}', 
                   xy=(beta_c, u_star), xytext=(beta_c+0.02, u_star+0.05),
                   fontsize=9, ha='left',
                   arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

ax.axhline(U_ising, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, 
           label=f'Ising U* = {U_ising}')
ax.axvline(0.7613, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, 
           label=f'Lit. β_c = 0.7613')

ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Binder cumulant $U_L(\beta)$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Binder Cumulant Crossing (finite-size scaling)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='lower right')
ax.set_xlim(0.65, 0.85)
ax.set_ylim(0.3, 0.75)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-binder-crossing.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-binder-crossing.svg', bbox_inches='tight')
plt.close()

print(f"\nFigure saved: t20-binder-crossing.png")

# --- Plot 2: U_L(β_c) vs 1/L to check extrapolation ---
fig, ax = plt.subplots(figsize=(8, 6))

L_values = [4, 6, 8]
inv_L = [1/L for L in L_values]

# Interpolate U at β_c ≈ 0.7613 for each L
U_at_bc = []
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    f = interp1d(d['betas'], d['binders'], kind='cubic', bounds_error=False, fill_value='extrapolate')
    U_at_bc.append(f(0.7613))

ax.plot(inv_L, U_at_bc, 'ko-', markersize=8, linewidth=2, label='U_L(β_c=0.7613)')

# Linear fit to extrapolate to L → ∞
coeffs = np.polyfit(inv_L, U_at_bc, 1)
U_inf = coeffs[1]  # intercept at 1/L = 0
ax.plot([0, max(inv_L)], [U_inf, coeffs[0]*max(inv_L) + U_inf], 
        'r--', linewidth=1.5, alpha=0.7, label=f'Linear fit: U_∞ = {U_inf:.4f}')

ax.axhline(U_ising, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=f'Ising U* = {U_ising}')
ax.set_xlabel(r'$1/L$', fontsize=13)
ax.set_ylabel(r'$U_L(\beta_c)$', fontsize=13)
ax.set_title(r'Binder Cumulant Extrapolation to $L \to \infty$', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-binder-extrapolation.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-binder-extrapolation.svg', bbox_inches='tight')
plt.close()

print(f"Figure saved: t20-binder-extrapolation.png")
print(f"\nU_∞ (extrapolated) = {U_inf:.4f}")
print(f"U_Ising (literature) = {U_ising:.4f}")
print(f"Difference: {U_inf - U_ising:+.4f}")
