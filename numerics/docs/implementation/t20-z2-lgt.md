---
title: "T20 — Z₂ LGT Monte Carlo Implementation"
subtitle: "Architecture and design decisions"
---

## Overview

This document describes the implementation architecture for the Z₂ Lattice Gauge Theory Monte Carlo simulation. The design follows the principle that **general-purpose lattice gauge theory tools belong in `ts-quantum`**, while **specific simulation setups, parameter sweeps, and analysis belong in `timesarrow/numerics/`**.

## ts-quantum: Lattice Gauge Theory Module

### Module Structure

```
src/lattice/
├── geometry.ts          # Lattice types and geometry
├── gaugeField.ts        # Z₂ gauge field (link variables)
├── action.ts            # Wilson action computation
├── monteCarlo.ts        # Metropolis algorithm
├── observables.ts       # Physical observables
└── index.ts             # Public API exports
```

### Lattice Geometry (`geometry.ts`)

**Types:**
- `Lattice` — base interface with `sites`, `links`, `plaquettes`
- `SquareLattice` — 2D square lattice, L×L sites
- `TriangularLattice` — 2D triangular lattice, L×L sites with skewed boundary
- `CubicLattice` — 3D cubic lattice, L³ sites

**Key functions:**
- `createSquareLattice(L)` — returns Lattice with periodic BC
- `createTriangularLattice(L)` — returns triangular Lattice
- `createCubicLattice(L)` — returns 3D cubic Lattice
- `getNeighbors(site, lattice)` — returns array of neighbor site indices
- `getPlaquettes(site, lattice)` — returns plaquettes containing site

### Gauge Field (`gaugeField.ts`)

**Class `Z2GaugeField`:**
```typescript
class Z2GaugeField {
  constructor(lattice: Lattice, init: 'hot' | 'cold' | 'random');
  
  // Link accessors
  getLink(site: number, direction: number): number;      // returns ±1
  setLink(site: number, direction: number, value: number); // value: ±1
  flipLink(site: number, direction: number): void;         // flips sign
  
  // State
  lattice: Lattice;
  links: Int8Array;  // flat array of ±1 values
  
  // I/O
  toJSON(): object;
  static fromJSON(data: object): Z2GaugeField;
}
```

### Action (`action.ts`)

**Wilson action for Z₂:**
$$S = -\beta \sum_{\text{plaquettes}} \prod_{e \in \square} \sigma_e$$

**Functions:**
- `computePlaquetteProduct(field, site, mu, nu)` — product of 4 links around plaquette
- `computeAction(field, beta)` — total action S
- `computeDeltaS(field, site, direction, beta)` — change in action from flipping one link

### Monte Carlo (`monteCarlo.ts`)

**Metropolis algorithm:**
```typescript
function metropolisSweep(field: Z2GaugeField, beta: number): void;
```
1. Iterate over all links
2. For each link, compute ΔS from flipping
3. Accept flip with probability min(1, exp(−ΔS))
4. Track acceptance rate

**Thermalization:**
```typescript
function thermalize(field: Z2GaugeField, beta: number, sweeps: number): void;
```

### Observables (`observables.ts`)

**Physical quantities:**
- `averagePlaquette(field)` — ⟨P⟩ = ⟨∏_□ σ_e⟩ per plaquette
- `specificHeat(field, beta)` — C_V = (⟨S²⟩ − ⟨S⟩²) / V
- `wilsonLoop(field, corner, size)` — W(C) = ⟨∏_C σ_e⟩ for rectangular loop
- `correlationLength(field)` — from exponential decay of Wilson loops

## timesarrow: Simulation Setup

### Directory Structure

```
numerics/src/
├── scripts/
│   ├── t20-z2-lgt-phase1.ts   # 2D square lattice
│   ├── t20-z2-lgt-phase2.ts   # 2D triangular lattice
│   └── t20-z2-lgt-phase3.ts   # 3D cubic lattice
├── analysis/
│   └── t20-analysis.ts         # Finite-size scaling, critical coupling
└── output/
    └── t20-z2-lgt.json         # Results
```

### Phase 1: 2D Square Lattice

**Parameters:**
- Lattice sizes: L = 8, 16, 32, 64
- Couplings: β = 0.1 to 1.0, step 0.05
- Thermalization: 10⁴ sweeps
- Measurement: 10⁵ sweeps, every 10
- Binning: 100 bins for error analysis

**Observables:**
- Average plaquette ⟨P⟩ vs β
- Specific heat C_V vs β (peak at β_c)
- Binder cumulant (for crossing point)

**Output:**
- Raw data: plaquette values, action values per sweep
- Analysis: ⟨P⟩(β), C_V(β), U(β) with jackknife errors
- Plots: phase diagram, finite-size scaling

### Phase 2: 2D Triangular Lattice

**Parameters:**
- Same as Phase 1 but triangular lattice
- Connects to T25 6-valent intertwiner work

**Key difference:**
- Plaquettes are triangles (3 links) not squares (4 links)
- Different β_c (universality class may differ)
- Tests geometric embedding from T25

### Phase 3: 3D Cubic Lattice

**Parameters:**
- Lattice sizes: L = 8, 12, 16, 20
- Couplings: K = 0.1 to 1.5, step 0.05
- Critical coupling: K_c ≈ 0.761

**Observables:**
- Average plaquette
- Specific heat (sharp peak at K_c)
- Wilson loops: W(r×r) for r = 1, 2, 4, 8
- String tension: from log W vs area (confined) or perimeter (deconfined)

**Confinement test:**
- K < K_c: area law W ~ exp(−σA), σ = string tension
- K > K_c: perimeter law W ~ exp(−μP)

## Design Decisions

### 1. Z₂ as Int8Array
- Memory efficient: 1 byte per link vs 8 for float64
- Fast: bitwise operations possible for bulk updates
- No floating point errors for ±1 values

### 2. Flat link indexing
- Links stored as flat array: `links[site * nDirections + dir]`
- Fast sequential access for sweeps
- No object overhead per link

### 3. Periodic boundary conditions
- Standard for finite-size scaling
- Implemented via modular arithmetic in neighbor lookups
- No ghost sites needed

### 4. Separation of concerns
- `ts-quantum`: physics (lattice, field, action, observables)
- `timesarrow`: simulation (parameters, sweeps, analysis, output)
- Enables reuse: same ts-quantum code for QHE-BHE or other LGT projects

## Performance Targets

- 2D L=64: ~10⁶ sweeps/hour on single core
- 3D L=16: ~10⁵ sweeps/hour on single core
- Memory: O(L^d) bytes (e.g., 3D L=32: 32³ × 6 links × 1 byte ≈ 200KB)

## Next Steps

1. Implement `ts-quantum/src/lattice/geometry.ts` (square lattice first)
2. Implement `Z2GaugeField` class
3. Implement action and Metropolis
4. Implement observables (plaquette, specific heat)
5. Write `timesarrow/numerics/src/scripts/t20-z2-lgt-phase1.ts`
6. Run parameter sweep and verify β_c ≈ 0.4407
7. Extend to triangular and 3D cubic

## References

- Paper: Section 4.2, Eq. (48)
- Kogut, J. B. (1979). An introduction to lattice gauge theory and spin systems. *Reviews of Modern Physics*, 51(4), 659.
- Balian, R., Drouffe, J. M., & Itzykson, C. (1975). Gauge fields on a lattice. II. Gauge-invariant Ising model. *Physical Review D*, 11(8), 2104.
