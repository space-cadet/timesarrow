#!/usr/bin/env python3
"""Generate 3D lattice plots for T20 Phase 3 results."""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Setup
output_dir = Path("/Users/sage/.openclaw/workspace/code/timesarrow/numerics/docs/assets")
output_dir.mkdir(parents=True, exist_ok=True)

# Load data
base = Path("/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output")

def load_data(filename):
    with open(base / filename) as f:
        return json.load(f)

data_l4 = load_data("t20-p3-L4-3D-20250625.json")
data_l6 = load_data("t20-p3-L6-3D-20250625.json")
data_l8 = load_data("t20-p3-L8-3D-20250625.json")

def extract(results):
    beta = [r["beta"] for r in results]
    plaquette = [r["meanPlaquette"] for r in results]
    chi = [r["susceptibility"] for r in results]
    cv = [r["specificHeat"] for r in results]
    binder = [r["binderCumulant"] for r in results]
    return beta, plaquette, chi, cv, binder

b4, p4, c4, cv4, u4 = extract(data_l4["results"])
b6, p6, c6, cv6, u6 = extract(data_l6["results"])
b8, p8, c8, cv8, u8 = extract(data_l8["results"])

# Color scheme
colors = {'L4': '#e74c3c', 'L6': '#3498db', 'L8': '#2ecc71'}

# Figure 1: Plaquette vs Beta
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(b4, p4, 'o-', color=colors['L4'], label='L = 4', linewidth=2, markersize=6)
ax.plot(b6, p6, 's-', color=colors['L6'], label='L = 6', linewidth=2, markersize=6)
ax.plot(b8, p8, '^-', color=colors['L8'], label='L = 8', linewidth=2, markersize=6)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Plaquette $\langle P \rangle$', fontsize=12)
ax.set_title('3D Z₂ LGT: Plaquette Expectation Value', fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim(0.45, 1.05)
ax.set_ylim(0.45, 1.02)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-plaquette-vs-beta.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-plaquette-vs-beta.svg', bbox_inches='tight')
plt.close()

# Figure 2: Susceptibility vs Beta
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(b4, c4, 'o-', color=colors['L4'], label='L = 4', linewidth=2, markersize=6)
ax.plot(b6, c6, 's-', color=colors['L6'], label='L = 6', linewidth=2, markersize=6)
ax.plot(b8, c8, '^-', color=colors['L8'], label='L = 8', linewidth=2, markersize=6)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Susceptibility $\chi$', fontsize=12)
ax.set_title('3D Z₂ LGT: Susceptibility (Critical Region)', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.set_xlim(0.45, 1.05)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-susceptibility-vs-beta.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-susceptibility-vs-beta.svg', bbox_inches='tight')
plt.close()

# Figure 3: Specific Heat vs Beta
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(b4, cv4, 'o-', color=colors['L4'], label='L = 4', linewidth=2, markersize=6)
ax.plot(b6, cv6, 's-', color=colors['L6'], label='L = 6', linewidth=2, markersize=6)
ax.plot(b8, cv8, '^-', color=colors['L8'], label='L = 8', linewidth=2, markersize=6)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Specific Heat $C_V$', fontsize=12)
ax.set_title('3D Z₂ LGT: Specific Heat', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.set_xlim(0.45, 1.05)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-specific-heat-vs-beta.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-specific-heat-vs-beta.svg', bbox_inches='tight')
plt.close()

# Figure 4: Binder Cumulant vs Beta
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(b4, u4, 'o-', color=colors['L4'], label='L = 4', linewidth=2, markersize=6)
ax.plot(b6, u6, 's-', color=colors['L6'], label='L = 6', linewidth=2, markersize=6)
ax.plot(b8, u8, '^-', color=colors['L8'], label='L = 8', linewidth=2, markersize=6)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7, label=r'$\beta_c \approx 0.76$')
ax.axhline(y=2/3, color='orange', linestyle=':', alpha=0.7, label=r'Ising $U^* = 2/3$')
ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
ax.set_ylabel(r'Binder Cumulant $U$', fontsize=12)
ax.set_title('3D Z₂ LGT: Binder Cumulant', fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim(0.45, 1.05)
ax.set_ylim(0.62, 0.68)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-binder-vs-beta.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-binder-vs-beta.svg', bbox_inches='tight')
plt.close()

# Figure 5: Combined subplot
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plaquette
ax = axes[0, 0]
ax.plot(b4, p4, 'o-', color=colors['L4'], label='L=4', linewidth=2, markersize=5)
ax.plot(b6, p6, 's-', color=colors['L6'], label='L=6', linewidth=2, markersize=5)
ax.plot(b8, p8, '^-', color=colors['L8'], label='L=8', linewidth=2, markersize=5)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$\langle P \rangle$')
ax.set_title('Plaquette Expectation')
ax.legend()
ax.grid(True, alpha=0.3)

# Susceptibility
ax = axes[0, 1]
ax.plot(b4, c4, 'o-', color=colors['L4'], label='L=4', linewidth=2, markersize=5)
ax.plot(b6, c6, 's-', color=colors['L6'], label='L=6', linewidth=2, markersize=5)
ax.plot(b8, c8, '^-', color=colors['L8'], label='L=8', linewidth=2, markersize=5)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$\chi$')
ax.set_title('Susceptibility')
ax.legend()
ax.grid(True, alpha=0.3)

# Specific Heat
ax = axes[1, 0]
ax.plot(b4, cv4, 'o-', color=colors['L4'], label='L=4', linewidth=2, markersize=5)
ax.plot(b6, cv6, 's-', color=colors['L6'], label='L=6', linewidth=2, markersize=5)
ax.plot(b8, cv8, '^-', color=colors['L8'], label='L=8', linewidth=2, markersize=5)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$C_V$')
ax.set_title('Specific Heat')
ax.legend()
ax.grid(True, alpha=0.3)

# Binder
ax = axes[1, 1]
ax.plot(b4, u4, 'o-', color=colors['L4'], label='L=4', linewidth=2, markersize=5)
ax.plot(b6, u6, 's-', color=colors['L6'], label='L=6', linewidth=2, markersize=5)
ax.plot(b8, u8, '^-', color=colors['L8'], label='L=8', linewidth=2, markersize=5)
ax.axvline(x=0.76, color='gray', linestyle='--', alpha=0.7)
ax.axhline(y=2/3, color='orange', linestyle=':', alpha=0.7)
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$U$')
ax.set_title('Binder Cumulant')
ax.legend()
ax.grid(True, alpha=0.3)

plt.suptitle('3D Z₂ Lattice Gauge Theory: Phase Transition', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(output_dir / 't20-p3-combined.png', dpi=150, bbox_inches='tight')
fig.savefig(output_dir / 't20-p3-combined.svg', bbox_inches='tight')
plt.close()

print(f"Generated 5 figures in {output_dir}")
