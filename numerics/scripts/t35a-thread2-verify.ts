/**
 * T35a Thread 2: Parent Hamiltonian Verification
 * 
 * Uses ts-quantum's sparse Lanczos eigensolver to verify:
 * 1. The CZX state is a ground state (H|Ψ⟩ = 0)
 * 2. The ground state is unique
 * 3. The Hamiltonian is gapped
 * 
 * The parent Hamiltonian for the CZX state on a 2×2 torus is:
 *   H = Σ_p h_p
 * where each plaquette term is:
 *   h_p = (1/2)[(I - XXXX) + (I - ZZII) + (I - IZZI) + (I - IIZZ)]
 * acting on the 4 qubits of plaquette p.
 */

import { 
  SparseOperator, 
  createSparseMatrix, 
  setSparseEntry,
  findLowestEigenvalues,
  IStateVector
} from 'ts-quantum';
import * as math from 'mathjs';

// System parameters
const N_PLAQUETTES = 4;
const QUBITS_PER_PLAQUETTE = 4;
const N_QUBITS = N_PLAQUETTES * QUBITS_PER_PLAQUETTE;
const DIM = 2 ** N_QUBITS;

function qidx(p: number, s: number): number {
  return p * QUBITS_PER_PLAQUETTE + s;
}

/**
 * Build the parent Hamiltonian as a sparse operator.
 * H = Σ_p h_p where h_p is the GHZ parent Hamiltonian on plaquette p.
 */
function buildParentHamiltonian(): SparseOperator {
  const H_sparse = createSparseMatrix(DIM, DIM);
  
  // Pauli matrices as sparse operators
  const I = [[{ re: 1, im: 0 }, { re: 0, im: 0 }], [{ re: 0, im: 0 }, { re: 1, im: 0 }]];
  const X = [[{ re: 0, im: 0 }, { re: 1, im: 0 }], [{ re: 1, im: 0 }, { re: 0, im: 0 }]];
  const Z = [[{ re: 1, im: 0 }, { re: 0, im: 0 }], [{ re: 0, im: 0 }, { re: -1, im: 0 }]];
  
  for (let p = 0; p < N_PLAQUETTES; p++) {
    const qubits = [qidx(p, 0), qidx(p, 1), qidx(p, 2), qidx(p, 3)];
    
    // h_p = 2I - (1/2)(XXXX + ZZII + IZZI + IIZZ)
    // We build each Pauli string as a sparse operator and add to H
    
    const pauliStrings = [
      ['X', 'X', 'X', 'X'],
      ['Z', 'Z', 'I', 'I'],
      ['I', 'Z', 'Z', 'I'],
      ['I', 'I', 'Z', 'Z']
    ];
    
    for (const paulis of pauliStrings) {
      // Build the sparse Pauli string operator
      const P_sparse = buildPauliStringSparse(paulis, qubits);
      
      // Add -0.5 * P to H
      for (const entry of P_sparse.entries) {
        const existing = getSparseEntry(H_sparse, entry.row, entry.col);
        const newValue = math.add(existing, math.multiply(entry.value, -0.5)) as math.Complex;
        setSparseEntry(H_sparse, entry.row, entry.col, newValue);
      }
    }
    
    // Add 2I for this plaquette
    for (let i = 0; i < DIM; i++) {
      const existing = getSparseEntry(H_sparse, i, i);
      const newValue = math.add(existing, 2) as math.Complex;
      setSparseEntry(H_sparse, i, i, newValue);
    }
  }
  
  return new SparseOperator(H_sparse, 'hermitian');
}

/**
 * Build a Pauli string operator as a sparse matrix.
 * paulis: array of 'I', 'X', 'Z', 'Y'
 * qubits: array of qubit indices
 */
function buildPauliStringSparse(paulis: string[], qubits: number[]) {
  const P = createSparseMatrix(DIM, DIM);
  
  // Iterate over all basis states
  for (let state = 0; state < DIM; state++) {
    let newState = state;
    let phase = 1;
    
    for (let i = 0; i < paulis.length; i++) {
      const q = qubits[i];
      const bit = (state >> (N_QUBITS - 1 - q)) & 1;
      
      if (paulis[i] === 'X') {
        newState ^= (1 << (N_QUBITS - 1 - q));
      } else if (paulis[i] === 'Z') {
        if (bit === 1) {
          phase *= -1;
        }
      }
      // 'I' does nothing
    }
    
    setSparseEntry(P, newState, state, math.complex(phase, 0));
  }
  
  return P;
}

/**
 * Get entry from sparse matrix (helper)
 */
function getSparseEntry(matrix: any, row: number, col: number) {
  const entry = matrix.entries.find((e: any) => e.row === row && e.col === col);
  return entry ? entry.value : math.complex(0, 0);
}

/**
 * Build the CZX ground state: |Ψ⟩ = ⊗_p |GHZ_p⟩
 */
function buildCZXGroundState(): IStateVector {
  const amplitudes: math.Complex[] = Array(DIM).fill(null).map(() => math.complex(0, 0));
  
  // All plaquettes must have uniform bits (all 0 or all 1)
  for (let config = 0; config < (1 << N_PLAQUETTES); config++) {
    let state = 0;
    for (let p = 0; p < N_PLAQUETTES; p++) {
      const bit = (config >> p) & 1;
      for (let s = 0; s < QUBITS_PER_PLAQUETTE; s++) {
        state |= bit << (N_QUBITS - 1 - qidx(p, s));
      }
    }
    amplitudes[state] = math.complex(1 / Math.sqrt(1 << N_PLAQUETTES), 0);
  }
  
  return {
    objectType: 'state',
    dimension: DIM,
    amplitudes,
    getAmplitudes: () => amplitudes,
    getState: (i: number) => amplitudes[i],
    setState: (i: number, v: math.Complex) => { amplitudes[i] = v; },
    innerProduct: () => math.complex(0, 0),
    norm: () => 1,
    normalize: () => ({ objectType: 'state', dimension: DIM, amplitudes } as any),
    tensorProduct: () => ({ objectType: 'state', dimension: DIM, amplitudes } as any),
    scale: () => ({ objectType: 'state', dimension: DIM, amplitudes } as any),
    add: () => ({ objectType: 'state', dimension: DIM, amplitudes } as any),
    equals: () => true,
    isZero: () => false,
    toArray: () => amplitudes,
    toString: () => 'CZX Ground State'
  } as IStateVector;
}

/**
 * Main verification function
 */
async function verifyParentHamiltonian() {
  console.log('=' .repeat(70));
  console.log('T35a Thread 2: Parent Hamiltonian Verification');
  console.log('Using ts-quantum sparse Lanczos eigensolver');
  console.log('=' .repeat(70));
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
  console.log('=' .repeat(70));
  console.log('SUMMARY');
  console.log('=' .repeat(70));
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
