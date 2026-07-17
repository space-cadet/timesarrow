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
//!
//! Over ℤ₂, orientations collapse to incidence (signs are irrelevant), but the
//! structure is still that of an oriented chain complex. Extension to ℤ or ℤₙ
//! would require signed entries.

use std::collections::{BTreeSet, HashMap, HashSet};

// =============================================================================
// SPARSE BOOLEAN MATRIX (CSR format over ℤ₂)
// =============================================================================

/// Compressed Sparse Row (CSR) matrix over ℤ₂.
///
/// All non-zero entries are implicitly 1. Only the sparsity pattern is stored.
/// Matrix dimensions: `n_rows × n_cols`.
#[derive(Clone, Debug, PartialEq, Eq)]
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
        let rows = (0..n_rows)
            .map(|row| {
                (0..n_cols)
                    .filter(|&col| dense[row * n_cols + col])
                    .collect()
            })
            .collect();
        Self::from_row_indices(n_rows, n_cols, rows)
    }

    /// Create a sparse matrix from its non-zero column indices, row by row.
    ///
    /// Rows are sorted and deduplicated; panics on out-of-range or duplicate
    /// column indices within a single row.
    pub fn from_row_indices(n_rows: usize, n_cols: usize, mut rows: Vec<Vec<usize>>) -> Self {
        assert_eq!(
            rows.len(),
            n_rows,
            "one row specification is required per matrix row"
        );

        let mut indptr = Vec::with_capacity(n_rows + 1);
        let mut indices = Vec::new();
        indptr.push(0);

        for row in &mut rows {
            row.sort_unstable();
            assert!(
                row.iter().all(|&col| col < n_cols),
                "column index out of range"
            );
            assert!(
                row.windows(2).all(|pair| pair[0] != pair[1]),
                "duplicate sparse entry"
            );
            indices.extend_from_slice(row);
            indptr.push(indices.len());
        }

        Self {
            n_rows,
            n_cols,
            indptr,
            indices,
        }
    }

    /// Create a sparse matrix from its non-zero row indices, column by column.
    pub fn from_column_indices(n_rows: usize, n_cols: usize, columns: &[Vec<usize>]) -> Self {
        assert_eq!(
            columns.len(),
            n_cols,
            "one column specification is required per matrix column"
        );
        let mut rows = vec![Vec::new(); n_rows];
        for (col, column_rows) in columns.iter().enumerate() {
            for &row in column_rows {
                assert!(row < n_rows, "row index out of range");
                rows[row].push(col);
            }
        }
        Self::from_row_indices(n_rows, n_cols, rows)
    }

    /// Number of rows.
    pub fn n_rows(&self) -> usize { self.n_rows }

    /// Number of columns.
    pub fn n_cols(&self) -> usize { self.n_cols }

    /// Number of non-zero entries.
    pub fn nnz(&self) -> usize { self.indices.len() }

    /// Iterator over non-zero column indices in a given row.
    pub fn row_iter(&self, row: usize) -> impl Iterator<Item = usize> + '_ {
        assert!(row < self.n_rows, "row index out of range");
        self.indices[self.indptr[row]..self.indptr[row + 1]]
            .iter()
            .copied()
    }

    /// Iterator over (row, col) pairs of all non-zero entries.
    pub fn entries(&self) -> impl Iterator<Item = (usize, usize)> + '_ {
        (0..self.n_rows).flat_map(move |row| self.row_iter(row).map(move |col| (row, col)))
    }

    /// Compute the transpose.
    pub fn transpose(&self) -> Self {
        let mut rows = vec![Vec::new(); self.n_cols];
        for (row, col) in self.entries() {
            rows[col].push(row);
        }
        Self::from_row_indices(self.n_cols, self.n_rows, rows)
    }

    /// Matrix-vector product over ℤ₂: y = A · x (mod 2).
    ///
    /// `x` must have length `n_cols`, result has length `n_rows`.
    pub fn matvec(&self, x: &[bool]) -> Vec<bool> {
        assert_eq!(x.len(), self.n_cols);
        (0..self.n_rows)
            .map(|row| self.row_iter(row).fold(false, |acc, col| acc ^ x[col]))
            .collect()
    }

    /// Sparse matrix-matrix product over ℤ₂: C = A · B (mod 2).
    ///
    /// Uses a BTreeSet per row to accumulate XOR toggles. This is efficient
    /// for very sparse boundary operators (the typical case in cell complexes),
    /// where the dense-buffer alternative would waste time scanning zeroes.
    ///
    /// # Panics
    /// Panics if `self.n_cols != other.n_rows`.
    pub fn matmul(&self, other: &Self) -> Self {
        assert_eq!(self.n_cols, other.n_rows, "incompatible matrix dimensions");
        let mut rows = Vec::with_capacity(self.n_rows);

        for row in 0..self.n_rows {
            let mut result = BTreeSet::new();
            for shared in self.row_iter(row) {
                for col in other.row_iter(shared) {
                    if !result.insert(col) {
                        result.remove(&col);
                    }
                }
            }
            rows.push(result.into_iter().collect());
        }
        Self::from_row_indices(self.n_rows, other.n_cols, rows)
    }

    /// Compute the rank over ℤ₂ using Gaussian elimination.
    ///
    /// This materializes a dense work buffer and is intended for
    /// topology checks, not for the Monte Carlo hot path.
    pub fn rank_z2(&self) -> usize {
        let mut rows = vec![vec![false; self.n_cols]; self.n_rows];
        for (row, col) in self.entries() {
            rows[row][col] = true;
        }

        let mut rank = 0;
        for col in 0..self.n_cols {
            let Some(pivot) = (rank..self.n_rows).find(|&row| rows[row][col]) else {
                continue;
            };
            rows.swap(rank, pivot);
            for row in (rank + 1)..self.n_rows {
                if rows[row][col] {
                    for entry in col..self.n_cols {
                        rows[row][entry] ^= rows[rank][entry];
                    }
                }
            }
            rank += 1;
            if rank == self.n_rows {
                break;
            }
        }
        rank
    }
}

/// Failure while constructing a chain complex.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CellComplexError {
    InconsistentDimensions,
    PlaquetteBoundaryIsNotClosed,
    CellBoundaryIsNotClosed,
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
    d1: SparseBoolMatrix,
    d2: SparseBoolMatrix,
    d3: SparseBoolMatrix,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Homology {
    pub h0: usize,
    pub h1: usize,
    pub h2: usize,
    pub h3: usize,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ValidationResult {
    pub d1_d2_zero: bool,
    pub d2_d3_zero: bool,
    pub euler_characteristic: i64,
    pub homology: Homology,
}

impl CellComplex {
    /// Construct and validate a chain complex.
    pub fn try_new(
        d1: SparseBoolMatrix,
        d2: SparseBoolMatrix,
        d3: SparseBoolMatrix,
    ) -> Result<Self, CellComplexError> {
        if d1.n_cols() != d2.n_rows() || d2.n_cols() != d3.n_rows() {
            return Err(CellComplexError::InconsistentDimensions);
        }
        if d1.matmul(&d2).nnz() != 0 {
            return Err(CellComplexError::PlaquetteBoundaryIsNotClosed);
        }
        if d2.matmul(&d3).nnz() != 0 {
            return Err(CellComplexError::CellBoundaryIsNotClosed);
        }
        Ok(Self { d1, d2, d3 })
    }

    /// Construct a validated chain complex, panicking with a clear error if the
    /// supplied incidence data are invalid.  Prefer `try_new` for external data.
    ///
    /// # Arguments
    /// - `d1`: n_v × n_e matrix, column j is the boundary of edge j (two vertices)
    /// - `d2`: n_e × n_p matrix, column j is the boundary of plaquette j (edges around it)
    /// - `d3`: n_p × n_c matrix, column j is the boundary of 3-cell j (plaquettes around it)
    ///
    /// # Panics
    /// Panics if dimensions are inconsistent (e.g., d1.n_cols != d2.n_rows).
    pub fn new(d1: SparseBoolMatrix, d2: SparseBoolMatrix, d3: SparseBoolMatrix) -> Self {
        Self::try_new(d1, d2, d3).expect("invalid cell-complex boundary operators")
    }

    /// Number of vertices (0-cells).
    pub fn n_vertices(&self) -> usize { self.d1.n_rows() }

    /// Number of edges (1-cells).
    pub fn n_edges(&self) -> usize { self.d1.n_cols() }

    /// Number of plaquettes (2-cells).
    pub fn n_plaquettes(&self) -> usize { self.d2.n_cols() }

    /// Number of 3-cells.
    pub fn n_cells(&self) -> usize { self.d3.n_cols() }

    /// Boundary operator ∂₁: edges → vertices.
    pub fn d1(&self) -> &SparseBoolMatrix { &self.d1 }

    /// Boundary operator ∂₂: plaquettes → edges.
    pub fn d2(&self) -> &SparseBoolMatrix { &self.d2 }

    /// Boundary operator ∂₃: 3-cells → plaquettes.
    pub fn d3(&self) -> &SparseBoolMatrix { &self.d3 }

    /// Verify that ∂₁∂₂ = 0 (every plaquette is a closed edge cycle).
    pub fn check_plaquette_closure(&self) -> bool {
        self.d1.matmul(&self.d2).nnz() == 0
    }

    /// Verify that ∂₂∂₃ = 0 (Bianchi identity: boundary of 3-cell has zero boundary).
    pub fn check_bianchi_identity(&self) -> bool {
        self.d2.matmul(&self.d3).nnz() == 0
    }

    pub fn euler_characteristic(&self) -> i64 {
        self.n_vertices() as i64 - self.n_edges() as i64 + self.n_plaquettes() as i64
            - self.n_cells() as i64
    }

    pub fn compute_homology(&self) -> Homology {
        let r1 = self.d1.rank_z2();
        let r2 = self.d2.rank_z2();
        let r3 = self.d3.rank_z2();
        let homology = Homology {
            h0: self.n_vertices() - r1,
            h1: self.n_edges() - r1 - r2,
            h2: self.n_plaquettes() - r2 - r3,
            h3: self.n_cells() - r3,
        };
        debug_assert_eq!(
            homology.h0 as i64 - homology.h1 as i64 + homology.h2 as i64 - homology.h3 as i64,
            self.euler_characteristic()
        );
        homology
    }

    pub fn validate(&self) -> ValidationResult {
        ValidationResult {
            d1_d2_zero: self.check_plaquette_closure(),
            d2_d3_zero: self.check_bianchi_identity(),
            euler_characteristic: self.euler_characteristic(),
            homology: self.compute_homology(),
        }
    }
}

type Vertex = usize;

#[derive(Clone, Copy)]
struct DiamondEdge {
    source: Vertex,
    target: Vertex,
    offset: (isize, isize, isize),
}

const DIAMOND_OFFSETS: [(isize, isize, isize); 4] =
    [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)];

fn wrap_coordinate(value: usize, delta: isize, size: usize) -> usize {
    (value as isize + delta).rem_euclid(size as isize) as usize
}

fn diamond_neighbor(
    vertex: (usize, usize, usize),
    offset: (isize, isize, isize),
    size: usize,
) -> (usize, usize, usize) {
    (
        wrap_coordinate(vertex.0, offset.0, size),
        wrap_coordinate(vertex.1, offset.1, size),
        wrap_coordinate(vertex.2, offset.2, size),
    )
}

fn is_a_sublattice(vertex: (usize, usize, usize)) -> bool {
    vertex.0.is_multiple_of(2)
        && vertex.1.is_multiple_of(2)
        && vertex.2.is_multiple_of(2)
        && (vertex.0 + vertex.1 + vertex.2).is_multiple_of(4)
}

fn is_b_sublattice(vertex: (usize, usize, usize)) -> bool {
    !vertex.0.is_multiple_of(2)
        && !vertex.1.is_multiple_of(2)
        && !vertex.2.is_multiple_of(2)
        && (vertex.0 + vertex.1 + vertex.2) % 4 == 3
}

fn negate(offset: (isize, isize, isize)) -> (isize, isize, isize) {
    (-offset.0, -offset.1, -offset.2)
}

fn add_offsets(left: (isize, isize, isize), right: (isize, isize, isize)) -> (isize, isize, isize) {
    (left.0 + right.0, left.1 + right.1, left.2 + right.2)
}

fn adjacency_from_edges(
    n_vertices: usize,
    edges: &[DiamondEdge],
) -> Vec<Vec<(Vertex, usize, (isize, isize, isize))>> {
    let mut adjacency = vec![Vec::new(); n_vertices];
    for (edge_index, edge) in edges.iter().enumerate() {
        adjacency[edge.source].push((edge.target, edge_index, edge.offset));
        adjacency[edge.target].push((edge.source, edge_index, negate(edge.offset)));
    }
    adjacency
}

fn enumerate_hexagons(
    adjacency: &[Vec<(Vertex, usize, (isize, isize, isize))>],
) -> Vec<Vec<usize>> {
    fn visit(
        start: Vertex,
        current: Vertex,
        depth: usize,
        displacement: (isize, isize, isize),
        adjacency: &[Vec<(Vertex, usize, (isize, isize, isize))>],
        visited: &mut [bool],
        path_edges: &mut Vec<usize>,
        faces: &mut HashSet<Vec<usize>>,
    ) {
        if depth == 6 {
            if current == start && displacement == (0, 0, 0) {
                let mut face = path_edges.clone();
                face.sort_unstable();
                if face.windows(2).all(|pair| pair[0] != pair[1]) {
                    faces.insert(face);
                }
            }
            return;
        }

        for &(next, edge, offset) in &adjacency[current] {
            if next == start {
                if depth + 1 == 6 {
                    path_edges.push(edge);
                    visit(
                        start,
                        next,
                        depth + 1,
                        add_offsets(displacement, offset),
                        adjacency,
                        visited,
                        path_edges,
                        faces,
                    );
                    path_edges.pop();
                }
                continue;
            }
            if next < start || visited[next] {
                continue;
            }
            visited[next] = true;
            path_edges.push(edge);
            visit(
                start,
                next,
                depth + 1,
                add_offsets(displacement, offset),
                adjacency,
                visited,
                path_edges,
                faces,
            );
            path_edges.pop();
            visited[next] = false;
        }
    }

    let mut faces = HashSet::new();
    for start in 0..adjacency.len() {
        let mut visited = vec![false; adjacency.len()];
        visited[start] = true;
        visit(
            start,
            start,
            0,
            (0, 0, 0),
            adjacency,
            &mut visited,
            &mut Vec::new(),
            &mut faces,
        );
    }
    let mut faces: Vec<_> = faces.into_iter().collect();
    faces.sort_unstable();
    faces
}

/// Build the periodic diamond-lattice 2-skeleton.
///
/// The generator supplies vertices, tetrahedrally coordinated edges, and the
/// elementary hexagonal faces.  It intentionally supplies no 3-cells: their
/// choice depends on the intended spatial cellulation and must be explicit.
pub fn diamond_lattice(l: usize) -> (CellComplex, Vec<(usize, usize, usize)>) {
    assert!(l >= 1, "l must be at least one");
    // Coordinates are scaled by a/4.  An FCC A sublattice plus its (1,1,1)
    // basis displacement gives eight diamond sites per conventional cell.
    let size = 4 * l;
    let vertices: Vec<_> = (0..size)
        .flat_map(|x| {
            (0..size).flat_map(move |y| {
                (0..size)
                    .map(move |z| (x, y, z))
                    .filter(|&vertex| is_a_sublattice(vertex) || is_b_sublattice(vertex))
            })
        })
        .collect();
    let vertex_index: HashMap<_, _> = vertices.iter().copied().zip(0..vertices.len()).collect();

    // Only A-sublattice sites emit bonds.  This preserves the diamond lattice's
    // alternating tetrahedral coordination instead of globally filtering links.
    let mut edges = Vec::with_capacity(16 * l.pow(3));
    for &vertex in &vertices {
        if !is_a_sublattice(vertex) {
            continue;
        }
        let source = vertex_index[&vertex];
        for offset in DIAMOND_OFFSETS {
            let target = vertex_index[&diamond_neighbor(vertex, offset, size)];
            edges.push(DiamondEdge {
                source,
                target,
                offset,
            });
        }
    }

    let adjacency = adjacency_from_edges(vertices.len(), &edges);
    let plaquettes = enumerate_hexagons(&adjacency);
    let d1 = SparseBoolMatrix::from_column_indices(
        vertices.len(),
        edges.len(),
        &edges
            .iter()
            .map(|edge| vec![edge.source, edge.target])
            .collect::<Vec<_>>(),
    );
    let d2 = SparseBoolMatrix::from_column_indices(edges.len(), plaquettes.len(), &plaquettes);
    let d3 = SparseBoolMatrix::empty(plaquettes.len(), 0);
    (CellComplex::new(d1, d2, d3), vertices)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn vertex_degrees(complex: &CellComplex) -> Vec<usize> {
        let mut degrees = vec![0; complex.n_vertices()];
        for (vertex, _) in complex.d1().entries() {
            degrees[vertex] += 1;
        }
        degrees
    }

    #[test]
    fn sparse_matrix_operations_are_z2_correct() {
        let matrix = SparseBoolMatrix::from_dense(2, 3, &[true, false, true, false, true, false]);
        assert_eq!(matrix.row_iter(0).collect::<Vec<_>>(), vec![0, 2]);
        assert_eq!(matrix.matvec(&[true, false, true]), vec![false, false]);
        assert_eq!(matrix.transpose().row_iter(2).collect::<Vec<_>>(), vec![0]);
        assert_eq!(matrix.rank_z2(), 2);

        let left = SparseBoolMatrix::from_dense(2, 2, &[true, false, true, true]);
        let right = SparseBoolMatrix::from_dense(2, 2, &[true, true, false, true]);
        assert_eq!(left.matmul(&right).row_iter(1).collect::<Vec<_>>(), vec![0]);
    }

    #[test]
    fn invalid_boundary_operators_are_rejected() {
        let d1 = SparseBoolMatrix::from_dense(1, 1, &[true]);
        let d2 = SparseBoolMatrix::from_dense(1, 1, &[true]);
        let d3 = SparseBoolMatrix::empty(1, 0);
        assert!(matches!(
            CellComplex::try_new(d1, d2, d3),
            Err(CellComplexError::PlaquetteBoundaryIsNotClosed)
        ));
    }

    #[test]
    fn standard_homology_examples_are_correct() {
        let interval = CellComplex::new(
            SparseBoolMatrix::from_dense(2, 1, &[true, true]),
            SparseBoolMatrix::empty(1, 0),
            SparseBoolMatrix::empty(0, 0),
        );
        assert_eq!(
            interval.compute_homology(),
            Homology {
                h0: 1,
                h1: 0,
                h2: 0,
                h3: 0
            }
        );

        let torus = CellComplex::new(
            SparseBoolMatrix::empty(1, 3),
            SparseBoolMatrix::empty(3, 3),
            SparseBoolMatrix::empty(3, 1),
        );
        assert_eq!(
            torus.compute_homology(),
            Homology {
                h0: 1,
                h1: 3,
                h2: 3,
                h3: 1
            }
        );
    }

    #[test]
    fn contractible_cube_has_trivial_higher_homology() {
        let edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ];
        let faces = vec![
            vec![0, 1, 2, 3],
            vec![4, 5, 6, 7],
            vec![0, 9, 4, 8],
            vec![2, 10, 6, 11],
            vec![3, 11, 7, 8],
            vec![1, 10, 5, 9],
        ];
        let cube = CellComplex::new(
            SparseBoolMatrix::from_column_indices(
                8,
                12,
                &edges.iter().map(|&(a, b)| vec![a, b]).collect::<Vec<_>>(),
            ),
            SparseBoolMatrix::from_column_indices(12, 6, &faces),
            SparseBoolMatrix::from_column_indices(6, 1, &[vec![0, 1, 2, 3, 4, 5]]),
        );
        assert_eq!(
            cube.compute_homology(),
            Homology {
                h0: 1,
                h1: 0,
                h2: 0,
                h3: 0
            }
        );
    }

    #[test]
    fn diamond_lattice_l1_has_the_expected_small_periodic_cellulation() {
        let (complex, _) = diamond_lattice(1);
        assert_eq!(
            (
                complex.n_vertices(),
                complex.n_edges(),
                complex.n_plaquettes()
            ),
            (8, 16, 16)
        );
        assert!(complex.check_plaquette_closure());
        assert_eq!(complex.compute_homology().h0, 1);
    }

    #[test]
    fn diamond_lattice_l2_is_connected_and_four_valent() {
        let (complex, _) = diamond_lattice(2);
        assert_eq!(
            (
                complex.n_vertices(),
                complex.n_edges(),
                complex.n_plaquettes()
            ),
            (64, 128, 128)
        );
        assert!(vertex_degrees(&complex).iter().all(|&degree| degree == 4));
        assert!(complex.check_plaquette_closure());
        assert_eq!(
            complex.compute_homology().h0,
            1,
            "periodic diamond lattice must be connected"
        );
    }

    #[test]
    fn diamond_lattice_l3_preserves_cell_counts_and_connectedness() {
        let (complex, _) = diamond_lattice(3);
        assert_eq!(
            (
                complex.n_vertices(),
                complex.n_edges(),
                complex.n_plaquettes()
            ),
            (216, 432, 432)
        );
        assert!(vertex_degrees(&complex).iter().all(|&degree| degree == 4));
        assert_eq!(complex.compute_homology().h0, 1);
    }
}
