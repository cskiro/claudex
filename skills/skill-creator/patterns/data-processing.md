# Data Processing Skill Pattern

Use this pattern when your skill **processes, analyzes, or transforms** data to extract insights.

## When to Use

- Skill ingests data from files or APIs
- Performs analysis or transformation
- Generates insights, reports, or visualizations
- Examples: cc-insights (conversation analysis)

## Structure

### Data Flow Architecture

Define clear data pipeline:

```
Input Sources → Processing → Storage → Query/Analysis → Output
```

Example:
```
JSONL files → Parser → SQLite + Vector DB → Search/Analytics → Reports/Dashboard
```

### Processing Modes

**Batch Processing:**
- Process all data at once
- Good for: Initial setup, complete reprocessing
- Trade-off: Slow startup, complete data

**Incremental Processing:**
- Process only new/changed data
- Good for: Regular updates, performance
- Trade-off: Complex state tracking

**Streaming Processing:**
- Process data as it arrives
- Good for: Real-time updates
- Trade-off: Complex implementation

### Storage Strategy

Choose appropriate storage:

**SQLite:**
- Structured metadata
- Fast queries
- Relational data
- Good for: Indexes, aggregations

**Vector Database (ChromaDB):**
- Semantic embeddings
- Similarity search
- Good for: RAG, semantic queries

**File System:**
- Raw data
- Large blobs
- Good for: Backups, archives

## Example: CC Insights

**Input**: Claude Code conversation JSONL files

**Processing Pipeline:**
1. JSONL Parser - Decode base64, extract messages
2. Metadata Extractor - Timestamps, files, tools
3. Embeddings Generator - Vector representations
4. Pattern Detector - Identify trends

**Storage:**
- SQLite: Conversation metadata, fast queries
- ChromaDB: Vector embeddings, semantic search
- Cache: Processed conversation data

**Query Interfaces:**
1. CLI Search - Command-line semantic search
2. Insight Generator - Pattern-based reports
3. Dashboard - Interactive web UI

**Outputs:**
- Search results with similarity scores
- Weekly activity reports
- File heatmaps
- Tool usage analytics

## Data Processing Workflow

### Phase 1: Ingestion
```markdown
1. **Discover Data Sources**
   - Locate input files/APIs
   - Validate accessibility
   - Calculate scope (file count, size)

2. **Initial Validation**
   - Check format validity
   - Verify schema compliance
   - Estimate processing time

3. **State Management**
   - Track what's been processed
   - Support incremental updates
   - Handle failures gracefully
```

### Phase 2: Processing
```markdown
1. **Parse/Transform**
   - Read raw data
   - Apply transformations
   - Handle errors and edge cases

2. **Extract Features**
   - Generate metadata
   - Calculate metrics
   - Create embeddings (if semantic search)

3. **Store Results**
   - Write to database(s)
   - Update indexes
   - Maintain consistency
```

### Phase 3: Analysis
```markdown
1. **Query Interface**
   - Support multiple query types
   - Optimize for common patterns
   - Return ranked results

2. **Pattern Detection**
   - Aggregate data
   - Identify trends
   - Generate insights

3. **Visualization**
   - Format for human consumption
   - Support multiple output formats
   - Interactive when possible
```

## Performance Characteristics

Document expected performance:

```markdown
### Performance Characteristics

- **Initial indexing**: ~1-2 minutes for 100 records
- **Incremental updates**: <5 seconds for new records
- **Search latency**: <1 second for queries
- **Report generation**: <10 seconds for standard reports
- **Memory usage**: ~200MB for 1000 records
```

## Best Practices

1. **Incremental Processing**: Don't reprocess everything on each run
2. **State Tracking**: Track what's been processed to avoid duplicates
3. **Batch Operations**: Process in batches for memory efficiency
4. **Progress Indicators**: Show progress for long operations
5. **Error Recovery**: Handle failures gracefully, resume where left off
6. **Data Validation**: Validate inputs before expensive processing
7. **Index Optimization**: Optimize databases for common queries
8. **Memory Management**: Stream large files, don't load everything
9. **Parallel Processing**: Use parallelism when possible
10. **Cache Wisely**: Cache expensive computations

## Scripts Structure

For data processing skills, provide helper scripts:

```
scripts/
├── processor.py          # Main data processing script
├── indexer.py           # Build indexes/embeddings
├── query.py             # Query interface (CLI)
└── generator.py         # Report/insight generation
```

### Script Best Practices

```python
# Good patterns for processing scripts:

# 1. Use click for CLI
import click

@click.command()
@click.option('--input', help='Input path')
@click.option('--reindex', is_flag=True)
def process(input, reindex):
    """Process data from input source."""
    pass

# 2. Show progress
from tqdm import tqdm
for item in tqdm(items, desc="Processing"):
    process_item(item)

# 3. Handle errors gracefully
try:
    result = process_item(item)
except Exception as e:
    logger.error(f"Failed to process {item}: {e}")
    continue  # Continue with next item

# 4. Support incremental updates
if not reindex and is_already_processed(item):
    continue

# 5. Use batch processing
for batch in chunks(items, batch_size=32):
    process_batch(batch)
```

## Storage Schema

Document your data schema:

```sql
-- Example SQLite schema
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    timestamp INTEGER,
    message_count INTEGER,
    files_modified TEXT,  -- JSON array
    tools_used TEXT       -- JSON array
);

CREATE INDEX idx_timestamp ON conversations(timestamp);
CREATE INDEX idx_files ON conversations(files_modified);
```

## Output Formats

Support multiple output formats:

1. **Markdown**: Human-readable reports
2. **JSON**: Machine-readable for integration
3. **CSV**: Spreadsheet-compatible data
4. **HTML**: Styled reports with charts
5. **Interactive**: Web dashboards (optional)
