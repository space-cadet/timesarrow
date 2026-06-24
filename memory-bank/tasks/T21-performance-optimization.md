# T21 — Performance Optimization: Fast Monte Carlo Kernel

*Created: 2026-06-25 03:35 IST*
*Status: 🔄 Planning*
*Depends on: T20-Phase2 completion*

## Problem

Pure JavaScript Monte Carlo is too slow for production lattice gauge theory simulations:
- Current: ~5-6 min per simulation (L=16, 100k+500k sweeps)
- Phase 2A full run: 72 simulations × ~5 min = ~6 hours
- Need: ~10-100× speedup for practical parameter sweeps

## Proposed Solution: Benchmark + Implement Fast Kernel

### Phase 1: Benchmarking (Immediate)

**Goal**: Write minimal test code in each candidate framework, measure actual performance on M2 Air.

**Test**: Single Z₂ LGT simulation, L=16, β=0.44, 10k sweeps. Measure wall-clock time.

**Candidates**:

| # | Approach | Expected Speedup | Effort | Notes |
|---|----------|-----------------|--------|-------|
| 1 | Node.js Worker Threads | 6-8× | Low | Parallelize across 8 cores, keep JS |
| 2 | Bun runtime | 3-5× | Very Low | Drop-in Node replacement |
| 3 | Rust + napi-rs | 50-100× | Medium | Native ARM64 binary, memory-safe |
| 4 | C++ + WASM | 20-50× | Medium | Portable, can run in browser |
| 5 | C++ native addon | 50-100× | Medium-High | Direct Node integration |

### Phase 2: Implementation (After Benchmarks)

**Decision criteria**:
1. Speed (wall-clock for realistic workload)
2. Maintainability (your familiarity with language)
3. Integration (how easily it fits ts-quantum architecture)
4. Future-proofing (GPU path, web deployment, etc.)

**Likely winner**: Rust + napi-rs
- Best performance + safety tradeoff
- Excellent M2 ARM64 support
- Can later compile to WASM for web
- Clear path to GPU (Rust → CUDA/Metal via crates)

### Phase 3: Integration

**Architecture**:
```
ts-quantum
├── src/lattice/          # TS interface (types, API)
├── src/lattice/native/   # Rust kernel (napi-rs)
│   ├── Cargo.toml
│   ├── src/lib.rs        # Z2GaugeField, metropolisSweep
│   └── src/observables.rs # averagePlaquetteMoments, etc.
└── src/lattice/index.ts  # Re-exports (fallback to JS if native unavailable)
```

**Fallback**: Keep pure-JS implementation for:
- Quick tests
- Environments without native build
- Debugging / verification

## Resources

- **M2 MacBook Air**: 8 cores (4P+4E), 16GB RAM
- **Rust**: Install via rustup (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`)
- **napi-rs**: `npm install @napi-rs/cli`
- **Bun**: `curl -fsSL https://bun.sh/install | bash`

## Benchmark Test Specification

```
Test: Z₂ LGT Metropolis sweep
Lattice: L=16, 2D square
β: 0.44
Sweeps: 10,000 (thermalization only)
Measurement: wall-clock time, 3 runs, average
Output: sweeps/second
```

## Acceptance Criteria

- [ ] Benchmark results for all 5 approaches
- [ ] Documented decision with speedup numbers
- [ ] Working fast kernel integrated into ts-quantum
- [ ] CI build for native addon (GitHub Actions)
- [ ] Pure-JS fallback preserved

## Notes

- **Don't start until T20-Phase2 simulation completes** — we need those results first
- **Incremental**: Start with Worker Threads (quick win), then migrate to Rust
- **Verification**: Ensure bit-exact or statistically equivalent results vs JS
