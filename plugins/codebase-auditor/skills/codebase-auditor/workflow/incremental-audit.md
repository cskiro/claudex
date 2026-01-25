# Incremental Audit Workflow

Strategies for auditing large codebases (>100k LOC) without overwhelming context or compute.

## Chunking Strategies

### 1. Directory-Based Chunking

Audit one directory tree at a time, rolling up results.

```bash
# Example: Audit src/ in chunks
audit_chunk() {
  local dir=$1
  python3 scripts/audit_engine.py --scope "$dir" --output "reports/${dir//\//_}.json"
}

# Run per top-level directory
for dir in src/*/; do
  audit_chunk "$dir"
done

# Merge results
python3 scripts/merge_reports.py reports/*.json > audit_report.json
```

**Best for:** Monorepos, microservices, clearly separated modules

### 2. Layer-Based Chunking

Audit by architectural layer to maintain cohesion.

| Layer | Directories | Priority |
|-------|-------------|----------|
| API | `src/api/`, `src/routes/` | P0 |
| Business Logic | `src/services/`, `src/domain/` | P0 |
| Data Access | `src/repositories/`, `src/models/` | P1 |
| Infrastructure | `src/config/`, `src/utils/` | P2 |
| Presentation | `src/components/`, `src/pages/` | P1 |

**Best for:** Layered architectures, MVC patterns

### 3. Risk-Based Chunking

Prioritize by security and complexity risk.

```yaml
high_risk_patterns:
  - "**/auth/**"
  - "**/payment/**"
  - "**/api/**"
  - "**/*controller*"
  - "**/*service*"

medium_risk_patterns:
  - "**/utils/**"
  - "**/helpers/**"
  - "**/*model*"

low_risk_patterns:
  - "**/tests/**"
  - "**/mocks/**"
  - "**/*.config.*"
```

**Best for:** Security-focused audits, compliance requirements

### 4. Change-Based Chunking

Audit only files changed since last audit.

```bash
# Get files changed since last audit
git diff --name-only $(cat .audit-baseline) HEAD > changed_files.txt

# Audit only changed files
python3 scripts/audit_engine.py --file-list changed_files.txt

# Update baseline
git rev-parse HEAD > .audit-baseline
```

**Best for:** CI/CD integration, PR reviews

## Session Resume

For audits interrupted mid-execution:

```json
{
  "session_id": "audit_2025-12-08_143022",
  "status": "in_progress",
  "completed_chunks": ["src/api", "src/services"],
  "pending_chunks": ["src/components", "src/utils"],
  "partial_results": "reports/session_partial.json",
  "resume_command": "python3 scripts/audit_engine.py --resume audit_2025-12-08_143022"
}
```

### Resume Protocol

1. Check for existing session file: `.audit-session.json`
2. If exists and `status: in_progress`, offer resume or restart
3. On resume, skip completed chunks, continue from pending
4. Merge partial results with new results on completion

## Progress Tracking

### CLI Progress Output

```
Codebase Audit Progress
========================
[################....] 80% (4/5 chunks)

Completed:
  ✓ src/api (23 findings)
  ✓ src/services (15 findings)
  ✓ src/models (8 findings)
  ✓ src/utils (12 findings)

In Progress:
  ⟳ src/components (analyzing...)

Pending:
  ○ (none)

Elapsed: 4m 32s | ETA: 1m 08s
```

### Progress File

```json
{
  "total_chunks": 5,
  "completed": 4,
  "findings_so_far": 58,
  "start_time": "2025-12-08T14:30:22Z",
  "estimated_completion": "2025-12-08T14:35:30Z"
}
```

## Memory Management

For very large codebases, prevent context overflow:

1. **Batch file processing**: Read files in batches of 50
2. **Stream results**: Write findings immediately, don't accumulate
3. **Summarize per-chunk**: Generate summary before moving to next chunk
4. **Garbage collect**: Clear parsed ASTs between chunks

```python
# Example: Streaming results
with open('findings.jsonl', 'a') as f:
    for finding in analyze_chunk(chunk):
        f.write(json.dumps(finding) + '\n')
        # Finding written immediately, memory freed
```
