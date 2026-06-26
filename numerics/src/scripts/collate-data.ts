// collate-data.ts - Automated data collation script for TimesArrow numerics
// Scans output/ directory, extracts metadata, updates registry.json

import { readdirSync, readFileSync, writeFileSync, existsSync } from 'fs';
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
  // Try pattern: t20-p3-L8-3D-wilson-fine-20250626.json (hyphen before date)
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

function discoverRuns(outputDir: string = OUTPUT_DIR): SimulationRun[] {
  if (!existsSync(outputDir)) {
    console.log(`⚠️ Output directory not found: ${outputDir}`);
    return [];
  }

  const files = readdirSync(outputDir).filter(f => f.endsWith('.json'));
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

    newRuns.push({
      runId: meta.runId!,
      task: meta.task!,
      phase: meta.phase!,
      status: 'complete',
      timestamp: new Date().toISOString(),
      description: meta.description!,
      parameters: {
        latticeSize: parseInt(meta.runId!.match(/L(\d+)/)?.[1] || '0'),
        ...params,
      },
      results: results,
      outputFiles: [path],
      page: `tasks/${meta.task!.toLowerCase()}-z2-lgt.qmd`,
    });
  }

  return newRuns;
}

function generateSummaryTable(runs: SimulationRun[]): string {
  const headers = ['Run ID', 'Task', 'Phase', 'Lattice', 'Status', 'Key Finding'];
  const rows = runs.map(r => [
    r.runId,
    r.task,
    r.phase,
    r.parameters.latticeSize ? `${r.parameters.latticeSize}×${r.parameters.latticeSize}` : '—',
    r.status,
    r.results.keyFinding || r.results.criticalBetaEstimate || '—',
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

  // Filter out already-registered runs
  const newRuns = allDiscovered.filter(r => !registeredIds.has(r.runId));

  if (newRuns.length === 0) {
    console.log('ℹ️ No new runs discovered');
  } else {
    console.log(`📊 Discovered ${newRuns.length} new run(s)`);
    registry.runs.push(...newRuns);

    // Update task phase references
    for (const run of newRuns) {
      const task = registry.tasks[run.task];
      if (task && task.phases[run.phase]) {
        if (!task.phases[run.phase].runs.includes(run.runId)) {
          task.phases[run.phase].runs.push(run.runId);
        }
      }
    }

    saveRegistry(registry);

    // Print summary
    console.log('\n📋 New Runs:');
    console.log(generateSummaryTable(newRuns));
  }

  console.log(`\n📊 Total runs in registry: ${registry.runs.length}`);
}
