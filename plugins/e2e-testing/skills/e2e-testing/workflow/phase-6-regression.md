# Phase 6: Regression Detection

**Purpose**: Compare current screenshots against baselines to detect changes

## Steps

### 1. Load baseline images

- Check if baselines exist in screenshots/baselines/
- If first run, current screenshots become baselines
- If baselines exist, proceed to comparison

### 2. Perform pixel-level comparison

```typescript
import { compareScreenshots } from 'playwright-core/lib/utils';

const diff = await compareScreenshots(
  baselinePath,
  currentPath,
  diffPath,
  { threshold: 0.2 } // 20% difference threshold
);
```

### 3. Generate visual diff reports

- Create side-by-side comparison images
- Highlight changed regions in red
- Calculate difference percentage
- Classify changes:
  - **Expected**: Intentional changes (new features, fixes)
  - **Suspicious**: Unintended changes requiring review
  - **Critical**: Major regressions (broken features)

### 4. Update baselines if approved

Ask user: "Accept these changes as new baseline?"
- If yes, copy current → baselines
- If no, flag as regressions needing fixes

## Output

Visual regression report with diff images:

```markdown
## Regression Report

### Changed Screenshots (3)

| Screenshot | Diff % | Classification |
|------------|--------|----------------|
| home-page | 5% | Expected |
| form-page | 25% | Suspicious |
| mobile-nav | 45% | Critical |

See screenshots/diffs/ for visual comparisons.
```

## Performance

~1-2 seconds per image pair

## Common Issues

**No baselines exist**
- Current screenshots become baselines automatically
- Message: "No baselines found. Current screenshots saved as baselines."

**False positive diffs**
- Adjust threshold (default 20%)
- Ignore dynamic content areas
- Use stable test data

## Transition

Proceed to Phase 7 (Fix Recommendation Generation)
