#!/usr/bin/env python3
"""Generate 3D FSS plots for all available T20 Phase 3 data."""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Setup
output_dir = Path("/Users/sage/.openclaw/workspace/code/timesarrow/numerics/figures")
output_dir.mkdir(parents=True, exist_ok=True)

# Load all available data
base = Path("/Users/sage/.openclaw/workspace/code/timesarrow/numerics")

def load_data(path):
    with open(path) as f:
        return json.load(f)

data_files = {
    'L4': base / "output/t20-p3-L4-3D-20250625.json",
    'L6': base / "output/t20-p3-L6-3D-20250625.json",
    'L8': base / "output/t20-p3-L8-3D-20250625.json",
    'L8_fine': base / "data/fss/t20-p3b-L8-3D-fine-20260627.json",
    'L16': base / "data/fss/t20-p3b-L16-3D-fine-20260626.json",
    'L24': base / "output/t20-p3-L24-3D-wilson-fine-20250626.json",
    'L32': base / "output/t20-p3-L32-3D-wilson-fine-20250626.json",
}

data = {}
for label, path in data_files.items():
    try:
        data[label] = load_data(path)
        print(f"Loaded {label}: {len(data[label]['results'])} betas")
    except Exception as e:
        print(f"Failed to load {label}: {e}")

def extract(results):
    beta = [r["beta"] for r in results]
    plaquette = [r["meanPlaquette"] for r in results]
    err_plaquette = [r.get("errorPlaquette", 0) for r in results]
    chi = [r["susceptibility"] for r in results]
    cv = [r["specificHeat"] for r in results]
    binder = [r["binderCumulant"] for r in results]
    # Polyakov loop if available
    polyakov = [r.get("meanPolyakov", None) for r in results]
    return beta, plaquette, err_plaquette, chi, cv, binder, polyakov

extracted = {}
for label, d in data.items():
    extracted[label] = extract(d["results"])

# Color scheme - gradient from light to dark
L_values = {
    'L4': 4, 'L6': 6, 'L8': 8, 'L16': 16, 'L24': 24, 'L32': 32
}

colors = {
    'L4': '#e74c3c',    # red
    'L6': '#e67e22',    # orange
    'L8': '#f1c40f',    # yellow
    'L16': '#2ecc71',   # green
    'L24': '#3498db',   # blue
    'L32': '#9b59b6',   # purple
}

markers = {
    'L4': 'o', 'L6': 's', 'L8': '^', 'L16': 'D', 'L24': 'v', 'L32': 'p'
}

# Figure 1: Plaquette vs Beta (FSS - all L values)
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L4', 'L6', 'L8', 'L16', 'L24', 'L32']:
    if label in extracted:
        b, p, _, _, _, _, _ = extracted[label]
        ax.plot(b, p, markers[label]+'-', color=colors[label], 
                label=f'L = {L_values[label]}', linewidth=2, markersize=6, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Plaquette $\langle P \rangle$', fontsize=12)
ax.set_title('3D Z₂ LGT: Finite-Size Scaling — Plaquette', fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=10, ncol=2)
ax.set_xlim(0.25, 1.25)
ax.set_ylim(0.25, 1.05)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-fss-plaquette.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-fss-plaquette.svg', bbox_inches='tight')
plt.close()

# Figure 2: Susceptibility vs Beta (FSS)
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L4', 'L6', 'L8', 'L16', 'L24', 'L32']:
    if label in extracted:
        b, _, _, chi, _, _, _ = extracted[label]
        ax.plot(b, chi, markers[label]+'-', color=colors[label], 
                label=f'L = {L_values[label]}', linewidth=2, markersize=6, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Susceptibility $\chi$', fontsize=12)
ax.set_title('3D Z₂ LGT: Finite-Size Scaling — Susceptibility', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=10, ncol=2)
ax.set_xlim(0.25, 1.25)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-fss-susceptibility.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-fss-susceptibility.svg', bbox_inches='tight')
plt.close()

# Figure 3: Specific Heat vs Beta (FSS)
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L4', 'L6', 'L8', 'L16', 'L24', 'L32']:
    if label in extracted:
        b, _, _, _, cv, _, _ = extracted[label]
        ax.plot(b, cv, markers[label]+'-', color=colors[label], 
                label=f'L = {L_values[label]}', linewidth=2, markersize=6, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Specific Heat $C_V$', fontsize=12)
ax.set_title('3D Z₂ LGT: Finite-Size Scaling — Specific Heat', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=10, ncol=2)
ax.set_xlim(0.25, 1.25)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-fss-specific-heat.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-fss-specific-heat.svg', bbox_inches='tight')
plt.close()

# Figure 4: Binder Cumulant vs Beta (FSS)
fig, ax = plt.subplots(figsize=(10, 6))
for label in ['L4', 'L6', 'L8', 'L16', 'L24', 'L32']:
    if label in extracted:
        b, _, _, _, _, binder, _ = extracted[label]
        ax.plot(b, binder, markers[label]+'-', color=colors[label], 
                label=f'L = {L_values[label]}', linewidth=2, markersize=6, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5, label=r'$\beta_c \approx 0.76$')
ax.axhline(y=2/3, color='orange', linestyle=':', alpha=0.7, label=r'Ising $U^* = 2/3$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Binder Cumulant $U$', fontsize=12)
ax.set_title('3D Z₂ LGT: Finite-Size Scaling — Binder Cumulant', fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=10, ncol=2)
ax.set_xlim(0.25, 1.25)
ax.set_ylim(0.62, 0.68)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-fss-binder.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-fss-binder.svg', bbox_inches='tight')
plt.close()

# Figure 5: Critical Region Zoom (L8 fine + L16 + L24 + L32)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plaquette zoom
critical_labels = ['L8_fine', 'L16', 'L24', 'L32']
critical_colors = {'L8_fine': '#2ecc71', 'L16': '#f1c40f', 'L24': '#3498db', 'L32': '#9b59b6'}
critical_markers = {'L8_fine': '^', 'L16': 'D', 'L24': 'v', 'L32': 'p'}

ax = axes[0, 0]
for label in critical_labels:
    if label in extracted:
        b, p, _, _, _, _, _ = extracted[label]
        L = 8 if label == 'L8_fine' else int(label[1:])
        ax.plot(b, p, critical_markers[label]+'-', color=critical_colors[label], 
                label=f'L = {L}', linewidth=2, markersize=5, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$\langle P \rangle$')
ax.set_title('Plaquette (Critical Region)')
ax.legend()
ax.set_xlim(0.68, 0.85)
ax.grid(True, alpha=0.3)

# Susceptibility zoom
ax = axes[0, 1]
for label in critical_labels:
    if label in extracted:
        b, _, _, chi, _, _, _ = extracted[label]
        L = 8 if label == 'L8_fine' else int(label[1:])
        ax.plot(b, chi, critical_markers[label]+'-', color=critical_colors[label], 
                label=f'L = {L}', linewidth=2, markersize=5, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$\chi$')
ax.set_title('Susceptibility (Critical Region)')
ax.legend()
ax.set_xlim(0.68, 0.85)
ax.grid(True, alpha=0.3)

# Specific Heat zoom
ax = axes[1, 0]
for label in critical_labels:
    if label in extracted:
        b, _, _, _, cv, _, _ = extracted[label]
        L = 8 if label == 'L8_fine' else int(label[1:])
        ax.plot(b, cv, critical_markers[label]+'-', color=critical_colors[label], 
                label=f'L = {L}', linewidth=2, markersize=5, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$C_V$')
ax.set_title('Specific Heat (Critical Region)')
ax.legend()
ax.set_xlim(0.68, 0.85)
ax.grid(True, alpha=0.3)

# Binder zoom
ax = axes[1, 1]
for label in critical_labels:
    if label in extracted:
        b, _, _, _, _, binder, _ = extracted[label]
        L = 8 if label == 'L8_fine' else int(label[1:])
        ax.plot(b, binder, critical_markers[label]+'-', color=critical_colors[label], 
                label=f'L = {L}', linewidth=2, markersize=5, alpha=0.8)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5)
ax.axhline(y=2/3, color='orange', linestyle=':', alpha=0.7)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$U$')
ax.set_title('Binder Cumulant (Critical Region)')
ax.legend()
ax.set_xlim(0.68, 0.85)
ax.set_ylim(0.62, 0.68)
ax.grid(True, alpha=0.3)

plt.suptitle('3D Z₂ LGT: Critical Region Zoom', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-fss-critical-zoom.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-fss-critical-zoom.svg', bbox_inches='tight')
plt.close()

# Figure 6: Polyakov Loop (if available)
has_polyakov = any(any(p is not None for p in extracted[label][6]) for label in extracted)
if has_polyakov:
    fig, ax = plt.subplots(figsize=(10, 6))
    for label in ['L8', 'L16', 'L24', 'L32']:
        if label in extracted:
            b, _, _, _, _, _, poly = extracted[label]
            if any(p is not None for p in poly):
                ax.plot(b, [abs(p) if p is not None else 0 for p in poly], 
                       markers[label]+'-', color=colors[label], 
                       label=f'L = {L_values[label]}', linewidth=2, markersize=6, alpha=0.8)
    ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.5, label=r'$\beta_c \approx 0.76$')
    ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
    ax.set_ylabel(r'$|\langle P \rangle|$ (Polyakov Loop)', fontsize=12)
    ax.set_title('3D Z₂ LGT: Polyakov Loop (Order Parameter)', fontsize=13, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.set_xlim(0.25, 1.25)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(output_dir / 't20-p3-fss-polyakov.png', dpi=150, bbox_inches='tight')
    fig.savefig(output_dir / 't20-p3-fss-polyakov.svg', bbox_inches='tight')
    plt.close()

print(f"Generated {len(list(output_dir.glob('t20-p3-fss*')))} figures in {output_dir}")
for f in sorted(output_dir.glob('t20-p3-fss*')):
    print(f"  {f.name}")
