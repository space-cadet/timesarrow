# timesarrow — Progress Tracker

*Updated: 2026-07-21 14:56:49 IST*

## T35b: Diamond-Lattice CZX Existence Test (2026-07-21) — EDGE-QUBIT MODEL BLOCKED

**Status:** Gate 1 complete. **Edge-qubit model fails for L≥3.** Need to reconsider qubit placement (vertex-qubits instead of edge-qubits).

### Gate 1 Results: Four-Valent Square-Lattice Test

**L=2 (Dense exact diagonalization):**
- Hilbert space: 8 edge-qubits, dim = 256
- Ground state energy: E₀ ≈ 1.2×10⁻¹² ≈ 0 ✅
- Intertwiner subspace dimension: 1
- <ψ|U_X|ψ> = +1.000000 ✅
- <ψ|U_CZ|ψ> = +1.000000 ✅
- First excited state: E₁ ≈ 2.20, gap ΔE ≈ 2.20

**L=3 (Power iteration, converged):**
- Hilbert space: 18 edge-qubits, dim = 262,144
- Ground state energy: E₀ ≈ 3.684 (converged, stable)
- **No exact intertwiner subspace exists** ❌

**Critical Finding:** The edge-qubit model is incompatible with simultaneous singlet constraints at all vertices for L≥3. For L=2: 4 vertices → intersection is 1-dim. For L=3: 9 vertices → intersection is EMPTY (best approximation has ~3.68 unsatisfied vertices).

### Hamiltonian Bug Fixed
Initial implementations computed `H = I - ΣPᵥ` instead of `H = Nᵥ·I - ΣPᵥ`. Correct: `H = Σᵥ(I - Pᵥ) = Nᵥ·I - Σᵥ Pᵥ`.

### Code
- `rust-lattice/src/t35b_gate1.rs` — dense (L=2) + Lanczos (L=3)
- `rust-lattice/src/t35b_power.rs` — power iteration for L=3
- `rust-lattice/src/t35b_verify.rs` — L=2 dense verification

### Next Steps
- [ ] Reconsider qubit placement: vertex-qubits (T35a-style) vs edge-qubits vs vertex-hexagon incidence
- [ ] Design new Gate 1 test with vertex-qubit placement
- [ ] Document this negative result and pivot direction

---

## T35a: CZX Microscopic Construction — Milestone Reached (2026-07-19)

**Status:** Many-body construction complete — single plaquette, open plaquette boundary, 2×2 torus (16 qubits).

**Verified:**
- Single plaquette: $|\Psi\rangle = (|0000\rangle + |1111\rangle)/\sqrt2$ is exact +1 eigenvector of $U_{CZX} = X^{\otimes 4} \prod CZ$
- Open plaquette: boundary signature with relative sign ($\langle\Psi|U|\Psi\rangle = 0$)
- 2×2 torus: global $\prod_s U_{CZX,s}$ preserves state; single-site $U_{CZX,s}$ maps to orthogonal state
- CZ cancellation on shared links is the mechanism

**Code:** `numerics/scripts/t35a-czx-construction-verify.py` (numpy exact state-vector).

**Open threads:** boundary MPUO / 3-cocycle computation, parent Hamiltonian, ts-quantum cross-check, 3D generalization to diamond lattice.

---

## T33–T35: Quantum-Geometric Numerics — NEW 🔄

**Status:** Created 2026-07-16

**Tasks:**
- T33a: General 4-valent 3D cell-complex API (🔄 IN PROGRESS)
- T33b: Diamond lattice Polyakov scan (⏳ PENDING, depends on T33a)
- T34a: Configuration snapshot output mode (⏳ PENDING)
- T34b: Flux loop analysis (⏳ PENDING, depends on T34a)
- T35a: Microscopic construction audit (🔄 IN PROGRESS; local audit complete)

**Plan:** `memory-bank/implementation-details/t33-t35-quantum-geometric-plan.md`

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

**2026-07-18 documentation restoration:** T33a's module docs restored with physics rationale, CSR field comments, boundary-operator notation, and orientation note. Benchmarked BTreeSet matmul: 2.8× faster than dense-buffer at 512×1024 (L≥3 diamond). Terra's valid improvements (try_new, Eq derives, idiomatic style) preserved. 45 tests pass.

**Blockers:** T33b still requires general-complex gauge integration after T33a. T35a requires a candidate many-vertex state and its symmetry action; T34a remains independent.

---

## T32 Correction Gate

**Status:** 🔄 In progress

The post-May simulation infrastructure and raw datasets are preserved, but the following interpretations are superseded pending correction:

- T20d: first-order classification, plaquette-Binder argument, and schematic histogram evidence.
- T22a: FK-vertex labeling and the extra squaring from approximately $0.45$ to $0.20$. **Resolved in canonical source and regenerated `_site` output (2026-07-08): now a normalized SU(2) four-leg group average with analytic result primary.**
- T31: iterative gauge alignment and phase-scaling claims based on the gauge-dependent path sum. **Further resolved (2026-07-15): the project has pivoted to the Polyakov loop, and additional archived hot/cold calibration artifacts now strengthen the negative result for the dressed signed-volume correlator rather than reopening it as an active production observable.**
- T25: spectral $± q$ pairing overinterpreted as a physical time-orientation symmetry without an explicit transformation operator. **Calibrated under T32 (2026-07-08): now described as algebraic spectral reflection symmetry with physical-transformation test deferred.**

TypeScript and Rust build/test reproducibility and repository artifact policy are also part of T32. The local validation workflow now passes in this checkout. Post-May numerical claims are blocked from the main manuscript until T32 is complete.

### T32 Error Inventory — 2026-07-08

- ✅ `post-may-numerics-correction-plan.md` now records a dedicated identified-error inventory.
- ✅ The inventory separates the actual errors from the correction workstreams.
- ✅ The inventory now records resolved-vs-remaining status for each error class.
- ✅ Dashboard source no longer duplicates superseded T20 first-order figures under unmarked titles.
- ✅ T31 docs now mark old signed-volume runs as gauge-dependent exploratory data and document the replacement observable.
- 🔄 T20d proof-of-principle reanalysis is now in place, while T31 production runs and artifact-policy cleanup remain pending under T32.

### T20d Proof-of-Principle Update — 2026-07-14

- Fresh `L=16` and `L=32` production reruns have now completed and are saved under `numerics/data/fss/`.
- The updated `L=16` rerun peaks at `β≈0.752`; the updated `L=32` rerun peaks at `β≈0.758`.
- Peak heights sharpen with lattice size, and the simple peak-drift guide lands near `β_c(∞)≈0.7618±0.0005`, close to the literature value `0.761`.
- Binder remains close to `2/3`, so this is still not a dramatic cumulant story.
- Current conclusion: `T20d` is now sufficient as proof-of-principle support for the corrected continuous-transition interpretation, but not as a precision critical-exponent result.
- Recommendation: treat further `L=48/64` runs and autocorrelation-aware exponent work as optional follow-ons, and move priority back to the more central volume-operator and related calculations.

### T20d Rerun Calibration — 2026-07-10

- Short timing calibrations were completed before launching the new fine-scan campaign.
- Measured today on this machine: `L=16` at `30k` thermal + `20k` measurement sweeps took about `11.2 s` per β; `L=32` at `20k` thermal + `10k` measurement sweeps took about `44.8 s` per β.
- A full new `L=8` fine-scan rerun completed locally as `numerics/data/fss/t20-p3b-L8-3D-fine-20260710.json` with `25/25` β values.
- Extrapolated wall-clock estimates for the remaining production settings are: `L=16` about `20–25 minutes`, `L=32` about `2.5–3 hours`, with `L=48/64` substantially longer.
- The large remaining T20d reruns are being handed off to Kimi after this calibration pass.

### T32 Deployment Audit — 2026-07-10

- Local corrected Quarto output in `numerics/docs/_site` includes the T20d continuous-transition correction, the T22a SU(2) four-leg group-average correction, and the T31 gauge-dependence correction.
- The local `space-cadet.github.io` checkout is clean at commit `bf552ea`, but `projects/timesarrow/numerics/` is stale relative to `_site`.
- Deployed `/tasks/` T20, T22, and T31 pages still contain withdrawn first-order, spin-foam dominance, and greedy-gauge language.
- The deployed dashboard HTML differs from the corrected `_site` render; an older project-local deployment copy also still lists superseded first-order dashboard figure entries.
- Deployment synchronization is now an explicit T32 acceptance criterion before the manuscript gate can close.

### T32 Deployment Sync — 2026-07-10

- Corrected `numerics/docs/_site/` output was mirrored into `/Users/deepak/code/space-cadet.github.io/projects/timesarrow/numerics/`.
- Stale deploy-only files and old first-order figure artifacts were removed from the published numerics subtree.
- Deployment commit `92d05cc` (`docs: deploy corrected timesarrow numerics`) was pushed to `space-cadet.github.io` `main`.
- T32 deployment synchronization is now complete; Rust validation, T20d fine-scan reanalysis, artifact policy, and the manuscript gate remain open.

### T32 Dashboard Repair — 2026-07-10

- Dashboard gallery figures were missing because the page referenced dynamically constructed asset paths that Quarto was not copying into `_site`.
- `numerics/docs/_quarto.yml` now includes `assets/**` as project resources, so the rendered site carries the full figure set.
- T20 Phase 3b Ising FSS figures now point at published `../assets/` files instead of the obsolete `../figures/t20d-ising/` path.
- The main numerics overview page now includes a `Last Updated` column in the `Simulation Tasks` table.
- Follow-up deploy commits `21a496e` and `efe6780` pushed the repaired render to `space-cadet.github.io`.

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
