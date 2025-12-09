# Installation Steps

## Detailed Installation Process

When you invoke this skill, it executes the following steps:

### 1. Detect Project Configuration
- Identify test framework (Vitest, Jest, Mocha, AVA)
- Check for TypeScript/JavaScript
- Validate git repository exists

### 2. Configure CLAUDE.md Safely
- Create automatic backup before any changes
- Merge test workflow requirements (preserves existing content)
- Add clear section markers for identification

### 3. Install npm Scripts
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

### 4. Install Git Hooks
- Pre-commit hook validates tests exist
- Prevents commits without tests
- Enforces test-first workflow

### 5. Create Helper Scripts
- Test template generator
- Compliance validator
- Rollback utility
- Section removal utility

## Behavior After Installation

Once installed, when you say something like:
```
"Implement user authentication"
```

Claude will **automatically**:

1. Create todo list with test phases:
   - [ ] RED: Write failing test for user authentication
   - [ ] Verify test fails with expected error
   - [ ] GREEN: Implement minimal authentication logic
   - [ ] Verify test passes
   - [ ] REFACTOR: Improve code quality
   - [ ] Verify all tests still pass

2. Create test file FIRST:
   `src/auth/authenticate.test.ts`

3. Write failing test with clear description

4. Run test and verify RED state:
   ```bash
   npm run test:red -- src/auth/authenticate.test.ts
   ```

5. Implement minimal code:
   `src/auth/authenticate.ts`

6. Run test and verify GREEN state:
   ```bash
   npm run test:green -- src/auth/authenticate.test.ts
   ```

7. Refactor if needed while keeping tests green

8. Final validation:
   ```bash
   npm run test:tdd
   ```
