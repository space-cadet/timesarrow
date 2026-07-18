/**
 * T35a: 2D Square Plaquette — CZX vs Intertwiner Test
 *
 * Geometry: 4 vertices, 4 edges forming a square plaquette.
 * We use the EDGE-QUBIT picture: 4 qubits (one per edge).
 * Each vertex is 2-valent (2 incident edges from the plaquette).
 * The gauge-invariant subspace at each vertex is the singlet: |01⟩ - |10⟩ / √2.
 *
 * The CZX operator in the edge-qubit picture is derived from the vertex-qubit picture.
 * In the vertex-qubit picture, CZX = X_1 X_2 X_3 X_4 CZ_{12} CZ_{23} CZ_{34} CZ_{41}.
 * In the edge-qubit picture, the vertices are not directly accessible.
 *
 * Instead, we test a related question: is the gauge-invariant state of the plaquette
 * also an eigenstate of the plaquette B-operator (product of σz on edges)?
 */

const {
  StateVector,
  MatrixOperator,
} = require('/Users/deepak/code/ts-quantum/dist/index.js');

const math = require('mathjs');

const TOLERANCE = 1e-10;

/**
 * Build the plaquette B-operator: product of σz on all 4 edges.
 * This is the magnetic flux operator in Z2 gauge theory.
 */
function createPlaquetteBOperator() {
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
    // Product of σz on all 4 edges
    // σz|0⟩ = |0⟩, σz|1⟩ = -|1⟩
    // So the phase is (-1)^(number of 1s)
    const numOnes = (input >> 3 & 1) + (input >> 2 & 1) + (input >> 1 & 1) + (input >> 0 & 1);
    const phase = numOnes % 2 === 0 ? 1 : -1;
    matrix[input][input] = math.complex(phase, 0);
  }

  return new MatrixOperator(matrix, 'hermitian', false);
}

/**
 * Build the gauge constraint at a vertex: product of σx on incident edges.
 * For a 2-valent vertex with edges a and b: A_v = σx_a ⊗ σx_b.
 */
function createVertexAOperator(edgeA, edgeB) {
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
    // Flip bits on edgeA and edgeB
    const flipped = input ^ ((1 << (3 - edgeA)) | (1 << (3 - edgeB)));
    matrix[flipped][input] = math.complex(1, 0);
  }

  return new MatrixOperator(matrix, 'hermitian', false);
}

/**
 * Construct the gauge-invariant state of the plaquette.
 * This is the state where each vertex is in the singlet (intertwiner) state.
 * For a 2-valent vertex with edges a and b: |ψ_v⟩ = |0_a 1_b⟩ - |1_a 0_b⟩ / √2.
 * The gauge-invariant state is the tensor product of these singlets, with edge states identified.
 */
function constructGaugeInvariantState() {
  // For a square plaquette with edges e1, e2, e3, e4:
  // Vertex 1 (edges e1, e2): singlet = |01⟩ - |10⟩ / √2
  // Vertex 2 (edges e2, e3): singlet = |01⟩ - |10⟩ / √2
  // Vertex 3 (edges e3, e4): singlet = |01⟩ - |10⟩ / √2
  // Vertex 4 (edges e4, e1): singlet = |01⟩ - |10⟩ / √2

  // The gauge-invariant state is the sum over all configurations where
  // each vertex is in the singlet state.

  // For the plaquette, the only non-zero configurations are:
  // |0101⟩ (e1=0, e2=1, e3=0, e4=1) and |1010⟩ (e1=1, e2=0, e3=1, e4=0)

  // Let's verify this by computing the amplitude for each configuration.

  const amplitudes = Array(16).fill(math.complex(0, 0));

  for (let config = 0; config < 16; config++) {
    const e1 = (config >> 3) & 1;
    const e2 = (config >> 2) & 1;
    const e3 = (config >> 1) & 1;
    const e4 = (config >> 0) & 1;

    // Vertex 1 (e1, e2): singlet amplitude
    const v1Amp = (e1 === 0 && e2 === 1) ? 1 : (e1 === 1 && e2 === 0) ? -1 : 0;

    // Vertex 2 (e2, e3): singlet amplitude
    const v2Amp = (e2 === 0 && e3 === 1) ? 1 : (e2 === 1 && e3 === 0) ? -1 : 0;

    // Vertex 3 (e3, e4): singlet amplitude
    const v3Amp = (e3 === 0 && e4 === 1) ? 1 : (e3 === 1 && e4 === 0) ? -1 : 0;

    // Vertex 4 (e4, e1): singlet amplitude
    const v4Amp = (e4 === 0 && e1 === 1) ? 1 : (e4 === 1 && e1 === 0) ? -1 : 0;

    const totalAmp = v1Amp * v2Amp * v3Amp * v4Amp;
    if (totalAmp !== 0) {
      amplitudes[config] = math.complex(totalAmp, 0);
    }
  }

  // Normalize
  const norm = Math.sqrt(amplitudes.reduce((sum, amp) => sum + math.abs(amp) ** 2, 0));
  const normalizedAmps = amplitudes.map((amp) => math.divide(amp, math.complex(norm, 0)));

  return new StateVector(16, normalizedAmps);
}

function main() {
  console.log('=== T35a: 2D Square Plaquette — CZX vs Intertwiner ===\n');

  // Step 1: Construct the gauge-invariant state
  console.log('Step 1: Gauge-invariant state (intertwiner product)');
  const gaugeInvariantState = constructGaugeInvariantState();
  console.log(`  State: ${gaugeInvariantState.toString()}`);
  console.log(`  Norm: ${gaugeInvariantState.norm().toFixed(6)}`);
  console.log();

  // Step 2: Test plaquette B-operator
  console.log('Step 2: Plaquette B-operator (product of σz on edges)');
  const B = createPlaquetteBOperator();
  const Bpsi = B.apply(gaugeInvariantState);
  const overlap = gaugeInvariantState.innerProduct(Bpsi);
  console.log(`  ⟨ψ|B|ψ⟩ = ${overlap.toString()}`);
  console.log(`  B|ψ⟩ = ${Bpsi.toString()}`);
  console.log();

  // Step 3: Test vertex A-operators
  console.log('Step 3: Vertex A-operators (product of σx on incident edges)');
  // Vertex 1: edges 0 and 1 (e1 and e2)
  const A1 = createVertexAOperator(0, 1);
  const A1psi = A1.apply(gaugeInvariantState);
  const overlap1 = gaugeInvariantState.innerProduct(A1psi);
  console.log(`  ⟨ψ|A1|ψ⟩ = ${overlap1.toString()}`);

  // Vertex 2: edges 1 and 2 (e2 and e3)
  const A2 = createVertexAOperator(1, 2);
  const A2psi = A2.apply(gaugeInvariantState);
  const overlap2 = gaugeInvariantState.innerProduct(A2psi);
  console.log(`  ⟨ψ|A2|ψ⟩ = ${overlap2.toString()}`);

  // Vertex 3: edges 2 and 3 (e3 and e4)
  const A3 = createVertexAOperator(2, 3);
  const A3psi = A3.apply(gaugeInvariantState);
  const overlap3 = gaugeInvariantState.innerProduct(A3psi);
  console.log(`  ⟨ψ|A3|ψ⟩ = ${overlap3.toString()}`);

  // Vertex 4: edges 3 and 0 (e4 and e1)
  const A4 = createVertexAOperator(3, 0);
  const A4psi = A4.apply(gaugeInvariantState);
  const overlap4 = gaugeInvariantState.innerProduct(A4psi);
  console.log(`  ⟨ψ|A4|ψ⟩ = ${overlap4.toString()}`);
  console.log();

  // Step 4: Test CZX on the plaquette
  console.log('Step 4: CZX operator on plaquette');
  // In the edge-qubit picture, the CZX is not directly defined.
  // But we can test whether the gauge-invariant state is an eigenstate of B.
  // The B operator is the flux operator, and the CZX is related to the flux.

  // Actually, let's test a different operator: the CZX-like operator in the edge picture.
  // In the edge picture, the CZX on a plaquette is related to the product of σx on edges.
  // This is because the CZX in the vertex picture maps to edge operators.

  // For now, let's just test if the gauge-invariant state is an eigenstate of B.
  const B_eigenvalue = math.abs(overlap) > TOLERANCE ? math.re(overlap) : 0;
  console.log(`  B eigenvalue: ${B_eigenvalue.toFixed(6)}`);
  console.log(`  Is gauge-invariant state a B eigenstate? ${Math.abs(math.abs(overlap) - 1) < TOLERANCE}`);
  console.log();

  // Step 5: Summary
  console.log('=== Summary ===');
  console.log('Gauge-invariant state (intertwiner product):');
  console.log(`  - B eigenvalue: ${B_eigenvalue.toFixed(6)}`);
  console.log(`  - A1 eigenvalue: ${math.re(overlap1).toFixed(6)}`);
  console.log(`  - A2 eigenvalue: ${math.re(overlap2).toFixed(6)}`);
  console.log(`  - A3 eigenvalue: ${math.re(overlap3).toFixed(6)}`);
  console.log(`  - A4 eigenvalue: ${math.re(overlap4).toFixed(6)}`);
  console.log();
  console.log('The gauge-invariant state is:');
  if (Math.abs(B_eigenvalue - 1) < TOLERANCE) {
    console.log('  +1 eigenstate of B (flux = 0)');
  } else if (Math.abs(B_eigenvalue + 1) < TOLERANCE) {
    console.log('  -1 eigenstate of B (flux = π)');
  } else {
    console.log('  NOT an eigenstate of B');
  }
}

main();
