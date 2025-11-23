# Skill Test Templates

Production-ready test templates for validating Claude Code skills in isolated environments.

## Overview

These templates provide standardized testing workflows for different skill types. Each template includes:
- Pre-flight environment validation
- Before/after snapshots for comparison
- Comprehensive safety and security checks
- Detailed reporting with pass/fail criteria
- Automatic cleanup on exit (success or failure)

## CI/CD Integration with JSON Output

All test templates support JSON output for integration with CI/CD pipelines. The JSON reporter generates:
- **Structured JSON** - Machine-readable test results
- **JUnit XML** - Compatible with Jenkins, GitLab CI, GitHub Actions
- **Markdown Summary** - Human-readable reports for GitHub Actions

**Enable JSON output:**
```bash
export JSON_ENABLED=true
./test-templates/docker-skill-test-json.sh my-skill
```

**Output files:**
- `test-report.json` - Full structured test data
- `test-report.junit.xml` - JUnit format for CI systems
- `test-report.md` - Markdown summary

**JSON Report Structure:**
```json
{
  "test_name": "docker-skill-test",
  "skill_name": "my-skill",
  "timestamp": "2025-11-02T12:00:00Z",
  "status": "passed",
  "duration_seconds": 45,
  "exit_code": 0,
  "metrics": {
    "containers_created": 2,
    "images_created": 1,
    "execution_duration_seconds": 12
  },
  "issues": [],
  "recommendations": []
}
```

**GitHub Actions Integration:**
```yaml
- name: Test Skill
  run: |
    export JSON_ENABLED=true
    ./test-templates/docker-skill-test-json.sh my-skill

- name: Upload Test Results
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: /tmp/skill-test-*/test-report.*
```

See `lib/json-reporter.sh` for full API documentation.

---

## Available Templates

### 1. Docker Skill Test (`docker-skill-test.sh`)

**Use for skills that:**
- Start or manage Docker containers
- Build Docker images
- Work with Docker volumes, networks, or compose files
- Require Docker daemon access

**Features:**
- Tracks Docker resource creation (containers, images, volumes, networks)
- Detects orphaned containers
- Validates cleanup behavior
- Resource limit enforcement

**Usage:**
```bash
chmod +x test-templates/docker-skill-test.sh
./test-templates/docker-skill-test.sh my-docker-skill
```

**Customization:**
Edit the skill execution command on line ~178:
```bash
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /root/.claude/skills/$SKILL_NAME
    ./skill.sh test-mode  # <-- Customize this
"
```

---

### 2. API Skill Test (`api-skill-test.sh`)

**Use for skills that:**
- Make HTTP/HTTPS requests to external APIs
- Require API keys or authentication
- Interact with web services
- Need network access

**Features:**
- Network traffic monitoring
- API call detection and counting
- API key/secret leak detection
- Rate limiting validation
- HTTPS enforcement checking

**Usage:**
```bash
chmod +x test-templates/api-skill-test.sh
./test-templates/api-skill-test.sh my-api-skill
```

**Optional: Enable network capture:**
```bash
# Requires tcpdump and sudo
sudo apt-get install tcpdump  # or brew install tcpdump
./test-templates/api-skill-test.sh my-api-skill
```

---

### 3. File Manipulation Skill Test (`file-manipulation-skill-test.sh`)

**Use for skills that:**
- Create, read, update, or delete files
- Modify configuration files
- Generate reports or artifacts
- Perform filesystem operations

**Features:**
- Complete filesystem diff (added/removed/modified files)
- File permission validation
- Sensitive data scanning
- Temp file cleanup verification
- MD5 checksum comparison

**Usage:**
```bash
chmod +x test-templates/file-manipulation-skill-test.sh
./test-templates/file-manipulation-skill-test.sh my-file-skill
```

**Customization:**
Add your own test files to the workspace (lines 54-70):
```bash
cat > "$TEST_DIR/test-workspace/your-file.txt" <<'EOF'
Your test content here
EOF
```

---

### 4. Git Skill Test (`git-skill-test.sh`)

**Use for skills that:**
- Create commits, branches, or tags
- Modify git history or configuration
- Work with git worktrees
- Interact with remote repositories

**Features:**
- Git state comparison (commits, branches, tags)
- Working tree cleanliness validation
- Force operation detection
- History rewriting detection
- Dangling commit detection

**Usage:**
```bash
chmod +x test-templates/git-skill-test.sh
./test-templates/git-skill-test.sh my-git-skill
```

**Customization:**
Modify the test repository setup (lines 59-81) to match your skill's requirements.

---

## Common Usage Patterns

### Basic Test Execution

```bash
# Run test for a specific skill
./test-templates/docker-skill-test.sh my-skill-name

# Keep container for debugging
export SKILL_TEST_KEEP_CONTAINER="true"
./test-templates/docker-skill-test.sh my-skill-name

# Keep images after test
export SKILL_TEST_REMOVE_IMAGES="false"
./test-templates/docker-skill-test.sh my-skill-name
```

### Custom Resource Limits

```bash
# Set custom memory/CPU limits
export SKILL_TEST_MEMORY_LIMIT="1g"
export SKILL_TEST_CPU_LIMIT="2.0"
./test-templates/docker-skill-test.sh my-skill-name
```

### Parallel Testing

```bash
# Test multiple skills in parallel
for skill in skill1 skill2 skill3; do
    ./test-templates/docker-skill-test.sh "$skill" &
done
wait
echo "All tests complete!"
```

### CI/CD Integration

```bash
# Exit code 0 = pass, 1 = fail
#!/bin/bash
set -e

SKILLS=(
    "skill-creator"
    "claude-code-otel-setup"
    "playwright-e2e-automation"
)

for skill in "${SKILLS[@]}"; do
    echo "Testing $skill..."
    ./test-templates/docker-skill-test.sh "$skill" || {
        echo "❌ $skill failed!"
        exit 1
    }
done

echo "✅ All skills passed!"
```

## Customizing Templates

### Add Custom Validation

Insert your own checks before the "Generate Test Report" section:

```bash
# ============================================================================
# Custom Validation
# ============================================================================

echo ""
echo "=== Running Custom Checks ==="

# Your custom checks here
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    # Example: Check if specific file exists
    test -f /workspace/expected-output.txt || {
        echo 'ERROR: Expected output file not found'
        exit 1
    }
"
```

### Modify Execution Command

Each template has a skill execution section. Customize the command to match your skill's interface:

```bash
# Example: Run skill with arguments
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    cd /root/.claude/skills/$SKILL_NAME
    ./skill.sh --mode=test --output=/workspace/results
"

# Example: Source skill as library
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    source /root/.claude/skills/$SKILL_NAME/lib.sh
    run_skill_tests
"
```

### Add Pre-Test Setup

Insert setup steps after the "Build Test Environment" section:

```bash
# Install additional dependencies
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    apt-get update && apt-get install -y your-package
"

# Set environment variables
docker exec "$SKILL_TEST_CONTAINER_ID" bash -c "
    export SKILL_CONFIG_PATH=/etc/skill-config.json
"
```

## Environment Variables

All templates support these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SKILL_TEST_KEEP_CONTAINER` | `false` | Keep container after test for debugging |
| `SKILL_TEST_REMOVE_IMAGES` | `true` | Remove test images after completion |
| `SKILL_TEST_MEMORY_LIMIT` | `512m` | Container memory limit |
| `SKILL_TEST_CPU_LIMIT` | `1.0` | Container CPU limit (cores) |
| `SKILL_TEST_TEMP_DIR` | `/tmp/skill-test-*` | Temporary directory for test artifacts |

## Exit Codes

- `0` - Test passed (skill executed successfully)
- `1` - Test failed (skill execution error or validation failure)
- `>1` - Other errors (environment setup, Docker issues, etc.)

## Troubleshooting

### "Docker daemon not running"
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker
```

### "Permission denied" errors
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Container hangs or never exits
```bash
# Set a timeout in your skill execution
timeout 300 ./test-templates/docker-skill-test.sh my-skill
```

### Need to inspect failed test
```bash
# Keep container after failure
export SKILL_TEST_KEEP_CONTAINER="true"
./test-templates/docker-skill-test.sh my-skill

# Inspect container
docker start -ai <container-id>
docker logs <container-id>
```

## Best Practices

1. **Run tests before committing** - Catch environment-specific bugs early
2. **Test in clean environment** - Don't rely on local configs or files
3. **Validate cleanup** - Ensure skills don't leave orphaned resources
4. **Check for secrets** - Never commit API keys or sensitive data
5. **Document dependencies** - List all required packages and tools
6. **Use resource limits** - Prevent runaway processes
7. **Review diffs carefully** - Understand all file system changes

## Contributing

To add a new test template:

1. Copy an existing template as a starting point
2. Customize for your skill type
3. Add comprehensive validation checks
4. Update this README with usage documentation
5. Test your template with at least 3 different skills

## Related Documentation

- `../lib/docker-helpers.sh` - Shared helper functions
- `../modes/mode2-docker.md` - Docker isolation mode documentation
- `../skill.md` - Main skill documentation

## Support

For issues or questions:
- Check the skill logs: `docker logs <container-id>`
- Review test artifacts in `/tmp/skill-test-*/`
- Consult the helper library: `lib/docker-helpers.sh`
