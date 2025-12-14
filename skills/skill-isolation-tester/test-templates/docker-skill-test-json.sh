#!/bin/bash
# Test Template for Docker-Based Skills with JSON Output
# This is an enhanced version of docker-skill-test.sh with CI/CD integration

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SKILL_NAME="${1:-example-docker-skill}"
SKILL_PATH="$HOME/.claude/skills/$SKILL_NAME"
TEST_ID="$(date +%s)"
TEST_DIR="/tmp/skill-test-$TEST_ID"

# JSON reporting
export JSON_REPORT_FILE="$TEST_DIR/test-report.json"
export JSON_ENABLED="${JSON_ENABLED:-true}"

# ============================================================================
# Load Helper Libraries
# ============================================================================

HELPER_LIB="$HOME/.claude/skills/skill-isolation-tester/lib/docker-helpers.sh"
JSON_LIB="$HOME/.claude/skills/skill-isolation-tester/lib/json-reporter.sh"

if [[ ! -f "$HELPER_LIB" ]]; then
    echo "ERROR: Helper library not found: $HELPER_LIB"
    exit 1
fi

if [[ ! -f "$JSON_LIB" ]]; then
    echo "ERROR: JSON reporter library not found: $JSON_LIB"
    exit 1
fi

# shellcheck source=/dev/null
source "$HELPER_LIB"
# shellcheck source=/dev/null
source "$JSON_LIB"

# ============================================================================
# Setup Cleanup Trap
# ============================================================================

export SKILL_TEST_TEMP_DIR="$TEST_DIR"
export SKILL_TEST_KEEP_CONTAINER="false"
export SKILL_TEST_REMOVE_IMAGES="true"

cleanup_and_finalize() {
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))

    # Finalize JSON report
    if [[ "$JSON_ENABLED" == "true" ]]; then
        json_finalize "$exit_code" "$duration"
        export_all_formats "$TEST_DIR/test-report"
    fi

    # Standard cleanup
    cleanup_on_exit

    exit "$exit_code"
}

trap cleanup_and_finalize EXIT

# ============================================================================
# Pre-flight Checks
# ============================================================================

echo "=== Docker Skill Test (JSON Mode): $SKILL_NAME ==="
echo "Test ID: $TEST_ID"
echo ""

# Create test directory
mkdir -p "$TEST_DIR"

# Initialize JSON report
if [[ "$JSON_ENABLED" == "true" ]]; then
    json_init "docker-skill-test" "$SKILL_NAME"
fi

# Validate skill exists
if [[ ! -d "$SKILL_PATH" ]]; then
    echo "ERROR: Skill not found: $SKILL_PATH"
    [[ "$JSON_ENABLED" == "true" ]] && json_add_issue "error" "setup" "Skill directory not found: $SKILL_PATH"
    exit 1
fi

# Validate Docker environment
if ! preflight_check_docker; then
    [[ "$JSON_ENABLED" == "true" ]] && json_add_issue "error" "environment" "Docker pre-flight checks failed"
    exit 1
fi

# ============================================================================
# Baseline Measurements (Before)
# ============================================================================

echo ""
echo "=== Taking Baseline Measurements ==="

START_TIME=$(date +%s)

BEFORE_CONTAINERS=$(docker ps -a --format '{{.ID}}' | wc -l)
BEFORE_IMAGES=$(docker images --format '{{.ID}}' | wc -l)
BEFORE_VOLUMES=$(docker volume ls --format '{{.Name}}' | wc -l)
BEFORE_NETWORKS=$(docker network ls --format '{{.ID}}' | wc -l)

echo "Before test:"
echo "  Containers: $BEFORE_CONTAINERS"
echo "  Images: $BEFORE_IMAGES"
echo "  Volumes: $BEFORE_VOLUMES"
echo "  Networks: $BEFORE_NETWORKS"

# Record baseline in JSON
if [[ "$JSON_ENABLED" == "true" ]]; then
    json_add_metric "baseline_containers" "$BEFORE_CONTAINERS"
    json_add_metric "baseline_images" "$BEFORE_IMAGES"
    json_add_metric "baseline_volumes" "$BEFORE_VOLUMES"
    json_add_metric "baseline_networks" "$BEFORE_NETWORKS"
fi

# ============================================================================
# Build Test Environment
# ============================================================================

echo ""
echo "=== Building Test Environment ==="

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
BUILD_START=$(date +%s)
if ! safe_docker_build "$TEST_DIR/Dockerfile" "skill-test:$SKILL_NAME"; then
    echo "ERROR: Failed to build test image"
    [[ "$JSON_ENABLED" == "true" ]] && json_add_issue "error" "build" "Docker image build failed"
    exit 1
fi
BUILD_END=$(date +%s)
BUILD_DURATION=$((BUILD_END - BUILD_START))

export SKILL_TEST_IMAGE_NAME="skill-test:$SKILL_NAME"

# Record build metrics
if [[ "$JSON_ENABLED" == "true" ]]; then
    json_add_metric "build_duration_seconds" "$BUILD_DURATION" "seconds"
fi

# ============================================================================
# Run Skill in Container
# ============================================================================

echo ""
echo "=== Running Skill in Isolated Container ==="

# Start container with Docker socket access
if ! safe_docker_run "skill-test:$SKILL_NAME" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    bash -c "sleep infinity"; then
    echo "ERROR: Failed to start test container"
    [[ "$JSON_ENABLED" == "true" ]] && json_add_issue "error" "runtime" "Container failed to start"
    exit 1
fi

# Execute skill
echo "Executing skill..."
EXEC_START=$(date +%s)

EXEC_OUTPUT=$(docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /root/.claude/skills/$SKILL_NAME
    echo 'Skill execution placeholder - customize this for your skill'
" 2>&1) || {
    EXEC_EXIT_CODE=$?
    echo "ERROR: Skill execution failed with exit code: $EXEC_EXIT_CODE"
    [[ "$JSON_ENABLED" == "true" ]] && json_add_issue "error" "execution" "Skill failed with exit code $EXEC_EXIT_CODE"
    exit "$EXEC_EXIT_CODE"
}

EXEC_END=$(date +%s)
EXEC_DURATION=$((EXEC_END - EXEC_START))

# Record execution metrics
if [[ "$JSON_ENABLED" == "true" ]]; then
    json_add_metric "execution_duration_seconds" "$EXEC_DURATION" "seconds"
fi

# ============================================================================
# Collect Measurements (After)
# ============================================================================

echo ""
echo "=== Collecting Post-Execution Measurements ==="

sleep 2  # Wait for async operations

AFTER_CONTAINERS=$(docker ps -a --format '{{.ID}}' | wc -l)
AFTER_IMAGES=$(docker images --format '{{.ID}}' | wc -l)
AFTER_VOLUMES=$(docker volume ls --format '{{.Name}}' | wc -l)
AFTER_NETWORKS=$(docker network ls --format '{{.ID}}' | wc -l)

CONTAINERS_DELTA=$((AFTER_CONTAINERS - BEFORE_CONTAINERS))
IMAGES_DELTA=$((AFTER_IMAGES - BEFORE_IMAGES))
VOLUMES_DELTA=$((AFTER_VOLUMES - BEFORE_VOLUMES))
NETWORKS_DELTA=$((AFTER_NETWORKS - BEFORE_NETWORKS))

echo "After test:"
echo "  Containers: $AFTER_CONTAINERS (delta: $CONTAINERS_DELTA)"
echo "  Images: $AFTER_IMAGES (delta: $IMAGES_DELTA)"
echo "  Volumes: $AFTER_VOLUMES (delta: $VOLUMES_DELTA)"
echo "  Networks: $AFTER_NETWORKS (delta: $NETWORKS_DELTA)"

# Record changes in JSON
if [[ "$JSON_ENABLED" == "true" ]]; then
    json_add_metric "containers_created" "$CONTAINERS_DELTA"
    json_add_metric "images_created" "$IMAGES_DELTA"
    json_add_metric "volumes_created" "$VOLUMES_DELTA"
    json_add_metric "networks_created" "$NETWORKS_DELTA"
fi

# ============================================================================
# Validate Cleanup Behavior
# ============================================================================

echo ""
echo "=== Validating Skill Cleanup ==="

# Check for orphaned containers
ORPHANED_CONTAINERS=$(docker ps -a --filter "label=created-by-skill=$SKILL_NAME" --format '{{.ID}}' | wc -l)
if [[ $ORPHANED_CONTAINERS -gt 0 ]]; then
    echo "⚠ WARNING: Skill left $ORPHANED_CONTAINERS orphaned container(s)"
    if [[ "$JSON_ENABLED" == "true" ]]; then
        json_add_issue "warning" "cleanup" "Found $ORPHANED_CONTAINERS orphaned containers"
        json_add_recommendation "Cleanup" "Implement automatic container cleanup in skill"
    fi
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
    [[ "$JSON_ENABLED" == "true" ]] && json_add_issue "error" "test-failure" "Container exited with code $CONTAINER_EXIT_CODE"
fi

echo ""
echo "Summary:"
echo "  - Exit code: $CONTAINER_EXIT_CODE"
echo "  - Build duration: ${BUILD_DURATION}s"
echo "  - Execution duration: ${EXEC_DURATION}s"
echo "  - Docker resources created: $CONTAINERS_DELTA containers, $IMAGES_DELTA images, $VOLUMES_DELTA volumes, $NETWORKS_DELTA networks"

if [[ "$JSON_ENABLED" == "true" ]]; then
    echo ""
    echo "JSON reports will be generated at:"
    echo "  - $TEST_DIR/test-report.json"
    echo "  - $TEST_DIR/test-report.junit.xml"
    echo "  - $TEST_DIR/test-report.md"
fi

# Exit with appropriate code (cleanup_and_finalize will handle JSON)
if [[ $CONTAINER_EXIT_CODE -eq 0 ]]; then
    exit 0
else
    exit 1
fi
