# timesarrow — Active Context

*Updated: 2026-07-08 17:42 IST*

## Current Session — 2026-07-08 Night

### T32: Post-May Numerics Correction and Reproducibility Pass — IN PROGRESS 🔄

- T20d's first-order conclusion is superseded; existing data must be reanalysed using continuous 3D Ising-universality scaling.
- The plaquette Binder value near $2/3$ is not accepted evidence of first-order behavior, and schematic histograms are not numerical evidence.
- T22a is now corrected as a normalized SU(2) four-leg group average, not a complete FK/EPRL vertex amplitude; the extra squaring to $0.20$ is removed in canonical source and regenerated `_site` output.
- T31 must not use greedy gauge alignment because spanning-tree alignment can force $|Q|=N$ in any phase; the Rust source now has a candidate gauge-invariant dressed orientation correlator and gauge-invariance tests, but no new production runs are accepted until those tests run under a Rust 2024-compatible toolchain.
- T25 spectral pairing is now calibrated as algebraic spectral reflection symmetry; the physical time-orientation transformation test is deferred.
- TypeScript/Rust build and test reproducibility are documented but not verified in the current shell because local Cargo cannot parse Rust edition 2024.
- `timesarrow.tex` remains gated from post-May numerical claims until T32 is complete.
- The correction plan now includes an explicit error inventory, not only a task list, covering T20d, T22a, T31, T25, reproducibility, and the manuscript gate.

**T20d correction progress (2026-07-05 23:12 IST):**

- Rewrote `t20d-fss-analysis.tex` around continuous 3D Ising universality.
- Corrected and rebuilt the canonical T20 Quarto task page and both tracked HTML outputs.
- Removed the first-order, latent-heat, synthetic-histogram, and failed-collapse claims from rendered publication text.
- Preserved raw data; numerical reanalysis, dashboard correction, and figure retirement/replacement remain open.

**Plan:** `implementation-details/post-may-numerics-correction-plan.md`

**Memory-bank update (2026-07-08 00:54 IST):**

- Expanded the plan with a forensic inventory of the identified post-May errors.
- Preserved the existing correction workstreams and T32 gate; no new task or implementation file was created beyond the required edit chunk.

**Docs/memory synchronization (2026-07-08 17:42 IST):**

- Updated the correction plan's error inventory with resolved-vs-remaining status for T20d, T22a, T31, T25, reproducibility, and the manuscript gate.
- Cleaned the dashboard source so superseded first-order T20 figures are omitted instead of duplicated under unmarked titles.
- Updated the T31 task page to mark old $|Q|/N$ data as exploratory, withdraw greedy gauge fixing, and document the candidate gauge-invariant dressed correlator.
- Rebuilt the Quarto site into `_site`; root-level rendered HTML artifacts were removed by the current `output-dir: _site` configuration.

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
- **Superseded next step**: The earlier plan to implement iterative gauge fixing is withdrawn by T32; new production runs require the gauge-invariant dressed correlator to pass validation.
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

### T22a: SU(2) Four-Leg Group Average — CORRECTED ✅
- Supersedes the older FK-vertex framing retained in pre-T32 history.
- Correct current interpretation: normalized SU(2) four-leg group average with $G(1)/G(1/2)=4/9 \approx 0.444$.
- The extra squaring to approximately $0.20$ was an error; the result does not establish physical $j=1/2$ dominance.
- Superseded `t22a-fk-vertex-*` scripts are retained only as provenance.

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
| 2 | **T32/T31** | **Run and validate the gauge-invariant replacement observable** | T31 |
| 3 | **T32/T20d** | **Finish controlled reanalysis and artifact cleanup** | T20d |
| 4 | **T32** | **Verify reproducible builds/tests with Rust 2024 toolchain** | T25, T27 |
| 5 | T29 | Extensible schema design | T32 |
| 6 | T23/T24 | Resume exploratory numerics after correction gate | T32 |

**Key decision:** Correct and verify the post-May numerical claims before further production runs or manuscript integration. T22b and new T31 runs are blocked by T32.
