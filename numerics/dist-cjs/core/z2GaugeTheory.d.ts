/**
 * Z₂ Lattice Gauge Theory utilities
 *
 * Shared code for Monte Carlo simulations (T20), entanglement (T23),
 * domain walls (T24), and coupled matter (T26)
 */
export interface Z2Config {
    L: number;
    K: number;
    beta?: number;
    seed?: number;
}
export type Z2Link = -1 | 1;
/**
 * Initialize random Z₂ gauge configuration (cold or hot start)
 */
export declare function initializeZ2Lattice(config: Z2Config, start?: 'cold' | 'hot'): Map<string, Z2Link>;
/**
 * Compute plaquette product around a square face
 * Returns σ₁σ₂σ₃σ₄ for the 4 links around the face
 */
export declare function computePlaquette(links: Map<string, Z2Link>, x: number, y: number, z: number, dir1: number, dir2: number, L: number): Z2Link;
/**
 * Compute Wilson loop W(γ) = ∏ σ_e along a closed path γ
 */
export declare function computeWilsonLoop(links: Map<string, Z2Link>, path: Array<{
    x: number;
    y: number;
    z: number;
    dir: number;
}>, L: number): Z2Link;
/**
 * Compute action S = -K Σ_plaquettes P(□)
 */
export declare function computeAction(links: Map<string, Z2Link>, config: Z2Config): number;
//# sourceMappingURL=z2GaugeTheory.d.ts.map