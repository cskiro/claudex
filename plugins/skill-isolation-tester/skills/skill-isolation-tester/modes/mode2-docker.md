# Mode 2: Docker Container Isolation

## Using Docker Helper Library

**RECOMMENDED:** Use the helper library for robust error handling and cleanup.

```bash
source ~/.claude/skills/skill-isolation-tester/lib/docker-helpers.sh

# Set cleanup trap (runs automatically on exit)
trap cleanup_on_exit EXIT

# Pre-flight checks
preflight_check_docker || exit 1
```

The helper library provides:
- Shell command validation (prevents syntax errors)
- Retry logic with exponential backoff
- Automatic cleanup on exit
- Pre-flight Docker environment checks
- Safe build and run functions

See `lib/docker-helpers.sh` for full documentation.

---

## When to Use

**Best for:**
- Skills that install npm/pip packages or system dependencies
- Skills that modify configuration files
- Medium-risk skills that need OS-level isolation
- Testing skills with different Claude Code versions
- Reproducible testing environments

**Not suitable for:**
- Skills that require VM operations or nested virtualization
- Skills that need GUI access (without X11 forwarding)
- Extremely high-risk skills (use VM mode instead)

**Risk Level**: Low to medium complexity skills

## Advantages

- 🏗️ **True OS Isolation**: Complete filesystem and process separation
- 📦 **Reproducible**: Same environment every time
- 🔒 **Sandboxed**: Limited access to host system
- 🎯 **Precise**: Control exactly what's installed
- 🗑️ **Clean**: Easy to destroy and recreate

## Limitations

- ⏱️ Slower than git worktree (container overhead)
- 💾 Requires disk space for images
- 🐳 Requires Docker installation and running daemon
- ⚙️ More complex setup than worktree
- 🔧 May need volume mounts for file access

## Prerequisites

1. Docker installed and running (`docker info`)
2. Sufficient disk space (~1GB for base image + skill)
3. Permissions to run Docker commands
4. Internet connection (first time only, to pull images)

## Workflow

### Step 1: Validate Docker Environment

```bash
# Check Docker is installed
command -v docker || { echo "Docker not installed"; exit 1; }

# Check Docker daemon is running
docker info > /dev/null 2>&1 || { echo "Docker daemon not running"; exit 1; }

# Check disk space
docker system df
```

### Step 2: Choose Base Image

**Options:**
1. **claude-code-base** (preferred if available)
   - Pre-built image with Claude Code installed
   - Fastest startup time

2. **ubuntu:22.04** (fallback)
   - Install Claude Code manually
   - More control over environment

**Check if custom image exists:**
```bash
docker images | grep claude-code-base
```

### Step 3: Prepare Skill for Container

**Create temporary directory:**
```bash
TEST_DIR="/tmp/skill-test-$(date +%s)"
mkdir -p "$TEST_DIR"

# Copy skill to test directory
cp -r ~/.claude/skills/[skill-name] "$TEST_DIR/"

# Create Dockerfile
cat > "$TEST_DIR/Dockerfile" <<'EOF'
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code (adjust version as needed)
RUN npm install -g @anthropic/claude-code

# Create directory structure
RUN mkdir -p /root/.claude/skills

# Copy skill
COPY [skill-name]/ /root/.claude/skills/[skill-name]/

# Set working directory
WORKDIR /root

# Default command
CMD ["/bin/bash"]
EOF
```

### Step 4: Build Docker Image

```bash
cd "$TEST_DIR"

# Build image with tag
docker build -t skill-test:[skill-name] .

# Verify build succeeded
docker images | grep skill-test
```

**Expected build time:** 2-5 minutes (first time), < 30s (cached)

### Step 5: Take "Before" Snapshot

**Create container (don't start yet):**
```bash
CONTAINER_ID=$(docker create \
  --name skill-test-$(date +%s) \
  --memory="512m" \
  --cpus="1.0" \
  skill-test:[skill-name])

echo "Container ID: $CONTAINER_ID"
```

**Snapshot filesystem:**
```bash
docker export $CONTAINER_ID | tar -t > /tmp/before-files.txt
```

### Step 6: Run Skill in Container

**Start container interactively:**
```bash
docker start -ai $CONTAINER_ID
```

**Or run with test command:**
```bash
docker run -it \
  --name skill-test \
  --rm \
  --memory="512m" \
  --cpus="1.0" \
  skill-test:[skill-name] \
  bash -c "claude skill run [skill-name] --test"
```

**Monitor execution:**
```bash
# In another terminal, watch resource usage
docker stats $CONTAINER_ID

# Watch logs
docker logs -f $CONTAINER_ID
```

### Step 7: Take "After" Snapshot

**Commit container state:**
```bash
docker commit $CONTAINER_ID skill-test:[skill-name]-after
```

**Export and compare files:**
```bash
# Export after state
docker export $CONTAINER_ID | tar -t > /tmp/after-files.txt

# Find differences
diff /tmp/before-files.txt /tmp/after-files.txt > /tmp/file-changes.txt

# Count changes
echo "Files added: $(grep ">" /tmp/file-changes.txt | wc -l)"
echo "Files removed: $(grep "<" /tmp/file-changes.txt | wc -l)"
```

**Check for running processes:**
```bash
docker exec $CONTAINER_ID ps aux > /tmp/processes.txt
```

### Step 8: Analyze Results

**Extract skill logs:**
```bash
docker logs $CONTAINER_ID > /tmp/skill-execution.log

# Check for errors
grep -i "error\|fail\|exception" /tmp/skill-execution.log
```

**Check resource usage:**
```bash
docker stats --no-stream $CONTAINER_ID
```

**Inspect filesystem changes:**
```bash
# List files in skill directory
docker exec $CONTAINER_ID find /root/.claude/skills/[skill-name] -type f

# Check temp directories
docker exec $CONTAINER_ID find /tmp -name "*skill*" -o -name "*.tmp"

# Check for leftover processes
docker exec $CONTAINER_ID ps aux | grep -v "ps\|bash"
```

**Analyze dependencies:**
```bash
# Check what packages were installed
docker diff $CONTAINER_ID | grep -E "^A /usr|^A /var/lib"

# Check what commands were executed
docker logs $CONTAINER_ID | grep -E "npm install|apt-get|pip install"
```

### Step 9: Generate Report

**Execution Status:**
```markdown
## Execution Results

**Container**: $CONTAINER_ID
**Base Image**: ubuntu:22.04
**Status**: [Running/Stopped/Exited]
**Exit Code**: $(docker inspect $CONTAINER_ID --format='{{.State.ExitCode}}')

**Resource Usage**:
- Memory: XMB / 512MB
- CPU: X%
- Execution Time: Xs
```

**Side Effects:**
```markdown
## Filesystem Changes

Files added: X
Files modified: X
Files deleted: X

**Significant changes:**
- /tmp/skill-temp-xyz.log (5KB)
- /root/.claude/cache/skill-data.json (15KB)
```

**Dependency Analysis:**
```markdown
## Dependencies Detected

**System Packages**:
- curl (already present)
- jq (installed by skill)

**NPM Packages**:
- lodash@4.17.21 (installed)

**Hardcoded Paths**:
⚠️ /root/.claude/config (line 45)
→ Use $HOME/.claude/config instead
```

### Step 10: Cleanup

**Ask user:**
```
Test complete. Container: $CONTAINER_ID

Options:
1. Keep container for debugging (docker start -ai $CONTAINER_ID)
2. Stop container, keep image (can restart later)
3. Remove container and image (full cleanup)

Your choice?
```

**Cleanup commands:**
```bash
# Option 2: Stop container
docker stop $CONTAINER_ID

# Option 3: Full cleanup
docker rm -f $CONTAINER_ID
docker rmi skill-test:[skill-name]
docker rmi skill-test:[skill-name]-after

# Cleanup test directory
rm -rf "$TEST_DIR"
```

**Cleanup all test containers:**
```bash
docker ps -a | grep skill-test | awk '{print $1}' | xargs docker rm -f
docker images | grep skill-test | awk '{print $3}' | xargs docker rmi -f
```

## Interpreting Results

### ✅ **PASS** - Production Ready
- Container exited with code 0
- Skill completed successfully
- No excessive resource usage
- All dependencies documented
- No orphaned processes
- Temp files in acceptable locations (/tmp only)

### ⚠️ **WARNING** - Needs Improvement
- Exit code 0 but warnings in logs
- Higher than expected resource usage
- Some undocumented dependencies
- Minor cleanup issues

### ❌ **FAIL** - Not Ready
- Container exited with non-zero code
- Skill crashed or hung
- Excessive resource usage (> 512MB memory)
- Attempted to access outside container
- Critical dependencies not documented

## Common Issues

### Issue: "Docker daemon not running"
**Fix**:
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker
```

### Issue: "Permission denied" when building image
**Cause**: User not in docker group
**Fix**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout/login or run:
newgrp docker
```

### Issue: "No space left on device"
**Cause**: Docker disk space full
**Fix**:
```bash
# Clean up old images and containers
docker system prune -a

# Check space
docker system df
```

### Issue: Skill requires GUI
**Cause**: Skill opens browser or displays graphics
**Fix**: Add X11 forwarding or mark skill as requiring GUI

## Advanced Techniques

### Volume Mounts for Live Testing

```bash
# Mount skill directory for live editing
docker run -it \
  -v ~/.claude/skills/[skill-name]:/root/.claude/skills/[skill-name] \
  skill-test:[skill-name]
```

### Custom Network Settings

```bash
# Isolated network (no internet)
docker run -it --network=none skill-test:[skill-name]

# Monitor network traffic
docker run -it --cap-add=NET_ADMIN skill-test:[skill-name]
```

### Multi-Stage Testing

```bash
# Test with different Node versions
docker build -t skill-test:node16 --build-arg NODE_VERSION=16 .
docker build -t skill-test:node18 --build-arg NODE_VERSION=18 .
docker build -t skill-test:node20 --build-arg NODE_VERSION=20 .
```

## Best Practices

1. **Always set resource limits** (`--memory`, `--cpus`) to prevent runaway processes
2. **Use `--rm` flag** for auto-cleanup in simple tests
3. **Tag images clearly** with skill name and version
4. **Cache base images** to speed up subsequent tests
5. **Export test results** before removing containers
6. **Test with minimal permissions** first, add as needed
7. **Document all APT/NPM/PIP installs** found during testing

## Quick Command Reference

```bash
# Build test image
docker build -t skill-test:my-skill .

# Run with auto-cleanup
docker run -it --rm skill-test:my-skill

# Run with resource limits
docker run -it --memory="512m" --cpus="1.0" skill-test:my-skill

# Check container status
docker ps -a | grep skill-test

# View container logs
docker logs <container-id>

# Execute command in running container
docker exec <container-id> <command>

# Stop and remove all test containers
docker ps -a | grep skill-test | awk '{print $1}' | xargs docker rm -f

# Remove all test images
docker images | grep skill-test | awk '{print $3}' | xargs docker rmi
```

---

**Remember:** Docker provides strong isolation with reproducible environments. Use for skills that install packages or modify system files. For highest security, use VM mode instead.
