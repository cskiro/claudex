# Troubleshooting Guide

## No conversations found

**Symptoms**: Skill reports 0 conversations

**Solution**:
1. Verify you're in a project with conversation history
2. Check `~/.claude/projects/` for your project folder
3. Ensure JSONL files exist in the project folder
4. Run initial processing if first time

---

## Search returns no results

**Symptoms**: Semantic search finds nothing

**Solution**:
1. Check embeddings were built (look for ChromaDB folder)
2. Rebuild embeddings: skill will do this automatically
3. Try broader search terms
4. Use metadata search for specific files

---

## Dashboard won't start

**Symptoms**: Error when launching dashboard

**Solution**:
1. Check Node.js is installed (v18+)
2. Run `npm install` in dashboard directory
3. Check port 3000 is available
4. Kill existing processes: `lsof -i :3000`

---

## Slow processing

**Symptoms**: Initial setup takes very long

**Solution**:
1. First-time embedding creation is slow (1-2 min normal)
2. Subsequent runs use incremental updates (fast)
3. For very large history, consider limiting date range

---

## Missing dependencies

**Symptoms**: Import errors when running

**Solution**:
```bash
pip install -r requirements.txt
```

Required packages:
- sentence-transformers
- chromadb
- sqlite3 (built-in)

---

## Embeddings out of date

**Symptoms**: New conversations not appearing in search

**Solution**:
1. Skill automatically updates on each use
2. Force rebuild: delete ChromaDB folder and rerun
3. Check incremental processing completed

---

## Database locked

**Symptoms**: SQLite errors about locked database

**Solution**:
1. Close other processes using the database
2. Close the dashboard if running
3. Wait a moment and retry
