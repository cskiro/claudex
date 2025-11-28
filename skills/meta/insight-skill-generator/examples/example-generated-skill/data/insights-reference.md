# Insights Reference: hook-deduplication-guide

This document contains the original insight from Claude Code's Explanatory output style that was used to create the **Hook Deduplication Guide** skill.

## Overview

**Total Insights**: 1
**Date Range**: 2025-11-03
**Categories**: hooks-and-events
**Sessions**: 1 unique session

---

## 1. Hook Deduplication Session Management

**Metadata**:
- **Date**: 2025-11-03
- **Category**: hooks-and-events
- **Session**: abc123-session-id
- **Source File**: docs/lessons-learned/hooks-and-events/2025-11-03-hook-deduplication.md

**Original Content**:

The extract-explanatory-insights hook initially used session-based deduplication, which prevented multiple insights from the same session from being stored. However, this created a limitation: if the same valuable insight appeared in different sessions, only the first one would be saved.

By switching to content-based deduplication using SHA256 hashing, we can:

1. **Allow multiple unique insights per session** - Different insights in the same conversation are all preserved
2. **Prevent true duplicates across sessions** - The same insight appearing in multiple conversations is stored only once
3. **Maintain efficient storage** - Hash file rotation keeps storage bounded

The implementation involves:

**Hash Generation**:
```bash
compute_content_hash() {
  local content="$1"
  echo -n "$content" | sha256sum | awk '{print $1}'
}
```

**Duplicate Detection**:
```bash
is_duplicate() {
  local content="$1"
  local content_hash=$(compute_content_hash "$content")

  if grep -Fxq "$content_hash" "$HASH_FILE"; then
    return 1  # Duplicate
  else
    return 0  # New content
  fi
}
```

**Hash Storage with Rotation**:
```bash
store_content_hash() {
  local content="$1"
  local content_hash=$(compute_content_hash "$content")
  echo "$content_hash" >> "$HASH_FILE"

  # Rotate if file exceeds MAX_HASHES
  local count=$(wc -l < "$HASH_FILE")
  if [ "$count" -gt 10000 ]; then
    tail -n 10000 "$HASH_FILE" > "${HASH_FILE}.tmp"
    mv "${HASH_FILE}.tmp" "$HASH_FILE"
  fi
}
```

This approach provides the best of both worlds: session independence and true deduplication based on content, not session boundaries.

---

## How This Insight Informs the Skill

### Hook Deduplication Session Management → Phase-Based Workflow

The insight's structure (problem → solution → implementation) maps directly to the skill's phases:

- **Problem Description** → Phase 1: Choose Deduplication Strategy
  - Explains why session-based is insufficient
  - Defines when content-based is needed

- **Solution Explanation** → Phase 2: Implement Content-Based Deduplication
  - Hash generation logic
  - Duplicate detection mechanism
  - State file management

- **Implementation Details** → Phase 3: Implement Hash Rotation
  - Rotation logic to prevent unbounded growth
  - MAX_HASHES configuration

- **Code Examples** → All phases
  - Bash functions extracted and integrated into workflow steps

---

## Additional Context

**Why This Insight Was Selected**:

This insight was selected for skill generation because it:
1. Provides a complete, actionable pattern
2. Includes working code examples
3. Solves a common problem in hook development
4. Is generally applicable (not project-specific)
5. Has clear benefits over the naive approach

**Quality Score**: 0.85 (high - qualified for standalone skill)

---

**Generated**: 2025-11-16
**Last Updated**: 2025-11-16
