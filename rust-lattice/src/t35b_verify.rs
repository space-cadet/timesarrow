/// Quick verification: compute L=2 Hamiltonian explicitly and check eigenvalues

use ndarray::Array2;
use rand::SeedableRng;
use rand::rngs::StdRng;
use rand::distr::{Distribution, Uniform};

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

fn main() {
    println!("L=2 Dense Hamiltonian Verification");
    
    let pv = build_singlet_projector();
    let l = 2usize;
    let n_qubits = 2 * l * l;
    let dim = 1usize << n_qubits;
    
    println!("Hilbert space dim: {}", dim);
    
    // Build vertex-edge incidence
    let mut vertices = Vec::new();
    let h = |x: usize, y: usize| -> usize { y * l + x };
    let v = |x: usize, y: usize| -> usize { l * l + y * l + x };
    for y in 0..l {
        for x in 0..l {
            vertices.push([
                h(x,y), v(x,y),
                h((x+l-1)%l, y), v(x, (y+l-1)%l)
            ]);
        }
    }
    
    // Build full Hamiltonian H = Σ_v (I - P_v)
    println!("Building dense Hamiltonian...");
    let mut h_matrix = vec![vec![0.0; dim]; dim];
    
    // Start with identity
    for i in 0..dim { h_matrix[i][i] = 4.0; } // 4 vertices, each contributes I
    
    // Subtract P_v for each vertex
    for edges in &vertices {
        // P_v acting on 4 qubits
        for state_idx in 0..dim {
            let mut local_idx = 0usize;
            for (k, &e) in edges.iter().enumerate() {
                local_idx |= ((state_idx >> (n_qubits - 1 - e)) & 1) << (3 - k);
            }
            
            for local_j in 0..16 {
                let coeff = pv[[local_j, local_idx]];
                if coeff.abs() < 1e-15 { continue; }
                
                // Find the state index corresponding to local_j on these edges
                let mut new_idx = state_idx;
                for (k, &e) in edges.iter().enumerate() {
                    let old_bit = (state_idx >> (n_qubits - 1 - e)) & 1;
                    let new_bit = (local_j >> (3 - k)) & 1;
                    if old_bit != new_bit {
                        new_idx ^= 1 << (n_qubits - 1 - e);
                    }
                }
                
                h_matrix[new_idx][state_idx] -= coeff;
            }
        }
    }
    
    println!("Finding smallest eigenvalues using inverse iteration...");
    
    // Build (H + shift*I) explicitly
    let shift = 5.0;
    let mut h_shifted = h_matrix.clone();
    for i in 0..dim { h_shifted[i][i] += shift; }
    
    // LU decomposition for solving linear systems
    println!("Computing LU decomposition...");
    let mut lu = h_shifted.clone();
    let mut pivots: Vec<usize> = (0..dim).collect();
    
    for k in 0..dim {
        // Find pivot
        let mut max_val = lu[k][k].abs();
        let mut max_row = k;
        for i in (k+1)..dim {
            if lu[i][k].abs() > max_val {
                max_val = lu[i][k].abs();
                max_row = i;
            }
        }
        
        // Swap rows
        if max_row != k {
            lu.swap(k, max_row);
            pivots.swap(k, max_row);
        }
        
        if lu[k][k].abs() < 1e-15 {
            println!("Warning: matrix is nearly singular at row {}", k);
            continue;
        }
        
        for i in (k+1)..dim {
            let factor = lu[i][k] / lu[k][k];
            lu[i][k] = factor;
            for j in (k+1)..dim {
                lu[i][j] -= factor * lu[k][j];
            }
        }
    }
    
    // Function to solve (H + shift*I) x = b using LU
    let solve = |b: &[f64]| -> Vec<f64> {
        let mut y = vec![0.0; dim];
        
        // Forward substitution (with pivoting)
        for i in 0..dim {
            y[i] = b[pivots[i]];
            for j in 0..i {
                y[i] -= lu[i][j] * y[j];
            }
        }
        
        // Back substitution
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
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new(-1.0, 1.0).unwrap();
    let mut v: Vec<f64> = (0..dim).map(|_| uniform.sample(&mut rng)).collect();
    let norm: f64 = v.iter().map(|x| x*x).sum::<f64>().sqrt();
    for x in &mut v { *x /= norm; }
    
    for iter in 0..100 {
        v = solve(&v);
        let norm: f64 = v.iter().map(|x| x*x).sum::<f64>().sqrt();
        for x in &mut v { *x /= norm; }
        
        // Compute Rayleigh quotient
        let mut hv = vec![0.0; dim];
        for i in 0..dim {
            for j in 0..dim {
                hv[i] += h_matrix[i][j] * v[j];
            }
        }
        let rayleigh: f64 = v.iter().zip(hv.iter()).map(|(a,b)| a*b).sum();
        
        if iter % 10 == 0 {
            println!("  Iter {}: E = {:.8e}", iter, rayleigh);
        }
    }
    
    // Final Rayleigh quotient
    let mut hv = vec![0.0; dim];
    for i in 0..dim {
        for j in 0..dim {
            hv[i] += h_matrix[i][j] * v[j];
        }
    }
    let e0: f64 = v.iter().zip(hv.iter()).map(|(a,b)| a*b).sum();
    
    println!("\nGround state energy (dense): {:.8e}", e0);
    
    // Find second eigenvalue by orthogonalizing against ground state
    let mut v2: Vec<f64> = (0..dim).map(|_| uniform.sample(&mut rng)).collect();
    let overlap: f64 = v2.iter().zip(v.iter()).map(|(a,b)| a*b).sum();
    for i in 0..dim { v2[i] -= overlap * v[i]; }
    let norm: f64 = v2.iter().map(|x| x*x).sum::<f64>().sqrt();
    for x in &mut v2 { *x /= norm; }
    
    for iter in 0..1000 {
        let mut hv = vec![0.0; dim];
        for i in 0..dim {
            for j in 0..dim {
                hv[i] += h_matrix[i][j] * v2[j];
            }
        }
        let rayleigh: f64 = v2.iter().zip(hv.iter()).map(|(a,b)| a*b).sum();
        
        if iter % 100 == 0 {
            println!("  Iter {}: E_1 = {:.8e}", iter, rayleigh);
        }
        
        for i in 0..dim {
            v2[i] = v2[i] - 0.01 * (hv[i] - rayleigh * v2[i]) / (rayleigh + shift + 1.0);
        }
        
        // Orthogonalize against ground state
        let overlap: f64 = v2.iter().zip(v.iter()).map(|(a,b)| a*b).sum();
        for i in 0..dim { v2[i] -= overlap * v[i]; }
        
        let norm: f64 = v2.iter().map(|x| x*x).sum::<f64>().sqrt();
        for x in &mut v2 { *x /= norm; }
    }
    
    let mut hv = vec![0.0; dim];
    for i in 0..dim {
        for j in 0..dim {
            hv[i] += h_matrix[i][j] * v2[j];
        }
    }
    let e1: f64 = v2.iter().zip(hv.iter()).map(|(a,b)| a*b).sum();
    
    println!("\nFirst excited state energy (dense): {:.8e}", e1);
    println!("Energy gap: {:.8e}", e1 - e0);
    
    if e0 < 1e-6 {
        println!("\nPASS: Ground state is in intertwiner subspace");
        
        // Test U_X
        let mut ux_v = vec![0.0; dim];
        let flip_mask = dim - 1;
        for i in 0..dim { ux_v[i ^ flip_mask] = v[i]; }
        let ux_overlap: f64 = v.iter().zip(ux_v.iter()).map(|(a,b)| a*b).sum();
        println!("<psi|U_X|psi> = {:.6}", ux_overlap);
        
        // Test U_CZ
        let mut ucz_v = v.clone();
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
                            if ucz_v[s].abs() < 1e-15 { continue; }
                            let b1 = (s >> (n_qubits - 1 - p_edges[i])) & 1;
                            let b2 = (s >> (n_qubits - 1 - p_edges[j])) & 1;
                            if b1 == 1 && b2 == 1 { ucz_v[s] *= -1.0; }
                        }
                    }
                }
            }
        }
        let ucz_overlap: f64 = v.iter().zip(ucz_v.iter()).map(|(a,b)| a*b).sum();
        println!("<psi|U_CZ|psi> = {:.6}", ucz_overlap);
    }
}
