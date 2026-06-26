const fs = require('fs');
const path = require('path');
const { openDb, closeDb } = require('./lib/sqlite.js');

async function parseTaskFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const basename = path.basename(filePath, '.md');
  
  // Extract title - try multiple patterns
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
  const statusMatch = content.match(/\*\*Status:\*\*\s*(.+)/);
  if (statusMatch) {
    const s = statusMatch[1].trim().toLowerCase();
    if (s.includes('completed') || s.includes('✅')) status = 'completed';
    else if (s.includes('active') || s.includes('🔄')) status = 'active';
    else if (s.includes('paused')) status = 'paused';
    else status = 'unknown';
  }
  
  // Extract priority
  let priority = 'medium';
  const priorityMatch = content.match(/\*\*Priority:\*\*\s*(.+)/);
  if (priorityMatch) {
    priority = priorityMatch[1].trim().toUpperCase();
  }
  
  // Extract dates
  let created = null, started = null, completed = null;
  const createdMatch = content.match(/\*\*Created:\*\*\s*(.+)/);
  if (createdMatch) created = createdMatch[1].trim();
  
  const startedMatch = content.match(/\*\*Started:\*\*\s*(.+)/);
  if (startedMatch) started = startedMatch[1].trim();
  
  const completedMatch = content.match(/\*\*Completed:\*\*\s*(.+)/);
  if (completedMatch) {
    const c = completedMatch[1].trim();
    if (c !== '—' && c !== '-') completed = c;
  }
  
  // Extract description
  let description = '';
  const descMatch = content.match(/## Description\n+([\s\S]+?)(?=\n## |\n---|$)/);
  if (descMatch) description = descMatch[1].trim().substring(0, 200);
  
  return {
    id: basename,
    title: title.length > 200 ? title.substring(0, 200) : title,
    status,
    priority,
    created,
    started,
    completed,
    description
  };
}

async function main() {
  const archiveDir = path.resolve(__dirname, '../archive/old-tasks');
  const files = fs.readdirSync(archiveDir).filter(f => f.match(/^T\d+/));
  
  await openDb('./memory_bank.db');
  const db = require('./lib/sqlite.js').db;
  
  for (const file of files.sort()) {
    const task = await parseTaskFile(path.join(archiveDir, file));
    
    // Check if already exists
    const existing = db.prepare('SELECT id FROM task_items WHERE id = ?').get(task.id);
    if (existing) {
      console.log(`SKIP: ${task.id} already in DB`);
      continue;
    }
    
    // Normalize dates
    const started = task.started || task.created || null;
    const completed = task.completed || null;
    
    try {
      db.prepare(`
        INSERT INTO task_items (id, title, status, priority, started, completed, details)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `).run(task.id, task.title, task.status, task.priority, started, completed, task.description);
      console.log(`IMPORTED: ${task.id} - ${task.title} (${task.status})`);
    } catch (e) {
      console.error(`ERROR importing ${task.id}:`, e.message);
    }
  }
  
  await closeDb();
  console.log('\nDone. Regenerate markdown files to see changes.');
}

main().catch(e => console.error(e));
