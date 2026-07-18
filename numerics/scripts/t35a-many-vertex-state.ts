/**
 * T35a: Many-Vertex CZX Candidate State Construction
 *
 * Tests whether a CZX-like symmetry preserves a state built from
 * intertwiner-singlet tensors on a 2-vertex diamond unit.
 *
 * Physics:
 * - 2 vertices, each with 4 spin-1/2 qubits (edge-ends)
 * - Intertwiner singlet at each vertex: 2D subspace of 16D 4-qubit space
 * - Global symmetry: U = U_CZX(v1) ⊗ U_CZX(v2)
 * - Question: does U preserve the product intertwiner subspace (4D)?
 */

import {
  StateVector,
  MatrixOperator,
  getFourSpinHalfBasis,
  createCzxOnSiteSymmetry,
} from 'ts-quantum/dist/index.js';
import * as math from 'mathjs';

const TOLERANCE = 1e-10;

interface EigenspaceResult {
  eigenvalue: number;
  eigenvectors: number[][]; // coefficients in intertwiner basis
  dimension: number;
}

interface VertexAuditResult {
  intertwinerBasis: StateVector[];
  czxMatrixInIntertwinerBasis: number[][]; // 2×2 complex matrix
  eigenvalues: number[];
  preservesSubspace: boolean;
  leakage: number;
}

/**
 * Compute the matrix elements of U_CZX in the intertwiner basis.
 * M_{ij} = ⟨I_i| U_CZX |I_j⟩
 */
function auditSingleVertex(): VertexAuditResult {
  const intertwinerSpace = getFourSpinHalfBasis();
  const basis = intertwinerSpace.basisStates.map((b) => b.stateVector);
  const symmetry = createCzxOnSiteSymmetry();

  const matrix: number[][] = [];
  for (let i = 0; i < basis.length; i++) {
    const row: number[] = [];
    for (let j = 0; j < basis.length; j++) {
      const transformed = symmetry.apply(basis[j]);
      const overlap = basis[i].innerProduct(transformed);
      // overlap should be real for this operator, but keep complex for safety
      const re = math.re(overlap) as number;
      const im = math.im(overlap) as number;
      if (Math.abs(im) > TOLERANCE) {
        console.warn(`  Imaginary part in M[${i}][${j}]: ${im}`);
      }
      row.push(re);
    }
    matrix.push(row);
  }

  // Check if matrix is Hermitian (it should be if U_CZX is unitary and basis is orthonormal)
  const isHermitian = matrix.every((row, i) =>
    row.every((val, j) => Math.abs(val - matrix[j][i]) < TOLERANCE)
  );

  // Eigenvalues of 2×2 matrix
  const [[a, b], [c, d]] = matrix;
  const trace = a + d;
  const det = a * d - b * c;
  const disc = trace * trace - 4 * det;
  const lambda1 = (trace + Math.sqrt(disc)) / 2;
  const lambda2 = (trace - Math.sqrt(disc)) / 2;

  // Check preservation: is M a unitary matrix? (i.e., does U preserve the subspace?)
  const identity = [
    [1, 0],
    [0, 1],
  ];
  const mTimesM = [
    [a * a + b * c, a * b + b * d],
    [c * a + d * c, c * b + d * d],
  ];
  const isUnitary =
    Math.abs(mTimesM[0][0] - 1) < TOLERANCE &&
    Math.abs(mTimesM[0][1]) < TOLERANCE &&
    Math.abs(mTimesM[1][0]) < TOLERANCE &&
    Math.abs(mTimesM[1][1] - 1) < TOLERANCE;

  // Leakage: norm of (U - PUP) applied to basis states
  let leakage = 0;
  for (let j = 0; j < basis.length; j++) {
    const transformed = symmetry.apply(basis[j]);
    const projected = basis.reduce((sum, bi, i) => {
      const coeff = bi.innerProduct(transformed);
      const scaled = bi.scale(coeff);
      return sum.add(scaled);
    }, StateVector.computationalBasis(basis[0].dimension, 0).scale(math.complex(0, 0)));

    const diff = transformed.add(projected.scale(math.complex(-1, 0)));
    const norm = (math.abs(diff.innerProduct(diff)) as unknown as number) ** 0.5;
    leakage = Math.max(leakage, norm);
  }

  return {
    intertwinerBasis: basis,
    czxMatrixInIntertwinerBasis: matrix,
    eigenvalues: [lambda1, lambda2],
    preservesSubspace: isUnitary,
    leakage,
  };
}

/**
 * For 2 vertices, the symmetry matrix in the 4D product intertwiner space
 * is M ⊗ M where M is the single-vertex matrix.
 */
function buildTwoVertexSymmetryMatrix(M: number[][]): number[][] {
  const dim = 4;
  const result: number[][] = Array(dim)
    .fill(null)
    .map(() => Array(dim).fill(0));

  // Basis ordering: |00⟩, |01⟩, |10⟩, |11⟩ where |ij⟩ = |I_i⟩ ⊗ |I_j⟩
  for (let i1 = 0; i1 < 2; i1++) {
    for (let j1 = 0; j1 < 2; j1++) {
      for (let i2 = 0; i2 < 2; i2++) {
        for (let j2 = 0; j2 < 2; j2++) {
          const row = i1 * 2 + i2;
          const col = j1 * 2 + j2;
          result[row][col] = M[i1][j1] * M[i2][j2];
        }
      }
    }
  }

  return result;
}

/**
 * Find eigenvalues and eigenvectors of a real symmetric matrix.
 */
function diagonalizeSymmetric(matrix: number[][]): EigenspaceResult[] {
  const n = matrix.length;

  // Use Jacobi iteration for small symmetric matrices
  // or just compute analytically for 4×4

  // For 4×4, use power iteration for each eigenvalue
  const results: EigenspaceResult[] = [];
  let remaining = matrix.map((row) => [...row]);

  for (let eigenIdx = 0; eigenIdx < n; eigenIdx++) {
    // Power iteration with deflation
    let vec = Array(n)
      .fill(0)
      .map(() => Math.random() - 0.5);

    for (let iter = 0; iter < 100; iter++) {
      // Multiply: new_vec = remaining * vec
      const newVec = remaining.map((row) =>
        row.reduce((sum, val, j) => sum + val * vec[j], 0)
      );
      const norm = Math.sqrt(newVec.reduce((sum, v) => sum + v * v, 0));
      vec = newVec.map((v) => v / norm);
    }

    // Rayleigh quotient for eigenvalue
    const eigenvalue = vec.reduce(
      (sum, vi, i) => sum + vi * remaining[i].reduce((s, val, j) => s + val * vec[j], 0),
      0
    );

    // Deflate
    const outer = vec.map((vi) => vec.map((vj) => vi * vj));
    remaining = remaining.map((row, i) => row.map((val, j) => val - eigenvalue * outer[i][j]));

    results.push({
      eigenvalue: Math.round(eigenvalue / TOLERANCE) * TOLERANCE, // round to tolerance
      eigenvectors: [vec],
      dimension: 1,
    });
  }

  // Group by eigenvalue
  const grouped: Map<number, number[][]> = new Map();
  for (const r of results) {
    const ev = Math.round(r.eigenvalue / TOLERANCE) * TOLERANCE;
    if (!grouped.has(ev)) grouped.set(ev, []);
    grouped.get(ev)!.push(r.eigenvectors[0]);
  }

  return Array.from(grouped.entries()).map(([eigenvalue, eigenvectors]) => ({
    eigenvalue,
    eigenvectors,
    dimension: eigenvectors.length,
  }));
}

function main() {
  console.log('=== T35a: Many-Vertex CZX Candidate State ===\n');

  // Step 1: Single-vertex audit (reproduce known result)
  console.log('Step 1: Single-vertex CZX in intertwiner basis');
  const singleVertex = auditSingleVertex();
  console.log(`  Intertwiner dimension: ${singleVertex.intertwinerBasis.length}`);
  console.log(`  CZX matrix M in intertwiner basis:`);
  for (const row of singleVertex.czxMatrixInIntertwinerBasis) {
    console.log(`    [${row.map((v) => v.toFixed(6)).join(', ')}]`);
  }
  console.log(`  Eigenvalues: ${singleVertex.eigenvalues.map((v) => v.toFixed(6)).join(', ')}`);
  console.log(`  Preserves subspace: ${singleVertex.preservesSubspace}`);
  console.log(`  Leakage: ${singleVertex.leakage.toExponential(2)}`);
  console.log();

  // Step 2: Two-vertex symmetry
  console.log('Step 2: Two-vertex product intertwiner space');
  const M = singleVertex.czxMatrixInIntertwinerBasis;
  const twoVertexMatrix = buildTwoVertexSymmetryMatrix(M);
  console.log(`  Symmetry matrix M⊗M in 4D product basis (|00⟩,|01⟩,|10⟩,|11⟩):`);
  for (const row of twoVertexMatrix) {
    console.log(`    [${row.map((v) => v.toFixed(6)).join(', ')}]`);
  }

  // Step 3: Diagonalize
  const eigenspaces = diagonalizeSymmetric(twoVertexMatrix);
  console.log(`  Eigenspaces:`);
  for (const es of eigenspaces) {
    console.log(`    λ = ${es.eigenvalue.toFixed(6)}, dim = ${es.dimension}`);
    for (const vec of es.eigenvectors) {
      console.log(`      [${vec.map((v) => v.toFixed(6)).join(', ')}]`);
    }
  }
  console.log();

  // Step 4: Interpretation
  console.log('Step 4: Interpretation');
  const plusOneEigenspace = eigenspaces.find((es) => Math.abs(es.eigenvalue - 1) < TOLERANCE);
  const minusOneEigenspace = eigenspaces.find((es) => Math.abs(es.eigenvalue + 1) < TOLERANCE);

  if (plusOneEigenspace) {
    console.log(`  +1 eigenspace dimension: ${plusOneEigenspace.dimension}`);
  } else {
    console.log(`  +1 eigenspace: EMPTY`);
  }
  if (minusOneEigenspace) {
    console.log(`  -1 eigenspace dimension: ${minusOneEigenspace.dimension}`);
  } else {
    console.log(`  -1 eigenspace: EMPTY`);
  }

  // Check if U^2 = I on the 4D subspace
  const mat = twoVertexMatrix;
  const mat2 = mat.map((row, i) =>
    row.map((_, j) => row.reduce((sum, val, k) => sum + val * mat[k][j], 0))
  );
  const isIdentity = mat2.every((row, i) =>
    row.every((val, j) => Math.abs(val - (i === j ? 1 : 0)) < TOLERANCE)
  );
  console.log(`  (M⊗M)^2 = I: ${isIdentity}`);
  console.log();

  // Step 5: Construct candidate state if +1 eigenspace is nontrivial
  if (plusOneEigenspace && plusOneEigenspace.dimension > 0) {
    console.log('Step 5: Candidate state construction');
    const basis = getFourSpinHalfBasis().basisStates.map((b) => b.stateVector);

    for (let idx = 0; idx < plusOneEigenspace.eigenvectors.length; idx++) {
      const vec = plusOneEigenspace.eigenvectors[idx];
      console.log(`  Candidate ${idx + 1} (coefficients in |I_i⟩⊗|I_j⟩ basis):`);
      console.log(`    [${vec.map((v) => v.toFixed(6)).join(', ')}]`);

      // Construct the actual state vector
      let state = StateVector.computationalBasis(basis[0].dimension * basis[0].dimension, 0).scale(
        math.complex(0, 0)
      );
      for (let i = 0; i < 2; i++) {
        for (let j = 0; j < 2; j++) {
          const coeff = vec[i * 2 + j];
          const productState = basis[i].tensorProduct(basis[j]);
          const scaled = productState.scale(math.complex(coeff, 0));
          state = state.add(scaled) as StateVector;
        }
      }
      state = state.normalize();
      console.log(`    State norm: ${state.norm().toFixed(6)}`);
      console.log(`    Nonzero amplitudes: ${state.amplitudes.filter((a) => (math.abs(a) as unknown as number) > TOLERANCE).length}`);
    }
  }

  // Summary
  console.log('\n=== Summary ===');
  if (singleVertex.preservesSubspace) {
    console.log('UNEXPECTED: Single-vertex CZX preserves intertwiner subspace');
  } else {
    console.log('CONFIRMED: Single-vertex CZX leaks out of intertwiner subspace');
  }

  if (plusOneEigenspace && plusOneEigenspace.dimension > 0) {
    console.log(`POSITIVE: ${plusOneEigenspace.dimension}-dimensional +1 eigenspace exists in product intertwiner space`);
    console.log('→ Candidate CZX-symmetric state CAN be constructed from intertwiner tensors');
  } else {
    console.log('NEGATIVE: No +1 eigenspace in product intertwiner space');
    console.log('→ No CZX-symmetric state can be built from intertwiner tensors alone');
  }
}

main();
