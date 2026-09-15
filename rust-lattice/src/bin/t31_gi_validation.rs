// T31 Production-Scale Gauge-Invariance Validation
//
// Tests gauge_invariant_signed_volume_3d() at production lattice sizes
// with thermalized configurations and multiple gauge transformations.
//
// Run: cargo run --release --bin t31_gi_validation

use z2_lattice_gauge::Z2GaugeField;
use std::time::Instant;

fn main() {
    println!("=== T31: Gauge-Invariant Signed-Volume Validation ===\n");
    
    let l_sizes = vec![8, 10, 12, 16];
    let beta = 0.440686; // Near critical point for 3D Z₂
    let n_thermal = 1000;
    let n_measure = 100;
    
    for &l in &l_sizes {
        println!("--- L={} ---", l);
        let start = Instant::now();
        
        // Thermalize
        let mut field = Z2GaugeField::new_dim(l, 3, 42);
        for _ in 0..n_thermal {
            field.sweep(beta);
        }
        
        let q_thermal = field.gauge_invariant_signed_volume_3d();
        println!("  Thermalized Q_GI = {:.6}", q_thermal);
        
        // Test 1: Single-site gauge transform
        let q_before = field.gauge_invariant_signed_volume_3d();
        field.local_gauge_transform_3d(l/2, l/2, l/2);
        let q_after = field.gauge_invariant_signed_volume_3d();
        let diff1 = (q_before - q_after).abs();
        println!("  Single-site transform: |ΔQ| = {:.2e} {}", 
            diff1, if diff1 < 1e-10 { "✅" } else { "❌" });
        
        // Test 2: Multiple random gauge transforms
        let mut field2 = Z2GaugeField::new_dim(l, 3, 42);
        for _ in 0..n_thermal {
            field2.sweep(beta);
        }
        let q_before2 = field2.gauge_invariant_signed_volume_3d();
        for _ in 0..10 {
            let x = (rand::random::<u64>() as usize) % l;
            let y = (rand::random::<u64>() as usize) % l;
            let z = (rand::random::<u64>() as usize) % l;
            field2.local_gauge_transform_3d(x, y, z);
        }
        let q_after2 = field2.gauge_invariant_signed_volume_3d();
        let diff2 = (q_before2 - q_after2).abs();
        println!("  10 random transforms:  |ΔQ| = {:.2e} {}",
            diff2, if diff2 < 1e-10 { "✅" } else { "❌" });
        
        // Test 3: Statistical properties
        let mut q_values = Vec::new();
        let mut field3 = Z2GaugeField::new_dim(l, 3, 42);
        for _ in 0..n_thermal {
            field3.sweep(beta);
        }
        for _ in 0..n_measure {
            field3.sweep(beta);
            q_values.push(field3.gauge_invariant_signed_volume_3d());
        }
        let mean_q: f64 = q_values.iter().sum::<f64>() / q_values.len() as f64;
        let var_q: f64 = q_values.iter()
            .map(|x| (x - mean_q).powi(2))
            .sum::<f64>() / q_values.len() as f64;
        println!("  Statistics: ⟨Q⟩ = {:.4} ± {:.4}, σ² = {:.6}",
            mean_q, (var_q / n_measure as f64).sqrt(), var_q);
        println!("  Range check: [{:.4}, {:.4}] ⊆ [-1,1] {}",
            q_values.iter().cloned().fold(f64::INFINITY, f64::min),
            q_values.iter().cloned().fold(f64::NEG_INFINITY, f64::max),
            if q_values.iter().all(|&q| (-1.0..=1.0).contains(&q)) { "✅" } else { "❌" });
        
        let elapsed = start.elapsed();
        println!("  Time: {:?}\n", elapsed);
    }
    
    println!("=== Validation Complete ===");
}
