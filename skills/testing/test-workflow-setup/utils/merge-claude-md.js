#!/usr/bin/env node

/**
 * CLAUDE.md Merger
 *
 * Safely merges TDD automation configuration into existing CLAUDE.md files
 * while preserving all existing content.
 */

const fs = require('fs');
const path = require('path');

class ClaudeMdMerger {
  constructor(existingContent = '') {
    this.existingContent = existingContent;
    this.version = '0.2.0';
  }

  /**
   * Merge TDD section with existing content
   * @returns {string} Merged CLAUDE.md content
   */
  merge() {
    // Strategy: Append TDD section with clear delimiters
    // This preserves ALL existing content

    const separator = '\n\n' + '='.repeat(80) + '\n\n';
    const timestamp = new Date().toISOString();

    const mergedContent = [
      this.existingContent.trimEnd(),
      separator,
      '<!-- TDD_AUTOMATION_START -->',
      `<!-- Added by tdd-automation skill -->`,
      `<!-- Version: ${this.version} -->`,
      `<!-- Date: ${timestamp} -->`,
      '',
      this.buildTddSection(),
      '',
      '<!-- TDD_AUTOMATION_END -->',
    ].join('\n');

    return mergedContent;
  }

  /**
   * Build the complete TDD automation section
   * @returns {string} TDD section content
   */
  buildTddSection() {
    return `# TDD Red-Green-Refactor Automation (Auto-Installed)

## ⚠️ CRITICAL: TDD is MANDATORY for all feature development

\`\`\`yaml
tdd-automation-version: ${this.version}
tdd-enforcement-level: strict
tdd-phase-tracking: required
\`\`\`

## Development Workflow (STRICTLY ENFORCED)

When implementing ANY new feature or functionality, you MUST follow this sequence:

### Phase 1: RED (Write Failing Test First)

**ALWAYS START HERE. DO NOT SKIP.**

1. **Create or modify the test file BEFORE writing ANY implementation code**
2. Write a test that describes the expected behavior
3. Run the test: \`npm run test:tdd -- <test-file>\`
4. **VERIFY the test fails for the RIGHT reason** (not syntax error, but missing functionality)
5. Use TodoWrite to mark RED phase complete

**DO NOT proceed to implementation until test fails correctly.**

#### RED Phase Checklist:
- [ ] Test file created/modified
- [ ] Test describes expected behavior clearly
- [ ] Test executed and verified to fail
- [ ] Failure reason is correct (missing functionality, not syntax error)
- [ ] RED phase marked in TodoWrite

### Phase 2: GREEN (Minimal Implementation)

**Only after RED phase is verified:**

1. Write ONLY enough code to make the failing test pass
2. No extra features, no "while we're here" additions
3. Keep it simple and focused on passing the test
4. Run test: \`npm run test:tdd -- <test-file>\`
5. **VERIFY the test now passes**
6. Use TodoWrite to mark GREEN phase complete

#### GREEN Phase Checklist:
- [ ] Minimal code written (no extras)
- [ ] Test executed and verified to pass
- [ ] All existing tests still pass
- [ ] GREEN phase marked in TodoWrite

### Phase 3: REFACTOR (Improve Quality)

**Only after GREEN phase is verified:**

1. Improve code structure, naming, and quality
2. Extract duplicated code
3. Simplify complex logic
4. Run full test suite: \`npm run test:tdd\`
5. **VERIFY all tests still pass after refactoring**
6. Use TodoWrite to mark REFACTOR phase complete

#### REFACTOR Phase Checklist:
- [ ] Code structure improved
- [ ] Duplicated code extracted
- [ ] Complex logic simplified
- [ ] All tests still pass
- [ ] REFACTOR phase marked in TodoWrite

## Pre-Implementation TodoWrite Template (ALWAYS Use)

Before writing ANY implementation code, create a todo list with these phases:

\`\`\`markdown
[ ] RED: Write failing test for [feature name]
[ ] Verify test fails with expected error message
[ ] GREEN: Implement minimal code to pass test
[ ] Verify test passes
[ ] REFACTOR: Improve code quality (if needed)
[ ] Verify all tests still pass
\`\`\`

**Example:**
\`\`\`markdown
[ ] RED: Write failing test for user authentication
[ ] Verify test fails with "authenticateUser is not defined"
[ ] GREEN: Implement minimal authenticateUser function
[ ] Verify test passes
[ ] REFACTOR: Extract validation logic to separate function
[ ] Verify all tests still pass
\`\`\`

## Critical Rules (NEVER Violate)

- ❌ **NEVER** write implementation code before writing the test
- ❌ **NEVER** skip the RED phase verification
- ❌ **NEVER** skip the GREEN phase verification
- ❌ **NEVER** skip TodoWrite phase tracking
- ✅ **ALWAYS** run tests to verify RED and GREEN states
- ✅ **ALWAYS** use TodoWrite to track TDD phases
- ✅ **ALWAYS** create test files BEFORE implementation files
- ✅ **ALWAYS** commit tests BEFORE committing implementation
- ✅ **ALWAYS** use semantic test names: \`"should [behavior] when [condition]"\`

## Test Execution Commands

This project has been configured with TDD-optimized test scripts:

\`\`\`bash
# Run all tests once (non-watch mode)
npm run test:tdd

# Run tests in watch mode for development
npm run test:tdd:watch

# Run specific test file (RED/GREEN phase)
npm run test:tdd -- path/to/test.test.ts

# Validate TDD compliance
npm run validate:tdd
\`\`\`

## File Structure Convention

For every implementation file, there must be a corresponding test file:

\`\`\`
src/features/auth/login.ts          → Implementation
src/features/auth/login.test.ts     → Tests (created FIRST)

src/utils/validation.ts             → Implementation
src/utils/validation.test.ts        → Tests (created FIRST)
\`\`\`

## Test Naming Convention

Use the pattern: \`"should [behavior] when [condition]"\`

**Good Examples:**
- \`"should return true when email is valid"\`
- \`"should throw error when password is too short"\`
- \`"should update user profile when data is valid"\`

**Bad Examples:**
- \`"test email validation"\` (not descriptive)
- \`"it works"\` (not specific)
- \`"validates email"\` (missing condition)

## Violation Handling

If you accidentally start writing implementation before tests:

1. **STOP immediately**
2. Create the test file first
3. Write the failing test
4. Verify RED state
5. **THEN** proceed with implementation

## TDD Automation Features

This installation includes:

- ✅ **Pre-commit hooks**: Validate tests exist before committing implementation
- ✅ **Test scaffolding**: Generate test file templates with \`npm run generate:test <file>\`
- ✅ **TDD validation**: Check compliance with \`npm run validate:tdd\`
- ✅ **Rollback capability**: Restore previous CLAUDE.md if needed

## Help & Maintenance

### Check TDD Compliance
\`\`\`bash
npm run validate:tdd
\`\`\`

### Generate Test Template
\`\`\`bash
npm run generate:test src/features/auth/login.ts
\`\`\`

### Rollback This Automation
\`\`\`bash
node .tdd-automation/scripts/rollback-tdd.js
\`\`\`

### Remove TDD Section
\`\`\`bash
node .tdd-automation/scripts/remove-tdd-section.js
\`\`\`

### View Backups
\`\`\`bash
ls -lh .claude/CLAUDE.md.backup.*
\`\`\`

## Documentation

- Setup documentation: \`.tdd-automation/README.md\`
- Pre-commit hook: \`.git/hooks/pre-commit\`
- Test templates: \`.tdd-automation/templates/\`

## Success Metrics

Track these metrics to measure TDD adherence:

- Test-first adherence rate: >95%
- RED-GREEN-REFACTOR cycle completion: >90%
- Defect escape rate: <2%
- Test coverage: >80%

---

**Note:** This section was automatically added by the tdd-automation skill.
For support or to report issues, see: .tdd-automation/README.md`;
  }

  /**
   * Create standalone TDD section (for new CLAUDE.md files)
   * @returns {string} TDD section content without existing content
   */
  static createNew() {
    const merger = new ClaudeMdMerger('');
    const timestamp = new Date().toISOString();

    return [
      '<!-- TDD_AUTOMATION_START -->',
      `<!-- Added by tdd-automation skill -->`,
      `<!-- Version: 0.2.0 -->`,
      `<!-- Date: ${timestamp} -->`,
      '',
      merger.buildTddSection(),
      '',
      '<!-- TDD_AUTOMATION_END -->',
    ].join('\n');
  }
}

module.exports = ClaudeMdMerger;
