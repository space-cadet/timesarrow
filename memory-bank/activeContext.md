# timesarrow — Active Context

*Updated: 2026-07-02 15:35 IST*

## Current Session — 2026-07-02 Afternoon

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

### T20 — Status (Updated 2026-06-29)

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
