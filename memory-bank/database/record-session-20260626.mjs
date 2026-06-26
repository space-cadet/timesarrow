import { recordSessionWork } from './lib/workflow.js';

const result = await recordSessionWork({
  task_id: 'T20',
  task_description: 'Rust checkpointing, data collation fix, and simulation dashboard deployment',
  files_modified: [
    { action: 'Modified', path: 'rust-lattice/src/main.rs', description: 'Added --checkpoint flag, mpsc streaming, atomic writes, resume support' },
    { action: 'Modified', path: 'rust-lattice/Cargo.toml', description: 'Added chrono dependency for timestamps' },
    { action: 'Modified', path: 'numerics/src/scripts/t20-sim-3d-fss-v2.py', description: 'Pass checkpoint path to Rust binary' },
    { action: 'Modified', path: 'numerics/src/scripts/collate-data.ts', description: 'Fixed ES module compatibility, updated regex for hyphen-date filenames' },
    { action: 'Modified', path: 'numerics/data/registry.json', description: 'Fixed syntax error, backfilled 22 missing June 26 runs (33 total)' },
    { action: 'Modified', path: 'numerics/output/benchmark-lattice-sizes-20250626.json', description: 'Reconstructed from corrupted file, added scaling analysis' },
    { action: 'Created', path: 'numerics/docs/dashboard.qmd', description: 'Interactive OJS dashboard for browsing simulation runs' },
    { action: 'Modified', path: 'numerics/docs/_quarto.yml', description: 'Added Dashboard to navbar and sidebar' },
    { action: 'Created', path: 'numerics/docs/data-registry.json', description: 'Registry snapshot for dashboard FileAttachment' }
  ],
  task_status: 'in_progress',
  session_period: 'morning',
  session_notes: 'Session focused on three areas: (1) Rust-level checkpointing for long-running simulations, (2) fixing broken data collation system and backfilling registry, (3) creating and deploying interactive dashboard to numerics website. Dashboard deployed to https://space-cadet.github.io/projects/timesarrow/numerics/dashboard.html but has rendering issues - needs investigation in next session.',
  output_dir: '../',
  tasks_dir: '../tasks',
  sessions_dir: '../sessions',
  edits_dir: '../edits'
});

console.log('Result:', JSON.stringify(result, null, 2));
