/**
 * Main orchestrator for Z₂ LGT Phase 1 with worker threads and checkpointing
 *
 * Runs multiple β values in parallel across CPU cores.
 * Saves checkpoint after each β completes for resumability.
 */
import { Worker } from 'worker_threads';
import * as os from 'os';
import * as path from 'path';
import { saveCheckpoint, loadCheckpoint, getRemainingBetas, createSimulationId } from 'ts-quantum';
const NUM_WORKERS = os.cpus().length;
const WORKER_SCRIPT = path.join(__dirname, 't20-z2-lgt-phase1-worker.js');
async function runParallelSweeps(config) {
    const { betaValues, params, simulationId: customId, verbose = true } = config;
    const simulationId = customId || createSimulationId('t20-phase1', params);
    // Check for existing checkpoint
    const checkpoint = loadCheckpoint(simulationId);
    const remainingBetas = getRemainingBetas(betaValues, checkpoint);
    const results = checkpoint?.results ? [...checkpoint.results] : [];
    const completed = checkpoint?.completed ? [...checkpoint.completed] : [];
    if (remainingBetas.length === 0) {
        if (verbose)
            console.log(`All ${betaValues.length} β values already completed!`);
        return results;
    }
    if (verbose) {
        console.log(`Simulation: ${simulationId}`);
        console.log(`Parameters: L=${params.L}, thermal=${params.thermalSweeps}, measure=${params.measureSweeps}`);
        console.log(`Workers: ${NUM_WORKERS}`);
        console.log(`Total β values: ${betaValues.length}`);
        console.log(`Already completed: ${completed.length}`);
        console.log(`Remaining: ${remainingBetas.length}`);
        console.log('');
    }
    return new Promise((resolve, reject) => {
        const workers = [];
        const queue = [...remainingBetas];
        let activeWorkers = 0;
        let totalDone = completed.length;
        const startTime = Date.now();
        function assignWork(worker) {
            if (queue.length === 0)
                return false;
            const beta = queue.shift();
            if (verbose)
                console.log(`[${new Date().toISOString()}] Starting β = ${beta} (${totalDone + 1}/${betaValues.length})`);
            worker.postMessage({ ...params, beta });
            return true;
        }
        function onResult(result) {
            results.push(result);
            completed.push(result.beta);
            totalDone++;
            if (verbose) {
                const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
                console.log(`[${elapsed}s] β = ${result.beta}: ⟨P⟩ = ${result.meanPlaquette.toFixed(4)} ± ${result.errorPlaquette.toFixed(4)} (${result.wallTimeMs}ms)`);
            }
            // Save checkpoint after each β
            const manifest = {
                simulationId,
                parameters: params,
                completed,
                results,
                timestamp: new Date().toISOString(),
                version: '1.0'
            };
            saveCheckpoint(manifest);
        }
        function onError(beta, error) {
            console.error(`Error for β = ${beta}: ${error}`);
            // Put beta back in queue for retry
            queue.push(beta);
        }
        // Create worker pool
        for (let i = 0; i < Math.min(NUM_WORKERS, remainingBetas.length); i++) {
            const worker = new Worker(WORKER_SCRIPT);
            workers.push(worker);
            worker.on('message', (msg) => {
                if (msg.type === 'result') {
                    onResult(msg.data);
                    // Assign next work or shut down
                    if (!assignWork(worker)) {
                        activeWorkers--;
                        if (activeWorkers === 0 && queue.length === 0) {
                            // All done
                            workers.forEach(w => w.terminate());
                            const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
                            if (verbose)
                                console.log(`\nAll simulations complete in ${totalTime}s`);
                            resolve(results);
                        }
                    }
                }
                else if (msg.type === 'error') {
                    onError(msg.beta, msg.error);
                    if (!assignWork(worker)) {
                        activeWorkers--;
                        if (activeWorkers === 0 && queue.length === 0) {
                            workers.forEach(w => w.terminate());
                            resolve(results);
                        }
                    }
                }
            });
            worker.on('error', (err) => {
                console.error('Worker error:', err);
                activeWorkers--;
                if (activeWorkers === 0 && queue.length === 0) {
                    workers.forEach(w => w.terminate());
                    resolve(results);
                }
            });
            // Initial assignment
            if (assignWork(worker)) {
                activeWorkers++;
            }
        }
    });
}
// CLI entry point
if (require.main === module) {
    const L = parseInt(process.argv[2]) || 8;
    const measureSweeps = parseInt(process.argv[3]) || 5000;
    const thermalSweeps = parseInt(process.argv[4]) || 1000;
    const betaValues = [0.1, 0.2, 0.3, 0.4, 0.44, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0];
    const params = {
        L,
        thermalSweeps,
        measureSweeps,
        measureEvery: 10,
        binSize: 100
    };
    console.log('═══════════════════════════════════════════');
    console.log('  Z₂ LGT Phase 1 — Worker Thread Version');
    console.log('═══════════════════════════════════════════\n');
    runParallelSweeps({ betaValues, params })
        .then(results => {
        console.log('\n═══════════════════════════════════════════');
        console.log('  Final Results');
        console.log('═══════════════════════════════════════════');
        console.log('');
        console.log('| β | ⟨P⟩ | Error |');
        console.log('|---|-----|-------|');
        results.forEach(r => {
            console.log(`| ${r.beta.toFixed(2)} | ${r.meanPlaquette.toFixed(4)} | ±${r.errorPlaquette.toFixed(4)} |`);
        });
        // Save final results
        const fs = require('fs');
        const outputDir = './output';
        if (!fs.existsSync(outputDir))
            fs.mkdirSync(outputDir, { recursive: true });
        const outputFile = `${outputDir}/t20-phase1-worker-L${L}.json`;
        fs.writeFileSync(outputFile, JSON.stringify({ parameters: params, results }, null, 2));
        console.log(`\nResults saved to: ${outputFile}`);
    })
        .catch(err => {
        console.error('Fatal error:', err);
        process.exit(1);
    });
}
export { runParallelSweeps };
//# sourceMappingURL=t20-z2-lgt-phase1-main.js.map