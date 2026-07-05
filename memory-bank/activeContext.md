# timesarrow — Active Context

*Updated: 2026-07-05 23:12:09 IST*

## Current Session — 2026-07-05 Night

### T32: Post-May Numerics Correction and Reproducibility Pass — IN PROGRESS 🔄

- T20d's first-order conclusion is superseded; existing data must be reanalysed using continuous 3D Ising-universality scaling.
- The plaquette Binder value near $2/3$ is not accepted evidence of first-order behavior, and schematic histograms are not numerical evidence.
- T22a is a normalized SU(2) four-leg group average, not a complete FK/EPRL vertex amplitude; the extra squaring to $0.20$ must be removed.
- T31 must not use greedy gauge alignment because spanning-tree alignment can force $|Q|=N$ in any phase.
- T25 spectral pairing remains useful but does not alone establish a physical time-orientation symmetry.
- TypeScript/Rust build and test reproducibility must be restored before manuscript promotion.
- `timesarrow.tex` remains gated from post-May numerical claims until T32 is complete.

**T20d correction progress (2026-07-05 23:12 IST):**

- Rewrote `t20d-fss-analysis.tex` around continuous 3D Ising universality.
- Corrected and rebuilt the canonical T20 Quarto task page and both tracked HTML outputs.
- Removed the first-order, latent-heat, synthetic-histogram, and failed-collapse claims from rendered publication text.
- Preserved raw data; numerical reanalysis, dashboard correction, and figure retirement/replacement remain open.

**Plan:** `implementation-details/post-may-numerics-correction-plan.md`

## Previous Session — 2026-07-02 Evening

> Superseded on 2026-07-05: the T20d, T22a, and T31 interpretations below are retained as historical session context, not current guidance.

### T31: Signed Volume Observable — IN PROGRESS 🔄
- **Concept**: Use signed volume operator Q̂ (not positive-definite V̂) for composite systems
- **Key insight**: Emergence of global time orientation ↔ emergence of macroscopic signed volume
- **Confined phase**: |Q| ~ √N (random walk cancellation, no arrow of time)
- **Deconfined phase**: |Q| ~ N (extensive, coherent orientation, arrow of time emerges)
- **Implementation**:
  - `signed_volume_3d()` — gauge-fixed vertex sign sum
  - `measure_signed_volume_3d()` — thermalize + measure with statistics
  - `signed_area_2d()` — 2D analogue for code validation
  - `measure_signed_area_2d()` — 2D measurement routine
- **Production runs completed** (2026-07-02 evening):
  - L=8, 10, 12 with 5000 thermal + 20000 measure sweeps
  - L=8: clearest signal, |Q|/N rises from 0.034 to 0.090 (2.6× increase)
  - L=10: anomalous at β=1.5 (gauge sector issue — stuck in checkerboard)
  - L=12: non-monotonic, fluctuates between sectors
  - **Gauge problem identified**: signed volume flips between ~N and ~0 in deconfined phase
- **Dashboard**: T31 runs and 3 figures added to numerics dashboard
- **Task page**: `tasks/t31-signed-volume.qmd` created and deployed
- **Next**: Implement iterative gauge-fixing, re-run with fixed gauge
- **Files**: `rust-lattice/src/lib.rs` (+241 lines), committed as `84a3fb1`
- **Memory-bank**: T31 task file, implementation-details doc updated with results

### T20d: FSS Analysis Published — COMPLETE ✅
- **T20 Task Page**: Added comprehensive FSS Analysis section
  - 4 figures with captions (FSS Overlay, Critical Exponents, Binder Cumulant, Scaling Collapse)
  - Summary table (This Work vs Literature)
  - Compute details table
  - ToC added for navigation
  - Timestamps updated to 2026-07-02 15:25 IST
- **Dashboard**: Replaced full FSS section with lightweight teaser
  - Links to T20 task page for detailed analysis
  - Keeps dashboard focused on simulation data
- **Key Result**: First-order transition confirmed at β_c = 0.7613(2), Binder U* = 2/3

### Previous Context (2026-06-29)
- L=16 + L=24 fine scans complete
- T22a FK vertex corrected
- Dashboard v2 deployed
- **L=16**: 21 β values [0.740, 0.780], peak χ=1.127 at β=0.752, Binder U=0.6664
- **L=24**: 21 β values [0.740, 0.780], peak χ=1.283 at β=0.756, Binder U=0.6666
- **Data**: `numerics/data/fss/t20d-L16-fine-20260629.json`, `t20d-L24-fine-20260629.json`
- **Plots**: 6 new figures (plaquette, susceptibility, binder, combined)
- **Manuscript**: `t20d-fss-analysis.tex` updated with new tables and β_c(∞)=0.7582±0.0008

### T22a: FK Vertex — CORRECTED ✅
- Original Python estimate was correct (ratio R ≈ 0.45)
- Bug found in TS: (2j+1)^4 instead of (2j+1)^3 in denominator
- Fixed: A_v(j=1/2)=0.250, |A_v|² ratio≈0.20, power law α≈2.0
- ts-quantum-spin-foam package created with tests

### Dashboard Integration — COMPLETE ✅
- Replaced old dashboard with v2 (interactive, filterable)
- Added dashboard links to all task pages (T20, T22, T25)
- Added timestamps to all pages (2026-06-29)
- Deployed: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard.html

### T20 — Status (All Phases Complete — Published 2026-07-02)

| Phase | Status | Key Results |
|-------|--------|-------------|
| T20a | ✅ Complete | 2D Wilson loops, string tension |
| T20b | ✅ Complete | BKT behavior confirmed |
| T20c | ✅ Complete | 3D first-order transition at β≈0.758 |
| T20d | ✅ Complete | FSS analysis published, β_c=0.7613(2) |

**Published:** https://space-cadet.github.io/projects/timesarrow/numerics/tasks/t20-z2-lgt.html

### Critical Finding (2026-06-27)

**3D Z₂ LGT first-order transition CONFIRMED:**
- L=32 plaquette jumps from 0.878 to 0.965 at β≈0.758 (Δβ≈0.001)
- Binder cumulant converges to 2/3 (3D Ising universal value)
- Peak susceptibility χ=1.3704 at β=0.758
- Critical βₑ ≈ 0.758 ± 0.002

**Remaining work (T20d):** 
- L=48/64 fine scans for asymptotic scaling (future work)

---

---

## T22: Spin Foam Amplitudes — IN PROGRESS 🔄

**Strategic decision (2026-06-28): Two-path approach**

### Path 1: Quick Estimate (Recommended)
- **Goal:** Single numerical check: |A_v(j=1)|² / |A_v(j=½)|² with ~10% precision
- **Effort:** 1-2 days
- **Value:** Strengthens manuscript by transforming assumption into supported claim
- **Method:** Monte Carlo over SU(2) for single 4-valent FK vertex
- **Limitations:** Single vertex, one model, simple intertwiners (conservative bound)

### Path 2: Full Systematic Study
- **Goal:** Comprehensive validation across spins, models, γ values
- **Effort:** 1-2 weeks
- **Value:** Research-grade result suitable for standalone publication
- **Method:** Cross-repo implementation (ts-quantum → spin-foam → timesarrow)

**Cross-repo architecture:**
- **ts-quantum core (T14):** SU(2) Haar sampling, Wigner D matrices
- **ts-quantum-spin-foam (T1-T5):** FK/EPRL vertices, MC integrator, coherent states
- **timesarrow (T22):** j=1/2 dominance check and manuscript integration

**Recommendation:** Start with Path 1. If suppression is weak (R > 0.1), upgrade to Path 2.

---

## What's Next (Updated 2026-07-05)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T32/T20d** | **Correct transition-order interpretation and published text** | T20d |
| 2 | **T32/T22a** | **Reclassify group-average toy result and remove squaring error** | T22a |
| 3 | **T32/T31** | **Design and validate a gauge-invariant replacement observable** | T31 |
| 4 | **T32** | **Calibrate T25 wording and restore reproducible builds/tests** | T25, T27 |
| 5 | T29 | Extensible schema design | T32 |
| 6 | T23/T24 | Resume exploratory numerics after correction gate | T32 |

**Key decision:** Correct and verify the post-May numerical claims before further production runs or manuscript integration. T22b and new T31 runs are blocked by T32.
