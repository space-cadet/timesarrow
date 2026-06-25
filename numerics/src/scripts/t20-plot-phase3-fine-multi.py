#!/usr/bin/env python3
"""
Regenerate all Phase 3 plots with fine-grained beta data — ALL lattice sizes overlaid
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import os

out_dir = '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets'
os.makedirs(out_dir, exist_ok=True)

# Load fine-grained data for all lattice sizes
lattices = {
    'L=4': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L4-3D-wilson-fine-20250626.json',
    'L=6': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L6-3D-wilson-fine-20250626.json',
    'L=8': '/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output/t20-p3-L8-3D-wilson-fine-20250626.json',
}

# Colors and styles for each lattice
colors = {
    'L=4': '#E94F37',  # Red
    'L=6': '#2E86AB',  # Blue
    'L=8': '#2ECC40',  # Green
}
markers = {
    'L=4': 'o',
    'L=6': 's',
    'L=8': '^',
}

# Parse data
data = {}
for label, path in lattices.items():
    with open(path) as f:
        d = json.load(f)
    results = d['results']
    data[label] = {
        'betas': [r['beta'] for r in results],
        'plaquettes': [r['meanPlaquette'] for r in results],
        'plaquette_errs': [r['errorPlaquette'] for r in results],
        'suscepts': [r['susceptibility'] for r in results],
        'specific_heats': [r['specificHeat'] for r in results],
        'binders': [r['binderCumulant'] for r in results],
    }

# --- Plot 1: Plaquette vs Beta (Multi-Lattice) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    ax.errorbar(d['betas'], d['plaquettes'], yerr=d['plaquette_errs'], 
                fmt=markers[label]+'-', color=colors[label], label=label,
                ecolor=colors[label], capsize=3, capthick=1.5, linewidth=2, markersize=5, alpha=0.8)
ax.axvline(0.76, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Average plaquette $\langle P \rangle$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Plaquette vs $\beta$ (fine-grained, multiple $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='lower right')
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-plaquette-vs-beta-multi.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-plaquette-vs-beta-multi.svg', bbox_inches='tight')
plt.close()

# --- Plot 2: Specific Heat vs Beta (Multi-Lattice) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    ax.plot(d['betas'], d['specific_heats'], markers[label]+'-', color=colors[label], 
            linewidth=2, markersize=5, label=label, alpha=0.8)
ax.axvline(0.76, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Specific heat $C_V$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Specific heat vs $\beta$ (fine-grained, multiple $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-specific-heat-vs-beta-multi.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-specific-heat-vs-beta-multi.svg', bbox_inches='tight')
plt.close()

# --- Plot 3: Susceptibility vs Beta (Multi-Lattice) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    ax.plot(d['betas'], d['suscepts'], markers[label]+'-', color=colors[label], 
            linewidth=2, markersize=5, label=label, alpha=0.8)
ax.axvline(0.76, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Susceptibility $\chi$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Susceptibility vs $\beta$ (fine-grained, multiple $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-susceptibility-vs-beta-multi.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-susceptibility-vs-beta-multi.svg', bbox_inches='tight')
plt.close()

# --- Plot 4: Binder Cumulant vs Beta (Multi-Lattice) ---
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    ax.plot(d['betas'], d['binders'], markers[label]+'-', color=colors[label], 
            linewidth=2, markersize=5, label=label, alpha=0.8)
ax.axvline(0.76, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.axhline(2/3, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=r'Ising $U^* = 2/3$')
ax.set_xlabel(r'Inverse coupling $\beta$', fontsize=13)
ax.set_ylabel(r'Binder cumulant $U$', fontsize=13)
ax.set_title(r'3D Z$_2$ LGT: Binder cumulant vs $\beta$ (fine-grained, multiple $L$)', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='lower right')
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-binder-vs-beta-multi.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-binder-vs-beta-multi.svg', bbox_inches='tight')
plt.close()

# --- Plot 5: Combined Overview (Multi-Lattice) ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    # Plaquette
    axes[0,0].errorbar(d['betas'], d['plaquettes'], yerr=d['plaquette_errs'], 
                       fmt=markers[label]+'-', color=colors[label], capsize=2, linewidth=1.5, markersize=4, label=label)
    # Specific heat
    axes[0,1].plot(d['betas'], d['specific_heats'], markers[label]+'-', color=colors[label], linewidth=1.5, markersize=4, label=label)
    # Susceptibility
    axes[1,0].plot(d['betas'], d['suscepts'], markers[label]+'-', color=colors[label], linewidth=1.5, markersize=4, label=label)
    # Binder cumulant
    axes[1,1].plot(d['betas'], d['binders'], markers[label]+'-', color=colors[label], linewidth=1.5, markersize=4, label=label)

axes[0,0].axvline(0.76, color='gray', linestyle='--', linewidth=1, alpha=0.7)
axes[0,0].set_ylabel(r'$\langle P \rangle$', fontsize=12)
axes[0,0].set_title('Plaquette', fontsize=12)
axes[0,0].grid(True, alpha=0.3)
axes[0,0].legend(fontsize=9, loc='lower right')

axes[0,1].axvline(0.76, color='gray', linestyle='--', linewidth=1, alpha=0.7)
axes[0,1].set_ylabel(r'$C_V$', fontsize=12)
axes[0,1].set_title('Specific heat', fontsize=12)
axes[0,1].grid(True, alpha=0.3)
axes[0,1].legend(fontsize=9)

axes[1,0].axvline(0.76, color='gray', linestyle='--', linewidth=1, alpha=0.7)
axes[1,0].set_xlabel(r'$\beta$', fontsize=12)
axes[1,0].set_ylabel(r'$\chi$', fontsize=12)
axes[1,0].set_title('Susceptibility', fontsize=12)
axes[1,0].grid(True, alpha=0.3)
axes[1,0].legend(fontsize=9)

axes[1,1].axvline(0.76, color='gray', linestyle='--', linewidth=1, alpha=0.7)
axes[1,1].axhline(2/3, color='gray', linestyle=':', linewidth=1, alpha=0.7)
axes[1,1].set_xlabel(r'$\beta$', fontsize=12)
axes[1,1].set_ylabel(r'$U$', fontsize=12)
axes[1,1].set_title('Binder cumulant', fontsize=12)
axes[1,1].grid(True, alpha=0.3)
axes[1,1].legend(fontsize=9, loc='lower right')

fig.suptitle(r'3D Z$_2$ LGT: Observables overview (fine-grained, 21 $\beta$ values, multiple $L$)', fontsize=14)
plt.tight_layout()
plt.savefig(f'{out_dir}/t20-p3-combined-multi.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{out_dir}/t20-p3-combined-multi.svg', bbox_inches='tight')
plt.close()

print("All Phase 3 multi-lattice plots regenerated!")
print(f"  - t20-p3-plaquette-vs-beta-multi.png")
print(f"  - t20-p3-specific-heat-vs-beta-multi.png")
print(f"  - t20-p3-susceptibility-vs-beta-multi.png")
print(f"  - t20-p3-binder-vs-beta-multi.png")
print(f"  - t20-p3-combined-multi.png")

# Print peak locations for each lattice
for label in ['L=4', 'L=6', 'L=8']:
    d = data[label]
    peak_c = np.argmax(d['specific_heats'])
    peak_chi = np.argmax(d['suscepts'])
    print(f"\n{label}:")
    print(f"  Peak C_V: β={d['betas'][peak_c]:.2f}, C_V={d['specific_heats'][peak_c]:.4f}")
    print(f"  Peak χ: β={d['betas'][peak_chi]:.2f}, χ={d['suscepts'][peak_chi]:.2f}")
