#!/bin/bash
# Docker Helper Functions for Skill Isolation Tester
# Provides robust command execution with validation, retry logic, and cleanup

# ============================================================================
# Shell Command Validation
# ============================================================================

# Validates shell command syntax before execution
# Usage: validate_shell_command "command string"
# Returns: 0 if valid, 1 if invalid
validate_shell_command() {
    local cmd="$1"

    # Check if command is non-empty
    if [[ -z "$cmd" ]]; then
        echo "ERROR: Empty command provided" >&2
        return 1
    fi

    # Validate syntax using bash -n (dry-run)
    if ! bash -n <<< "$cmd" 2>/dev/null; then
        echo "ERROR: Invalid shell syntax in command:" >&2
        echo "  $cmd" >&2
        return 1
    fi

    return 0
}

# ============================================================================
# Retry Logic for Docker Commands
# ============================================================================

# Executes Docker command with retry logic and exponential backoff
# Usage: retry_docker_command <max_retries> <command> [args...]
# Example: retry_docker_command 3 docker run -it ubuntu:22.04
retry_docker_command() {
    local max_retries="$1"
    shift
    local cmd=("$@")

    local attempt=1
    local wait_time=2

    while [[ $attempt -le $max_retries ]]; do
        echo "Attempt $attempt/$max_retries: ${cmd[*]}"

        if "${cmd[@]}"; then
            echo "✓ Command succeeded on attempt $attempt"
            return 0
        fi

        local exit_code=$?

        if [[ $attempt -lt $max_retries ]]; then
            echo "✗ Command failed with exit code $exit_code"
            echo "  Retrying in ${wait_time}s..."
            sleep "$wait_time"
            wait_time=$((wait_time * 2))  # Exponential backoff
            attempt=$((attempt + 1))
        else
            echo "✗ Command failed after $max_retries attempts (exit code: $exit_code)"
            return "$exit_code"
        fi
    done
}

# ============================================================================
# Cleanup Trap Handler
# ============================================================================

# Cleanup function to be called on script exit
# Usage: Set with trap 'cleanup_on_exit' EXIT
cleanup_on_exit() {
    local exit_code=$?

    echo ""
    echo "=== Cleanup triggered (exit code: $exit_code) ==="

    # Stop and remove test containers
    if [[ -n "$SKILL_TEST_CONTAINER_ID" ]]; then
        echo "Stopping container: $SKILL_TEST_CONTAINER_ID"
        docker stop "$SKILL_TEST_CONTAINER_ID" 2>/dev/null || true

        if [[ "$SKILL_TEST_KEEP_CONTAINER" != "true" ]]; then
            echo "Removing container: $SKILL_TEST_CONTAINER_ID"
            docker rm "$SKILL_TEST_CONTAINER_ID" 2>/dev/null || true
        else
            echo "Keeping container for debugging: docker start -ai $SKILL_TEST_CONTAINER_ID"
        fi
    fi

    # Remove test images (optional)
    if [[ "$SKILL_TEST_REMOVE_IMAGES" == "true" && -n "$SKILL_TEST_IMAGE_NAME" ]]; then
        echo "Removing test image: $SKILL_TEST_IMAGE_NAME"
        docker rmi "$SKILL_TEST_IMAGE_NAME" 2>/dev/null || true
    fi

    # Cleanup temporary files
    if [[ -n "$SKILL_TEST_TEMP_DIR" && -d "$SKILL_TEST_TEMP_DIR" ]]; then
        echo "Removing temporary directory: $SKILL_TEST_TEMP_DIR"
        rm -rf "$SKILL_TEST_TEMP_DIR"
    fi

    echo "=== Cleanup complete ==="

    # Exit with original exit code
    exit "$exit_code"
}

# ============================================================================
# Pre-flight Checks
# ============================================================================

# Validates Docker environment before running tests
# Usage: preflight_check_docker
# Returns: 0 if ready, 1 if not
preflight_check_docker() {
    echo "=== Pre-flight Docker Checks ==="

    # Check Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "✗ ERROR: Docker is not installed"
        echo "  Install from: https://docs.docker.com/get-docker/"
        return 1
    fi
    echo "✓ Docker is installed"

    # Check Docker daemon is running
    if ! docker info > /dev/null 2>&1; then
        echo "✗ ERROR: Docker daemon is not running"
        echo "  Please start Docker Desktop or run: sudo systemctl start docker"
        return 1
    fi
    echo "✓ Docker daemon is running"

    # Check disk space
    local available_space
    available_space=$(df -BG "$HOME" | tail -1 | awk '{print $4}' | sed 's/G//')

    if [[ "$available_space" -lt 2 ]]; then
        echo "⚠ WARNING: Low disk space (${available_space}GB available)"
        echo "  Minimum 2GB recommended for Docker testing"
    else
        echo "✓ Sufficient disk space (${available_space}GB available)"
    fi

    # Check permissions
    if ! docker ps > /dev/null 2>&1; then
        echo "✗ ERROR: Cannot execute Docker commands"
        echo "  You may need to add your user to the docker group:"
        echo "    sudo usermod -aG docker $USER"
        echo "    newgrp docker"
        return 1
    fi
    echo "✓ Docker permissions OK"

    echo "=== Pre-flight checks passed ==="
    return 0
}

# ============================================================================
# Safe Docker Build
# ============================================================================

# Builds Docker image with validation and error handling
# Usage: safe_docker_build <dockerfile_path> <image_name>
safe_docker_build() {
    local dockerfile_path="$1"
    local image_name="$2"

    # Validate inputs
    if [[ ! -f "$dockerfile_path" ]]; then
        echo "ERROR: Dockerfile not found: $dockerfile_path" >&2
        return 1
    fi

    if [[ -z "$image_name" ]]; then
        echo "ERROR: Image name not provided" >&2
        return 1
    fi

    # Validate Dockerfile syntax (basic check)
    if ! grep -q "^FROM " "$dockerfile_path"; then
        echo "ERROR: Invalid Dockerfile (missing FROM directive)" >&2
        return 1
    fi

    # Build with retry
    echo "Building Docker image: $image_name"
    echo "Dockerfile: $dockerfile_path"

    local build_dir
    build_dir=$(dirname "$dockerfile_path")

    retry_docker_command 3 docker build \
        -t "$image_name" \
        -f "$dockerfile_path" \
        "$build_dir"
}

# ============================================================================
# Safe Docker Run
# ============================================================================

# Runs Docker container with validation and resource limits
# Usage: safe_docker_run <image_name> [additional_args...]
safe_docker_run() {
    local image_name="$1"
    shift
    local additional_args=("$@")

    # Validate image exists
    if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${image_name}$"; then
        echo "ERROR: Docker image not found: $image_name" >&2
        echo "Available images:" >&2
        docker images >&2
        return 1
    fi

    # Generate unique container name
    local container_name="skill-test-$(date +%s)"

    # Default resource limits
    local memory_limit="${SKILL_TEST_MEMORY_LIMIT:-512m}"
    local cpu_limit="${SKILL_TEST_CPU_LIMIT:-1.0}"

    echo "Starting container: $container_name"
    echo "Image: $image_name"
    echo "Memory limit: $memory_limit"
    echo "CPU limit: $cpu_limit"

    # Run with retry
    local container_id
    container_id=$(retry_docker_command 3 docker run \
        --name "$container_name" \
        --memory="$memory_limit" \
        --cpus="$cpu_limit" \
        -d \
        "${additional_args[@]}" \
        "$image_name")

    if [[ -n "$container_id" ]]; then
        export SKILL_TEST_CONTAINER_ID="$container_id"
        echo "✓ Container started: $container_id"
        return 0
    else
        echo "✗ Failed to start container"
        return 1
    fi
}

# ============================================================================
# Container Status Check
# ============================================================================

# Checks if container is still running
# Usage: is_container_running <container_id>
is_container_running() {
    local container_id="$1"

    docker inspect -f '{{.State.Running}}' "$container_id" 2>/dev/null | grep -q "true"
}

# Get container exit code
# Usage: get_container_exit_code <container_id>
get_container_exit_code() {
    local container_id="$1"

    docker inspect -f '{{.State.ExitCode}}' "$container_id" 2>/dev/null
}

# ============================================================================
# Usage Example
# ============================================================================

# Example usage in a test script:
#
# #!/bin/bash
# source "$(dirname "$0")/lib/docker-helpers.sh"
#
# # Set cleanup trap
# trap cleanup_on_exit EXIT
#
# # Pre-flight checks
# preflight_check_docker || exit 1
#
# # Set environment variables for cleanup
# export SKILL_TEST_TEMP_DIR="/tmp/skill-test-$$"
# export SKILL_TEST_KEEP_CONTAINER="false"
# export SKILL_TEST_REMOVE_IMAGES="true"
#
# # Build image
# safe_docker_build "$SKILL_TEST_TEMP_DIR/Dockerfile" "skill-test:my-skill" || exit 1
# export SKILL_TEST_IMAGE_NAME="skill-test:my-skill"
#
# # Run container
# safe_docker_run "skill-test:my-skill" bash -c "sleep infinity" || exit 1
#
# # Test passes automatically trigger cleanup via trap
