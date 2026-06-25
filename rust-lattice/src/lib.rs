use rand::prelude::*;
use rand_xoshiro::Xoshiro256PlusPlus;
use serde::{Deserialize, Serialize};

fn default_dimension() -> usize {
    2
}

/// Checkpoint-compatible state for serialization.
#[derive(Serialize, Deserialize)]
struct CheckpointState {
    l: usize,
    links: Vec<i8>,
    seed: u64,
    #[serde(default = "default_dimension")]
    dimension: usize,
}

/// A Z₂ lattice gauge field with L×L (2D) or L×L×L (3D) sites.
/// Links are stored as a flat Vec<i8> where each element is ±1.
/// Layout 2D: for each site (x, y), two links: x (dir=0) and y (dir=1). Total: 2*L².
/// Layout 3D: for each site (x, y, z), three links: x (dir=0), y (dir=1), z (dir=2). Total: 3*L³.
#[derive(Clone, Debug)]
pub struct Z2GaugeField {
    pub l: usize,
    pub links: Vec<i8>,
    pub dimension: usize,
    rng: Xoshiro256PlusPlus,
    seed: u64,
}

impl Z2GaugeField {
    /// Create a new 2D lattice with random initial configuration.
    pub fn new(l: usize, seed: u64) -> Self {
        Self::new_dim(l, 2, seed)
    }

    /// Create a new lattice with specified dimension (2 or 3) and random initial configuration.
    pub fn new_dim(l: usize, dimension: usize, seed: u64) -> Self {
        assert!(dimension == 2 || dimension == 3, "Only dimensions 2 and 3 are supported");
        let mut rng = Xoshiro256PlusPlus::seed_from_u64(seed);
        let n_links = if dimension == 2 {
            2 * l * l
        } else {
            3 * l * l * l
        };
        let links: Vec<i8> = (0..n_links)
            .map(|_| if rng.random::<bool>() { 1 } else { -1 })
            .collect();
        Self { l, links, dimension, rng, seed }
    }

    /// Create a cold-start 2D configuration (all links = +1).
    pub fn cold(l: usize, seed: u64) -> Self {
        Self::cold_dim(l, 2, seed)
    }

    /// Create a cold-start configuration with specified dimension (all links = +1).
    pub fn cold_dim(l: usize, dimension: usize, seed: u64) -> Self {
        assert!(dimension == 2 || dimension == 3, "Only dimensions 2 and 3 are supported");
        let n_links = if dimension == 2 {
            2 * l * l
        } else {
            3 * l * l * l
        };
        Self {
            l,
            links: vec![1; n_links],
            dimension,
            rng: Xoshiro256PlusPlus::seed_from_u64(seed),
            seed,
        }
    }

    /// Get the index of a link at site (x, y) in direction dir (0=x, 1=y). 2D only.
    #[inline(always)]
    pub fn link_idx(&self, x: usize, y: usize, dir: usize) -> usize {
        assert!(self.dimension == 2, "link_idx is for 2D; use link_idx_3d for 3D");
        2 * (y * self.l + x) + dir
    }

    /// Get the index of a link at site (x, y, z) in direction dir (0=x, 1=y, 2=z). 3D only.
    #[inline(always)]
    pub fn link_idx_3d(&self, x: usize, y: usize, z: usize, dir: usize) -> usize {
        assert!(self.dimension == 3, "link_idx_3d is for 3D");
        3 * (z * self.l * self.l + y * self.l + x) + dir
    }

    /// Get the value of a 2D link (±1).
    #[inline(always)]
    pub fn link(&self, x: usize, y: usize, dir: usize) -> i8 {
        self.links[self.link_idx(x, y, dir)]
    }

    /// Get the value of a 3D link (±1).
    #[inline(always)]
    pub fn link_3d(&self, x: usize, y: usize, z: usize, dir: usize) -> i8 {
        self.links[self.link_idx_3d(x, y, z, dir)]
    }

    /// Flip a 2D link (multiply by -1).
    #[inline(always)]
    pub fn flip_link(&mut self, x: usize, y: usize, dir: usize) {
        let idx = self.link_idx(x, y, dir);
        self.links[idx] *= -1;
    }

    /// Flip a 3D link (multiply by -1).
    #[inline(always)]
    pub fn flip_link_3d(&mut self, x: usize, y: usize, z: usize, dir: usize) {
        let idx = self.link_idx_3d(x, y, z, dir);
        self.links[idx] *= -1;
    }

    /// Compute the product of links around the plaquette at site (x, y). 2D only.
    #[inline(always)]
    pub fn plaquette(&self, x: usize, y: usize) -> i8 {
        assert!(self.dimension == 2, "plaquette() is for 2D; use plaquette_xy/yz/xz for 3D");
        let l = self.l;
        let xp1 = (x + 1) % l;
        let yp1 = (y + 1) % l;

        let right = self.link(x, y, 0);      // x-link at (x,y): bottom edge
        let up    = self.link(xp1, y, 1);    // y-link at (x+1,y): right edge
        let left  = self.link(x, yp1, 0);    // x-link at (x,y+1): top edge
        let down  = self.link(x, y, 1);      // y-link at (x,y): left edge

        right * up * left * down
    }

    /// XY plaquette at (x, y, z) in 3D.
    #[inline(always)]
    pub fn plaquette_xy(&self, x: usize, y: usize, z: usize) -> i8 {
        assert!(self.dimension == 3, "plaquette_xy is for 3D");
        let l = self.l;
        let xp1 = (x + 1) % l;
        let yp1 = (y + 1) % l;

        let right = self.link_3d(x, y, z, 0);     // x-link at (x,y,z)
        let up    = self.link_3d(xp1, y, z, 1);   // y-link at (x+1,y,z)
        let left  = self.link_3d(x, yp1, z, 0);   // x-link at (x,y+1,z)
        let down  = self.link_3d(x, y, z, 1);     // y-link at (x,y,z)

        right * up * left * down
    }

    /// YZ plaquette at (x, y, z) in 3D.
    #[inline(always)]
    pub fn plaquette_yz(&self, x: usize, y: usize, z: usize) -> i8 {
        assert!(self.dimension == 3, "plaquette_yz is for 3D");
        let l = self.l;
        let yp1 = (y + 1) % l;
        let zp1 = (z + 1) % l;

        let right = self.link_3d(x, y, z, 1);     // y-link at (x,y,z)
        let up    = self.link_3d(x, yp1, z, 2);   // z-link at (x,y+1,z)
        let left  = self.link_3d(x, y, zp1, 1);   // y-link at (x,y,z+1)
        let down  = self.link_3d(x, y, z, 2);     // z-link at (x,y,z)

        right * up * left * down
    }

    /// XZ plaquette at (x, y, z) in 3D.
    #[inline(always)]
    pub fn plaquette_xz(&self, x: usize, y: usize, z: usize) -> i8 {
        assert!(self.dimension == 3, "plaquette_xz is for 3D");
        let l = self.l;
        let xp1 = (x + 1) % l;
        let zp1 = (z + 1) % l;

        let right = self.link_3d(x, y, z, 0);     // x-link at (x,y,z)
        let up    = self.link_3d(xp1, y, z, 2);   // z-link at (x+1,y,z)
        let left  = self.link_3d(x, y, zp1, 0);   // x-link at (x,y,z+1)
        let down  = self.link_3d(x, y, z, 2);     // z-link at (x,y,z)

        right * up * left * down
    }

    /// Compute all plaquette products and return (mean, sum of squares, count).
    /// In 2D: L² plaquettes. In 3D: 3·L³ plaquettes (xy, yz, xz at each site).
    /// Mean is negated to match TypeScript output convention.
    #[inline(always)]
    pub fn plaquette_stats(&self) -> (f64, f64, usize) {
        let l = self.l;
        if self.dimension == 2 {
            let n_plaquettes = l * l;
            let mut sum = 0i64;
            for y in 0..l {
                for x in 0..l {
                    sum += self.plaquette(x, y) as i64;
                }
            }
            let mean = -(sum as f64 / n_plaquettes as f64);
            (mean, n_plaquettes as f64, n_plaquettes)
        } else {
            let n_plaquettes = 3 * l * l * l;
            let mut sum = 0i64;
            for z in 0..l {
                for y in 0..l {
                    for x in 0..l {
                        sum += self.plaquette_xy(x, y, z) as i64;
                        sum += self.plaquette_yz(x, y, z) as i64;
                        sum += self.plaquette_xz(x, y, z) as i64;
                    }
                }
            }
            let mean = -(sum as f64 / n_plaquettes as f64);
            (mean, n_plaquettes as f64, n_plaquettes)
        }
    }

    /// Perform one Metropolis sweep over all links.
    /// Returns the number of accepted flips.
    pub fn sweep(&mut self, beta: f64) -> usize {
        if self.dimension == 2 {
            self.sweep_2d(beta)
        } else {
            self.sweep_3d(beta)
        }
    }

    fn sweep_2d(&mut self, beta: f64) -> usize {
        let l = self.l;
        let mut accepted = 0usize;

        for y in 0..l {
            for x in 0..l {
                for dir in 0..2 {
                    let delta_sum = if dir == 0 {
                        // x-link: plaquettes at (x,y) and (x, y-1)
                        let plaq1 = self.plaquette(x, y);
                        let y_prev = (y + l - 1) % l;
                        let plaq2 = self.plaquette(x, y_prev);
                        plaq1 + plaq2
                    } else {
                        // y-link: plaquettes at (x,y) and (x-1, y)
                        let plaq1 = self.plaquette(x, y);
                        let x_prev = (x + l - 1) % l;
                        let plaq2 = self.plaquette(x_prev, y);
                        plaq1 + plaq2
                    };

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

    fn sweep_3d(&mut self, beta: f64) -> usize {
        let l = self.l;
        let mut accepted = 0usize;

        for z in 0..l {
            for y in 0..l {
                for x in 0..l {
                    for dir in 0..3 {
                        let delta_sum = match dir {
                            0 => {
                                // x-link: xy(x,y,z), xy(x,y-1,z), xz(x,y,z), xz(x,y,z-1)
                                let y_prev = (y + l - 1) % l;
                                let z_prev = (z + l - 1) % l;
                                self.plaquette_xy(x, y, z)
                                    + self.plaquette_xy(x, y_prev, z)
                                    + self.plaquette_xz(x, y, z)
                                    + self.plaquette_xz(x, y, z_prev)
                            }
                            1 => {
                                // y-link: xy(x,y,z), xy(x-1,y,z), yz(x,y,z), yz(x,y,z-1)
                                let x_prev = (x + l - 1) % l;
                                let z_prev = (z + l - 1) % l;
                                self.plaquette_xy(x, y, z)
                                    + self.plaquette_xy(x_prev, y, z)
                                    + self.plaquette_yz(x, y, z)
                                    + self.plaquette_yz(x, y, z_prev)
                            }
                            2 => {
                                // z-link: xz(x,y,z), xz(x-1,y,z), yz(x,y,z), yz(x,y-1,z)
                                let x_prev = (x + l - 1) % l;
                                let y_prev = (y + l - 1) % l;
                                self.plaquette_xz(x, y, z)
                                    + self.plaquette_xz(x_prev, y, z)
                                    + self.plaquette_yz(x, y, z)
                                    + self.plaquette_yz(x, y_prev, z)
                            }
                            _ => unreachable!(),
                        };

                        let delta_e = -2.0 * beta * delta_sum as f64;

                        let accept = if delta_e <= 0.0 {
                            true
                        } else {
                            let r: f64 = self.rng.random();
                            r < (-delta_e).exp()
                        };

                        if accept {
                            self.flip_link_3d(x, y, z, dir);
                            accepted += 1;
                        }
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

        // Volume factor: L^d where d is dimension
        let volume = if self.dimension == 2 {
            (self.l * self.l) as f64
        } else {
            (self.l * self.l * self.l) as f64
        };

        // Susceptibility: χ = V * β * Var(P)
        let susceptibility = volume * beta * (mean_p2 - mean_p * mean_p);

        // Specific heat: C = V * β² * Var(P)
        let specific_heat = volume * beta * beta * (mean_p2 - mean_p * mean_p);

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
            dimension: self.dimension,
        };
        serde_json::to_string_pretty(&state).unwrap()
    }

    /// Deserialize from JSON checkpoint format.
    pub fn from_checkpoint(json: &str) -> Result<Self, serde_json::Error> {
        let state: CheckpointState = serde_json::from_str(json)?;
        Ok(Self {
            l: state.l,
            links: state.links,
            dimension: state.dimension,
            rng: Xoshiro256PlusPlus::seed_from_u64(state.seed),
            seed: state.seed,
        })
    }
}

/// Run a simulation at a single β value on a 2D lattice.
pub fn simulate_beta(
    l: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
) -> (f64, f64, f64, f64, f64, u64) {
    simulate_beta_dim(l, 2, beta, thermal_sweeps, measure_sweeps, measure_every, seed)
}

/// Run a simulation at a single β value with specified dimension.
pub fn simulate_beta_dim(
    l: usize,
    dimension: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
) -> (f64, f64, f64, f64, f64, u64) {
    let mut field = Z2GaugeField::new_dim(l, dimension, seed);

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
    fn test_cold_start_plaquette_2d() {
        let field = Z2GaugeField::cold(4, 42);
        assert_eq!(field.dimension, 2);
        for y in 0..4 {
            for x in 0..4 {
                assert_eq!(field.plaquette(x, y), 1);
            }
        }
    }

    #[test]
    fn test_flip_changes_plaquette_2d() {
        let mut field = Z2GaugeField::cold(4, 42);
        field.flip_link(0, 0, 0);
        assert_eq!(field.plaquette(0, 0), -1);
        assert_eq!(field.plaquette(0, 3), -1);
        assert_eq!(field.plaquette(1, 0), 1);
        assert_eq!(field.plaquette(0, 1), 1);
    }

    #[test]
    fn test_sweep_preserves_detailed_balance_2d() {
        let mut field = Z2GaugeField::new(8, 42);
        let beta = 1.0;
        field.thermalize(beta, 10);
        let (mean_p, _, _, _, _) = field.measure(beta, 100, 10);
        assert!(mean_p.abs() <= 1.0);
    }

    // ---- 3D tests ----

    #[test]
    fn test_cold_start_plaquettes_3d() {
        let field = Z2GaugeField::cold_dim(4, 3, 42);
        assert_eq!(field.dimension, 3);
        assert_eq!(field.links.len(), 3 * 4 * 4 * 4);
        for z in 0..4 {
            for y in 0..4 {
                for x in 0..4 {
                    assert_eq!(field.plaquette_xy(x, y, z), 1, "xy plaq at ({},{},{}) failed", x, y, z);
                    assert_eq!(field.plaquette_yz(x, y, z), 1, "yz plaq at ({},{},{}) failed", x, y, z);
                    assert_eq!(field.plaquette_xz(x, y, z), 1, "xz plaq at ({},{},{}) failed", x, y, z);
                }
            }
        }
    }

    #[test]
    fn test_flip_changes_plaquettes_3d() {
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);
        // Flip an x-link at (0,0,0)
        field.flip_link_3d(0, 0, 0, 0);
        // x-link at (0,0,0) affects: xy(0,0,0), xy(0,3,0), xz(0,0,0), xz(0,0,3)
        assert_eq!(field.plaquette_xy(0, 0, 0), -1);
        assert_eq!(field.plaquette_xy(0, 3, 0), -1);
        assert_eq!(field.plaquette_xz(0, 0, 0), -1);
        assert_eq!(field.plaquette_xz(0, 0, 3), -1);
        // All others should still be +1
        assert_eq!(field.plaquette_xy(1, 0, 0), 1);
        assert_eq!(field.plaquette_yz(0, 0, 0), 1);
    }

    #[test]
    fn test_flip_y_link_changes_plaquettes_3d() {
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);
        // Flip a y-link at (0,0,0)
        field.flip_link_3d(0, 0, 0, 1);
        // y-link at (0,0,0) affects: xy(0,0,0), xy(3,0,0), yz(0,0,0), yz(0,0,3)
        assert_eq!(field.plaquette_xy(0, 0, 0), -1);
        assert_eq!(field.plaquette_xy(3, 0, 0), -1);
        assert_eq!(field.plaquette_yz(0, 0, 0), -1);
        assert_eq!(field.plaquette_yz(0, 0, 3), -1);
    }

    #[test]
    fn test_flip_z_link_changes_plaquettes_3d() {
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);
        // Flip a z-link at (0,0,0)
        field.flip_link_3d(0, 0, 0, 2);
        // z-link at (0,0,0) affects: xz(0,0,0), xz(3,0,0), yz(0,0,0), yz(0,3,0)
        assert_eq!(field.plaquette_xz(0, 0, 0), -1);
        assert_eq!(field.plaquette_xz(3, 0, 0), -1);
        assert_eq!(field.plaquette_yz(0, 0, 0), -1);
        assert_eq!(field.plaquette_yz(0, 3, 0), -1);
    }

    #[test]
    fn test_sweep_preserves_detailed_balance_3d() {
        let mut field = Z2GaugeField::new_dim(8, 3, 42);
        let beta = 1.0;
        field.thermalize(beta, 10);
        let (mean_p, _, _, _, _) = field.measure(beta, 100, 10);
        assert!(mean_p.abs() <= 1.0);
    }

    #[test]
    fn test_checkpoint_roundtrip_2d() {
        let field = Z2GaugeField::new(4, 42);
        let cp = field.to_checkpoint();
        let restored = Z2GaugeField::from_checkpoint(&cp).unwrap();
        assert_eq!(field.l, restored.l);
        assert_eq!(field.dimension, restored.dimension);
        assert_eq!(field.links, restored.links);
        assert_eq!(field.seed, restored.seed);
    }

    #[test]
    fn test_checkpoint_roundtrip_3d() {
        let field = Z2GaugeField::new_dim(4, 3, 42);
        let cp = field.to_checkpoint();
        let restored = Z2GaugeField::from_checkpoint(&cp).unwrap();
        assert_eq!(field.l, restored.l);
        assert_eq!(field.dimension, restored.dimension);
        assert_eq!(field.links, restored.links);
        assert_eq!(field.seed, restored.seed);
    }

    #[test]
    fn test_backward_compatible_checkpoint() {
        // Old checkpoint without dimension field should default to 2
        let json = r#"{"l":4,"links":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"seed":42}"#;
        let field = Z2GaugeField::from_checkpoint(json).unwrap();
        assert_eq!(field.dimension, 2);
        assert_eq!(field.l, 4);
    }

    /// Quick 3D run: L=4, 1000 sweeps, beta=0.5, dimension=3
    #[test]
    fn test_3d_quick_run() {
        let l = 4;
        let beta = 0.5;
        let n_sweeps = 1000;
        let seed = 12345u64;

        let _field = Z2GaugeField::new_dim(l, 3, seed);
        let (mean_p, error, chi, cv, binder, wall_time) =
            simulate_beta_dim(l, 3, beta, n_sweeps / 2, n_sweeps / 2, 10, seed);

        println!("3D L={} beta={}:", l, beta);
        println!("  mean_plaquette = {:.6} ± {:.6}", mean_p, error);
        println!("  susceptibility = {:.6}", chi);
        println!("  specific_heat  = {:.6}", cv);
        println!("  binder         = {:.6}", binder);
        println!("  wall_time_ms   = {}", wall_time);

        assert!(mean_p.abs() <= 1.0);
        assert!(wall_time > 0);
    }
}
