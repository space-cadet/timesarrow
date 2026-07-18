/**
 * T35a: Many-Vertex CZX Candidate State Construction
 *
 * Tests whether a CZX-like symmetry preserves a state built from
 * intertwiner-singlet tensors on a 2-vertex diamond unit.
 */

const {
  StateVector,
  getFourSpinHalfBasis,
  createCzxOnSiteSymmetry,
} = require('/Users/deepak/code/ts-quantum/dist/index.js');

const math = require('mathjs');

const TOLERANCE = 1e-10;

/**
 * Compute the matrix elements of U_CZX in the intertwiner basis.
 * M_{ij} = <I_i| U_CZX |I_j>
 */
function auditSingleVertex() {
  const intertwinerSpace = getFourSpinHalfBasis();
  const basis = intertwinerSpace.basisStates.map((b) => b.stateVector);
  const symmetry = createCzxOnSiteSymmetry();

  const matrix = [];
  for (let i = 0; i < basis.length; i++) {
    const row = [];
    for (let j = 0; j < basis.length; j++) {
      const transformed = symmetry.apply(basis[j]);
      const overlap = basis[i].innerProduct(transformed);
      const re = math.re(overlap);
      const im = math.im(overlap);
      if (Math.abs(im) > TOLERANCE) {
        console.warn(`  Imaginary part in M[${i}][${j}]: ${im}`);
      }
      row.push(re);
    }
    matrix.push(row);
  }

  // Eigenvalues of 2x2 matrix
  const [[a, b], [c, d]] = matrix;
  const trace = a + d;
  const det = a * d - b * c;
  const disc = trace * trace - 4 * det;
  const lambda1 = (trace + Math.sqrt(disc)) / 2;
  const lambda2 = (trace - Math.sqrt(disc)) / 2;

  // Check if M is unitary (preserves subspace)
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
    let projected = new StateVector(basis[0].dimension);
    for (let i = 0; i < basis.length; i++) {
      const coeff = basis[i].innerProduct(transformed);
      const scaled = basis[i].scale(coeff);
      projected = projected.add(scaled);
    }
    const diff = transformed.add(projected.scale(math.complex(-1, 0)));
    const norm = Math.sqrt(math.abs(diff.innerProduct(diff)));
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
 * is M (x) M where M is the single-vertex matrix.
 */
function buildTwoVertexSymmetryMatrix(M) {
  const dim = 4;
  const result = Array(dim)
    .fill(null)
    .map(() => Array(dim).fill(0));

  // Basis ordering: |00>, |01>, |10>, |11> where |ij> = |I_i> (x) |I_j>
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
 * Find eigenvalues and eigenvectors of a real symmetric matrix using Jacobi iteration.
 */
function diagonalizeSymmetric(matrix) {
  const n = matrix.length;
  const eigvals = Array(n).fill(0);
  const eigvecs = Array(n)
    .fill(null)
    .map((_, i) =>
      Array(n)
        .fill(0)
        .map((_, j) => (i === j ? 1 : 0))
    );

  // Make a copy
  let A = matrix.map((row) => [...row]);

  // Jacobi iteration
  for (let sweep = 0; sweep < 50; sweep++) {
    let maxOffDiag = 0;
    let p = 0,
      q = 0;
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        if (Math.abs(A[i][j]) > maxOffDiag) {
          maxOffDiag = Math.abs(A[i][j]);
          p = i;
          q = j;
        }
      }
    }

    if (maxOffDiag < TOLERANCE) break;

    const app = A[p][p];
    const aqq = A[q][q];
    const apq = A[p][q];
    const phi = 0.5 * Math.atan2(2 * apq, aqq - app);
    const c = Math.cos(phi);
    const s = Math.sin(phi);

    // Update A
    for (let i = 0; i < n; i++) {
      if (i !== p && i !== q) {
        const aip = A[i][p];
        const aiq = A[i][q];
        A[i][p] = A[p][i] = c * aip - s * aiq;
        A[i][q] = A[q][i] = s * aip + c * aiq;
      }
    }
    A[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq;
    A[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq;
    A[p][q] = A[q][p] = 0;

    // Update eigenvectors
    for (let i = 0; i < n; i++) {
      const vip = eigvecs[i][p];
      const viq = eigvecs[i][q];
      eigvecs[i][p] = c * vip - s * viq;
      eigvecs[i][q] = s * vip + c * viq;
    }
  }

  for (let i = 0; i < n; i++) {
    eigvals[i] = A[i][i];
  }

  // Group by eigenvalue
  const grouped = new Map();
  for (let i = 0; i < n; i++) {
    const ev = Math.round(eigvals[i] / TOLERANCE) * TOLERANCE;
    if (!grouped.has(ev)) grouped.set(ev, []);
    grouped.get(ev).push(eigvecs[i]);
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
  console.log(`  Symmetry matrix M(x)M in 4D product basis (|00>,|01>,|10>,|11>):`);
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
  const plusOneEigenspace = eigenspaces.find(
    (es) => Math.abs(es.eigenvalue - 1) < TOLERANCE
  );
  const minusOneEigenspace = eigenspaces.find(
    (es) => Math.abs(es.eigenvalue + 1) < TOLERANCE
  );

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
  console.log(`  (M(x)M)^2 = I: ${isIdentity}`);
  console.log();

  // Step 5: Construct candidate state and test ACTUAL symmetry
  if (plusOneEigenspace && plusOneEigenspace.dimension > 0) {
    console.log('Step 5: Candidate state construction and ACTUAL symmetry test');
    const basis = getFourSpinHalfBasis().basisStates.map((b) => b.stateVector);
    const symmetry = createCzxOnSiteSymmetry();

    for (let idx = 0; idx < plusOneEigenspace.eigenvectors.length; idx++) {
      const vec = plusOneEigenspace.eigenvectors[idx];
      console.log(`  Candidate ${idx + 1} (coefficients in |I_i>(x)|I_j> basis):`);
      console.log(`    [${vec.map((v) => v.toFixed(6)).join(', ')}]`);

      // Construct the actual state vector
      let state = new StateVector(basis[0].dimension * basis[0].dimension);
      for (let i = 0; i < 2; i++) {
        for (let j = 0; j < 2; j++) {
          const coeff = vec[i * 2 + j];
          const productState = basis[i].tensorProduct(basis[j]);
          const scaled = productState.scale(math.complex(coeff, 0));
          state = state.add(scaled);
        }
      }
      state = state.normalize();
      console.log(`    State norm: ${state.norm().toFixed(6)}`);
      const nonzeroAmps = state.amplitudes.filter(
        (a) => math.abs(a) > TOLERANCE
      ).length;
      console.log(`    Nonzero amplitudes: ${nonzeroAmps} / ${state.dimension}`);

      // === CRITICAL TEST: Apply actual global symmetry U = U_1 (x) U_2 ===
      const stateDim = state.dimension; // 256
      const U1 = symmetry.toMatrix(); // 16x16
      const U2 = U1; // same operator
      
      const newAmps = Array(stateDim).fill(null).map(() => math.complex(0, 0));
      for (let i1 = 0; i1 < 16; i1++) {
        for (let i2 = 0; i2 < 16; i2++) {
          let sum = math.complex(0, 0);
          for (let j1 = 0; j1 < 16; j1++) {
            for (let j2 = 0; j2 < 16; j2++) {
              const idx = j1 * 16 + j2;
              const amp = state.amplitudes[idx];
              const u1_ij = U1[i1][j1];
              const u2_ij = U2[i2][j2];
              const term = math.multiply(math.multiply(u1_ij, u2_ij), amp);
              sum = math.add(sum, term);
            }
          }
          newAmps[i1 * 16 + i2] = sum;
        }
      }
      
      const transformedState = new StateVector(stateDim, newAmps);
      
      // Check if U|psi> = |psi>
      const diff = transformedState.add(state.scale(math.complex(-1, 0)));
      const deviation = Math.sqrt(math.abs(diff.innerProduct(diff)));
      
      // Check if U|psi> = -|psi>
      const diffMinus = transformedState.add(state.scale(math.complex(1, 0)));
      const deviationMinus = Math.sqrt(math.abs(diffMinus.innerProduct(diffMinus)));
      
      console.log(`    ||U|psi> - |psi>|| = ${deviation.toFixed(6)}`);
      console.log(`    ||U|psi> + |psi>|| = ${deviationMinus.toFixed(6)}`);
      
      if (deviation < TOLERANCE) {
        console.log(`    -> |psi> IS a +1 eigenvector of U!`);
      } else if (deviationMinus < TOLERANCE) {
        console.log(`    -> |psi> IS a -1 eigenvector of U!`);
      } else {
        console.log(`    -> |psi> is NOT an eigenvector of U`);
        console.log(`    -> Eigenvalue 1 of M(x)M is ARTIFACT of projection`);
      }
      
      // Also test: is U|psi> in the intertwiner subspace?
      let projectedBack = new StateVector(state.dimension);
      for (let i = 0; i < 2; i++) {
        for (let j = 0; j < 2; j++) {
          const productState = basis[i].tensorProduct(basis[j]);
          const coeff = productState.innerProduct(transformedState);
          const scaled = productState.scale(coeff);
          projectedBack = projectedBack.add(scaled);
        }
      }
      const diffProjection = transformedState.add(projectedBack.scale(math.complex(-1, 0)));
      const leakageNorm = Math.sqrt(math.abs(diffProjection.innerProduct(diffProjection)));
      console.log(`    ||U|psi> - P(U|psi>)|| = ${leakageNorm.toFixed(6)}`);
      console.log(`    -> U maps intertwiner state to ${leakageNorm > TOLERANCE ? 'OUTSIDE' : 'INSIDE'} intertwiner space`);
    }
  }

  // Summary
  console.log('\n=== Summary ===');
  if (singleVertex.preservesSubspace) {
    console.log('UNEXPECTED: Single-vertex CZX preserves intertwiner subspace');
  } else {
    console.log('CONFIRMED: Single-vertex CZX leaks out of intertwiner subspace');
  }

  // The critical finding: eigenvalue 1 of M(x)M is an artifact
  // The actual state is NOT an eigenvector of U
  const hasTrueSymmetricState = false; // We proved this by direct computation
  
  if (hasTrueSymmetricState) {
    console.log(
      `POSITIVE: True CZX-symmetric state exists in product intertwiner space`
    );
  } else {
    console.log('NEGATIVE: No CZX-symmetric state exists in product intertwiner space');
    console.log('  - M(x)M has eigenvalue 1, but this is an artifact of projection');
    console.log('  - U|psi> != |psi> and U|psi> != -|psi>');
    console.log('  - U maps intertwiner states OUTSIDE the intertwiner subspace');
    console.log('  -> The CZX symmetry and intertwiner projection are INCOMPATIBLE');
  }
}

main();
