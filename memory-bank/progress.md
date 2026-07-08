# timesarrow — Progress Tracker

*Updated: 2026-07-08 17:42 IST*

## T32 Correction Gate

**Status:** 🔄 In progress

The post-May simulation infrastructure and raw datasets are preserved, but the following interpretations are superseded pending correction:

- T20d: first-order classification, plaquette-Binder argument, and schematic histogram evidence.
- T22a: FK-vertex labeling and the extra squaring from approximately $0.45$ to $0.20$. **Resolved in canonical source and regenerated `_site` output (2026-07-08): now a normalized SU(2) four-leg group average with analytic result primary.**
- T31: iterative gauge alignment and phase-scaling claims based on the gauge-dependent path sum. **Partially resolved (2026-07-08): old runs are exploratory and greedy gauge fixing is withdrawn; Rust source contains a candidate gauge-invariant dressed correlator and tests, but production validation remains pending.**
- T25: spectral $± q$ pairing overinterpreted as a physical time-orientation symmetry without an explicit transformation operator. **Calibrated under T32 (2026-07-08): now described as algebraic spectral reflection symmetry with physical-transformation test deferred.**

TypeScript and Rust build/test reproducibility and repository artifact policy are also part of T32. Post-May numerical claims are blocked from the main manuscript until T32 is complete.

### T32 Error Inventory — 2026-07-08

- ✅ `post-may-numerics-correction-plan.md` now records a dedicated identified-error inventory.
- ✅ The inventory separates the actual errors from the correction workstreams.
- ✅ The inventory now records resolved-vs-remaining status for each error class.
- ✅ Dashboard source no longer duplicates superseded T20 first-order figures under unmarked titles.
- ✅ T31 docs now mark old signed-volume runs as gauge-dependent exploratory data and document the replacement observable.
- 🔄 T20d numerical reanalysis, Rust 2024-compatible validation, new T31 production runs, and artifact-policy cleanup remain pending under T32.

### T20d Correction Progress — 2026-07-05

- ✅ Standalone annexure rewritten around the continuous 3D Ising-universality transition.
- ✅ Canonical Quarto task page corrected and rebuilt successfully.
- ✅ Unsupported first-order, latent-heat, schematic-histogram, and failed-collapse conclusions removed from rendered text.
- 🔄 Autocorrelation-aware numerical reanalysis remains pending.
- ✅ Dashboard source correction completed; stale first-order entries removed from the active source.
- 🔄 Misleading figure artifact policy and controlled reanalysis remain pending.

> Sections below preserve the 2026-07-02 progress snapshot and may contain claims superseded by T32.

## Active Tasks

### T20: Z₂ Lattice Gauge Theory — Phase 3 (3D) + Phase 3b (FSS)

| Sub-task | Status | Completion |
|----------|--------|------------|
| T20a (2D, L=16) | ✅ Complete | Wilson loops, string tension |
| T20b (2D FSS) | ✅ Complete | Data collected, analysis pending |
| T20c (3D, L=8-24) | ✅ Complete | Wilson loops, string tension, first-order analysis |
| T20d (3D FSS, fine β) | ✅ Complete | L=8,16,24,32 done; FSS plots + manuscript updated |
| L=48/64 | ⏳ Pending | Future work for asymptotic scaling |

**T20d Progress (Complete — Published 2026-07-02):**
- L=8: ✅ 25 β values, 0.70–0.82, Δβ=0.005, 1M sweeps
- L=16: ✅ 21 β values, 0.740–0.780, Δβ=0.002, 500k sweeps (300k therm + 200k measure), 4 workers, ~58 min wall
- L=24: ✅ 21 β values, 0.740–0.780, Δβ=0.002, 500k sweeps, 4 workers, ~107 min wall
- L=32: ✅ 21 β values, 0.74–0.78, Δβ=0.002, 500k sweeps, 8 workers, ~6h wall
- L=48: ⏳ Pending (β=0.75–0.77, Δβ=0.0015, 2M sweeps)
- L=64: ⏳ Pending (β=0.75–0.77, Δβ=0.001, 3M sweeps)
- FSS Analysis: ✅ Published to T20 task page with 4 figures, summary table, ToC
- Dashboard: ✅ Updated with teaser linking to full analysis

**T20 Historical Snapshot (superseded by T32):**
- β_c (3D) ≈ 0.758 ± 0.002 — from Binder cumulant crossing (L=8,16,24,32)
- First-order transition was previously claimed from the plaquette jump near β≈0.758; this interpretation is superseded by T32 and must not be used as current guidance.
- Binder cumulant U → 0.666 (3D Ising universal value 2/3) as L increases
- Peak susceptibility χ_max grows with L: 0.87 (L=8) → 1.13 (L=16) → 1.28 (L=24) → 1.37 (L=32)
- Peak specific heat C_max grows with L: 0.65 (L=8) → 0.85 (L=16) → 0.97 (L=24) → 1.04 (L=32)
- χ_max/L³ scaling: 1.70×10⁻³ (L=8) → 2.75×10⁻⁴ (L=16) → 9.29×10⁻⁵ (L=24) → 4.19×10⁻⁵ (L=32)
- β_c(L) shift: β_c(∞)=0.7582±0.0008 from the old first-order fit; retained only as historical provenance.
- String tension σ vanishes at β_c
- Results match Creutz et al. (1979) within error

### T22a: SU(2) Four-Leg Group Average — CORRECTED ✅

**Status:** Complete — reclassified under T32 on 2026-07-08

**Key Finding:** The calculation is a normalized SU(2) four-leg group average, not a complete FK/EPRL spin-foam vertex amplitude.

**Corrected Results:**
- $G(j=1/2) = 1/4 = 0.25$
- $G(j=1) = 1/9 \approx 0.111$
- $G(1)/G(1/2) = 4/9 \approx 0.444$
- The extra squaring to approximately $0.20$ was an error and is removed from current guidance.
- **Conclusion:** This is a useful toy normalization/code-check result, but it does not establish $j=1/2$ dominance in a physical spin-foam model.

**Implementation:**
- Corrected scripts: `numerics/scripts/su2-four-leg-group-average*.py`
- Superseded provenance scripts: `numerics/scripts/t22a-fk-vertex*.py`

**Files:** `memory-bank/tasks/T22a.md`, `numerics/docs/tasks/t22-spin-foam.qmd`, `numerics/scripts/su2-four-leg-group-average.py`

### T28a: Simulation Dashboard v2 (Functional)

| Feature | Status | Notes |
|---------|--------|-------|
| Runs & Results | ✅ Complete | Filterable, sortable, selectable, detail panel, export |
| Figure Archive | ✅ Complete | 6 FSS figures, thumbnails, click-to-zoom, orthogonal filters |
| Performance Chart | ✅ Complete | SVG log-log scatter plot, color by dimension |
| Data Export | ✅ Complete | JSON + CSV for selected run |
| Dark Mode | ✅ Complete | `prefers-color-scheme` media query |
| Mobile Responsive | ✅ Complete | CSS grid + flexbox, breakpoints |
| External Data | ✅ Complete | `fetch()` from JSON files, GitHub raw fallback |

**Architecture:**
- Vanilla JS, single HTML file, zero build step, zero dependencies
- External JSON data: `dashboard-data.json` (33 runs metadata), `dashboard-figures.json` (6 figures)
- GitHub raw fallback for immediate availability (avoids GitHub Pages cache delay)
- Abandoned OJS/Quarto approach (fragile runtime loading, cells rendered as raw code)
- Abandoned 235KB inline JSON blob (syntax errors, blank page)

**Deployment:**
- URL: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard-v2.html
- Commit: `db2bfef` (space-cadet.github.io)

### T29: Extensible Schema Design

| Phase | Status | Notes |
|-------|--------|-------|
| Design spec | ✅ Complete | `extensible-schema-design.md` written |
| Base schema | ⏳ Pending | `base-registry.schema.json` not yet created |
| Extension registry | ⏳ Pending | `lgt.schema.json`, `dmrg.schema.json` not yet created |
| Migration script | ⏳ Pending | v1.0 → v2.0 converter not yet written |
| Dashboard v3 | ⏳ Pending | Schema-driven UI not yet started |

### T31: Signed Volume Observable — IN PROGRESS 🔄

**Status:** Original implementation complete; old measurements are exploratory because of gauge dependence. T32 has specified a candidate gauge-invariant dressed correlator in Rust, but production validation remains pending.

**Concept:** Use signed volume operator Q̂ (not positive-definite V̂) for composite systems. Emergence of global time orientation ↔ emergence of macroscopic signed volume.

**Implementation:**
- `signed_volume_3d()` — gauge-fixed vertex sign sum
- `measure_signed_volume_3d()` — thermalize + measure with statistics
- `signed_area_2d()` — 2D analogue for code validation
- `--signed-volume` CLI flag added

**Results (superseded exploratory data):**
- 2D (L=8): |Q|/N ≈ 0.08–0.11 across all β (consistent with 1/√N, no deconfined phase)
- 3D (L=6): |Q|/N grows from ~0.02 (β=0.4) to ~0.29 (β=1.5), transition region β ≈ 0.8–1.0
- 3D (L=8,10,12): Simulations complete, data in registry

**Issue Identified:** Gauge dependence. Greedy or iterative alignment is withdrawn because it can force $|Q|=N$ in any phase. New production runs must use a validated gauge-invariant replacement observable.

**Files:** `rust-lattice/src/lib.rs` (+241 lines), `docs/tasks/t31-signed-volume.qmd`

---

## Blockers

1. **T31**: Candidate gauge-invariant dressed correlator needs Rust 2024-compatible test execution, physical review, and new production runs.
2. **T20d**: Controlled continuous-transition reanalysis remains pending.
3. **T29**: None — can start when user prioritizes

---

## Recent Commits

### timesarrow repo
- `0db8bcf` — T20d: L=32 simulation complete, data committed
- `7f4f77a` — fix(dashboard): Observable Plot instead of Vega-Lite
- `6fb8f5e` — fix(dashboard): word wrap for key finding
- `e4a0b15` — feat(dashboard): Plot Gallery + Run Detail Browser
- `b2c5d39` — fix(dashboard): Results card formatting
- `e9d57f7` — fix(dashboard): named function for formatValue

### space-cadet.github.io repo
- `db2bfef` — Dashboard v2: add GitHub raw fallback for data loading
- `43587fe` — Dashboard v2: clean rewrite with external JSON loading
- `0457c05` — Dashboard v2 initial deployment with inline data fix
