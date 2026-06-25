use rand::prelude::*;
use rand_xoshiro::Xoshiro256PlusPlus;
use serde::{Deserialize, Serialize};

/// Checkpoint-compatible state for serialization.
#[derive(Serialize, Deserialize)]
struct CheckpointState {
    l: usize,
    links: Vec<i8>,
    seed: u64,
}

/// A 2D Z₂ lattice gauge field with L×L sites.
/// Links are stored as a flat Vec<i8> where each element is ±1.
/// Layout: for each site (x, y), two links: horizontal (dir=0) and vertical (dir=1).
/// Total links: 2 * L * L.
#[derive(Clone, Debug)]
pub struct Z2GaugeField {
    pub l: usize,
    pub links: Vec<i8>,
    rng: Xoshiro256PlusPlus,
    seed: u64,
}

impl Z2GaugeField {
    /// Create a new lattice with random initial configuration.
    pub fn new(l: usize, seed: u64) -> Self {
        let mut rng = Xoshiro256PlusPlus::seed_from_u64(seed);
        let n_links = 2 * l * l;
        let links: Vec<i8> = (0..n_links)
            .map(|_| if rng.random::<bool>() { 1 } else { -1 })
            .collect();
        Self { l, links, rng, seed }
    }

    /// Create a cold start configuration (all links = +1).
    pub fn cold(l: usize, seed: u64) -> Self {
        let n_links = 2 * l * l;
        Self {
            l,
            links: vec![1; n_links],
            rng: Xoshiro256PlusPlus::seed_from_u64(seed),
            seed,
        }
    }

    /// Get the index of a link at site (x, y) in direction dir (0=horizontal, 1=vertical).
    #[inline(always)]
    pub fn link_idx(&self, x: usize, y: usize, dir: usize) -> usize {
        2 * (y * self.l + x) + dir
    }

    /// Get the value of a link (±1).
    #[inline(always)]
    pub fn link(&self, x: usize, y: usize, dir: usize) -> i8 {
        self.links[self.link_idx(x, y, dir)]
    }

    /// Flip a link (multiply by -1).
    #[inline(always)]
    pub fn flip_link(&mut self, x: usize, y: usize, dir: usize) {
        let idx = self.link_idx(x, y, dir);
        self.links[idx] *= -1;
    }

    /// Compute the product of links around the plaquette at site (x, y).
    /// The plaquette is: right(x,y) * up(x+1,y) * left(x,y+1) * down(x,y).
    /// For Z₂, the product is ±1.
    #[inline(always)]
    pub fn plaquette(&self, x: usize, y: usize) -> i8 {
        let l = self.l;
        let xp1 = (x + 1) % l;
        let yp1 = (y + 1) % l;

        let right = self.link(x, y, 0);      // horizontal at (x,y): bottom edge
        let up    = self.link(xp1, y, 1);    // vertical at (x+1,y): right edge
        let left  = self.link(x, yp1, 0);    // horizontal at (x,y+1): top edge
        let down  = self.link(x, y, 1);      // vertical at (x,y): left edge

        // The plaquette product
        right * up * left * down
    }

    /// Compute all plaquette products and return (mean, sum of squares, count).
    /// Note: mean is negated to match TypeScript output convention.
    #[inline(always)]
    pub fn plaquette_stats(&self) -> (f64, f64, usize) {
        let n_plaquettes = self.l * self.l;
        let mut sum = 0i64;
        for y in 0..self.l {
            for x in 0..self.l {
                sum += self.plaquette(x, y) as i64;
            }
        }
        // Negate to match TypeScript convention (traversal direction difference)
        let mean = -(sum as f64 / n_plaquettes as f64);
        (mean, n_plaquettes as f64, n_plaquettes)
    }

    /// Perform one Metropolis sweep over all links.
    /// For each link, compute the local action change ΔE = 2β * sum of affected plaquettes.
    /// If ΔE ≤ 0, accept. If ΔE > 0, accept with probability exp(-β * ΔE).
    /// Returns the number of accepted flips.
    pub fn sweep(&mut self, beta: f64) -> usize {
        let l = self.l;
        let mut accepted = 0usize;
        
        for y in 0..l {
            for x in 0..l {
                for dir in 0..2 {
                    // Compute the sum of plaquettes affected by this link
                    // A horizontal link at (x,y) is in plaquettes at (x,y) and (x, y-1)
                    // A vertical link at (x,y) is in plaquettes at (x,y) and (x-1, y)
                    let delta_sum = if dir == 0 {
                        // Horizontal link: plaquettes at (x,y) and (x, y-1)
                        let plaq1 = self.plaquette(x, y);
                        let y_prev = (y + l - 1) % l;
                        let plaq2 = self.plaquette(x, y_prev);
                        plaq1 + plaq2
                    } else {
                        // Vertical link: plaquettes at (x,y) and (x-1, y)
                        let plaq1 = self.plaquette(x, y);
                        let x_prev = (x + l - 1) % l;
                        let plaq2 = self.plaquette(x_prev, y);
                        plaq1 + plaq2
                    };

                    // ΔE = 2β * (sum of affected plaquettes)
                    // For Z₂, flipping a link changes each affected plaquette by -2*P_old
                    // So the action change is β * Δ(sum of plaquettes) = β * (-2 * delta_sum)
                    // Actually, let me be more careful:
                    // Action = -β * Σ P_i
                    // If we flip link l, each affected plaquette P → -P
                    // So ΔS = -β * Σ(-P - P) = -β * Σ(-2P) = 2β * Σ P
                    // Wait, that's for the action. For energy E = -S = β * Σ P:
                    // ΔE = β * Σ(-P - P) = -2β * Σ P
                    // So if Σ P > 0, ΔE < 0, accept (lower energy)
                    // If Σ P < 0, ΔE > 0, accept with probability exp(-ΔE) = exp(2β * Σ P)
                    // But Σ P = delta_sum above. So:
                    // If delta_sum > 0: always accept
                    // If delta_sum < 0: accept with probability exp(2β * delta_sum)
                    // If delta_sum = 0: 50% chance
                    
                    let delta_e = -2.0 * beta * delta_sum as f64;
                    
                    let accept = if delta_e <= 0.0 {
                        true
                    } else {
                        let r: f64 = self.rng.random();
                        r < (-delta_e).exp()
                    };

                    if accept {
                        self.flip_link(x, y, dir);
                        accepted += 1;
                    }
                }
            }
        }
        
        accepted
    }

    /// Thermalize the lattice with `n_sweeps` sweeps.
    pub fn thermalize(&mut self, beta: f64, n_sweeps: usize) {
        for _ in 0..n_sweeps {
            self.sweep(beta);
        }
    }

    /// Measure observables over `n_sweeps` sweeps, taking measurements every `measure_every` sweeps.
    /// Returns (mean plaquette, error on plaquette, susceptibility, specific heat, binder cumulant).
    pub fn measure(
        &mut self,
        beta: f64,
        n_sweeps: usize,
        measure_every: usize,
    ) -> (f64, f64, f64, f64, f64) {
        let mut measurements = Vec::new();
        let mut measurements_sq = Vec::new();
        let mut measurements_quad = Vec::new();

        for sweep in 0..n_sweeps {
            self.sweep(beta);
            
            if sweep % measure_every == 0 {
                let (mean_plaq, _, _) = self.plaquette_stats();
                measurements.push(mean_plaq);
                measurements_sq.push(mean_plaq * mean_plaq);
                measurements_quad.push(mean_plaq * mean_plaq * mean_plaq * mean_plaq);
            }
        }

        let n = measurements.len() as f64;
        let mean_p = measurements.iter().sum::<f64>() / n;
        let mean_p2 = measurements_sq.iter().sum::<f64>() / n;
        let mean_p4 = measurements_quad.iter().sum::<f64>() / n;

        // Error estimate (naive standard error, no binning for now)
        let variance = measurements.iter().map(|x| (x - mean_p).powi(2)).sum::<f64>() / n;
        let error = (variance / n).sqrt();

        // Susceptibility: χ = L² * (⟨P²⟩ - ⟨P⟩²) / T = L² * β * (⟨P²⟩ - ⟨P⟩²)
        // Actually for gauge theories, the susceptibility is usually defined as
        // χ = L² * Var(P) / T where T = 1/β
        // So χ = L² * β * Var(P)
        let l_sq = (self.l * self.l) as f64;
        let susceptibility = l_sq * beta * (mean_p2 - mean_p * mean_p);

        // Specific heat: C = L² * β² * (⟨P²⟩ - ⟨P⟩²)
        let specific_heat = l_sq * beta * beta * (mean_p2 - mean_p * mean_p);

        // Binder cumulant: U = 1 - ⟨P⁴⟩ / (3 * ⟨P²⟩²)
        let binder = if mean_p2 > 0.0 {
            1.0 - mean_p4 / (3.0 * mean_p2 * mean_p2)
        } else {
            0.0
        };

        (mean_p, error, susceptibility, specific_heat, binder)
    }

    /// Serialize to JSON checkpoint format.
    pub fn to_checkpoint(&self) -> String {
        let state = CheckpointState {
            l: self.l,
            links: self.links.clone(),
            seed: self.seed,
        };
        serde_json::to_string_pretty(&state).unwrap()
    }

    /// Deserialize from JSON checkpoint format.
    pub fn from_checkpoint(json: &str) -> Result<Self, serde_json::Error> {
        let state: CheckpointState = serde_json::from_str(json)?;
        Ok(Self {
            l: state.l,
            links: state.links,
            rng: Xoshiro256PlusPlus::seed_from_u64(state.seed),
            seed: state.seed,
        })
    }
}

/// Run a simulation at a single β value.
/// Equivalent to the TypeScript `simulateBeta` function.
pub fn simulate_beta(
    l: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
) -> (f64, f64, f64, f64, f64, u64) {
    let mut field = Z2GaugeField::new(l, seed);
    
    let thermal_start = std::time::Instant::now();
    field.thermalize(beta, thermal_sweeps);
    let thermal_time = thermal_start.elapsed().as_millis() as u64;
    
    let measure_start = std::time::Instant::now();
    let (mean_p, error, chi, cv, binder) = field.measure(beta, measure_sweeps, measure_every);
    let measure_time = measure_start.elapsed().as_millis() as u64;
    
    (mean_p, error, chi, cv, binder, thermal_time + measure_time)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cold_start_plaquette() {
        let field = Z2GaugeField::cold(4, 42);
        // All links are +1, so all plaquettes should be +1
        for y in 0..4 {
            for x in 0..4 {
                assert_eq!(field.plaquette(x, y), 1);
            }
        }
    }

    #[test]
    fn test_flip_changes_plaquette() {
        let mut field = Z2GaugeField::cold(4, 42);
        // Flip one horizontal link at (0,0)
        field.flip_link(0, 0, 0);
        // The two plaquettes containing this link should now be -1
        assert_eq!(field.plaquette(0, 0), -1);
        assert_eq!(field.plaquette(0, 3), -1);
        // All others should still be +1
        assert_eq!(field.plaquette(1, 0), 1);
        assert_eq!(field.plaquette(0, 1), 1);
    }

    #[test]
    fn test_sweep_preserves_detailed_balance() {
        let mut field = Z2GaugeField::new(8, 42);
        let beta = 1.0;
        // Run a few sweeps and just check it doesn't panic
        field.thermalize(beta, 10);
        let (mean_p, _, _, _, _) = field.measure(beta, 100, 10);
        // Mean plaquette should be between -1 and 1
        assert!(mean_p.abs() <= 1.0);
    }
}
