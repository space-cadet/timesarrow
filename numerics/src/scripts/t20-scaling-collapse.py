#!/usr/bin/env python3
"""
Finite-size scaling collapse test for 3D Z2 LGT.

Uses literature 3D Ising exponents to test universality:
- ν = 0.630, γ = 1.237, β_c = 0.7613

If 3D Z2 LGT is in the 3D Ising universality class, then plotting:
  L^(-γ/ν) χ  vs  L^(1/ν)(β - β_c)
should collapse all curves onto a single universal function.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import os

out_dir = '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets'
os.makedirs(out_dir, exist_ok=True)

# Literature values
nu = 0.630
gamma = 1.237
beta_c = 0.7613

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
        'suscepts': np.array([r['susceptibility'] for r in results]),
        'plaquettes': np.array([r['meanPlaquette'] for r in results]),
    }

# Scaling variables
x_label = r'$L^{1/\nu}(\beta - \beta_c)$'
y_label_chi = r'$L^{-\gamma/\nu} \chi$'
y_label_p = r'$L^{\beta/\nu} \langle P \rangle$'

beta_exp = 0.327  # order parameter exponent (3D Ising)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# --- Susceptibility collapse ---
ax = axes[0]
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    L = int(label.split('=')[1])
    
    x = L**(1/nu) * (d['betas'] - beta_c)
    y = L**(-gamma/nu) * d['suscepts']
    
    ax.plot(x, y, markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=5, label=label, alpha=0.8)

ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label_chi, fontsize=12)
ax.set_title(r'Susceptibility scaling collapse', fontsize=13)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_xlim(-2, 2)

# --- Order parameter collapse ---
ax = axes[1]
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    L = int(label.split('=')[1])
    
    x = L**(1/nu) * (d['betas'] - beta_c)
    # For β > β_c: P ~ |β - β_c|^β, so L^(β/ν) P ~ f(x)
    y = L**(beta_exp/nu) * d['plaquettes']
    
    ax.plot(x, y, markers[label]+'-', color=colors[label], 
            linewidth=1.5, markersize=5, label=label, alpha=0.8)

ax.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label_p, fontsize=12)
ax.set_title(r'Order parameter scaling collapse', fontsize=13)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_xlim(-2, 2)

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-scaling-collapse.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-scaling-collapse.svg', bbox_inches='tight')
plt.close()

print("=" * 60)
print("SCALING COLLAPSE TEST")
print("3D Z2 LGT — 3D Ising universality class")
print("=" * 60)
print(f"\nUsing literature exponents:")
print(f"  β_c = {beta_c}")
print(f"  ν = {nu}")
print(f"  γ = {gamma}")
print(f"  β (order parameter) = {beta_exp}")
print(f"\nIf curves collapse → confirmed 3D Ising universality")
print(f"If curves separate → different universality class or need larger L")
print(f"\nFigure saved: t20-scaling-collapse.png")
