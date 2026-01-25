#!/bin/bash
# Test Template for Git-Operation Skills
# Use this template when testing skills that:
# - Create commits, branches, or tags
# - Modify git history or configuration
# - Work with git worktrees
# - Interact with remote repositories

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SKILL_NAME="${1:-example-git-skill}"
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

echo "=== Git Skill Test: $SKILL_NAME ==="
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
# Create Test Git Repository
# ============================================================================

echo ""
echo "=== Creating Test Git Repository ==="

mkdir -p "$TEST_DIR/test-repo"
cd "$TEST_DIR/test-repo"

# Initialize git repo
git init
git config user.name "Test User"
git config user.email "test@example.com"

# Create initial commit
echo "# Test Repository" > README.md
echo "Initial content" > file1.txt
git add .
git commit -m "Initial commit"

# Create a branch
git checkout -b feature-branch
echo "Feature content" > feature.txt
git add feature.txt
git commit -m "Add feature"

# Go back to main
git checkout main

# Create a tag
git tag v1.0.0

echo "Test repository created:"
git log --oneline --all --graph
echo ""
git branch -a
echo ""
git tag

# ============================================================================
# Build Test Environment
# ============================================================================

echo ""
echo "=== Building Test Environment ==="

cd "$TEST_DIR"

# Create Dockerfile
cat > "$TEST_DIR/Dockerfile" <<EOF
FROM ubuntu:22.04

# Install git
RUN apt-get update && apt-get install -y \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Configure git
RUN git config --global user.name "Test User" && \\
    git config --global user.email "test@example.com"

# Copy skill
COPY skill/ /root/.claude/skills/$SKILL_NAME/

# Copy test repository
COPY test-repo/ /workspace/

WORKDIR /workspace

CMD ["/bin/bash"]
EOF

# Copy skill
cp -r "$SKILL_PATH" "$TEST_DIR/skill/"

# Build test image
safe_docker_build "$TEST_DIR/Dockerfile" "skill-test:$SKILL_NAME" || {
    echo "ERROR: Failed to build test image"
    exit 1
}

export SKILL_TEST_IMAGE_NAME="skill-test:$SKILL_NAME"

# ============================================================================
# Take "Before" Git Snapshot
# ============================================================================

echo ""
echo "=== Taking Git Snapshot (Before) ==="

# Start container
safe_docker_run "skill-test:$SKILL_NAME" bash -c "sleep infinity" || {
    echo "ERROR: Failed to start test container"
    exit 1
}

# Capture git state before
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /workspace
    git log --all --oneline --graph > /tmp/before-log.txt
    git branch -a > /tmp/before-branches.txt
    git tag > /tmp/before-tags.txt
    git status > /tmp/before-status.txt
    git config --list > /tmp/before-config.txt
" || true

# Copy snapshots out
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/before-log.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/before-branches.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/before-tags.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/before-status.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/before-config.txt" "$TEST_DIR/"

BEFORE_COMMIT_COUNT=$(docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "cd /workspace && git rev-list --all --count")
BEFORE_BRANCH_COUNT=$(wc -l < "$TEST_DIR/before-branches.txt")
BEFORE_TAG_COUNT=$(wc -l < "$TEST_DIR/before-tags.txt")

echo "Before execution:"
echo "  Commits: $BEFORE_COMMIT_COUNT"
echo "  Branches: $BEFORE_BRANCH_COUNT"
echo "  Tags: $BEFORE_TAG_COUNT"

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
    # Example: ./git-skill.sh /workspace
    echo 'Skill execution placeholder - customize this for your skill'
" || {
    EXEC_EXIT_CODE=$?
    echo "ERROR: Skill execution failed with exit code: $EXEC_EXIT_CODE"
    exit "$EXEC_EXIT_CODE"
}

# ============================================================================
# Take "After" Git Snapshot
# ============================================================================

echo ""
echo "=== Taking Git Snapshot (After) ==="

# Capture git state after
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /workspace
    git log --all --oneline --graph > /tmp/after-log.txt
    git branch -a > /tmp/after-branches.txt
    git tag > /tmp/after-tags.txt
    git status > /tmp/after-status.txt
    git config --list > /tmp/after-config.txt
" || true

# Copy snapshots out
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/after-log.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/after-branches.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/after-tags.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/after-status.txt" "$TEST_DIR/"
docker cp "$SKILL_TEST_CONTAINER_ID:/tmp/after-config.txt" "$TEST_DIR/"

AFTER_COMMIT_COUNT=$(docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "cd /workspace && git rev-list --all --count")
AFTER_BRANCH_COUNT=$(wc -l < "$TEST_DIR/after-branches.txt")
AFTER_TAG_COUNT=$(wc -l < "$TEST_DIR/after-tags.txt")

echo "After execution:"
echo "  Commits: $AFTER_COMMIT_COUNT"
echo "  Branches: $AFTER_BRANCH_COUNT"
echo "  Tags: $AFTER_TAG_COUNT"

# ============================================================================
# Analyze Git Changes
# ============================================================================

echo ""
echo "=== Analyzing Git Changes ==="

# New commits
COMMIT_DIFF=$((AFTER_COMMIT_COUNT - BEFORE_COMMIT_COUNT))
if [[ $COMMIT_DIFF -gt 0 ]]; then
    echo "✓ Added $COMMIT_DIFF new commit(s)"

    echo ""
    echo "New commits:"
    docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
        cd /workspace
        git log --oneline -n $COMMIT_DIFF
    "
else
    echo "No new commits created"
fi

# New branches
echo ""
echo "Branch Changes:"
comm -13 "$TEST_DIR/before-branches.txt" "$TEST_DIR/after-branches.txt" > "$TEST_DIR/branches-added.txt"
BRANCH_ADDED=$(wc -l < "$TEST_DIR/branches-added.txt")
if [[ $BRANCH_ADDED -gt 0 ]]; then
    echo "  Added $BRANCH_ADDED branch(es):"
    cat "$TEST_DIR/branches-added.txt"
fi

comm -23 "$TEST_DIR/before-branches.txt" "$TEST_DIR/after-branches.txt" > "$TEST_DIR/branches-removed.txt"
BRANCH_REMOVED=$(wc -l < "$TEST_DIR/branches-removed.txt")
if [[ $BRANCH_REMOVED -gt 0 ]]; then
    echo "  Removed $BRANCH_REMOVED branch(es):"
    cat "$TEST_DIR/branches-removed.txt"
fi

if [[ $BRANCH_ADDED -eq 0 && $BRANCH_REMOVED -eq 0 ]]; then
    echo "  No branch changes"
fi

# New tags
echo ""
echo "Tag Changes:"
comm -13 "$TEST_DIR/before-tags.txt" "$TEST_DIR/after-tags.txt" > "$TEST_DIR/tags-added.txt"
TAG_ADDED=$(wc -l < "$TEST_DIR/tags-added.txt")
if [[ $TAG_ADDED -gt 0 ]]; then
    echo "  Added $TAG_ADDED tag(s):"
    cat "$TEST_DIR/tags-added.txt"
fi

# Config changes
echo ""
echo "Git Config Changes:"
diff "$TEST_DIR/before-config.txt" "$TEST_DIR/after-config.txt" > "$TEST_DIR/config-diff.txt" || true
if [[ -s "$TEST_DIR/config-diff.txt" ]]; then
    echo "  Configuration was modified:"
    cat "$TEST_DIR/config-diff.txt"
else
    echo "  No configuration changes"
fi

# ============================================================================
# Check Working Tree Status
# ============================================================================

echo ""
echo "=== Checking Working Tree Status ==="

UNCOMMITTED_CHANGES=$(docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "cd /workspace && git status --porcelain" || echo "")
if [[ -n "$UNCOMMITTED_CHANGES" ]]; then
    echo "⚠ WARNING: Uncommitted changes detected:"
    echo "$UNCOMMITTED_CHANGES"
    echo ""
    echo "Skills should clean up working tree after execution!"
else
    echo "✓ Working tree is clean"
fi

# ============================================================================
# Validate Git Safety
# ============================================================================

echo ""
echo "=== Git Safety Checks ==="

# Check for force operations in logs
docker logs "$SKILL_TEST_CONTAINER_ID" 2>&1 | grep -i "force\|--force\|-f" > "$TEST_DIR/force-operations.txt" || true
FORCE_OPS=$(wc -l < "$TEST_DIR/force-operations.txt")
if [[ $FORCE_OPS -gt 0 ]]; then
    echo "⚠ WARNING: Detected $FORCE_OPS force operations"
    cat "$TEST_DIR/force-operations.txt"
else
    echo "✓ No force operations detected"
fi

# Check for history rewriting
docker logs "$SKILL_TEST_CONTAINER_ID" 2>&1 | grep -i "rebase\|reset --hard\|filter-branch" > "$TEST_DIR/history-rewrites.txt" || true
REWRITES=$(wc -l < "$TEST_DIR/history-rewrites.txt")
if [[ $REWRITES -gt 0 ]]; then
    echo "⚠ WARNING: Detected $REWRITES history rewrite operations"
    cat "$TEST_DIR/history-rewrites.txt"
else
    echo "✓ No history rewriting detected"
fi

# Check for dangling commits
DANGLING_COMMITS=$(docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "cd /workspace && git fsck --lost-found 2>&1 | grep 'dangling commit'" || echo "")
if [[ -n "$DANGLING_COMMITS" ]]; then
    echo "⚠ WARNING: Dangling commits found (potential data loss)"
    echo "$DANGLING_COMMITS"
else
    echo "✓ No dangling commits"
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
echo "Git Changes Summary:"
echo "  - Commits added: $COMMIT_DIFF"
echo "  - Branches added: $BRANCH_ADDED"
echo "  - Branches removed: $BRANCH_REMOVED"
echo "  - Tags added: $TAG_ADDED"

echo ""
echo "Safety Checklist:"
[[ -z "$UNCOMMITTED_CHANGES" ]] && echo "  ✓ Clean working tree" || echo "  ✗ Uncommitted changes"
[[ $FORCE_OPS -eq 0 ]] && echo "  ✓ No force operations" || echo "  ✗ Force operations detected"
[[ $REWRITES -eq 0 ]] && echo "  ✓ No history rewriting" || echo "  ✗ History rewriting detected"
[[ -z "$DANGLING_COMMITS" ]] && echo "  ✓ No dangling commits" || echo "  ✗ Dangling commits found"

echo ""
echo "Detailed Snapshots:"
echo "  - Before log: $TEST_DIR/before-log.txt"
echo "  - After log: $TEST_DIR/after-log.txt"
echo "  - Branch changes: $TEST_DIR/branches-added.txt"
echo "  - Config diff: $TEST_DIR/config-diff.txt"

# Exit with appropriate code
if [[ $CONTAINER_EXIT_CODE -eq 0 ]]; then
    exit 0
else
    exit 1
fi
