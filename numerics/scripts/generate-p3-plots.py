#!/usr/bin/env python3
"""Generate 3D lattice plots for T20 Phase 3 results."""

import sys
from pathlib import Path

# Add numerics/ to path for src.plotting import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.plotting import (
    load_run,
    extract_observables,
    save_figure,
    lattice_plot_kwargs,
    annotate_beta_c,
    annotate_ising_U_star,
    setup_grid,
    FIG_SIZES,
    PATHS,
)

import matplotlib.pyplot as plt
import numpy as np

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

OUTPUT_DIR = PATHS['docs_assets']
RUNS = [
    (4,  't20-p3-L4-3D-20250625'),
    (6,  't20-p3-L6-3D-20250625'),
    (8,  't20-p3-L8-3D-20250625'),
]

# ─────────────────────────────────────────────────────────────
# Load all runs
# ─────────────────────────────────────────────────────────────

loaded = {}
for L, run_id in RUNS:
    data = load_run(run_id)
    loaded[L] = extract_observables(data['results'])

# ─────────────────────────────────────────────────────────────
# Helper: plot single observable
# ─────────────────────────────────────────────────────────────

def plot_observable(ax, obs_key, title, ylabel, ylim=None, show_ising_line=False):
    """Plot a single observable for all lattice sizes."""
    for L, obs in loaded.items():
        ax.plot(obs['betas'], obs[obs_key], **lattice_plot_kwargs(L))

    annotate_beta_c(ax)
    if show_ising_line:
        annotate_ising_U_star(ax)

    ax.set_xlabel(r'Coupling $\beta$')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='best', fontsize=9)
    ax.set_xlim(0.45, 1.05)
    if ylim:
        ax.set_ylim(ylim)
    setup_grid(ax)

# ─────────────────────────────────────────────────────────────
# Individual figures
# ─────────────────────────────────────────────────────────────

# Figure 1: Plaquette
fig, ax = plt.subplots(figsize=FIG_SIZES['compact'])
plot_observable(ax, 'plaquettes',
                '3D Z₂ LGT: Plaquette Expectation Value',
                r'Plaquette $\langle P \rangle$',
                ylim=(0.45, 1.02))
ax.legend(loc='lower right', fontsize=10)
save_figure(fig, 't20-p3-plaquette-vs-beta', output_dir=OUTPUT_DIR)
plt.close()

# Figure 2: Susceptibility
fig, ax = plt.subplots(figsize=FIG_SIZES['compact'])
plot_observable(ax, 'susceptibilities',
                '3D Z₂ LGT: Susceptibility (Critical Region)',
                r'Susceptibility $\chi$')
ax.legend(loc='upper right', fontsize=10)
save_figure(fig, 't20-p3-susceptibility-vs-beta', output_dir=OUTPUT_DIR)
plt.close()

# Figure 3: Specific Heat
fig, ax = plt.subplots(figsize=FIG_SIZES['compact'])
plot_observable(ax, 'specific_heats',
                '3D Z₂ LGT: Specific Heat',
                r'Specific Heat $C_V$')
ax.legend(loc='upper right', fontsize=10)
save_figure(fig, 't20-p3-specific-heat-vs-beta', output_dir=OUTPUT_DIR)
plt.close()

# Figure 4: Binder Cumulant
fig, ax = plt.subplots(figsize=FIG_SIZES['compact'])
plot_observable(ax, 'binder_cumulants',
                '3D Z₂ LGT: Binder Cumulant',
                r'Binder Cumulant $U$',
                ylim=(0.62, 0.68),
                show_ising_line=True)
ax.legend(loc='lower right', fontsize=10)
save_figure(fig, 't20-p3-binder-vs-beta', output_dir=OUTPUT_DIR)
plt.close()

# ─────────────────────────────────────────────────────────────
# Figure 5: Combined 2×2 subplot
# ─────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=FIG_SIZES['square'])

# Map: (row, col) → (observable_key, title, ylabel)
panels = [
    ((0, 0), 'plaquettes',       r'$\langle P \rangle$', 'Plaquette Expectation'),
    ((0, 1), 'susceptibilities', r'$\chi$',              'Susceptibility'),
    ((1, 0), 'specific_heats',   r'$C_V$',               'Specific Heat'),
    ((1, 1), 'binder_cumulants', r'$U$',                 'Binder Cumulant'),
]

for (row, col), obs_key, ylabel, title in panels:
    ax = axes[row, col]
    for L, obs in loaded.items():
        ax.plot(obs['betas'], obs[obs_key], **lattice_plot_kwargs(L, markersize=5))
    annotate_beta_c(ax)
    if obs_key == 'binder_cumulants':
        annotate_ising_U_star(ax)
    ax.set_xlabel(r'$\beta$')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(fontsize=8)
    setup_grid(ax)

plt.suptitle('3D Z₂ Lattice Gauge Theory: Phase Transition', fontsize=14, fontweight='bold')
plt.tight_layout()
save_figure(fig, 't20-p3-combined', output_dir=OUTPUT_DIR)
plt.close()

print(f"Generated 5 figures in {OUTPUT_DIR}")
