#!/usr/bin/env python3
"""
Binder cumulant crossing analysis for 3D Z2 LGT finite-size scaling.

The Binder cumulant U_L(β) = 1 - <P^4>/(3<P^2>^2) should cross at a 
universal value U* for different L at the critical point β_c.
For 3D Ising universality: U* ≈ 0.623 (periodic b.c.) or 0.465 (fixed b.c.)
We use periodic b.c. → U* ≈ 0.623.

This script:
1. Loads L=4,6,8,16,24,32 data from fine-grained β runs
2. Finds where U_L curves for different L pairs cross
3. Estimates β_c and U* from crossings
4. Checks convergence with L
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.plotting import (
    load_run,
    extract_observables,
    save_publication,
    setup_grid,
    annotate_beta_c,
    lattice_plot_kwargs,
    FIG_SIZES,
    PATHS,
)

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import brentq

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

U_ISING = 0.623       # 3D Ising periodic b.c.
BETA_C_LIT = 0.7613   # Creutz et al. 1979

# ─────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────

data = {}
for L, run_id in RUNS.items():
    d = load_run(run_id)
    obs = extract_observables(d['results'])
    data[L] = {
        'betas': obs['betas'],
        'binders': obs['binder_cumulants'],
    }
    print(f"  Loaded L={L}: {len(obs['betas'])} β values")

# ─────────────────────────────────────────────────────────────
# Find crossing points between pairs
# ─────────────────────────────────────────────────────────────

def find_crossing(betas1, u1, betas2, u2, beta_min=0.65, beta_max=0.85):
    """Find β where U_L1(β) = U_L2(β) using interpolation."""
    f1 = interp1d(betas1, u1, kind='cubic', bounds_error=False, fill_value='extrapolate')
    f2 = interp1d(betas2, u2, kind='cubic', bounds_error=False, fill_value='extrapolate')
    
    def diff(beta):
        return f1(beta) - f2(beta)
    
    try:
        d_min = diff(beta_min)
        d_max = diff(beta_max)
        if d_min * d_max < 0:
            beta_cross = brentq(diff, beta_min, beta_max)
            u_cross = f1(beta_cross)
            return beta_cross, u_cross
    except ValueError:
        pass
    return None, None

pairs = [(8, 16), (16, 24), (24, 32), (8, 32)]
crossings = {}

for l1, l2 in pairs:
    d1 = data[l1]
    d2 = data[l2]
    beta_c, u_star = find_crossing(d1['betas'], d1['binders'], d2['betas'], d2['binders'])
    crossings[(l1, l2)] = (beta_c, u_star)

# ─────────────────────────────────────────────────────────────
# Print results
# ─────────────────────────────────────────────────────────────

print("=" * 60)
print("BINDER CUMULANT CROSSING ANALYSIS")
print("3D Z2 LGT — Fine-grained β grid")
print("=" * 60)
print(f"\n{'Pair':<12} {'β_c (crossing)':<18} {'U* (crossing)':<18} {'U* - U_Ising':<15}")
print("-" * 60)

valid_crossings = []
for (l1, l2), (beta_c, u_star) in crossings.items():
    if beta_c is not None:
        diff = u_star - U_ISING if u_star else None
        print(f"L{l1}×L{l2:<6} {beta_c:.4f}            {u_star:.4f}            {diff:+.4f}")
        valid_crossings.append((beta_c, u_star))
    else:
        print(f"L{l1}×L{l2:<6} No crossing found")

if valid_crossings:
    avg_beta_c = np.mean([bc for bc, _ in valid_crossings])
    avg_u_star = np.mean([us for _, us in valid_crossings])
    print(f"\n{'Average':<12} {avg_beta_c:.4f}            {avg_u_star:.4f}")
    print(f"\nLiterature β_c (Creutz et al. 1979): {BETA_C_LIT}")
    print(f"Deviation: {avg_beta_c - BETA_C_LIT:+.4f}")

# ─────────────────────────────────────────────────────────────
# Plot 1: Binder cumulant vs β with crossings
# ─────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])

for L, d in sorted(data.items()):
    kwargs = lattice_plot_kwargs(L)
    ax.plot(d['betas'], d['binders'], **kwargs)

# Mark crossings
for (l1, l2), (beta_c, u_star) in crossings.items():
    if beta_c is not None:
        ax.plot(beta_c, u_star, 'k*', markersize=15, zorder=5)
        ax.annotate(f'L{l1}×L{l2}\nβ_c={beta_c:.3f}',
                   xy=(beta_c, u_star), xytext=(beta_c+0.02, u_star+0.05),
                   fontsize=8, ha='left',
                   arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

ax.axhline(U_ISING, color='gray', linestyle=':', linewidth=1.5, alpha=0.7,
           label=f'Ising U* = {U_ISING}')
annotate_beta_c(ax, beta_c=BETA_C_LIT)

ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Binder cumulant $U_L(\beta)$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Binder Cumulant Crossing (finite-size scaling)', fontsize=14)
ax.set_xlim(0.65, 0.85)
ax.set_ylim(0.3, 0.75)
setup_grid(ax)
ax.legend(fontsize=9, loc='lower right')

plt.tight_layout()
save_publication(fig, 't20-binder-crossing', output_dir=OUTPUT_DIR)
plt.close()

print(f"\nFigure saved: t20-binder-crossing.png")

# ─────────────────────────────────────────────────────────────
# Plot 2: U_L(β_c) vs 1/L extrapolation
# ─────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=FIG_SIZES['compact'])

L_values = sorted(data)
inv_L = [1/L for L in L_values]

# Interpolate U at β_c ≈ 0.7613 for each L
U_at_bc = []
for L in L_values:
    d = data[L]
    f = interp1d(d['betas'], d['binders'], kind='cubic', bounds_error=False, fill_value='extrapolate')
    U_at_bc.append(f(BETA_C_LIT))

ax.plot(inv_L, U_at_bc, 'ko-', markersize=8, linewidth=2, label=f'$U_L(\\beta_c={BETA_C_LIT})$')

# Linear fit to extrapolate to L → ∞
coeffs = np.polyfit(inv_L, U_at_bc, 1)
U_inf = coeffs[1]
ax.plot([0, max(inv_L)], [U_inf, coeffs[0]*max(inv_L) + U_inf],
        'r--', linewidth=1.5, alpha=0.7, label=f'Linear fit: $U_\\infty$ = {U_inf:.4f}')

ax.axhline(U_ISING, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=f'Ising U* = {U_ISING}')
ax.set_xlabel(r'$1/L$', fontsize=13)
ax.set_ylabel(r'$U_L(\beta_c)$', fontsize=13)
ax.set_title(r'Binder Cumulant Extrapolation to $L \to \infty$', fontsize=14)
setup_grid(ax)
ax.legend(fontsize=10)

plt.tight_layout()
save_publication(fig, 't20-binder-extrapolation', output_dir=OUTPUT_DIR)
plt.close()

print(f"Figure saved: t20-binder-extrapolation.png")
print(f"\nU_∞ (extrapolated) = {U_inf:.4f}")
print(f"U_Ising (literature) = {U_ISING:.4f}")
print(f"Difference: {U_inf - U_ISING:+.4f}")
