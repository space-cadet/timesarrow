#!/usr/bin/env python3
"""
Generate Wilson loop plots with fine-grained beta data
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Load analysis data
with open('/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L8-3D-wilson-analysis.json') as f:
    data = json.load(f)

results = data['results']

# Extract string tension data
betas = [r['beta'] for r in results if r['tension']['sigma'] is not None]
sigmas = [r['tension']['sigma'] for r in results if r['tension']['sigma'] is not None]
sigma_errors = [r['tension']['sigmaError'] for r in results if r['tension']['sigma'] is not None]

# Create output directory
out_dir = '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets'
os.makedirs(out_dir, exist_ok=True)

# Plot 1: String tension vs beta
fig, ax = plt.subplots(figsize=(10, 6))

# Plot with error bars
ax.errorbar(betas, sigmas, yerr=sigma_errors, fmt='o-', color='#2E86AB', 
            ecolor='#A23B72', capsize=4, capthick=1.5, linewidth=2, markersize=6)

# Shade critical region
ax.axvspan(0.70, 0.80, alpha=0.15, color='red', label='Critical region')

# Labels and formatting
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'String tension $\sigma(\beta)$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Confinement-deconfinement transition (L=8)', fontsize=14)
ax.set_yscale('log')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

# Add text annotations
ax.text(0.45, 0.4, 'Confined\n(Area law)', fontsize=10, ha='center', 
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax.text(1.05, 0.001, 'Deconfined\n(Perimeter law)', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-string-tension.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-string-tension.svg', bbox_inches='tight')
plt.close()

# Plot 2: Wilson loops vs Area for selected betas
fig, ax = plt.subplots(figsize=(10, 6))

colors = ['#E94F37', '#F6AE2D', '#3B1F2B']
betas_to_plot = [0.50, 0.70, 0.90]

for i, beta_target in enumerate(betas_to_plot):
    result = next(r for r in results if abs(r['beta'] - beta_target) < 0.01)
    areas = [w['area'] for w in result['wilsonLoops']]
    absWs = [w['absW'] for w in result['wilsonLoops']]
    
    ax.plot(areas, absWs, 'o-', color=colors[i], linewidth=2, markersize=8,
            label=f'$\\beta = {beta_target:.2f}$')

ax.set_xlabel('Loop area $A = r \\times c$ [lattice units]', fontsize=13)
ax.set_ylabel(r'$|W(\gamma)|$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Wilson loop vs area', fontsize=14)
ax.set_yscale('log')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

# Add annotations
ax.text(12, 0.3, 'Area law: |W| ~ exp(-σA)', fontsize=11, 
        color=colors[0], fontweight='bold')
ax.text(12, 0.85, 'Perimeter law: |W| ~ exp(-τP)', fontsize=11,
        color=colors[2], fontweight='bold')

plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-wilson-loops.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-wilson-loops.svg', bbox_inches='tight')
plt.close()

print("Plots saved successfully!")
print(f"  - {out_dir}/t20-p3-string-tension.png")
print(f"  - {out_dir}/t20-p3-wilson-loops.png")
