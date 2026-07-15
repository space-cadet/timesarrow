# timesarrow — Active Context

*Updated: 2026-07-16 03:30 IST*

**T33–T35 quantum-geometric plan created (2026-07-16 03:30 IST):**

- New task files: T33a (cell-complex API), T33b (diamond Polyakov), T34a (snapshot output), T34b (flux loop analysis), T35a (microscopic construction audit)
- Implementation plan: `memory-bank/implementation-details/t33-t35-quantum-geometric-plan.md` with full back-and-forth between Sage, GPT 5.6 Luna, and Deepak Vaid
- Key principle: gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim
- T31 clarification preserved: classical 3D Z₂ transition is control physics, not the paper's novelty

## Current Session — 2026-07-14 Night

### T32: Post-May Numerics Correction and Reproducibility Pass — IN PROGRESS 🔄

- T20d's first-order conclusion is superseded; existing data must be reanalysed using continuous 3D Ising-universality scaling.
- The plaquette Binder value near $2/3$ is not accepted evidence of first-order behavior, and schematic histograms are not numerical evidence.
- T22a is now corrected as a normalized SU(2) four-leg group average, not a complete FK/EPRL vertex amplitude; the extra squaring to $0.20$ is removed in canonical source and regenerated `_site` output.
- T31 must not use greedy gauge alignment because spanning-tree alignment can force $|Q|=N$ in any phase; the Rust source now has a candidate gauge-invariant dressed orientation correlator and gauge-invariance tests, but no new production runs are accepted until those tests run under a Rust 2024-compatible toolchain.
- T25 spectral pairing is now calibrated as algebraic spectral reflection symmetry; the physical time-orientation transformation test is deferred.
- TypeScript/Rust build and test reproducibility are now verified in this checkout via the updated `scripts/validate.sh` workflow, including the Rust 2024-compatible toolchain path.
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

**Deployment audit (2026-07-10 18:40 IST):**

- The local corrected render in `numerics/docs/_site` contains the T20d continuous-transition correction, the T22a four-leg group-average correction, and the T31 gauge-dependence correction.
- The local `space-cadet.github.io` checkout is clean but stale for `projects/timesarrow/numerics/`: deployed `/tasks/` T20, T22, and T31 pages still contain withdrawn first-order, spin-foam dominance, and greedy-gauge language. The dashboard HTML also differs from the corrected `_site` render.
- T32 now explicitly tracks deployment synchronization as an open acceptance criterion.

**Deployment sync (2026-07-10 18:45 IST):**

- Mirrored `numerics/docs/_site/` into `/Users/deepak/code/space-cadet.github.io/projects/timesarrow/numerics/` with stale files removed.
- Committed and pushed the deployment as `92d05cc` on `space-cadet.github.io` `main`.
- T32 deployment synchronization is now complete; remaining blockers are Rust 2024 validation, T20d fine-scan reanalysis, artifact policy, and the manuscript gate.

**Dashboard follow-up (2026-07-10 19:05 IST):**

- Added `assets/**` to `numerics/docs/_quarto.yml` resources so Quarto copies the dashboard gallery figures into `_site/assets/`.
- Normalized dashboard, index, T20, T22, and T31 page timestamps so `date-modified` and visible "Last updated" text agree.
- Corrected the T20 Phase 3b Ising FSS figure paths from the old `../figures/t20d-ising/` location to the published `../assets/` location.
- Added a `Last Updated` column to the main numerics `Simulation Tasks` table.
- Redeployed the refreshed numerics site twice: `21a496e` restored the missing dashboard assets and timestamp refresh, and `efe6780` fixed the T20 Phase 3b figure references plus the main-page task table.

**Validation and rerun calibration (2026-07-10 19:31 IST):**

- Ran the `T31` Rust unit tests successfully using `rustup` toolchain `1.92.0-aarch64-apple-darwin`; the default local `cargo 1.73.0` is too old for edition 2024.
- Confirmed the gauge-invariance tests around `gauge_invariant_signed_volume_3d()` pass in the Rust 2024-compatible environment.
- Measured short `T20d` rerun calibrations: `L=16` at `30k` thermal + `20k` measurement sweeps took about `11.2 s` per β, and `L=32` at `20k` thermal + `10k` measurement sweeps took about `44.8 s` per β.
- Completed a full local `L=8` fine-scan rerun as `numerics/data/fss/t20-p3b-L8-3D-fine-20260710.json` with `25/25` β values.
- Estimated production runtimes for the remaining larger reruns are now roughly: `L=16` about `20–25 minutes` and `L=32` about `2.5–3 hours`; `L=48/64` remain multi-hour jobs.
- The long remaining reruns are being handed off to Kimi.

**Proof-of-principle rerun update (2026-07-14 04:55 IST):**

- Completed fresh production fine scans for `L=16` and `L=32` with the updated runner and recorded the new artifacts under `numerics/data/fss/`.
- `L=16` shows `χ` and `C_V` peaks at `β≈0.752`; `L=32` shifts both peaks to `β≈0.758` and sharpens them further.
- Updated `numerics/src/scripts/t20d-ising-reanalysis.py` now consumes the current fine-scan artifacts and treats the result as proof-of-principle support for the corrected continuous-transition interpretation rather than a precision critical-exponent measurement.
- A simple peak-drift guide now gives `β_c(∞)≈0.7618±0.0005`, close to the literature value `0.761`, but this is recorded as consistency support only.
- Given the current project priorities, `T20d` is now good enough as supporting numerics; the more central volume-operator and related calculations should take precedence over further exponent-chasing.

**T31 provenance salvage (2026-07-15 18:35 IST):**

- Recovered the unpushed 2026-07-14 signed-volume calibration branch onto a clean branch from `origin/main` and kept only the pieces that still fit the current T31 story.
- Preserved additional `L=4`/`L=6` hot-start, cold-start, and multi-seed signed-volume calibration artifacts under `numerics/data/signed-volume/` as negative-result provenance.
- Added `--cold-start` support plus explicit signed-volume kind metadata in the Rust CLI so archived gauge-invariant calibration runs remain self-describing.
- These salvaged artifacts reinforce, rather than weaken, the existing T31 pivot: the dressed signed-volume correlator remains sector-sensitive and should stay provenance-only while Polyakov-loop work remains the active deconfinement path.

## Previous Session — 2026-07-02 Evening

> Superseded on 2026-07-05: the T20d, T22a, and T31 interpretations below are retained as historical session context, not current guidance.

### T31: Signed Volume Observable — PIVOTED to Polyakov Loop (2026-07-14)

**Status:** IN PROGRESS — Polyakov loop proof-of-principle scan complete

**Negative result recorded:** The gauge-invariant dressed correlator `gauge_invariant_signed_volume_3d()` was implemented and validated. It passes gauge-invariance tests and gives Q_GI = 1 for cold-start (all links +1). However, on thermalized configurations:
- L=6: Q_GI ≈ 0.02–0.08 across β = 0.5–0.85 (weak trend, wrong magnitude)
- L=8: Q_GI ≈ 0.01 across all β (flat, no phase discrimination)

**Root cause:** Elitzur's theorem — individual link variables are random ±1 in any thermalized state, so path products are ±1 with equal probability. The triple product `s(r₁)·W·s(r₂)` averages to ~0 regardless of phase.

**Decision:** Abandon signed volume as a deconfinement order parameter. Use the Polyakov loop (already implemented, `--polyakov` flag) as the standard gauge-invariant order parameter.

**Polyakov loop results (2026-07-14):**
- Fixed measurement bug: was averaging |P| (always 1 for Z₂), now correctly averages signed P̄
- Proof-of-principle scans for L=8, 10, 12 across β = 0.60–0.85 (10k thermal + 10k measure sweeps)
- Susceptibility χ_P peaks at β = 0.76 for all L, with growing peak height: 355 (L=8) → 621 (L=10) → 886 (L=12)
- Mean Polyakov loop |⟨P̄⟩| → 1 in ordered phase, ≈ 0 in disordered phase
- Binder cumulant U_P → 0.665 in deep ordered phase (close to 2/3)
- Data saved to `numerics/data/t31-polyakov-proof-of-principle-20260714.json`

**Next steps:**
1. Extract critical exponents from Polyakov loop susceptibility scaling
2. Run longer production scans with better statistics
3. Update T31 task page and manuscript with Polyakov loop results

**Files updated:**
- `rust-lattice/src/lib.rs` — Fixed Polyakov loop measurement (signed average)
- `memory-bank/tasks/T31.md` — Recorded pivot decision and Polyakov loop results
- `memory-bank/implementation-details/signed-volume-observable.md` — Documented Elitzur theorem obstruction
- `memory-bank/activeContext.md` — Updated T31 status
- `numerics/data/t31-polyakov-proof-of-principle-20260714.json` — New data file

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

## What's Next (Updated 2026-07-16)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T33a** | **General 4-valent 3D cell-complex API** | — |
| 2 | **T34a** | **Configuration snapshot output mode** | — |
| 3 | **T33b** | **Diamond lattice Polyakov scan** | T33a |
| 4 | **T34b** | **Flux loop analysis** | T34a |
| 5 | **T35a** | **Microscopic construction audit** | T33a |
| 6 | T32 | Verify reproducible builds/tests with Rust 2024 toolchain | T25, T27 |
| 7 | T29 | Extensible schema design | T32 |
| 8 | T23/T24 | Resume exploratory numerics after correction gate | T32 |

**Key decision:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.
