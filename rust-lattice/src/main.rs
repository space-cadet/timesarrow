use z2_lattice_gauge::*;
use std::env;
use rayon::prelude::*;

#[derive(Debug)]
struct BetaResult {
    beta: f64,
    mean_plaquette: f64,
    error_plaquette: f64,
    susceptibility: f64,
    specific_heat: f64,
    binder_cumulant: f64,
    num_measurements: usize,
    wall_time_ms: u64,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 6 {
        eprintln!("Usage: {} <L> <measure_sweeps> <thermal_sweeps> <workers> <beta_values...>", args[0]);
        eprintln!("  L: lattice size (e.g., 16)");
        eprintln!("  measure_sweeps: number of measurement sweeps (e.g., 100000)");
        eprintln!("  thermal_sweeps: number of thermalization sweeps (e.g., 10000)");
        eprintln!("  workers: number of parallel workers (e.g., 3)");
        eprintln!("  beta_values: space-separated list of beta values");
        std::process::exit(1);
    }
    
    let l: usize = args[1].parse().expect("L must be a positive integer");
    let measure_sweeps: usize = args[2].parse().expect("measure_sweeps must be a positive integer");
    let thermal_sweeps: usize = args[3].parse().expect("thermal_sweeps must be a positive integer");
    let workers: usize = args[4].parse().expect("workers must be a positive integer");
    
    let beta_values: Vec<f64> = args[5..]
        .iter()
        .map(|s| s.parse().expect("beta values must be floats"))
        .collect();
    
    println!("{{");
    println!("  \"parameters\": {{");
    println!("    \"L\": {},", l);
    println!("    \"thermalSweeps\": {},", thermal_sweeps);
    println!("    \"measureSweeps\": {},", measure_sweeps);
    println!("    \"measureEvery\": 10,");
    println!("    \"binSize\": 10,");
    println!("    \"workers\": {}", workers);
    println!("  }},");
    println!("  \"results\": [");
    
    let total_start = std::time::Instant::now();
    
    // Run each beta value in parallel using rayon
    let results: Vec<BetaResult> = beta_values
        .par_iter()
        .enumerate()
        .map(|(i, beta)| {
            let seed = 42 + i as u64;
            let (mean_p, error, chi, cv, binder, wall_time) = simulate_beta(
                l, *beta, thermal_sweeps, measure_sweeps, 10, seed
            );
            BetaResult {
                beta: *beta,
                mean_plaquette: mean_p,
                error_plaquette: error,
                susceptibility: chi,
                specific_heat: cv,
                binder_cumulant: binder,
                num_measurements: measure_sweeps / 10,
                wall_time_ms: wall_time,
            }
        })
        .collect();
    
    let total_time = total_start.elapsed().as_millis() as u64;
    
    // Print results in deterministic order (beta values are already sorted)
    for (i, res) in results.iter().enumerate() {
        let comma = if i < results.len() - 1 { "," } else { "" };
        println!("    {{");
        println!("      \"beta\": {},", res.beta);
        println!("      \"meanPlaquette\": {},", res.mean_plaquette);
        println!("      \"errorPlaquette\": {},", res.error_plaquette);
        println!("      \"susceptibility\": {},", res.susceptibility);
        println!("      \"specificHeat\": {},", res.specific_heat);
        println!("      \"binderCumulant\": {},", res.binder_cumulant);
        println!("      \"numMeasurements\": {},", res.num_measurements);
        println!("      \"wallTimeMs\": {}", res.wall_time_ms);
        println!("    }}{}", comma);
    }
    
    println!("  ],");
    println!("  \"totalWallTimeMs\": {}", total_time);
    println!("}}");
}
