#!/usr/bin/env python3
"""Generate 3D FSS plots for all available T20 Phase 3 data."""

import sys
from pathlib import Path

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

OUTPUT_DIR = PATHS['figures']

# Run definitions: (label_for_display, L_value, run_id, search_dirs)
# search_dirs defaults to [PATHS['output'], PATHS['fss']]
ALL_L_RUNS = [
    (4,   't20-p3-L4-3D-20250625'),
    (6,   't20-p3-L6-3D-20250625'),
    (8,   't20-p3-L8-3D-20250625'),
    (16,  't20-p3b-L16-3D-fine-20260626'),
    (24,  't20-p3-L24-3D-wilson-fine-20250626'),
    (32,  't20-p3-L32-3D-wilson-fine-20250626'),
]

CRITICAL_RUNS = [
    (8,   't20-p3b-L8-3D-fine-20260627'),   # fine scan
    (16,  't20-p3b-L16-3D-fine-20260626'),
    (24,  't20-p3-L24-3D-wilson-fine-20250626'),
    (32,  't20-p3-L32-3D-wilson-fine-20250626'),
]

# ─────────────────────────────────────────────────────────────
# Load all runs
# ─────────────────────────────────────────────────────────────

def load_runs(run_list):
    """Load a list of (L, run_id) tuples, returning {L: obs_dict}."""
    loaded = {}
    for L, run_id in run_list:
        try:
            data = load_run(run_id)
            loaded[L] = extract_observables(data['results'])
            print(f"  Loaded L={L}: {len(loaded[L]['betas'])} β values")
        except FileNotFoundError as e:
            print(f"  ⚠ L={L}: {e}")
    return loaded

print("Loading all-L runs...")
all_l = load_runs(ALL_L_RUNS)

print("Loading critical region runs...")
critical = load_runs(CRITICAL_RUNS)

# ─────────────────────────────────────────────────────────────
# Helper: plot single observable across lattice sizes
# ─────────────────────────────────────────────────────────────

def plot_fss(ax, obs_key, data_dict, title, ylabel, ylim=None,
             show_ising_line=False, xlim=(0.25, 1.25), ncol=2):
    """Plot FSS overlay for a single observable."""
    for L, obs in sorted(data_dict.items()):
        ax.plot(obs['betas'], obs[obs_key], **lattice_plot_kwargs(L))

    annotate_beta_c(ax)
    if show_ising_line:
        annotate_ising_U_star(ax)

    ax.set_xlabel(r'Coupling $\beta$')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='best', fontsize=9, ncol=ncol)
    ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    setup_grid(ax)

# ─────────────────────────────────────────────────────────────
# Figures 1–4: FSS overlays (all L values)
# ─────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])
plot_fss(ax, 'plaquettes', all_l,
         '3D Z₂ LGT: Finite-Size Scaling — Plaquette',
         r'Plaquette $\langle P \rangle$',
         ylim=(0.25, 1.05))
save_figure(fig, 't20-p3-fss-plaquette', output_dir=OUTPUT_DIR)
plt.close()

fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])
plot_fss(ax, 'susceptibilities', all_l,
         '3D Z₂ LGT: Finite-Size Scaling — Susceptibility',
         r'Susceptibility $\chi$')
save_figure(fig, 't20-p3-fss-susceptibility', output_dir=OUTPUT_DIR)
plt.close()

fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])
plot_fss(ax, 'specific_heats', all_l,
         '3D Z₂ LGT: Finite-Size Scaling — Specific Heat',
         r'Specific Heat $C_V$')
save_figure(fig, 't20-p3-fss-specific-heat', output_dir=OUTPUT_DIR)
plt.close()

fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])
plot_fss(ax, 'binder_cumulants', all_l,
         '3D Z₂ LGT: Finite-Size Scaling — Binder Cumulant',
         r'Binder Cumulant $U$',
         ylim=(0.62, 0.68),
         show_ising_line=True)
save_figure(fig, 't20-p3-fss-binder', output_dir=OUTPUT_DIR)
plt.close()

# ─────────────────────────────────────────────────────────────
# Figure 5: Critical Region Zoom (2×2 subplot)
# ─────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=FIG_SIZES['square'])

panels = [
    ((0, 0), 'plaquettes',       r'$\langle P \rangle$', 'Plaquette (Critical Region)'),
    ((0, 1), 'susceptibilities', r'$\chi$',              'Susceptibility (Critical Region)'),
    ((1, 0), 'specific_heats',   r'$C_V$',               'Specific Heat (Critical Region)'),
    ((1, 1), 'binder_cumulants', r'$U$',                 'Binder Cumulant (Critical Region)'),
]

for (row, col), obs_key, ylabel, title in panels:
    ax = axes[row, col]
    for L, obs in sorted(critical.items()):
        ax.plot(obs['betas'], obs[obs_key], **lattice_plot_kwargs(L, markersize=5))
    annotate_beta_c(ax)
    if obs_key == 'binder_cumulants':
        annotate_ising_U_star(ax)
    ax.set_xlabel(r'$\beta$')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.set_xlim(0.68, 0.85)
    if obs_key == 'binder_cumulants':
        ax.set_ylim(0.62, 0.68)
    setup_grid(ax)

plt.suptitle('3D Z₂ LGT: Critical Region Zoom', fontsize=14, fontweight='bold')
plt.tight_layout()
save_figure(fig, 't20-p3-fss-critical-zoom', output_dir=OUTPUT_DIR)
plt.close()

# ─────────────────────────────────────────────────────────────
# Figure 6: Polyakov Loop (if available)
# ─────────────────────────────────────────────────────────────

has_polyakov = any(
    any(p is not None for p in obs['polyakovs'])
    for obs in all_l.values()
)

if has_polyakov:
    fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])
    for L, obs in sorted(all_l.items()):
        poly = obs['polyakovs']
        if any(p is not None for p in poly):
            ax.plot(obs['betas'], [abs(p) if p is not None else 0 for p in poly],
                   **lattice_plot_kwargs(L))
    annotate_beta_c(ax)
    ax.set_xlabel(r'Coupling $\beta$')
    ax.set_ylabel(r'$|\langle P \rangle|$ (Polyakov Loop)')
    ax.set_title('3D Z₂ LGT: Polyakov Loop (Order Parameter)')
    ax.legend(loc='lower right', fontsize=10)
    ax.set_xlim(0.25, 1.25)
    setup_grid(ax)
    save_figure(fig, 't20-p3-fss-polyakov', output_dir=OUTPUT_DIR)
    plt.close()

# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────

print(f"\nGenerated {len(list(OUTPUT_DIR.glob('t20-p3-fss*')))} figures in {OUTPUT_DIR}")
for f in sorted(OUTPUT_DIR.glob('t20-p3-fss*')):
    print(f"  {f.name}")
