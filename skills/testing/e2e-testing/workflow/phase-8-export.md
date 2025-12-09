# Phase 8: Test Suite Export

**Purpose**: Provide production-ready test suite for ongoing use

## Steps

### 1. Export test files

- Copy generated tests to project's tests/ directory
- Ensure proper TypeScript types and imports
- Add comments explaining test purpose

### 2. Create README documentation

```markdown
# Playwright E2E Test Suite

## Running Tests
```bash
npm run test:e2e              # Run all e2e tests
npm run test:e2e:headed       # Run with browser UI
npm run test:e2e:debug        # Run with Playwright Inspector
```

## Screenshot Management
- Baselines: `screenshots/baselines/`
- Current: `screenshots/current/`
- Diffs: `screenshots/diffs/`

## Updating Baselines
```bash
npm run test:e2e:update-snapshots
```
```

### 3. Add npm scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:update-snapshots": "playwright test --update-snapshots"
  }
}
```

### 4. Document CI/CD integration

- Provide GitHub Actions workflow example
- Explain screenshot artifact storage
- Show how to update baselines in CI
- Configure Playwright HTML reporter for CI

See `reference/ci-cd-integration.md` for complete examples.

## Output

Complete, documented test suite ready for development workflow:
- Tests in `tests/` directory
- README with usage instructions
- npm scripts configured
- CI/CD documentation

## Common Issues

**Tests don't run after export**
- Check TypeScript types
- Verify imports are correct
- Ensure Playwright is in dependencies

**CI/CD integration issues**
- See `reference/ci-cd-integration.md`
- Check browser installation in CI

## Success Criteria

- [ ] Test suite exported to project
- [ ] All tests executable via npm run test:e2e
- [ ] README includes usage instructions
- [ ] CI/CD guidance documented
