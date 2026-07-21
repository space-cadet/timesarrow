/// Quick L=3 test with simple Lanczos (no reorthogonalization)

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

fn normalize(v: &mut [f64]) {
    let norm: f64 = v.iter().map(|x| x*x).sum::<f64>().sqrt();
    if norm > 1e-15 { for x in v { *x /= norm; } }
}

fn dot(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b.iter()).map(|(x,y)| x*y).sum()
}

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

fn main() {
    println!("L=3 Simple Lanczos Test (no reorthog, fixed Hamiltonian)");
    
    let pv = build_singlet_projector();
    let l = 3usize;
    let n_qubits = 2 * l * l;
    let dim = 1usize << n_qubits;
    println!("Qubits: {}, dim: {}", n_qubits, dim);
    
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
    
    let nv = vertices.len() as f64;
    
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new(-1.0, 1.0).unwrap();
    let mut v0: Vec<f64> = (0..dim).map(|_| uniform.sample(&mut rng)).collect();
    normalize(&mut v0);
    
    let mut alphas = Vec::new();
    let mut betas = Vec::new();
    let mut vs: Vec<Vec<f64>> = Vec::new();
    vs.push(v0.clone());
    
    let mut w = vec![0.0; dim];
    
    for iter in 0..100 {
        // w = H * v where H = Σ_v (I - P_v) = nv*I - Σ_v P_v
        for i in 0..dim { w[i] = nv * vs[iter][i]; }
        for (_coords, edges) in &vertices {
            let mut pv_v = vs[iter].clone();
            apply_vertex_projector(&mut pv_v, edges, n_qubits, &pv);
            for i in 0..dim { w[i] -= pv_v[i]; }
        }
        
        let alpha = dot(&w, &vs[iter]);
        alphas.push(alpha);
        for i in 0..dim { w[i] -= alpha * vs[iter][i]; }
        
        if iter > 0 {
            let beta = betas[betas.len() - 1];
            for i in 0..dim { w[i] -= beta * vs[iter - 1][i]; }
        }
        
        let beta_new: f64 = w.iter().map(|x| x*x).sum::<f64>().sqrt();
        
        if beta_new < 1e-10 {
            println!("  Lanczos converged at iter {}", iter);
            break;
        }
        
        betas.push(beta_new);
        
        let mut v_next = vec![0.0; dim];
        for i in 0..dim { v_next[i] = w[i] / beta_new; }
        vs.push(v_next);
        
        // Print energy estimate every 10 iters
        if iter % 10 == 0 {
            let n = alphas.len();
            let mut t = vec![vec![0.0; n]; n];
            for i in 0..n {
                t[i][i] = alphas[i];
                if i < n - 1 { t[i][i+1] = betas[i]; t[i+1][i] = betas[i]; }
            }
            
            // Quick QR
            for _ in 0..100 {
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
            }
            
            let mut eigs: Vec<f64> = (0..n).map(|i| t[i][i]).collect();
            eigs.sort_by(|a, b| a.partial_cmp(b).unwrap());
            
            println!("  Iter {}: E_0 = {:.8e}", iter, eigs[0]);
        }
    }
    
    println!("\nDone!");
}
