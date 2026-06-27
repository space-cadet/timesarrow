# Memory Bank - Sage Workspace

*Created: 2026-06-27 10:45:51 IST*
*Last Updated: 2026-06-27 10:45:51 IST*

## Overview

This is the Memory Bank for the Sage (灵剑) OpenClaw workspace.

## Active Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T20 | Z₂ Lattice Gauge Theory Monte Carlo | 🔄 | HIGH | 2026-06-24 | T25, T27 | [Details](tasks/T20.md) |
| T20a | Phase 1 — 2D Square Lattice | ✅ | HIGH | 2026-06-24 | — | [Details](tasks/T20a.md) |
| T20b | Phase 2 — Multi-Lattice FSS | ✅ | HIGH | 2026-06-25 | T20a | [Details](tasks/T20b.md) |
| T20c | Phase 3 — 3D Cubic Lattice | ✅ | HIGH | 2026-06-25 | T20a | [Details](tasks/T20c.md) |
| T20d | Critical Exponent Extraction from 3D Z₂ LGT | 🔄 | MEDIUM | 2026-06-26 | — | [Details](tasks/T20d.md) |
| T21 | Worker Threads + Checkpointing | 🔄 | HIGH | 2026-06-25 | — | [Details](tasks/T21.md) |
| T21a | Fast Monte Carlo Kernel | 🔄 | HIGH | 2026-06-25 | T20b | [Details](tasks/T21a.md) |
| T22 | Spin Foam Amplitudes | 🔄 | HIGH | 2026-06-25 | T20c | [Details](tasks/T22.md) |
| T23 | Entanglement Structure | 🔄 | HIGH | 2026-06-24 | T20 | [Details](tasks/T23.md) |
| T24 | Domain Wall Dynamics | 🔄 | HIGH | 2026-06-24 | T20, T21 | [Details](tasks/T24.md) |
| T25 | Volume Operator Eigenvalues | 🔄 | HIGH | 2026-06-24 | — | [Details](tasks/T25.md) |
| T27 | Rust Z₂ LGT Framework | 🔄 | HIGH | 2026-06-25 | — | [Details](tasks/T27.md) |
| T28 | Simulation Dashboard (v1) | ✅ | MEDIUM | 2026-06-26 | — | [Details](tasks/T28.md) |

## Completed Tasks

| ID | Title | Status | Priority | Started | Completed | Dependencies | Details |
|----|-------|--------|----------|---------|-----------|--------------|---------|
| T28-db-fix | Fixed DB schema drift in timesarrow memory-bank: updated project-local JS files to match mb-core v1.1 schema. | ✅ | MEDIUM | 2026-06-27 | 2026-06-27 | - | [Details](tasks/T28-db-fix.md) |
| T28a | Dashboard v2 — Functional JS Implementation | ✅ | HIGH | 2026-06-27 | 2026-06-27 | T20 | [Details](tasks/T28a.md) |

## Pending Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T29 | Extensible Numerics Schema Design | ⬜ | MEDIUM | 2026-06-27 | T28a | [Details](tasks/T29.md) |

## Task Relationships

```
T20: Z₂ Lattice Gauge Theory Monte Carlo
  └── T25
  └── T27
T20a: Phase 1 — 2D Square Lattice
  └── [Details](tasks/T20a.md)
T20b: Phase 2 — Sharp Phase Transition / Multi-Lattice FSS
  └── T20a
T20c: Phase 3 — 3D Cubic Lattice
  └── T20a
T20d: Critical Exponent Extraction from 3D Z₂ LGT
  └── —
T21: Worker Threads + Checkpointing
  └── [Details](tasks/T21.md)
T21a: Performance Optimization — Fast Monte Carlo Kernel
  └── T20b
T22: Spin Foam Amplitudes
  └── T20c
T23: Entanglement Structure of the Deconfined Phase
  └── T20
T24: Domain Wall Dynamics and Surface Topological Order
  └── T20
  └── T21
T25: Volume Operator Eigenvalues
  └── [Details](tasks/T25.md)
T27: Rust Z₂ LGT Framework
  └── [Details](tasks/T27.md)
T28: Simulation Dashboard
  └── [Details](tasks/T28.md)
T28-db-fix: Fixed DB schema drift in timesarrow memory-bank: updated project-local JS files (inserts.js, workflow.js, regenerate.js) to match mb-core v1.1 schema (session_date→date, session_period→period, focus_task→focus). Migrated session_cache table schema. DB-native workflow now fully functional.
T28a: Dashboard v2 — Functional JS Implementation
T29: Extensible Numerics Schema Design
```

## Status Summary

- **Active**: 8
- **Completed**: 4 (T20a, T20b, T20c, T28-db-fix, T28a)
- **Paused**: 0
- **Pending**: 1 (T29)
- **Total**: 14
