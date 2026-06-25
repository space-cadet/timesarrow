// collate-data.ts - Automated data collation script for TimesArrow numerics
// Scans output/ directory, extracts metadata, updates registry.json

import { readdirSync, readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

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

function discoverRuns(): SimulationRun[] {
  const files = readdirSync(OUTPUT_DIR).filter(f => f.endsWith('.json'));
  const newRuns: SimulationRun[] = [];

  for (const file of files) {
    const path = join(OUTPUT_DIR, file);
    const data = JSON.parse(readFileSync(path, 'utf-8'));
    
    // Skip already-registered runs (check by filename match)
    // In production, use runId matching
    
    // Extract metadata from filename convention:
    // t20-p2-L16-20250625.json → task=T20, phase=phase2, L=16
    const match = file.match(/^(t\d+)-(p\d+)-L(\d+)-(.+)\.json$/);
    if (match) {
      const [, taskCode, phaseCode, latticeSize, dateStr] = match;
      const task = taskCode.toUpperCase();
      const phase = phaseCode.replace('p', 'phase');
      
      newRuns.push({
        runId: `${taskCode}-${phaseCode}-L${latticeSize}-${dateStr}`,
        task,
        phase,
        status: 'complete',
        timestamp: new Date().toISOString(),
        description: `Auto-discovered run from ${file}`,
        parameters: {
          latticeSize: parseInt(latticeSize),
          ...data.parameters
        },
        results: data.results || {},
        outputFiles: [path]
      });
    }
  }

  return newRuns;
}

function generateSummaryTable(runs: SimulationRun[]): string {
  // Generate Markdown table for Quarto pages
  const headers = ['Run ID', 'Lattice', 'β Range', 'Status', 'Key Finding'];
  const rows = runs.map(r => [
    r.runId,
    `${r.parameters.latticeSize}×${r.parameters.latticeSize}`,
    `${Math.min(...(r.parameters.betaValues || []))}–${Math.max(...(r.parameters.betaValues || []))}`,
    r.status,
    r.results.keyFinding || '—'
  ]);

  let md = '| ' + headers.join(' | ') + ' |\n';
  md += '|' + headers.map(() => '---').join('|') + '|\n';
  for (const row of rows) {
    md += '| ' + row.join(' | ') + ' |\n';
  }
  return md;
}

// Main execution
if (require.main === module) {
  console.log('🔍 Scanning for new simulation data...');
  
  const registry = loadRegistry();
  const newRuns = discoverRuns();
  
  if (newRuns.length === 0) {
    console.log('ℹ️ No new runs discovered');
  } else {
    console.log(`📊 Discovered ${newRuns.length} new run(s)`);
    registry.runs.push(...newRuns);
    
    // Update task phase references
    for (const run of newRuns) {
      const task = registry.tasks[run.task];
      if (task && task.phases[run.phase]) {
        task.phases[run.phase].runs.push(run.runId);
      }
    }
    
    saveRegistry(registry);
    
    // Print summary
    console.log('\n📋 Simulation Summary:');
    console.log(generateSummaryTable(registry.runs));
  }
}
