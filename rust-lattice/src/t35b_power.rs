/// T35b Gate 1: Power iteration for L=3 (avoids Lanczos instability)

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

fn apply_hamiltonian(state: &[f64], vertices: &[((usize, usize), [usize; 4])], n_qubits: usize, pv: &Array2<f64>) -> Vec<f64> {
    let dim = 1usize << n_qubits;
    let mut result = vec![0.0; dim];
    let nv = vertices.len() as f64;
    for i in 0..dim { result[i] = nv * state[i]; }
    for (_coords, edges) in vertices {
        let mut pv_v = state.to_vec();
        apply_vertex_projector(&mut pv_v, edges, n_qubits, pv);
        for i in 0..dim { result[i] -= pv_v[i]; }
    }
    result
}

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

fn power_iteration_ground_state(
    vertices: &[((usize, usize), [usize; 4])],
    n_qubits: usize,
    pv: &Array2<f64>,
    max_iter: usize,
) -> (f64, Vec<f64>) {
    let dim = 1usize << n_qubits;
    let mut rng = StdRng::seed_from_u64(42);
    let uniform = Uniform::new(-1.0, 1.0).unwrap();
    
    let mut v: Vec<f64> = (0..dim).map(|_| uniform.sample(&mut rng)).collect();
    normalize(&mut v);
    
    // Use power method on (I - εH)
    let epsilon = 0.1;
    
    for iter in 0..max_iter {
        let hv = apply_hamiltonian(&v, vertices, n_qubits, pv);
        let rayleigh = dot(&v, &hv);
        
        for i in 0..dim {
            v[i] = v[i] - epsilon * (hv[i] - rayleigh * v[i]);
        }
        normalize(&mut v);
        
        if iter % 100 == 0 {
            let hv = apply_hamiltonian(&v, vertices, n_qubits, pv);
            let e = dot(&v, &hv);
            println!("  Iter {}: E = {:.8e}", iter, e);
        }
    }
    
    let hv = apply_hamiltonian(&v, vertices, n_qubits, pv);
    let e0 = dot(&v, &hv);
    
    (e0, v)
}

fn main() {
    println!("═══════════════════════════════════════════════════════════════");
    println!("T35b Gate 1: L=3 Power Iteration Test");
    println!("═══════════════════════════════════════════════════════════════\n");
    
    println!("Building singlet projector P_v...");
    let pv = build_singlet_projector();
    println!("  P_v trace = {:.1}\n", (0..16).map(|i| pv[[i,i]]).sum::<f64>());
    
    let l = 3usize;
    println!("L = {} Periodic Square Lattice (Power Iteration)", l);
    
    let n_qubits = 2 * l * l;
    let dim = 1usize << n_qubits;
    println!("Qubits: {}, Hilbert space dim: {}", n_qubits, dim);
    
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
    println!("Vertices: {}", vertices.len());
    
    println!("\nFinding ground state (power iteration)...");
    let (e0, ground_state) = power_iteration_ground_state(&vertices, n_qubits, &pv, 2000);
    
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
        println!("No exact intertwiner ground state (E_0 = {})", e0);
    }
    
    println!("\n═══════════════════════════════════════════════════════════════");
    println!("Done!");
    println!("═══════════════════════════════════════════════════════════════");
}
