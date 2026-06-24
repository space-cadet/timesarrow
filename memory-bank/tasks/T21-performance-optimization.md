# T21 — Performance Optimization: Fast Monte Carlo Kernel

*Task ID: T21*  
*Created: 2026-06-25 03:35 IST*  
*Status: 🔄 Planning*  
*Depends on: T20-Phase2 completion*

## Description

Implement a fast numerical kernel for Monte Carlo simulations to replace the current pure-JavaScript implementation. The JS version is too slow for production lattice gauge theory parameter sweeps.

## Status

- 🔄 Planning / Benchmark design
- ⏳ Blocked: Waiting for T20-Phase2 simulation results to validate physics

## Completion Criteria

- [ ] Benchmark results for all 5 approaches (documented in implementation details)
- [ ] Decision record with speedup numbers and rationale
- [ ] Working fast kernel integrated into ts-quantum
- [ ] **Checkpointing & resume**: Simulations must be pausable and resumable (save/load state)
- [ ] Incremental result writing (don't lose progress on crash)
- [ ] CI build for native addon
- [ ] Pure-JS fallback preserved for testing/debugging

## Progress

1. ⬜ Design benchmark test specification
2. ⬜ Implement Worker Threads test (Node.js)
3. ⬜ Implement Bun runtime test
4. ⬜ Implement Rust + napi-rs test
5. ⬜ Implement C++ + WASM test
6. ⬜ Implement C++ native addon test
7. ⬜ Run benchmarks on M2 Air, record results
8. ⬜ Select winner, implement production kernel
9. ⬜ Integrate into ts-quantum with fallback
10. ⬜ Verify bit-exact / statistically equivalent results

## Related Files

- `memory-bank/implementation/T21-performance-optimization.md` — Architecture & benchmark plan
- `ts-quantum/src/lattice/` — Lattice module (integration target)
- `numerics/src/scripts/` — Simulation scripts (users of kernel)

## Context

**Current performance**: ~5-6 min per simulation (L=16, 100k+500k sweeps). Phase 2A full run: 72 simulations ≈ 6 hours.

**Target**: 10-100× speedup for practical parameter sweeps.

**Hardware**: M2 MacBook Air (8 cores: 4P+4E, 16GB RAM).
