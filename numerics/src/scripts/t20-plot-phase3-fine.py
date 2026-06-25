#!/usr/bin/env python3
"""
Regenerate all Phase 3 plots with fine-grained beta data (21 values)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import os

# Load fine-grained data
with open('/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L8-3D-wilson-fine-20250626.json') as f:
    data = json.load(f)

results = data['results']

betas = [r['beta'] for r in results]
plaquettes = [r['meanPlaquette'] for r in results]
plaquette_errs = [r['errorPlaquette'] for r in results]
suscepts = [r['susceptibility'] for r in results]
specific_heats = [r['specificHeat'] for r in results]
binders = [r['binderCumulant'] for r in results]

out_dir = '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets'
os.makedirs(out_dir, exist_ok=True)

# Color scheme
color_main = '#2E86AB'
color_err = '#A23B72'
color_crit = '#E94F37'

# --- Plot 1: Plaquette vs Beta ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.errorbar(betas, plaquettes, yerr=plaquette_errs, fmt='o-', color=color_main,
            ecolor=color_err, capsize=3, capthick=1.5, linewidth=2, markersize=5)
ax.axvspan(0.70, 0.80, alpha=0.12, color='red', label='Critical region')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Average plaquette $\langle P \rangle$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Plaquette vs $\beta$ (L=8, fine-grained)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-plaquette-vs-beta.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-plaquette-vs-beta.svg', bbox_inches='tight')
plt.close()

# --- Plot 2: Specific Heat vs Beta ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(betas, specific_heats, 'o-', color=color_main, linewidth=2, markersize=5)
ax.axvspan(0.70, 0.80, alpha=0.12, color='red', label='Critical region')
# Mark peak
peak_idx = np.argmax(specific_heats)
ax.plot(betas[peak_idx], specific_heats[peak_idx], '*', color=color_crit, markersize=15,
        label=f'Peak: β={betas[peak_idx]:.2f}, C$_V$={specific_heats[peak_idx]:.2f}')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Specific heat $C_V$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Specific heat vs $\beta$ (L=8, fine-grained)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-specific-heat-vs-beta.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-specific-heat-vs-beta.svg', bbox_inches='tight')
plt.close()

# --- Plot 3: Susceptibility vs Beta ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(betas, suscepts, 'o-', color=color_main, linewidth=2, markersize=5)
ax.axvspan(0.70, 0.80, alpha=0.12, color='red', label='Critical region')
peak_idx = np.argmax(suscepts)
ax.plot(betas[peak_idx], suscepts[peak_idx], '*', color=color_crit, markersize=15,
        label=f'Peak: β={betas[peak_idx]:.2f}, χ={suscepts[peak_idx]:.1f}')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Susceptibility $\chi$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Susceptibility vs $\beta$ (L=8, fine-grained)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-susceptibility-vs-beta.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-susceptibility-vs-beta.svg', bbox_inches='tight')
plt.close()

# --- Plot 4: Binder Cumulant vs Beta ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(betas, binders, 'o-', color=color_main, linewidth=2, markersize=5)
ax.axvspan(0.70, 0.80, alpha=0.12, color='red', label='Critical region')
ax.axhline(2/3, color='gray', linestyle='--', linewidth=1.5, label=r'Ising $U^* = 2/3$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Binder cumulant $U$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Binder cumulant vs $\beta$ (L=8, fine-grained)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-binder-vs-beta.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-binder-vs-beta.svg', bbox_inches='tight')
plt.close()

# --- Plot 5: Combined Overview ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plaquette
axes[0,0].errorbar(betas, plaquettes, yerr=plaquette_errs, fmt='o-', color=color_main,
                   ecolor=color_err, capsize=2, linewidth=1.5, markersize=4)
axes[0,0].axvspan(0.70, 0.80, alpha=0.12, color='red')
axes[0,0].set_ylabel(r'$\langle P \rangle$', fontsize=12)
axes[0,0].set_title('Plaquette', fontsize=12)
axes[0,0].grid(True, alpha=0.3)

# Specific heat
axes[0,1].plot(betas, specific_heats, 'o-', color=color_main, linewidth=1.5, markersize=4)
axes[0,1].axvspan(0.70, 0.80, alpha=0.12, color='red')
axes[0,1].set_ylabel(r'$C_V$', fontsize=12)
axes[0,1].set_title('Specific heat', fontsize=12)
axes[0,1].grid(True, alpha=0.3)

# Susceptibility
axes[1,0].plot(betas, suscepts, 'o-', color=color_main, linewidth=1.5, markersize=4)
axes[1,0].axvspan(0.70, 0.80, alpha=0.12, color='red')
axes[1,0].set_xlabel(r'$\beta$', fontsize=12)
axes[1,0].set_ylabel(r'$\chi$', fontsize=12)
axes[1,0].set_title('Susceptibility', fontsize=12)
axes[1,0].grid(True, alpha=0.3)

# Binder cumulant
axes[1,1].plot(betas, binders, 'o-', color=color_main, linewidth=1.5, markersize=4)
axes[1,1].axvspan(0.70, 0.80, alpha=0.12, color='red')
axes[1,1].axhline(2/3, color='gray', linestyle='--', linewidth=1)
axes[1,1].set_xlabel(r'$\beta$', fontsize=12)
axes[1,1].set_ylabel(r'$U$', fontsize=12)
axes[1,1].set_title('Binder cumulant', fontsize=12)
axes[1,1].grid(True, alpha=0.3)

fig.suptitle(r'3D Z$_2$ LGT: Observables overview (L=8, fine-grained, 21 $\beta$ values)', fontsize=14)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-combined.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-combined.svg', bbox_inches='tight')
plt.close()

print("All Phase 3 plots regenerated with fine-grained data!")
print(f"  - t20-p3-plaquette-vs-beta.png")
print(f"  - t20-p3-specific-heat-vs-beta.png")
print(f"  - t20-p3-susceptibility-vs-beta.png")
print(f"  - t20-p3-binder-vs-beta.png")
print(f"  - t20-p3-combined.png")
print(f"\nPeak specific heat: β={betas[peak_idx]:.2f}, C_V={specific_heats[peak_idx]:.4f}")
print(f"Peak susceptibility: β={betas[np.argmax(suscepts)]:.2f}, χ={suscepts[np.argmax(suscepts)]:.2f}")
