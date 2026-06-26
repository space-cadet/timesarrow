# T20: Rust-Level Checkpointing for Monte Carlo Simulations

*Date: 2026-06-26*
*Applies to: rust-lattice/src/main.rs, numerics/src/scripts/t20-sim-3d-fss-v2.py*

## Problem

The original `main.rs` collected all results in a `Vec` via `rayon::par_iter().collect()` and only printed JSON at the very end. If the process was killed (subagent timeout, system restart, context compaction), all intermediate results were lost.

## Solution: Streaming Checkpointing

### Architecture

```
main.rs (single thread)          worker threads (rayon)
       |                               |
       |  mpsc channel (sender)        |
       |<------------------------------|
       |  (beta, result)               |
       |                               |
       |  Append to checkpoint file    |
       |  (atomic: .tmp → rename)      |
```

### Key Changes

1. **Added `--checkpoint <path>` flag**
2. **Replaced `.collect()` with `mpsc` channel** — workers send results as they finish
3. **Main thread receives and appends** to checkpoint file immediately
4. **Atomic writes**: Write to `path.tmp`, then `fs::rename` to `path`
5. **Resume on startup**: Read existing checkpoint, skip completed betas
6. **Final output**: Merges checkpoint + new results into clean JSON

### Rust Implementation

```rust
// Argument parsing
let checkpoint_path: Option<String> = /* ... */;

// Resume: read existing results
let mut completed_betas: HashSet<f64> = HashSet::new();
let mut existing_results: Vec<SimulationResult> = Vec::new();

if let Some(ref path) = checkpoint_path {
    if let Ok(contents) = fs::read_to_string(path) {
        if let Ok(data) = serde_json::from_str::<serde_json::Value>(&contents) {
            if let Some(results) = data.get("results").and_then(|r| r.as_array()) {
                for r in results {
                    if let Some(beta) = r.get("beta").and_then(|b| b.as_f64()) {
                        completed_betas.insert(beta);
                        existing_results.push(
                            serde_json::from_value(r.clone()).unwrap()
                        );
                    }
                }
            }
        }
    }
}

// Filter remaining betas
let remaining_betas: Vec<f64> = all_betas.into_iter()
    .filter(|b| !completed_betas.contains(b))
    .collect();

// Run with mpsc channel
let (tx, rx) = mpsc::channel::<SimulationResult>();

// Spawn writer thread
let checkpoint = checkpoint_path.clone();
let writer = thread::spawn(move || {
    let mut results: Vec<SimulationResult> = existing_results;
    while let Ok(result) = rx.recv() {
        results.push(result);
        // Atomic write
        if let Some(ref path) = checkpoint {
            let tmp = format!("{}.tmp", path);
            if let Ok(json) = serde_json::to_string_pretty(&json!({"results": &results})) {
                let _ = fs::write(&tmp, json);
                let _ = fs::rename(&tmp, path);
            }
        }
    }
    results
});

// Parallel workers
remaining_betas.into_par_iter().for_each(|beta| {
    let result = run_simulation(beta, sweeps);
    let _ = tx.send(result);
});

drop(tx); // Signal completion
let all_results = writer.join().unwrap();
```

### Python Integration

The Python script passes the checkpoint path to Rust:

```python
outfile = f"output/t20-p3b-L{L}-3D-fine-{date_suffix}.json"
checkpoint = f"output/t20-p3b-L{L}-3D-fine-{date_suffix}.checkpoint.json"

cmd = [
    "cargo", "run", "--release", "--",
    "--lattice-size", str(L),
    "--dimension", "3",
    "--beta", ",".join(map(str, betas)),
    "--sweeps", str(sweeps),
    "--checkpoint", checkpoint
]
```

### Benefits

- **No data loss**: Every completed β is saved immediately
- **Resumable**: Kill and restart without losing progress
- **Atomic**: Never have partially-written corrupt files
- **Transparent**: Python script doesn't need checkpoint logic

### Dependencies

- `chrono` (added to `Cargo.toml`) for timestamps in output
- `serde_json` (already present) for JSON serialization
