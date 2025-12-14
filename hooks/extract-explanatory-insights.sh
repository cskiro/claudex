#!/bin/bash
# extract-explanatory-insights.sh
# Extracts ★ Insight blocks from Claude Code responses and saves them to docs/lessons-learned
# Hook Type: Stop (command-based)
# Trigger: After Claude completes a response (main agent stop event)
# Exit Codes: 0 (success), 1 (no insights found - silent), 2 (error - blocks execution)
# Version: 2.1.0 - Content-based deduplication using SHA256 hashes (allows multiple insights per session)

set -o pipefail
# Note: -e and -u removed for resilience - hooks should never crash Claude Code

# Read hook input from stdin
INPUT=$(cat)

# Extract key variables from JSON input
PROJECT_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

# Validate required inputs
if [[ -z "$PROJECT_DIR" || -z "$TRANSCRIPT_PATH" ]]; then
    # Silent exit - no error for missing context
    exit 0
fi

# Skip if not in a project directory (e.g., global ~/.claude)
if [[ "$PROJECT_DIR" == "$HOME/.claude" ]]; then
    exit 0
fi

# Create lessons-learned directory structure
LESSONS_DIR="$PROJECT_DIR/docs/lessons-learned"
mkdir -p "$LESSONS_DIR"

# Optional: Enable logging for debugging (uncomment to enable)
LOG_FILE="$HOME/.claude/state/logs/hook-extract-insights.log"
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date)] Processing session: $SESSION_ID" >> "$LOG_FILE"
echo "[$(date)] PROJECT_DIR: $PROJECT_DIR" >> "$LOG_FILE"
echo "[$(date)] TRANSCRIPT_PATH: $TRANSCRIPT_PATH" >> "$LOG_FILE"

# Deduplication: Track processed insight hashes to avoid duplicates
STATE_DIR="$HOME/.claude/state/hook-state"
mkdir -p "$STATE_DIR"
PROCESSED_HASHES_FILE="$STATE_DIR/insights-hashes.txt"

# Create hash file if it doesn't exist
touch "$PROCESSED_HASHES_FILE"

# Read the last 500 lines from transcript (Stop event = complete response)
# Stop hook fires after Claude's full response, so we capture more context
if [[ ! -f "$TRANSCRIPT_PATH" ]]; then
    # Transcript not accessible - silent exit
    exit 0
fi

# Extract text content from JSONL transcript (assistant messages only)
# The transcript is in JSONL format with escaped newlines, so we need to:
# 1. Filter for assistant messages with text content
# 2. Extract the text field and unescape newlines
# 3. Then parse for insight blocks
LAST_RESPONSE=$(tail -n 500 "$TRANSCRIPT_PATH" 2>/dev/null | \
    grep '"type":"assistant"' | \
    python3 -c '
import sys
import json

for line in sys.stdin:
    try:
        obj = json.loads(line.strip())
        content = obj.get("message", {}).get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    print(item.get("text", ""))
    except:
        pass
' 2>/dev/null || echo "")

# Exit if transcript read failed or is empty
if [[ -z "$LAST_RESPONSE" ]]; then
    echo "[$(date)] No assistant messages found in transcript" >> "$LOG_FILE"
    exit 0
fi

# Check if there's an insight block in the last response
if ! echo "$LAST_RESPONSE" | grep -q "★ Insight"; then
    # No insights found - silent exit
    echo "[$(date)] No insights found in transcript" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date)] Found insights in transcript!" >> "$LOG_FILE"

# Extract all insight blocks from the last response
INSIGHTS=$(echo "$LAST_RESPONSE" | awk '
    /★ Insight ─+/ {
        in_insight = 1
        insight = ""
        next
    }
    /─+/ && in_insight {
        in_insight = 0
        if (length(insight) > 0) {
            print insight
            print "---INSIGHT_SEPARATOR---"
        }
        next
    }
    in_insight {
        insight = insight $0 "\n"
    }
')

# Exit if no insights extracted
if [[ -z "$INSIGHTS" ]]; then
    echo "[$(date)] Insights found but extraction failed" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date)] Successfully extracted insights, processing..." >> "$LOG_FILE"

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_SLUG=$(date '+%Y-%m-%d')

# Determine category from insight content (simple heuristic)
# This can be enhanced with more sophisticated categorization
categorize_insight() {
    local insight="$1"

    # Check for common patterns to auto-categorize
    if echo "$insight" | grep -iq "test\|testing\|coverage\|tdd\|vitest\|jest"; then
        echo "testing"
    elif echo "$insight" | grep -iq "config\|settings\|inheritance\|precedence"; then
        echo "configuration"
    elif echo "$insight" | grep -iq "hook\|lifecycle\|event\|trigger"; then
        echo "hooks-and-events"
    elif echo "$insight" | grep -iq "security\|vulnerability\|auth\|permission"; then
        echo "security"
    elif echo "$insight" | grep -iq "performance\|optimize\|cache\|memory"; then
        echo "performance"
    elif echo "$insight" | grep -iq "architecture\|design\|pattern\|structure"; then
        echo "architecture"
    elif echo "$insight" | grep -iq "git\|commit\|branch\|merge\|pr\|pull request"; then
        echo "version-control"
    elif echo "$insight" | grep -iq "react\|component\|tsx\|jsx\|hooks"; then
        echo "react"
    elif echo "$insight" | grep -iq "typescript\|type\|interface\|generic"; then
        echo "typescript"
    else
        echo "general"
    fi
}

# Process insights and create one file per session per category
# Bash 3.2 compatible - no associative arrays
CURRENT_INSIGHT=""
PROCESSED_CATEGORIES=""

while IFS= read -r line; do
    if [[ "$line" == "---INSIGHT_SEPARATOR---" ]]; then
        if [[ -n "${CURRENT_INSIGHT:-}" ]]; then
            # Generate hash of insight content for deduplication
            INSIGHT_HASH=$(echo "$CURRENT_INSIGHT" | shasum -a 256 | awk '{print $1}')

            # Check if this insight has already been processed
            if grep -q "^$INSIGHT_HASH$" "$PROCESSED_HASHES_FILE" 2>/dev/null; then
                echo "[$(date)] Skipping duplicate insight (hash: ${INSIGHT_HASH:0:12}...)" >> "$LOG_FILE"
                CURRENT_INSIGHT=""
                continue
            fi

            # Categorize the insight
            CATEGORY=$(categorize_insight "$CURRENT_INSIGHT")
            CATEGORY_DIR="$LESSONS_DIR/$CATEGORY"
            mkdir -p "$CATEGORY_DIR"

            # Check if this is the first insight in this category for this session
            if ! echo "$PROCESSED_CATEGORIES" | grep -q "^${CATEGORY}$"; then
                # First insight in this category - create new file with descriptive name
                FIRST_TITLE=$(echo "$CURRENT_INSIGHT" | head -n 1 | sed 's/^[*_[:space:]]*//' | sed 's/[*_[:space:]]*$//')

                # Create a slugified filename from the title
                # Convert to lowercase, replace spaces with hyphens, remove special chars
                SLUG=$(echo "$FIRST_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 -]//g' | tr -s ' ' '-' | cut -c1-50)

                # Generate filename: YYYY-MM-DD-descriptive-name.md
                OUTPUT_FILE="$CATEGORY_DIR/${DATE_SLUG}-${SLUG}.md"

                # Uppercase first letter of category for header (bash 3.2 compatible)
                CATEGORY_TITLE="$(echo "$CATEGORY" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')"

                # Create the file with header
                cat > "$OUTPUT_FILE" <<EOF
# $CATEGORY_TITLE Insights - $(date '+%B %d, %Y')

Auto-generated lessons learned from Claude Code Explanatory insights.

**Session**: $SESSION_ID
**Generated**: $TIMESTAMP

---

EOF
                # Mark this category as processed
                PROCESSED_CATEGORIES="${PROCESSED_CATEGORIES}${CATEGORY}"$'\n'

                echo "[$(date)] Created new file: $OUTPUT_FILE" >> "$LOG_FILE"
            fi

            # Extract the title for this insight
            TITLE=$(echo "$CURRENT_INSIGHT" | head -n 1 | sed 's/^[*_[:space:]]*//' | sed 's/[*_[:space:]]*$//')

            # Append the insight to the category file
            cat >> "$OUTPUT_FILE" <<EOF
## $TITLE

$CURRENT_INSIGHT

---

EOF

            # Mark this insight hash as processed
            echo "$INSIGHT_HASH" >> "$PROCESSED_HASHES_FILE"
            echo "[$(date)] Processed insight: $TITLE (hash: ${INSIGHT_HASH:0:12}...)" >> "$LOG_FILE"

            CURRENT_INSIGHT=""
        fi
    else
        CURRENT_INSIGHT="${CURRENT_INSIGHT:-}${line}"$'\n'
    fi
done <<< "$INSIGHTS"

# Create/update the index file
INDEX_FILE="$LESSONS_DIR/README.md"
cat > "$INDEX_FILE" <<'EOF'
# Lessons Learned Index

This directory contains auto-extracted insights from Claude Code sessions using the Explanatory output style.

## Directory Structure

Insights are organized by category with timestamped, descriptive filenames:

```
docs/lessons-learned/
├── README.md (this file)
├── architecture/
│   ├── 2025-11-14-system-design-patterns.md
│   └── 2025-11-10-microservices-architecture.md
├── configuration/
│   └── 2025-11-12-config-inheritance.md
├── hooks-and-events/
│   ├── 2025-11-14-hook-debugging-strategy.md
│   └── 2025-11-13-lifecycle-events.md
├── performance/
│   └── 2025-11-11-optimization-techniques.md
├── react/
│   └── 2025-11-14-component-patterns.md
├── security/
│   └── 2025-11-09-auth-best-practices.md
├── testing/
│   └── 2025-11-14-tdd-workflow.md
├── typescript/
│   └── 2025-11-10-type-safety.md
├── version-control/
│   └── 2025-11-08-git-workflow.md
└── general/
    └── 2025-11-07-general-tips.md
```

## Categories

EOF

# List all categories with their insight files
for category_dir in "$LESSONS_DIR"/*/; do
    if [[ -d "$category_dir" && "$category_dir" != "$LESSONS_DIR/" ]]; then
        category=$(basename "$category_dir")

        # Find all markdown files in this category (sorted by date, newest first)
        files=$(find "$category_dir" -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -r)

        if [[ -n "$files" ]]; then
            # Count total insights across all files
            total_insights=0
            file_count=0

            # Uppercase first letter (bash 3.2 compatible)
            category_title="$(echo "$category" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')"

            cat >> "$INDEX_FILE" <<EOF
### $category_title

EOF

            # List each file with its insight count
            while IFS= read -r file; do
                if [[ -f "$file" ]]; then
                    filename=$(basename "$file")
                    count=$(grep -c "^## " "$file" 2>/dev/null || echo "0")
                    total_insights=$((total_insights + count))
                    file_count=$((file_count + 1))
                    last_updated=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || stat -c "%y" "$file" 2>/dev/null | cut -d' ' -f1 || echo "Unknown")

                    cat >> "$INDEX_FILE" <<EOF
- [\`$filename\`](./$category/$filename) - $count insight$([ "$count" -ne 1 ] && echo "s" || echo "") (Updated: $last_updated)
EOF
                fi
            done <<< "$files"

            cat >> "$INDEX_FILE" <<EOF

**Total**: $total_insights insight$([ "$total_insights" -ne 1 ] && echo "s" || echo "") across $file_count file$([ "$file_count" -ne 1 ] && echo "s" || echo "")

EOF
        fi
    fi
done

cat >> "$INDEX_FILE" <<'EOF'

## Usage

Each category contains an `insights.md` file with chronologically ordered insights. Insights are automatically categorized based on content analysis.

### Manual Categorization

If you need to recategorize an insight:
1. Cut the insight from the current file
2. Paste it into the appropriate category file
3. The index will auto-update on the next extraction

### Searching

Use grep to search across all insights:
```bash
grep -r "your search term" docs/lessons-learned/
```

Or use ripgrep for faster searches:
```bash
rg "your search term" docs/lessons-learned/
```

---

*Auto-generated by extract-explanatory-insights.sh hook*
EOF

# Cleanup: Keep only last 10000 processed insight hashes to prevent file bloat
if [[ -f "$PROCESSED_HASHES_FILE" ]]; then
    HASH_COUNT=$(wc -l < "$PROCESSED_HASHES_FILE")
    if [[ $HASH_COUNT -gt 10000 ]]; then
        tail -n 10000 "$PROCESSED_HASHES_FILE" > "${PROCESSED_HASHES_FILE}.tmp" && mv "${PROCESSED_HASHES_FILE}.tmp" "$PROCESSED_HASHES_FILE"
        echo "[$(date)] Cleaned up hash file (kept last 10000 of $HASH_COUNT hashes)" >> "$LOG_FILE"
    fi
fi

# Optional: Log success (uncomment if logging enabled)
echo "[$(date)] Successfully processed session: $SESSION_ID" >> "$LOG_FILE"

# Silent success - insights extracted
exit 0
