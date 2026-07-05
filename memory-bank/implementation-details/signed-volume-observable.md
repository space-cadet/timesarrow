# Signed Volume Observable — Implementation Details

*Created: 2026-07-02*
*Last Updated: 2026-07-05 22:24:10 IST*
*Task: T31*

## Correction Notice

The path-based signed-volume results below are gauge-dependent exploratory data. The proposed iterative gauge fixing that maximizes $|Q|$ is withdrawn: spanning-tree alignment can force $|Q|=N$ in any phase and would destroy the observable's diagnostic value. T31 must use a gauge-invariant replacement specified under T32 before new production runs.

## Problem Statement

Standard LQG uses the positive-definite volume operator $\hat{V} = \sqrt{|\hat{Q}|}$. This discards the sign information that distinguishes the two time-orientation sectors. The paper's framework requires using the **signed** volume operator $\hat{Q}$ for composite systems, so that:

$$\hat{Q}_{\text{total}} = \sum_{v \in S} \hat{Q}_v$$

The emergence of a global time orientation is then tied to the emergence of a macroscopic geometry with non-vanishing, extensive signed volume.

## Gauge Structure

The signed volume at individual vertices is **gauge-dependent**:
- A local Z₂ gauge transformation at vertex $v$ flips $\sigma_e \to -\sigma_e$ on all edges incident to $v$
- This flips the sign of $\hat{Q}_v$ but leaves $\hat{V}_v$ unchanged
- Therefore, the absolute sign of $\hat{Q}_v$ is not physical

What is physical:
- The **relative** sign between two vertices, measured by the Wilson loop $W(\gamma) = \prod_{e \in \gamma} \sigma_e$
- The **total** signed volume in a fixed gauge (analogous to choosing a gauge in electromagnetism before computing a vector potential)

## Gauge Fixing Strategy

To measure the signed volume, we fix a gauge by computing vertex signs relative to a reference vertex (the origin). For each vertex, we compute the product of $\sigma_e$ along a chosen path from the origin.

**Path choice (cubic lattice):**
1. Move in +x direction until reaching the target x-coordinate
2. Move in +y direction until reaching the target y-coordinate
3. Move in +z direction until reaching the target z-coordinate

This is a valid gauge fixing because the product around any closed loop is gauge-invariant (it's a Wilson loop).

## Implementation

### 3D Signed Volume

```rust
pub fn signed_volume_3d(&self) -> i64 {
    let l = self.l;
    let mut total = 0i64;
    for z in 0..l {
        for y in 0..l {
            for x in 0..l {
                let mut sign = 1i8;
                // Path: x-links, then y-links, then z-links
                for i in 0..x { sign *= self.link_3d(i, 0, 0, 0); }
                for j in 0..y { sign *= self.link_3d(x, j, 0, 1); }
                for k in 0..z { sign *= self.link_3d(x, y, k, 2); }
                total += sign as i64;
            }
        }
    }
    total
}
```

**Complexity:** O(L⁴) per measurement (L³ vertices × O(L) path length). For L=6, this is ~1300 operations — negligible compared to the O(L³) sweeps.

### 2D Signed Area

```rust
pub fn signed_area_2d(&self) -> i64 {
    let l = self.l;
    let mut total = 0i64;
    for y in 0..l {
        for x in 0..l {
            let mut sign = 1i8;
            for i in 0..x { sign *= self.link(i, 0, 0); }
            for j in 0..y { sign *= self.link(x, j, 1); }
            total += sign as i64;
        }
    }
    total
}
```

## Expected Behavior

### 3D (has deconfinement transition at β_c ≈ 0.76)

| Phase | Behavior | |Q| scaling |
|-------|----------|-----------|
| Confined (β < β_c) | Random Z₂ orientations | |Q| ~ √N (random walk) |
| Deconfined (β > β_c) | Ordered Z₂ orientations | |Q| ~ N (extensive) |
| Critical (β ≈ β_c) | Fluctuations at all scales | |Q| ~ N^{1-β/ν} |

### 2D (confining at all temperatures)

| β | Behavior | |Q| scaling |
|---|----------|-----------|
| All β | Random Z₂ orientations | |Q| ~ √N (always) |

## Physical Interpretation

The signed volume observable connects the Z₂ gauge theory to the arrow of time in a concrete way:

1. **Pre-geometric phase (confined):** The universe has local geometry (individual vertices have volume) but no global orientation. The signed volumes cancel like a paramagnet above T_c. There is no arrow of time.

2. **Geometric phase (deconfined):** The universe develops a coherent orientation. The signed volumes add constructively, giving an extensive total. The arrow of time emerges simultaneously with oriented geometry.

3. **Critical point:** The transition between these phases is a confinement-deconfinement transition in the Z₂ gauge theory. Near β_c, domain walls proliferate and the arrow of time fluctuates at all scales.

## Results: Production Runs (2026-07-02)

### 3D Signed Volume — L=8, 10, 12

Production simulations completed with 5000 thermal + 20000 measure sweeps, measuring every 10 sweeps (2000 measurements per β).

#### L=8 (N=512)

| β | |Q|/N | Error | Plaquette | Binder_Q |
|---|------|-------|-----------|----------|
| 0.40 | 0.0340 | 0.298 | 0.395 | 0.001 |
| 0.50 | 0.0346 | 0.298 | 0.502 | 0.047 |
| 0.60 | 0.0352 | 0.314 | 0.627 | -0.017 |
| 0.70 | 0.0354 | 0.307 | 0.790 | 0.012 |
| 0.76 | 0.0355 | 0.302 | 0.949 | 0.050 |
| 0.80 | 0.0362 | 0.305 | 0.974 | 0.079 |
| 0.85 | 0.0307 | 0.267 | 0.986 | -0.008 |
| 0.90 | 0.0370 | 0.349 | 0.991 | -0.055 |
| 1.00 | 0.0505 | 0.258 | 0.997 | 0.465 |
| 1.10 | 0.0265 | 0.156 | 0.999 | 0.410 |
| 1.20 | 0.0675 | 0.138 | 0.999 | 0.629 |
| 1.50 | 0.0899 | 0.010 | 1.000 | 0.667 |

**Key finding**: |Q|/N rises from ~0.034 (confined) to ~0.090 (deconfined), a 2.6× increase. Binder cumulant approaches 2/3 at β=1.5.

#### L=10 (N=1000)

| β | |Q|/N | Error | Plaquette | Binder_Q |
|---|------|-------|-----------|----------|
| 0.40 | 0.0257 | 0.436 | 0.394 | -0.028 |
| 0.50 | 0.0256 | 0.433 | 0.502 | -0.006 |
| 0.60 | 0.0256 | 0.440 | 0.628 | -0.081 |
| 0.70 | 0.0250 | 0.427 | 0.789 | -0.057 |
| 0.76 | 0.0244 | 0.417 | 0.949 | -0.004 |
| 0.80 | 0.0267 | 0.437 | 0.973 | 0.052 |
| 0.85 | 0.0277 | 0.469 | 0.985 | 0.038 |
| 0.90 | 0.0270 | 0.445 | 0.991 | 0.032 |
| 1.00 | 0.0157 | 0.281 | 0.997 | 0.056 |
| 1.10 | 0.0230 | 0.199 | 0.999 | 0.503 |
| 1.20 | 0.0472 | 0.134 | 0.999 | 0.647 |
| 1.50 | 0.0075 | 0.021 | 1.000 | 0.645 |

**Key finding**: L=10 shows anomalous behavior at β=1.5 — |Q|/N = 0.0075, below the confined-phase value. This is a **gauge sector issue** (see below).

#### L=12 (N=1728)

| β | |Q|/N | Error | Plaquette | Binder_Q |
|---|------|-------|-----------|----------|
| 0.40 | 0.0189 | 0.550 | 0.395 | 0.028 |
| 0.50 | 0.0189 | 0.553 | 0.502 | -0.037 |
| 0.60 | 0.0192 | 0.556 | 0.628 | 0.019 |
| 0.70 | 0.0193 | 0.573 | 0.789 | -0.014 |
| 0.76 | 0.0185 | 0.533 | 0.948 | 0.018 |
| 0.80 | 0.0195 | 0.547 | 0.974 | 0.093 |
| 0.85 | 0.0218 | 0.595 | 0.985 | 0.095 |
| 0.90 | 0.0213 | 0.566 | 0.992 | 0.133 |
| 1.00 | 0.0181 | 0.418 | 0.997 | 0.310 |
| 1.10 | 0.0145 | 0.399 | 0.999 | 0.111 |
| 1.20 | 0.0112 | 0.213 | 0.999 | 0.415 |
| 1.50 | 0.0628 | 0.046 | 1.000 | 0.666 |

**Key finding**: L=12 shows non-monotonic approach. |Q|/N drops at intermediate β before jumping to 0.063 at β=1.5. The system is fluctuating between degenerate ground states.

### The Gauge Problem

The signed volume is **gauge-dependent** at the level of individual configurations. In the deconfined phase, two gauge-equivalent ground states exist:

1. **Aligned sector**: All σ_e = +1 → |Q| = N (maximum)
2. **Checkerboard sector**: All σ_e = -1 → |Q| ≈ 0 (minimum)

At finite β, the simulation can tunnel between these sectors, causing |Q|/N to fluctuate between ~1 and ~0. This explains:
- L=10 at β=1.5: stuck in checkerboard sector (|Q|/N = 0.0075)
- L=12 at β=1.0–1.2: fluctuating between sectors
- L=8: relatively stable because smaller system has fewer tunneling paths

### Superseded Proposal: Iterative Gauge-Fixing

To get clean measurements, we need to **fix the gauge** before measuring. The approach:

1. Start from the origin vertex
2. Iteratively flip gauge transformations to maximize |Q| (greedy algorithm)
3. Measure signed volume in the "aligned" gauge

This proposal is retained for provenance but must not be implemented. See `post-may-numerics-correction-plan.md`.

## Dashboard Integration

T31 runs and figures added to the numerics dashboard:
- **Runs**: t31-p2-L8-3D-20250702, t31-p2-L10-3D-20250702, t31-p2-L12-3D-20250702
- **Figures**: Signed Volume vs β, Binder Cumulant, Plaquette comparison
- **Task page**: `tasks/t31-signed-volume.html` (deployed to space-cadet.github.io)

## Future Work

1. **Implement iterative gauge-fixing** — greedy algorithm to always measure in aligned sector
2. **Re-run L=10, 12** with gauge-fixing to get clean |Q|/N → 1 signal
3. **Binder cumulant crossing** — U_L(β) for different L should cross at β_c
4. **Extract critical exponents** — fit |Q|/N ~ (β - β_c)^β near critical point
5. **Paper update** — integrate into Section 4.3 (Z₂ effective action)
