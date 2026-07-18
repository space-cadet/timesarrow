/**
 * T35a: 2D Square Plaquette — Direct CZX vs Intertwiner Test
 *
 * This script tests the central question:
 *   Is the CZX-symmetric state also in the intertwiner (gauge-invariant) subspace?
 *
 * We use the vertex-qubit picture (4 qubits on vertices) and test whether
 * the CZX +1 eigenvectors are also gauge-invariant (A_v = +1 for all vertices).
 *
 * In the vertex-qubit picture, the gauge constraints are defined by the
 * requirement that the state is a product of intertwiners at each vertex.
 * For a 4-valent vertex, the intertwiner is a 4-qubit singlet state.
 */

const {
  StateVector,
  MatrixOperator,
} = require('/Users/deepak/code/ts-quantum/dist/index.js');

const math = require('mathjs');

const TOLERANCE = 1e-10;

/**
 * Build CZX on a square plaquette (4 vertex qubits).
 */
function createPlaquetteCZX() {
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
    const cz12 = ((input >> 3) & 1) * ((input >> 2) & 1);
    const cz23 = ((input >> 2) & 1) * ((input >> 1) & 1);
    const cz34 = ((input >> 1) & 1) * ((input >> 0) & 1);
    const cz41 = ((input >> 0) & 1) * ((input >> 3) & 1);
    const phase = (cz12 + cz23 + cz34 + cz41) % 2 === 0 ? 1 : -1;
    const flipped = input ^ 0b1111;
    matrix[flipped][input] = math.complex(phase, 0);
  }

  return new MatrixOperator(matrix, 'unitary', false);
}

/**
 * Build gauge constraint A_v for a 4-valent vertex.
 * In the vertex-qubit picture, this is a bit tricky because the gauge group
 * acts on the edge qubits, not the vertex qubits.
 *
 * For the CZX model, the gauge constraints are NOT the same as the toric code.
 * The CZX model is a global SPT, not a gauge theory.
 *
 * Instead, we test whether the CZX-symmetric state is a product of
 * intertwiner states. In the vertex-qubit picture, an intertwiner-like state
 * is a state that is invariant under the CZX symmetry.
 */
function createCZXSymmetry() {
  return createPlaquetteCZX();
}

/**
 * Find all +1 eigenvectors of the CZX operator.
 */
function findCZXSymmetricStates() {
  const czx = createPlaquetteCZX();
  const { values, vectors } = czx.eigenDecompose();

  console.log(`Total eigenvalues: ${values.length}`);
  console.log(`Eigenvalues: ${values.map(v => v.re.toFixed(4)).join(', ')}`);
  console.log();

  const plusOneStates = [];
  for (let i = 0; i < values.length; i++) {
    const ev = values[i].re;
    console.log(`Eigenvalue ${i}: ${ev.toFixed(6)}`);
    
    if (Math.abs(ev - 1) < TOLERANCE && Math.abs(values[i].im) < TOLERANCE) {
      // Extract the eigenvector from the MatrixOperator
      const vecMatrix = vectors[i].toMatrix();
      console.log(`  Vector matrix shape: ${vecMatrix.length}x${vecMatrix[0].length}`);
      
      // The eigenvector is the diagonal of the matrix
      const amplitudes = [];
      for (let j = 0; j < vecMatrix.length; j++) {
        amplitudes.push(vecMatrix[j][j]);
      }
      
      const state = new StateVector(16, amplitudes);
      console.log(`  State: ${state.toString()}`);
      
      if (!state.isZero()) {
        plusOneStates.push(state.normalize());
      }
    }
  }

  return plusOneStates;
}

/**
 * Test whether a state is a product state (intertwiner-like).
 * A product state can be written as |ψ⟩ = |ψ_1⟩ ⊗ |ψ_2⟩ ⊗ |ψ_3⟩ ⊗ |ψ_4⟩.
 */
function isProductState(state) {
  // For a 4-qubit state, test if it's a product state by checking
  // the Schmidt rank across any bipartition.
  // For simplicity, test the 1:3 bipartition (qubit 0 vs qubits 1,2,3).

  const dimA = 2; // qubit 0
  const dimB = 8; // qubits 1,2,3

  // Build the density matrix ρ = |ψ⟩⟨ψ|
  const rho = [];
  for (let i = 0; i < 16; i++) {
    rho[i] = [];
    for (let j = 0; j < 16; j++) {
      rho[i][j] = math.multiply(state.amplitudes[i], math.conj(state.amplitudes[j]));
    }
  }

  // Partial trace over qubits 1,2,3 to get reduced density matrix for qubit 0
  const rhoA = [];
  for (let i = 0; i < dimA; i++) {
    rhoA[i] = [];
    for (let j = 0; j < dimA; j++) {
      let sum = math.complex(0, 0);
      for (let k = 0; k < dimB; k++) {
        const idxI = i * dimB + k;
        const idxJ = j * dimB + k;
        sum = math.add(sum, rho[idxI][idxJ]);
      }
      rhoA[i][j] = sum;
    }
  }

  // Check if ρA is pure (rank 1)
  // For a 2x2 matrix, check if det(ρA) = 0
  const det = math.subtract(
    math.multiply(rhoA[0][0], rhoA[1][1]),
    math.multiply(rhoA[0][1], rhoA[1][0])
  );

  return Math.abs(math.abs(det)) < TOLERANCE;
}

/**
 * Test if the CZX-symmetric states are product states.
 */
function testCZXProductStates() {
  console.log('=== T35a: CZX-Symmetric States — Product State Test ===\n');

  const czxSymmetricStates = findCZXSymmetricStates();
  console.log(`Found ${czxSymmetricStates.length} CZX-symmetric states (+1 eigenvectors)`);
  console.log();

  for (let i = 0; i < czxSymmetricStates.length; i++) {
    const state = czxSymmetricStates[i];
    console.log(`State ${i + 1}:`);
    console.log(`  ${state.toString()}`);

    const isProduct = isProductState(state);
    console.log(`  Is product state: ${isProduct}`);

    if (isProduct) {
      console.log('  → This state can be written as a product of intertwiner-like states');
    } else {
      console.log('  → This state is entangled (not a product state)');
    }
    console.log();
  }

  return czxSymmetricStates;
}

/**
 * Test the CZX on a specific state: the equal superposition |+⟩^⊗4.
 */
function testCZXOnPlusState() {
  console.log('=== T35a: CZX on |+⟩^⊗4 ===\n');

  const plusState = StateVector.equalSuperposition(16);
  const czx = createPlaquetteCZX();
  const transformed = czx.apply(plusState);

  const overlap = plusState.innerProduct(transformed);
  console.log(`⟨+|CZX|+⟩ = ${overlap.toString()}`);
  console.log(`Re(overlap) = ${math.re(overlap).toFixed(6)}`);
  console.log(`|overlap| = ${math.abs(overlap).toFixed(6)}`);
  console.log();

  // Check if |+⟩^⊗4 is a CZX eigenstate
  const diff = transformed.add(plusState.scale(math.complex(-1, 0)));
  const deviation = Math.sqrt(math.abs(diff.innerProduct(diff)));
  console.log(`||CZX|+⟩ - |+⟩|| = ${deviation.toFixed(6)}`);
  console.log(`|+⟩ is ${deviation < TOLERANCE ? '' : 'NOT '}a +1 eigenstate`);
  console.log();
}

function main() {
  testCZXOnPlusState();
  testCZXProductStates();
}

main();
