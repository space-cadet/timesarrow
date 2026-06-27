"""
Unified plotting module for TimesArrow numerics.

Provides shared infrastructure for data loading, styling, and figure output
to eliminate duplication across visualization scripts.

Usage:
    from src.plotting import load_run, save_figure, COLORS, FIG_SIZES

    data = load_run('t20-p3-L8-3D-fine-20260627')
    fig, ax = plt.subplots(figsize=FIG_SIZES['standard'])
    ax.plot(data['betas'], data['plaquettes'], **COLORS['L8'])
    save_figure(fig, 'my-plot', output_dir='figures/')
"""

import json
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# ─────────────────────────────────────────────────────────────
# Auto-detect project root
# ─────────────────────────────────────────────────────────────

def _find_project_root() -> Path:
    """Find timesarrow numerics root from this file's location."""
    # This file lives at numerics/src/plotting.py
    here = Path(__file__).resolve().parent  # numerics/src/
    return here.parent  # numerics/

PROJECT_ROOT = _find_project_root()

# ─────────────────────────────────────────────────────────────
# Path constants (relative to numerics/)
# ─────────────────────────────────────────────────────────────

PATHS = {
    'output': PROJECT_ROOT / 'output',
    'fss': PROJECT_ROOT / 'data' / 'fss',
    'figures': PROJECT_ROOT / 'figures',
    'docs_assets': PROJECT_ROOT / 'docs' / 'assets',
}

# ─────────────────────────────────────────────────────────────
# Color palette — unified, colorblind-friendly
# ─────────────────────────────────────────────────────────────

# Main palette: distinct hues for each lattice size
LATTICE_COLORS = {
    'L4':  '#E94F37',   # red-orange
    'L6':  '#E67E22',   # orange
    'L8':  '#F1C40F',   # yellow
    'L12': '#2ECC71',   # green
    'L16': '#1ABC9C',   # teal
    'L20': '#3498DB',   # blue
    'L24': '#9B59B6',   # purple
    'L32': '#E84393',   # magenta
}

# Numeric L → color mapping (auto-assigns if not in LATTICE_COLORS)
def color_for_L(L: int) -> str:
    """Get the canonical color for a given lattice size."""
    key = f'L{L}'
    if key in LATTICE_COLORS:
        return LATTICE_COLORS[key]
    # Fallback: generate from a colormap for unknown sizes
    cmap = plt.cm.get_cmap('tab10')
    return cmap(hash(key) % 10)

# Markers for lattice sizes
LATTICE_MARKERS = {
    'L4':  'o',
    'L6':  's',
    'L8':  '^',
    'L12': 'D',
    'L16': 'v',
    'L20': 'p',
    'L24': 'h',
    'L32': '*',
}

def marker_for_L(L: int) -> str:
    """Get the canonical marker for a given lattice size."""
    key = f'L{L}'
    return LATTICE_MARKERS.get(key, 'o')

# Standard plot kwargs for lattice data
def lattice_plot_kwargs(L: int, alpha: float = 0.8, linewidth: float = 2,
                        markersize: Optional[int] = None) -> dict:
    """Return standardized plot kwargs for a given lattice size."""
    ms = markersize or (6 if L <= 16 else 5)
    return {
        'color': color_for_L(L),
        'marker': marker_for_L(L),
        'linestyle': '-',
        'linewidth': linewidth,
        'markersize': ms,
        'alpha': alpha,
        'label': f'L = {L}',
    }

# ─────────────────────────────────────────────────────────────
# Figure size presets
# ─────────────────────────────────────────────────────────────

FIG_SIZES = {
    'standard':     (10, 6),   # single plot, FSS overlays
    'compact':      (8, 5),    # quick plots, documentation
    'wide':         (14, 4.5), # multi-panel horizontal
    'square':       (12, 10),  # 2×2 subplots
    'publication':  (6, 4),    # single column, journal
}

# ─────────────────────────────────────────────────────────────
# Style defaults
# ─────────────────────────────────────────────────────────────

STYLE = {
    'dpi': 150,
    'dpi_publication': 200,
    'font.size': 12,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'grid.alpha': 0.3,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
}

def apply_style():
    """Apply default style settings to matplotlib."""
    plt.rcParams.update({
        'font.size': STYLE['font.size'],
        'axes.titlesize': STYLE['axes.titlesize'],
        'axes.labelsize': STYLE['axes.labelsize'],
        'legend.fontsize': STYLE['legend.fontsize'],
    })

# ─────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────

def find_data_file(run_id: str, search_dirs: Optional[list[Path]] = None) -> Path:
    """Find a JSON data file by run ID across known directories."""
    dirs = search_dirs or [PATHS['output'], PATHS['fss']]
    for d in dirs:
        candidates = list(d.glob(f'{run_id}*.json'))
        if candidates:
            # Prefer exact match, then shortest (most specific)
            exact = [c for c in candidates if c.stem == run_id]
            if exact:
                return exact[0]
            return min(candidates, key=lambda p: len(p.name))
    raise FileNotFoundError(f"No data file found for run '{run_id}' in {dirs}")

def load_json(path: Path) -> dict:
    """Load JSON data from path."""
    with open(path) as f:
        return json.load(f)

def load_run(run_id: str, search_dirs: Optional[list[Path]] = None) -> dict:
    """Load a complete run by ID, returning full JSON with added metadata."""
    path = find_data_file(run_id, search_dirs)
    data = load_json(path)
    data['_meta'] = {
        'run_id': run_id,
        'source_path': str(path),
        'n_betas': len(data.get('results', [])),
    }
    return data

def extract_observables(results: list[dict]) -> dict:
    """
    Extract standard observables from a list of result dicts.

    Returns dict with keys: betas, plaquettes, plaquette_errors,
    susceptibilities, specific_heats, binder_cumulants, polyakovs,
    polyakov_suscepts, polyakov_binders.
    """
    def get(key, default=0.0):
        return np.array([r.get(key, default) for r in results])

    return {
        'betas':              get('beta'),
        'plaquettes':         get('meanPlaquette'),
        'plaquette_errors':   get('errorPlaquette'),
        'susceptibilities':   get('susceptibility'),
        'specific_heats':     get('specificHeat'),
        'binder_cumulants':   get('binderCumulant'),
        'polyakovs':          get('meanPolyakov'),
        'polyakov_suscepts':  get('polyakovSusceptibility'),
        'polyakov_binders':   get('polyakovBinder'),
    }

def extract_L(data: dict) -> Optional[int]:
    """Extract lattice size L from run metadata or parameters."""
    # Try metadata.taskId (e.g., 't20-p3b-L32-lean')
    task_id = data.get('metadata', {}).get('taskId', '')
    if 'L' in task_id:
        # Parse L32 or similar
        import re
        m = re.search(r'L(\d+)', task_id)
        if m:
            return int(m.group(1))
    # Try parameters.L
    params = data.get('parameters', {})
    if 'L' in params:
        return params['L']
    if 'latticeSize' in params:
        return params['latticeSize']
    return None

# ─────────────────────────────────────────────────────────────
# Figure output
# ─────────────────────────────────────────────────────────────

def save_figure(fig: plt.Figure, name: str,
                output_dir: Optional[Path] = None,
                formats: tuple[str, ...] = ('png', 'svg'),
                dpi: Optional[int] = None) -> list[Path]:
    """
    Save figure in specified formats with consistent styling.

    Args:
        fig: matplotlib Figure
        name: base filename (without extension)
        output_dir: directory to save to (default: PATHS['figures'])
        formats: file formats to save
        dpi: override default DPI

    Returns:
        List of saved file paths
    """
    out = output_dir or PATHS['figures']
    out.mkdir(parents=True, exist_ok=True)
    dpi_val = dpi or STYLE['dpi']

    saved = []
    for fmt in formats:
        path = out / f'{name}.{fmt}'
        fig.savefig(path, dpi=dpi_val, bbox_inches=STYLE['savefig.bbox'],
                    pad_inches=STYLE['savefig.pad_inches'])
        saved.append(path)

    return saved

def save_publication(fig: plt.Figure, name: str,
                     output_dir: Optional[Path] = None) -> list[Path]:
    """Save figure at publication quality (200 DPI)."""
    return save_figure(fig, name, output_dir=output_dir, dpi=STYLE['dpi_publication'])

# ─────────────────────────────────────────────────────────────
# Common annotations
# ─────────────────────────────────────────────────────────────

def annotate_beta_c(ax, beta_c: float = 0.76, **kwargs):
    """Add a vertical line marking critical coupling."""
    defaults = {
        'color': 'gray',
        'linestyle': '--',
        'linewidth': 1,
        'alpha': 0.5,
        'label': rf'$\beta_c \approx {beta_c}$',
    }
    defaults.update(kwargs)
    ax.axvline(beta_c, **defaults)

def annotate_ising_U_star(ax, U_star: float = 2/3, **kwargs):
    """Add a horizontal line marking Ising universal Binder cumulant."""
    defaults = {
        'color': 'orange',
        'linestyle': ':',
        'linewidth': 1.5,
        'alpha': 0.7,
        'label': rf'Ising $U^* = {U_star:.3f}$',
    }
    defaults.update(kwargs)
    ax.axhline(U_star, **defaults)

def setup_grid(ax, alpha: Optional[float] = None):
    """Apply consistent grid styling."""
    ax.grid(True, alpha=alpha or STYLE['grid.alpha'])

# ─────────────────────────────────────────────────────────────
# Batch figure generation
# ─────────────────────────────────────────────────────────────

def generate_multi_panel(runs: list[tuple[int, str, str]],
                         observables: list[str],
                         figsize: tuple[float, float] = (12, 10),
                         output_name: Optional[str] = None) -> plt.Figure:
    """
    Generate a multi-panel figure with multiple observables.

    Args:
        runs: list of (L, run_id, label) tuples
        observables: list of observable keys from extract_observables()
        figsize: figure size
        output_name: if given, save figure with this name

    Returns:
        matplotlib Figure
    """
    n = len(observables)
    ncols = 2
    nrows = (n + 1) // 2

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = np.atleast_2d(axes).flatten()

    obs_labels = {
        'plaquettes':       (r'$\beta$', r'$\langle P \rangle$', 'Plaquette'),
        'susceptibilities': (r'$\beta$', r'$\chi$', 'Susceptibility'),
        'specific_heats':   (r'$\beta$', r'$C_V$', 'Specific Heat'),
        'binder_cumulants': (r'$\beta$', r'$U$', 'Binder Cumulant'),
        'polyakovs':        (r'$\beta$', r'$|\langle P \rangle|$', 'Polyakov Loop'),
    }

    for idx, obs_key in enumerate(observables):
        ax = axes[idx]
        xlabel, ylabel, title = obs_labels.get(obs_key, (r'$\beta$', obs_key, obs_key))

        for L, run_id, label in runs:
            data = load_run(run_id)
            obs = extract_observables(data['results'])
            kwargs = lattice_plot_kwargs(L)
            ax.plot(obs['betas'], obs[obs_key], **kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(fontsize=9)
        setup_grid(ax)

    # Hide unused subplots
    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle('Finite-Size Scaling: Multiple Observables', fontsize=14, fontweight='bold')
    plt.tight_layout()

    if output_name:
        save_figure(fig, output_name)

    return fig

# ─────────────────────────────────────────────────────────────
# Module self-test
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("TimesArrow plotting module")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output path: {PATHS['output']}")
    print(f"FSS path: {PATHS['fss']}")
    print(f"Figures path: {PATHS['figures']}")
    print(f"\nAvailable lattice colors: {list(LATTICE_COLORS.keys())}")
    print(f"Available figure sizes: {list(FIG_SIZES.keys())}")

    # Quick smoke test: load a known run
    try:
        run = load_run('t20-p3b-L32-lean-20260627')
        obs = extract_observables(run['results'])
        print(f"\nSmoke test: loaded L=32 run, {len(obs['betas'])} β values")
        print(f"  β range: [{obs['betas'].min():.3f}, {obs['betas'].max():.3f}]")
        print(f"  χ_max: {obs['susceptibilities'].max():.4f}")
        print("✓ Module working")
    except FileNotFoundError as e:
        print(f"\n⚠ Smoke test failed: {e}")
