#!/bin/bash
# Test Template for File-Manipulation Skills
# Use this template when testing skills that:
# - Create, read, update, or delete files
# - Modify configurations or codebases
# - Generate reports or artifacts
# - Work with filesystem operations

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SKILL_NAME="${1:-example-file-skill}"
SKILL_PATH="$HOME/.claude/skills/$SKILL_NAME"
TEST_ID="$(date +%s)"
TEST_DIR="/tmp/skill-test-$TEST_ID"

# ============================================================================
# Load Helper Library
# ============================================================================

HELPER_LIB="$HOME/.claude/skills/skill-isolation-tester/lib/docker-helpers.sh"
if [[ ! -f "$HELPER_LIB" ]]; then
    echo "ERROR: Helper library not found: $HELPER_LIB"
    exit 1
fi

# shellcheck source=/dev/null
source "$HELPER_LIB"

# ============================================================================
# Setup Cleanup Trap
# ============================================================================

export SKILL_TEST_TEMP_DIR="$TEST_DIR"
export SKILL_TEST_KEEP_CONTAINER="false"
export SKILL_TEST_REMOVE_IMAGES="true"

trap cleanup_on_exit EXIT

# ============================================================================
# Pre-flight Checks
# ============================================================================

echo "=== File Manipulation Skill Test: $SKILL_NAME ==="
echo "Test ID: $TEST_ID"
echo ""

# Validate skill exists
if [[ ! -d "$SKILL_PATH" ]]; then
    echo "ERROR: Skill not found: $SKILL_PATH"
    exit 1
fi

# Validate Docker environment
preflight_check_docker || exit 1

# ============================================================================
# Build Test Environment with Sample Files
# ============================================================================

echo ""
echo "=== Building Test Environment ==="

mkdir -p "$TEST_DIR/test-workspace"

# Create sample files for the skill to manipulate
cat > "$TEST_DIR/test-workspace/sample.txt" <<'EOF'
This is a sample text file for testing.
Line 2
Line 3
EOF

cat > "$TEST_DIR/test-workspace/config.json" <<'EOF'
{
  "setting1": "value1",
  "setting2": 42,
  "enabled": true
}
EOF

mkdir -p "$TEST_DIR/test-workspace/subdir"
echo "Nested file" > "$TEST_DIR/test-workspace/subdir/nested.txt"

# Create Dockerfile
cat > "$TEST_DIR/Dockerfile" <<EOF
FROM ubuntu:22.04

# Install file manipulation tools
RUN apt-get update && apt-get install -y \\
    coreutils \\
    jq \\
    tree \\
    && rm -rf /var/lib/apt/lists/*

# Create workspace
RUN mkdir -p /workspace

# Copy skill
COPY skill/ /root/.claude/skills/$SKILL_NAME/

# Copy test files
COPY test-workspace/ /workspace/

WORKDIR /workspace

CMD ["/bin/bash"]
EOF

# Copy skill to test directory
cp -r "$SKILL_PATH" "$TEST_DIR/skill/"

# Build test image
safe_docker_build "$TEST_DIR/Dockerfile" "skill-test:$SKILL_NAME" || {
    echo "ERROR: Failed to build test image"
    exit 1
}

export SKILL_TEST_IMAGE_NAME="skill-test:$SKILL_NAME"

# ============================================================================
# Take "Before" Filesystem Snapshot
# ============================================================================

echo ""
echo "=== Taking Filesystem Snapshot (Before) ==="

# Start container
safe_docker_run "skill-test:$SKILL_NAME" bash -c "sleep infinity" || {
    echo "ERROR: Failed to start test container"
    exit 1
}

# Get baseline file list
docker exec "$SKILL_TEST_CONTAINER_ID" find /workspace -type f -o -type d | sort > "$TEST_DIR/before-files.txt"

# Get file sizes and checksums
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /workspace
    find . -type f -exec md5sum {} \; | sort
" > "$TEST_DIR/before-checksums.txt"

# Count files
BEFORE_FILE_COUNT=$(docker exec "$SKILL_TEST_CONTAINER_ID" find /workspace -type f | wc -l)
BEFORE_DIR_COUNT=$(docker exec "$SKILL_TEST_CONTAINER_ID" find /workspace -type d | wc -l)

echo "Before execution:"
echo "  Files: $BEFORE_FILE_COUNT"
echo "  Directories: $BEFORE_DIR_COUNT"

# ============================================================================
# Run Skill in Container
# ============================================================================

echo ""
echo "=== Running Skill in Isolated Container ==="

# Execute skill
echo "Executing skill..."
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /root/.claude/skills/$SKILL_NAME
    # Add your skill execution command here
    # Example: ./file-processor.sh /workspace
    echo 'Skill execution placeholder - customize this for your skill'
" || {
    EXEC_EXIT_CODE=$?
    echo "ERROR: Skill execution failed with exit code: $EXEC_EXIT_CODE"
    exit "$EXEC_EXIT_CODE"
}

# ============================================================================
# Take "After" Filesystem Snapshot
# ============================================================================

echo ""
echo "=== Taking Filesystem Snapshot (After) ==="

# Get updated file list
docker exec "$SKILL_TEST_CONTAINER_ID" find /workspace -type f -o -type d | sort > "$TEST_DIR/after-files.txt"

# Get updated checksums
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /workspace
    find . -type f -exec md5sum {} \; | sort
" > "$TEST_DIR/after-checksums.txt"

# Count files
AFTER_FILE_COUNT=$(docker exec "$SKILL_TEST_CONTAINER_ID" find /workspace -type f | wc -l)
AFTER_DIR_COUNT=$(docker exec "$SKILL_TEST_CONTAINER_ID" find /workspace -type d | wc -l)

echo "After execution:"
echo "  Files: $AFTER_FILE_COUNT"
echo "  Directories: $AFTER_DIR_COUNT"

# ============================================================================
# Analyze Filesystem Changes
# ============================================================================

echo ""
echo "=== Analyzing Filesystem Changes ==="

# Files added
echo ""
echo "Files Added:"
comm -13 "$TEST_DIR/before-files.txt" "$TEST_DIR/after-files.txt" > "$TEST_DIR/files-added.txt"
ADDED_COUNT=$(wc -l < "$TEST_DIR/files-added.txt")
echo "  Count: $ADDED_COUNT"
if [[ $ADDED_COUNT -gt 0 ]]; then
    head -10 "$TEST_DIR/files-added.txt"
    if [[ $ADDED_COUNT -gt 10 ]]; then
        echo "  ... and $((ADDED_COUNT - 10)) more"
    fi
fi

# Files removed
echo ""
echo "Files Removed:"
comm -23 "$TEST_DIR/before-files.txt" "$TEST_DIR/after-files.txt" > "$TEST_DIR/files-removed.txt"
REMOVED_COUNT=$(wc -l < "$TEST_DIR/files-removed.txt")
echo "  Count: $REMOVED_COUNT"
if [[ $REMOVED_COUNT -gt 0 ]]; then
    head -10 "$TEST_DIR/files-removed.txt"
    if [[ $REMOVED_COUNT -gt 10 ]]; then
        echo "  ... and $((REMOVED_COUNT - 10)) more"
    fi
fi

# Files modified
echo ""
echo "Files Modified:"
comm -12 "$TEST_DIR/before-files.txt" "$TEST_DIR/after-files.txt" | while read -r file; do
    BEFORE_HASH=$(grep "$file" "$TEST_DIR/before-checksums.txt" 2>/dev/null | awk '{print $1}' || echo "")
    AFTER_HASH=$(grep "$file" "$TEST_DIR/after-checksums.txt" 2>/dev/null | awk '{print $1}' || echo "")

    if [[ -n "$BEFORE_HASH" && -n "$AFTER_HASH" && "$BEFORE_HASH" != "$AFTER_HASH" ]]; then
        echo "  $file"
    fi
done | tee "$TEST_DIR/files-modified.txt"
MODIFIED_COUNT=$(wc -l < "$TEST_DIR/files-modified.txt")
echo "  Count: $MODIFIED_COUNT"

# ============================================================================
# Validate File Permissions
# ============================================================================

echo ""
echo "=== Checking File Permissions ==="

# Find files with unusual permissions
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    find /workspace -type f -perm /111 -ls
" > "$TEST_DIR/executable-files.txt" || true

EXECUTABLE_COUNT=$(wc -l < "$TEST_DIR/executable-files.txt")
if [[ $EXECUTABLE_COUNT -gt 0 ]]; then
    echo "⚠ WARNING: Found $EXECUTABLE_COUNT executable files"
    cat "$TEST_DIR/executable-files.txt"
else
    echo "✓ No unexpected executable files"
fi

# Check for world-writable files
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    find /workspace -type f -perm -002 -ls
" > "$TEST_DIR/world-writable-files.txt" || true

WRITABLE_COUNT=$(wc -l < "$TEST_DIR/world-writable-files.txt")
if [[ $WRITABLE_COUNT -gt 0 ]]; then
    echo "⚠ WARNING: Found $WRITABLE_COUNT world-writable files (security risk)"
    cat "$TEST_DIR/world-writable-files.txt"
else
    echo "✓ No world-writable files"
fi

# ============================================================================
# Check for Sensitive Data
# ============================================================================

echo ""
echo "=== Scanning for Sensitive Data ==="

# Check for potential secrets in new files
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    grep -rni 'password\|api[-_]key\|secret\|token' /workspace
" 2>/dev/null | tee "$TEST_DIR/potential-secrets.txt" || true

SECRET_COUNT=$(wc -l < "$TEST_DIR/potential-secrets.txt")
if [[ $SECRET_COUNT -gt 0 ]]; then
    echo "⚠ WARNING: Found $SECRET_COUNT lines with potential secrets"
    echo "  Review: $TEST_DIR/potential-secrets.txt"
else
    echo "✓ No obvious secrets detected"
fi

# ============================================================================
# Validate Cleanup Behavior
# ============================================================================

echo ""
echo "=== Validating Cleanup Behavior ==="

# Check for leftover temp files
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    find /tmp -name '*skill*' -o -name '*.tmp' -o -name '*.temp'
" > "$TEST_DIR/temp-files.txt" || true

TEMP_COUNT=$(wc -l < "$TEST_DIR/temp-files.txt")
if [[ $TEMP_COUNT -gt 0 ]]; then
    echo "⚠ WARNING: Found $TEMP_COUNT leftover temp files"
    cat "$TEST_DIR/temp-files.txt"
else
    echo "✓ No leftover temp files"
fi

# ============================================================================
# Generate Test Report
# ============================================================================

echo ""
echo "=== Test Report ==="
echo ""

CONTAINER_EXIT_CODE=$(get_container_exit_code "$SKILL_TEST_CONTAINER_ID")

if [[ $CONTAINER_EXIT_CODE -eq 0 ]]; then
    echo "✅ TEST PASSED"
else
    echo "❌ TEST FAILED"
fi

echo ""
echo "Filesystem Changes Summary:"
echo "  - Files added: $ADDED_COUNT"
echo "  - Files removed: $REMOVED_COUNT"
echo "  - Files modified: $MODIFIED_COUNT"
echo "  - Total file count change: $((AFTER_FILE_COUNT - BEFORE_FILE_COUNT))"

echo ""
echo "Security & Quality Checklist:"
[[ $EXECUTABLE_COUNT -eq 0 ]] && echo "  ✓ No unexpected executable files" || echo "  ✗ Found executable files"
[[ $WRITABLE_COUNT -eq 0 ]] && echo "  ✓ No world-writable files" || echo "  ✗ Found world-writable files"
[[ $SECRET_COUNT -eq 0 ]] && echo "  ✓ No secrets in files" || echo "  ✗ Potential secrets found"
[[ $TEMP_COUNT -eq 0 ]] && echo "  ✓ Clean temp directory" || echo "  ✗ Leftover temp files"

echo ""
echo "Detailed Reports:"
echo "  - Files added: $TEST_DIR/files-added.txt"
echo "  - Files removed: $TEST_DIR/files-removed.txt"
echo "  - Files modified: $TEST_DIR/files-modified.txt"
echo "  - Before snapshot: $TEST_DIR/before-files.txt"
echo "  - After snapshot: $TEST_DIR/after-files.txt"

# Exit with appropriate code
if [[ $CONTAINER_EXIT_CODE -eq 0 ]]; then
    exit 0
else
    exit 1
fi
