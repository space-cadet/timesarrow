/**
 * Z₂ Lattice Gauge Theory utilities
 *
 * Shared code for Monte Carlo simulations (T20), entanglement (T23),
 * domain walls (T24), and coupled matter (T26)
 */
/**
 * Initialize random Z₂ gauge configuration (cold or hot start)
 */
export function initializeZ2Lattice(config, start = 'hot') {
    const links = new Map();
    // Key format: "x,y,z,dir" where dir ∈ {0,1,2} for x,y,z directions
    for (let x = 0; x < config.L; x++) {
        for (let y = 0; y < config.L; y++) {
            for (let z = 0; z < config.L; z++) {
                for (let dir = 0; dir < 3; dir++) {
                    const key = `${x},${y},${z},${dir}`;
                    const value = start === 'cold' ? 1 : (Math.random() > 0.5 ? 1 : -1);
                    links.set(key, value);
                }
            }
        }
    }
    return links;
}
/**
 * Compute plaquette product around a square face
 * Returns σ₁σ₂σ₃σ₄ for the 4 links around the face
 */
export function computePlaquette(links, x, y, z, dir1, dir2, L) {
    // Get the 4 links around the plaquette
    const link1 = getLink(links, x, y, z, dir1, L);
    const link2 = getLink(links, (x + (dir1 === 0 ? 1 : 0)) % L, (y + (dir1 === 1 ? 1 : 0)) % L, (z + (dir1 === 2 ? 1 : 0)) % L, dir2, L);
    const link3 = getLink(links, (x + (dir2 === 0 ? 1 : 0)) % L, (y + (dir2 === 1 ? 1 : 0)) % L, (z + (dir2 === 2 ? 1 : 0)) % L, dir1, L);
    const link4 = getLink(links, x, y, z, dir2, L);
    return (link1 * link2 * link3 * link4);
}
function getLink(links, x, y, z, dir, L) {
    const key = `${x % L},${y % L},${z % L},${dir}`;
    return links.get(key) ?? 1;
}
/**
 * Compute Wilson loop W(γ) = ∏ σ_e along a closed path γ
 */
export function computeWilsonLoop(links, path, L) {
    let product = 1;
    for (const { x, y, z, dir } of path) {
        product = (product * getLink(links, x, y, z, dir, L));
    }
    return product;
}
/**
 * Compute action S = -K Σ_plaquettes P(□)
 */
export function computeAction(links, config) {
    let S = 0;
    const { L, K } = config;
    // Sum over all plaquettes
    for (let x = 0; x < L; x++) {
        for (let y = 0; y < L; y++) {
            for (let z = 0; z < L; z++) {
                // XY plaquettes
                S += computePlaquette(links, x, y, z, 0, 1, L);
                // XZ plaquettes
                S += computePlaquette(links, x, y, z, 0, 2, L);
                // YZ plaquettes
                S += computePlaquette(links, x, y, z, 1, 2, L);
            }
        }
    }
    return -K * S;
}
//# sourceMappingURL=z2GaugeTheory.js.map