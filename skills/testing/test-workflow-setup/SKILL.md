---
name: test-workflow-setup
version: 0.3.0
description: Use PROACTIVELY when setting up test infrastructure, enforcing test-first workflows, or configuring test automation for new projects. Installs git hooks, npm scripts, and CLAUDE.md configuration to enforce testing discipline including TDD red-green-refactor. Not for prototypes or projects without test requirements.
---

# Test Workflow Setup

## Overview

This skill sets up test infrastructure that automatically enforces test-first workflows when using Claude Code. Once installed, Claude will follow test-driven development patterns without manual prompting.

**Version:** 0.3.0
**Status:** Stable

## What This Skill Does

**Automatic Test Enforcement** - When you ask Claude to implement a feature, it will:

1. **RED Phase**: Write failing test FIRST
2. **GREEN Phase**: Implement minimal code to pass test
3. **REFACTOR Phase**: Improve code quality while keeping tests green

**No manual steps required** - The LLM is automatically configured through CLAUDE.md.

## When to Use This Skill

**Use when:**
- Starting a new project requiring test discipline
- Setting up test infrastructure for existing projects
- Enforcing test-first workflows in team environments
- Ensuring consistent quality in LLM-generated code
- Working on mission-critical code needing high coverage

**Don't use if:**
- Project doesn't have or need tests
- Working on prototypes or experiments
- Test workflow conflicts with existing practices

## Trigger Phrases

- Direct: `test-workflow-setup`
- "Set up test workflow"
- "Configure test infrastructure"
- "Install test enforcement"
- "Set up TDD automation"
- "Enforce test-first development"

## Installation Summary

The skill will:

1. **Detect** test framework (Vitest, Jest, Mocha, AVA)
2. **Configure** CLAUDE.md with test workflow requirements
3. **Install** npm scripts (`test:tdd`, `test:red`, `test:green`, `validate:tdd`)
4. **Add** git pre-commit hook for test validation
5. **Create** helper scripts for maintenance

See `workflow/installation-steps.md` for detailed procedures.

## Success Criteria

Installation succeeds when:
- CLAUDE.md contains test workflow configuration
- npm scripts added to package.json
- Git pre-commit hook installed (if git repo exists)
- Helper scripts created in `.tdd-automation/`
- Backups created for all modified files
- Validation passes: `npm run validate:tdd`

## Safety Features

- **Non-destructive**: Automatic backups before modifications
- **Merge-safe**: Preserves existing CLAUDE.md content
- **Reversible**: Rollback utility included
- **Idempotent**: Skips if already installed

See `reference/technical-details.md` for full safety documentation.

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| LLM not following workflow | Run `npm run validate:tdd` |
| Git hook blocking commits | Ensure tests exist, or `git commit --no-verify` |
| Want to remove | Run `node .tdd-automation/scripts/rollback-tdd.js` |

See `reference/technical-details.md` for detailed troubleshooting.

## Additional Resources

- **Detailed workflow**: `workflow/installation-steps.md`
- **Technical reference**: `reference/technical-details.md`
- **Full documentation**: `README.md`
- **Helper scripts**: `.tdd-automation/scripts/`

## Version History

- **0.3.0** - Renamed to test-workflow-setup, refactored to progressive disclosure
- **0.2.0** - Stable release with full implementation
- **0.1.0** - Initial proof-of-concept
