#!/usr/bin/env python3
"""
Generate plot for SU(2) four-leg group average vs spin j

Reads the multi-spin data file and produces publication-ready figures.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
project_root = Path(__file__).resolve().parent.parent.parent
output_dir = project_root / "output"
data_path = output_dir / "su2-four-leg-group-average-multi-spin-20260708.json"

with open(data_path) as f:
    data = json.load(f)

results = data["results"]
js = [r["j"] for r in results]
Gs_exact = [r["analytic"] for r in results]
Gs_mc = [r["mc_estimate"] for r in results]
errors = [r["mc_error"] for r in results]

# Exact power law: G(j) = 1/(2j+1)^2
js_fit = np.linspace(0.3, 3.5, 200)
Gs_fit = 1.0 / (2*js_fit + 1)**2

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot exact values as points
ax.plot(js, Gs_exact, 'o', color='#E84393', markersize=10, 
        label='Exact: $G(j) = 1/(2j+1)^2$', zorder=3)

# Plot MC validation with error bars
ax.errorbar(js, Gs_mc, yerr=errors, fmt='s', color='#3498DB', 
            markersize=7, capsize=4, capthick=1.5, 
            label='Monte Carlo validation (2M samples)', alpha=0.8)

# Plot exact curve
ax.plot(js_fit, Gs_fit, '-', color='#2C3E50', linewidth=1.5, 
        alpha=0.5, label='_nolegend_')

# Labels and styling
ax.set_xlabel('Spin $j$', fontsize=14)
ax.set_ylabel('$G(j) = (2j+1)^{-3} \\int dh \\,[\\chi^j(h)]^4$', fontsize=13)
ax.set_title('SU(2) Four-Leg Group Average (Normalized)', fontsize=14)
ax.set_yscale('log')
ax.set_xscale('log')
ax.grid(True, alpha=0.3, which='both')
ax.legend(fontsize=12, loc='upper right')

# Add annotation for exact ratio
ratio_exact = Gs_exact[1] / Gs_exact[0]
ax.annotate(f'Exact: $j=1 / j=1/2 = {ratio_exact:.4f} = 4/9$', 
            xy=(1.0, Gs_exact[1]), xytext=(1.6, 0.15),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, color='gray')

plt.tight_layout()

# Save figure
figures_dir = project_root / "figures"
figures_dir.mkdir(exist_ok=True)

fig_path_png = figures_dir / "su2-four-leg-group-average-vs-spin.png"
fig_path_svg = figures_dir / "su2-four-leg-group-average-vs-spin.svg"

plt.savefig(fig_path_png, dpi=150, bbox_inches='tight')
plt.savefig(fig_path_svg, bbox_inches='tight')

print(f"Saved: {fig_path_png}")
print(f"Saved: {fig_path_svg}")

# Also show the plot
plt.show()
