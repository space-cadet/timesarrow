# timesarrow — Active Context

*Updated: 2026-06-25 03:37 IST*

## Current Focus

**T20-Phase2**: Multi-lattice finite-size scaling simulation is RUNNING.

**Status**: Batch 1/12 in progress. 72 total simulations (3 lattice sizes × 24 β values).
**ETA**: ~60-90 minutes.
**Monitoring**: Process `fresh-seaslug` (pid 54286), healthy at 99.9% CPU.

## T21 — Performance Optimization (New)

**Status**: 🔄 Planning phase. **Blocked until T20-Phase2 completes**.

**Plan**: Benchmark 5 approaches for fast MC kernel, then implement winner.

| # | Approach | Expected Speedup | Effort |
|---|----------|-----------------|--------|
| 1 | Node.js Worker Threads | 6-8× | Low |
| 2 | Bun runtime | 3-5× | Very Low |
| 3 | Rust + napi-rs | 50-100× | Medium |
| 4 | C++ + WASM | 20-50× | Medium |
| 5 | C++ native addon | 50-100× | Medium-High |

**Approach**: Write minimal benchmark test in each framework, measure actual wall-clock time on M2 Air for identical workload (L=16, 10k sweeps). Decide based on speed × maintainability.

**Likely winner**: Rust + napi-rs (best perf/safety tradeoff, ARM64-native, path to GPU).

## Key Decisions (this session)

- **GPU not needed**: CPU parallelization of independent simulations sufficient.
- **T21 deferred**: Start benchmarking after T20-Phase2 results confirm physics is correct.
- **Pure-JS preserved**: Fast kernel will be opt-in; JS fallback stays for testing/debugging.

## Files in Play

| File | Role | Status |
|------|------|--------|
| `ts-quantum/src/lattice/observables.ts` | P², P⁴, Binder, C, χ | ✅ Added |
| `numerics/src/scripts/t20-z2-lgt-phase2a.cjs` | Production multi-lattice sweep | 🔄 Running |
| `numerics/output/t20-phase2a-finite-size.json` | Results (81 sims) | ⏳ Pending |
| `memory-bank/tasks/T21-performance-optimization.md` | Benchmark plan | ✅ Created |

## What's Next

1. **Wait** for T20-Phase2 simulation to complete (~1 hour)
2. **Validate** results: check χ peaks, U crossing, ⟨P⟩ sharpening
3. **Start T21 benchmarks**: Worker Threads → Bun → Rust → C++
4. **Implement** winner and integrate into ts-quantum

---

*See `memory-bank/tasks/T20-Phase2-sharp-transition.md` for Phase 2 plan.*
*See `memory-bank/tasks/T21-performance-optimization.md` for benchmark plan.*
