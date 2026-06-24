# T21 — Performance Optimization: Fast Monte Carlo Kernel

*Implementation Details for Task T21*  
*Created: 2026-06-25 03:35 IST*  
*Last Updated: 2026-06-25 03:40 IST*

## Problem Statement

Pure JavaScript Monte Carlo is too slow for production lattice gauge theory simulations:

| Metric | Current (JS) | Needed |
|--------|-------------|--------|
| Single sim (L=16, 600k sweeps) | ~5-6 min | <30 sec |
| Phase 2A full run (72 sims) | ~6 hours | <10 min |
| Speedup | 1× | 10-100× |

## Root Cause

The Z₂ Metropolis algorithm is inherently sequential (single-site updates), but the inner loop (site iteration, plaquette product, acceptance) is pure arithmetic that JavaScript cannot optimize well:
- No SIMD vectorization
- Dynamic typing overhead
- No inlining guarantees
- GC pauses during long runs

## Benchmark Approach

### Test Specification

```
Workload: Z₂ LGT Metropolis sweep
Lattice: L=16, 2D square (256 sites, ~512 plaquettes)
β: 0.44 (near critical, moderate acceptance)
Sweeps: 10,000 (thermalization only, no measurement overhead)
Metric: sweeps/second (wall-clock, single core)
Runs: 5, drop fastest/slowest, average middle 3
```

### Why This Test?

- **Representative**: Single sweep is the unit of work; all kernels must implement this
- **Isolated**: No measurement, no I/O, no parallelization tricks
- **Reproducible**: Fixed lattice, fixed RNG seed, deterministic hot path
- **Scalable**: If a kernel does 10k sweeps in X seconds, 600k sweeps take 60X seconds

### Candidates

| # | Approach | Expected Speedup | Effort | Notes |
|---|----------|-----------------|--------|-------|
| 1 | Node.js Worker Threads | 6-8× | Low | Parallelize across 8 cores; still JS per core |
| 2 | Bun runtime | 3-5× | Very Low | Drop-in Node replacement; faster JS engine |
| 3 | Rust + napi-rs | 50-100× | Medium | Native ARM64; memory-safe; path to GPU |
| 4 | C++ + WASM | 20-50× | Medium | Portable; can run in browser; WASM overhead |
| 5 | C++ native addon | 50-100× | Medium-High | Direct Node integration; platform-specific builds |

### Selection Criteria

Weighted score = (speedup × 0.4) + (maintainability × 0.3) + (integration_ease × 0.2) + (future_proof × 0.1)

## Architecture Design

### Target Structure (Post-Implementation)

```
ts-quantum/
├── src/
│   ├── lattice/
│   │   ├── geometry.ts          # Lattice types (unchanged)
│   │   ├── gaugeField.ts        # TS wrapper + fallback
│   │   ├── action.ts            # Action definitions (unchanged)
│   │   ├── monteCarlo.ts        # Orchestration (unchanged)
│   │   ├── observables.ts       # Observable calculations (TS)
│   │   └── native/              # NEW: fast kernels
│   │       ├── Cargo.toml       # Rust crate manifest
│   │       ├── src/lib.rs       # Z2GaugeField struct, sweep kernel
│   │       ├── src/observables.rs # Fast plaquette moments
│   │       └── build.rs         # napi-rs build script
│   └── index.ts                 # Re-exports with auto-detection
├── package.json                 # Add native dependency + optional
└── Cargo.toml (workspace root)  # If Rust workspace
```

### Integration Pattern

```typescript
// src/lattice/gaugeField.ts
import { Z2GaugeFieldNative } from './native';

export class Z2GaugeField {
  private native: Z2GaugeFieldNative | null = null;
  
  constructor(lattice: SquareLattice, init: 'random' | 'ordered') {
    // Try native first
    try {
      this.native = new Z2GaugeFieldNative(lattice.size, init);
    } catch {
      // Fallback to pure JS
      this.useJsImplementation(lattice, init);
    }
  }
  
  metropolisSweep(beta: number): void {
    if (this.native) {
      this.native.metropolisSweep(beta);
    } else {
      this.jsMetropolisSweep(beta);
    }
  }
}
```

### Rust Kernel Design (Likely Winner)

```rust
// native/src/lib.rs
use napi_derive::napi;
use rand::rngs::StdRng;
use rand::SeedableRng;

#[napi]
pub struct Z2GaugeField {
    links: Vec<i8>,   // Flattened link array: ±1
    size: u32,
    rng: StdRng,
}

#[napi]
impl Z2GaugeField {
    #[napi(constructor)]
    pub fn new(size: u32, init_ordered: bool) -> Self {
        // ...
    }
    
    #[napi]
    pub fn metropolis_sweep(&mut self, beta: f64) {
        // Hot path: iterate all sites, compute plaquettes, accept/reject
        // Key optimizations:
        // - Precompute neighbor indices (no hash lookups)
        // - SIMD-friendly plaquette product (4 multiplies)
        // - Branchless acceptance (compare to precomputed exp(-2βΔS))
    }
    
    #[napi]
    pub fn average_plaquette_moments(&self) -> PlaquetteMoments {
        // Single-pass: compute P, P², P⁴
    }
}
```

### Key Optimizations

1. **Memory layout**: Flat `Vec<i8>` instead of nested arrays; contiguous access
2. **Precomputed neighbors**: Build neighbor index table once at construction
3. **Branchless Metropolis**: `if random < precomputed_threshold { flip }`
4. **SIMD plaquette product**: 4 contiguous links → `_mm_mul_epi8` or similar
5. **Single-pass observables**: Compute P, P², P⁴ in one lattice traversal

## Verification Strategy

### Correctness Tests

1. **Bit-exact for small L**: Run Rust and JS on L=4, same seed → identical configs after N sweeps
2. **Statistical equivalence**: Run both on L=16, different seeds → same ⟨P⟩ within error
3. **Observable parity**: χ, C, U computed from both → values agree within 1%

### Performance Tests

1. **Sweep throughput**: sweeps/second, single core
2. **Scaling**: L=8,16,32,64 — measure time vs L² (should be ~linear)
3. **Parallel efficiency**: 1,2,4,6,8 cores — measure speedup vs ideal

## Decision Record

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-25 | Start with benchmarks, not implementation | Need data to choose; no premature optimization |
| 2026-06-25 | Worker Threads first (quick win) | 6-8× speedup, zero new dependencies |
| 2026-06-25 | Rust as likely long-term winner | Best perf/safety tradeoff, ARM64-native, GPU path |

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Rust build fails on M2 | Test with `cargo build --target aarch64-apple-darwin` early |
| napi-rs integration complex | Start with minimal PoC: one function, one test |
| JS/Rust results differ | Implement deterministic test harness; compare bit-exact |
| Native addon breaks CI | Build matrix: macOS (ARM64), Linux (x64), optional Windows |

## Resources

- **M2 MacBook Air**: 8 cores (4P+4E), 16GB RAM
- **Rust**: Install via rustup
- **napi-rs**: `npm install @napi-rs/cli`
- **Bun**: `curl -fsSL https://bun.sh/install | bash`

## Next Steps

1. **T20-Phase2 completes** → validate physics is correct
2. **Write minimal benchmark tests** for each approach (single file each)
3. **Run benchmarks** → record numbers
4. **Decide** → based on speedup × maintainability
5. **Implement** → production kernel + integration
