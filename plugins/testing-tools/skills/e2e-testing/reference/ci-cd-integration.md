# CI/CD Integration

## GitHub Actions Example

```yaml
name: Playwright E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npm run test:e2e

      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-screenshots
          path: screenshots/

      - name: Upload HTML report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

## Baseline Management in CI

### 1. Store baselines in repository

```bash
git add screenshots/baselines/
git commit -m "chore: update visual regression baselines"
```

### 2. Update baselines on approval

1. Run tests locally: `npm run test:e2e`
2. Review diffs: `npx playwright show-report`
3. Update baselines: `npm run test:e2e:update-snapshots`
4. Commit updated baselines

### 3. Fail CI on visual regressions

- Configure threshold in playwright.config.ts
- Tests fail if diffs exceed threshold
- Review in CI artifacts before merging

## GitLab CI Example

```yaml
e2e-tests:
  image: mcr.microsoft.com/playwright:v1.40.0-jammy
  stage: test
  script:
    - npm ci
    - npm run test:e2e
  artifacts:
    when: always
    paths:
      - screenshots/
      - playwright-report/
    expire_in: 7 days
```

## CircleCI Example

```yaml
version: 2.1
jobs:
  e2e-tests:
    docker:
      - image: mcr.microsoft.com/playwright:v1.40.0-jammy
    steps:
      - checkout
      - run: npm ci
      - run: npm run test:e2e
      - store_artifacts:
          path: screenshots
      - store_artifacts:
          path: playwright-report
```

## Best Practices

### Screenshot Artifact Storage

- Always upload screenshots as artifacts
- Keep artifacts for at least 7 days
- Consider cloud storage for long-term retention

### Parallel Execution

```yaml
# Run tests across multiple shards
- name: Run Playwright tests
  run: npx playwright test --shard=${{ matrix.shard }}/${{ strategy.job-total }}
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
```

### Caching

```yaml
- name: Cache Playwright browsers
  uses: actions/cache@v3
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ hashFiles('package-lock.json') }}
```

### Notifications

Configure notifications for test failures:
- Slack integration
- Email alerts
- PR comments with screenshot diffs
