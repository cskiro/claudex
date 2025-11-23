# Phase 3: Test Generation

**Purpose**: Create screenshot-enabled test suite covering critical workflows

## Steps

### 1. Generate page object models

- Create POM classes for each major page/component
- Define locators using best practices (getByRole, getByLabel, getByText)
- Add screenshot capture methods to each POM

### 2. Create test specifications

Generate tests for each critical user journey with screenshot capture at key points:
- Initial page load
- Before interaction (button click, form fill)
- After interaction
- Error states
- Success states

### 3. Add accessibility checks

- Integrate axe-core for automated a11y testing
- Capture accessibility violations in screenshots
- Generate accessibility reports

### 4. Set up screenshot helpers

```typescript
// templates/screenshot-helper.ts
export async function captureWithContext(
  page: Page,
  name: string,
  context?: string
) {
  const timestamp = new Date().toISOString();
  const path = `screenshots/current/${name}-${timestamp}.png`;
  await page.screenshot({ path, fullPage: true });
  return { path, context, timestamp };
}
```

## Output

Complete test suite with screenshot automation

## Test Coverage

Aim for critical user journeys (80/20 rule):
- Core functionality tests
- Authentication flows
- Form submissions
- Key interactions

## Common Issues

**Too many tests generated**
- Focus on critical paths
- Prioritize user journeys over edge cases

**Locators not found**
- Use semantic locators (getByRole, getByLabel)
- Add test IDs as last resort

## Transition

Proceed to Phase 4 (Screenshot Capture & Execution)
