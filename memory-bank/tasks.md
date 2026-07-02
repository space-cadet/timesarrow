# Memory Bank - Sage Workspace

*Created: 2026-07-02 16:48:02 IST*
*Last Updated: 2026-07-02 16:48:02 IST*

## Overview

This is the Memory Bank for the Sage (灵剑) OpenClaw workspace.

## Active Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T23 | Entanglement Structure | 🔄 | HIGH | 2026-06-24 | T20 | [Details](tasks/T23.md) |
| T24 | Domain Wall Dynamics | 🔄 | HIGH | 2026-06-24 | T20, T21 | [Details](tasks/T24.md) |
| T31 | Signed Volume Observable | 🔄 | MEDIUM | 2026-07-02 | — | [Details](tasks/T31.md) |

## Completed Tasks

| ID | Title | Status | Priority | Started | Completed | Dependencies | Details |
|----|-------|--------|----------|---------|-----------|--------------|---------|
| T14 | SU(2) Haar + Representation (ts-quantum core) | ✅ | HIGH | 2026-06-28 | 2026-06-28 | — | [Details](tasks/T14.md) |
| T15 | Spin Foam Package (ts-quantum-spin-foam) | ✅ | HIGH | 2026-06-28 | 2026-06-28 | 2026-06-29, T14 | [Details](tasks/T15.md) |
| T20 | Z₂ Lattice Gauge Theory Monte Carlo | ✅ | HIGH | 2026-06-24 | 2026-06-24 | T25, T27 | [Details](tasks/T20.md) |
| T20a | Phase 1 — 2D Square Lattice | ✅ | HIGH | 2026-06-24 | 2026-06-24 | — | [Details](tasks/T20a.md) |
| T20b | Phase 2 — Multi-Lattice FSS | ✅ | HIGH | 2026-06-25 | 2026-06-25 | T20a | [Details](tasks/T20b.md) |
| T20c | Phase 3 — 3D Cubic Lattice | ✅ | HIGH | 2026-06-25 | 2026-06-25 | T20a | [Details](tasks/T20c.md) |
| T20d | Critical Exponent Extraction from 3D Z₂ LGT | ✅ | MEDIUM | 2026-06-26 | 2026-06-26 | 2026-06-29, — | [Details](tasks/T20d.md) |
| T21 | Worker Threads + Checkpointing | ✅ | HIGH | 2026-06-25 | 2026-06-25 | — | [Details](tasks/T21.md) |
| T21a | Fast Monte Carlo Kernel | ✅ | HIGH | 2026-06-25 | 2026-06-25 | T20b | [Details](tasks/T21a.md) |
| T22 | Spin Foam Amplitudes | ✅ | HIGH | 2026-06-25 | 2026-06-25 | T14, T20c | [Details](tasks/T22.md) |
| T22a | Path 1 — Quick Estimate (FK Vertex j=½ vs j=1) | ✅ | HIGH | 2026-06-28 | 2026-06-28 | 2026-06-29, — | [Details](tasks/T22a.md) |
| T25 | Volume Operator Eigenvalues | ✅ | HIGH | 2026-06-24 | 2026-06-24 | — | [Details](tasks/T25.md) |
| T27 | Rust Z₂ LGT Framework | ✅ | HIGH | 2026-06-25 | 2026-06-25 | — | [Details](tasks/T27.md) |
| T28 | Simulation Dashboard (v1) | ✅ | MEDIUM | 2026-06-26 | 2026-06-26 | — | [Details](tasks/T28.md) |
| T28a | Dashboard v2 — Functional JS | ✅ | HIGH | 2026-06-27 | 2026-06-27 | 2026-06-27, T20 | [Details](tasks/T28a.md) |
| T30 | Unified Plotting Module | ✅ | MEDIUM | 2026-06-27 | 2026-06-27 | — | [Details](tasks/T30.md) |

## Pending Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T22b | Path 2 — Full Systematic Study | ⬜ | MEDIUM | 2026-06-28 | T22a | [Details](tasks/T22b.md) |
| T29 | Extensible Numerics Schema Design | ⬜ | MEDIUM | 2026-06-27 | T28a | [Details](tasks/T29.md) |

## Task Relationships

```
T14: SU(2) Haar + Representation (ts-quantum core)
  └── —
T15: Spin Foam Package (ts-quantum-spin-foam)
  └── 2026-06-29
  └── T14
T20: Z₂ Lattice Gauge Theory Monte Carlo
  └── T25
  └── T27
T20a: Phase 1 — 2D Square Lattice
  └── —
T20b: Phase 2 — Multi-Lattice FSS
  └── T20a
T20c: Phase 3 — 3D Cubic Lattice
  └── T20a
T20d: Critical Exponent Extraction from 3D Z₂ LGT
  └── 2026-06-29
  └── —
T21: Worker Threads + Checkpointing
  └── —
T21a: Fast Monte Carlo Kernel
  └── T20b
T22: Spin Foam Amplitudes
  └── T14
  └── T20c
T22a: Path 1 — Quick Estimate (FK Vertex j=½ vs j=1)
  └── 2026-06-29
  └── —
T22b: Path 2 — Full Systematic Study
  └── T22a
T23: Entanglement Structure
  └── T20
T24: Domain Wall Dynamics
  └── T20
  └── T21
T25: Volume Operator Eigenvalues
  └── —
T27: Rust Z₂ LGT Framework
  └── —
T28: Simulation Dashboard (v1)
  └── —
T28a: Dashboard v2 — Functional JS
  └── 2026-06-27
  └── T20
T29: Extensible Numerics Schema Design
  └── T28a
T30: Unified Plotting Module
  └── —
T31: Signed Volume Observable
  └── —
```

## Status Summary

- **Active**: 3
- **Completed**: 16
- **Paused**: 0
- **Total**: 21
