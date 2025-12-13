# Skill Isolation Tester

> Automated testing framework for Claude Code skills in isolated environments

## Overview

Test your newly created Claude Code skills in isolated environments before sharing them publicly. This skill automatically spins up git worktrees, Docker containers, or VMs to validate that your skills work correctly without hidden dependencies on your local setup.

## Features

- **Multiple Isolation Levels**: Choose from git worktree (fast), Docker (balanced), or VM (safest)
- **Automatic Mode Detection**: Analyzes skill risk and suggests appropriate isolation level
- **Comprehensive Validation**: Checks execution, side effects, dependencies, and cleanup
- **Detailed Reports**: Get actionable feedback with specific issues and recommendations
- **Safe Testing**: Protect your main development environment from experimental skills

## Quick Start

### Basic Usage

```
test skill my-new-skill in isolation
```

Claude will analyze your skill and choose the appropriate isolation environment.

### Specify Environment

```
test skill my-new-skill in worktree  # Fast, lightweight
test skill my-new-skill in docker    # OS isolation
test skill my-new-skill in vm        # Maximum security
```

### Check for Issues

```
check if skill my-new-skill has hidden dependencies
verify skill my-new-skill cleans up after itself
```

## Isolation Modes

### 🚀 Git Worktree (Fast)

**Best for**: Read-only skills, quick iteration during development

- ✅ Creates test in seconds
- ✅ Minimal disk space
- ⚠️ Limited isolation (shares system packages)

**Prerequisites**: Git 2.5+

### 🐳 Docker (Balanced)

**Best for**: Skills that install packages or modify files

- ✅ Full OS isolation
- ✅ Reproducible environment
- ⚠️ Requires Docker installed

**Prerequisites**: Docker daemon running

### 🖥️ VM (Safest)

**Best for**: High-risk skills, untrusted sources

- ✅ Complete isolation
- ✅ Test on different OS versions
- ⚠️ Slower, resource-intensive

**Prerequisites**: Multipass, UTM, or VirtualBox

## What Gets Tested

### ✅ Execution Validation
- Skill completes without errors
- No unhandled exceptions
- Acceptable performance

### ✅ Side Effect Detection
- Files created/modified/deleted
- Processes started (and stopped)
- System configuration changes
- Network activity

### ✅ Dependency Analysis
- Required system packages
- NPM/pip dependencies
- Hardcoded paths
- Environment variables needed

### ✅ Cleanup Verification
- Temporary files removed
- Processes terminated
- System state restored

## Example Report

```markdown
# Skill Isolation Test Report: my-new-skill

## Status: ⚠️ WARNING (Ready with minor fixes)

### Execution Results
✅ Skill completed successfully
✅ No errors detected
⏱️ Execution time: 12s

### Issues Found

**HIGH Priority:**
- Missing documentation for `jq` dependency
- Hardcoded path: /Users/connor/.claude/config (line 45)

**MEDIUM Priority:**
- 3 temporary files not cleaned up in /tmp

### Recommendations
1. Document `jq` requirement in README
2. Replace hardcoded path with $HOME/.claude/config
3. Add cleanup for /tmp/skill-temp-*.log files

### Overall Grade: B (READY after addressing HIGH priority items)
```

## Installation

This skill is already available in your Claude Code skills directory.

### Manual Installation

```bash
cp -r skill-isolation-tester ~/.claude/skills/
```

### Verify Installation

Start Claude Code and say:
```
test skill [any-skill-name] in isolation
```

## Prerequisites

### Required (All Modes)
- Git 2.5+
- Claude Code 1.0+

### Optional (Docker Mode)
- Docker Desktop or Docker Engine
- 1GB+ free disk space

### Optional (VM Mode)
- Multipass (recommended) or
- UTM (macOS) or
- VirtualBox (cross-platform)
- 8GB+ host RAM
- 20GB+ free disk space

## Configuration

### Set Default Isolation Mode

Create `~/.claude/skills/skill-isolation-tester/config.json`:

```json
{
  "default_mode": "docker",
  "docker": {
    "base_image": "ubuntu:22.04",
    "memory_limit": "512m",
    "cpu_limit": "1.0"
  },
  "vm": {
    "platform": "multipass",
    "os_version": "22.04",
    "cpus": 2,
    "memory": "2G",
    "disk": "10G"
  }
}
```

## Use Cases

### Before Submitting to Claudex Marketplace

```
validate skill my-marketplace-skill in docker
```

Ensures your skill works in clean environment without your personal configs.

### Testing Skills from Others

```
test skill untrusted-skill in vm
```

Maximum isolation protects your system from potential issues.

### Catching Environment-Specific Bugs

```
test skill my-skill in worktree
```

Quickly verify skill doesn't depend on your specific setup.

### CI/CD Integration

```bash
#!/bin/bash
# In your CI pipeline
claude "test skill $SKILL_NAME in docker"

if [ $? -eq 0 ]; then
  echo "✅ Skill tests passed"
  exit 0
else
  echo "❌ Skill tests failed"
  exit 1
fi
```

## Troubleshooting

### "Docker daemon not running"

**macOS**: Open Docker Desktop
**Linux**: `sudo systemctl start docker`

### "Multipass not found"

```bash
# macOS
brew install multipass

# Linux
sudo snap install multipass
```

### "Permission denied"

Add your user to docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### "Out of disk space"

Clean up Docker:
```bash
docker system prune -a
```

## Best Practices

1. **Test before committing** - Catch issues early
2. **Start with worktree** - Fast iteration during development
3. **Use Docker for final validation** - Before public release
4. **Use VM for untrusted skills** - Safety first
5. **Review test reports** - Address all HIGH priority issues
6. **Document dependencies** - Help other users

## Advanced Usage

### Custom Test Scenarios

```
test skill my-skill with inputs "test-file.txt, --option value"
```

### Batch Testing

```
test all skills in directory ./skills/ in worktree
```

### Keep Environment for Debugging

```
test skill my-skill in docker --keep
```

Preserves container/VM for manual inspection.

## Architecture

```
skill-isolation-tester/
├── SKILL.md                    # Main skill manifest
├── README.md                   # This file
├── CHANGELOG.md                # Version history
├── plugin.json                 # Marketplace metadata
├── modes/                      # Mode-specific workflows
│   ├── mode1-git-worktree.md  # Fast isolation
│   ├── mode2-docker.md        # Container isolation
│   └── mode3-vm.md            # VM isolation
├── data/                       # Reference materials
│   ├── risk-assessment.md     # How to assess skill risk
│   └── side-effect-checklist.md  # What to check for
├── templates/                  # Report templates
│   └── test-report.md         # Standard report format
└── examples/                   # Sample outputs
    └── test-results/          # Example test results
```

## Contributing

Found a bug or have a feature request? Issues and PRs welcome!

## License

MIT License - see LICENSE file for details

## Related Skills

- **skill-creator**: Create new skills with proper structure
- **git-worktree-setup**: Manage parallel development workflows

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Credits

Created by Connor
Inspired by best practices in software testing and isolation

---

**Remember**: Test in isolation, ship with confidence! 🚀
