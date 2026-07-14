#!/usr/bin/env python3
"""
⚠️  SUPERCEDED — This script generates plots from the old t22a-fk-vertex data.
The calculation was mislabeled as an FK/EPRL vertex amplitude.

See: numerics/scripts/su2-four-leg-group-average-plot.py
     for the corrected plot generation.

Original description (retained for provenance):
T22a: Generate plot for FK vertex amplitude vs spin j
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
data_path = output_dir / "t22a-fk-vertex-multi-spin-20260628.json"

with open(data_path) as f:
    data = json.load(f)

results = data["results"]
js = [r["j"] for r in results]
amps = [r["amplitude_sq"] for r in results]
errors = [r["error"] for r in results]

# Get power law fit
alpha = data["analysis"]["power_law_fit"]["exponent_alpha"]
c = np.exp(data["analysis"]["power_law_fit"]["prefactor_log_c"])

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data points
ax.errorbar(js, amps, yerr=errors, fmt='o', color='#E84393', 
            markersize=8, capsize=5, capthick=2, label='Monte Carlo (2M samples)')

# Plot power law fit
js_fit = np.linspace(0.5, 3.5, 100)
amps_fit = c * js_fit**(-alpha)
ax.plot(js_fit, amps_fit, '--', color='#3498DB', linewidth=2, 
        label=f'Power law fit: $\\propto j^{{-{alpha:.2f}}}$')

# Labels and styling
ax.set_xlabel('Spin $j$', fontsize=14)
ax.set_ylabel('$|A_v(j)|^2$', fontsize=14)
ax.set_title('FK Vertex Amplitude vs Spin (4-valent, simple intertwiner)', fontsize=14)
ax.set_yscale('log')
ax.set_xscale('log')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=12)

# Add annotation for j=1/2 vs j=1
ratio_1 = amps[1] / amps[0]
ax.annotate(f'j=1 / j=½ = {ratio_1:.3f}', 
            xy=(1.0, amps[1]), xytext=(1.5, 0.05),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, color='gray')

plt.tight_layout()

# Save figure
figures_dir = project_root / "figures"
figures_dir.mkdir(exist_ok=True)

fig_path_png = figures_dir / "t22a-fk-vertex-vs-spin.png"
fig_path_svg = figures_dir / "t22a-fk-vertex-vs-spin.svg"

plt.savefig(fig_path_png, dpi=150, bbox_inches='tight')
plt.savefig(fig_path_svg, bbox_inches='tight')

print(f"Saved: {fig_path_png}")
print(f"Saved: {fig_path_svg}")

# Also show the plot
plt.show()
