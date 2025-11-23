---
name: tdd-automation
version: 0.2.0
description: Use PROACTIVELY when starting new projects requiring strict TDD adherence, or when user wants to enforce test-first workflow. Automates red-green-refactor cycle for LLM-assisted development with git hooks, npm scripts, and CLAUDE.md configuration. Not for prototypes or projects without test requirements.
author: Pattern Suggestion Pipeline
category: productivity
status: stable
tags: [tdd, testing, automation, workflow]
---

# TDD Red-Green-Refactor Automation

## Overview

This skill transforms any project to automatically enforce TDD (Test-Driven Development) workflow when using LLMs for code generation. Once installed, Claude Code will automatically follow the red-green-refactor cycle without manual prompting.

**Version:** 0.2.0
**Status:** Stable
**Success Rate:** 86% (based on 37 pattern applications)
**Source:** Pattern Suggestion Pipeline (Issue #13)

## What This Skill Does

**Automatic TDD Enforcement** - When you ask Claude to implement a feature, it will:

1. 🔴 **RED Phase**: Write failing test FIRST
2. 🟢 **GREEN Phase**: Implement minimal code to pass test
3. 🔵 **REFACTOR Phase**: Improve code quality while keeping tests green

**No manual steps required** - The LLM is automatically configured through CLAUDE.md to follow this workflow.

## Installation Process

When you invoke this skill, it will:

1. **Detect project configuration**
   - Identify test framework (Vitest, Jest, Mocha, AVA)
   - Check for TypeScript/JavaScript
   - Validate git repository exists

2. **Configure CLAUDE.md safely**
   - Create automatic backup before any changes
   - Merge TDD requirements (preserves existing content)
   - Add clear section markers for identification

3. **Install npm scripts**
   - `test:tdd` - Run all tests once
   - `test:tdd:watch` - Run tests in watch mode
   - `test:red` - Verify test fails (RED phase)
   - `test:green` - Verify test passes (GREEN phase)
   - `validate:tdd` - Check TDD compliance
   - `generate:test` - Create test template

4. **Install git hooks**
   - Pre-commit hook validates tests exist
   - Prevents commits without tests
   - Enforces test-first workflow

5. **Create helper scripts**
   - Test template generator
   - TDD compliance validator
   - Rollback utility
   - Section removal utility

## When to Use This Skill

**Use this skill when:**
- Starting a new project that requires strict TDD adherence
- Migrating existing project to TDD workflow
- Training team members on TDD practices
- Ensuring consistent quality in LLM-generated code
- Working on mission-critical code that needs high test coverage

**Don't use this skill if:**
- Project doesn't have or need tests
- Working on prototypes or experiments
- TDD workflow conflicts with existing practices

## Trigger Phrases

The skill can be invoked by:
- Direct invocation: `tdd-automation`
- Natural language: "Set up TDD automation"
- Natural language: "Configure automatic TDD workflow"
- Natural language: "Install TDD enforcement"

## Behavior After Installation

Once installed, when you say something like:
```
"Implement user authentication"
```

Claude will **automatically**:
```
1. Create todo list with TDD phases:
   - [ ] RED: Write failing test for user authentication
   - [ ] Verify test fails with expected error
   - [ ] GREEN: Implement minimal authentication logic
   - [ ] Verify test passes
   - [ ] REFACTOR: Improve code quality
   - [ ] Verify all tests still pass

2. Create test file FIRST:
   src/auth/authenticate.test.ts

3. Write failing test with clear description

4. Run test and verify RED state:
   npm run test:red -- src/auth/authenticate.test.ts

5. Implement minimal code:
   src/auth/authenticate.ts

6. Run test and verify GREEN state:
   npm run test:green -- src/auth/authenticate.test.ts

7. Refactor if needed while keeping tests green

8. Final validation:
   npm run test:tdd
```

## Safety Features

### Non-Destructive Installation
- Automatic backups before file modifications
- Merge strategy preserves all existing CLAUDE.md content
- Clear markers (`<!-- TDD_AUTOMATION_START/END -->`) for identification
- Rollback capability to restore previous state

### Validation Before Installation
- Detects if TDD automation already installed (skips if present)
- Checks for existing CLAUDE.md (merges safely)
- Validates project structure
- Reports warnings for missing dependencies

### Clean Uninstallation
- Remove only TDD section without affecting other content
- Restore from timestamped backups
- Utility scripts for easy maintenance

## Response Style

After installation, this skill guides Claude Code to:

- **Be explicit**: Always state which TDD phase is active
- **Be thorough**: Verify each phase completion before proceeding
- **Be traceable**: Use TodoWrite to track progress
- **Be safe**: Run tests to confirm RED/GREEN states
- **Be helpful**: Provide clear error messages if TDD is violated

## Files Modified/Created

### Modified Files
- `.claude/CLAUDE.md` - TDD workflow configuration added (backed up)
- `package.json` - npm scripts added (backed up)
- `.git/hooks/pre-commit` - TDD validation added (backed up if exists)

### Created Files
```
.tdd-automation/
├── scripts/
│   ├── generate-test.js       # Test template generator
│   ├── validate-tdd.js        # Compliance checker
│   ├── rollback-tdd.js        # Restore previous state
│   └── remove-tdd-section.js  # Clean uninstall
├── templates/
│   └── test-template.js       # Test file template
└── README.md                  # Usage documentation

.claude/
├── CLAUDE.md.backup.* # Timestamped backups
└── hooks/
    └── tdd-auto-enforcer.sh   # Pre-prompt hook (optional)
```

## Success Criteria

Installation succeeds when:
1. ✅ CLAUDE.md contains TDD configuration
2. ✅ npm scripts added to package.json
3. ✅ Git pre-commit hook installed (if git repo exists)
4. ✅ Helper scripts created in .tdd-automation/
5. ✅ Backups created for all modified files
6. ✅ Validation passes: `npm run validate:tdd`

## Troubleshooting

### Issue: LLM not following TDD

**Check:**
```bash
# Verify CLAUDE.md has TDD configuration
grep "TDD_AUTOMATION" .claude/CLAUDE.md

# Verify npm scripts
npm run test:tdd

# Run validation
npm run validate:tdd
```

### Issue: Git hook blocking commits

**Solution:**
1. Ensure tests exist for implementation files
2. Commit tests before implementation
3. Or bypass temporarily: `git commit --no-verify`

### Issue: Want to remove TDD automation

**Options:**
```bash
# Option 1: Remove CLAUDE.md section only
node .tdd-automation/scripts/remove-tdd-section.js

# Option 2: Rollback to previous CLAUDE.md
node .tdd-automation/scripts/rollback-tdd.js
```

## Generated By

🤖 **Pattern Suggestion Pipeline**
- Detected from 37 successful TDD applications
- Success rate: 86%
- Source: GitHub Issue #13
- Generated: 2025-11-02
- Enhanced with full implementation: 2025-11-02

## Version History

- **0.2.0** (2025-11-02) - Stable release with full implementation
- **0.1.0** (2025-11-02) - Initial proof-of-concept

## Additional Resources

- Full documentation: `README.md`
- Helper scripts: `.tdd-automation/scripts/`
- Examples: See README.md "Usage Examples" section
