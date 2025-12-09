---
name: test-driven-development
version: 0.3.0
description: Use PROACTIVELY when enforcing TDD red-green-refactor, setting up test infrastructure, configuring coverage gates, or implementing the Testing Trophy model. Installs git hooks, npm scripts, and CLAUDE.md configuration to enforce test-first development. Supports coverage thresholds and test distribution analysis. Not for prototypes or projects without test requirements.
---

# Test-Driven Development

## Overview

This skill enforces test-driven development (TDD) workflows when using Claude Code. Once installed, Claude will automatically follow red-green-refactor patterns without manual prompting.

**Version:** 0.3.0
**Status:** Stable

## What This Skill Does

**Automatic TDD Enforcement** - When you ask Claude to implement a feature:

1. **RED Phase**: Write failing test FIRST
2. **GREEN Phase**: Implement minimal code to pass test
3. **REFACTOR Phase**: Improve code quality while keeping tests green

**No manual prompting required** - configured through CLAUDE.md.

## When to Use This Skill

**Use when:**
- Enforcing TDD red-green-refactor workflow
- Setting up test infrastructure for new projects
- Configuring coverage gates and thresholds
- Implementing Testing Trophy model (70/20/10 distribution)
- Ensuring consistent test quality in LLM-generated code

**Don't use if:**
- Project doesn't need tests
- Working on prototypes or experiments
- Existing test workflow is incompatible

## Trigger Phrases

- "Set up TDD" / "Enforce TDD workflow"
- "Configure test-first development"
- "Set up coverage gates"
- "Implement Testing Trophy model"
- "Install test enforcement"

## Testing Trophy Model

From Kent C. Dodds: *"Write tests. Not too many. Mostly integration."*

| Type | Emphasis | Purpose |
|------|----------|---------|
| Integration | **Majority** | Test user workflows and component interactions |
| Unit | Smaller | Test complex isolated business logic |
| E2E | Minimal | Test critical user journeys only |
| Static | Base | TypeScript, ESLint (catches errors before runtime) |

## Coverage Gates

Default thresholds (configurable):

| Metric | Threshold |
|--------|-----------|
| Line coverage | 80% |
| Branch coverage | 75% |
| Function coverage | 90% |

## Installation Summary

The skill will:

1. **Detect** test framework (Vitest, Jest, Mocha, AVA)
2. **Configure** CLAUDE.md with TDD workflow requirements
3. **Install** npm scripts (`test:tdd`, `test:red`, `test:green`, `validate:tdd`)
4. **Add** git pre-commit hook for test validation
5. **Create** helper scripts for maintenance

See `workflow/installation-steps.md` for detailed procedures.

## Success Criteria

- CLAUDE.md contains TDD configuration
- npm scripts added to package.json
- Git pre-commit hook installed
- Coverage thresholds configured
- Validation passes: `npm run validate:tdd`

## Safety Features

- **Non-destructive**: Automatic backups before modifications
- **Merge-safe**: Preserves existing CLAUDE.md content
- **Reversible**: Rollback utility included
- **Idempotent**: Skips if already installed

See `reference/technical-details.md` for full documentation.

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| LLM not following TDD | Run `npm run validate:tdd` |
| Git hook blocking commits | Ensure tests exist, or `git commit --no-verify` |
| Want to remove | Run `node .tdd-automation/scripts/rollback-tdd.js` |

## Additional Resources

- **Detailed workflow**: `workflow/installation-steps.md`
- **Technical reference**: `reference/technical-details.md`
- **Full documentation**: `README.md`

## Version History

- **0.3.0** - Renamed to test-driven-development, added Testing Trophy and coverage gates
- **0.2.0** - Stable release (as tdd-automation)
- **0.1.0** - Initial proof-of-concept
