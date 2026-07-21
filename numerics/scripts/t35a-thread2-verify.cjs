/**
 * T35a Thread 2: Parent Hamiltonian Verification (CommonJS wrapper)
 * 
 * Uses ts-quantum's sparse Lanczos eigensolver via CommonJS require.
 */

const { 
  SparseOperator, 
  createSparseMatrix, 
  setSparseEntry,
  findLowestEigenvalues
} = require('ts-quantum');

// System parameters
const N_PLAQUETTES = 4;
const QUBITS_PER_PLAQUETTE = 4;
const N_QUBITS = N_PLAQUETTES * QUBITS_PER_PLAQUETTE;
const DIM = 2 ** N_QUBITS;

function qidx(p, s) {
  return p * QUBITS_PER_PLAQUETTE + s;
}

/**
 * Get entry from sparse matrix (helper)
 */
function getSparseEntry(matrix, row, col) {
  const entry = matrix.entries.find(e => e.row === row && e.col === col);
  return entry ? entry.value : { re: 0, im: 0 };
}

/**
 * Build a Pauli string operator as a sparse matrix.
 */
function buildPauliStringSparse(paulis, qubits) {
  const P = createSparseMatrix(DIM, DIM);
  
  for (let state = 0; state < DIM; state++) {
    let newState = state;
    let phase = 1;
    
    for (let i = 0; i < paulis.length; i++) {
      const q = qubits[i];
      const bit = (state >> (N_QUBITS - 1 - q)) & 1;
      
      if (paulis[i] === 'X') {
        newState ^= (1 << (N_QUBITS - 1 - q));
      } else if (paulis[i] === 'Z') {
        if (bit === 1) phase *= -1;
      }
    }
    
    setSparseEntry(P, newState, state, { re: phase, im: 0 });
  }
  
  return P;
}

/**
 * Build the parent Hamiltonian as a sparse operator.
 */
function buildParentHamiltonian() {
  const H_sparse = createSparseMatrix(DIM, DIM);
  
  for (let p = 0; p < N_PLAQUETTES; p++) {
    const qubits = [qidx(p, 0), qidx(p, 1), qidx(p, 2), qidx(p, 3)];
    
    const pauliStrings = [
      ['X', 'X', 'X', 'X'],
      ['Z', 'Z', 'I', 'I'],
      ['I', 'Z', 'Z', 'I'],
      ['I', 'I', 'Z', 'Z']
    ];
    
    for (const paulis of pauliStrings) {
      const P_sparse = buildPauliStringSparse(paulis, qubits);
      
      for (const entry of P_sparse.entries) {
        const existing = getSparseEntry(H_sparse, entry.row, entry.col);
        const newValue = {
          re: existing.re + entry.value.re * (-0.5),
          im: existing.im + entry.value.im * (-0.5)
        };
        setSparseEntry(H_sparse, entry.row, entry.col, newValue);
      }
    }
    
    for (let i = 0; i < DIM; i++) {
      const existing = getSparseEntry(H_sparse, i, i);
      setSparseEntry(H_sparse, i, i, { re: existing.re + 2, im: 0 });
    }
  }
  
  return new SparseOperator(H_sparse, 'hermitian');
}

/**
 * Build the CZX ground state: |Ψ⟩ = ⊗_p |GHZ_p⟩
 */
function buildCZXGroundState() {
  const amplitudes = Array(DIM).fill(null).map(() => ({ re: 0, im: 0 }));
  
  for (let config = 0; config < (1 << N_PLAQUETTES); config++) {
    let state = 0;
    for (let p = 0; p < N_PLAQUETTES; p++) {
      const bit = (config >> p) & 1;
      for (let s = 0; s < QUBITS_PER_PLAQUETTE; s++) {
        state |= bit << (N_QUBITS - 1 - qidx(p, s));
      }
    }
    amplitudes[state] = { re: 1 / Math.sqrt(1 << N_PLAQUETTES), im: 0 };
  }
  
  return {
    objectType: 'state',
    dimension: DIM,
    amplitudes,
    getAmplitudes: () => amplitudes,
    getState: (i) => amplitudes[i],
    setState: (i, v) => { amplitudes[i] = v; },
    innerProduct: () => ({ re: 0, im: 0 }),
    norm: () => 1,
    normalize: () => ({ objectType: 'state', dimension: DIM, amplitudes }),
    tensorProduct: () => ({ objectType: 'state', dimension: DIM, amplitudes }),
    scale: () => ({ objectType: 'state', dimension: DIM, amplitudes }),
    add: () => ({ objectType: 'state', dimension: DIM, amplitudes }),
    equals: () => true,
    isZero: () => false,
    toArray: () => amplitudes,
    toString: () => 'CZX Ground State'
  };
}

/**
 * Main verification function
 */
async function verifyParentHamiltonian() {
  console.log('='.repeat(70));
  console.log('T35a Thread 2: Parent Hamiltonian Verification');
  console.log('Using ts-quantum sparse Lanczos eigensolver');
  console.log('='.repeat(70));
  console.log(`System: 2×2 torus, ${N_QUBITS} qubits, Hilbert space dim = ${DIM}`);
  console.log();
  
  console.log('Building parent Hamiltonian H = Σ_p h_p...');
  const H = buildParentHamiltonian();
  console.log(`  Nonzero elements: ${H.getSparseMatrix().nnz}`);
  console.log();
  
  // Check 1: H|ψ₀⟩ = 0
  console.log('Check 1: CZX state is ground state?');
  const psi0 = buildCZXGroundState();
  const H_psi = H.apply(psi0);
  const norm = Math.sqrt(H_psi.getAmplitudes().reduce((sum, a) => sum + a.re * a.re + a.im * a.im, 0));
  console.log(`  ||H|ψ₀⟩|| = ${norm.toExponential(2)}`);
  console.log(`  Result: ${norm < 1e-10 ? 'PASS ✓' : 'FAIL ✗'}`);
  console.log();
  
  // Check 2: Find lowest eigenvalues using sparse Lanczos
  console.log('Check 2: Low-energy spectrum (sparse Lanczos)...');
  const result = findLowestEigenvalues(H.getSparseMatrix(), 5, { 
    seed: 42,
    maxIterations: 100,
    tolerance: 1e-10
  });
  
  console.log('  Lowest 5 eigenvalues:');
  for (let i = 0; i < result.eigenvalues.length; i++) {
    const marker = Math.abs(result.eigenvalues[i]) < 1e-10 ? ' ← GROUND' : '';
    console.log(`    E_${i} = ${result.eigenvalues[i].toFixed(10)}${marker}`);
  }
  
  const zeroCount = result.eigenvalues.filter(e => Math.abs(e) < 1e-10).length;
  const gap = zeroCount > 0 && zeroCount < result.eigenvalues.length
    ? result.eigenvalues[zeroCount] - result.eigenvalues[zeroCount - 1]
    : result.eigenvalues[1] - result.eigenvalues[0];
  
  console.log(`  Zero eigenvalues: ${zeroCount}`);
  console.log(`  Gap to first excited: ${gap.toFixed(6)}`);
  console.log(`  Result: ${zeroCount === 1 && gap > 1e-10 ? 'PASS (unique + gapped) ✓' : 'PARTIAL'}`);
  console.log();
  
  // Check 3: Positive semidefinite
  console.log('Check 3: H is positive semidefinite?');
  console.log(`  Minimum eigenvalue: ${result.eigenvalues[0].toFixed(10)}`);
  console.log(`  Result: ${result.eigenvalues[0] > -1e-10 ? 'PASS ✓' : 'FAIL ✗'}`);
  console.log();
  
  // Summary
  console.log('='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));
  const checks = [
    ['Ground state (H|ψ⟩ = 0)', norm < 1e-10],
    ['Unique ground state', zeroCount === 1],
    ['Gapped', gap > 1e-10],
    ['Positive semidefinite', result.eigenvalues[0] > -1e-10]
  ];
  
  for (const [name, passed] of checks) {
    console.log(`  ${name}: ${passed ? '✓' : '✗'}`);
  }
  
  const allPass = checks.every(([, p]) => p);
  console.log();
  console.log(`Overall: ${allPass ? 'PASS (valid parent Hamiltonian) ✓' : 'FAIL'}`);
}

// Run verification
verifyParentHamiltonian().catch(console.error);
