# Memory Bank - timesarrow

*Created: 2026-06-26*
*Last Updated: 2026-06-27 10:20:00 IST*

## Overview
Memory bank for the timesarrow project — Z₂ lattice gauge theory simulations and related numerics.

## Active Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T20 | Z₂ Lattice Gauge Theory Monte Carlo | 🔄 | HIGH | 2026-06-24 | T25, T27 | [Details](tasks/T20.md) |
| T20b | Phase 2 — Sharp Phase Transition / Multi-Lattice FSS | 🔄 | HIGH | 2026-06-25 | T20a | [Details](tasks/T20b.md) |
| T20c | Phase 3 — 3D Cubic Lattice | 🔄 | HIGH | 2026-06-25 | T20a | [Details](tasks/T20c.md) |
| T20d | Critical Exponent Extraction from 3D Z₂ LGT | 🔄 | MEDIUM | 2026-06-26 | — | [Details](tasks/T20d.md) |
| T21a | Performance Optimization — Fast Monte Carlo Kernel | 🔄 | MEDIUM | 2026-06-25 | T20b | [Details](tasks/T21a.md) |
| T22 | Spin Foam Amplitudes | 🔄 | MEDIUM | 2026-06-25 | T20c | [Details](tasks/T22.md) |
| T23 | Entanglement Structure of the Deconfined Phase | 🔄 | MEDIUM | 2026-06-24 | T20 | [Details](tasks/T23.md) |
| T24 | Domain Wall Dynamics and Surface Topological Order | 🔄 | MEDIUM | 2026-06-24 | T20, T21 | [Details](tasks/T24.md) |
| T26 | Coupled Spin Network + Matter Field Simulation | 🔄 | LOW | — | T20 | [Details](tasks/T26.md) |
| T28 | Simulation Dashboard | 🔄 | MEDIUM | 2026-06-26 | — | [Details](tasks/T28.md) |

## Completed Tasks

| ID | Title | Priority | Started | Completed | Details |
|----|-------|----------|---------|-----------|---------|
| T1 | Initial Memory Bank Population | HIGH | 2026-04-16 | — | [Details](tasks/T1.md) |
| T2 | Analyze Manuscript Gaps | MEDIUM | 2026-04-16 | — | [Details](tasks/T2.md) |
| T3 | Rewrite z2-action-derivation.tex | HIGH | 2026-04-16 | — | [Details](tasks/T3.md) |
| T4 | Rewrite spt-lqg-mapping.tex | HIGH | 2026-04-16 | — | [Details](tasks/T4.md) |
| T5 | Update Title and Abstract | HIGH | 2026-04-16 | — | [Details](tasks/T5.md) |
| T6 | Revise Discussion Section | MEDIUM | 2026-04-16 | — | [Details](tasks/T6.md) |
| T7 | Trim MPS Pedagogy and Appendices | MEDIUM | 2026-04-16 | — | [Details](tasks/T7.md) |
| T8 | Fix Typos and Cleanup | LOW | 2026-04-17 | — | [Details](tasks/T8.md) |
| T9 | Create Missing Figure — 2D TNS Matrix Insertion | MEDIUM | 2026-04-17 | — | [Details](tasks/T9.md) |
| T10 | Fix 17 Bibliography Metadata Errors | MEDIUM | — | — | [Details](tasks/T10.md) |
| T11 | Fix Critical Manuscript Errors | HIGH | — | — | [Details](tasks/T11.md) |
| T12 | Address Major Issues and Add Recent Citations | HIGH | — | — | [Details](tasks/T12.md) |
| T13 | Create Accessible Web Presentation (Time's Arrow) | MEDIUM | 2026-04-18 | — | [Details](tasks/T13.md) |
| T14 | Minimal Web Presentation | MEDIUM | 2026-04-18 | — | [Details](tasks/T14.md) |
| T15 | 3D SPT Survey and Mapping | HIGH | 2026-04-20 | — | [Details](tasks/T15.md) |
| T16 | Submission Documentation | HIGH | 2026-04-29 | — | [Details](tasks/T16.md) |
| T17 | arXiv Submission Preparation | HIGH | 2026-05-05 | — | [Details](tasks/T17.md) |
| T18 | Manuscript Claim-Hardening and Reviewer-Response Roadmap | HIGH | 2026-05-06 | — | [Details](tasks/T18.md) |
| T19 | Markdown-First Z2 Section Pilot | MEDIUM | 2026-05-09 | — | [Details](tasks/T19.md) |
| T20a | Phase 1 — 2D Square Lattice | HIGH | 2026-06-24 | 2026-06-24 | [Details](tasks/T20a.md) |
| T21 | Worker Threads + Checkpointing | MEDIUM | 2026-06-25 | 2026-06-25 | [Details](tasks/T21.md) |
| T25 | Volume Operator Eigenvalues | MEDIUM | 2026-06-24 | 2026-06-24 | [Details](tasks/T25.md) |
| T27 | Rust Z₂ LGT Framework | MEDIUM | 2026-06-25 | 2026-06-25 | [Details](tasks/T27.md) |
| T28 | Simulation Dashboard | MEDIUM | 2026-06-26 | 2026-06-26 | [Details](tasks/T28.md) |

## Task Relationships

```
T20: Z₂ Lattice Gauge Theory Monte Carlo
├── T20a: Phase 1 — 2D Square Lattice ✅
├── T20b: Phase 2 — Sharp Phase Transition / FSS 🔄
├── T20c: Phase 3 — 3D Cubic Lattice 🔄
└── T20d: Critical Exponent Extraction 🔄

T21: Worker Threads + Checkpointing ✅
└── T21a: Performance Optimization 🔄

T22: Spin Foam Amplitudes 🔄
  └── T20c

T23: Entanglement Structure 🔄
  └── T20

T24: Domain Wall Dynamics 🔄
  └── T20, T21

T26: Coupled Matter Field 🔄
  └── T20
```

## Status Summary

- **Active**: 9
- **Completed**: 25
- **Paused**: 0
- **Total**: 34
