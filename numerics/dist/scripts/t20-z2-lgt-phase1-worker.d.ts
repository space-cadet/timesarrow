/**
 * Worker thread entry point for Z₂ LGT simulation
 *
 * Receives a single β value and runs the full thermalization + measurement.
 * Posts result back to main thread when done.
 */
interface WorkerInput {
    beta: number;
    L: number;
    thermalSweeps: number;
    measureSweeps: number;
    measureEvery: number;
    binSize: number;
    seed?: number;
}
declare function runSimulation(params: WorkerInput): {
    beta: number;
    meanPlaquette: number;
    errorPlaquette: number;
    numMeasurements: number;
    wallTimeMs: number;
};
export { runSimulation };
export type { WorkerInput };
//# sourceMappingURL=t20-z2-lgt-phase1-worker.d.ts.map