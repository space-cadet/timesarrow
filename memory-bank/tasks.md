# Memory Bank - Sage Workspace

*Created: 2026-07-08 10:19:36 IST*
*Last Updated: 2026-07-10 19:05:00 IST*

## Overview

This is the Memory Bank for the Sage (灵剑) OpenClaw workspace.

## Active Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T20d | Critical Exponent Extraction from 3D Z₂ LGT | 🔄 | MEDIUM | 2026-06-26 | T32 | [Details](tasks/T20d.md) |
| T23 | Entanglement Structure | 🔄 | HIGH | 2026-06-24 | T20 | [Details](tasks/T23.md) |
| T24 | Domain Wall Dynamics | 🔄 | HIGH | 2026-06-24 | T20, T21 | [Details](tasks/T24.md) |
| T31 | Signed Volume Observable | 🔄 | MEDIUM | 2026-07-02 | — | [Details](tasks/T31.md) |
| T32 | Post-May Numerics Correction and Reproducibility Pass | 🔄 | HIGH | 2026-07-05 | T20d, T22a, T25, T27, T31 | [Details](tasks/T32.md) |

## Completed Tasks

| ID | Title | Status | Priority | Started | Completed | Dependencies | Details |
|----|-------|--------|----------|---------|-----------|--------------|---------|
| T14 | SU(2) Haar + Representation (ts-quantum core) | ✅ | HIGH | 2026-06-28 | 2026-06-28 | 2026-06-28 | [Details](tasks/T14.md) |
| T15 | Spin Foam Package (ts-quantum-spin-foam) | ✅ | HIGH | 2026-06-28 | 2026-06-28 | 2026-06-28 | [Details](tasks/T15.md) |
| T20 | Z₂ Lattice Gauge Theory Monte Carlo | ✅ | HIGH | 2026-06-24 | 2026-06-24 | 2026-06-24 | [Details](tasks/T20.md) |
| T20a | Phase 1 — 2D Square Lattice | ✅ | HIGH | 2026-06-24 | 2026-06-24 | 2026-06-24 | [Details](tasks/T20a.md) |
| T20b | Phase 2 — Multi-Lattice FSS | ✅ | HIGH | 2026-06-25 | 2026-06-25 | 2026-06-25 | [Details](tasks/T20b.md) |
| T20c | Phase 3 — 3D Cubic Lattice | ✅ | HIGH | 2026-06-25 | 2026-06-25 | 2026-06-25 | [Details](tasks/T20c.md) |
| T21 | Worker Threads + Checkpointing | ✅ | HIGH | 2026-06-25 | 2026-06-25 | 2026-06-25 | [Details](tasks/T21.md) |
| T21a | Fast Monte Carlo Kernel | ✅ | HIGH | 2026-06-25 | 2026-06-25 | 2026-06-25 | [Details](tasks/T21a.md) |
| T22 | Spin Foam Amplitudes | ✅ | HIGH | 2026-06-25 | 2026-06-25 | 2026-06-25 | [Details](tasks/T22.md) |
| T22a | Path 1 — SU(2) Four-Leg Group-Average Estimate | ✅ | HIGH | 2026-06-28 | 2026-06-28 | 2026-06-28 | [Details](tasks/T22a.md) |
| T25 | Volume Operator Eigenvalues | ✅ | HIGH | 2026-06-24 | 2026-06-24 | 2026-06-24 | [Details](tasks/T25.md) |
| T27 | Rust Z₂ LGT Framework | ✅ | HIGH | 2026-06-25 | 2026-06-25 | 2026-06-25 | [Details](tasks/T27.md) |
| T28 | Simulation Dashboard (v1) | ✅ | MEDIUM | 2026-06-26 | 2026-06-26 | 2026-06-26 | [Details](tasks/T28.md) |
| T28a | Dashboard v2 — Functional JS | ✅ | HIGH | 2026-06-27 | 2026-06-27 | 2026-06-27 | [Details](tasks/T28a.md) |
| T30 | Unified Plotting Module | ✅ | MEDIUM | 2026-06-27 | 2026-06-27 | 2026-06-27 | [Details](tasks/T30.md) |

## Pending Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T22b | Path 2 — Full Systematic Study | ⬜ | MEDIUM | 2026-06-28 | T22a | [Details](tasks/T22b.md) |
| T29 | Extensible Numerics Schema Design | ⬜ | MEDIUM | 2026-06-27 | T28a | [Details](tasks/T29.md) |

## Task Relationships

```
T14: SU(2) Haar + Representation (ts-quantum core)
  └── 2026-06-28
T15: Spin Foam Package (ts-quantum-spin-foam)
  └── 2026-06-28
T20: Z₂ Lattice Gauge Theory Monte Carlo
  └── 2026-06-24
T20a: Phase 1 — 2D Square Lattice
  └── 2026-06-24
T20b: Phase 2 — Multi-Lattice FSS
  └── 2026-06-25
T20c: Phase 3 — 3D Cubic Lattice
  └── 2026-06-25
T20d: Critical Exponent Extraction from 3D Z₂ LGT
  └── T32
T21: Worker Threads + Checkpointing
  └── 2026-06-25
T21a: Fast Monte Carlo Kernel
  └── 2026-06-25
T22: Spin Foam Amplitudes
  └── 2026-06-25
T22a: Path 1 — SU(2) Four-Leg Group-Average Estimate
  └── 2026-06-28
T22b: Path 2 — Full Systematic Study
  └── T22a
T23: Entanglement Structure
  └── T20
T24: Domain Wall Dynamics
  └── T20
  └── T21
T25: Volume Operator Eigenvalues
  └── 2026-06-24
T27: Rust Z₂ LGT Framework
  └── 2026-06-25
T28: Simulation Dashboard (v1)
  └── 2026-06-26
T28a: Dashboard v2 — Functional JS
  └── 2026-06-27
T29: Extensible Numerics Schema Design
  └── T28a
T30: Unified Plotting Module
  └── 2026-06-27
T31: Signed Volume Observable
  └── —
T32: Post-May Numerics Correction and Reproducibility Pass
  └── T20d
  └── T22a
  └── T25
  └── T27
  └── T31
```

## Status Summary

- **Active**: 5
- **Completed**: 15
- **Paused**: 0
- **Total**: 22
