# T20-TA: Z₂ Lattice Gauge Theory Monte Carlo

*Created: 2026-06-24 15:09 IST*
*Project: timesarrow numerics*
*Depends on: T25 (COMPLETE)*

## Objective
Classical Monte Carlo simulation of Z₂ gauge theory to demonstrate the confinement-deconfinement transition. This is the core numerical demonstration for the timesarrow paper.

## Architecture

**General tools → `ts-quantum/src/lattice/`, specific sim → `timesarrow/numerics/`**

### timesarrow (simulation setup)
- `numerics/src/scripts/t20-z2-lgt-phase1.ts` — 2D square lattice parameter sweep
- `numerics/src/scripts/t20-z2-lgt-phase1.cjs` — Compiled CommonJS version
- `numerics/src/scripts/t20-z2-lgt-phase1-fast.cjs` — Reduced sweeps for quick testing
- `numerics/src/scripts/t20-test.cjs` — Minimal smoke test
- `numerics/output/t20-phase1-fast.json` — Phase 1 raw data + statistics
- `numerics/docs/assets/t20-plaquette-vs-beta.png` — Phase transition plot
- `numerics/docs/assets/t20-susceptibility.png` — Response function plot
- `numerics/docs/assets/t20-error-bars.png` — Statistical quality plot

## Phases

### Phase 1: 2D Square Lattice — ✅ COMPLETE
- Simplest case, exact solution known: β_c = ½ ln(1+√2) ≈ 0.4407
- L = 8, thermal sweeps = 1000, measure sweeps = 5000
- Observables: ⟨P⟩(β), error bars from binning + jackknife

#### Results (L=8)
| β | ⟨P⟩ | Phase |
|---|-----|-------|
| 0.10 | 0.0969 ± 0.0036 | Confined |
| 0.20 | 0.1994 ± 0.0042 | Confined |
| 0.30 | 0.3012 ± 0.0039 | Confined |
| 0.40 | 0.3748 ± 0.0039 | Near critical |
| **0.44** | **0.4162 ± 0.0035** | **Critical** |
| 0.50 | 0.4608 ± 0.0033 | Deconfined |
| 0.60 | 0.5335 ± 0.0030 | Deconfined |
| 0.80 | 0.6645 ± 0.0028 | Deconfined |
| 1.00 | 0.7572 ± 0.0022 | Deconfined |
| 1.50 | 0.9047 ± 0.0017 | Strongly ordered |

### Phase 2: 2D Triangular Lattice — PENDING
- Connects to T25 6-valent intertwiner work
- Different universality class

### Phase 3: 3D Cubic Lattice — PENDING
- Paper target: confinement-deconfinement transition

## Numerics Pages

- `numerics/docs/tasks/t20-z2-lgt.qmd` — Full documentation with theory, results, figures, code
- `numerics/docs/index.qmd` — T20 status: 🟢 Phase 1 Complete
- Deployed to: https://space-cadet.github.io/projects/timesarrow/numerics/tasks/t20-z2-lgt.html

## Commits
- `287ead6` — feat: T20 Phase 1 Z₂ LGT simulation + numerics page
- `389634e` — fix: T25/T20 links on index page
- `bb43032` — feat: T20 Phase 1 plots

## Planned Work

### Interactive Browser Widget
- Compile ts-quantum lattice module to JS bundle (esbuild IIFE)
- Features: L slider, β slider, run button, real-time plot
- Page: `t20-interactive.html` on space-cadet.github.io
- Status: AWAITING USER DECISION

## Dependencies
- ts-quantum `src/lattice/` module (see ts-quantum project memory-bank)
