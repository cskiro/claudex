# cc-insights: Claude Code Conversation Insights

Automatically process, search, and analyze your Claude Code conversation history using RAG-powered semantic search and intelligent pattern detection.

## Overview

This skill transforms your Claude Code conversations into actionable insights without any manual effort. It automatically processes conversations stored in `~/.claude/projects/`, builds a searchable knowledge base with semantic understanding, and generates insightful reports about your development patterns.

### Key Features

- 🔍 **RAG-Powered Semantic Search**: Find conversations by meaning, not just keywords
- 📊 **Automatic Insight Reports**: Detect patterns, file hotspots, and tool usage analytics
- 📈 **Activity Trends**: Understand development patterns over time
- 💡 **Knowledge Extraction**: Surface recurring topics and solutions
- 🎯 **Zero Manual Effort**: Fully automatic processing of existing conversations
- 🚀 **Fast Performance**: <1s search, <10s report generation

## Quick Start

### 1. Installation

```bash
# Navigate to the skill directory
cd .claude/skills/cc-insights

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python scripts/conversation-processor.py --help
```

### 2. Initial Setup

Process your existing conversations:

```bash
# Process all conversations for current project
python scripts/conversation-processor.py --project-name annex --verbose --stats

# Build semantic search index
python scripts/rag-indexer.py --verbose --stats
```

This one-time setup will:
- Parse all JSONL files from `~/.claude/projects/`
- Extract metadata (files, tools, topics, timestamps)
- Build SQLite database for fast queries
- Generate vector embeddings for semantic search
- Create ChromaDB index

**Time**: ~1-2 minutes for 100 conversations

### 3. Search Conversations

```bash
# Semantic search (understands meaning)
python scripts/search-conversations.py "fixing authentication bugs"

# Search by file
python scripts/search-conversations.py --file "src/auth/token.ts"

# Search by tool
python scripts/search-conversations.py --tool "Write"

# Keyword search with date filter
python scripts/search-conversations.py "refactoring" --keyword --date-from 2025-10-01
```

### 4. Generate Insights

```bash
# Weekly activity report
python scripts/insight-generator.py weekly --verbose

# File heatmap (most modified files)
python scripts/insight-generator.py file-heatmap

# Tool usage analytics
python scripts/insight-generator.py tool-usage

# Save report to file
python scripts/insight-generator.py weekly --output weekly-report.md
```

## Usage via Skill

Once set up, you can interact with the skill naturally:

```
User: "Search conversations about React performance optimization"
→ Returns top semantic matches with context

User: "Generate insights for the past week"
→ Creates comprehensive weekly report with metrics

User: "Show me files I've modified most often"
→ Generates file heatmap with recommendations
```

## Architecture

```
.claude/skills/cc-insights/
├── SKILL.md                   # Skill definition for Claude
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
│
├── scripts/                   # Core functionality
│   ├── conversation-processor.py   # Parse JSONL, extract metadata
│   ├── rag-indexer.py              # Build vector embeddings
│   ├── search-conversations.py     # Search interface
│   └── insight-generator.py        # Report generation
│
├── templates/                 # Report templates
│   └── weekly-summary.md
│
└── .processed/               # Generated data (gitignored)
    ├── conversations.db       # SQLite metadata
    └── embeddings/           # ChromaDB vector store
        ├── chroma.sqlite3
        └── [embedding data]
```

## Scripts Reference

### conversation-processor.py

Parse JSONL files and extract conversation metadata.

**Usage:**
```bash
python scripts/conversation-processor.py [OPTIONS]

Options:
  --project-name TEXT    Project to process (default: annex)
  --db-path PATH         Database path
  --reindex              Reprocess all (ignore cache)
  --verbose              Show detailed logs
  --stats                Display statistics after processing
```

**What it does:**
- Scans `~/.claude/projects/[project]/*.jsonl`
- Decodes base64-encoded conversation content
- Extracts: messages, files, tools, topics, timestamps
- Stores in SQLite with indexes for fast queries
- Tracks processing state for incremental updates

**Output:**
- SQLite database at `.processed/conversations.db`
- Processing state for incremental updates

### rag-indexer.py

Build vector embeddings for semantic search.

**Usage:**
```bash
python scripts/rag-indexer.py [OPTIONS]

Options:
  --db-path PATH         Database path
  --embeddings-dir PATH  ChromaDB directory
  --model TEXT           Embedding model (default: all-MiniLM-L6-v2)
  --rebuild              Rebuild entire index
  --batch-size INT       Batch size (default: 32)
  --verbose              Show detailed logs
  --stats                Display statistics
  --test-search TEXT     Test search with query
```

**What it does:**
- Reads conversations from SQLite
- Generates embeddings using sentence-transformers
- Stores in ChromaDB for similarity search
- Supports incremental indexing (only new conversations)

**Models:**
- `all-MiniLM-L6-v2` (default): Fast, good quality, 384 dimensions
- `all-mpnet-base-v2`: Higher quality, slower, 768 dimensions

### search-conversations.py

Search conversations with semantic + metadata filters.

**Usage:**
```bash
python scripts/search-conversations.py QUERY [OPTIONS]

Options:
  --semantic/--keyword   Semantic (RAG) or keyword search (default: semantic)
  --file TEXT            Filter by file pattern
  --tool TEXT            Search by tool name
  --date-from TEXT       Start date (ISO format)
  --date-to TEXT         End date (ISO format)
  --limit INT            Max results (default: 10)
  --format TEXT          Output: text|json|markdown (default: text)
  --verbose              Show detailed logs
```

**Examples:**
```bash
# Semantic search
python scripts/search-conversations.py "authentication bugs"

# Filter by file
python scripts/search-conversations.py "React optimization" --file "src/components"

# Search by tool
python scripts/search-conversations.py --tool "Edit"

# Date range
python scripts/search-conversations.py "deployment" --date-from 2025-10-01

# JSON output for integration
python scripts/search-conversations.py "testing" --format json > results.json
```

### insight-generator.py

Generate pattern-based reports and analytics.

**Usage:**
```bash
python scripts/insight-generator.py REPORT_TYPE [OPTIONS]

Report Types:
  weekly          Weekly activity summary
  file-heatmap    File modification heatmap
  tool-usage      Tool usage analytics

Options:
  --date-from TEXT       Start date (ISO format)
  --date-to TEXT         End date (ISO format)
  --output PATH          Save to file (default: stdout)
  --verbose              Show detailed logs
```

**Examples:**
```bash
# Weekly report (last 7 days)
python scripts/insight-generator.py weekly

# Custom date range
python scripts/insight-generator.py weekly --date-from 2025-10-01 --date-to 2025-10-15

# File heatmap with output
python scripts/insight-generator.py file-heatmap --output heatmap.md

# Tool analytics
python scripts/insight-generator.py tool-usage
```

## Data Storage

All processed data is stored locally in `.processed/` (gitignored):

### SQLite Database (`conversations.db`)

**Tables:**
- `conversations`: Main metadata (timestamps, messages, topics)
- `file_interactions`: File-level interactions (read, write, edit)
- `tool_usage`: Tool usage counts per conversation
- `processing_state`: Tracks processed files for incremental updates

**Indexes:**
- `idx_timestamp`: Fast date-range queries
- `idx_project`: Filter by project
- `idx_file_path`: File-based searches
- `idx_tool_name`: Tool usage queries

### ChromaDB Vector Store (`embeddings/`)

**Contents:**
- Vector embeddings (384-dimensional by default)
- Document text for retrieval
- Metadata for filtering
- HNSW index for fast similarity search

**Performance:**
- <1 second for semantic search
- Handles 10,000+ conversations efficiently
- ~100MB per 1,000 conversations

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Initial processing (100 convs) | ~30s | One-time setup |
| Initial indexing (100 convs) | ~60s | One-time setup |
| Incremental processing | <5s | Only new conversations |
| Semantic search | <1s | Top 10 results |
| Keyword search | <0.1s | SQLite FTS |
| Weekly report generation | <10s | Includes visualizations |

## Troubleshooting

### "Database not found"

**Problem:** Scripts can't find `conversations.db`

**Solution:**
```bash
# Run processor first
python scripts/conversation-processor.py --project-name annex --verbose
```

### "No conversations found"

**Problem:** Project name doesn't match or no JSONL files

**Solution:**
```bash
# Check project directories
ls ~/.claude/projects/

# Use correct project name (may be encoded)
python scripts/conversation-processor.py --project-name [actual-name] --verbose
```

### "ImportError: sentence_transformers"

**Problem:** Dependencies not installed

**Solution:**
```bash
# Install requirements
pip install -r requirements.txt

# Or individually
pip install sentence-transformers chromadb jinja2 click python-dateutil
```

### "Slow embedding generation"

**Problem:** Large number of conversations

**Solution:**
```bash
# Use smaller batch size
python scripts/rag-indexer.py --batch-size 16

# Or use faster model (lower quality)
python scripts/rag-indexer.py --model all-MiniLM-L6-v2
```

### "Out of memory"

**Problem:** Too many conversations processed at once

**Solution:**
```bash
# Smaller batch size
python scripts/rag-indexer.py --batch-size 8

# Or process in chunks by date
python scripts/conversation-processor.py --date-from 2025-10-01 --date-to 2025-10-15
```

## Incremental Updates

The system automatically handles incremental updates:

1. **Conversation Processor**: Tracks file hashes in `processing_state` table
   - Only reprocesses changed files
   - Detects new JSONL files automatically

2. **RAG Indexer**: Checks ChromaDB for existing IDs
   - Only indexes new conversations
   - Skips already-embedded conversations

**Recommended workflow:**
```bash
# Daily/weekly: Run both for new conversations
python scripts/conversation-processor.py --project-name annex
python scripts/rag-indexer.py

# Takes <5s if only a few new conversations
```

## Integration Examples

### Search from command line
```bash
# Quick search function in .bashrc or .zshrc
cc-search() {
  python ~/.claude/skills/cc-insights/scripts/search-conversations.py "$@"
}

# Usage
cc-search "authentication bugs"
```

### Generate weekly report automatically
```bash
# Add to crontab for weekly reports
0 9 * * MON cd ~/.claude/skills/cc-insights && python scripts/insight-generator.py weekly --output ~/reports/weekly-$(date +\%Y-\%m-\%d).md
```

### Export data for external tools
```bash
# Export to JSON
python scripts/search-conversations.py "testing" --format json | jq

# Export metadata
sqlite3 .processed/conversations.db "SELECT * FROM conversations" -json > export.json
```

## Privacy & Security

- **Local-only**: All data stays on your machine
- **No external APIs**: Embeddings generated locally
- **Project-scoped**: Only accesses current project
- **Gitignored**: `.processed/` excluded from version control
- **Sensitive data**: Review before sharing reports (may contain secrets)

## Requirements

### Python Dependencies
- `sentence-transformers>=2.2.0` - Semantic embeddings
- `chromadb>=0.4.0` - Vector database
- `jinja2>=3.1.0` - Template engine
- `click>=8.1.0` - CLI framework
- `python-dateutil>=2.8.0` - Date utilities

### System Requirements
- Python 3.8+
- 500MB disk space (for 1,000 conversations)
- 2GB RAM (for embedding generation)

## Limitations

- **Read-only**: Analyzes existing conversations, doesn't modify them
- **Single project**: Designed for per-project insights (not cross-project)
- **Static analysis**: Analyzes saved conversations, not real-time
- **Embedding quality**: Good but not GPT-4 level (local models)
- **JSONL format**: Depends on Claude Code's internal storage format

## Future Enhancements

Potential additions (not currently implemented):

- [ ] Cross-project analytics dashboard
- [ ] AI-powered summarization with LLM
- [ ] Slack/Discord integration for weekly reports
- [ ] Git commit correlation
- [ ] VS Code extension
- [ ] Web dashboard (Next.js)
- [ ] Confluence/Notion export
- [ ] Custom embedding models

## FAQ

**Q: How often should I rebuild the index?**
A: Never, unless changing models. Use incremental updates.

**Q: Can I change the embedding model?**
A: Yes, use `--model` flag with rag-indexer.py, then `--rebuild`.

**Q: Does this work with incognito mode?**
A: No, incognito conversations aren't saved to JSONL files.

**Q: Can I share reports with my team?**
A: Yes, but review for sensitive information first (API keys, secrets).

**Q: What if Claude Code changes the JSONL format?**
A: The processor may need updates. File an issue if parsing breaks.

**Q: Can I delete old conversations?**
A: Yes, remove JSONL files and run `--reindex` to rebuild.

## Contributing

Contributions welcome! Areas to improve:

- Additional report templates
- Better pattern detection algorithms
- Performance optimizations
- Web dashboard implementation
- Documentation improvements

## License

MIT License - See repository root for details

## Support

For issues or questions:
1. Check this README and SKILL.md
2. Review script `--help` output
3. Run with `--verbose` to see detailed logs
4. Check `.processed/logs/` if created
5. Open an issue in the repository

---

**Built for Connor's annex project**
*Zero-effort conversation intelligence*
