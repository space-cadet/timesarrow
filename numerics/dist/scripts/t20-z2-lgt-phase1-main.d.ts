/**
 * Main orchestrator for Z₂ LGT Phase 1 with worker threads and checkpointing
 *
 * Runs multiple β values in parallel across CPU cores.
 * Saves checkpoint after each β completes for resumability.
 */
import { SimulationParameters, BetaResult } from 'ts-quantum';
interface RunConfig {
    betaValues: number[];
    params: SimulationParameters;
    simulationId?: string;
    verbose?: boolean;
}
declare function runParallelSweeps(config: RunConfig): Promise<BetaResult[]>;
export { runParallelSweeps };
export type { RunConfig };
//# sourceMappingURL=t20-z2-lgt-phase1-main.d.ts.map