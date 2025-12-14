# Semantic Release Tagger

Automated git tagging agent that analyzes your repository, parses conventional commits, recommends semantic versions, and executes tag creation with your confirmation.

## Overview

This skill is an **interactive automation agent** that handles the complete git tagging workflow. It analyzes repository state, detects existing conventions, parses conventional commits to determine version bumps, and executes tag creation commands with your confirmation.

## Installation

Install from the Claudex marketplace using Claude Code.

## Quick Start

Invoke this skill when you need help with:
- "how should I tag this release?"
- "version this component"
- "create semantic git tags"
- "monorepo versioning strategy"

The skill will automatically:
1. **Analyze your repository** - Detect tags, conventions, and recent commits
2. **Calculate next version** - Parse conventional commits for intelligent version bumps
3. **Recommend tag** - Present findings and suggested version
4. **Execute after confirmation** - Create and push tag with one command
5. **Optionally create GitHub release** - Auto-generated changelog from commits

## Trigger Phrases

- "how should I tag this release?"
- "version this component"
- "create semantic git tags"
- "tag naming convention"
- "monorepo versioning strategy"
- "git tag vs github release"
- "semantic versioning guidance"

## Features

- ✅ **Automated context analysis** - Auto-detects existing patterns
- ✅ **Conventional commit parsing** - Intelligent MAJOR/MINOR/PATCH detection
- ✅ **Command execution** - Creates and pushes tags after confirmation
- ✅ **Monorepo support** - Component-specific versioning with namespaces
- ✅ **GitHub release integration** - Auto-generated changelogs
- ✅ **Consistency auditing** - Detects mixed tag conventions
- ✅ **CI/CD patterns** - Tag filtering for automation

## Workflow

1. **Phase 0: Auto-Analysis** (runs automatically)
   - Detects tag conventions, latest versions, commits since last tag
2. **Phase 1: Convention Selection** (if needed)
   - Choose namespace pattern for monorepos
3. **Phase 2: Version Calculation** (automated)
   - Parse conventional commits, determine version bump
4. **Phase 3: Tag Creation** (after confirmation)
   - Execute git tag and push commands
5. **Phase 4: GitHub Release** (optional)
   - Create release with auto-generated changelog

## Documentation

See [SKILL.md](SKILL.md) for complete documentation including:
- Detailed workflow phases
- Conventional commit parsing rules
- Tag naming convention trade-offs
- Troubleshooting guide
- Real-world examples

## Source

Generated from 7 production insights from version-control workflows (2025-11-14 to 2025-11-15).

## Version

0.1.0 - Initial marketplace release

## License

Part of the Claudex marketplace.
