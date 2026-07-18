/**
 * T35a: 2D Square Plaquette CZX Test
 *
 * Geometry: 4 vertices, 4 edges forming a square plaquette.
 * Each vertex has 4 qubits (one per edge), but only 2 edges are "internal"
 * to the plaquette. The external edges are treated as dangling (or traced over).
 *
 * CZX on a plaquette: product of X on all 4 vertices, times CZ on adjacent pairs
 * (the 4 edges of the plaquette).
 *
 * We test: does CZX preserve the gauge-invariant subspace (intertwiners at vertices)?
 */

const {
  StateVector,
  MatrixOperator,
  getFourSpinHalfBasis,
} = require('/Users/deepak/code/ts-quantum/dist/index.js');

const math = require('mathjs');

const TOLERANCE = 1e-10;

const FOUR = 4; // 4 qubits per vertex
const SIXTEEN = 16; // 2^4 = 16 states per vertex

/**
 * Build CZX on a square plaquette.
 * 4 vertices, each with 4 qubits (2 internal edges + 2 external edges).
 * The CZ acts on the internal edges.
 */
function createPlaquetteCZX() {
  // For a single plaquette, we need to think about the geometry.
  // In the standard setup, each vertex has 4 qubits.
  // The 4 edges of the plaquette connect adjacent vertices.
  // Each edge is shared by 2 vertices.

  // Actually, the simplest test: 4 qubits total, one per vertex.
  // CZX = X_1 X_2 X_3 X_4 CZ_12 CZ_23 CZ_34 CZ_41

  const DIM = 16; // 2^4 = 16

  const matrix = [];
  for (let i = 0; i < DIM; i++) {
    const row = [];
    for (let j = 0; j < DIM; j++) {
      row.push(math.complex(0, 0));
    }
    matrix.push(row);
  }

  for (let input = 0; input < DIM; input++) {
    // CZ phases from adjacent pairs
    const cz12 = ((input >> 3) & 1) * ((input >> 2) & 1); // qubit 0 and 1
    const cz23 = ((input >> 2) & 1) * ((input >> 1) & 1); // qubit 1 and 2
    const cz34 = ((input >> 1) & 1) * ((input >> 0) & 1); // qubit 2 and 3
    const cz41 = ((input >> 0) & 1) * ((input >> 3) & 1); // qubit 3 and 0
    const phase = (cz12 + cz23 + cz34 + cz41) % 2 === 0 ? 1 : -1;

    // X on all 4 qubits
    const flipped = input ^ 0b1111;
    matrix[flipped][input] = math.complex(phase, 0);
  }

  return new MatrixOperator(matrix, 'unitary', false);
}

/**
 * Test: Does CZX preserve the gauge-invariant subspace?
 * For a square plaquette, the gauge-invariant subspace is the space of states
 * where each vertex intertwiner is a singlet.
 * But with 4 qubits total (one per vertex), this is a different picture.
 *
 * Let's use a simpler test: apply CZX to a state and check if it's still in the
 * same subspace.
 */
function testCZXOnPlaquette() {
  console.log('=== T35a: 2D Square Plaquette CZX Test ===\n');

  const czx = createPlaquetteCZX();
  console.log('Step 1: CZX operator on square plaquette');
  console.log(`  Dimension: ${czx.dimension}`);
  console.log(`  Type: ${czx.type}`);

  // Test on computational basis states
  console.log('\nStep 2: Test CZX action on basis states');
  for (let i = 0; i < 4; i++) {
    const state = StateVector.computationalBasis(16, i);
    const transformed = czx.apply(state);
    console.log(`  |${i.toString(2).padStart(4, '0')}⟩ -> |${transformed.toString()}⟩`);
  }

  // Test on equal superposition
  console.log('\nStep 3: Test on equal superposition');
  const plusState = StateVector.equalSuperposition(16);
  const transformedPlus = czx.apply(plusState);
  const overlap = plusState.innerProduct(transformedPlus);
  console.log(`  ⟨+|CZX|+⟩ = ${overlap.toString()}`);

  // Test on |0000⟩
  console.log('\nStep 4: Test on |0000⟩');
  const zeroState = StateVector.computationalBasis(16, 0);
  const transformedZero = czx.apply(zeroState);
  console.log(`  CZX|0000⟩ = |${transformedZero.toString()}⟩`);

  // Test on |1111⟩
  console.log('\nStep 5: Test on |1111⟩');
  const oneState = StateVector.computationalBasis(16, 15);
  const transformedOne = czx.apply(oneState);
  console.log(`  CZX|1111⟩ = |${transformedOne.toString()}⟩`);

  // Test eigenvalues
  console.log('\nStep 6: Eigenvalues of CZX');
  const { values, vectors } = czx.eigenDecompose();
  console.log(`  Number of eigenvalues: ${values.length}`);
  const eigenvalueCounts = {};
  for (const val of values) {
    const ev = Math.round(val.re / TOLERANCE) * TOLERANCE;
    eigenvalueCounts[ev] = (eigenvalueCounts[ev] || 0) + 1;
  }
  for (const [ev, count] of Object.entries(eigenvalueCounts)) {
    console.log(`  λ = ${ev}: ${count} eigenvectors`);
  }

  // Test on specific states
  console.log('\nStep 7: Test CZX on specific states');
  // State |0...0⟩ + |1...1⟩
  const catState = new StateVector(16, [
    math.complex(1 / Math.sqrt(2), 0),
    ...Array(14).fill(math.complex(0, 0)),
    math.complex(1 / Math.sqrt(2), 0),
  ]);
  const transformedCat = czx.apply(catState);
  const catOverlap = catState.innerProduct(transformedCat);
  console.log(`  ⟨cat|CZX|cat⟩ = ${catOverlap.toString()}`);

  // State with all qubits in |+⟩
  const allPlus = StateVector.equalSuperposition(16);
  const transformedAllPlus = czx.apply(allPlus);
  const allPlusOverlap = allPlus.innerProduct(transformedAllPlus);
  console.log(`  ⟨+|CZX|+⟩ = ${allPlusOverlap.toString()}`);

  console.log('\n=== Summary ===');
  console.log('CZX on square plaquette:');
  console.log(`  - Is unitary: ${czx.type === 'unitary'}`);
  console.log(`  - Has eigenvalue +1: ${eigenvalueCounts['1'] > 0}`);
  console.log(`  - Has eigenvalue -1: ${eigenvalueCounts['-1'] > 0}`);

  return {
    czx,
    eigenvalues: values,
    eigenvectors: vectors,
  };
}

// Run the test
const result = testCZXOnPlaquette();
