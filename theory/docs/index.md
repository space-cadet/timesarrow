# TimesArrow Theory Index

**Last Updated:** 2026-07-18

## Overview

This directory contains theoretical investigations, analytical constructions, and symmetry analysis related to the TimesArrow project. Unlike the numerics folder which focuses on simulations and data, the theory folder focuses on:

- Symmetry analysis (CZX, SPT, gauge invariance)
- Intertwiner space constructions
- Analytical solutions and exact results
- Connections to loop quantum gravity and spin-network theory
- Theoretical frameworks for quantum geometry

## Active Investigations

### T35a: CZX-Intertwiner Compatibility
- **Status:** Active — Partial Results
- **Question:** Can CZX-symmetric states coexist with gauge-invariant intertwiner subspace?
- **Files:**
  - `../numerics/scripts/t35a-czx-intertwiner-overlap.cjs` — overlap test (toy model)
  - `../numerics/scripts/t35a-square-plaquette.cjs` — CZX operator construction
  - `../numerics/scripts/t35a-czx-product-test.cjs` — product state analysis
  - `docs/czx-intertwiner-analysis.md` — detailed analysis
- **Key Result:** 2D toy model (2-valent) shows positive overlap, but correct 4-valent analysis is pending

## Directory Structure

```
theory/
├── docs/              # Theory documentation and analysis
│   ├── index.md       # This file
│   └── czx-intertwiner-analysis.md  # T35a detailed analysis
├── pages/             # Dashboard and visualizations
│   └── dashboard.html # Theory dashboard (vanilla JS)
└── README.md          # Project overview
```

## Relationship to Numerics

| Theory Concept | Numerics Implementation | Status |
|---------------|---------------------------|--------|
| CZX symmetry | `t35a-square-plaquette.cjs` | ✅ Working |
| Intertwiner gauge | `t35a-square-plaquette-intertwiner.cjs` | ⚠️ Toy model |
| SPT order parameters | — | Not yet implemented |
| Wilson loops | T20 numerics | ✅ Complete |
| Volume observables | T31 numerics | ✅ Complete |
| Polyakov loop | T31 numerics | ✅ Complete |

## How to Use

1. **Dashboard:** Open `pages/dashboard.html` in a browser for an overview
2. **Documentation:** Read `docs/*.md` for detailed analysis
3. **Scripts:** Run `numerics/scripts/t35a*.cjs` for computational verification

## Adding New Theory Work

1. Create a new markdown file in `docs/`
2. Update this index with the new investigation
3. Update `pages/dashboard.html` with the new task/data entry
4. Link to relevant numerics scripts in `numerics/scripts/`

## Conventions

- **Task IDs:** Use T35a, T35b, etc. (aligned with numerics task numbering)
- **Status tags:** `active`, `complete`, `pending`, `blocked`
- **Geometry notation:** 2D = square lattice, 3D = diamond lattice
- **Valence notation:** n-valent = n edges per vertex
