# Session Cache

*Created: 2026-07-08 10:21:16 IST*
*Last Updated: 2026-07-14 04:55:00 IST*

**Started**: 2026-07-14 04:55:00 IST
**Focus Task**: T32: Post-May Numerics Correction and Reproducibility Pass
**Session File**: `sessions/2026-07-14-night.md`
**Status**: 🔄 Active: 5, Paused: 0, Completed: 15

## Overview

- Active: 5 | Paused: 0 | Completed: 15
- Last Session: 2026-07-14
- Current Period: night

## Active Tasks

### T20d: Critical Exponent Extraction from 3D Z₂ LGT
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-26
**Context**: [Details](tasks/T20d.md)
**Progress**:
[Details](tasks/T20d.md)

### T23: Entanglement Structure
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: [Details](tasks/T23.md)
**Progress**:
[Details](tasks/T23.md)

### T24: Domain Wall Dynamics
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-06-24
**Context**: [Details](tasks/T24.md)
**Progress**:
[Details](tasks/T24.md)

### T31: Signed Volume Observable
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-07-02
**Context**: [Details](tasks/T31.md)
**Progress**:
[Details](tasks/T31.md)

### T32: Post-May Numerics Correction and Reproducibility Pass
**Status:** 🔄 **IN PROGRESS**
**Started:** 2026-07-05
**Context**: [Details](tasks/T32.md)
**Progress**:
[Details](tasks/T32.md)
Audited the published numerics deployment against the corrected local Quarto render. Synced the corrected `_site` output to `space-cadet.github.io` and pushed deploy commit `92d05cc`. Repaired missing dashboard asset publishing, fixed T20 Phase 3b figure paths, normalized page timestamps, added a `Last Updated` column on the numerics index, redeployed the refreshed site via `21a496e` and `efe6780`, then validated the T31 Rust tests under a Rust 2024-compatible toolchain, measured T20d rerun timing calibrations, completed a fresh local `L=8` fine-scan rerun, and handed the long remaining reruns to Kimi.

Follow-up: repaired the local validation workflow so `scripts/validate.sh` now passes in this checkout, completed fresh `T20d` production reruns for `L=16` and `L=32`, and updated the `T20d` reanalysis to treat the result as proof-of-principle support for the corrected continuous-transition interpretation rather than a precision critical-exponent measurement. The new comparison set now shows the susceptibility/specific-heat peak drifting from `β≈0.752` at `L=16` to `β≈0.758` at `L=32`, with a simple peak-drift guide near the literature value `β_c≈0.761`.

## Completed Tasks

### T14: SU(2) Haar + Representation (ts-quantum core)
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-28
**Completed:** 2026-06-28

### T15: Spin Foam Package (ts-quantum-spin-foam)
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-28
**Completed:** 2026-06-28

### T20: Z₂ Lattice Gauge Theory Monte Carlo
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-24
**Completed:** 2026-06-24

### T20a: Phase 1 — 2D Square Lattice
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-24
**Completed:** 2026-06-24

### T20b: Phase 2 — Multi-Lattice FSS
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-25
**Completed:** 2026-06-25

### T20c: Phase 3 — 3D Cubic Lattice
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-25
**Completed:** 2026-06-25

### T21: Worker Threads + Checkpointing
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-25
**Completed:** 2026-06-25

### T21a: Fast Monte Carlo Kernel
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-25
**Completed:** 2026-06-25

### T22: Spin Foam Amplitudes
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-25
**Completed:** 2026-06-25

### T22a: Path 1 — SU(2) Four-Leg Group-Average Estimate
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-28
**Completed:** 2026-06-28

### T25: Volume Operator Eigenvalues
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-24
**Completed:** 2026-06-24

### T27: Rust Z₂ LGT Framework
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-25
**Completed:** 2026-06-25

### T28: Simulation Dashboard (v1)
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-26
**Completed:** 2026-06-26

### T28a: Dashboard v2 — Functional JS
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-27
**Completed:** 2026-06-27

### T30: Unified Plotting Module
**Status:** ✅ **COMPLETED**
**Started:** 2026-06-27
**Completed:** 2026-06-27

## Next Session Focus

1. T20d: Critical Exponent Extraction from 3D Z₂ LGT
1. T23: Entanglement Structure
1. T24: Domain Wall Dynamics

## System Status

- **Memory Bank**: 🔄 Active
- **OpenClaw**: ✅ Operational
