#!/bin/bash
# Test Template for Docker-Based Skills
# Use this template when testing skills that:
# - Start Docker containers
# - Build Docker images
# - Manage Docker volumes/networks
# - Require Docker daemon access

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SKILL_NAME="${1:-example-docker-skill}"
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

echo "=== Docker Skill Test: $SKILL_NAME ==="
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
# Baseline Measurements (Before)
# ============================================================================

echo ""
echo "=== Taking Baseline Measurements ==="

# Count Docker resources before test
BEFORE_CONTAINERS=$(docker ps -a --format '{{.ID}}' | wc -l)
BEFORE_IMAGES=$(docker images --format '{{.ID}}' | wc -l)
BEFORE_VOLUMES=$(docker volume ls --format '{{.Name}}' | wc -l)
BEFORE_NETWORKS=$(docker network ls --format '{{.ID}}' | wc -l)

echo "Before test:"
echo "  Containers: $BEFORE_CONTAINERS"
echo "  Images: $BEFORE_IMAGES"
echo "  Volumes: $BEFORE_VOLUMES"
echo "  Networks: $BEFORE_NETWORKS"

# ============================================================================
# Build Test Environment
# ============================================================================

echo ""
echo "=== Building Test Environment ==="

mkdir -p "$TEST_DIR"

# Create test Dockerfile
cat > "$TEST_DIR/Dockerfile" <<EOF
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    git \\
    nodejs \\
    npm \\
    docker.io \\
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code (mock for testing)
RUN mkdir -p /root/.claude/skills

# Copy skill under test
COPY skill/ /root/.claude/skills/$SKILL_NAME/

WORKDIR /root

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
# Run Skill in Container
# ============================================================================

echo ""
echo "=== Running Skill in Isolated Container ==="

# Start container with Docker socket access (for Docker-in-Docker skills)
safe_docker_run "skill-test:$SKILL_NAME" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    bash -c "sleep infinity" || {
    echo "ERROR: Failed to start test container"
    exit 1
}

# Execute skill (customize this command based on your skill's interface)
echo "Executing skill..."
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /root/.claude/skills/$SKILL_NAME
    # Add your skill execution command here
    # Example: ./skill.sh test-mode
    echo 'Skill execution placeholder - customize this for your skill'
" || {
    EXEC_EXIT_CODE=$?
    echo "ERROR: Skill execution failed with exit code: $EXEC_EXIT_CODE"
    exit "$EXEC_EXIT_CODE"
}

# ============================================================================
# Collect Measurements (After)
# ============================================================================

echo ""
echo "=== Collecting Post-Execution Measurements ==="

# Wait for async operations to complete
sleep 2

AFTER_CONTAINERS=$(docker ps -a --format '{{.ID}}' | wc -l)
AFTER_IMAGES=$(docker images --format '{{.ID}}' | wc -l)
AFTER_VOLUMES=$(docker volume ls --format '{{.Name}}' | wc -l)
AFTER_NETWORKS=$(docker network ls --format '{{.ID}}' | wc -l)

echo "After test:"
echo "  Containers: $AFTER_CONTAINERS (delta: $((AFTER_CONTAINERS - BEFORE_CONTAINERS)))"
echo "  Images: $AFTER_IMAGES (delta: $((AFTER_IMAGES - BEFORE_IMAGES)))"
echo "  Volumes: $AFTER_VOLUMES (delta: $((AFTER_VOLUMES - BEFORE_VOLUMES)))"
echo "  Networks: $AFTER_NETWORKS (delta: $((AFTER_NETWORKS - BEFORE_NETWORKS)))"

# ============================================================================
# Validate Cleanup Behavior
# ============================================================================

echo ""
echo "=== Validating Skill Cleanup ==="

# Check for orphaned containers
ORPHANED_CONTAINERS=$(docker ps -a --filter "label=created-by-skill=$SKILL_NAME" --format '{{.ID}}' | wc -l)
if [[ $ORPHANED_CONTAINERS -gt 0 ]]; then
    echo "⚠ WARNING: Skill left $ORPHANED_CONTAINERS orphaned container(s)"
    docker ps -a --filter "label=created-by-skill=$SKILL_NAME"
fi

# Check for unlabeled containers (potential orphans)
SKILL_CONTAINERS=$(docker ps -a --filter "name=$SKILL_NAME" --format '{{.ID}}' | wc -l)
if [[ $SKILL_CONTAINERS -gt 1 ]]; then
    echo "⚠ WARNING: Found $SKILL_CONTAINERS containers with skill name pattern"
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
    echo ""
    echo "Summary:"
    echo "  - Skill executed successfully"
    echo "  - Exit code: 0"
    echo "  - Container cleanup: Will be handled by trap"
else
    echo "❌ TEST FAILED"
    echo ""
    echo "Summary:"
    echo "  - Skill execution failed"
    echo "  - Exit code: $CONTAINER_EXIT_CODE"
    echo "  - Check logs: docker logs $SKILL_TEST_CONTAINER_ID"
fi

echo ""
echo "Docker Resources Created:"
echo "  - Containers: $((AFTER_CONTAINERS - BEFORE_CONTAINERS))"
echo "  - Images: $((AFTER_IMAGES - BEFORE_IMAGES))"
echo "  - Volumes: $((AFTER_VOLUMES - BEFORE_VOLUMES))"
echo "  - Networks: $((AFTER_NETWORKS - BEFORE_NETWORKS))"

echo ""
echo "Cleanup Instructions:"
echo "  - Test container will be removed automatically"
echo "  - To manually clean up: docker rm -f $SKILL_TEST_CONTAINER_ID"
echo "  - To remove test image: docker rmi skill-test:$SKILL_NAME"

# Exit with appropriate code
if [[ $CONTAINER_EXIT_CODE -eq 0 ]]; then
    exit 0
else
    exit 1
fi
