# Session Cache

*Created: 2026-06-27 10:45:51 IST*
*Last Updated: 2026-06-27 10:45:51 IST*

**Started**: 2026-06-27 07:11:46 IST
**Focus Task**: T28: Simulation Dashboard
**Session File**: `sessions/2026-06-27-afternoon.md`
**Status**: 🔄 Active: 13, Paused: 0, Completed: 1

## Overview

- Active: 13 | Paused: 0 | Completed: 1
- Last Session: 2026-06-27
- Current Period: afternoon

## Active Tasks

### T20: Z₂ Lattice Gauge Theory Monte Carlo
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: [Details](tasks/T20.md)
**Progress**:
[Details](tasks/T20.md)

### T20a: Phase 1 — 2D Square Lattice
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: No context

### T20b: Phase 2 — Sharp Phase Transition / Multi-Lattice FSS
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-25
**Context**: [Details](tasks/T20b.md)
**Progress**:
[Details](tasks/T20b.md)

### T20c: Phase 3 — 3D Cubic Lattice
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-25
**Context**: [Details](tasks/T20c.md)
**Progress**:
[Details](tasks/T20c.md)

### T20d: Critical Exponent Extraction from 3D Z₂ LGT
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-26
**Context**: [Details](tasks/T20d.md)
**Progress**:
[Details](tasks/T20d.md)
L=32 simulation running (PID 49975, ~2h elapsed, 690% CPU). Corrected timing estimate: ~6h total wall time for 21 betas x 2M sweeps. L=8 and L=16 complete. Monitoring via subagent.

### T21: Worker Threads + Checkpointing
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-25
**Context**: No context

### T21a: Performance Optimization — Fast Monte Carlo Kernel
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-25
**Context**: [Details](tasks/T21a.md)
**Progress**:
[Details](tasks/T21a.md)

### T22: Spin Foam Amplitudes
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-25
**Context**: [Details](tasks/T22.md)
**Progress**:
[Details](tasks/T22.md)

### T23: Entanglement Structure of the Deconfined Phase
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: [Details](tasks/T23.md)
**Progress**:
[Details](tasks/T23.md)

### T24: Domain Wall Dynamics and Surface Topological Order
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: [Details](tasks/T24.md)
**Progress**:
[Details](tasks/T24.md)

### T25: Volume Operator Eigenvalues
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: No context

### T27: Rust Z₂ LGT Framework
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-25
**Context**: No context

### T28: Simulation Dashboard
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-26
**Context**: No context
**Progress**:
Test DB workflow after full schema fix
Design enhanced simulation dashboard v2: integrated within timesarrow (not standalone), adds performance metrics (wall time, CPU time, timestamps), data export (JSON/CSV), plot gallery, live progress monitoring, task pipeline visualization. Architecture: Quarto + OJS + static JSON (GitHub Pages compatible). Design spec written to memory-bank/implementation/dashboard-v2-design.md.
Session end: T20d L=32 still running (~3.7h CPU). T28 dashboard v2 design complete, collate-data.ts v2 in progress. DB workflow fixed. All changes committed and pushed to GitHub.
Implemented Plot Gallery with 20 plots (category-filtered), Run Detail Browser with parameters/results/timing, performance scaling chart with Observable Plot, compact summary cards, test run indicators. Fixed key finding word wrap, Results card formatting, Vega-Lite→Observable Plot migration. Deployed 5 commits to GitHub Pages.
Created dashboard v2 static HTML prototype with unified Runs & Results + Figure Archive layout. Analyzed old dashboard UX issues (unclear Plot Gallery dropdown, overlapping sections). Proposed extensible schema design with base+extension architecture for general numerics dashboard.

## Completed Tasks

### T28-db-fix: Fixed DB schema drift in timesarrow memory-bank: updated project-local JS files (inserts.js, workflow.js, regenerate.js) to match mb-core v1.1 schema (session_date→date, session_period→period, focus_task→focus). Migrated session_cache table schema. DB-native workflow now fully functional.
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-27
**Completed:** 2026-06-27

## Next Session Focus

1. T20: Z₂ Lattice Gauge Theory Monte Carlo
1. T20a: Phase 1 — 2D Square Lattice
1. T20b: Phase 2 — Sharp Phase Transition / Multi-Lattice FSS

## System Status

- **Memory Bank**: 🔄 Active
- **OpenClaw**: ✅ Operational
