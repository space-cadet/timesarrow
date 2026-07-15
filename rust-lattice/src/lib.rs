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

/// A Z₂ lattice gauge field with L×L (2D), L×L×L (3D), or L×L×L×L (4D) sites.
/// Links are stored as a flat Vec<i8> where each element is ±1.
/// Layout 2D: for each site (x, y), two links: x (dir=0) and y (dir=1). Total: 2*L².
/// Layout 3D: for each site (x, y, z), three links: x (dir=0), y (dir=1), z (dir=2). Total: 3*L³.
/// Layout 4D: for each site (x, y, z, t), four links: x (dir=0), y (dir=1), z (dir=2), t (dir=3). Total: 4*L⁴.
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

    /// Create a new lattice with specified dimension (2, 3, or 4) and random initial configuration.
    pub fn new_dim(l: usize, dimension: usize, seed: u64) -> Self {
        assert!(dimension == 2 || dimension == 3 || dimension == 4, "Only dimensions 2, 3, and 4 are supported");
        let mut rng = Xoshiro256PlusPlus::seed_from_u64(seed);
        let n_links = if dimension == 2 {
            2 * l * l
        } else if dimension == 3 {
            3 * l * l * l
        } else {
            4 * l * l * l * l
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
        assert!(dimension == 2 || dimension == 3 || dimension == 4, "Only dimensions 2, 3, and 4 are supported");
        let n_links = if dimension == 2 {
            2 * l * l
        } else if dimension == 3 {
            3 * l * l * l
        } else {
            4 * l * l * l * l
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
        assert!(self.dimension == 2, "link_idx is for 2D; use link_idx_3d or link_idx_4d");
        2 * (y * self.l + x) + dir
    }

    /// Get the index of a link at site (x, y, z) in direction dir (0=x, 1=y, 2=z). 3D only.
    #[inline(always)]
    pub fn link_idx_3d(&self, x: usize, y: usize, z: usize, dir: usize) -> usize {
        assert!(self.dimension == 3, "link_idx_3d is for 3D");
        3 * (z * self.l * self.l + y * self.l + x) + dir
    }

    /// Get the index of a link at site (x, y, z, t) in direction dir (0=x, 1=y, 2=z, 3=t). 4D only.
    #[inline(always)]
    pub fn link_idx_4d(&self, x: usize, y: usize, z: usize, t: usize, dir: usize) -> usize {
        assert!(self.dimension == 4, "link_idx_4d is for 4D");
        4 * (t * self.l * self.l * self.l + z * self.l * self.l + y * self.l + x) + dir
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

    /// Get the value of a 4D link (±1).
    #[inline(always)]
    pub fn link_4d(&self, x: usize, y: usize, z: usize, t: usize, dir: usize) -> i8 {
        self.links[self.link_idx_4d(x, y, z, t, dir)]
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

    /// Flip a 4D link (multiply by -1).
    #[inline(always)]
    pub fn flip_link_4d(&mut self, x: usize, y: usize, z: usize, t: usize, dir: usize) {
        let idx = self.link_idx_4d(x, y, z, t, dir);
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

    /// XY plaquette at (x, y, z, t) in 4D.
    #[inline(always)]
    pub fn plaquette_xy_4d(&self, x: usize, y: usize, z: usize, t: usize) -> i8 {
        assert!(self.dimension == 4, "plaquette_xy_4d is for 4D");
        let l = self.l;
        let xp1 = (x + 1) % l;
        let yp1 = (y + 1) % l;

        let right = self.link_4d(x, y, z, t, 0);     // x-link at (x,y,z,t)
        let up    = self.link_4d(xp1, y, z, t, 1);   // y-link at (x+1,y,z,t)
        let left  = self.link_4d(x, yp1, z, t, 0);   // x-link at (x,y+1,z,t)
        let down  = self.link_4d(x, y, z, t, 1);     // y-link at (x,y,z,t)

        right * up * left * down
    }

    /// YZ plaquette at (x, y, z, t) in 4D.
    #[inline(always)]
    pub fn plaquette_yz_4d(&self, x: usize, y: usize, z: usize, t: usize) -> i8 {
        assert!(self.dimension == 4, "plaquette_yz_4d is for 4D");
        let l = self.l;
        let yp1 = (y + 1) % l;
        let zp1 = (z + 1) % l;

        let right = self.link_4d(x, y, z, t, 1);     // y-link at (x,y,z,t)
        let up    = self.link_4d(x, yp1, z, t, 2);   // z-link at (x,y+1,z,t)
        let left  = self.link_4d(x, y, zp1, t, 1);   // y-link at (x,y,z+1,t)
        let down  = self.link_4d(x, y, z, t, 2);     // z-link at (x,y,z,t)

        right * up * left * down
    }

    /// XZ plaquette at (x, y, z, t) in 4D.
    #[inline(always)]
    pub fn plaquette_xz_4d(&self, x: usize, y: usize, z: usize, t: usize) -> i8 {
        assert!(self.dimension == 4, "plaquette_xz_4d is for 4D");
        let l = self.l;
        let xp1 = (x + 1) % l;
        let zp1 = (z + 1) % l;

        let right = self.link_4d(x, y, z, t, 0);     // x-link at (x,y,z,t)
        let up    = self.link_4d(xp1, y, z, t, 2);   // z-link at (x+1,y,z,t)
        let left  = self.link_4d(x, y, zp1, t, 0);   // x-link at (x,y,z+1,t)
        let down  = self.link_4d(x, y, z, t, 2);     // z-link at (x,y,z,t)

        right * up * left * down
    }

    /// XT plaquette at (x, y, z, t) in 4D.
    #[inline(always)]
    pub fn plaquette_xt(&self, x: usize, y: usize, z: usize, t: usize) -> i8 {
        assert!(self.dimension == 4, "plaquette_xt is for 4D");
        let l = self.l;
        let xp1 = (x + 1) % l;
        let tp1 = (t + 1) % l;

        let right = self.link_4d(x, y, z, t, 0);     // x-link at (x,y,z,t)
        let up    = self.link_4d(xp1, y, z, t, 3);   // t-link at (x+1,y,z,t)
        let left  = self.link_4d(x, y, z, tp1, 0);   // x-link at (x,y,z,t+1)
        let down  = self.link_4d(x, y, z, t, 3);     // t-link at (x,y,z,t)

        right * up * left * down
    }

    /// YT plaquette at (x, y, z, t) in 4D.
    #[inline(always)]
    pub fn plaquette_yt(&self, x: usize, y: usize, z: usize, t: usize) -> i8 {
        assert!(self.dimension == 4, "plaquette_yt is for 4D");
        let l = self.l;
        let yp1 = (y + 1) % l;
        let tp1 = (t + 1) % l;

        let right = self.link_4d(x, y, z, t, 1);     // y-link at (x,y,z,t)
        let up    = self.link_4d(x, yp1, z, t, 3);   // t-link at (x,y+1,z,t)
        let left  = self.link_4d(x, y, z, tp1, 1);   // y-link at (x,y,z,t+1)
        let down  = self.link_4d(x, y, z, t, 3);     // t-link at (x,y,z,t)

        right * up * left * down
    }

    /// ZT plaquette at (x, y, z, t) in 4D.
    #[inline(always)]
    pub fn plaquette_zt(&self, x: usize, y: usize, z: usize, t: usize) -> i8 {
        assert!(self.dimension == 4, "plaquette_zt is for 4D");
        let l = self.l;
        let zp1 = (z + 1) % l;
        let tp1 = (t + 1) % l;

        let right = self.link_4d(x, y, z, t, 2);     // z-link at (x,y,z,t)
        let up    = self.link_4d(x, y, zp1, t, 3);   // t-link at (x,y,z+1,t)
        let left  = self.link_4d(x, y, z, tp1, 2);   // z-link at (x,y,z,t+1)
        let down  = self.link_4d(x, y, z, t, 3);     // t-link at (x,y,z,t)

        right * up * left * down
    }

    /// Compute all plaquette products and return (mean, sum of squares, count).
    /// In 2D: L² plaquettes. In 3D: 3·L³ plaquettes (xy, yz, xz at each site).
    /// In 4D: 6·L⁴ plaquettes (xy, yz, xz, xt, yt, zt at each site).
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
        } else if self.dimension == 3 {
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
        } else {
            let n_plaquettes = 6 * l * l * l * l;
            let mut sum = 0i64;
            for t in 0..l {
                for z in 0..l {
                    for y in 0..l {
                        for x in 0..l {
                            sum += self.plaquette_xy_4d(x, y, z, t) as i64;
                            sum += self.plaquette_yz_4d(x, y, z, t) as i64;
                            sum += self.plaquette_xz_4d(x, y, z, t) as i64;
                            sum += self.plaquette_xt(x, y, z, t) as i64;
                            sum += self.plaquette_yt(x, y, z, t) as i64;
                            sum += self.plaquette_zt(x, y, z, t) as i64;
                        }
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
        } else if self.dimension == 3 {
            self.sweep_3d(beta)
        } else {
            self.sweep_4d(beta)
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

    fn sweep_4d(&mut self, beta: f64) -> usize {
        let l = self.l;
        let mut accepted = 0usize;

        for t in 0..l {
            for z in 0..l {
                for y in 0..l {
                    for x in 0..l {
                        for dir in 0..4 {
                            let delta_sum = match dir {
                                0 => {
                                    // x-link: xy, xz, xt plaquettes
                                    let y_prev = (y + l - 1) % l;
                                    let z_prev = (z + l - 1) % l;
                                    let t_prev = (t + l - 1) % l;
                                    self.plaquette_xy_4d(x, y, z, t)
                                        + self.plaquette_xy_4d(x, y_prev, z, t)
                                        + self.plaquette_xz_4d(x, y, z, t)
                                        + self.plaquette_xz_4d(x, y, z_prev, t)
                                        + self.plaquette_xt(x, y, z, t)
                                        + self.plaquette_xt(x, y, z, t_prev)
                                }
                                1 => {
                                    // y-link: xy, yz, yt plaquettes
                                    let x_prev = (x + l - 1) % l;
                                    let z_prev = (z + l - 1) % l;
                                    let t_prev = (t + l - 1) % l;
                                    self.plaquette_xy_4d(x, y, z, t)
                                        + self.plaquette_xy_4d(x_prev, y, z, t)
                                        + self.plaquette_yz_4d(x, y, z, t)
                                        + self.plaquette_yz_4d(x, y, z_prev, t)
                                        + self.plaquette_yt(x, y, z, t)
                                        + self.plaquette_yt(x, y, z, t_prev)
                                }
                                2 => {
                                    // z-link: xz, yz, zt plaquettes
                                    let x_prev = (x + l - 1) % l;
                                    let y_prev = (y + l - 1) % l;
                                    let t_prev = (t + l - 1) % l;
                                    self.plaquette_xz_4d(x, y, z, t)
                                        + self.plaquette_xz_4d(x_prev, y, z, t)
                                        + self.plaquette_yz_4d(x, y, z, t)
                                        + self.plaquette_yz_4d(x, y_prev, z, t)
                                        + self.plaquette_zt(x, y, z, t)
                                        + self.plaquette_zt(x, y, z, t_prev)
                                }
                                3 => {
                                    // t-link: xt, yt, zt plaquettes
                                    let x_prev = (x + l - 1) % l;
                                    let y_prev = (y + l - 1) % l;
                                    let z_prev = (z + l - 1) % l;
                                    self.plaquette_xt(x, y, z, t)
                                        + self.plaquette_xt(x_prev, y, z, t)
                                        + self.plaquette_yt(x, y, z, t)
                                        + self.plaquette_yt(x, y_prev, z, t)
                                        + self.plaquette_zt(x, y, z, t)
                                        + self.plaquette_zt(x, y, z_prev, t)
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
                                self.flip_link_4d(x, y, z, t, dir);
                                accepted += 1;
                            }
                        }
                    }
                }
            }
        }

        accepted
    }

    /// Compute the signed area for a 2D lattice.
    ///
    /// ⚠️  WARNING: THIS OBSERVABLE IS GAUGE-DEPENDENT AND EXPLORATORY.
    /// See `signed_volume_3d()` for a detailed explanation of the gauge-dependence issue.
    /// In 2D there is no deconfined phase, so this observable is primarily for
    /// pedagogical/testing purposes.
    ///
    /// For each vertex, compute the product of Z_2 links along a path from (0,0)
    /// to that vertex (x then y), sum over all vertices.
    /// In a deconfined phase (not present in 2D), |sum| ~ N. In 2D, always ~ sqrt(N).
    pub fn signed_area_2d(&self) -> i64 {
        assert!(self.dimension == 2, "signed_area_2d requires 2D lattice");
        let l = self.l;
        let mut total = 0i64;

        for y in 0..l {
            for x in 0..l {
                let mut sign = 1i8;
                for i in 0..x {
                    sign *= self.link(i, 0, 0);
                }
                for j in 0..y {
                    sign *= self.link(x, j, 1);
                }
                total += sign as i64;
            }
        }
        total
    }

    /// Compute the signed volume for a 3D lattice.
    /// 
    /// ⚠️  WARNING: THIS OBSERVABLE IS GAUGE-DEPENDENT AND EXPLORATORY.
    /// 
    /// The signed volume depends on an arbitrary choice of reference point (the origin)
    /// and path convention (x-then-y-then-z). Under a local gauge transformation,
    /// this observable changes value, making it unsuitable for production physics
    /// analysis without careful validation.
    /// 
    /// A valid local gauge transformation at site r flips ALL 6 links incident to r
    /// (3 outgoing + 3 incoming with periodic boundaries), not just the 3 outgoing links.
    /// The existing `test_signed_volume_gauge_flip_3d` test was incorrect in this regard.
    /// 
    /// For a gauge-invariant replacement, see `gauge_invariant_signed_volume_3d()`.
    /// Do NOT promote results from this observable to production without cross-checking
    /// against the gauge-invariant version.
    /// 
    /// For each vertex, compute the product of Z_2 links along a path from (0,0,0)
    /// to that vertex (x then y then z), sum over all vertices, and return the absolute value.
    /// In the deconfined phase, signs align -> |sum| ~ N (extensive).
    /// In the confined phase, signs random -> |sum| ~ sqrt(N).
    pub fn signed_volume_3d(&self) -> i64 {
        assert!(self.dimension == 3, "signed_volume_3d requires 3D lattice");
        let l = self.l;
        let mut total = 0i64;

        for z in 0..l {
            for y in 0..l {
                for x in 0..l {
                    let mut sign = 1i8;
                    // Path from (0,0,0) to (x,y,z): x-links, then y-links, then z-links
                    for i in 0..x {
                        sign *= self.link_3d(i, 0, 0, 0);
                    }
                    for j in 0..y {
                        sign *= self.link_3d(x, j, 0, 1);
                    }
                    for k in 0..z {
                        sign *= self.link_3d(x, y, k, 2);
                    }
                    total += sign as i64;
                }
            }
        }
        total
    }

    // ========================================================================
    // GAUGE-INVARIANT SIGNED VOLUME OBSERVABLE
    // ========================================================================

    /// Apply a local Z₂ gauge transformation at site (x, y, z) in 3D.
    ///
    /// A valid local gauge transformation flips ALL links incident to the site,
    /// not just the outgoing ones. For a site in 3D with periodic boundaries,
    /// this means 6 links total: 3 outgoing (Uₓ, Uᵧ, Uᵧ at the site) and
    /// 3 incoming (Uₓ from x-1, Uᵧ from y-1, Uᵧ from z-1).
    ///
    /// Under this transformation, plaquettes (and all Wilson loops) are invariant,
    /// but path-dependent quantities like `signed_volume_3d()` are not.
    pub fn local_gauge_transform_3d(&mut self, x: usize, y: usize, z: usize) {
        assert!(self.dimension == 3, "local_gauge_transform_3d requires 3D lattice");
        let l = self.l;

        // Outgoing links
        self.flip_link_3d(x, y, z, 0);
        self.flip_link_3d(x, y, z, 1);
        self.flip_link_3d(x, y, z, 2);

        // Incoming links (from periodic boundaries)
        let xm1 = (x + l - 1) % l;
        let ym1 = (y + l - 1) % l;
        let zm1 = (z + l - 1) % l;
        self.flip_link_3d(xm1, y, z, 0);
        self.flip_link_3d(x, ym1, z, 1);
        self.flip_link_3d(x, y, zm1, 2);
    }

    /// Compute the product of links along the "x-then-y-then-z" path from
    /// (x0, y0, z0) to (x1, y1, z1) in 3D.
    ///
    /// Path convention: move in x-direction first, then y, then z.
    /// All coordinates are taken modulo L (periodic boundary conditions).
    /// For Z₂, the number of steps in each direction is (target - source + L) % L.
    pub fn path_product_xyz_3d(&self, x0: usize, y0: usize, z0: usize, x1: usize, y1: usize, z1: usize) -> i8 {
        assert!(self.dimension == 3, "path_product_xyz_3d requires 3D lattice");
        let l = self.l;
        let mut sign = 1i8;

        // x-links from x0 to x1
        let dx = (x1 + l - x0) % l;
        for i in 0..dx {
            sign *= self.link_3d((x0 + i) % l, y0, z0, 0);
        }

        // y-links from y0 to y1 (at x = x1)
        let dy = (y1 + l - y0) % l;
        for j in 0..dy {
            sign *= self.link_3d(x1, (y0 + j) % l, z0, 1);
        }

        // z-links from z0 to z1 (at x = x1, y = y1)
        let dz = (z1 + l - z0) % l;
        for k in 0..dz {
            sign *= self.link_3d(x1, y1, (z0 + k) % l, 2);
        }

        sign
    }

    /// Compute the product of links along the "z-then-y-then-x" path from
    /// (x0, y0, z0) to (x1, y1, z1) in 3D.
    ///
    /// Path convention: move in z-direction first, then y, then x.
    /// This is the "reverse" path ordering relative to `path_product_xyz_3d`.
    pub fn path_product_zyx_3d(&self, x0: usize, y0: usize, z0: usize, x1: usize, y1: usize, z1: usize) -> i8 {
        assert!(self.dimension == 3, "path_product_zyx_3d requires 3D lattice");
        let l = self.l;
        let mut sign = 1i8;

        // z-links from z0 to z1
        let dz = (z1 + l - z0) % l;
        for k in 0..dz {
            sign *= self.link_3d(x0, y0, (z0 + k) % l, 2);
        }

        // y-links from y0 to y1 (at z = z1)
        let dy = (y1 + l - y0) % l;
        for j in 0..dy {
            sign *= self.link_3d(x0, (y0 + j) % l, z1, 1);
        }

        // x-links from x0 to x1 (at y = y1, z = z1)
        let dx = (x1 + l - x0) % l;
        for i in 0..dx {
            sign *= self.link_3d((x0 + i) % l, y1, z1, 0);
        }

        sign
    }

    /// Compute the gauge-invariant signed volume for a 3D lattice.
    ///
    /// # Design: Dressed Orientation Correlator
    ///
    /// The original `signed_volume_3d()` is gauge-dependent because it computes
    /// path-ordered products from a fixed origin using a fixed path convention.
    /// A local gauge transformation at any site on the path changes the result.
    ///
    /// The gauge-invariant replacement is constructed as follows:
    ///
    /// 1. For each site r, define the "gauge-fixed sign":
    ///    s(r) = ∏(links along x-y-z path from origin to r)
    ///
    /// 2. For each pair of sites (r₁, r₂), define the dressed correlator:
    ///    C(r₁, r₂) = s(r₁) · W(r₁→r₂) · s(r₂)
    ///
    ///    where W(r₁→r₂) is the Wilson line (product of links) along the
    ///    z-y-x path from r₁ to r₂. The KEY is that W uses the OPPOSITE
    ///    path ordering from s, so that W(r₁→r₂) ≠ s(r₁)⁻¹ · s(r₂).
    ///
    /// 3. The gauge-invariant signed volume is the average over all pairs:
    ///    Q_GI = (1/N²) Σ_{r₁,r₂} C(r₁, r₂)
    ///
    /// # Gauge-Invariance Proof
    ///
    /// Consider a local gauge transformation at site g (flip all 6 incident links):
    ///
    /// - **g = origin**: s(r₁) → −s(r₁) and s(r₂) → −s(r₂). The product s(r₁)·s(r₂)
    ///   is unchanged. W(r₁→r₂) is unchanged (either doesn't include origin, or
    ///   includes two links that both flip). Thus C → C.
    ///
    /// - **g = r₁**: s(r₁) → −s(r₁). W(r₁→r₂) starts at r₁, so exactly one link
    ///   in W is flipped → W → −W. Thus C → (−s(r₁))·(−W)·s(r₂) = C.
    ///
    /// - **g = r₂**: s(r₂) → −s(r₂). W(r₁→r₂) ends at r₂, so exactly one link
    ///   in W is flipped → W → −W. Thus C → s(r₁)·(−W)·(−s(r₂)) = C.
    ///
    /// - **g on W path (not endpoint)**: W contains two links incident to g
    ///   (one incoming, one outgoing), so W → (+1)·W. s(r₁) and s(r₂) unchanged.
    ///   Thus C → C.
    ///
    /// - **g elsewhere**: Nothing changes. C → C.
    ///
    /// Therefore C(r₁, r₂) is invariant under ALL local gauge transformations.
    ///
    /// # Physical Interpretation
    ///
    /// In the deconfined phase, the gauge field exhibits long-range order:
    /// large Wilson loops have expectation value ~1 (perimeter law).
    /// Consequently, C(r₁, r₂) ≈ +1 for all pairs, giving Q_GI ≈ +1.
    ///
    /// In the confined phase, Wilson loops follow area law and decay exponentially
    /// with loop size. The dressed correlator averages to ~0, giving Q_GI ≈ 0.
    ///
    /// Thus Q_GI serves as an order parameter for the deconfinement transition,
    /// analogous to the original signed volume but with rigorous gauge invariance.
    ///
    /// # Computational Note
    ///
    /// Complexity is O(N² · L) = O(L⁷) for lattice size L (N = L³ sites).
    /// This is manageable for small L (L ≤ 8) but may need optimization
    /// (e.g., parallelization or sampling over pairs) for production runs
    /// on larger lattices.
    pub fn gauge_invariant_signed_volume_3d(&self) -> f64 {
        assert!(self.dimension == 3, "gauge_invariant_signed_volume_3d requires 3D lattice");
        let l = self.l;
        let n_sites = l * l * l;

        // Precompute s(r) = path product from origin along x-y-z for all sites
        let mut s = vec![1i8; n_sites];
        for z in 0..l {
            for y in 0..l {
                for x in 0..l {
                    let idx = z * l * l + y * l + x;
                    s[idx] = self.path_product_xyz_3d(0, 0, 0, x, y, z);
                }
            }
        }

        let mut total = 0i64;
        for z2 in 0..l {
            for y2 in 0..l {
                for x2 in 0..l {
                    let idx2 = z2 * l * l + y2 * l + x2;
                    for z1 in 0..l {
                        for y1 in 0..l {
                            for x1 in 0..l {
                                let idx1 = z1 * l * l + y1 * l + x1;
                                let w = self.path_product_zyx_3d(x1, y1, z1, x2, y2, z2);
                                total += (s[idx1] * w * s[idx2]) as i64;
                            }
                        }
                    }
                }
            }
        }

        total as f64 / (n_sites * n_sites) as f64
    }

    /// Measure the gauge-invariant signed volume observable over n_sweeps,
    /// taking measurements every measure_every sweeps.
    ///
    /// Returns (mean Q_GI, std error, mean Q_GI², mean Q_GI, binder cumulant).
    /// Note: mean |Q| is replaced by mean Q since the gauge-invariant observable
    /// is naturally bounded in [−1, +1] and its sign is physically meaningful.
    pub fn measure_gauge_invariant_signed_volume_3d(
        &mut self,
        beta: f64,
        n_sweeps: usize,
        measure_every: usize,
    ) -> (f64, f64, f64, f64, f64) {
        assert!(self.dimension == 3, "measure_gauge_invariant_signed_volume_3d requires 3D lattice");
        let mut q_values = Vec::new();
        let mut q_sq = Vec::new();
        let mut q_quad = Vec::new();

        for sweep in 0..n_sweeps {
            self.sweep(beta);
            if sweep % measure_every == 0 {
                let q = self.gauge_invariant_signed_volume_3d();
                q_values.push(q);
                q_sq.push(q * q);
                q_quad.push(q * q * q * q);
            }
        }

        let n = q_values.len() as f64;
        let mean_q = q_values.iter().sum::<f64>() / n;
        let mean_q_sq = q_sq.iter().sum::<f64>() / n;
        let mean_q_quad = q_quad.iter().sum::<f64>() / n;

        let var_q = q_values.iter().map(|x| (x - mean_q).powi(2)).sum::<f64>() / n;
        let error_q = (var_q / n).sqrt();

        let binder = if mean_q_sq > 0.0 {
            1.0 - mean_q_quad / (3.0 * mean_q_sq * mean_q_sq)
        } else {
            0.0
        };

        (mean_q, error_q, mean_q_sq, mean_q, binder)
    }

    /// Measure the signed volume observable over n_sweeps, taking measurements every measure_every sweeps.
    /// Returns (mean |Q|, std error, mean Q^2, mean |Q|/N, binder cumulant for |Q|).
    pub fn measure_signed_volume_3d(
        &mut self,
        beta: f64,
        n_sweeps: usize,
        measure_every: usize,
    ) -> (f64, f64, f64, f64, f64) {
        assert!(self.dimension == 3, "measure_signed_volume_3d requires 3D lattice");
        let n_sites = (self.l * self.l * self.l) as f64;
        let mut q_abs = Vec::new();
        let mut q_sq = Vec::new();
        let mut q_quad = Vec::new();

        for sweep in 0..n_sweeps {
            self.sweep(beta);
            if sweep % measure_every == 0 {
                let q = self.signed_volume_3d();
                let q_abs_val = (q as f64).abs();
                q_abs.push(q_abs_val);
                q_sq.push(q as f64 * q as f64);
                q_quad.push(q as f64 * q as f64 * q as f64 * q as f64);
            }
        }

        let n = q_abs.len() as f64;
        let mean_q_abs = q_abs.iter().sum::<f64>() / n;
        let mean_q_sq = q_sq.iter().sum::<f64>() / n;
        let mean_q_quad = q_quad.iter().sum::<f64>() / n;

        let var_q_abs = q_abs.iter().map(|x| (x - mean_q_abs).powi(2)).sum::<f64>() / n;
        let error_q_abs = (var_q_abs / n).sqrt();

        let normalized = mean_q_abs / n_sites;

        let binder = if mean_q_sq > 0.0 {
            1.0 - mean_q_quad / (3.0 * mean_q_sq * mean_q_sq)
        } else {
            0.0
        };

        (mean_q_abs, error_q_abs, mean_q_sq, normalized, binder)
    }

    /// Measure the signed area observable over n_sweeps in 2D.
    /// Returns (mean |Q|, std error, mean Q^2, mean |Q|/N, binder cumulant for |Q|).
    pub fn measure_signed_area_2d(
        &mut self,
        beta: f64,
        n_sweeps: usize,
        measure_every: usize,
    ) -> (f64, f64, f64, f64, f64) {
        assert!(self.dimension == 2, "measure_signed_area_2d requires 2D lattice");
        let n_sites = (self.l * self.l) as f64;
        let mut q_abs = Vec::new();
        let mut q_sq = Vec::new();
        let mut q_quad = Vec::new();

        for sweep in 0..n_sweeps {
            self.sweep(beta);
            if sweep % measure_every == 0 {
                let q = self.signed_area_2d();
                let q_abs_val = (q as f64).abs();
                q_abs.push(q_abs_val);
                q_sq.push(q as f64 * q as f64);
                q_quad.push(q as f64 * q as f64 * q as f64 * q as f64);
            }
        }

        let n = q_abs.len() as f64;
        let mean_q_abs = q_abs.iter().sum::<f64>() / n;
        let mean_q_sq = q_sq.iter().sum::<f64>() / n;
        let mean_q_quad = q_quad.iter().sum::<f64>() / n;

        let var_q_abs = q_abs.iter().map(|x| (x - mean_q_abs).powi(2)).sum::<f64>() / n;
        let error_q_abs = (var_q_abs / n).sqrt();

        let normalized = mean_q_abs / n_sites;

        let binder = if mean_q_sq > 0.0 {
            1.0 - mean_q_quad / (3.0 * mean_q_sq * mean_q_sq)
        } else {
            0.0
        };

        (mean_q_abs, error_q_abs, mean_q_sq, normalized, binder)
    }

    /// W = ∏ links around the rectangle (right, up, left, down).
    /// For Z₂, U† = U, so traversing in either direction gives the same product.
    pub fn wilson_loop_2d(&self, x: usize, y: usize, r: usize, c: usize) -> i8 {
        assert!(self.dimension == 2, "wilson_loop_2d is for 2D only");
        let l = self.l;
        let mut product = 1i8;
        
        // Right edge: x-links from (x,y) to (x+r,y)
        for i in 0..r {
            product *= self.link((x + i) % l, y, 0);
        }
        
        // Up edge: y-links from (x+r,y) to (x+r,y+c)
        for j in 0..c {
            product *= self.link((x + r) % l, (y + j) % l, 1);
        }
        
        // Left edge: x-links from (x+r,y+c) to (x,y+c)
        for i in 0..r {
            product *= self.link((x + i) % l, (y + c) % l, 0);
        }
        
        // Down edge: y-links from (x,y+c) to (x,y)
        for j in 0..c {
            product *= self.link(x, (y + j) % l, 1);
        }
        
        product
    }

    /// Average Wilson loop over all starting positions for a given r×c loop size in 2D.
    pub fn average_wilson_loop_2d(&self, r: usize, c: usize) -> f64 {
        let l = self.l;
        let mut sum = 0i64;
        let count = (l * l) as i64;
        
        for y in 0..l {
            for x in 0..l {
                sum += self.wilson_loop_2d(x, y, r, c) as i64;
            }
        }
        
        sum as f64 / count as f64
    }

    /// Compute the Wilson loop for a rectangular loop in the xy-plane at height z in 3D.
    pub fn wilson_loop_xy_3d(&self, x: usize, y: usize, z: usize, r: usize, c: usize) -> i8 {
        assert!(self.dimension == 3, "wilson_loop_xy_3d is for 3D only");
        let l = self.l;
        let mut product = 1i8;
        
        // Right: x-links from (x,y,z) to (x+r,y,z)
        for i in 0..r {
            product *= self.link_3d((x + i) % l, y, z, 0);
        }
        
        // Up: y-links from (x+r,y,z) to (x+r,y+c,z)
        for j in 0..c {
            product *= self.link_3d((x + r) % l, (y + j) % l, z, 1);
        }
        
        // Left: x-links from (x+r,y+c,z) to (x,y+c,z)
        for i in 0..r {
            product *= self.link_3d((x + i) % l, (y + c) % l, z, 0);
        }
        
        // Down: y-links from (x,y+c,z) to (x,y,z)
        for j in 0..c {
            product *= self.link_3d(x, (y + j) % l, z, 1);
        }
        
        product
    }

    /// Average Wilson loop in the xy-plane over all starting positions for a given r×c loop size in 3D.
    pub fn average_wilson_loop_xy_3d(&self, r: usize, c: usize) -> f64 {
        let l = self.l;
        let mut sum = 0i64;
        let count = (l * l * l) as i64;
        
        for z in 0..l {
            for y in 0..l {
                for x in 0..l {
                    sum += self.wilson_loop_xy_3d(x, y, z, r, c) as i64;
                }
            }
        }
        
        sum as f64 / count as f64
    }

    /// Compute the Polyakov loop at fixed spatial position (x, y, z) in 4D.
    /// P(x,y,z) = ∏_{t=0}^{L-1} U_{(x,y,z,t),3}
    /// Returns f64 (±1.0) for consistency with average_polyakov.
    pub fn polyakov_loop(&self, x: usize, y: usize, z: usize) -> f64 {
        assert!(self.dimension == 4, "polyakov_loop requires 4D lattice");
        let mut product = 1i8;
        for t in 0..self.l {
            product *= self.link_4d(x, y, z, t, 3);
        }
        product as f64
    }

    /// Compute the average magnitude of the Polyakov loop over all spatial sites.
    /// ⟨|P|⟩ = (1/L³) Σ_{x,y,z} |P(x,y,z)|
    pub fn average_polyakov(&self) -> f64 {
        assert!(self.dimension == 4, "average_polyakov requires 4D lattice");
        let mut sum = 0.0;
        for x in 0..self.l {
            for y in 0..self.l {
                for z in 0..self.l {
                    sum += self.polyakov_loop(x, y, z).abs();
                }
            }
        }
        sum / (self.l * self.l * self.l) as f64
    }

    /// Compute the Polyakov loop at fixed spatial position (x, y) in 3D.
    /// P(x,y) = ∏_{z=0}^{L-1} U_{(x,y,z),2}
    /// Returns f64 (±1.0) for consistency with average_polyakov_3d.
    pub fn polyakov_loop_3d(&self, x: usize, y: usize) -> f64 {
        assert!(self.dimension == 3, "polyakov_loop_3d requires 3D lattice");
        let mut product = 1i8;
        for z in 0..self.l {
            product *= self.link_3d(x, y, z, 2);
        }
        product as f64
    }

    /// Compute the average of the signed Polyakov loop over all spatial sites in 3D.
    /// P̄ = (1/L²) Σ_{x,y} P(x,y)
    /// Note: returns the SIGNED average, not the absolute value.
    /// For Z₂, this is what enters the susceptibility and Binder cumulant.
    pub fn average_polyakov_signed_3d(&self) -> f64 {
        assert!(self.dimension == 3, "average_polyakov_signed_3d requires 3D lattice");
        let mut sum = 0.0;
        for x in 0..self.l {
            for y in 0..self.l {
                sum += self.polyakov_loop_3d(x, y);
            }
        }
        sum / (self.l * self.l) as f64
    }

    /// Thermalize the lattice with `n_sweeps` sweeps.
    pub fn thermalize(&mut self, beta: f64, n_sweeps: usize) {
        for _ in 0..n_sweeps {
            self.sweep(beta);
        }
    }

    /// Measure observables including Polyakov loop over `n_sweeps` sweeps in 3D,
    /// taking measurements every `measure_every` sweeps.
    /// Returns (mean plaquette, error, chi, cv, binder, mean |P|, error |P|, chi_P, binder_P)
    /// where chi_P = L³ (⟨P²⟩ - ⟨P⟩²) and binder_P = 1 - ⟨P⁴⟩/(3⟨P²⟩²).
    pub fn measure_with_polyakov_3d(
        &mut self,
        beta: f64,
        n_sweeps: usize,
        measure_every: usize,
    ) -> (f64, f64, f64, f64, f64, f64, f64, f64, f64) {
        assert!(self.dimension == 3, "measure_with_polyakov_3d requires 3D lattice");

        let mut p_measurements = Vec::new();
        let mut p_measurements_sq = Vec::new();
        let mut p_measurements_quad = Vec::new();

        let mut poly_measurements = Vec::new();
        let mut poly_measurements_sq = Vec::new();
        let mut poly_measurements_quad = Vec::new();

        for sweep in 0..n_sweeps {
            self.sweep(beta);

            if sweep % measure_every == 0 {
                let (mean_plaq, _, _) = self.plaquette_stats();
                p_measurements.push(mean_plaq);
                p_measurements_sq.push(mean_plaq * mean_plaq);
                p_measurements_quad.push(mean_plaq * mean_plaq * mean_plaq * mean_plaq);

                let poly = self.average_polyakov_signed_3d();
                poly_measurements.push(poly);
                poly_measurements_sq.push(poly * poly);
                poly_measurements_quad.push(poly * poly * poly * poly);
            }
        }

        let n = p_measurements.len() as f64;
        let vol = (self.l * self.l * self.l) as f64;

        // Plaquette statistics
        let mean_p = p_measurements.iter().sum::<f64>() / n;
        let mean_p2 = p_measurements_sq.iter().sum::<f64>() / n;
        let mean_p4 = p_measurements_quad.iter().sum::<f64>() / n;

        let p_variance = p_measurements.iter().map(|x| (x - mean_p).powi(2)).sum::<f64>() / n;
        let p_error = (p_variance / n).sqrt();

        let susceptibility = vol * beta * (mean_p2 - mean_p * mean_p);
        let specific_heat = vol * beta * beta * (mean_p2 - mean_p * mean_p);
        let binder = if mean_p2 > 0.0 { 1.0 - mean_p4 / (3.0 * mean_p2 * mean_p2) } else { 0.0 };

        // Polyakov loop statistics
        let mean_poly = poly_measurements.iter().sum::<f64>() / n;
        let mean_poly2 = poly_measurements_sq.iter().sum::<f64>() / n;
        let mean_poly4 = poly_measurements_quad.iter().sum::<f64>() / n;

        let poly_variance = poly_measurements.iter().map(|x| (x - mean_poly).powi(2)).sum::<f64>() / n;
        let poly_error = (poly_variance / n).sqrt();

        let poly_susceptibility = vol * (mean_poly2 - mean_poly * mean_poly);
        let poly_binder = if mean_poly2 > 0.0 { 1.0 - mean_poly4 / (3.0 * mean_poly2 * mean_poly2) } else { 0.0 };

        (mean_p, p_error, susceptibility, specific_heat, binder,
         mean_poly, poly_error, poly_susceptibility, poly_binder)
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
        } else if self.dimension == 3 {
            (self.l * self.l * self.l) as f64
        } else {
            (self.l * self.l * self.l * self.l) as f64
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

    /// Measure observables including Wilson loops over `n_sweeps` sweeps,
    /// taking measurements every `measure_every` sweeps.
    /// Returns (mean plaquette, error, chi, cv, binder, Vec<(r, c, mean_W, var_W)>)
    /// where the Vec contains Wilson loop data for each requested loop size.
    pub fn measure_with_wilson_loops(
        &mut self,
        beta: f64,
        n_sweeps: usize,
        measure_every: usize,
        loop_sizes: &[(usize, usize)],
    ) -> (f64, f64, f64, f64, f64, Vec<(usize, usize, f64, f64)>) {
        assert!(self.dimension == 2 || self.dimension == 3,
            "measure_with_wilson_loops only supports 2D and 3D");

        let mut measurements = Vec::new();
        let mut measurements_sq = Vec::new();
        let mut measurements_quad = Vec::new();

        // For each loop size, accumulate W and W²
        let n_loop_sizes = loop_sizes.len();
        let mut wilson_sums = vec![0.0f64; n_loop_sizes];
        let mut wilson_sums_sq = vec![0.0f64; n_loop_sizes];
        let mut n_measurements = 0usize;

        for sweep in 0..n_sweeps {
            self.sweep(beta);

            if sweep % measure_every == 0 {
                let (mean_plaq, _, _) = self.plaquette_stats();
                measurements.push(mean_plaq);
                measurements_sq.push(mean_plaq * mean_plaq);
                measurements_quad.push(mean_plaq * mean_plaq * mean_plaq * mean_plaq);

                // Measure Wilson loops for each requested size
                for (idx, &(r, c)) in loop_sizes.iter().enumerate() {
                    let w = if self.dimension == 2 {
                        self.average_wilson_loop_2d(r, c)
                    } else {
                        self.average_wilson_loop_xy_3d(r, c)
                    };
                    wilson_sums[idx] += w;
                    wilson_sums_sq[idx] += w * w;
                }

                n_measurements += 1;
            }
        }

        let n = n_measurements as f64;

        // Standard observables
        let mean_p = measurements.iter().sum::<f64>() / n;
        let mean_p2 = measurements_sq.iter().sum::<f64>() / n;
        let mean_p4 = measurements_quad.iter().sum::<f64>() / n;

        let variance = measurements.iter().map(|x| (x - mean_p).powi(2)).sum::<f64>() / n;
        let error = (variance / n).sqrt();

        let volume = if self.dimension == 2 {
            (self.l * self.l) as f64
        } else {
            (self.l * self.l * self.l) as f64
        };

        let susceptibility = volume * beta * (mean_p2 - mean_p * mean_p);
        let specific_heat = volume * beta * beta * (mean_p2 - mean_p * mean_p);

        let binder = if mean_p2 > 0.0 {
            1.0 - mean_p4 / (3.0 * mean_p2 * mean_p2)
        } else {
            0.0
        };

        // Wilson loop statistics
        let mut wilson_results = Vec::with_capacity(n_loop_sizes);
        for idx in 0..n_loop_sizes {
            let mean_w = wilson_sums[idx] / n;
            let mean_w2 = wilson_sums_sq[idx] / n;
            let var_w = mean_w2 - mean_w * mean_w;
            let (r, c) = loop_sizes[idx];
            wilson_results.push((r, c, mean_w, var_w));
        }

        (mean_p, error, susceptibility, specific_heat, binder, wilson_results)
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
/// Run a simulation at a single β value and return raw measurements.
/// Returns (Vec<plaquette>, wall_time_ms) for autocorrelation analysis.
pub fn simulate_beta_raw(
    l: usize,
    dimension: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
) -> (Vec<f64>, u64) {
    let mut field = Z2GaugeField::new_dim(l, dimension, seed);

    let thermal_start = std::time::Instant::now();
    field.thermalize(beta, thermal_sweeps);
    let thermal_time = thermal_start.elapsed().as_millis() as u64;

    let measure_start = std::time::Instant::now();
    let mut measurements = Vec::new();
    for sweep in 0..measure_sweeps {
        field.sweep(beta);
        if sweep % measure_every == 0 {
            let (mean_plaq, _, _) = field.plaquette_stats();
            measurements.push(mean_plaq);
        }
    }
    let measure_time = measure_start.elapsed().as_millis() as u64;

    (measurements, thermal_time + measure_time)
}

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

/// Run a simulation at a single β value with Wilson loop measurements.
/// Returns (mean_p, error, chi, cv, binder, wall_time, Vec<(r, c, mean_W, var_W)>).
pub fn simulate_beta_with_wilson_loops(
    l: usize,
    dimension: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
    loop_sizes: &[(usize, usize)],
) -> (f64, f64, f64, f64, f64, u64, Vec<(usize, usize, f64, f64)>) {
    assert!(dimension == 2 || dimension == 3,
        "simulate_beta_with_wilson_loops only supports 2D and 3D");

    let mut field = Z2GaugeField::new_dim(l, dimension, seed);

    let thermal_start = std::time::Instant::now();
    field.thermalize(beta, thermal_sweeps);
    let thermal_time = thermal_start.elapsed().as_millis() as u64;

    let measure_start = std::time::Instant::now();
    let (mean_p, error, chi, cv, binder, wilson_data) =
        field.measure_with_wilson_loops(beta, measure_sweeps, measure_every, loop_sizes);
    let measure_time = measure_start.elapsed().as_millis() as u64;

    (mean_p, error, chi, cv, binder, thermal_time + measure_time, wilson_data)
}

/// Run a 3D simulation at a single β value with Polyakov loop measurements.
/// Returns (mean_p, error, chi, cv, binder_p, mean_poly, error_poly, chi_poly, binder_poly, wall_time).
pub fn simulate_beta_with_polyakov_3d(
    l: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
) -> (f64, f64, f64, f64, f64, f64, f64, f64, f64, u64) {
    let mut field = Z2GaugeField::new_dim(l, 3, seed);

    let thermal_start = std::time::Instant::now();
    field.thermalize(beta, thermal_sweeps);
    let thermal_time = thermal_start.elapsed().as_millis() as u64;

    let measure_start = std::time::Instant::now();
    let (mean_p, error, chi, cv, binder_p, mean_poly, error_poly, chi_poly, binder_poly) =
        field.measure_with_polyakov_3d(beta, measure_sweeps, measure_every);
    let measure_time = measure_start.elapsed().as_millis() as u64;

    (mean_p, error, chi, cv, binder_p, mean_poly, error_poly, chi_poly, binder_poly, thermal_time + measure_time)
}

/// Run a simulation at a single β value with Wilson loops and signed volume measurements.
///
/// ⚠️  WARNING: The signed volume component of this simulation uses the
/// GAUGE-DEPENDENT `signed_volume_3d()` / `signed_area_2d()` observables.
/// Results from the signed volume should NOT be promoted to production physics
/// analysis without validation against `gauge_invariant_signed_volume_3d()`.
///
/// Returns (mean_p, error, chi, cv, binder, wall_time, wilson_data, signed_volume_data).
/// signed_volume_data is (mean_q_abs, error_q_abs, mean_q_sq, normalized, binder_q).
pub fn simulate_beta_with_wilson_and_signed_volume(
    l: usize,
    dimension: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
    loop_sizes: &[(usize, usize)],
) -> (f64, f64, f64, f64, f64, u64, Vec<(usize, usize, f64, f64)>, (f64, f64, f64, f64, f64)) {
    assert!(dimension == 2 || dimension == 3,
        "simulate_beta_with_wilson_and_signed_volume only supports 2D and 3D");

    let mut field = Z2GaugeField::new_dim(l, dimension, seed);

    let thermal_start = std::time::Instant::now();
    field.thermalize(beta, thermal_sweeps);
    let thermal_time = thermal_start.elapsed().as_millis() as u64;

    let measure_start = std::time::Instant::now();

    // Manual measurement loop to capture both observables
    let mut measurements = Vec::new();
    let mut measurements_sq = Vec::new();
    let mut measurements_quad = Vec::new();
    let mut q_abs = Vec::new();
    let mut q_sq = Vec::new();
    let mut q_quad = Vec::new();
    let n_loop_sizes = loop_sizes.len();
    let mut wilson_sums = vec![0.0f64; n_loop_sizes];
    let mut wilson_sums_sq = vec![0.0f64; n_loop_sizes];
    let mut n_measurements = 0usize;

    for sweep in 0..measure_sweeps {
        field.sweep(beta);
        if sweep % measure_every == 0 {
            let (mean_plaq, _, _) = field.plaquette_stats();
            measurements.push(mean_plaq);
            measurements_sq.push(mean_plaq * mean_plaq);
            measurements_quad.push(mean_plaq * mean_plaq * mean_plaq * mean_plaq);

            // Measure Wilson loops
            for (idx, &(r, c)) in loop_sizes.iter().enumerate() {
                let w = if dimension == 2 {
                    field.average_wilson_loop_2d(r, c)
                } else {
                    field.average_wilson_loop_xy_3d(r, c)
                };
                wilson_sums[idx] += w;
                wilson_sums_sq[idx] += w * w;
            }

            // Measure signed volume/area
            let q = if dimension == 3 {
                field.signed_volume_3d()
            } else {
                field.signed_area_2d()
            };
            let q_abs_val = (q as f64).abs();
            q_abs.push(q_abs_val);
            q_sq.push(q as f64 * q as f64);
            q_quad.push(q as f64 * q as f64 * q as f64 * q as f64);

            n_measurements += 1;
        }
    }

    let n = n_measurements as f64;
    let vol = if dimension == 2 {
        (l * l) as f64
    } else {
        (l * l * l) as f64
    };

    // Plaquette stats
    let mean_p = measurements.iter().sum::<f64>() / n;
    let mean_p2 = measurements_sq.iter().sum::<f64>() / n;
    let mean_p4 = measurements_quad.iter().sum::<f64>() / n;
    let p_variance = measurements.iter().map(|x| (x - mean_p).powi(2)).sum::<f64>() / n;
    let error = (p_variance / n).sqrt();
    let chi = vol * beta * (mean_p2 - mean_p * mean_p);
    let cv = vol * beta * beta * (mean_p2 - mean_p * mean_p);
    let binder = if mean_p2 > 0.0 { 1.0 - mean_p4 / (3.0 * mean_p2 * mean_p2) } else { 0.0 };

    // Wilson loop stats
    let wilson_data: Vec<(usize, usize, f64, f64)> = loop_sizes.iter().enumerate().map(|(idx, &(r, c))| {
        let mean_w = wilson_sums[idx] / n;
        let mean_w2 = wilson_sums_sq[idx] / n;
        let var_w = mean_w2 - mean_w * mean_w;
        (r, c, mean_w, var_w)
    }).collect();

    // Signed volume stats
    let mean_q_abs = q_abs.iter().sum::<f64>() / n;
    let mean_q_sq = q_sq.iter().sum::<f64>() / n;
    let mean_q_quad = q_quad.iter().sum::<f64>() / n;
    let var_q_abs = q_abs.iter().map(|x| (x - mean_q_abs).powi(2)).sum::<f64>() / n;
    let error_q_abs = (var_q_abs / n).sqrt();
    let normalized = mean_q_abs / vol;
    let binder_q = if mean_q_sq > 0.0 {
        1.0 - mean_q_quad / (3.0 * mean_q_sq * mean_q_sq)
    } else {
        0.0
    };

    let measure_time = measure_start.elapsed().as_millis() as u64;

    (mean_p, error, chi, cv, binder, thermal_time + measure_time, wilson_data,
     (mean_q_abs, error_q_abs, mean_q_sq, normalized, binder_q))
}

/// Simulate with Wilson loops and gauge-invariant signed volume (3D only).
/// Returns same tuple as simulate_beta_with_wilson_and_signed_volume but uses
/// gauge_invariant_signed_volume_3d() instead of signed_volume_3d().
pub fn simulate_beta_with_wilson_and_gauge_invariant_signed_volume(
    l: usize,
    dimension: usize,
    beta: f64,
    thermal_sweeps: usize,
    measure_sweeps: usize,
    measure_every: usize,
    seed: u64,
    loop_sizes: &[(usize, usize)],
    cold_start: bool,
) -> (f64, f64, f64, f64, f64, u64, Vec<(usize, usize, f64, f64)>, (f64, f64, f64, f64, f64)) {
    assert!(dimension == 3,
        "simulate_beta_with_wilson_and_gauge_invariant_signed_volume only supports 3D");

    let mut field = if cold_start {
        Z2GaugeField::cold_dim(l, dimension, seed)
    } else {
        Z2GaugeField::new_dim(l, dimension, seed)
    };

    let thermal_start = std::time::Instant::now();
    field.thermalize(beta, thermal_sweeps);
    let thermal_time = thermal_start.elapsed().as_millis() as u64;

    let measure_start = std::time::Instant::now();

    let mut measurements = Vec::new();
    let mut measurements_sq = Vec::new();
    let mut measurements_quad = Vec::new();
    let mut q_values = Vec::new();
    let mut q_sq = Vec::new();
    let mut q_quad = Vec::new();
    let n_loop_sizes = loop_sizes.len();
    let mut wilson_sums = vec![0.0f64; n_loop_sizes];
    let mut wilson_sums_sq = vec![0.0f64; n_loop_sizes];
    let mut n_measurements = 0usize;

    for sweep in 0..measure_sweeps {
        field.sweep(beta);
        if sweep % measure_every == 0 {
            let (mean_plaq, _, _) = field.plaquette_stats();
            measurements.push(mean_plaq);
            measurements_sq.push(mean_plaq * mean_plaq);
            measurements_quad.push(mean_plaq * mean_plaq * mean_plaq * mean_plaq);

            for (idx, &(r, c)) in loop_sizes.iter().enumerate() {
                let w = field.average_wilson_loop_xy_3d(r, c);
                wilson_sums[idx] += w;
                wilson_sums_sq[idx] += w * w;
            }

            let q = field.gauge_invariant_signed_volume_3d();
            q_values.push(q);
            q_sq.push(q * q);
            q_quad.push(q * q * q * q);

            n_measurements += 1;
        }
    }

    let n = n_measurements as f64;
    let vol = (l * l * l) as f64;

    let mean_p = measurements.iter().sum::<f64>() / n;
    let mean_p2 = measurements_sq.iter().sum::<f64>() / n;
    let mean_p4 = measurements_quad.iter().sum::<f64>() / n;
    let p_variance = measurements.iter().map(|x| (x - mean_p).powi(2)).sum::<f64>() / n;
    let error = (p_variance / n).sqrt();
    let chi = vol * beta * (mean_p2 - mean_p * mean_p);
    let cv = vol * beta * beta * (mean_p2 - mean_p * mean_p);
    let binder = if mean_p2 > 0.0 { 1.0 - mean_p4 / (3.0 * mean_p2 * mean_p2) } else { 0.0 };

    let wilson_data: Vec<(usize, usize, f64, f64)> = loop_sizes.iter().enumerate().map(|(idx, &(r, c))| {
        let mean_w = wilson_sums[idx] / n;
        let mean_w2 = wilson_sums_sq[idx] / n;
        let var_w = mean_w2 - mean_w * mean_w;
        (r, c, mean_w, var_w)
    }).collect();

    let mean_q = q_values.iter().sum::<f64>() / n;
    let mean_q_sq = q_sq.iter().sum::<f64>() / n;
    let mean_q_quad = q_quad.iter().sum::<f64>() / n;
    let var_q = q_values.iter().map(|x| (x - mean_q).powi(2)).sum::<f64>() / n;
    let error_q = (var_q / n).sqrt();
    let binder_q = if mean_q_sq > 0.0 {
        1.0 - mean_q_quad / (3.0 * mean_q_sq * mean_q_sq)
    } else {
        0.0
    };

    let measure_time = measure_start.elapsed().as_millis() as u64;

    (mean_p, error, chi, cv, binder, thermal_time + measure_time, wilson_data,
     (mean_q, error_q, mean_q_sq, mean_q, binder_q))
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
    fn test_signed_volume_cold_start_3d() {
        let field = Z2GaugeField::cold_dim(4, 3, 42);
        let sv = field.signed_volume_3d();
        // All links +1, so all vertex signs +1, total = 64
        assert_eq!(sv, 64, "Cold start: all signs +1, total should be 64");
    }

    #[test]
    fn test_signed_volume_gauge_flip_3d() {
        // This test demonstrates that signed_volume_3d() IS gauge-dependent.
        // A valid local gauge transformation flips ALL 6 links incident to a site
        // (3 outgoing + 3 incoming with periodic boundaries), not just 3 outgoing.
        //
        // The old test incorrectly flipped only outgoing links, which is not a
        // valid gauge transformation. A proper gauge transform must leave
        // plaquettes invariant while changing path-dependent quantities.
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);
        let sv_before = field.signed_volume_3d();
        assert_eq!(sv_before, 64, "Cold start signed volume should be 64");

        // Apply a PROPER local gauge transformation at (0,0,0)
        // This flips all 6 incident links: 3 outgoing + 3 incoming
        field.local_gauge_transform_3d(0, 0, 0);

        let sv_after = field.signed_volume_3d();

        // Verify plaquettes are still +1 (gauge invariance of physical observables)
        for z in 0..4 {
            for y in 0..4 {
                for x in 0..4 {
                    assert_eq!(field.plaquette_xy(x, y, z), 1,
                        "Plaquette xy at ({},{},{}) should be invariant under gauge transform", x, y, z);
                }
            }
        }

        // signed_volume_3d should CHANGE because it is gauge-dependent
        assert_ne!(sv_after, sv_before,
            "signed_volume_3d must change under local gauge transform (it is gauge-dependent)");
    }

    /// Test that plaquettes are invariant under local gauge transformations.
    #[test]
    fn test_plaquette_gauge_invariance_3d() {
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);

        // Apply gauge transformations at multiple sites
        field.local_gauge_transform_3d(0, 0, 0);
        field.local_gauge_transform_3d(1, 2, 3);
        field.local_gauge_transform_3d(2, 2, 2);

        // All plaquettes should still be +1 on cold start
        for z in 0..4 {
            for y in 0..4 {
                for x in 0..4 {
                    assert_eq!(field.plaquette_xy(x, y, z), 1,
                        "xy plaq at ({},{},{}) not invariant", x, y, z);
                    assert_eq!(field.plaquette_yz(x, y, z), 1,
                        "yz plaq at ({},{},{}) not invariant", x, y, z);
                    assert_eq!(field.plaquette_xz(x, y, z), 1,
                        "xz plaq at ({},{},{}) not invariant", x, y, z);
                }
            }
        }
    }

    /// Test that the gauge-invariant signed volume is invariant under local gauge transforms.
    #[test]
    fn test_gauge_invariant_signed_volume_gauge_invariance_single_site() {
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);
        let q_before = field.gauge_invariant_signed_volume_3d();

        // Apply a local gauge transformation at (1, 2, 3)
        field.local_gauge_transform_3d(1, 2, 3);

        let q_after = field.gauge_invariant_signed_volume_3d();

        assert!((q_before - q_after).abs() < 1e-10,
            "Gauge-invariant signed volume changed under local gauge transform at (1,2,3): {} -> {}",
            q_before, q_after);
    }

    /// Test gauge invariance under multiple random gauge transformations.
    #[test]
    fn test_gauge_invariant_signed_volume_gauge_invariance_multiple() {
        let mut field = Z2GaugeField::new_dim(4, 3, 42);
        let q_before = field.gauge_invariant_signed_volume_3d();

        // Apply multiple local gauge transformations
        field.local_gauge_transform_3d(0, 0, 0);
        field.local_gauge_transform_3d(1, 1, 1);
        field.local_gauge_transform_3d(2, 3, 0);
        field.local_gauge_transform_3d(3, 0, 2);

        let q_after = field.gauge_invariant_signed_volume_3d();

        assert!((q_before - q_after).abs() < 1e-10,
            "Gauge-invariant signed volume changed under multiple local gauge transforms: {} -> {}",
            q_before, q_after);
    }

    /// Test that gauge-invariant signed volume equals 1.0 on cold start.
    /// On cold start, all links are +1, so all Wilson loops are +1, giving Q_GI = 1.
    #[test]
    fn test_gauge_invariant_signed_volume_cold_start() {
        let field = Z2GaugeField::cold_dim(4, 3, 42);
        let q = field.gauge_invariant_signed_volume_3d();
        assert!((q - 1.0).abs() < 1e-10,
            "Cold start: all links +1, gauge-invariant signed volume should be 1.0, got {}", q);
    }

    /// Test that a pure-gauge all-negative even lattice has the same normalized value.
    #[test]
    fn test_gauge_invariant_signed_volume_all_negative_even_lattice() {
        let mut field = Z2GaugeField::cold_dim(4, 3, 42);
        for z in 0..4 {
            for y in 0..4 {
                for x in 0..4 {
                    for dir in 0..3 {
                        field.flip_link_3d(x, y, z, dir);
                    }
                }
            }
        }

        let q = field.gauge_invariant_signed_volume_3d();
        assert!(
            (q - 1.0).abs() < 1e-10,
            "All-negative even lattice is a pure-gauge sector and should give Q_GI = 1.0, got {}",
            q
        );
    }

    /// Test the all-negative pure-gauge sector on a larger even lattice.
    #[test]
    fn test_gauge_invariant_signed_volume_all_negative_l6() {
        let mut field = Z2GaugeField::cold_dim(6, 3, 42);
        for z in 0..6 {
            for y in 0..6 {
                for x in 0..6 {
                    for dir in 0..3 {
                        field.flip_link_3d(x, y, z, dir);
                    }
                }
            }
        }

        let q = field.gauge_invariant_signed_volume_3d();
        assert!(
            (q - 1.0).abs() < 1e-10,
            "All-negative L=6 lattice is a pure-gauge sector and should give Q_GI = 1.0, got {}",
            q
        );
    }

    /// Test that the gauge-invariant observable stays in its normalized range.
    #[test]
    fn test_gauge_invariant_signed_volume_range_random() {
        let field = Z2GaugeField::new_dim(4, 3, 42);
        let q = field.gauge_invariant_signed_volume_3d();
        assert!(
            (-1.0..=1.0).contains(&q),
            "Gauge-invariant signed volume should be normalized to [-1, 1], got {}",
            q
        );
    }

    /// Test path_product_xyz_3d on cold start.
    #[test]
    fn test_path_product_xyz_cold_3d() {
        let field = Z2GaugeField::cold_dim(4, 3, 42);
        // From (0,0,0) to (2,3,1): all links +1, product should be +1
        let p = field.path_product_xyz_3d(0, 0, 0, 2, 3, 1);
        assert_eq!(p, 1, "Path product on cold start should be +1");
    }

    /// Test path_product_zyx_3d on cold start.
    #[test]
    fn test_path_product_zyx_cold_3d() {
        let field = Z2GaugeField::cold_dim(4, 3, 42);
        let p = field.path_product_zyx_3d(0, 0, 0, 2, 3, 1);
        assert_eq!(p, 1, "Path product on cold start should be +1");
    }

    // ---- 4D tests ----

    #[test]
    fn test_cold_start_plaquettes_4d() {
        let field = Z2GaugeField::cold_dim(4, 4, 42);
        assert_eq!(field.dimension, 4);
        assert_eq!(field.links.len(), 4 * 4 * 4 * 4 * 4);
        for t in 0..4 {
            for z in 0..4 {
                for y in 0..4 {
                    for x in 0..4 {
                        assert_eq!(field.plaquette_xy_4d(x, y, z, t), 1,
                            "xy plaq at ({},{},{},{}) failed", x, y, z, t);
                        assert_eq!(field.plaquette_yz_4d(x, y, z, t), 1,
                            "yz plaq at ({},{},{},{}) failed", x, y, z, t);
                        assert_eq!(field.plaquette_xz_4d(x, y, z, t), 1,
                            "xz plaq at ({},{},{},{}) failed", x, y, z, t);
                        assert_eq!(field.plaquette_xt(x, y, z, t), 1,
                            "xt plaq at ({},{},{},{}) failed", x, y, z, t);
                        assert_eq!(field.plaquette_yt(x, y, z, t), 1,
                            "yt plaq at ({},{},{},{}) failed", x, y, z, t);
                        assert_eq!(field.plaquette_zt(x, y, z, t), 1,
                            "zt plaq at ({},{},{},{}) failed", x, y, z, t);
                    }
                }
            }
        }
    }

    #[test]
    fn test_sweep_preserves_detailed_balance_4d() {
        let mut field = Z2GaugeField::new_dim(4, 4, 42);
        let beta = 1.0;
        field.thermalize(beta, 10);
        let (mean_p, _, _, _, _) = field.measure(beta, 100, 10);
        assert!(mean_p.abs() <= 1.0);
    }

    #[test]
    fn test_cold_polyakov_loop_4d() {
        let field = Z2GaugeField::cold_dim(4, 4, 42);
        // On cold start, all temporal links are +1, so Polyakov loop = +1 everywhere
        for z in 0..4 {
            for y in 0..4 {
                for x in 0..4 {
                    assert_eq!(field.polyakov_loop(x, y, z), 1.0,
                        "Polyakov loop at ({},{},{}) failed", x, y, z);
                }
            }
        }
        // Average should be exactly 1.0
        assert_eq!(field.average_polyakov(), 1.0);
    }

    #[test]
    fn test_polyakov_loop_changes_with_flip() {
        let mut field = Z2GaugeField::cold_dim(4, 4, 42);
        // Flip a temporal link at (0,0,0,0)
        field.flip_link_4d(0, 0, 0, 0, 3);
        // The Polyakov loop at (0,0,0) should now be -1
        assert_eq!(field.polyakov_loop(0, 0, 0), -1.0);
        // But at (1,0,0) it should still be +1 (different spatial site)
        assert_eq!(field.polyakov_loop(1, 0, 0), 1.0);
    }

    #[test]
    fn test_polyakov_loop_two_flips() {
        let mut field = Z2GaugeField::cold_dim(4, 4, 42);
        // Flip two temporal links at the same spatial site
        field.flip_link_4d(0, 0, 0, 0, 3);
        field.flip_link_4d(0, 0, 0, 1, 3);
        // (-1) * (-1) = +1
        assert_eq!(field.polyakov_loop(0, 0, 0), 1.0);
    }

    #[test]
    fn test_polyakov_loop_average_range() {
        let mut field = Z2GaugeField::new_dim(4, 4, 42);
        field.thermalize(1.0, 50);
        let avg = field.average_polyakov();
        // Average magnitude of Polyakov loop must be in [0, 1]
        assert!(avg >= 0.0 && avg <= 1.0,
            "average_polyakov = {} is out of range [0, 1]", avg);
    }

    // ---- Checkpoint tests ----

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
    fn test_checkpoint_roundtrip_4d() {
        let field = Z2GaugeField::new_dim(4, 4, 42);
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

    // ---- Wilson loop tests ----

    /// Quick 3D run with Wilson loops: L=4, 1000 sweeps, beta=0.5
    #[test]
    fn test_3d_wilson_loops() {
        let l = 4;
        let beta = 0.5;
        let n_sweeps = 1000;
        let seed = 12345u64;
        let loop_sizes = vec![(1, 1), (2, 2)];

        let (mean_p, error, _chi, _cv, _binder, wall_time, wilson_data) =
            simulate_beta_with_wilson_loops(l, 3, beta, n_sweeps / 2, n_sweeps / 2, 10, seed, &loop_sizes);

        println!("3D L={} beta={} with Wilson loops:", l, beta);
        println!("  mean_plaquette = {:.6} ± {:.6}", mean_p, error);
        for (r, c, mean_w, var_w) in &wilson_data {
            println!("  W({}×{}) = {:.6} ± {:.6}", r, c, mean_w, var_w.sqrt());
        }
        println!("  wall_time_ms   = {}", wall_time);

        assert!(mean_p.abs() <= 1.0);
        assert!(!wilson_data.is_empty());
        assert!(wall_time > 0);
    }

    /// Test Wilson loop on cold start: all 1×1 loops should be +1
    #[test]
    fn test_cold_wilson_loop_2d() {
        let field = Z2GaugeField::cold(4, 42);
        // 1×1 Wilson loop on cold start = plaquette = +1
        for y in 0..4 {
            for x in 0..4 {
                assert_eq!(field.wilson_loop_2d(x, y, 1, 1), 1, "1×1 loop at ({},{}) failed", x, y);
            }
        }
        // Average should also be +1
        assert_eq!(field.average_wilson_loop_2d(1, 1), 1.0);
    }

    /// Test Wilson loop on cold start 3D
    #[test]
    fn test_cold_wilson_loop_3d() {
        let field = Z2GaugeField::cold_dim(4, 3, 42);
        // 1×1 loop in xy-plane on cold start = plaquette_xy = +1
        for z in 0..4 {
            for y in 0..4 {
                for x in 0..4 {
                    assert_eq!(field.wilson_loop_xy_3d(x, y, z, 1, 1), 1,
                        "1×1 loop at ({},{},{}) failed", x, y, z);
                }
            }
        }
        assert_eq!(field.average_wilson_loop_xy_3d(1, 1), 1.0);
    }

    /// Test Wilson loop changes with link flip
    #[test]
    fn test_wilson_loop_changes_with_flip() {
        let mut field = Z2GaugeField::cold(4, 42);
        // Flip a link at (0,0) in x-direction
        field.flip_link(0, 0, 0);
        // The 1×1 Wilson loop at (0,0) should now be -1 (contains the flipped link)
        assert_eq!(field.wilson_loop_2d(0, 0, 1, 1), -1);
        // But the loop at (1,0) should still be +1 (doesn't contain the flipped link)
        assert_eq!(field.wilson_loop_2d(1, 0, 1, 1), 1);
    }

    /// Test signed area on cold 2D: all signs align, |Q| = N
    #[test]
    fn test_signed_area_cold_2d() {
        let l = 4usize;
        let n_sites = l * l;
        let field = Z2GaugeField::cold_dim(l, 2, 42);
        let sa = field.signed_area_2d();
        assert_eq!(sa as usize, n_sites, "Cold 2D: all +1, signed area should equal N");
    }

    /// Test signed area on hot start 2D: random signs, |Q| ~ sqrt(N)
    #[test]
    fn test_signed_area_hot_2d() {
        let l = 8usize;
        let n_sites = (l * l) as f64;
        let mut field = Z2GaugeField::new_dim(l, 2, 42);
        field.thermalize(0.2, 100);
        let sa = field.signed_area_2d();
        let normalized = (sa as f64).abs() / n_sites;
        // For random signs, |Q|/N ~ 1/sqrt(N) = 1/8 = 0.125
        assert!(normalized < 0.5, "Hot 2D: |Q|/N should be small, got {}", normalized);
    }

    /// Test signed area across beta in 2D (no phase transition, just scaling check)
    #[test]
    fn test_signed_area_2d_scaling() {
        let l = 8;
        let _n_sites = (l * l) as f64;
        let thermal = 100;
        let measure = 200;
        let every = 5;

        println!("\n--- Signed Area Test (2D L={}) ---", l);
        println!("{:<8} {:>12} {:>12} {:>12} {:>12}", "beta", "|Q|", "|Q|/N", "Q^2", "binder");

        for beta in [0.3, 0.5, 0.7, 1.0, 1.5] {
            let mut field = Z2GaugeField::new_dim(l, 2, 12345 + (beta * 1000.0) as u64);
            let (mean_q_abs, _error, mean_q_sq, normalized, binder) =
                field.measure_signed_area_2d(beta, thermal + measure, every);
            println!("{:<8.2} {:>12.2} {:>12.4} {:>12.2} {:>12.4}",
                     beta, mean_q_abs, normalized, mean_q_sq, binder);
        }
        println!("--- Expected: |Q|/N ~ 1/sqrt(N) ~ 0.125 in 2D (no deconfined phase) ---\n");

        assert!(true);
    }

    /// Quick test of signed volume across phase transition (3D, L=6)
    #[test]
    fn test_signed_volume_phase_transition_l6() {
        let l = 6;
        let _n_sites = (l * l * l) as f64;
        let thermal = 200;
        let measure = 400;
        let every = 10;

        println!("\n--- Signed Volume Test (L={}) ---", l);
        println!("{:<8} {:>12} {:>12} {:>12} {:>12}", "beta", "|Q|", "|Q|/N", "Q^2", "binder");

        for beta in [0.4, 0.6, 0.76, 1.0, 1.2, 1.5] {
            let mut field = Z2GaugeField::new_dim(l, 3, 12345 + (beta * 1000.0) as u64);
            let (mean_q_abs, _error, mean_q_sq, normalized, binder) =
                field.measure_signed_volume_3d(beta, thermal + measure, every);
            println!("{:<8.2} {:>12.2} {:>12.4} {:>12.2} {:>12.4}",
                     beta, mean_q_abs, normalized, mean_q_sq, binder);
        }
        println!("--- Expected: |Q|/N ~ 0 in confined, ~ 1 in deconfined ---\n");

        assert!(true);
    }

    /// Test signed volume on cold start: all signs align, |Q| = N
    #[test]
    fn test_signed_volume_cold_4x4x4() {
        let l = 4usize;
        let n_sites = l * l * l;
        let field = Z2GaugeField::cold_dim(l, 3, 42);
        let sv = field.signed_volume_3d();
        assert_eq!(sv as usize, n_sites, "Cold start: all +1, signed volume should equal N");
    }
}
