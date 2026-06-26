import Database from 'better-sqlite3';
import fs from 'fs';
import path from 'path';

const db = new Database('./memory_bank.db');

function parseTaskFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const basename = path.basename(filePath, '.md');
  
  // Extract title
  let title = basename;
  const titleMatch = content.match(/\*\*Title:\*\*\s*(.+)/);
  if (titleMatch) {
    title = titleMatch[1].trim();
  } else {
    const h1Match = content.match(/^#\s+(.+)/m);
    if (h1Match) title = h1Match[1].replace(/^Task:\s*/, '').trim();
  }
  
  // Extract status
  let status = 'unknown';
  const statusMatch = content.match(/\*\*Status:\*\*\s*(.+)/i);
  if (statusMatch) {
    const s = statusMatch[1].trim().toLowerCase();
    if (s.includes('completed') || s.includes('✅')) status = 'completed';
    else if (s.includes('active') || s.includes('🔄')) status = 'in_progress';
    else if (s.includes('paused')) status = 'paused';
    else status = 'unknown';
  }
  
  // Extract priority
  let priority = 'MEDIUM';
  const priorityMatch = content.match(/\*\*Priority:\*\*\s*(.+)/i);
  if (priorityMatch) {
    priority = priorityMatch[1].trim().toUpperCase();
  }
  
  // Extract dates
  let started = null;
  const startedMatch = content.match(/\*\*Started:\*\*\s*(.+)/);
  if (startedMatch) started = startedMatch[1].trim();
  
  // Extract description
  let description = '';
  const descMatch = content.match(/## Description\n+([\s\S]+?)(?=\n## |\n---|$)/);
  if (descMatch) description = descMatch[1].trim().substring(0, 200);
  
  return {
    id: basename,
    title: title.length > 200 ? title.substring(0, 200) : title,
    status,
    priority,
    started: started || new Date().toISOString().split('T')[0],
    description
  };
}

const archiveDir = path.resolve(process.cwd(), '../archive/old-tasks');
const files = fs.readdirSync(archiveDir).filter(f => f.match(/^T\d+.*\.md$/));

const insert = db.prepare(`
  INSERT OR REPLACE INTO task_items (id, title, status, priority, started, details)
  VALUES (?, ?, ?, ?, ?, ?)
`);

for (const file of files.sort()) {
  const task = parseTaskFile(path.join(archiveDir, file));
  
  insert.run(
    task.id,
    task.title,
    task.status,
    task.priority,
    task.started,
    task.description
  );
  console.log(`IMPORTED: ${task.id} - ${task.title} (${task.status})`);
}

db.close();
console.log('\nDone. All old tasks imported into DB.');
