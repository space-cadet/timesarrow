/// T35b Gate 1: Four-Valent Square-Lattice Intertwiner Test
/// Dense exact diagonalization for L=2, matrix-free Lanczos for L=3
///
/// Tests whether U = X^{⊗N} · U_CZ preserves the SU(2) intertwiner subspace

use ndarray::Array2;
use rand::SeedableRng;
use rand::rngs::StdRng;
use rand::distr::{Distribution, Uniform};
use std::f64;

// ─── 1. SINGLET PROJECTOR ───

fn build_singlet_projector() -> Array2<f64> {
    let dim = 16usize;
    let mut sx = Array2::<f64>::zeros((dim, dim));
    let mut sz = Array2::<f64>::zeros((dim, dim));
    let mut sy_im = Array2::<f64>::zeros((dim, dim));
    
    for q in 0..4 {
        let bit_pos = 3 - q;
        for i in 0..dim {
            let j = i ^ (1 << bit_pos);
            sx[[i, j]] += 0.5;
            let bit = (i >> bit_pos) & 1;
            sz[[i, i]] += if bit == 1 { -0.5 } else { 0.5 };
            let flipped = i ^ (1 << bit_pos);
            let bit_i = (i >> bit_pos) & 1;
            if bit_i == 0 { sy_im[[i, flipped]] += 0.5; }
            else { sy_im[[i, flipped]] -= 0.5; }
        }
    }
    
    let mut s2 = Array2::<f64>::zeros((dim, dim));
    for i in 0..dim { for j in 0..dim { for k in 0..dim { s2[[i,j]] += sx[[i,k]]*sx[[k,j]]; } } }
    for i in 0..dim { for j in 0..dim { for k in 0..dim { s2[[i,j]] -= sy_im[[i,k]]*sy_im[[k,j]]; } } }
    for i in 0..dim { for j in 0..dim { for k in 0..dim { s2[[i,j]] += sz[[i,k]]*sz[[k,j]]; } } }
    
    let sz0_states: Vec<usize> = (0..dim).filter(|&s| s.count_ones() == 2).collect();
    let n_sz0 = sz0_states.len();
    let mut s2_sz0 = Array2::<f64>::zeros((n_sz0, n_sz0));
    for (a, &i) in sz0_states.iter().enumerate() {
        for (b, &j) in sz0_states.iter().enumerate() {
            s2_sz0[[a, b]] = s2[[i, j]];
        }
    }
    
    let mut eigenvectors: Vec<Vec<f64>> = Vec::new();
    let mut eigenvalues: Vec<f64> = Vec::new();
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new(-1.0, 1.0).unwrap();
    
    for _ in 0..6 {
        let mut v: Vec<f64> = (0..n_sz0).map(|_| uniform.sample(&mut rng)).collect();
        for ev in &eigenvectors {
            let overlap: f64 = v.iter().zip(ev.iter()).map(|(a,b)| a*b).sum();
            for i in 0..n_sz0 { v[i] -= overlap * ev[i]; }
        }
        let norm: f64 = v.iter().map(|x| x*x).sum::<f64>().sqrt();
        if norm < 1e-10 { continue; }
        for x in &mut v { *x /= norm; }
        
        for _iter in 0..2000 {
            let mut av = vec![0.0; n_sz0];
            for i in 0..n_sz0 {
                for j in 0..n_sz0 { av[i] += s2_sz0[[i,j]] * v[j]; }
                av[i] += 0.001 * v[i];
            }
            for i in 0..n_sz0 { v[i] -= 0.05 * av[i]; }
            for ev in &eigenvectors {
                let overlap: f64 = v.iter().zip(ev.iter()).map(|(a,b)| a*b).sum();
                for i in 0..n_sz0 { v[i] -= overlap * ev[i]; }
            }
            let norm: f64 = v.iter().map(|x| x*x).sum::<f64>().sqrt();
            if norm > 1e-15 { for x in &mut v { *x /= norm; } }
        }
        
        let mut av = vec![0.0; n_sz0];
        for i in 0..n_sz0 { for j in 0..n_sz0 { av[i] += s2_sz0[[i,j]] * v[j]; } }
        let rayleigh: f64 = v.iter().zip(av.iter()).map(|(a,b)| a*b).sum();
        
        eigenvectors.push(v);
        eigenvalues.push(rayleigh);
    }
    
    let mut indexed_eigs: Vec<(usize, f64)> = eigenvalues.iter().enumerate()
        .map(|(i,&v)| (i, v.abs())).collect();
    indexed_eigs.sort_by(|a,b| a.1.partial_cmp(&b.1).unwrap());
    
    let singlet_indices: Vec<usize> = indexed_eigs.iter().take(2).map(|(i,_)| *i).collect();
    
    println!("  S² eigenvalues: {:?}", 
        eigenvalues.iter().map(|v| format!("{:.4}", v)).collect::<Vec<_>>());
    
    let mut s1_full = vec![0.0; dim];
    let mut s2_full = vec![0.0; dim];
    for (a, &i) in sz0_states.iter().enumerate() {
        s1_full[i] = eigenvectors[singlet_indices[0]][a];
        s2_full[i] = eigenvectors[singlet_indices[1]][a];
    }
    
    let norm1: f64 = s1_full.iter().map(|x| x*x).sum::<f64>().sqrt();
    for x in &mut s1_full { *x /= norm1; }
    let overlap: f64 = s1_full.iter().zip(s2_full.iter()).map(|(a,b)| a*b).sum();
    for i in 0..dim { s2_full[i] -= overlap * s1_full[i]; }
    let norm2: f64 = s2_full.iter().map(|x| x*x).sum::<f64>().sqrt();
    for x in &mut s2_full { *x /= norm2; }
    
    let mut projector = Array2::<f64>::zeros((dim, dim));
    for i in 0..dim {
        for j in 0..dim {
            projector[[i,j]] = s1_full[i]*s1_full[j] + s2_full[i]*s2_full[j];
        }
    }
    projector
}

// ─── 2. UTILITIES ───

fn normalize(v: &mut [f64]) {
    let norm: f64 = v.iter().map(|x| x*x).sum::<f64>().sqrt();
    if norm > 1e-15 { for x in v { *x /= norm; } }
}

fn dot(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b.iter()).map(|(x,y)| x*y).sum()
}

fn build_square_incidence(l: usize) -> Vec<((usize, usize), [usize; 4])> {
    let mut vertices = Vec::new();
    let h = |x: usize, y: usize| -> usize { y * l + x };
    let v = |x: usize, y: usize| -> usize { l * l + y * l + x };
    for y in 0..l {
        for x in 0..l {
            vertices.push(((x,y), [
                h(x,y), v(x,y),
                h((x+l-1)%l, y), v(x, (y+l-1)%l)
            ]));
        }
    }
    vertices
}

// ─── 3. MATRIX-FREE OPERATORS ───

fn apply_ux(state: &mut [f64], n_qubits: usize) {
    let dim = 1usize << n_qubits;
    let mut new_state = vec![0.0; dim];
    let flip_mask = dim - 1;
    for i in 0..dim {
        if state[i].abs() > 1e-15 { new_state[i ^ flip_mask] = state[i]; }
    }
    state.copy_from_slice(&new_state);
}

fn apply_ucz(state: &mut [f64], l: usize, n_qubits: usize) {
    let dim = 1usize << n_qubits;
    let n_h = l * l;
    for py in 0..l {
        for px in 0..l {
            let p_edges = [
                py * l + px,
                n_h + py * l + (px + 1) % l,
                ((py + 1) % l) * l + px,
                n_h + py * l + px,
            ];
            for i in 0..4 {
                for j in (i+1)..4 {
                    for s in 0..dim {
                        if state[s].abs() < 1e-15 { continue; }
                        let b1 = (s >> (n_qubits - 1 - p_edges[i])) & 1;
                        let b2 = (s >> (n_qubits - 1 - p_edges[j])) & 1;
                        if b1 == 1 && b2 == 1 { state[s] *= -1.0; }
                    }
                }
            }
        }
    }
}

// ─── 4. DENSE HAMILTONIAN FOR L=2 ───

fn build_dense_hamiltonian(
    vertices: &[((usize, usize), [usize; 4])],
    n_qubits: usize,
    pv: &Array2<f64>,
) -> Vec<Vec<f64>> {
    let dim = 1usize << n_qubits;
    let mut h = vec![vec![0.0; dim]; dim];
    
    // H = Σ_v (I - P_v) = N_v * I - Σ_v P_v
    for i in 0..dim { h[i][i] = vertices.len() as f64; }
    
    for (_coords, edges) in vertices {
        for state_idx in 0..dim {
            let mut local_idx = 0usize;
            for (k, &e) in edges.iter().enumerate() {
                local_idx |= ((state_idx >> (n_qubits - 1 - e)) & 1) << (3 - k);
            }
            
            for local_j in 0..16 {
                let coeff = pv[[local_j, local_idx]];
                if coeff.abs() < 1e-15 { continue; }
                
                let mut new_idx = state_idx;
                for (k, &e) in edges.iter().enumerate() {
                    let old_bit = (state_idx >> (n_qubits - 1 - e)) & 1;
                    let new_bit = (local_j >> (3 - k)) & 1;
                    if old_bit != new_bit {
                        new_idx ^= 1 << (n_qubits - 1 - e);
                    }
                }
                
                h[new_idx][state_idx] -= coeff;
            }
        }
    }
    
    h
}

fn solve_dense_ground_state(h: &[Vec<f64>]) -> (f64, Vec<f64>) {
    let dim = h.len();
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new(-1.0, 1.0).unwrap();
    
    // Power iteration with shift
    let shift = 10.0;
    let mut v: Vec<f64> = (0..dim).map(|_| uniform.sample(&mut rng)).collect();
    normalize(&mut v);
    
    // Build H + shift*I and LU decompose
    let mut lu = vec![vec![0.0; dim]; dim];
    for i in 0..dim {
        for j in 0..dim { lu[i][j] = h[i][j]; }
        lu[i][i] += shift;
    }
    
    let mut pivots: Vec<usize> = (0..dim).collect();
    
    for k in 0..dim {
        let mut max_val = lu[k][k].abs();
        let mut max_row = k;
        for i in (k+1)..dim {
            if lu[i][k].abs() > max_val {
                max_val = lu[i][k].abs();
                max_row = i;
            }
        }
        
        if max_row != k {
            lu.swap(k, max_row);
            pivots.swap(k, max_row);
        }
        
        if lu[k][k].abs() < 1e-15 { continue; }
        
        for i in (k+1)..dim {
            let factor = lu[i][k] / lu[k][k];
            lu[i][k] = factor;
            for j in (k+1)..dim {
                lu[i][j] -= factor * lu[k][j];
            }
        }
    }
    
    // Solve (H + shift*I) x = b
    let solve = |b: &[f64]| -> Vec<f64> {
        let mut y = vec![0.0; dim];
        for i in 0..dim {
            y[i] = b[pivots[i]];
            for j in 0..i {
                y[i] -= lu[i][j] * y[j];
            }
        }
        
        let mut x = vec![0.0; dim];
        for i in (0..dim).rev() {
            let mut sum = y[i];
            for j in (i+1)..dim {
                sum -= lu[i][j] * x[j];
            }
            x[i] = sum / lu[i][i];
        }
        x
    };
    
    // Inverse power iteration
    for _iter in 0..100 {
        v = solve(&v);
        normalize(&mut v);
    }
    
    // Compute Rayleigh quotient
    let mut hv = vec![0.0; dim];
    for i in 0..dim {
        for j in 0..dim { hv[i] += h[i][j] * v[j]; }
    }
    let e0 = v.iter().zip(hv.iter()).map(|(a,b)| a*b).sum();
    
    (e0, v)
}

// ─── 5. LANCZOS FOR L=3 ───

fn apply_vertex_projector(state: &mut [f64], edges: &[usize; 4], n_qubits: usize, pv: &Array2<f64>) {
    let dim = 1usize << n_qubits;
    let mut new_state = vec![0.0; dim];
    let other_edges: Vec<usize> = (0..n_qubits).filter(|e| !edges.contains(e)).collect();
    
    for state_idx in 0..dim {
        if state[state_idx].abs() < 1e-15 { continue; }
        let mut local_idx = 0usize;
        for (k, &e) in edges.iter().enumerate() {
            local_idx |= ((state_idx >> (n_qubits - 1 - e)) & 1) << (3 - k);
        }
        let mut frozen = 0usize;
        for (k, &e) in other_edges.iter().enumerate() {
            frozen |= ((state_idx >> (n_qubits - 1 - e)) & 1) << k;
        }
        for local_j in 0..16 {
            let coeff = pv[[local_j, local_idx]] * state[state_idx];
            if coeff.abs() < 1e-15 { continue; }
            let mut new_idx = 0usize;
            for (k, &e) in edges.iter().enumerate() {
                new_idx |= ((local_j >> (3 - k)) & 1) << (n_qubits - 1 - e);
            }
            for (k, &e) in other_edges.iter().enumerate() {
                new_idx |= ((frozen >> k) & 1) << (n_qubits - 1 - e);
            }
            new_state[new_idx] += coeff;
        }
    }
    state.copy_from_slice(&new_state);
}

fn lanczos_ground_state(
    vertices: &[((usize, usize), [usize; 4])],
    n_qubits: usize,
    pv: &Array2<f64>,
    max_iter: usize,
) -> (f64, Vec<f64>) {
    let dim = 1usize << n_qubits;
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new(-1.0, 1.0).unwrap();
    
    let mut v0: Vec<f64> = (0..dim).map(|_| uniform.sample(&mut rng)).collect();
    normalize(&mut v0);
    
    let mut alphas = Vec::new();
    let mut betas = Vec::new();
    let mut vs: Vec<Vec<f64>> = Vec::new();
    vs.push(v0.clone());
    
    let mut w = vec![0.0; dim];
    
    for iter in 0..max_iter {
        // w = H * v where H = Σ_v (I - P_v)
        let nv = vertices.len() as f64;
        for i in 0..dim { w[i] = nv * vs[iter][i]; }
        for (_coords, edges) in vertices {
            let mut pv_v = vs[iter].clone();
            apply_vertex_projector(&mut pv_v, edges, n_qubits, pv);
            for i in 0..dim { w[i] -= pv_v[i]; }
        }
        
        let alpha = dot(&w, &vs[iter]);
        alphas.push(alpha);
        for i in 0..dim { w[i] -= alpha * vs[iter][i]; }
        
        if iter > 0 {
            let beta = betas[betas.len() - 1];
            for i in 0..dim { w[i] -= beta * vs[iter - 1][i]; }
        }
        
        // FULL REORTHOGONALIZATION
        for prev in vs.iter() {
            let overlap = dot(&w, prev);
            for i in 0..dim { w[i] -= overlap * prev[i]; }
        }
        
        let beta_new: f64 = w.iter().map(|x| x*x).sum::<f64>().sqrt();
        
        if beta_new < 1e-10 {
            println!("  Lanczos converged at iter {}", iter);
            break;
        }
        
        betas.push(beta_new);
        
        let mut v_next = vec![0.0; dim];
        for i in 0..dim { v_next[i] = w[i] / beta_new; }
        
        // Reorthogonalize new vector too
        for prev in vs.iter() {
            let overlap = dot(&v_next, prev);
            for i in 0..dim { v_next[i] -= overlap * prev[i]; }
        }
        normalize(&mut v_next);
        
        vs.push(v_next);
        
        // Check convergence every 10 iterations
        if iter > 0 && iter % 10 == 0 {
            let eigs = solve_tridiagonal_eigenvalues(&alphas, &betas);
            
            // Check orthonormality
            let mut max_overlap = 0.0;
            for i in 0..vs.len() {
                for j in (i+1)..vs.len() {
                    let o = dot(&vs[i], &vs[j]).abs();
                    if o > max_overlap { max_overlap = o; }
                }
            }
            
            println!("  Iter {}: E_0 = {:.8e}, E_1 = {:.8e}, gap = {:.8e}, max_orth_err = {:.2e}", 
                iter, eigs[0], if eigs.len() > 1 { eigs[1] } else { 0.0 }, 
                if eigs.len() > 1 { eigs[1] - eigs[0] } else { 0.0 },
                max_overlap);
        }
    }
    
    // Solve tridiagonal eigenproblem
    let eigs = solve_tridiagonal_eigenvalues(&alphas, &betas);
    let e0 = eigs[0];
    
    // Ground state vector of tridiagonal
    let v = solve_tridiagonal_ground_state(&alphas, &betas, e0);
    
    // Reconstruct ground state
    let mut ground_state = vec![0.0; dim];
    for (i, coeff) in v.iter().enumerate().take(vs.len()) {
        for j in 0..dim { ground_state[j] += coeff * vs[i][j]; }
    }
    normalize(&mut ground_state);
    
    (e0, ground_state)
}

fn solve_tridiagonal_eigenvalues(alphas: &[f64], betas: &[f64]) -> Vec<f64> {
    let n = alphas.len();
    if n == 0 { return vec![]; }
    
    // Use dense QR on small tridiagonal matrix
    let mut t = vec![vec![0.0; n]; n];
    for i in 0..n {
        t[i][i] = alphas[i];
        if i < n - 1 { t[i][i+1] = betas[i]; t[i+1][i] = betas[i]; }
    }
    
    for _iter in 0..1000 {
        let mut q = vec![vec![0.0; n]; n];
        for i in 0..n { q[i][i] = 1.0; }
        
        for i in 0..n-1 {
            let r = (t[i][i]*t[i][i] + t[i+1][i]*t[i+1][i]).sqrt();
            if r < 1e-15 { continue; }
            let c = t[i][i] / r;
            let s = t[i+1][i] / r;
            
            for j in i..n {
                let aij = t[i][j];
                let ai1j = t[i+1][j];
                t[i][j] = c * aij + s * ai1j;
                t[i+1][j] = -s * aij + c * ai1j;
            }
            
            for j in 0..n {
                let qji = q[j][i];
                let qji1 = q[j][i+1];
                q[j][i] = c * qji + s * qji1;
                q[j][i+1] = -s * qji + c * qji1;
            }
        }
        
        let mut new_t = vec![vec![0.0; n]; n];
        for i in 0..n {
            for j in 0..n {
                for k in 0..n { new_t[i][j] += t[i][k] * q[j][k]; }
            }
        }
        t = new_t;
        
        let mut converged = true;
        for i in 0..n-1 {
            if t[i+1][i].abs() > 1e-12 { converged = false; break; }
        }
        if converged { break; }
    }
    
    let mut eigs: Vec<f64> = (0..n).map(|i| t[i][i]).collect();
    eigs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    eigs
}

fn solve_tridiagonal_ground_state(alphas: &[f64], betas: &[f64], e0: f64) -> Vec<f64> {
    let n = alphas.len();
    if n == 0 { return vec![]; }
    
    let mut v = vec![1.0; n];
    normalize(&mut v);
    
    for _ in 0..200 {
        let mut c_prime = vec![0.0; n];
        let mut d_prime = vec![0.0; n];
        
        let denom0 = alphas[0] - e0;
        c_prime[0] = if n > 1 { betas[0] / denom0 } else { 0.0 };
        d_prime[0] = v[0] / denom0;
        
        for i in 1..n {
            let denom = (alphas[i] - e0) - betas[i-1] * c_prime[i-1];
            if i < n - 1 { c_prime[i] = betas[i] / denom; }
            d_prime[i] = (v[i] - betas[i-1] * d_prime[i-1]) / denom;
        }
        
        let mut v_new = vec![0.0; n];
        v_new[n-1] = d_prime[n-1];
        for i in (0..n-1).rev() {
            v_new[i] = d_prime[i] - c_prime[i] * v_new[i+1];
        }
        
        normalize(&mut v_new);
        v = v_new;
    }
    
    v
}

// ─── 6. MAIN ───

fn main() {
    println!("═══════════════════════════════════════════════════════════════");
    println!("T35b Gate 1: Four-Valent Square-Lattice Intertwiner Test");
    println!("═══════════════════════════════════════════════════════════════\n");
    
    println!("Building singlet projector P_v...");
    let pv = build_singlet_projector();
    println!("  P_v trace = {:.1}\n", (0..16).map(|i| pv[[i,i]]).sum::<f64>());
    
    // Test L = 2 (dense)
    {
        let l = 2usize;
        println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("L = {} Periodic Square Lattice (Dense)", l);
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        
        let n_qubits = 2 * l * l;
        let dim = 1usize << n_qubits;
        println!("Qubits: {}, Hilbert space dim: {}", n_qubits, dim);
        
        let vertices = build_square_incidence(l);
        println!("Vertices: {}", vertices.len());
        
        println!("\nBuilding dense Hamiltonian...");
        let h = build_dense_hamiltonian(&vertices, n_qubits, &pv);
        
        println!("Finding ground state...");
        let (e0, ground_state) = solve_dense_ground_state(&h);
        
        println!("\nGround state energy: {:.8e}", e0);
        
        if e0 < 1e-6 {
            println!("PASS: Ground state is in intertwiner subspace");
            
            let mut ux_gs = ground_state.clone();
            apply_ux(&mut ux_gs, n_qubits);
            println!("<psi|U_X|psi> = {:.6}", dot(&ground_state, &ux_gs));
            
            let mut ucz_gs = ground_state.clone();
            apply_ucz(&mut ucz_gs, l, n_qubits);
            println!("<psi|U_CZ|psi> = {:.6}", dot(&ground_state, &ucz_gs));
        }
    }
    
    // Test L = 3 (Lanczos)
    {
        let l = 3usize;
        println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("L = {} Periodic Square Lattice (Lanczos)", l);
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        
        let n_qubits = 2 * l * l;
        let dim = 1usize << n_qubits;
        println!("Qubits: {}, Hilbert space dim: {}", n_qubits, dim);
        
        let vertices = build_square_incidence(l);
        println!("Vertices: {}", vertices.len());
        
        println!("\nFinding ground state (Lanczos)...");
        let (e0, ground_state) = lanczos_ground_state(&vertices, n_qubits, &pv, 200);
        
        println!("\nGround state energy: {:.8e}", e0);
        
        if e0 < 1e-6 {
            println!("PASS: Ground state is in intertwiner subspace");
            
            let mut ux_gs = ground_state.clone();
            apply_ux(&mut ux_gs, n_qubits);
            println!("<psi|U_X|psi> = {:.6}", dot(&ground_state, &ux_gs));
            
            let mut ucz_gs = ground_state.clone();
            apply_ucz(&mut ucz_gs, l, n_qubits);
            println!("<psi|U_CZ|psi> = {:.6}", dot(&ground_state, &ucz_gs));
        } else {
            println!("No intertwiner ground state (E_0 = {})", e0);
        }
    }
    
    println!("\n═══════════════════════════════════════════════════════════════");
    println!("Done!");
    println!("═══════════════════════════════════════════════════════════════");
}
