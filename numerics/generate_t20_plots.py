import json
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Load data
with open('output/t20-phase1-fast.json') as f:
    data = json.load(f)

results = data['results']
betas = np.array([r['beta'] for r in results])
plaquettes = np.array([r['meanPlaquette'] for r in results])
errors = np.array([r['errorPlaquette'] for r in results])

# Create output directory
import os
os.makedirs('docs/assets', exist_ok=True)

# Color scheme
confined_color = '#e74c3c'  # red for confined
intermediate_color = '#f39c12'  # orange for near-critical
deconfined_color = '#27ae60'  # green for deconfined

# Plot 1: Plaquette vs β (main order parameter)
fig, ax = plt.subplots(figsize=(10, 6))

# Color points by phase
for i, beta in enumerate(betas):
    if beta < 0.4:
        color = confined_color
    elif beta <= 0.5:
        color = intermediate_color
    else:
        color = deconfined_color
    ax.errorbar(beta, plaquettes[i], yerr=errors[i], fmt='o', color=color, 
                markersize=8, capsize=5, capthick=2, elinewidth=2, zorder=5)

# Add smooth interpolation for the curve
beta_smooth = np.linspace(betas.min(), betas.max(), 200)
# Use cubic interpolation
from scipy.interpolate import make_interp_spline
spline = make_interp_spline(betas, plaquettes, k=3)
plaquette_smooth = spline(beta_smooth)
ax.plot(beta_smooth, plaquette_smooth, 'k--', alpha=0.4, linewidth=1, zorder=1)

# Mark critical point
beta_c = 0.5 * np.log(1 + np.sqrt(2))
ax.axvline(beta_c, color='purple', linestyle='--', linewidth=2, alpha=0.7, label=f'βc = {beta_c:.4f}')

# Add phase labels
ax.axhspan(0, 0.3, alpha=0.05, color=confined_color)
ax.axhspan(0.7, 1.0, alpha=0.05, color=deconfined_color)
ax.text(0.15, 0.15, 'Confined', fontsize=12, color=confined_color, fontweight='bold', alpha=0.7)
ax.text(1.0, 0.85, 'Deconfined', fontsize=12, color=deconfined_color, fontweight='bold', alpha=0.7)

ax.set_xlabel('Coupling β', fontsize=14)
ax.set_ylabel('Plaquette expectation ⟨P⟩', fontsize=14)
ax.set_title('Z₂ LGT on 2D Square Lattice (L=8)\nPhase Transition from Confinement to Deconfinement', fontsize=16)
ax.legend(fontsize=12, loc='lower right')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1.0)

plt.tight_layout()
plt.savefig('docs/assets/t20-plaquette-vs-beta.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: docs/assets/t20-plaquette-vs-beta.png')

# Plot 2: Susceptibility estimate (finite difference)
# χ = d⟨P⟩/dβ ≈ Δ⟨P⟩/Δβ (we can also estimate from fluctuations if we had raw data)
fig, ax = plt.subplots(figsize=(10, 6))

# Compute numerical derivative
# Use centered differences for interior points, forward/backward for endpoints
d_beta = np.diff(betas)
d_plaquette = np.diff(plaquettes)
derivative = d_plaquette / d_beta

# Plot at midpoints
mid_betas = (betas[:-1] + betas[1:]) / 2

# Color by phase
for i, mb in enumerate(mid_betas):
    if mb < 0.4:
        color = confined_color
    elif mb <= 0.5:
        color = intermediate_color
    else:
        color = deconfined_color
    ax.bar(mb, derivative[i], width=0.08, color=color, alpha=0.6, edgecolor='black', linewidth=1.5)

ax.axvline(beta_c, color='purple', linestyle='--', linewidth=2, alpha=0.7, label=f'βc = {beta_c:.4f}')

ax.set_xlabel('Coupling β', fontsize=14)
ax.set_ylabel('d⟨P⟩/dβ (approx)', fontsize=14)
ax.set_title('Z₂ LGT — Response Function (Numerical Derivative)\nPeak indicates critical region', fontsize=16)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/assets/t20-susceptibility.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: docs/assets/t20-susceptibility.png')

# Plot 3: Error bar analysis (shows statistical quality)
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(range(len(betas)), errors, color='steelblue', alpha=0.7, edgecolor='navy', linewidth=1.5)
ax.set_xticks(range(len(betas)))
ax.set_xticklabels([f'{b:.2f}' for b in betas], rotation=45)
ax.set_xlabel('Coupling β', fontsize=14)
ax.set_ylabel('Standard Error', fontsize=14)
ax.set_title('Statistical Error by Coupling\n(Error bars from binning + jackknife analysis)', fontsize=16)
ax.grid(True, alpha=0.3, axis='y')

# Add error threshold line
ax.axhline(0.005, color='red', linestyle='--', alpha=0.5, label='5×10⁻³ threshold')
ax.legend(fontsize=12)

plt.tight_layout()
plt.savefig('docs/assets/t20-error-bars.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: docs/assets/t20-error-bars.png')

print('All plots generated successfully!')
