#!/usr/bin/env python3
"""
Finite-size scaling collapse test for 3D Z2 LGT.

Uses literature 3D Ising exponents to test universality:
- ν = 0.630, γ = 1.237, β_c = 0.7613

If 3D Z2 LGT is in the 3D Ising universality class, then plotting:
  L^(-γ/ν) χ  vs  L^(1/ν)(β - β_c)
should collapse all curves onto a single universal function.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.plotting import (
    load_run,
    extract_observables,
    save_publication,
    setup_grid,
    lattice_plot_kwargs,
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

# Literature values
NU = 0.630
GAMMA = 1.237
BETA_C = 0.7613
BETA_EXP = 0.327  # order parameter exponent

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
# Scaling collapse plots
# ─────────────────────────────────────────────────────────────

x_label = r'$L^{1/\nu}(\beta - \beta_c)$'
y_label_chi = r'$L^{-\gamma/\nu} \chi$'
y_label_p = r'$L^{\beta/\nu} \langle P \rangle$'

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['wide'])

# --- Susceptibility collapse ---
ax = axes[0]
for L in sorted(data):
    obs = data[L]
    x = L**(1/NU) * (obs['betas'] - BETA_C)
    y = L**(-GAMMA/NU) * obs['susceptibilities']
    ax.plot(x, y, **lattice_plot_kwargs(L, markersize=5))

ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label_chi, fontsize=12)
ax.set_title(r'Susceptibility scaling collapse', fontsize=13)
ax.set_xlim(-2, 2)
setup_grid(ax)
ax.legend(fontsize=9)

# --- Order parameter collapse ---
ax = axes[1]
for L in sorted(data):
    obs = data[L]
    x = L**(1/NU) * (obs['betas'] - BETA_C)
    y = L**(BETA_EXP/NU) * obs['plaquettes']
    ax.plot(x, y, **lattice_plot_kwargs(L, markersize=5))

ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label_p, fontsize=12)
ax.set_title(r'Order parameter scaling collapse', fontsize=13)
ax.set_xlim(-2, 2)
setup_grid(ax)
ax.legend(fontsize=9)

plt.tight_layout()
save_publication(fig, 't20-scaling-collapse', output_dir=OUTPUT_DIR)
plt.close()

# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────

print("=" * 60)
print("SCALING COLLAPSE TEST")
print("3D Z2 LGT — 3D Ising universality class")
print("=" * 60)
print(f"\nUsing literature exponents:")
print(f"  β_c = {BETA_C}")
print(f"  ν = {NU}")
print(f"  γ = {GAMMA}")
print(f"  β (order parameter) = {BETA_EXP}")
print(f"\nIf curves collapse → confirmed 3D Ising universality")
print(f"If curves separate → different universality class or need larger L")
print(f"\nFigure saved: t20-scaling-collapse.png")
