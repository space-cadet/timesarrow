# Memory-Bank Database Schema Fix

*Date: 2026-06-26*
*Related: T20/T20d infrastructure*

## Problem

The timesarrow memory-bank database had a schema mismatch. The `schema.sql` file was from mb-core v1.1, but the actual database was created with v1.0-era column names. This broke the `mb-cli` DB workflow commands (`mb task list`, `mb workflow --regenerate`, etc.).

## Root Cause

The `sessions` table in the database had these column names:
```sql
session_date, session_period, focus_task
```

But `mb-cli` v1.1 expected:
```sql
date, period, focus
```

This caused all `mb-cli` queries to fail with "column not found" errors.

## Diagnosis Steps

1. `mb db init --db memory_bank.db` failed to create correct schema
2. Manual inspection with sql.js revealed column name mismatch
3. Found `parse-sessions.js` and `parse-edits.js` also used old column names

## Fix Applied (Option A — Recreate from Text)

Since text files are the canonical source of truth and were intact:

### Step 1: Backup
```bash
cp memory_bank.db memory_bank.db.backup.pre-migration.20260626_235231
```

### Step 2: Reinitialize Schema
```bash
rm memory_bank.db
mb db init --db memory_bank.db
```

### Step 3: Fix Parse Scripts
Updated column names in:
- `parse-sessions.js`: `session_date` → `date`, `session_period` → `period`, `focus_task` → `focus`
- `parse-edits.js`: Fixed regex from `^###` to `^##` to match actual edit chunk headers

### Step 4: Repopulate Database
```bash
node parse-tasks.js      # 13 tasks imported
node parse-sessions.js    # 18 sessions imported
node parse-edits.js       # 31 edit entries imported
```

### Step 5: Verify
```bash
mb task list              # ✅ All tasks visible
mb session list           # ✅ All sessions visible
mb workflow --regenerate  # ✅ edit_history.md rebuilt correctly
```

## Commits

| Commit | Message |
|--------|---------|
| `59e405e` | docs: Add schema fix plan and update session cache |
| `02bb3a7` | fix: Update DB schema to v1.1 and fix parse scripts |
| `f24711c` | chore: Remove build artifacts and DB backups from tracking |

## Files Modified

- `memory-bank/database/parse-sessions.js` — Updated column names
- `memory-bank/database/parse-edits.js` — Fixed header regex
- `memory-bank/database/schema.sql` — Replaced with correct v1.1 schema
- `memory-bank/database/memory_bank.db` — Recreated from text

## Lessons Learned

1. **Text files are source of truth.** When DB is broken, always regenerate from text, not the other way around.
2. **Column name consistency matters.** A mismatch between `schema.sql` and `mb-cli` code silently breaks everything.
3. **Parse scripts must match text format.** The `parse-edits.js` regex mismatch shows even small discrepancies cause total failures.
4. **Don't commit build artifacts.** The `target/release/` directory should have been `.gitignore`d from the start.

## References

- Edit chunk: `memory-bank/edits/2026-06-26/235000-T20-schema-fix-plan.md`
- Plan created as prerequisite per user request before executing Option A
