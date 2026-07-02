# Signed Volume Observable — Implementation Details

*Created: 2026-07-02*
*Task: T31*

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

## Future Work

1. **Finite-size scaling:** Run L = 8, 10, 12, 16 to extract critical exponents from |Q|/N
2. **Binder cumulant crossing:** U_L(β) for different L should cross at β_c
3. **Comparison with plaquette order parameter:** Does |Q|/N show sharper critical behavior than ⟨P⟩?
4. **Paper update:** Integrate this discussion into Section 4.3 (Z₂ effective action)
