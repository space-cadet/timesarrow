# Memory Bank - Sage Workspace

*Created: 2026-06-27 10:45:51 IST*
*Last Updated: 2026-07-02 21:40 IST*

## Overview

This is the Memory Bank for the Sage (灵剑) OpenClaw workspace.

## Active Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T20 | Z₂ Lattice Gauge Theory Monte Carlo | ✅ | HIGH | 2026-06-24 | T25, T27 | [Details](tasks/T20.md) |
| T20a | Phase 1 — 2D Square Lattice | ✅ | HIGH | 2026-06-24 | — | [Details](tasks/T20a.md) |
| T20b | Phase 2 — Multi-Lattice FSS | ✅ | HIGH | 2026-06-25 | T20a | [Details](tasks/T20b.md) |
| T20c | Phase 3 — 3D Cubic Lattice | ✅ | HIGH | 2026-06-25 | T20a | [Details](tasks/T20c.md) |
| T20d | Critical Exponent Extraction from 3D Z₂ LGT | ✅ | MEDIUM | 2026-06-26 | — | [Details](tasks/T20d.md) |
| T21 | Worker Threads + Checkpointing | ✅ | HIGH | 2026-06-25 | — | [Details](tasks/T21.md) |
| T21a | Fast Monte Carlo Kernel | ✅ | HIGH | 2026-06-25 | T20b | [Details](tasks/T21a.md) |
| T22 | Spin Foam Amplitudes | ✅ | HIGH | 2026-06-25 | T20c, T14 | [Details](tasks/T22.md) |
| T22a | Path 1 — Quick Estimate (FK Vertex j=½ vs j=1) | ✅ | HIGH | 2026-06-28 | — | [Details](tasks/T22a.md) |
| T22b | Path 2 — Full Systematic Study | ⬜ | MEDIUM | 2026-06-28 | T22a | [Details](tasks/T22b.md) |
| T14 | SU(2) Haar + Representation (ts-quantum core) | ✅ | HIGH | 2026-06-28 | — | [Details](../ts-quantum/memory-bank/tasks/T14.md) |
| T15 | Spin Foam Package (ts-quantum-spin-foam) | ✅ | HIGH | 2026-06-28 | T14 | [Details](../ts-quantum-spin-foam/memory-bank/tasks/T1.md) |
| T23 | Entanglement Structure | 🔄 | HIGH | 2026-06-24 | T20 | [Details](tasks/T23.md) |
| T24 | Domain Wall Dynamics | 🔄 | HIGH | 2026-06-24 | T20, T21 | [Details](tasks/T24.md) |
| T25 | Volume Operator Eigenvalues | ✅ | HIGH | 2026-06-24 | — | [Details](tasks/T25.md) |
| T27 | Rust Z₂ LGT Framework | ✅ | HIGH | 2026-06-25 | — | [Details](tasks/T27.md) |
| T28 | Simulation Dashboard (v1) | ✅ | MEDIUM | 2026-06-26 | — | [Details](tasks/T28.md) |
| T28a | Dashboard v2 — Functional JS | ✅ | HIGH | 2026-06-27 | T20 | [Details](tasks/T28a.md) |
| T31 | Signed Volume Observable | 🔄 | MEDIUM | 2026-07-02 | — | [Details](tasks/T31.md) |
| T30 | Unified Plotting Module | ✅ | MEDIUM | 2026-06-27 | — | [Details](tasks/T30.md) |

## Completed Tasks

| ID | Title | Status | Priority | Started | Completed | Dependencies | Details |
|----|-------|--------|----------|---------|-----------|--------------|---------|
| T28-db-fix | Fixed DB schema drift in timesarrow memory-bank: updated project-local JS files to match mb-core v1.1 schema. | ✅ | MEDIUM | 2026-06-27 | 2026-06-27 | - | [Details](tasks/T28-db-fix.md) |
| T28a | Dashboard v2 — Functional JS Implementation | ✅ | HIGH | 2026-06-27 | 2026-06-27 | T20 | [Details](tasks/T28a.md) |
| T20d | Critical Exponent Extraction from 3D Z₂ LGT | ✅ | MEDIUM | 2026-06-26 | 2026-06-29 | — | [Details](tasks/T20d.md) |
| T22a | Path 1 — Quick Estimate (FK Vertex j=½ vs j=1) | ✅ | HIGH | 2026-06-28 | 2026-06-29 | — | [Details](tasks/T22a.md) |
| T15 | Spin Foam Package (ts-quantum-spin-foam) | ✅ | HIGH | 2026-06-28 | 2026-06-29 | T14 | [Details](../ts-quantum-spin-foam/memory-bank/tasks/T1.md) |

## Pending Tasks

| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T29 | Extensible Numerics Schema Design | ⬜ | MEDIUM | 2026-06-27 | T28a | [Details](tasks/T29.md) |
| T22b | Path 2 — Full Systematic Study | ⬜ | MEDIUM | 2026-06-28 | T22a | [Details](tasks/T22b.md) |
| T20d-ext | L=48/64 fine scans | ⬜ | LOW | — | T20d | Future work |

## Task Relationships

```
T20: Z₂ Lattice Gauge Theory Monte Carlo
  ├── T20a: 2D Square Lattice ✅
  ├── T20b: 2D FSS ✅
  ├── T20c: 3D Cubic Lattice ✅
  ├── T20d: 3D FSS ✅
  │   └── T20d-ext: L=48/64 ⬜
  └── T27: Rust Framework ✅

T22: Spin Foam Amplitudes
  ├── T22a: FK Vertex Estimate ✅
  └── T22b: Full Systematic Study ⬜

T31: Signed Volume Observable 🔄
  └── Gauge-fixing iteration needed
  
T25: Volume Operator Eigenvalues ✅
T28: Dashboard v1 ✅ → T28a: Dashboard v2 ✅
T30: Unified Plotting Module ✅

Cross-repo:
  T14 (ts-quantum) → T15 (ts-quantum-spin-foam) → T22a
```
