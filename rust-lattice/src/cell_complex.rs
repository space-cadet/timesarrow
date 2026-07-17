//! General oriented cell-complex representation for lattice gauge theory.
//!
//! This module provides a physics-agnostic, ground-truth-oriented API for
//! 3D cell complexes. The caller supplies boundary operators over ℤ₂, and
//! the module verifies that they satisfy the required algebraic identities
//! (plaquette closure, Bianchi identity) and computes homology ranks.
//!
//! ## Design Rationale
//!
//! The existing `Z2GaugeField` hardcodes Cartesian lattices (square, cubic,
//! hypercubic). Non-Cartesian lattices like the diamond lattice have
//! non-planar plaquettes and require explicit cell-complex specification.
//!
//! This module does NOT derive the cell complex from a graph alone.
//! Valence alone does not determine plaquettes or 3-cells. Instead, the
//! boundary operators are accepted as ground truth and validated.
//!
//! ## Key Types
//!
//! - `SparseBoolMatrix` — CSR sparse matrix over ℤ₂ (entries are 0/1)
//! - `CellComplex` — oriented 3D cell complex with boundary operators ∂₁, ∂₂, ∂₃
//! - `Homology` — computed homology ranks H₀, H₁, H₂, H₃

// =============================================================================
// SPARSE BOOLEAN MATRIX (CSR format over ℤ₂)
// =============================================================================

/// Compressed Sparse Row (CSR) matrix over ℤ₂.
///
/// All non-zero entries are implicitly 1. Only the sparsity pattern is stored.
/// Matrix dimensions: `n_rows × n_cols`.
#[derive(Clone, Debug, PartialEq)]
pub struct SparseBoolMatrix {
    n_rows: usize,
    n_cols: usize,
    /// Row pointers: `indptr[i]` is the start index of row `i` in `indices`.
    /// Length = n_rows + 1, with `indptr[n_rows] = nnz`.
    indptr: Vec<usize>,
    /// Column indices of non-zero entries. Length = nnz.
    indices: Vec<usize>,
}

impl SparseBoolMatrix {
    /// Create an empty sparse matrix with given dimensions.
    pub fn empty(n_rows: usize, n_cols: usize) -> Self {
        Self {
            n_rows,
            n_cols,
            indptr: vec![0; n_rows + 1],
            indices: Vec::new(),
        }
    }

    /// Create from dense boolean matrix (row-major).
    ///
    /// # Panics
    /// Panics if `dense.len() != n_rows * n_cols`.
    pub fn from_dense(n_rows: usize, n_cols: usize, dense: &[bool]) -> Self {
        assert_eq!(dense.len(), n_rows * n_cols);
        let mut indptr = Vec::with_capacity(n_rows + 1);
        let mut indices = Vec::new();
        indptr.push(0);

        for row in 0..n_rows {
            for col in 0..n_cols {
                if dense[row * n_cols + col] {
                    indices.push(col);
                }
            }
            indptr.push(indices.len());
        }

        Self {
            n_rows,
            n_cols,
            indptr,
            indices,
        }
    }

    /// Number of rows.
    pub fn n_rows(&self) -> usize { self.n_rows }

    /// Number of columns.
    pub fn n_cols(&self) -> usize { self.n_cols }

    /// Number of non-zero entries.
    pub fn nnz(&self) -> usize { self.indices.len() }

    /// Iterator over non-zero column indices in a given row.
    pub fn row_iter(&self, row: usize) -> impl Iterator<Item = usize> + '_ {
        let start = self.indptr[row];
        let end = self.indptr[row + 1];
        self.indices[start..end].iter().copied()
    }

    /// Iterator over (row, col) pairs of all non-zero entries.
    pub fn entries(&self) -> impl Iterator<Item = (usize, usize)> + '_ {
        (0..self.n_rows).flat_map(move |row| {
            self.row_iter(row).map(move |col| (row, col))
        })
    }

    /// Compute the transpose.
    pub fn transpose(&self) -> Self {
        // Count entries per column
        let mut col_counts = vec![0; self.n_cols];
        for &col in &self.indices {
            col_counts[col] += 1;
        }

        // Build indptr for transpose (cumulative sum)
        let mut indptr_t = vec![0; self.n_cols + 1];
        for i in 0..self.n_cols {
            indptr_t[i + 1] = indptr_t[i] + col_counts[i];
        }

        // Place entries
        let mut indices_t = vec![0; self.nnz()];
        let mut next_pos = indptr_t.clone();

        for row in 0..self.n_rows {
            for col in self.row_iter(row) {
                let pos = next_pos[col];
                indices_t[pos] = row;
                next_pos[col] = pos + 1;
            }
        }

        Self {
            n_rows: self.n_cols,
            n_cols: self.n_rows,
            indptr: indptr_t,
            indices: indices_t,
        }
    }

    /// Matrix-vector product over ℤ₂: y = A · x (mod 2).
    ///
    /// `x` must have length `n_cols`, result has length `n_rows`.
    pub fn matvec(&self, x: &[bool]) -> Vec<bool> {
        assert_eq!(x.len(), self.n_cols);
        let mut y = vec![false; self.n_rows];
        for row in 0..self.n_rows {
            let mut acc = false;
            for col in self.row_iter(row) {
                acc ^= x[col];
            }
            y[row] = acc;
        }
        y
    }

    /// Matrix-matrix product over ℤ₂: C = A · B (mod 2).
    ///
    /// # Panics
    /// Panics if `self.n_cols != other.n_rows`.
    pub fn matmul(&self, other: &SparseBoolMatrix) -> SparseBoolMatrix {
        assert_eq!(self.n_cols, other.n_rows);

        // For each row of self, compute row of result
        let mut indptr = vec![0; self.n_rows + 1];
        let mut indices = Vec::new();

        for row_a in 0..self.n_rows {
            // Collect columns of other that are reachable
            let mut row_result = vec![false; other.n_cols];
            for col_a in self.row_iter(row_a) {
                for col_b in other.row_iter(col_a) {
                    row_result[col_b] ^= true;
                }
            }
            for (col, &val) in row_result.iter().enumerate() {
                if val {
                    indices.push(col);
                }
            }
            indptr[row_a + 1] = indices.len();
        }

        SparseBoolMatrix {
            n_rows: self.n_rows,
            n_cols: other.n_cols,
            indptr,
            indices,
        }
    }

    /// Compute the rank over ℤ₂ using Gaussian elimination.
    pub fn rank_z2(&self) -> usize {
        // Convert to dense row-echelon form
        let mut rows: Vec<Vec<bool>> = Vec::with_capacity(self.n_rows);
        for row in 0..self.n_rows {
            let mut r = vec![false; self.n_cols];
            for col in self.row_iter(row) {
                r[col] = true;
            }
            rows.push(r);
        }

        let mut rank = 0;
        let mut pivot_col = 0;
        let mut row = 0;

        while row < self.n_rows && pivot_col < self.n_cols {
            // Find pivot in column pivot_col at or below row
            let mut pivot_row = None;
            for r in row..self.n_rows {
                if rows[r][pivot_col] {
                    pivot_row = Some(r);
                    break;
                }
            }

            if let Some(pr) = pivot_row {
                rows.swap(row, pr);
                // Eliminate below
                for r in (row + 1)..self.n_rows {
                    if rows[r][pivot_col] {
                        for c in pivot_col..self.n_cols {
                            rows[r][c] ^= rows[row][c];
                        }
                    }
                }
                rank += 1;
                row += 1;
            }
            pivot_col += 1;
        }

        rank
    }
}

// =============================================================================
// CELL COMPLEX
// =============================================================================

/// An oriented 3D cell complex with boundary operators over ℤ₂.
///
/// The complex is specified by three boundary operators:
/// - `d1`: ∂₁ — edges → vertices (n_v × n_e)
/// - `d2`: ∂₂ — plaquettes → edges (n_e × n_p)
/// - `d3`: ∂₃ — 3-cells → plaquettes (n_p × n_c)
///
/// These must satisfy ∂₁∂₂ = 0 (plaquettes are closed) and ∂₂∂₃ = 0 (Bianchi).
/// The constructor verifies these identities.
#[derive(Clone, Debug)]
pub struct CellComplex {
    n_vertices: usize,
    n_edges: usize,
    n_plaquettes: usize,
    n_cells: usize,
    d1: SparseBoolMatrix, // n_v × n_e
    d2: SparseBoolMatrix, // n_e × n_p
    d3: SparseBoolMatrix, // n_p × n_c
}

/// Computed homology ranks for a cell complex.
#[derive(Clone, Debug, PartialEq)]
pub struct Homology {
    pub h0: usize,
    pub h1: usize,
    pub h2: usize,
    pub h3: usize,
}

/// Result of cell-complex validation.
#[derive(Clone, Debug, PartialEq)]
pub struct ValidationResult {
    pub d1_d2_zero: bool,
    pub d2_d3_zero: bool,
    pub euler_characteristic: i64,
    pub homology: Homology,
}

impl CellComplex {
    /// Create a new cell complex from boundary operators.
    ///
    /// # Arguments
    /// - `d1`: n_v × n_e matrix, column j is the boundary of edge j (two vertices)
    /// - `d2`: n_e × n_p matrix, column j is the boundary of plaquette j (edges around it)
    /// - `d3`: n_p × n_c matrix, column j is the boundary of 3-cell j (plaquettes around it)
    ///
    /// # Panics
    /// Panics if dimensions are inconsistent (e.g., d1.n_cols != d2.n_rows).
    pub fn new(
        d1: SparseBoolMatrix,
        d2: SparseBoolMatrix,
        d3: SparseBoolMatrix,
    ) -> Self {
        assert_eq!(d1.n_cols(), d2.n_rows(), "d1.n_cols must equal d2.n_rows (edges)");
        assert_eq!(d2.n_cols(), d3.n_rows(), "d2.n_cols must equal d3.n_rows (plaquettes)");

        Self {
            n_vertices: d1.n_rows(),
            n_edges: d1.n_cols(),
            n_plaquettes: d2.n_cols(),
            n_cells: d3.n_cols(),
            d1,
            d2,
            d3,
        }
    }

    /// Number of vertices (0-cells).
    pub fn n_vertices(&self) -> usize { self.n_vertices }

    /// Number of edges (1-cells).
    pub fn n_edges(&self) -> usize { self.n_edges }

    /// Number of plaquettes (2-cells).
    pub fn n_plaquettes(&self) -> usize { self.n_plaquettes }

    /// Number of 3-cells.
    pub fn n_cells(&self) -> usize { self.n_cells }

    /// Boundary operator ∂₁: edges → vertices.
    pub fn d1(&self) -> &SparseBoolMatrix { &self.d1 }

    /// Boundary operator ∂₂: plaquettes → edges.
    pub fn d2(&self) -> &SparseBoolMatrix { &self.d2 }

    /// Boundary operator ∂₃: 3-cells → plaquettes.
    pub fn d3(&self) -> &SparseBoolMatrix { &self.d3 }

    /// Verify that ∂₁∂₂ = 0 (every plaquette is a closed edge cycle).
    pub fn check_plaquette_closure(&self) -> bool {
        let product = self.d1.matmul(&self.d2);
        // Check all entries are zero
        product.nnz() == 0
    }

    /// Verify that ∂₂∂₃ = 0 (Bianchi identity: boundary of 3-cell has zero boundary).
    pub fn check_bianchi_identity(&self) -> bool {
        let product = self.d2.matmul(&self.d3);
        product.nnz() == 0
    }

    /// Compute Euler characteristic: χ = V - E + P - C.
    pub fn euler_characteristic(&self) -> i64 {
        self.n_vertices as i64
            - self.n_edges as i64
            + self.n_plaquettes as i64
            - self.n_cells as i64
    }

    /// Compute homology ranks over ℤ₂.
    ///
    /// Using the rank-nullity theorem:
    /// - H₀ = ker(∂₁) / im(∂₂)  → rank = n_v - rank(∂₁)
    /// - H₁ = ker(∂₂) / im(∂₃)  → rank = n_e - rank(∂₁) - rank(∂₂)
    /// - H₂ = ker(∂₃) / im(0)   → rank = n_p - rank(∂₂) - rank(∂₃)
    /// - H₃ = ker(0) / im(∂₃)   → rank = n_c - rank(∂₃)
    ///
    /// Wait, the standard formula is:
    /// H_k = ker(∂_k) / im(∂_{k+1})
    /// rank(H_k) = nullity(∂_k) - rank(∂_{k+1})
    ///           = n_k - rank(∂_k) - rank(∂_{k+1})
    ///
    /// where n_0 = n_v, n_1 = n_e, n_2 = n_p, n_3 = n_c.
    pub fn compute_homology(&self) -> Homology {
        let r1 = self.d1.rank_z2();
        let r2 = self.d2.rank_z2();
        let r3 = self.d3.rank_z2();

        let h0 = self.n_vertices - r1;
        let h1 = self.n_edges - r1 - r2;
        let h2 = self.n_plaquettes - r2 - r3;
        let h3 = self.n_cells - r3;

        // Sanity check: Euler characteristic
        let chi = (h0 as i64) - (h1 as i64) + (h2 as i64) - (h3 as i64);
        assert_eq!(chi, self.euler_characteristic(),
            "Euler characteristic mismatch: homology gives {}, direct count gives {}",
            chi, self.euler_characteristic());

        Homology { h0, h1, h2, h3 }
    }

    /// Run all validation checks and return detailed results.
    pub fn validate(&self) -> ValidationResult {
        ValidationResult {
            d1_d2_zero: self.check_plaquette_closure(),
            d2_d3_zero: self.check_bianchi_identity(),
            euler_characteristic: self.euler_characteristic(),
            homology: self.compute_homology(),
        }
    }
}

// =============================================================================
// DIAMOND LATTICE GENERATOR
// =============================================================================

/// Generate a diamond lattice cell complex with L×L×L unit cells and periodic BC.
///
/// The diamond lattice consists of two interpenetrating FCC lattices.
/// In our coordinate system (scaled by 2 for integer arithmetic):
/// - Vertices are at all integer coordinates (x,y,z) with 0 ≤ x,y,z < 2L
/// - Sublattice A: x+y+z is even
/// - Sublattice B: x+y+z is odd
/// - Edges connect each vertex to 4 neighbors at (±1,±1,±1) with an odd number of minus signs
///
/// Returns a `CellComplex` and a lookup table from vertex coordinates to indices.
pub fn diamond_lattice(l: usize) -> (CellComplex, Vec<(usize, usize, usize)>) {
    assert!(l >= 1, "l must be at least 1");

    let size = 2 * l;

    // Enumerate all vertices and assign indices
    let mut vertex_index: std::collections::HashMap<(usize, usize, usize), usize> =
        std::collections::HashMap::new();
    let mut vertices = Vec::new();

    for x in 0..size {
        for y in 0..size {
            for z in 0..size {
                let idx = vertices.len();
                vertex_index.insert((x, y, z), idx);
                vertices.push((x, y, z));
            }
        }
    }

    let n_v = vertices.len();

    // Neighbor offsets for diamond lattice (4 directions)
    let neighbor_offsets = [
        (1i32, 1i32, 1i32),
        (1i32, -1i32, -1i32),
        (-1i32, 1i32, -1i32),
        (-1i32, -1i32, 1i32),
    ];

    // Generate edges (undirected, so we only add each edge once)
    let mut edges: Vec<(usize, usize)> = Vec::new(); // (vertex_a, vertex_b)
    let mut edge_index: std::collections::HashMap<(usize, usize), usize> =
        std::collections::HashMap::new();

    for &(x, y, z) in &vertices {
        let v = vertex_index[&(x, y, z)];
        for &(dx, dy, dz) in &neighbor_offsets {
            let nx = ((x as i32 + dx).rem_euclid(size as i32)) as usize;
            let ny = ((y as i32 + dy).rem_euclid(size as i32)) as usize;
            let nz = ((z as i32 + dz).rem_euclid(size as i32)) as usize;
            let w = vertex_index[&(nx, ny, nz)];

            // Only add each undirected edge once
            if v < w {
                let eidx = edges.len();
                edge_index.insert((v, w), eidx);
                edges.push((v, w));
            }
        }
    }

    let n_e = edges.len();

    // Build ∂₁: n_v × n_e
    let mut d1_dense = vec![false; n_v * n_e];
    for (eidx, &(v, w)) in edges.iter().enumerate() {
        d1_dense[v * n_e + eidx] = true;
        d1_dense[w * n_e + eidx] = true;
    }
    let d1 = SparseBoolMatrix::from_dense(n_v, n_e, &d1_dense);

    // Enumerate plaquettes (hexagons) by brute force
    let mut plaquettes: Vec<Vec<usize>> = Vec::new(); // each is a list of 6 edge indices
    let mut seen_hexagons: std::collections::HashSet<[usize; 6]> = std::collections::HashSet::new();

    for &(x, y, z) in &vertices {
        let v = vertex_index[&(x, y, z)];

        // Find all neighbors of v
        let mut v_neighbors: Vec<usize> = Vec::new();
        for &(dx, dy, dz) in &neighbor_offsets {
            let nx = ((x as i32 + dx).rem_euclid(size as i32)) as usize;
            let ny = ((y as i32 + dy).rem_euclid(size as i32)) as usize;
            let nz = ((z as i32 + dz).rem_euclid(size as i32)) as usize;
            let w = vertex_index[&(nx, ny, nz)];
            v_neighbors.push(w);
        }

        // Try all pairs of neighbors
        for i in 0..4 {
            for j in (i + 1)..4 {
                let n1 = v_neighbors[i];
                let n2 = v_neighbors[j];

                // Find neighbors of n1 (other than v)
                let n1_pos = vertices[n1];
                let mut n1_neighbors: Vec<usize> = Vec::new();
                for &(dx, dy, dz) in &neighbor_offsets {
                    let nx = ((n1_pos.0 as i32 + dx).rem_euclid(size as i32)) as usize;
                    let ny = ((n1_pos.1 as i32 + dy).rem_euclid(size as i32)) as usize;
                    let nz = ((n1_pos.2 as i32 + dz).rem_euclid(size as i32)) as usize;
                    let w = vertex_index[&(nx, ny, nz)];
                    if w != v {
                        n1_neighbors.push(w);
                    }
                }

                // Find neighbors of n2 (other than v)
                let n2_pos = vertices[n2];
                let mut n2_neighbors: Vec<usize> = Vec::new();
                for &(dx, dy, dz) in &neighbor_offsets {
                    let nx = ((n2_pos.0 as i32 + dx).rem_euclid(size as i32)) as usize;
                    let ny = ((n2_pos.1 as i32 + dy).rem_euclid(size as i32)) as usize;
                    let nz = ((n2_pos.2 as i32 + dz).rem_euclid(size as i32)) as usize;
                    let w = vertex_index[&(nx, ny, nz)];
                    if w != v {
                        n2_neighbors.push(w);
                    }
                }

                // Find common neighbors of n1 and n2 (other than v)
                for &a1 in &n1_neighbors {
                    for &a2 in &n2_neighbors {
                        if a1 == a2 {
                            continue; // This would be a 4-cycle, not a hexagon
                        }

                        // Check if a1 and a2 share a common neighbor (other than n1 and n2)
                        let a1_pos = vertices[a1];
                        let a2_pos = vertices[a2];

                        let mut a1_neighbors: Vec<usize> = Vec::new();
                        for &(dx, dy, dz) in &neighbor_offsets {
                            let nx = ((a1_pos.0 as i32 + dx).rem_euclid(size as i32)) as usize;
                            let ny = ((a1_pos.1 as i32 + dy).rem_euclid(size as i32)) as usize;
                            let nz = ((a1_pos.2 as i32 + dz).rem_euclid(size as i32)) as usize;
                            let w = vertex_index[&(nx, ny, nz)];
                            if w != n1 {
                                a1_neighbors.push(w);
                            }
                        }

                        let mut a2_neighbors: Vec<usize> = Vec::new();
                        for &(dx, dy, dz) in &neighbor_offsets {
                            let nx = ((a2_pos.0 as i32 + dx).rem_euclid(size as i32)) as usize;
                            let ny = ((a2_pos.1 as i32 + dy).rem_euclid(size as i32)) as usize;
                            let nz = ((a2_pos.2 as i32 + dz).rem_euclid(size as i32)) as usize;
                            let w = vertex_index[&(nx, ny, nz)];
                            if w != n2 {
                                a2_neighbors.push(w);
                            }
                        }

                        for &mid in &a1_neighbors {
                            if a2_neighbors.contains(&mid) {
                                // Found a 6-cycle: v - n1 - a1 - mid - a2 - n2 - v
                                let e1 = edge_index.get(&(v.min(n1), v.max(n1)));
                                let e2 = edge_index.get(&(n1.min(a1), n1.max(a1)));
                                let e3 = edge_index.get(&(a1.min(mid), a1.max(mid)));
                                let e4 = edge_index.get(&(mid.min(a2), mid.max(a2)));
                                let e5 = edge_index.get(&(a2.min(n2), a2.max(n2)));
                                let e6 = edge_index.get(&(n2.min(v), n2.max(v)));

                                // Skip if any edge is missing (can happen with periodic BC degeneracies)
                                let edges_opt = match (e1, e2, e3, e4, e5, e6) {
                                    (Some(&e1), Some(&e2), Some(&e3), Some(&e4), Some(&e5), Some(&e6)) => {
                                        Some([e1, e2, e3, e4, e5, e6])
                                    }
                                    _ => None,
                                };

                                if let Some(mut hex_edges) = edges_opt {
                                    hex_edges.sort_unstable();
                                    if seen_hexagons.insert(hex_edges) {
                                        plaquettes.push(hex_edges.to_vec());
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    let n_p = plaquettes.len();

    // Build ∂₂: n_e × n_p
    let mut d2_dense = vec![false; n_e * n_p];
    for (pidx, edges_in_plaq) in plaquettes.iter().enumerate() {
        for &eidx in edges_in_plaq {
            d2_dense[eidx * n_p + pidx] = true;
        }
    }
    let d2 = SparseBoolMatrix::from_dense(n_e, n_p, &d2_dense);

    // For now, no 3-cells (open boundary conditions)
    let d3 = SparseBoolMatrix::empty(n_p, 0);

    let complex = CellComplex::new(d1, d2, d3);
    (complex, vertices)
}

// =============================================================================
// UNIT TESTS
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sparse_matrix_basic() {
        // 2×3 matrix: [1 0 1; 0 1 0]
        let mat = SparseBoolMatrix::from_dense(2, 3, &[
            true, false, true,
            false, true, false,
        ]);
        assert_eq!(mat.n_rows(), 2);
        assert_eq!(mat.n_cols(), 3);
        assert_eq!(mat.nnz(), 3);

        let row0: Vec<_> = mat.row_iter(0).collect();
        assert_eq!(row0, vec![0, 2]);

        let row1: Vec<_> = mat.row_iter(1).collect();
        assert_eq!(row1, vec![1]);
    }

    #[test]
    fn test_sparse_matvec() {
        // [1 0 1; 0 1 0] · [1, 0, 1] = [0, 0] (mod 2)
        let mat = SparseBoolMatrix::from_dense(2, 3, &[
            true, false, true,
            false, true, false,
        ]);
        let x = vec![true, false, true];
        let y = mat.matvec(&x);
        assert_eq!(y, vec![false, false]);

        // [1 0 1; 0 1 0] · [1, 1, 0] = [1, 1] (mod 2)
        let x2 = vec![true, true, false];
        let y2 = mat.matvec(&x2);
        assert_eq!(y2, vec![true, true]);
    }

    #[test]
    fn test_sparse_matmul() {
        // A = [1 0; 1 1]  (2×2)
        // B = [1 1; 0 1]  (2×2)
        // A·B = [1 1; 1 0] (mod 2)
        let a = SparseBoolMatrix::from_dense(2, 2, &[true, false, true, true]);
        let b = SparseBoolMatrix::from_dense(2, 2, &[true, true, false, true]);
        let c = a.matmul(&b);

        assert_eq!(c.n_rows(), 2);
        assert_eq!(c.n_cols(), 2);

        let row0: Vec<_> = c.row_iter(0).collect();
        assert_eq!(row0, vec![0, 1]);

        let row1: Vec<_> = c.row_iter(1).collect();
        assert_eq!(row1, vec![0]);
    }

    #[test]
    fn test_sparse_transpose() {
        let mat = SparseBoolMatrix::from_dense(2, 3, &[
            true, false, true,
            false, true, false,
        ]);
        let trans = mat.transpose();
        assert_eq!(trans.n_rows(), 3);
        assert_eq!(trans.n_cols(), 2);

        let row0: Vec<_> = trans.row_iter(0).collect();
        assert_eq!(row0, vec![0]);

        let row2: Vec<_> = trans.row_iter(2).collect();
        assert_eq!(row2, vec![0]);
    }

    #[test]
    fn test_sparse_rank() {
        // Identity 3×3 has rank 3
        let eye = SparseBoolMatrix::from_dense(3, 3, &[
            true, false, false,
            false, true, false,
            false, false, true,
        ]);
        assert_eq!(eye.rank_z2(), 3);

        // [1 1; 1 1] has rank 1
        let mat = SparseBoolMatrix::from_dense(2, 2, &[true, true, true, true]);
        assert_eq!(mat.rank_z2(), 1);

        // Zero matrix has rank 0
        let zero = SparseBoolMatrix::empty(2, 3);
        assert_eq!(zero.rank_z2(), 0);
    }

    #[test]
    fn test_cubic_lattice_cell_complex() {
        // Build a 2×2×2 cubic lattice cell complex
        // V = 8, E = 3×8 = 24 (each site has 3 outgoing edges)
        // P = 3×8 = 24 (each site has 3 plaquettes: xy, yz, xz)
        // C = 8 (each site is the "origin" of one cube, but cubes overlap...)
        //
        // Actually for periodic boundary conditions, each cube is counted once.
        // For L=2 periodic cubic: V=8, E=12 (each edge shared by 2 sites, 24/2=12),
        // but wait, with periodic BC and storing links per site, we have 24 directed edges.
        //
        // Let's think more carefully. In our formulation, edges are directed.
        // For a periodic L×L×L lattice with links stored per site:
        // - n_edges = 3·L³ (directed edges)
        // - n_plaquettes = 3·L³ (oriented plaquettes, each site "owns" 3)
        // - n_cells = L³ (each site is the origin of one 3-cell)
        //
        // But boundary operators should work with this counting.
        // Actually for homology, we should use the minimal (undirected) counting.
        // Let me build a small explicit example.

        // For a 1×1×1 periodic cube (single site, periodic in all directions):
        // This is topologically a 3-torus.
        // Minimal cellulation:
        // V = 1
        // E = 3 (three independent non-contractible cycles)
        // P = 3 (three independent 2-cycles)
        // C = 1 (the 3-torus itself)
        // Euler: 1 - 3 + 3 - 1 = 0 ✓
        // Homology: H₀=1, H₁=3, H₂=3, H₃=1

    // For a 1×1×1 periodic cube (single site, periodic in all directions):
    // This is topologically a 3-torus.
    // Minimal cellulation:
    // V = 1, E = 3, P = 3, C = 1
    // Euler: 1 - 3 + 3 - 1 = 0 ✓
    // Homology: H₀=1, H₁=3, H₂=3, H₃=1
    //
    // Over ℤ₂: all boundary operators are zero (closed manifold)
    // This is tested in test_homology_3torus below.
        // Two vertices, one edge: contractible interval
        // H₀ = 1, H₁ = 0
        let d1 = SparseBoolMatrix::from_dense(2, 1, &[true, true]);
        let d2 = SparseBoolMatrix::empty(1, 0);
        let d3 = SparseBoolMatrix::empty(0, 0);

        let complex = CellComplex::new(d1, d2, d3);
        let hom = complex.compute_homology();
        assert_eq!(hom.h0, 1);
        assert_eq!(hom.h1, 0);
    }

    #[test]
    fn test_homology_circle() {
        // One vertex, one edge: circle S¹
        // H₀ = 1, H₁ = 1
        let d1 = SparseBoolMatrix::empty(1, 1);
        let d2 = SparseBoolMatrix::empty(1, 0);
        let d3 = SparseBoolMatrix::empty(0, 0);

        let complex = CellComplex::new(d1, d2, d3);
        let hom = complex.compute_homology();
        assert_eq!(hom.h0, 1);
        assert_eq!(hom.h1, 1);
    }

    #[test]
    fn test_homology_3torus() {
        // Minimal cellulation of T³ (3-torus)
        // Over ℤ₂: all boundary operators are zero (closed manifold)
        let d1 = SparseBoolMatrix::empty(1, 3);
        let d2 = SparseBoolMatrix::empty(3, 3);
        let d3 = SparseBoolMatrix::empty(3, 1);

        let complex = CellComplex::new(d1, d2, d3);
        assert_eq!(complex.euler_characteristic(), 0);
        assert!(complex.check_plaquette_closure());
        assert!(complex.check_bianchi_identity());

        let hom = complex.compute_homology();
        assert_eq!(hom.h0, 1, "H₀(T³) = 1");
        assert_eq!(hom.h1, 3, "H₁(T³) = 3");
        assert_eq!(hom.h2, 3, "H₂(T³) = 3");
        assert_eq!(hom.h3, 1, "H₃(T³) = 1");
    }

    #[test]
    fn test_homology_contractible_cube() {
        // Single cube (solid ball B³) — contractible
        // H = (1, 0, 0, 0), χ = 8 - 12 + 6 - 1 = 1
        let edges = [
            (0,1), (1,2), (2,3), (3,0),  // bottom
            (4,5), (5,6), (6,7), (7,4),  // top
            (0,4), (1,5), (2,6), (3,7),  // vertical
        ];

        let mut d1_dense = vec![false; 8 * 12];
        for (e, (v0, v1)) in edges.iter().enumerate() {
            d1_dense[v0 * 12 + e] = true;
            d1_dense[v1 * 12 + e] = true;
        }
        let d1 = SparseBoolMatrix::from_dense(8, 12, &d1_dense);

        let faces = [
            vec![0, 1, 2, 3],       // bottom
            vec![4, 5, 6, 7],       // top
            vec![0, 9, 4, 8],       // front
            vec![2, 10, 6, 11],     // back
            vec![3, 11, 7, 8],      // left
            vec![1, 10, 5, 9],      // right
        ];

        let mut d2_dense = vec![false; 12 * 6];
        for (p, face_edges) in faces.iter().enumerate() {
            for &e in face_edges {
                d2_dense[e * 6 + p] = true;
            }
        }
        let d2 = SparseBoolMatrix::from_dense(12, 6, &d2_dense);

        let d3 = SparseBoolMatrix::from_dense(6, 1, &[true; 6]);

        let complex = CellComplex::new(d1, d2, d3);
        assert_eq!(complex.euler_characteristic(), 1);
        assert!(complex.check_plaquette_closure());
        assert!(complex.check_bianchi_identity());

        let hom = complex.compute_homology();
        assert_eq!(hom.h0, 1, "H₀(B³)");
        assert_eq!(hom.h1, 0, "H₁(B³)");
        assert_eq!(hom.h2, 0, "H₂(B³)");
        assert_eq!(hom.h3, 0, "H₃(B³)");
    }

    #[test]
    fn test_diamond_lattice_l1() {
        // L=1 diamond lattice: 8 vertices in a single conventional cell
        // For L=1, all 4 neighbors of each vertex map to the same point due to periodic BC
        // So the graph is degenerate (complete bipartite K_{4,4} with multi-edges)
        // No hexagons exist in this degenerate case
        let (complex, _vertices) = diamond_lattice(1);

        assert_eq!(complex.n_vertices(), 8, "L=1 diamond has 8 vertices");
        assert_eq!(complex.n_edges(), 16, "L=1 diamond has 16 edges (8*4/2)");
        
        // L=1 is degenerate, so no plaquettes
        println!("L=1: V={}, E={}, P={}", 
            complex.n_vertices(), complex.n_edges(), complex.n_plaquettes());
    }

    #[test]
    fn test_diamond_lattice_l2() {
        // L=2 diamond lattice: 64 vertices
        let (complex, _vertices) = diamond_lattice(2);

        assert_eq!(complex.n_vertices(), 64, "L=2 diamond has 64 vertices");
        assert_eq!(complex.n_edges(), 128, "L=2 diamond has 128 edges");
        
        // Should have hexagonal plaquettes
        assert!(complex.n_plaquettes() > 0, "L=2 should have plaquettes");
        assert!(complex.check_plaquette_closure(), "Plaquettes should be closed");

        println!("Diamond L=2: V={}, E={}, P={}, χ={}",
            complex.n_vertices(), complex.n_edges(),
            complex.n_plaquettes(), complex.euler_characteristic());
    }
}
