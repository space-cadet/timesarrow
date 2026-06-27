# T30: Unified Plotting Module — Implementation Details

*Created: 2026-06-27*

## Architecture

```
numerics/
├── src/
│   └── plotting.py          ← New: shared infrastructure
├── scripts/
│   ├── generate-p3-plots.py       ← Refactor to use plotting.py
│   └── generate-p3-fss-plots.py   ← Refactor to use plotting.py
├── src/scripts/
│   ├── t20-critical-exponents.py      ← Refactor
│   ├── t20-scaling-collapse.py        ← Refactor
│   ├── t20-binder-crossing-analysis.py ← Refactor
│   └── ... (14 more scripts)
├── output/                   ← Raw simulation JSON
├── data/fss/                ← Fine-scan / checkpoint JSON
├── figures/                 ← Generated figures (via plotting.py default)
└── docs/assets/             ← Documentation figures
```

## Module API

### Constants

```python
# Paths (auto-detected)
PROJECT_ROOT          # numerics/ directory
PATHS['output']       # numerics/output/
PATHS['fss']          # numerics/data/fss/
PATHS['figures']      # numerics/figures/
PATHS['docs_assets']  # numerics/docs/assets/

# Colors
LATTICE_COLORS['L4']  → '#E94F37'
LATTICE_COLORS['L8']  → '#F1C40F'
LATTICE_COLORS['L32'] → '#E84393'
# ... etc

# Figure sizes
FIG_SIZES['standard']      → (10, 6)
FIG_SIZES['compact']       → (8, 5)
FIG_SIZES['wide']          → (14, 4.5)
FIG_SIZES['square']        → (12, 10)
FIG_SIZES['publication']   → (6, 4)

# Style defaults
STYLE['dpi']               → 150
STYLE['dpi_publication']   → 200
STYLE['grid.alpha']        → 0.3
```

### Functions

#### Data Loading

```python
load_run(run_id: str) → dict
    # Finds and loads JSON from output/ or data/fss/
    # Adds _meta with run_id, source_path, n_betas

extract_observables(results: list[dict]) → dict
    # Extracts: betas, plaquettes, plaquette_errors,
    #           susceptibilities, specific_heats, binder_cumulants,
    #           polyakovs, polyakov_suscepts, polyakov_binders
    # All returned as numpy arrays

extract_L(data: dict) → int | None
    # Extracts L from metadata.taskId or parameters.L
```

#### Styling

```python
color_for_L(L: int) → str
marker_for_L(L: int) → str
lattice_plot_kwargs(L: int, ...) → dict
    # Returns: {color, marker, linestyle, linewidth, markersize, alpha, label}

apply_style() → None
    # Sets matplotlib rcParams for consistent fonts
```

#### Output

```python
save_figure(fig, name, output_dir=None, formats=('png', 'svg'), dpi=None) → list[Path]
    # Saves PNG + SVG by default
    # Returns list of saved paths

save_publication(fig, name, output_dir=None) → list[Path]
    # Convenience: 200 DPI save
```

#### Annotations

```python
annotate_beta_c(ax, beta_c=0.76, **kwargs)
    # Gray dashed vertical line + label

annotate_ising_U_star(ax, U_star=2/3, **kwargs)
    # Orange dotted horizontal line + label

setup_grid(ax, alpha=None)
    # Consistent grid styling
```

#### Batch

```python
generate_multi_panel(runs, observables, figsize=(12,10), output_name=None) → Figure
    # Generates 2×N/2 subplot grid for multiple observables
    # Optionally saves figure
```

## Color Palette Design

The palette is designed for:
1. **Distinctness**: Each L value has a unique hue
2. **Colorblind safety**: Avoids red-green confusion (red-orange and green are far apart in hue)
3. **Monotonic progression**: Larger L → warmer/darker colors (roughly)
4. **Literature consistency**: Where figures already exist, closest match preserved

| L | Hex | Hue | Notes |
|---|-----|-----|-------|
| 4 | #E94F37 | Red-orange | Matches existing L4 color |
| 6 | #E67E22 | Orange | Matches existing L6 color |
| 8 | #F1C40F | Yellow | Matches existing L8 color |
| 12 | #2ECC71 | Green | |
| 16 | #1ABC9C | Teal | |
| 20 | #3498DB | Blue | |
| 24 | #9B59B6 | Purple | |
| 32 | #E84393 | Magenta | Distinct from L4 red |

## Migration Strategy

### For each script to refactor:

1. **Replace imports**:
   ```python
   # OLD
   import json
   import matplotlib.pyplot as plt
   import numpy as np
   from pathlib import Path

   # NEW
   import sys
   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
   from src.plotting import (
       load_run, extract_observables, save_figure,
       COLORS, FIG_SIZES, annotate_beta_c, setup_grid
   )
   ```

2. **Replace data loading**:
   ```python
   # OLD
   def load_data(path):
       with open(path) as f:
           return json.load(f)
   data = load_data(base / "t20-p3-L8-3D-fine-20250627.json")

   # NEW
   data = load_run('t20-p3b-L8-3D-fine-20260627')
   obs = extract_observables(data['results'])
   ```

3. **Replace plotting boilerplate**:
   ```python
   # OLD
   fig, ax = plt.subplots(figsize=(8, 5))
   ax.plot(b8, p8, '^-', color=colors['L8'], label='L = 8', ...)
   ax.set_xlabel(r'Coupling $\beta$', fontsize=12)
   # ... tight_layout, savefig boilerplate

   # NEW
   fig, ax = plt.subplots(figsize=FIG_SIZES['compact'])
   ax.plot(obs['betas'], obs['plaquettes'], **lattice_plot_kwargs(8))
   annotate_beta_c(ax)
   setup_grid(ax)
   save_figure(fig, 'my-plot')
   ```

## Testing

The module includes a self-test on `__main__`:

```bash
cd numerics
python src/plotting.py
```

Expected output:
```
TimesArrow plotting module
Project root: /Users/sage/.openclaw/workspace/code/timesarrow/numerics
Output path: .../numerics/output
FSS path: .../numerics/data/fss
Figures path: .../numerics/figures
Available lattice colors: ['L4', 'L6', 'L8', 'L12', 'L16', 'L20', 'L24', 'L32']
Available figure sizes: ['standard', 'compact', 'wide', 'square', 'publication']

Smoke test: loaded L=32 run, 21 β values
  β range: [0.740, 0.780]
  χ_max: 1.3704
✓ Module working
```

## Future Work (Tier 2/3)

- **Tier 2**: Single CLI script `generate-plots.py --phase 3 --lattices 4,6,8,16,32`
- **Tier 3**: Analysis pipeline unification (fitting, exponent extraction)
- **Registry integration**: Read `data/registry.json` instead of globbing files
- **Observable plugins**: Allow custom observable extraction without modifying the module
