#!/bin/bash
# Test Template for API-Calling Skills
# Use this template when testing skills that:
# - Make HTTP/HTTPS requests to external APIs
# - Require API keys or authentication
# - Need network access
# - Interact with web services

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SKILL_NAME="${1:-example-api-skill}"
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

echo "=== API Skill Test: $SKILL_NAME ==="
echo "Test ID: $TEST_ID"
echo ""

# Validate skill exists
if [[ ! -d "$SKILL_PATH" ]]; then
    echo "ERROR: Skill not found: $SKILL_PATH"
    exit 1
fi

# Validate Docker environment
preflight_check_docker || exit 1

# Check internet connectivity
if ! curl -s --max-time 5 https://www.google.com > /dev/null 2>&1; then
    echo "⚠ WARNING: No internet connectivity detected"
    echo "  API skill may fail if it requires external network access"
fi

# ============================================================================
# Build Test Environment
# ============================================================================

echo ""
echo "=== Building Test Environment ==="

mkdir -p "$TEST_DIR"

# Create test Dockerfile
cat > "$TEST_DIR/Dockerfile" <<EOF
FROM ubuntu:22.04

# Install dependencies for API testing
RUN apt-get update && apt-get install -y \\
    curl \\
    jq \\
    ca-certificates \\
    && rm -rf /var/lib/apt/lists/*

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
# Network Monitoring Setup
# ============================================================================

echo ""
echo "=== Setting Up Network Monitoring ==="

# Create network monitor log
NETWORK_LOG="$TEST_DIR/network-activity.log"
touch "$NETWORK_LOG"

# Start tcpdump in background (if available)
if command -v tcpdump &> /dev/null; then
    echo "Starting network capture..."
    sudo tcpdump -i any -w "$TEST_DIR/network-capture.pcap" &
    TCPDUMP_PID=$!
    echo "tcpdump PID: $TCPDUMP_PID"
else
    echo "tcpdump not available - skipping network capture"
    TCPDUMP_PID=""
fi

# ============================================================================
# Run Skill in Container
# ============================================================================

echo ""
echo "=== Running Skill in Isolated Container ==="

# Start container with DNS configuration
safe_docker_run "skill-test:$SKILL_NAME" \
    --dns 8.8.8.8 \
    --dns 8.8.4.4 \
    bash -c "sleep infinity" || {
    echo "ERROR: Failed to start test container"
    exit 1
}

# Execute skill and capture network activity
echo "Executing skill..."
START_TIME=$(date +%s)

docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /root/.claude/skills/$SKILL_NAME
    # Add your skill execution command here
    # Example: ./api-skill.sh --test-mode
    echo 'Skill execution placeholder - customize this for your skill'

    # Log any curl/wget/http calls made
    if command -v curl &> /dev/null; then
        echo 'curl is available in container'
    fi
    if command -v wget &> /dev/null; then
        echo 'wget is available in container'
    fi
" 2>&1 | tee "$NETWORK_LOG" || {
    EXEC_EXIT_CODE=$?
    echo "ERROR: Skill execution failed with exit code: $EXEC_EXIT_CODE"

    # Stop network capture
    if [[ -n "$TCPDUMP_PID" ]]; then
        sudo kill "$TCPDUMP_PID" 2>/dev/null || true
    fi

    exit "$EXEC_EXIT_CODE"
}

END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))

# Stop network capture
if [[ -n "$TCPDUMP_PID" ]]; then
    sudo kill "$TCPDUMP_PID" 2>/dev/null || true
    echo "Network capture saved to: $TEST_DIR/network-capture.pcap"
fi

# ============================================================================
# Analyze Network Activity
# ============================================================================

echo ""
echo "=== Analyzing Network Activity ==="

# Check for API calls in logs
echo "Searching for HTTP/HTTPS requests..."

API_CALLS=$(grep -iE "http://|https://|curl|wget|GET|POST|PUT|DELETE" "$NETWORK_LOG" || true)

if [[ -n "$API_CALLS" ]]; then
    echo "Detected API calls:"
    echo "$API_CALLS"

    # Extract unique domains
    DOMAINS=$(echo "$API_CALLS" | grep -oE "https?://[^/\"]+" | sort -u || true)
    if [[ -n "$DOMAINS" ]]; then
        echo ""
        echo "Unique API endpoints:"
        echo "$DOMAINS"
    fi
else
    echo "No obvious API calls detected in logs"
fi

# Check container network stats
echo ""
echo "Container network statistics:"
docker stats --no-stream --format "table {{.Name}}\t{{.NetIO}}" "$SKILL_TEST_CONTAINER_ID"

# ============================================================================
# Validate API Key Handling
# ============================================================================

echo ""
echo "=== Validating API Key Security ==="

# Check if API keys appear in logs (security concern)
POTENTIAL_KEYS=$(grep -iE "api[-_]?key|token|secret|password|bearer" "$NETWORK_LOG" | grep -v "API_KEY=" || true)

if [[ -n "$POTENTIAL_KEYS" ]]; then
    echo "⚠ WARNING: Potential API keys/secrets found in logs:"
    echo "$POTENTIAL_KEYS"
    echo ""
    echo "SECURITY ISSUE: API keys should NOT appear in logs!"
    echo "  - Use environment variables instead"
    echo "  - Redact sensitive data in log output"
fi

# Check for hardcoded endpoints
HARDCODED_URLS=$(grep -rn "http://" "$SKILL_PATH" 2>/dev/null | grep -v "example.com" || true)
if [[ -n "$HARDCODED_URLS" ]]; then
    echo "⚠ WARNING: Hardcoded HTTP URLs found (should use HTTPS):"
    echo "$HARDCODED_URLS"
fi

# ============================================================================
# Rate Limiting Check
# ============================================================================

echo ""
echo "=== Checking Rate Limiting Behavior ==="

# Count number of requests made
REQUEST_COUNT=$(grep -icE "GET|POST|PUT|DELETE" "$NETWORK_LOG" || echo "0")
echo "Total HTTP requests detected: $REQUEST_COUNT"

if [[ $REQUEST_COUNT -gt 100 ]]; then
    echo "⚠ WARNING: High number of API requests ($REQUEST_COUNT)"
    echo "  - Consider implementing rate limiting"
    echo "  - Use caching to reduce API calls"
    echo "  - Check for request loops"
fi

REQUESTS_PER_SECOND=$((REQUEST_COUNT / EXECUTION_TIME))
echo "Requests per second: $REQUESTS_PER_SECOND"

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
echo "Summary:"
echo "  - Exit code: $CONTAINER_EXIT_CODE"
echo "  - Execution time: ${EXECUTION_TIME}s"
echo "  - API requests: $REQUEST_COUNT"
echo "  - Network log: $NETWORK_LOG"

echo ""
echo "Security Checklist:"
if [[ -z "$POTENTIAL_KEYS" ]]; then
    echo "  ✓ No API keys in logs"
else
    echo "  ✗ API keys found in logs"
fi

if [[ -z "$HARDCODED_URLS" ]]; then
    echo "  ✓ No hardcoded HTTP URLs"
else
    echo "  ✗ Hardcoded HTTP URLs found"
fi

if [[ $REQUEST_COUNT -lt 100 ]]; then
    echo "  ✓ Reasonable request volume"
else
    echo "  ✗ High request volume"
fi

echo ""
echo "Recommendations:"
echo "  - Document all external API dependencies"
echo "  - Implement request caching where possible"
echo "  - Use exponential backoff for retries"
echo "  - Respect API rate limits"
echo "  - Use HTTPS for all API calls"
echo "  - Never log API keys or secrets"

# Exit with appropriate code
if [[ $CONTAINER_EXIT_CODE -eq 0 ]]; then
    exit 0
else
    exit 1
fi
