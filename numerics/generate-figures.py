#!/usr/bin/env python3
"""Generate figures for T20 Z2 LGT results."""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load L=16 production data
with open('output/t20-phase1-square-lattice.json') as f:
    data16 = json.load(f)

# Load L=8 fast data
with open('output/t20-phase1-fast.json') as f:
    data8 = json.load(f)

results16 = data16['results']
results8 = data8['results']

beta16 = [r['beta'] for r in results16]
p16 = [r['meanPlaquette'] for r in results16]
err16 = [r['errorPlaquette'] for r in results16]

beta8 = [r['beta'] for r in results8]
p8 = [r['meanPlaquette'] for r in results8]
err8 = [r['errorPlaquette'] for r in results8]

# Critical coupling
beta_c = 0.5 * np.log(1 + np.sqrt(2))

# Colors by phase
def color_by_beta(b):
    if b < 0.42:
        return '#e74c3c'  # Red: confined
    elif b < 0.48:
        return '#f39c12'  # Orange: near-critical
    else:
        return '#27ae60'  # Green: deconfined

colors16 = [color_by_beta(b) for b in beta16]

# Create assets dir
assets_dir = Path('docs/assets')
assets_dir.mkdir(exist_ok=True)

# Figure 1: Plaquette vs beta (L=16 with L=8 comparison)
fig, ax = plt.subplots(figsize=(10, 6))

# L=16 data
ax.errorbar(beta16, p16, yerr=err16, fmt='o', markersize=6, capsize=3,
            color='#2980b9', ecolor='#95a5a6', linewidth=1.5,
            label=f'L=16 (N=100k, err~{np.mean(err16)*1000:.1f}×10⁻³)')

# L=8 data
ax.errorbar(beta8, p8, yerr=err8, fmt='s', markersize=5, capsize=3,
            color='#e74c3c', ecolor='#bdc3c7', linewidth=1,
            alpha=0.6, label=f'L=8 (N=5k, err~{np.mean(err8)*1000:.1f}×10⁻³)')

# Critical point
ax.axvline(x=beta_c, color='#8e44ad', linestyle='--', linewidth=2,
           label=f'βc = {beta_c:.4f}')

ax.set_xlabel('Coupling β', fontsize=13)
ax.set_ylabel('⟨P⟩ — Average Plaquette', fontsize=13)
ax.set_title('Z₂ LGT: Plaquette Expectation vs Coupling', fontsize=14, fontweight='bold')
ax.legend(loc='lower right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 2.1)
ax.set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig(assets_dir / 't20-plaquette-vs-beta-L16.png', dpi=150, bbox_inches='tight')
plt.close()

print("Generated: t20-plaquette-vs-beta-L16.png")

# Figure 2: Error comparison (L=16 vs L=8)
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(beta16))
width = 0.35

# Match L=8 errors to L=16 beta values
err8_matched = []
for b in beta16:
    idx = beta8.index(b) if b in beta8 else None
    err8_matched.append(err8[idx] if idx is not None else 0)

bars1 = ax.bar(x - width/2, [e*1000 for e in err16], width,
               label='L=16', color='#2980b9', alpha=0.8)
bars2 = ax.bar(x + width/2, [e*1000 for e in err8_matched], width,
               label='L=8', color='#e74c3c', alpha=0.6)

ax.set_xlabel('β', fontsize=13)
ax.set_ylabel('Error × 10⁻³', fontsize=13)
ax.set_title('Statistical Error: L=16 vs L=8', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f'{b:.2f}' for b in beta16], rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add improvement ratio text
avg_ratio = np.mean([e8/e16 for e8, e16 in zip(err8_matched, err16) if e16 > 0])
ax.text(0.98, 0.95, f'Mean improvement:\nL=16 errors are\n{avg_ratio:.1f}× smaller',
        transform=ax.transAxes, fontsize=10, verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(assets_dir / 't20-error-comparison-L16.png', dpi=150, bbox_inches='tight')
plt.close()

print("Generated: t20-error-comparison-L16.png")

# Figure 3: Convergence plot (error vs N for L=16)
fig, ax = plt.subplots(figsize=(10, 6))

# Theoretical 1/sqrt(N) scaling
N_vals = np.logspace(3, 5, 100)
scaling = 0.06 / np.sqrt(N_vals / 1000)  # Normalized

ax.loglog(N_vals, scaling, 'k--', linewidth=2, label='1/√N scaling')

# Actual errors at beta=0.44 (critical point - hardest to converge)
# We don't have intermediate N data, so annotate the points
ax.scatter([5000], [err8[beta8.index(0.44)]], s=100, color='#e74c3c',
           marker='s', label='L=8, N=5k', zorder=5)
ax.scatter([100000], [err16[beta16.index(0.44)]], s=100, color='#2980b9',
           marker='o', label='L=16, N=100k', zorder=5)

ax.set_xlabel('Number of Measurements', fontsize=13)
ax.set_ylabel('Statistical Error', fontsize=13)
ax.set_title('Monte Carlo Convergence at β=0.44 (Critical Point)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(assets_dir / 't20-convergence-L16.png', dpi=150, bbox_inches='tight')
plt.close()

print("Generated: t20-convergence-L16.png")

print("\nAll figures generated successfully!")
