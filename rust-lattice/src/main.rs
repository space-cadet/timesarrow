use z2_lattice_gauge::*;
use std::env;
use std::fs;
use std::sync::mpsc;
use rayon::prelude::*;
use serde_json::{json, Value};

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
    // Polyakov loop fields (optional, only for 3D with --polyakov)
    mean_polyakov: Option<f64>,
    error_polyakov: Option<f64>,
    polyakov_susceptibility: Option<f64>,
    polyakov_binder: Option<f64>,
}

/// Read existing checkpoint and return completed beta values + saved results.
fn load_checkpoint(path: &str) -> Option<(Vec<f64>, Vec<Value>)> {
    if !std::path::Path::new(path).exists() {
        return None;
    }
    let content = fs::read_to_string(path).ok()?;
    let data: Value = serde_json::from_str(&content).ok()?;
    let completed: Vec<f64> = data.get("completed")?
        .as_array()?
        .iter()
        .filter_map(|v| v.as_f64())
        .collect();
    let results: Vec<Value> = data.get("results")?.as_array()?.clone();
    Some((completed, results))
}

/// Atomically write checkpoint: write to .tmp then rename.
fn save_checkpoint(path: &str, params: &Value, results: &[Value], completed: &[f64]) {
    let checkpoint = json!({
        "parameters": params,
        "results": results,
        "completed": completed,
        "metadata": {
            "timestamp": chrono::Utc::now().to_rfc3339(),
            "completed": completed.len(),
        }
    });
    let tmp_path = format!("{}.tmp", path);
    if let Ok(json_str) = serde_json::to_string_pretty(&checkpoint) {
        let _ = fs::write(&tmp_path, json_str);
        let _ = fs::rename(&tmp_path, path);
    }
}

/// Convert BetaResult to serde_json::Value for checkpointing.
fn result_to_json(res: &BetaResult) -> Value {
    let mut obj = json!({
        "beta": res.beta,
        "meanPlaquette": res.mean_plaquette,
        "errorPlaquette": res.error_plaquette,
        "susceptibility": res.susceptibility,
        "specificHeat": res.specific_heat,
        "binderCumulant": res.binder_cumulant,
        "numMeasurements": res.num_measurements,
        "wallTimeMs": res.wall_time_ms,
        "wilsonLoops": []
    });

    if let Some(mp) = res.mean_polyakov {
        obj["meanPolyakov"] = json!(mp);
        obj["errorPolyakov"] = json!(res.error_polyakov.unwrap());
        obj["polyakovSusceptibility"] = json!(res.polyakov_susceptibility.unwrap());
        obj["polyakovBinder"] = json!(res.polyakov_binder.unwrap());
    }

    let wilson_json: Vec<Value> = res.wilson_loops.iter().map(|(r, c, mean_w, var_w)| {
        json!({"r": r, "c": c, "meanW": mean_w, "varW": var_w})
    }).collect();
    obj["wilsonLoops"] = json!(wilson_json);

    obj
}

fn main() {
    let mut args: Vec<String> = env::args().collect();

    // Parse flags
    let mut base_seed: u64 = 42;
    let mut use_polyakov = false;
    let mut raw_output = false;
    let mut checkpoint_path: Option<String> = None;
    let mut i = 1;
    while i < args.len() {
        if args[i] == "--seed" && i + 1 < args.len() {
            base_seed = args[i + 1].parse().expect("seed must be a positive integer");
            args.remove(i);     // remove --seed
            args.remove(i);     // remove value
        } else if args[i] == "--polyakov" {
            use_polyakov = true;
            args.remove(i);
        } else if args[i] == "--raw-output" {
            raw_output = true;
            args.remove(i);
        } else if args[i] == "--checkpoint" && i + 1 < args.len() {
            checkpoint_path = Some(args[i + 1].clone());
            args.remove(i);     // remove --checkpoint
            args.remove(i);     // remove value
        } else {
            i += 1;
        }
    }

    if args.len() < 8 {
        eprintln!("Usage: {} [--polyakov] [--raw-output] [--checkpoint <path>] <L> <dimension> <measure_sweeps> <thermal_sweeps> <workers> <loop_sizes> <beta_values...> [--seed <value>]", args[0]);
        eprintln!("  --polyakov: measure Polyakov loop (3D only)");
        eprintln!("  --raw-output: output raw time series (plaquette values) for autocorrelation analysis");
        eprintln!("  --checkpoint <path>: write incremental checkpoint after each beta completes");
        eprintln!("  L: lattice size (e.g., 16)");
        eprintln!("  dimension: lattice dimension 2 or 3 (e.g., 3)");
        eprintln!("  measure_sweeps: number of measurement sweeps (e.g., 100000)");
        eprintln!("  thermal_sweeps: number of thermalization sweeps (e.g., 10000)");
        eprintln!("  workers: number of parallel workers (e.g., 4)");
        eprintln!("  loop_sizes: comma-separated list of rxc loop sizes (e.g., '1x1,2x2,4x4')");
        eprintln!("  beta_values: space-separated list of beta values");
        eprintln!("  --seed <value>: base random seed (default: 42)");
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

    // Validate --polyakov flag
    if use_polyakov && dimension != 3 {
        eprintln!("Warning: --polyakov is only supported for 3D lattices. Ignoring flag.");
        use_polyakov = false;
    }

    // Build parameters JSON for checkpoint
    let params_json = json!({
        "L": l,
        "dimension": dimension,
        "thermalSweeps": thermal_sweeps,
        "measureSweeps": measure_sweeps,
        "measureEvery": 10,
        "binSize": 10,
        "workers": workers,
        "polyakov": use_polyakov,
        "loopSizes": loop_sizes.iter().map(|(r, c)| json!({"r": r, "c": c})).collect::<Vec<_>>(),
    });

    // Load checkpoint if specified
    let mut completed_betas: Vec<f64> = Vec::new();
    let mut checkpoint_results: Vec<Value> = Vec::new();
    if let Some(ref cp_path) = checkpoint_path {
        if let Some((completed, results)) = load_checkpoint(cp_path) {
            eprintln!("[checkpoint] Resuming from {} — {} of {} betas already completed",
                cp_path, completed.len(), beta_values.len());
            completed_betas = completed;
            checkpoint_results = results;
        }
    }

    // Filter out already-completed betas
    let remaining_betas: Vec<f64> = beta_values.iter()
        .filter(|b| !completed_betas.iter().any(|c| (c - *b).abs() < 1e-9))
        .copied()
        .collect();

    if remaining_betas.is_empty() {
        eprintln!("[checkpoint] All betas already complete!");
        // Still print full JSON output for compatibility
    } else {
        eprintln!("[checkpoint] Running {} remaining betas...", remaining_betas.len());
    }

    println!("{{");
    println!("  \"parameters\": {{");
    println!("    \"L\": {},", l);
    println!("    \"dimension\": {},", dimension);
    println!("    \"thermalSweeps\": {},", thermal_sweeps);
    println!("    \"measureSweeps\": {},", measure_sweeps);
    println!("    \"measureEvery\": 10,");
    println!("    \"binSize\": 10,");
    println!("    \"workers\": {},", workers);
    println!("    \"polyakov\": {},", use_polyakov);
    println!("    \"loopSizes\": [",);
    for (i, (r, c)) in loop_sizes.iter().enumerate() {
        let comma = if i < loop_sizes.len() - 1 { "," } else { "" };
        println!("      {{\"r\": {}, \"c\": {}}}{}", r, c, comma);
    }
    println!("    ]");
    println!("  }},");
    println!("  \"results\": [");

    let total_start = std::time::Instant::now();

    // Raw output mode: output raw measurements for autocorrelation analysis
    if raw_output {
        let raw_results: Vec<(f64, Vec<f64>, u64)> = remaining_betas
            .par_iter()
            .enumerate()
            .map(|(i, beta)| {
                let seed = base_seed + i as u64;
                let (measurements, wall_time) = simulate_beta_raw(
                    l, dimension, *beta, thermal_sweeps, measure_sweeps, 10, seed
                );
                (*beta, measurements, wall_time)
            })
            .collect();

        let total_time = total_start.elapsed().as_millis() as u64;

        // Print checkpointed results first
        for res in &checkpoint_results {
            println!("    {},", serde_json::to_string(res).unwrap());
        }

        for (i, (beta, measurements, wall_time)) in raw_results.iter().enumerate() {
            let comma = if i < raw_results.len() - 1 { "," } else { "" };
            println!("    {{");
            println!("      \"beta\": {},", beta);
            println!("      \"numMeasurements\": {},", measurements.len());
            println!("      \"wallTimeMs\": {},", wall_time);
            println!("      \"rawPlaquettes\": [");
            for (j, val) in measurements.iter().enumerate() {
                let v_comma = if j < measurements.len() - 1 { "," } else { "" };
                println!("        {}{}", val, v_comma);
            }
            println!("      ]");
            println!("    }}{}", comma);
        }

        println!("  ],");
        println!("  \"totalWallTimeMs\": {}", total_time);
        println!("}}");
        return;
    }

    // Normal mode: binned statistics with streaming checkpointing
    let mut all_results: Vec<Value> = checkpoint_results.clone();

    if !remaining_betas.is_empty() {
        let (tx, rx) = mpsc::channel::<BetaResult>();
        let n_remaining = remaining_betas.len();

        // Spawn worker threads via rayon
        remaining_betas.par_iter().enumerate().for_each_with(tx, |tx, (i, beta)| {
            let seed = base_seed + i as u64;
            let res = if use_polyakov {
                let (mean_p, error, chi, cv, binder_p, mean_poly, error_poly, chi_poly, binder_poly, wall_time) =
                    simulate_beta_with_polyakov_3d(l, *beta, thermal_sweeps, measure_sweeps, 10, seed);
                BetaResult {
                    beta: *beta,
                    mean_plaquette: mean_p,
                    error_plaquette: error,
                    susceptibility: chi,
                    specific_heat: cv,
                    binder_cumulant: binder_p,
                    num_measurements: measure_sweeps / 10,
                    wall_time_ms: wall_time,
                    wilson_loops: Vec::new(),
                    mean_polyakov: Some(mean_poly),
                    error_polyakov: Some(error_poly),
                    polyakov_susceptibility: Some(chi_poly),
                    polyakov_binder: Some(binder_poly),
                }
            } else {
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
                    mean_polyakov: None,
                    error_polyakov: None,
                    polyakov_susceptibility: None,
                    polyakov_binder: None,
                }
            };
            tx.send(res).unwrap();
        });

        // Main thread: receive results as they complete and write checkpoint
        for _ in 0..n_remaining {
            let res = rx.recv().expect("Worker thread panicked");
            let beta = res.beta;
            let json_val = result_to_json(&res);
            all_results.push(json_val);
            completed_betas.push(beta);

            // Write checkpoint
            if let Some(ref cp_path) = checkpoint_path {
                save_checkpoint(cp_path, &params_json, &all_results, &completed_betas);
                eprintln!("[checkpoint] β={:.4} done — {}/{} complete", beta, completed_betas.len(), beta_values.len());
            }
        }
    }

    let total_time = total_start.elapsed().as_millis() as u64;

    // Print results in deterministic order (beta values are already sorted)
    for (i, res_val) in all_results.iter().enumerate() {
        let comma = if i < all_results.len() - 1 { "," } else { "" };
        println!("    {}{}", serde_json::to_string(res_val).unwrap(), comma);
    }

    println!("  ],");
    println!("  \"totalWallTimeMs\": {}", total_time);
    println!("}}");

    // Final checkpoint write (in case we want to keep it)
    if let Some(ref cp_path) = checkpoint_path {
        save_checkpoint(cp_path, &params_json, &all_results, &completed_betas);
        eprintln!("[checkpoint] Final checkpoint saved to {}", cp_path);
    }
}
