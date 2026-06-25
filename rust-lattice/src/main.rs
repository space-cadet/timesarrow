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
    wilson_loops: Vec<(usize, usize, f64, f64)>, // (r, c, mean_W, var_W)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 8 {
        eprintln!("Usage: {} <L> <dimension> <measure_sweeps> <thermal_sweeps> <workers> <loop_sizes> <beta_values...>", args[0]);
        eprintln!("  L: lattice size (e.g., 16)");
        eprintln!("  dimension: lattice dimension 2 or 3 (e.g., 3)");
        eprintln!("  measure_sweeps: number of measurement sweeps (e.g., 100000)");
        eprintln!("  thermal_sweeps: number of thermalization sweeps (e.g., 10000)");
        eprintln!("  workers: number of parallel workers (e.g., 4)");
        eprintln!("  loop_sizes: comma-separated list of rxc loop sizes (e.g., '1x1,2x2,4x4')");
        eprintln!("  beta_values: space-separated list of beta values");
        std::process::exit(1);
    }
    
    let l: usize = args[1].parse().expect("L must be a positive integer");
    let dimension: usize = args[2].parse().expect("dimension must be 2 or 3");
    let measure_sweeps: usize = args[3].parse().expect("measure_sweeps must be a positive integer");
    let thermal_sweeps: usize = args[4].parse().expect("thermal_sweeps must be a positive integer");
    let workers: usize = args[5].parse().expect("workers must be a positive integer");
    
    // Parse loop sizes: "1x1,2x2,4x4" -> vec![(1,1), (2,2), (4,4)]
    let loop_sizes: Vec<(usize, usize)> = args[6]
        .split(',')
        .map(|s| {
            let parts: Vec<&str> = s.split('x').collect();
            if parts.len() != 2 {
                panic!("Loop size must be in format 'rxr' (e.g., '1x1')");
            }
            let r = parts[0].parse::<usize>().expect("Loop size r must be integer");
            let c = parts[1].parse::<usize>().expect("Loop size c must be integer");
            (r, c)
        })
        .collect();
    
    let beta_values: Vec<f64> = args[7..]
        .iter()
        .map(|s| s.parse().expect("beta values must be floats"))
        .collect();
    
    println!("{{");
    println!("  \"parameters\": {{");
    println!("    \"L\": {},", l);
    println!("    \"dimension\": {},", dimension);
    println!("    \"thermalSweeps\": {},", thermal_sweeps);
    println!("    \"measureSweeps\": {},", measure_sweeps);
    println!("    \"measureEvery\": 10,");
    println!("    \"binSize\": 10,");
    println!("    \"workers\": {},", workers);
    println!("    \"loopSizes\": [",);
    for (i, (r, c)) in loop_sizes.iter().enumerate() {
        let comma = if i < loop_sizes.len() - 1 { "," } else { "" };
        println!("      {{\"r\": {}, \"c\": {}}}{}", r, c, comma);
    }
    println!("    ]");
    println!("  }},");
    println!("  \"results\": [");
    
    let total_start = std::time::Instant::now();
    
    // Run each beta value in parallel using rayon
    let results: Vec<BetaResult> = beta_values
        .par_iter()
        .enumerate()
        .map(|(i, beta)| {
            let seed = 42 + i as u64;
            let (mean_p, error, chi, cv, binder, wall_time, wilson_data) = simulate_beta_with_wilson_loops(
                l, dimension, *beta, thermal_sweeps, measure_sweeps, 10, seed, &loop_sizes
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
                wilson_loops: wilson_data,
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
        println!("      \"wallTimeMs\": {},", res.wall_time_ms);
        println!("      \"wilsonLoops\": [");
        for (j, (r, c, mean_w, var_w)) in res.wilson_loops.iter().enumerate() {
            let w_comma = if j < res.wilson_loops.len() - 1 { "," } else { "" };
            println!("        {{\"r\": {}, \"c\": {}, \"meanW\": {}, \"varW\": {}}}{}", r, c, mean_w, var_w, w_comma);
        }
        println!("      ]");
        println!("    }}{}", comma);
    }
    
    println!("  ],");
    println!("  \"totalWallTimeMs\": {}", total_time);
    println!("}}");
}
