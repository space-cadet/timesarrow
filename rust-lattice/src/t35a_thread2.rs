use ndarray::{Array1, Array2, s};
use rand::SeedableRng;
use rand::rngs::StdRng;
use rand::distr::{Distribution, Uniform};
use std::f64;

const N_PLAQUETTES: usize = 4;
const QUBITS_PER_PLAQUETTE: usize = 4;
const N_QUBITS: usize = N_PLAQUETTES * QUBITS_PER_PLAQUETTE;
const DIM: usize = 1 << N_QUBITS; // 65536

fn qidx(p: usize, s: usize) -> usize {
    p * QUBITS_PER_PLAQUETTE + s
}

/// Apply a Pauli string to a state vector.
/// `paulis`: slice of 'I', 'X', 'Z', 'Y'
/// `qubits`: which qubits the Paulis act on
fn apply_pauli_string(state: &Array1<f64>, paulis: &[char], qubits: &[usize]) -> Array1<f64> {
    let mut result = Array1::zeros(DIM);
    
    for idx in 0..DIM {
        if state[idx] == 0.0 {
            continue;
        }
        let mut new_idx = idx;
        let mut phase = 1.0;
        
        for (p, &q) in paulis.iter().zip(qubits.iter()) {
            let bit = (idx >> (N_QUBITS - 1 - q)) & 1;
            match p {
                'X' => new_idx ^= 1 << (N_QUBITS - 1 - q),
                'Z' => if bit == 1 { phase *= -1.0; }
                'I' => {}
                _ => panic!("Unknown Pauli: {}", p),
            }
        }
        result[new_idx] += phase * state[idx];
    }
    
    result
}

/// Apply plaquette Hamiltonian h_p to a state vector.
fn apply_plaquette_hamiltonian(state: &Array1<f64>, p: usize) -> Array1<f64> {
    let qubits: Vec<usize> = (0..4).map(|s| qidx(p, s)).collect();
    
    let pauli_strings: Vec<Vec<char>> = vec![
        vec!['X', 'X', 'X', 'X'],
        vec!['Z', 'Z', 'I', 'I'],
        vec!['I', 'Z', 'Z', 'I'],
        vec!['I', 'I', 'Z', 'Z'],
    ];
    
    // h_p = 2I - 0.5 * sum(Pauli strings)
    let mut result = state * 2.0;
    
    for paulis in &pauli_strings {
        let qubits_slice: Vec<char> = paulis.clone();
        let ps = apply_pauli_string(state, &qubits_slice, &qubits);
        result = result - ps * 0.5;
    }
    
    result
}

/// Apply full parent Hamiltonian H = Σ_p h_p
fn apply_parent_hamiltonian(state: &Array1<f64>) -> Array1<f64> {
    let mut result = Array1::zeros(DIM);
    for p in 0..N_PLAQUETTES {
        result = result + apply_plaquette_hamiltonian(state, p);
    }
    result
}

/// Build the CZX ground state: |Ψ⟩ = ⊗_p |GHZ_p⟩
fn build_czx_ground_state() -> Array1<f64> {
    let mut amplitudes = Array1::zeros(DIM);
    let norm = 1.0 / ((1 << N_PLAQUETTES) as f64).sqrt();
    
    for config in 0..(1 << N_PLAQUETTES) {
        let mut state = 0usize;
        for p in 0..N_PLAQUETTES {
            let bit = (config >> p) & 1;
            for s in 0..QUBITS_PER_PLAQUETTE {
                state |= bit << (N_QUBITS - 1 - qidx(p, s));
            }
        }
        amplitudes[state] = norm;
    }
    
    amplitudes
}

/// Compute dot product ⟨a|b⟩
fn dot(a: &Array1<f64>, b: &Array1<f64>) -> f64 {
    a.iter().zip(b.iter()).map(|(&x, &y)| x * y).sum()
}

/// Compute norm ||v||
fn norm(v: &Array1<f64>) -> f64 {
    dot(v, v).sqrt()
}

/// Lanczos iteration for finding lowest eigenvalues
/// Returns: (eigenvalues, eigenvectors, iterations, converged)
fn lanczos_lowest(
    apply_h: &dyn Fn(&Array1<f64>) -> Array1<f64>,
    dim: usize,
    num_eigenvalues: usize,
    max_iterations: usize,
    tolerance: f64,
    seed: u64,
) -> (Vec<f64>, Vec<Array1<f64>>, usize, bool) {
    let mut rng = StdRng::seed_from_u64(seed);
    let uniform = Uniform::new_inclusive(-1.0f64, 1.0).unwrap();
    
    // Initial random vector
    let mut v_prev = Array1::from_vec((0..dim).map(|_| uniform.sample(&mut rng)).collect::<Vec<_>>());
    v_prev = v_prev.clone() / norm(&v_prev);
    
    let mut alphas = Vec::with_capacity(max_iterations);
    let mut betas = Vec::with_capacity(max_iterations);
    let mut vs: Vec<Array1<f64>> = Vec::with_capacity(max_iterations);
    vs.push(v_prev.clone());
    
    let mut converged = false;
    let mut it = 0;
    
    for j in 0..max_iterations {
        it = j + 1;
        
        // w = H * v_j
        let w = apply_h(&v_prev);
        
        // α_j = ⟨v_j|H|v_j⟩
        let alpha = dot(&v_prev, &w);
        alphas.push(alpha);
        
        // w = w - α_j * v_j - β_{j-1} * v_{j-1}
        let mut w = w - &v_prev * alpha;
        if j > 0 {
            w = w - &vs[j - 1] * betas[j - 1];
        }
        
        // Full reorthogonalization
        for vi in &vs {
            let proj = dot(vi, &w);
            w = w - vi * proj;
        }
        
        // β_j = ||w||
        let beta = norm(&w);
        betas.push(beta);
        
        if beta < tolerance {
            converged = true;
            break;
        }
        
        // v_{j+1} = w / β_j
        v_prev = w / beta;
        vs.push(v_prev.clone());
        
        // Check convergence of eigenvalues every 10 iterations
        if it >= num_eigenvalues && it % 10 == 0 {
            let (eigs, _) = diagonalize_tridiagonal(&alphas, &betas[..alphas.len()]);
            if eigs.len() >= num_eigenvalues {
                // Could add more sophisticated convergence check here
            }
        }
    }
    
    // Diagonalize the tridiagonal matrix T
    let (eigenvalues, eigenvectors_t) = diagonalize_tridiagonal(&alphas, &betas[..alphas.len()]);
    
    // Transform eigenvectors from T-basis to original basis
    let mut eigenvectors = Vec::with_capacity(num_eigenvalues);
    for k in 0..num_eigenvalues.min(eigenvalues.len()) {
        let mut v = Array1::zeros(dim);
        for (i, vi) in vs.iter().enumerate() {
            v = v + vi * eigenvectors_t[[i, k]];
        }
        v = v.clone() / norm(&v);
        eigenvectors.push(v);
    }
    
    (eigenvalues, eigenvectors, it, converged)
}

/// Diagonalize a symmetric tridiagonal matrix.
/// T has alphas on diagonal and betas on off-diagonal.
/// Returns (eigenvalues, eigenvectors) where eigenvalues are sorted ascending.
fn diagonalize_tridiagonal(alphas: &[f64], betas: &[f64]) -> (Vec<f64>, Array2<f64>) {
    let n = alphas.len();
    
    // Build dense T matrix
    let mut t = Array2::zeros((n, n));
    for i in 0..n {
        t[[i, i]] = alphas[i];
        if i < n - 1 {
            t[[i, i + 1]] = betas[i];
            t[[i + 1, i]] = betas[i];
        }
    }
    
    // Use QR iteration (simple implementation)
    // For small n, this is fine
    qr_algorithm(t, 1000, 1e-12)
}

/// Simple QR algorithm for symmetric matrices.
fn qr_algorithm(mut a: Array2<f64>, max_iter: usize, tol: f64) -> (Vec<f64>, Array2<f64>) {
    let n = a.nrows();
    let mut q_total = Array2::eye(n);
    
    for _ in 0..max_iter {
        let (q, r) = gram_schmidt_qr(&a);
        a = r.dot(&q);
        q_total = q_total.dot(&q);
        
        // Check off-diagonal convergence
        let mut off_diag_norm = 0.0;
        for i in 0..n {
            for j in 0..i {
                off_diag_norm += a[[i, j]].powi(2);
            }
        }
        if off_diag_norm.sqrt() < tol {
            break;
        }
    }
    
    // Extract eigenvalues (diagonal)
    let mut eigenvalues: Vec<f64> = (0..n).map(|i| a[[i, i]]).collect();
    eigenvalues.sort_by(|a, b| a.partial_cmp(b).unwrap());
    
    // Sort eigenvectors accordingly
    let mut indices: Vec<usize> = (0..n).collect();
    indices.sort_by(|&i, &j| {
        let vi = a[[i, i]];
        let vj = a[[j, j]];
        vi.partial_cmp(&vj).unwrap()
    });
    
    let mut sorted_q = Array2::zeros((n, n));
    for (new_col, &old_col) in indices.iter().enumerate() {
        for row in 0..n {
            sorted_q[[row, new_col]] = q_total[[row, old_col]];
        }
    }
    
    (eigenvalues, sorted_q)
}

/// QR decomposition via Gram-Schmidt.
fn gram_schmidt_qr(a: &Array2<f64>) -> (Array2<f64>, Array2<f64>) {
    let (m, n) = a.dim();
    let mut q = Array2::zeros((m, n));
    let mut r = Array2::zeros((n, n));
    
    for j in 0..n {
        let mut v = a.slice(s![.., j]).to_owned();
        for i in 0..j {
            let q_i = q.slice(s![.., i]);
            r[[i, j]] = q_i.dot(&v);
            v = v - &q_i * r[[i, j]];
        }
        r[[j, j]] = norm(&v);
        if r[[j, j]] > 1e-15 {
            q.slice_mut(s![.., j]).assign(&(v / r[[j, j]]));
        }
    }
    
    (q, r)
}

fn main() {
    println!("{}", "=".repeat(70));
    println!("T35a Thread 2: Parent Hamiltonian Verification (Rust)");
    println!("Matrix-free Lanczos eigensolver");
    println!("{}", "=".repeat(70));
    println!("System: 2×2 torus, {} qubits, Hilbert space dim = {}", N_QUBITS, DIM);
    println!();
    
    // Check 1: H|ψ₀⟩ = 0
    println!("Check 1: CZX state is ground state?");
    let psi_0 = build_czx_ground_state();
    let h_psi = apply_parent_hamiltonian(&psi_0);
    let norm_h_psi = norm(&h_psi);
    println!("  ||H|ψ₀⟩|| = {:.2e}", norm_h_psi);
    println!("  Result: {}", if norm_h_psi < 1e-10 { "PASS ✓" } else { "FAIL ✗" });
    println!();
    
    // Check 2: Lanczos for lowest eigenvalues
    println!("Check 2: Low-energy spectrum (Lanczos)...");
    let (eigenvalues, _eigenvectors, iters, converged) = lanczos_lowest(
        &|v| apply_parent_hamiltonian(v),
        DIM,
        5,
        100,
        1e-10,
        42,
    );
    
    println!("  Lanczos iterations: {}", iters);
    println!("  Converged: {}", converged);
    println!("  Lowest 5 eigenvalues:");
    for (i, &e) in eigenvalues.iter().enumerate().take(5) {
        let marker = if e.abs() < 1e-10 { " ← GROUND" } else { "" };
        println!("    E_{} = {:.10}{}", i, e, marker);
    }
    
    let zero_count = eigenvalues.iter().filter(|&&e| e.abs() < 1e-10).count();
    let gap = if zero_count > 0 && zero_count < eigenvalues.len() {
        eigenvalues[zero_count] - eigenvalues[zero_count - 1]
    } else if eigenvalues.len() > 1 {
        eigenvalues[1] - eigenvalues[0]
    } else {
        0.0
    };
    
    println!("  Zero eigenvalues: {}", zero_count);
    println!("  Gap to first excited: {:.6}", gap);
    println!("  Result: {}", if zero_count == 1 && gap > 1e-10 { "PASS (unique + gapped) ✓" } else { "PARTIAL" });
    println!();
    
    // Check 3: Positive semidefinite
    println!("Check 3: H is positive semidefinite?");
    println!("  Minimum eigenvalue: {:.10}", eigenvalues[0]);
    println!("  Result: {}", if eigenvalues[0] > -1e-10 { "PASS ✓" } else { "FAIL ✗" });
    println!();
    
    // Check 4: Do plaquette terms commute?
    println!("Check 4: Do local terms commute?");
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new_inclusive(-1.0f64, 1.0).unwrap();
    let test_state: Array1<f64> = Array1::from_vec(
        (0..DIM).map(|_| uniform.sample(&mut rng)).collect::<Vec<_>>()
    );
    let test_state = test_state.clone() / norm(&test_state);
    
    let mut all_commute = true;
    for i in 0..4 {
        for j in (i+1)..4 {
            let h_i_h_j = apply_plaquette_hamiltonian(
                &apply_plaquette_hamiltonian(&test_state, j), i);
            let h_j_h_i = apply_plaquette_hamiltonian(
                &apply_plaquette_hamiltonian(&test_state, i), j);
            let diff = norm(&(h_i_h_j - h_j_h_i));
            if diff > 1e-10 {
                println!("  ||[h_{}, h_{}]|| = {:.6} — DO NOT COMMUTE", i, j, diff);
                all_commute = false;
            } else {
                println!("  ||[h_{}, h_{}]|| = {:.2e} — commute", i, j, diff);
            }
        }
    }
    println!("  Result: {}", if all_commute { "PASS ✓" } else { "FAIL ✗" });
    println!();
    
    // Summary
    println!("{}", "=".repeat(70));
    println!("SUMMARY");
    println!("{}", "=".repeat(70));
    let checks = [
        ("Ground state (H|ψ⟩ = 0)", norm_h_psi < 1e-10),
        ("Unique ground state", zero_count == 1),
        ("Gapped", gap > 1e-10),
        ("Positive semidefinite", eigenvalues[0] > -1e-10),
        ("Local terms commute", all_commute),
    ];
    
    for (name, passed) in &checks {
        println!("  {}: {}", name, if *passed { "✓" } else { "✗" });
    }
    
    let all_pass = checks.iter().all(|(_, p)| *p);
    println!();
    println!("Overall: {}", if all_pass { "PASS (valid parent Hamiltonian) ✓" } else { "FAIL" });
}
