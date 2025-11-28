# Phase 1: Insight Discovery and Parsing

**Purpose**: Locate, read, deduplicate, and structure all insights from the project's lessons-learned directory.

## Steps

### 1. Verify project structure
- Ask user for project root directory (default: current working directory)
- Check if `docs/lessons-learned/` exists
- If not found, explain the expected structure and offer to search alternative locations
- List all categories found (testing, configuration, hooks-and-events, etc.)

### 2. Scan and catalog insight files

**File Naming Convention**:
Files MUST follow: `YYYY-MM-DD-descriptive-slug.md`
- Date prefix for chronological sorting
- Descriptive slug (3-5 words) summarizing the insight topic
- Examples:
  - `2025-11-21-jwt-refresh-token-pattern.md`
  - `2025-11-20-vitest-mocking-best-practices.md`
  - `2025-11-19-react-testing-library-queries.md`

**Scanning**:
- Use Glob tool to find all markdown files: `docs/lessons-learned/**/*.md`
- For each file found, extract:
  - File path and category (from directory name)
  - Creation date (from filename prefix)
  - Descriptive title (from filename slug)
  - File size and line count
- Build initial inventory report

### 3. Deduplicate insights (CRITICAL)

**Why**: The extraction hook may create duplicate entries within files.

**Deduplication Algorithm**:
```python
def deduplicate_insights(insights):
    seen_hashes = set()
    unique_insights = []

    for insight in insights:
        # Create hash from normalized content
        content_hash = hash(normalize(insight.title + insight.content[:200]))

        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_insights.append(insight)
        else:
            log_duplicate(insight)

    return unique_insights
```

**Deduplication Checks**:
- Exact title match → duplicate
- First 200 chars content match → duplicate
- Same code blocks in same order → duplicate
- Report: "Found X insights, removed Y duplicates (Z unique)"

### 4. Parse individual insights
- Read each file using Read tool
- Extract session metadata (session ID, timestamp from file headers)
- Split file content on `---` separator (insights are separated by horizontal rules)
- For each insight section:
  - Extract title (first line, often wrapped in `**bold**`)
  - Extract body content (remaining markdown)
  - Identify code blocks
  - Extract actionable items (lines starting with `- [ ]` or numbered lists)
  - Note any warnings/cautions

### 5. Apply quality filters

**Filter out low-depth insights** that are:
- Basic explanatory notes without actionable steps
- Simple definitions or concept explanations
- Single-paragraph observations

**Keep insights that have**:
- Actionable workflows (numbered steps, checklists)
- Decision frameworks (trade-offs, when to use X vs Y)
- Code patterns with explanation of WHY
- Troubleshooting guides with solutions
- Best practices with concrete examples

**Quality Score Calculation**:
```
score = 0
if has_actionable_items: score += 3
if has_code_examples: score += 2
if has_numbered_steps: score += 2
if word_count > 200: score += 1
if has_warnings_or_notes: score += 1

# Minimum score for skill consideration: 4
```

### 6. Build structured insight inventory
```
{
  id: unique_id,
  title: string,
  content: string,
  category: string,
  date: ISO_date,
  session_id: string,
  source_file: path,
  code_examples: [{ language, code }],
  action_items: [string],
  keywords: [string],
  quality_score: int,
  paragraph_count: int,
  line_count: int
}
```

### 7. Present discovery summary
- Total insights found (before deduplication)
- Duplicates removed
- Low-quality insights filtered
- **Final count**: Unique, quality insights
- Category breakdown
- Date range (earliest to latest)
- Preview of top 5 insights by quality score

## Output

Deduplicated, quality-filtered inventory of insights with metadata and categorization.

## Common Issues

- **No lessons-learned directory**: Ask if user wants to search elsewhere or exit
- **Empty files**: Skip and report count of empty files
- **Malformed markdown**: Log warning but continue parsing (best effort)
- **Missing session metadata**: Use filename date as fallback
- **High duplicate count**: Indicates extraction hook bug - warn user
- **All insights filtered as low-quality**: Lower threshold or suggest manual curation
- **Files without descriptive names**: Suggest renaming for better organization
