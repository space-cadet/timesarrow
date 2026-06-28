# timesarrow — Active Context

*Updated: 2026-06-27 21:15 IST*

## Current Session — 2026-06-27 Evening

### T28a: Dashboard v2 — FUNCTIONAL ✅ COMPLETE

**What was built:**
- Full vanilla JS dashboard with 3 tabs: Runs & Results, Figure Archive, Performance
- 14 runs loaded from external JSON (with GitHub raw fallback for immediate availability)
- Filterable, sortable runs table with row selection and detail panel
- Detail panel: Parameters, Results, Key Findings, Timing, Export (JSON/CSV)
- 6 FSS figures with thumbnails, click-to-zoom modal, orthogonal filters
- Performance chart: SVG log-log scatter plot (Wall time vs Lattice Size)
- Dark mode via `prefers-color-scheme`, mobile responsive

**Deployment:**
- URL: https://space-cadet.github.io/projects/timesarrow/numerics/dashboard-v2.html
- Repo: space-cadet.github.io (GitHub Pages)
- Commit: `db2bfef`

**Architecture decisions:**
- External JSON files instead of inline data (235KB blob caused syntax errors)
- GitHub raw fallback for data files (GitHub Pages cache delay ~5min)
- Vanilla JS over React: faster iteration, no build step, sufficient for current features

### T20d: L=32 Simulation — COMPLETE ✅
- **Run ID:** `t20-p3b-L32-lean-20260627`
- **Status:** Complete, data committed to `numerics/data/fss/`
- **Results:** Peak χ=1.3704 at β=0.758, Peak C=1.0388 at β=0.758, Binder U≈0.666
- **Plaquette:** First-order jump from ~0.88 to ~0.96 at β≈0.758
- **Wall time:** ~6h total (distributed across 8 workers)

### T30: Unified Plotting Module — IN PROGRESS 🔄
- **Status:** Phase 1 complete (core module created)
- **Module:** `numerics/src/plotting.py` — shared infrastructure for all plotting scripts
- **Features:** Auto-detected paths, unified color palette (colorblind-friendly), standardized data loading, consistent figure output, annotation helpers
- **Smoke test:** ✅ Passed (loaded L=32 run, 21 β values, χ_max=1.3704)
- **Next:** Phase 2 — refactor existing scripts to use the module

### T29: Extensible Schema Design — PENDING ⬜
- Status: Pending, not started
- Goal: Physics-agnostic base schema + extension namespaces for any simulation domain
- Key idea: `extensions: { lgt: {...}, dmrg: {...} }` in base schema
- See: `memory-bank/implementation/extensible-schema-design.md`

---

## T20 — Status (Updated 2026-06-27)

| Phase | Description | Data Status | Analysis Status | Key Missing |
|-------|-------------|-------------|-----------------|-------------|
| T20a | 2D square, L=16 | ✅ Data collected | ✅ Wilson loops complete | Critical exponents |
| T20b | 2D finite-size scaling | ✅ Data collected | 🔄 Missing analysis | Scaling collapse, Binder crossing, ξ |
| T20c | 3D cubic lattice | ✅ Data collected | ✅ Wilson loops & string tension complete | Critical exponents |
| T20d | FSS critical exponent extraction | ✅ L=8,16,32 complete | 🔄 Scripts ready | L=48,64; FSS plots; exponent fitting |

### Critical Finding (2026-06-27)

**3D Z₂ LGT first-order transition CONFIRMED:**
- L=32 plaquette jumps from 0.878 to 0.965 at β≈0.758 (Δβ≈0.001)
- Binder cumulant converges to 2/3 (3D Ising universal value)
- Peak susceptibility χ=1.3704 at β=0.758
- Critical βₑ ≈ 0.758 ± 0.002

**Remaining work:** 
- Generate FSS comparison plots (L=8,16,32 overlay)
- Extract critical exponents (ν, γ, α) from scaling
- Start L=48/64 if needed for thermodynamic limit

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

## What's Next (Updated 2026-06-28)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T22-P1** | **Quick estimate: FK vertex j=1/2 vs j=1** | — |
| 2 | **T14** | **Implement SU(2) Haar + representation in ts-quantum** | — |
| 3 | **T20d** | **Generate FSS plots (L=8,16,32 overlay)** | L=32 completion |
| 4 | T20d | Critical exponent fitting (ν, γ, β, α) | FSS plots |
| 5 | T30 | Refactor scripts to use unified plotting module | Phase 1 complete |
| 6 | T29 | Extensible schema design | — |
| 7 | T23 | Entanglement entropy — needs T22 completion | T22 |

**Key decision:** T20d is substantially complete (first-order transition confirmed, Binder cumulant converged). T22 is now the highest-priority active task because it addresses the manuscript's deepest theoretical gap.

---

## What's Next (Previous — 2026-06-27)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T20d** | **Generate FSS plots (L=8,16,32 overlay)** | L=32 completion |
| 2 | **T20d** | **Critical exponent fitting (ν, γ, β, α)** | FSS plots |
| 3 | **T30** | **Refactor scripts to use unified plotting module** | Phase 1 complete |
| 4 | T29 | Extensible schema design | — |
| 5 | T20d | Start L=48/64 if needed for better extrapolation | L=32 analysis |
| 6 | T20b | Scaling collapse plots (existing 2D data) | — |
| 7 | T22 | Spin Foam Amplitudes — single vertex computation | T20 |
| 8 | T23 | Entanglement entropy — needs T22 completion | T22 |

**Key decision:** T28a complete. T20d L=32 complete. T30 Phase 1 (plotting module) complete. Next priority is T20d FSS analysis, then T30 Phase 2 (script refactoring) or T29 schema work when user prioritizes it.
