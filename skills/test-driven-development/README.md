# TDD Red-Green-Refactor Automation

Automated TDD enforcement for LLM-assisted development. This skill installs infrastructure that guides Claude Code to automatically follow TDD workflow without manual intervention.

## Version

**0.2.0** - Stable release with comprehensive safety features

## What This Skill Does

Transforms your project so that when you ask Claude to implement features, it **automatically**:

1. 🔴 **RED Phase** - Writes failing tests FIRST
2. 🟢 **GREEN Phase** - Implements minimal code to pass tests
3. 🔵 **REFACTOR Phase** - Improves code quality while keeping tests green

**No slash commands. No manual prompting. Just say "implement X" and TDD happens.**

## Installation

```bash
# From claudex marketplace
/plugin install tdd-automation

# Or directly invoke the skill
tdd-automation
```

## What Gets Installed

### 1. CLAUDE.md Configuration
- Adds TDD requirements to project's `.claude/CLAUDE.md`
- **Safety**: Backs up existing files, merges cleanly, fully reversible
- Configures LLM to automatically follow TDD workflow

### 2. npm Scripts
```json
{
  "test:tdd": "vitest --run",
  "test:tdd:watch": "vitest",
  "test:red": "vitest --run --reporter=verbose",
  "test:green": "vitest --run --reporter=verbose",
  "validate:tdd": "node .tdd-automation/scripts/validate-tdd.js",
  "generate:test": "node .tdd-automation/scripts/generate-test.js"
}
```

### 3. Git Hooks
- **Pre-commit hook**: Validates tests exist before allowing commits
- Prevents TDD violations at the version control level
- Can be bypassed with `--no-verify` if needed

### 4. Helper Scripts
```
.tdd-automation/
├── scripts/
│   ├── generate-test.js       # Create test templates
│   ├── validate-tdd.js        # Check compliance
│   ├── rollback-tdd.js        # Restore previous state
│   └── remove-tdd-section.js  # Clean uninstall
└── templates/
    └── test-template.js       # Test file template
```

## Usage Examples

### Before Installation
```
You: "Add user authentication"
Claude: *writes implementation code directly* ❌
```

### After Installation
```
You: "Add user authentication"

Claude: "I'll implement user authentication following TDD red-green-refactor.

Let me create a todo list to track the phases:
- [ ] RED: Write failing test for user authentication
- [ ] Verify test fails with expected error
- [ ] GREEN: Implement minimal authentication logic
- [ ] Verify test passes
- [ ] REFACTOR: Improve code quality

Starting RED phase - I'll create the test file first..."

*Creates src/auth/authenticate.test.ts*
*Writes failing test*
*Runs: npm run test:red*
*Verifies failure*

"Test is failing as expected. Moving to GREEN phase..."

*Implements minimal code*
*Runs: npm run test:green*
*Verifies pass*

"All tests passing. Moving to REFACTOR phase..."

*Improves code structure*
*Runs: npm run test:tdd*

"✅ Feature complete with TDD workflow followed."
```

## Available Commands

### Validation
```bash
# Check if project follows TDD practices
npm run validate:tdd
```

### Test Generation
```bash
# Generate test template for implementation file
npm run generate:test src/features/auth/login.ts
```

### Maintenance
```bash
# Rollback to previous CLAUDE.md
node .tdd-automation/scripts/rollback-tdd.js

# Remove only TDD section from CLAUDE.md
node .tdd-automation/scripts/remove-tdd-section.js

# View available backups
ls -lh .claude/CLAUDE.md.backup.*
```

## Safety Features

### ✅ Non-Destructive Installation
- **Automatic backups** before any file modification
- **Merge strategy** preserves all existing content
- **Clear markers** for easy identification of additions
- **Rollback capability** to restore previous state

### ✅ Validation Before Installation
- Detects existing TDD automation (skips if present)
- Checks for existing CLAUDE.md (merges safely)
- Validates project structure
- Reports warnings for missing dependencies

### ✅ Clean Uninstallation
- Remove TDD section without affecting other content
- Restore from timestamped backups
- No orphaned files or configurations

## Configuration

### Enforcement Level

By default, TDD is **strictly enforced**. To customize:

Edit `.claude/CLAUDE.md` and modify:
```yaml
tdd-enforcement-level: strict  # or: advisory, optional
```

- **strict**: LLM must follow TDD (default)
- **advisory**: LLM suggests TDD but allows flexibility
- **optional**: TDD is available but not required

### Test Framework

The skill auto-detects your test framework:
- Vitest (default, recommended)
- Jest
- Mocha
- AVA

To override, edit `.tdd-automation/config.json`:
```json
{
  "testCommand": "jest",
  "testExtension": ".test.ts"
}
```

## Troubleshooting

### Issue: LLM not following TDD

**Solution:**
1. Check CLAUDE.md has TDD configuration:
   ```bash
   grep -A 5 "TDD_AUTOMATION" .claude/CLAUDE.md
   ```

2. Verify npm scripts installed:
   ```bash
   npm run test:tdd
   ```

3. Validate installation:
   ```bash
   npm run validate:tdd
   ```

### Issue: Git hook blocking commits

**Solution:**
1. Ensure tests exist for implementation files
2. Commit tests before implementation:
   ```bash
   git add src/**/*.test.ts
   git commit -m "Add tests for feature X"
   git add src/**/!(*test).ts
   git commit -m "Implement feature X"
   ```

3. Or bypass hook temporarily:
   ```bash
   git commit --no-verify
   ```

### Issue: Want to remove TDD automation

**Solution:**
```bash
# Option 1: Remove only CLAUDE.md section
node .tdd-automation/scripts/remove-tdd-section.js

# Option 2: Rollback to previous CLAUDE.md
node .tdd-automation/scripts/rollback-tdd.js

# Option 3: Manual removal
# 1. Edit .claude/CLAUDE.md
# 2. Delete section between <!-- TDD_AUTOMATION_START --> and <!-- TDD_AUTOMATION_END -->
# 3. Remove .tdd-automation/ directory
# 4. Remove npm scripts from package.json
```

## Technical Details

### Architecture

```
┌─────────────────────────────────────────┐
│         User Request                     │
│   "Implement feature X"                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    CLAUDE.md (LLM Configuration)        │
│  • TDD workflow requirements             │
│  • Phase-by-phase instructions          │
│  • TodoWrite templates                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Claude Code (LLM)                  │
│  1. Creates test file                    │
│  2. Writes failing test (RED)           │
│  3. Runs: npm run test:red              │
│  4. Implements code (GREEN)             │
│  5. Runs: npm run test:green            │
│  6. Refactors (REFACTOR)                │
│  7. Runs: npm run test:tdd              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Git Pre-Commit Hook                │
│  • Validates tests exist                 │
│  • Blocks commits without tests          │
│  • Ensures test-first compliance         │
└─────────────────────────────────────────┘
```

### File Structure

```
project/
├── .claude/
│   ├── CLAUDE.md                    # TDD configuration (modified)
│   ├── CLAUDE.md.backup.*           # Safety backups
│   └── hooks/
│       └── tdd-auto-enforcer.sh     # Pre-prompt hook (optional)
├── .git/
│   └── hooks/
│       └── pre-commit               # TDD validation (modified)
├── .tdd-automation/                 # Installed by skill
│   ├── scripts/
│   │   ├── generate-test.js
│   │   ├── validate-tdd.js
│   │   ├── rollback-tdd.js
│   │   └── remove-tdd-section.js
│   ├── templates/
│   │   └── test-template.js
│   └── README.md
└── package.json                     # npm scripts added
```

## Success Metrics

Track TDD adherence:

```bash
npm run validate:tdd
```

**Target Metrics:**
- Test-first adherence: >95%
- RED-GREEN-REFACTOR cycles: >90%
- Defect escape rate: <2%
- Test coverage: >80%

## Contributing

This skill was auto-generated by the Pattern Suggestion Pipeline from 37 successful TDD applications with 86% success rate.

**Issues or improvements:**
- GitHub: https://github.com/cskiro/claudex/issues
- Pattern source: Issue #13

## License

MIT

## Version History

- **0.2.0** (2025-11-02)
  - Stable release with full implementation
  - Comprehensive safety features (backup, rollback, merge)
  - Automatic LLM TDD enforcement via CLAUDE.md
  - Git hooks for pre-commit validation
  - Helper scripts (generate-test, validate-tdd)
  - Multi-framework support (Vitest, Jest, Mocha, AVA)
  - Complete documentation and troubleshooting guide

- **0.1.0** (2025-11-02)
  - Initial proof-of-concept
  - Auto-generated by Pattern Pipeline
  - Basic skill structure and manifest
