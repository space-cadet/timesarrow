// collate-data.ts - Automated data collation script for TimesArrow numerics
// Scans output/ and data/fss/ directories, extracts metadata + timing, updates registry.json

import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from 'fs';
import { join, basename } from 'path';
import { fileURLToPath } from 'url';

interface SimulationRun {
  runId: string;
  task: string;
  phase: string;
  status: string;
  timestamp: string;
  description: string;
  parameters: Record<string, any>;
  results: Record<string, any>;
  outputFiles: string[];
  page?: string;
  // v2 enhanced fields
  dataUrl?: string;
  wallTimeMs?: number;
  cpuTimeMs?: number;
  startTime?: string;
  endTime?: string;
  betasCompleted?: number;
  totalBetas?: number;
  sweepsPerSecond?: number;
  figures?: string[];
}

interface Registry {
  schemaVersion: string;
  project: string;
  description: string;
  lastUpdated: string;
  runs: SimulationRun[];
  tasks: Record<string, any>;
}

const OUTPUT_DIR = './output';
const FSS_DIR = './data/fss';
const FIGURES_DIR = './figures';
const REGISTRY_FILE = './data/registry.json';

function loadRegistry(): Registry {
  if (!existsSync(REGISTRY_FILE)) {
    throw new Error(`Registry file not found: ${REGISTRY_FILE}`);
  }
  return JSON.parse(readFileSync(REGISTRY_FILE, 'utf-8'));
}

function saveRegistry(registry: Registry): void {
  registry.lastUpdated = new Date().toISOString();
  writeFileSync(REGISTRY_FILE, JSON.stringify(registry, null, 2));
  console.log(`✅ Registry updated: ${registry.lastUpdated}`);
}

function extractMetadataFromFile(file: string, data: any): Partial<SimulationRun> | null {
  // Try pattern: t20-p3-L8-3D-wilson-fine-20250626.json
  let match = file.match(/^(t\d+)-(p\d+)-L(\d+)-(.+)-(\d{8})\.json$/);
  if (!match) {
    // Try pattern with dot before date: t20-p2-L16.20250625.json
    match = file.match(/^(t\d+)-(p\d+)-L(\d+)\.(\d{8})\.json$/);
  }
  if (match) {
    const [, taskCode, phaseCode, latticeSize, suffix, dateStr] = match;
    const task = taskCode.toUpperCase();
    const phase = phaseCode.replace('p', 'phase');
    const suffixStr = suffix || 'run';
    return {
      runId: `${taskCode}-${phaseCode}-L${latticeSize}-${suffixStr}-${dateStr}`,
      task,
      phase,
      description: `${suffixStr.replace(/-/g, ' ')}, L=${latticeSize}`,
    };
  }

  // Try pattern without L prefix: t20-p3-L4-3D-20250625.json
  match = file.match(/^(t\d+)-(p\d+)-L(\d+)-(\d{8})\.json$/);
  if (match) {
    const [, taskCode, phaseCode, latticeSize, dateStr] = match;
    const task = taskCode.toUpperCase();
    const phase = phaseCode.replace('p', 'phase');
    return {
      runId: `${taskCode}-${phaseCode}-L${latticeSize}-${dateStr}`,
      task,
      phase,
      description: `Auto-discovered run from ${file}`,
    };
  }

  // Try pattern: t20-phase1-fast.json (no date)
  match = file.match(/^(t\d+)-phase(\d+)-(.+)\.json$/);
  if (match) {
    const [, taskCode, phaseNum, suffix] = match;
    const task = taskCode.toUpperCase();
    const phase = `phase${phaseNum}`;
    return {
      runId: `${taskCode}-${phase}-${suffix}`,
      task,
      phase,
      description: `Auto-discovered run from ${file}`,
    };
  }

  // Try pattern: benchmark-lattice-sizes-20250626.json
  match = file.match(/^(benchmark-.+)-(\d{8})\.json$/);
  if (match) {
    const [, suffix, dateStr] = match;
    return {
      runId: `benchmark-${suffix}-${dateStr}`,
      task: 'BENCHMARK',
      phase: 'benchmark',
      description: `Benchmark run from ${file}`,
    };
  }

  // Try pattern: t25-volume-operator-spectrum.json
  match = file.match(/^(t\d+)-(.+)\.json$/);
  if (match) {
    const [, taskCode, suffix] = match;
    return {
      runId: `${taskCode}-${suffix}`,
      task: taskCode.toUpperCase(),
      phase: 'unknown',
      description: `Auto-discovered run from ${file}`,
    };
  }

  return null;
}

function extractTiming(data: any, filePath: string): Partial<SimulationRun> {
  const timing: Partial<SimulationRun> = {};

  // Extract wall time from Rust output
  if (data.totalWallTimeMs) {
    timing.wallTimeMs = data.totalWallTimeMs;
  }

  // Extract from individual beta results
  if (Array.isArray(data.results) && data.results.length > 0) {
    const wallTimes = data.results
      .map((r: any) => r.wallTimeMs)
      .filter((t: number | undefined) => typeof t === 'number');
    
    if (wallTimes.length > 0 && !timing.wallTimeMs) {
      timing.wallTimeMs = wallTimes.reduce((a: number, b: number) => a + b, 0);
    }

    timing.betasCompleted = data.results.length;
  }

  // Count total betas from parameters
  if (data.parameters?.betaValues) {
    timing.totalBetas = data.parameters.betaValues.length;
  }

  // Calculate sweeps per second
  const measureSweeps = data.parameters?.measureSweeps || data.parameters?.measurementSweeps;
  if (measureSweeps && timing.wallTimeMs && timing.wallTimeMs > 0) {
    // If we have multiple betas, total sweeps = measureSweeps * betasCompleted
    const totalSweeps = measureSweeps * (timing.betasCompleted || 1);
    timing.sweepsPerSecond = (totalSweeps * 1000) / timing.wallTimeMs;
  }

  // Extract start/end from file modification times
  try {
    const stats = statSync(filePath);
    timing.endTime = stats.mtime.toISOString();
    // Approximate start time: end time - wall time
    if (timing.wallTimeMs) {
      const startMs = stats.mtime.getTime() - timing.wallTimeMs;
      timing.startTime = new Date(startMs).toISOString();
    }
  } catch (e) {
    // File stat failed, skip timing
  }

  return timing;
}

function discoverFigures(runId: string): string[] {
  if (!existsSync(FIGURES_DIR)) {
    return [];
  }

  const files = readdirSync(FIGURES_DIR);
  const prefix = runId.split('-').slice(0, 3).join('-'); // e.g., "t20-p3-L8"
  
  return files
    .filter(f => f.startsWith(prefix) && (f.endsWith('.png') || f.endsWith('.svg')))
    .map(f => `figures/${f}`);
}

function discoverRuns(outputDir: string = OUTPUT_DIR): SimulationRun[] {
  if (!existsSync(outputDir)) {
    console.log(`⚠️ Output directory not found: ${outputDir}`);
    return [];
  }

  const files = readdirSync(outputDir)
    .filter(f => f.endsWith('.json'))
    .filter(f => !f.startsWith('.') && !f.includes('checkpoint')); // Skip checkpoints and dotfiles
  const newRuns: SimulationRun[] = [];

  for (const file of files) {
    const path = join(outputDir, file);
    let data: any;
    try {
      data = JSON.parse(readFileSync(path, 'utf-8'));
    } catch (e) {
      console.log(`⚠️ Skipping unreadable file: ${file}`);
      continue;
    }

    const meta = extractMetadataFromFile(file, data);
    if (!meta) {
      console.log(`⚠️ Unrecognized filename pattern: ${file}`);
      continue;
    }

    // Extract parameters from data if available
    const params = data.parameters || {};
    const results = data.results || {};
    
    // Extract timing data
    const timing = extractTiming(data, path);
    
    // Flag test runs (short sweeps)
    const measureSweeps = params.measureSweeps || params.measurementSweeps;
    const isTestRun = measureSweeps && measureSweeps < 500000;

    // Discover associated figures
    const figures = discoverFigures(meta.runId!);

    newRuns.push({
      runId: meta.runId!,
      task: meta.task!,
      phase: meta.phase!,
      status: 'complete',
      timestamp: new Date().toISOString(),
      description: isTestRun ? `[TEST] ${meta.description!}` : meta.description!,
      parameters: {
        latticeSize: parseInt(meta.runId!.match(/L(\d+)/)?.[1] || '0'),
        ...params,
      },
      results: results,
      outputFiles: [path],
      page: `tasks/${meta.task!.toLowerCase()}-z2-lgt.qmd`,
      dataUrl: path,
      ...timing,
      figures: figures.length > 0 ? figures : undefined,
    });
  }

  return newRuns;
}

function generateSummaryTable(runs: SimulationRun[]): string {
  const headers = ['Run ID', 'Task', 'Phase', 'Lattice', 'Status', 'Wall Time', 'βs', 'Perf (sw/s)'];
  const rows = runs.map(r => [
    r.runId,
    r.task,
    r.phase,
    r.parameters.latticeSize ? `${r.parameters.latticeSize}×${r.parameters.latticeSize}` : '—',
    r.status,
    r.wallTimeMs ? `${(r.wallTimeMs / 1000).toFixed(1)}s` : '—',
    r.betasCompleted ? `${r.betasCompleted}/${r.totalBetas || '?'}` : '—',
    r.sweepsPerSecond ? r.sweepsPerSecond.toFixed(0) : '—',
  ]);

  let md = '| ' + headers.join(' | ') + ' |\n';
  md += '|' + headers.map(() => '---').join('|') + '|\n';
  for (const row of rows) {
    md += '| ' + row.join(' | ') + ' |\n';
  }
  return md;
}

// Main execution
const __filename = fileURLToPath(import.meta.url);

if (process.argv[1] === __filename) {
  console.log('🔍 Scanning for new simulation data...');

  const registry = loadRegistry();
  const registeredIds = new Set(registry.runs.map(r => r.runId));

  // Scan both output/ and data/fss/
  const outputRuns = discoverRuns(OUTPUT_DIR);
  const fssRuns = discoverRuns(FSS_DIR);
  const allDiscovered = [...outputRuns, ...fssRuns];

  // Filter out already-registered runs (by runId)
  const newRuns = allDiscovered.filter(r => !registeredIds.has(r.runId));

  // For existing runs, update timing data if missing
  let updatedCount = 0;
  for (const existingRun of registry.runs) {
    const discovered = allDiscovered.find(r => r.runId === existingRun.runId);
    if (discovered) {
      // Update timing fields if they were missing
      if (!existingRun.wallTimeMs && discovered.wallTimeMs) {
        existingRun.wallTimeMs = discovered.wallTimeMs;
        existingRun.sweepsPerSecond = discovered.sweepsPerSecond;
        existingRun.betasCompleted = discovered.betasCompleted;
        existingRun.totalBetas = discovered.totalBetas;
        existingRun.startTime = discovered.startTime;
        existingRun.endTime = discovered.endTime;
        existingRun.dataUrl = discovered.dataUrl;
        updatedCount++;
      }
      // Update figures if missing
      if ((!existingRun.figures || existingRun.figures.length === 0) && discovered.figures && discovered.figures.length > 0) {
        existingRun.figures = discovered.figures;
        if (!updatedCount) updatedCount++;
      }
    }
  }

  if (newRuns.length === 0 && updatedCount === 0) {
    console.log('ℹ️ No new runs discovered, no timing updates needed');
  } else {
    if (newRuns.length > 0) {
      console.log(`📊 Discovered ${newRuns.length} new run(s)`);
      registry.runs.push(...newRuns);
    }
    if (updatedCount > 0) {
      console.log(`🔄 Updated timing data for ${updatedCount} existing run(s)`);
    }

    // Update task phase references
    for (const run of [...newRuns]) {
      const task = registry.tasks[run.task];
      if (task && task.phases[run.phase]) {
        if (!task.phases[run.phase].runs.includes(run.runId)) {
          task.phases[run.phase].runs.push(run.runId);
        }
      }
    }

    saveRegistry(registry);

    // Print summary
    if (newRuns.length > 0) {
      console.log('\n📋 New Runs:');
      console.log(generateSummaryTable(newRuns));
    }
  }

  console.log(`\n📊 Total runs in registry: ${registry.runs.length}`);
  
  // Print performance summary
  const runsWithTiming = registry.runs.filter(r => r.wallTimeMs);
  if (runsWithTiming.length > 0) {
    console.log(`\n⚡ Runs with timing data: ${runsWithTiming.length}`);
    const totalWallTime = runsWithTiming.reduce((sum, r) => sum + (r.wallTimeMs || 0), 0);
    console.log(`⏱️ Total wall time: ${(totalWallTime / 1000 / 60).toFixed(1)} minutes`);
    const avgPerf = runsWithTiming
      .filter(r => r.sweepsPerSecond)
      .reduce((sum, r, _, arr) => sum + (r.sweepsPerSecond || 0) / arr.length, 0);
    if (avgPerf > 0) {
      console.log(`🚀 Average performance: ${avgPerf.toFixed(0)} sweeps/sec`);
    }
  }
}
