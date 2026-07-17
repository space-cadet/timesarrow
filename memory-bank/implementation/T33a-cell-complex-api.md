# T33a Implementation: General 4-Valent 3D Cell-Complex API

*Created: 2026-07-17*
*Status: ✅ COMPLETE*

## What Was Built

### `rust-lattice/src/cell_complex.rs`

A new module providing a physics-agnostic, ground-truth-oriented API for 3D cell complexes with boundary operators over ℤ₂.

#### Core Types

| Type | Purpose |
|------|---------|
| `SparseBoolMatrix` | CSR sparse matrix over ℤ₂ (entries implicitly 1) |
| `CellComplex` | Oriented 3D cell complex with ∂₁, ∂₂, ∂₃ |
| `Homology` | Computed ranks H₀, H₁, H₂, H₃ |
| `ValidationResult` | Ground-truth check results |

#### Key Methods

- `SparseBoolMatrix::from_dense()` — construct from boolean matrix
- `SparseBoolMatrix::matmul()` — matrix multiplication over ℤ₂
- `SparseBoolMatrix::rank_z2()` — Gaussian elimination over GF(2)
- `CellComplex::check_plaquette_closure()` — verify ∂₁∂₂ = 0
- `CellComplex::check_bianchi_identity()` — verify ∂₂∂₃ = 0
- `CellComplex::compute_homology()` — compute H₀, H₁, H₂, H₃
- `CellComplex::validate()` — run all checks

#### Diamond Lattice Generator

```rust
pub fn diamond_lattice(l: usize) -> (CellComplex, Vec<(usize, usize, usize)>)
```

Generates a diamond lattice with L×L×L unit cells and periodic boundary conditions:
- Vertices: all integer coords (x,y,z) with 0 ≤ x,y,z < 2L
- Sublattice A: x+y+z even, Sublattice B: x+y+z odd
- Edges: 4 neighbors at (±1,±1,±1) with odd number of minus signs
- Plaquettes: hexagonal 6-cycles found by brute-force enumeration

### Design Decisions

1. **Sparse CSR format**: Efficient for boundary operators which are typically very sparse
2. **Brute-force plaquette enumeration**: For the diamond lattice, hexagons are found by checking all pairs of neighbors at each vertex. Deduplicated via canonical edge sorting.
3. **No 3-cells yet**: The generator creates ∂₃ as empty. For periodic BC, H₃ should be 1 (3-torus), but computing 3-cells for the diamond lattice is non-trivial and deferred.
4. **Ground-truth validation**: Every cell complex can be checked for plaquette closure and Bianchi identity. Homology provides topological sanity check.

### Test Results

All 11 tests pass:
- `test_sparse_matrix_basic` — CSR construction
- `test_sparse_matvec` — ℤ₂ matrix-vector product
- `test_sparse_matmul` — ℤ₂ matrix multiplication
- `test_sparse_transpose` — matrix transpose
- `test_sparse_rank` — Gaussian elimination rank
- `test_cubic_lattice_cell_complex` — single cube (contractible)
- `test_homology_single_edge` — interval [0,1]
- `test_homology_circle` — S¹ (H₁=1)
- `test_homology_3torus` — T³ (H=(1,3,3,1))
- `test_homology_contractible_cube` — B³ (H=(1,0,0,0))
- `test_diamond_lattice_l1` — 8 vertices, degenerate (no plaquettes)
- `test_diamond_lattice_l2` — 64 vertices, 128 edges, 64 plaquettes, χ=0

### Verified Topological Invariants

| Complex | V | E | P | C | χ | H₀ | H₁ | H₂ | H₃ |
|---------|---|---|---|---|---|----|----|----|----|
| Single edge | 2 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| Circle S¹ | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 3-Torus T³ | 1 | 3 | 3 | 1 | 0 | 1 | 3 | 3 | 1 |
| Contractible cube B³ | 8 | 12 | 6 | 1 | 1 | 1 | 0 | 0 | 0 |
| Diamond L=2 (periodic) | 64 | 128 | 64 | 0 | 0 | — | — | — | — |

### Integration

The module is exported in `lib.rs`:
```rust
pub mod cell_complex;
```

Users can:
1. Construct arbitrary cell complexes via `CellComplex::new(d1, d2, d3)`
2. Generate diamond lattices via `cell_complex::diamond_lattice(l)`
3. Validate complexes via `.validate()`
4. Use `SparseBoolMatrix` for general ℤ₂ linear algebra

### Future Work (T33b/T34)

- Add 3-cell enumeration for diamond lattice (needed for full homology)
- Implement gauge field on general cell complex (Z₂ links on edges)
- Add Metropolis sweeps for non-Cartesian plaquettes
- Port to TypeScript for ts-quantum integration

## Files Modified

- `rust-lattice/src/cell_complex.rs` — New module (800+ lines)
- `rust-lattice/src/lib.rs` — Added `pub mod cell_complex`

## References

- Task: `memory-bank/tasks/T33a.md`
- This doc: `memory-bank/implementation/T33a-cell-complex-api.md`
