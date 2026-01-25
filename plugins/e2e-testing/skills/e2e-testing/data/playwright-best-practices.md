# Playwright Best Practices

Official best practices for Playwright test automation, optimized for LLM-assisted development.

## Test Structure

### Use Page Object Models (POM)

**Why**: Separates page structure from test logic, improves maintainability

```typescript
// Good: Page Object Model
// pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.page.getByLabel('Username').fill(username);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
  }
}

// specs/login.spec.ts
test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### Use Semantic Selectors

**Priority order** (most stable → least stable):

1. **getByRole** - Accessible role (button, heading, textbox, etc.)
2. **getByLabel** - Form inputs with associated labels
3. **getByPlaceholder** - Input placeholder text
4. **getByText** - User-visible text content
5. **getByTestId** - data-testid attributes (last resort)

```typescript
// Best: Role-based (accessible and stable)
await page.getByRole('button', { name: 'Submit' }).click();

// Good: Label-based (for forms)
await page.getByLabel('Email address').fill('user@example.com');

// Acceptable: Text-based
await page.getByText('Continue to checkout').click();

// Avoid: CSS selectors (brittle)
await page.click('.btn-primary');  // ❌ Breaks if class changes

// Last resort: Test IDs (when semantic selectors don't work)
await page.getByTestId('checkout-button').click();
```

## Screenshot Best Practices

### When to Capture Screenshots

1. **Initial page load** - Baseline visual state
2. **Before interaction** - Pre-state for comparison
3. **After interaction** - Result of user action
4. **Error states** - When validation fails or errors occur
5. **Success states** - Confirmation screens, success messages
6. **Test failures** - Automatic capture for debugging

### Screenshot Naming Convention

```typescript
// Pattern: {test-name}-{viewport}-{state}-{timestamp}.png

await page.screenshot({
  path: `screenshots/current/login-desktop-initial-${Date.now()}.png`,
  fullPage: true
});

await page.screenshot({
  path: `screenshots/current/checkout-mobile-error-${Date.now()}.png`,
  fullPage: true
});
```

### Full-Page vs Element Screenshots

```typescript
// Full-page: For layout and overall UI analysis
await page.screenshot({
  path: 'homepage-full.png',
  fullPage: true  // Captures entire scrollable page
});

// Element-specific: For component testing
const button = page.getByRole('button', { name: 'Submit' });
await button.screenshot({
  path: 'submit-button.png'
});
```

## Waiting and Timing

### Auto-Waiting

Playwright automatically waits for:
- Element to be attached to DOM
- Element to be visible
- Element to be stable (not animating)
- Element to receive events (not obscured)
- Element to be enabled

```typescript
// This automatically waits for button to be clickable
await page.getByRole('button', { name: 'Submit' }).click();
```

### Explicit Waits (when needed)

```typescript
// Wait for navigation
await page.waitForURL('/dashboard');

// Wait for network idle (good before screenshots)
await page.waitForLoadState('networkidle');

// Wait for specific element
await page.waitForSelector('img[alt="Profile picture"]');

// Wait for custom condition
await page.waitForFunction(() => window.scrollY === 0);
```

### Avoid Fixed Timeouts

```typescript
// Bad: Arbitrary delays
await page.waitForTimeout(3000);  // ❌ Flaky, slow

// Good: Wait for specific condition
await expect(page.getByText('Success')).toBeVisible();  // ✅ Fast and reliable
```

## Test Isolation

### Independent Tests

Each test should be completely independent:

```typescript
// Good: Test is self-contained
test('user can add item to cart', async ({ page }) => {
  // Set up: Create user, log in
  await page.goto('/');
  await login(page, 'user@example.com', 'password');

  // Action: Add to cart
  await page.getByRole('button', { name: 'Add to cart' }).click();

  // Assert: Item in cart
  await expect(page.getByTestId('cart-count')).toHaveText('1');

  // Cleanup happens automatically with new page context
});

// Bad: Depends on previous test state
test('user can checkout', async ({ page }) => {
  // ❌ Assumes cart already has items from previous test
  await page.goto('/checkout');
  // ...
});
```

### Use test.beforeEach for Common Setup

```typescript
test.describe('Shopping cart', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await login(page, 'user@example.com', 'password');
  });

  test('can add item to cart', async ({ page }) => {
    // Setup already done
    await page.getByRole('button', { name: 'Add to cart' }).click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');
  });

  test('can remove item from cart', async ({ page }) => {
    // Setup already done, fresh state
    await page.getByRole('button', { name: 'Add to cart' }).click();
    await page.getByRole('button', { name: 'Remove' }).click();
    await expect(page.getByTestId('cart-count')).toHaveText('0');
  });
});
```

## Visual Regression Testing

### Snapshot Testing

```typescript
// Basic snapshot
await expect(page).toHaveScreenshot('homepage.png');

// With threshold (allow minor differences)
await expect(page).toHaveScreenshot('homepage.png', {
  maxDiffPixelRatio: 0.05  // Allow 5% difference
});

// Element snapshot
const card = page.getByRole('article').first();
await expect(card).toHaveScreenshot('product-card.png');
```

### Updating Baselines

```bash
# Update all snapshots
npx playwright test --update-snapshots

# Update specific test
npx playwright test login.spec.ts --update-snapshots
```

### Baseline Management

- **Store baselines in git** - Commit to repository for consistency
- **Review diffs carefully** - Not all changes are bugs
- **Update deliberately** - Only update when changes are intentional
- **Use CI checks** - Fail pipeline on unexpected visual changes

## Configuration Best Practices

### playwright.config.ts Essentials

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',

  // Timeout for each test
  timeout: 30 * 1000,

  // Global setup/teardown
  globalSetup: require.resolve('./tests/setup/global-setup.ts'),

  // Fail fast on CI, retry locally
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,

  // Parallel execution
  workers: process.env.CI ? 1 : undefined,

  // Reporter
  reporter: process.env.CI ? 'github' : 'html',

  use: {
    // Base URL
    baseURL: 'http://localhost:5173',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Trace on first retry
    trace: 'on-first-retry',

    // Video on failure
    video: 'retain-on-failure',
  },

  // Projects for multi-browser testing
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 13'] },
    },
  ],

  // Web server for dev
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Debugging

### Playwright Inspector

```bash
# Debug specific test
npx playwright test --debug login.spec.ts

# Debug from specific line
npx playwright test --debug --grep "user can login"
```

### VS Code Debugger

```json
// .vscode/launch.json
{
  "configurations": [
    {
      "name": "Debug Playwright Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/@playwright/test/cli.js",
      "args": ["test", "--headed", "${file}"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Trace Viewer

```bash
# Run with trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

## Performance Optimization

### Parallel Execution

```typescript
// Run tests in parallel (default)
test.describe.configure({ mode: 'parallel' });

// Run tests serially (when needed)
test.describe.configure({ mode: 'serial' });
```

### Reuse Authentication State

```typescript
// global-setup.ts
import { chromium } from '@playwright/test';

export default async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('http://localhost:5173/login');
  await page.getByLabel('Username').fill('admin');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Save authentication state
  await page.context().storageState({ path: 'auth.json' });
  await browser.close();
}

// Use in tests
test.use({ storageState: 'auth.json' });
```

## Common Pitfalls to Avoid

### 1. Not Waiting for Network Idle Before Screenshots

```typescript
// Bad: Screenshot may capture loading state
await page.goto('/dashboard');
await page.screenshot({ path: 'dashboard.png' });

// Good: Wait for content to load
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
await page.screenshot({ path: 'dashboard.png' });
```

### 2. Using Non-Stable Selectors

```typescript
// Bad: Position-based (breaks if order changes)
await page.locator('button').nth(2).click();

// Good: Content-based
await page.getByRole('button', { name: 'Submit' }).click();
```

### 3. Not Handling Dynamic Content

```typescript
// Bad: Assumes content is already loaded
const text = await page.getByTestId('user-name').textContent();

// Good: Wait for element first
await expect(page.getByTestId('user-name')).toBeVisible();
const text = await page.getByTestId('user-name').textContent();
```

### 4. Overly Broad Assertions

```typescript
// Bad: Fails on any minor change
await expect(page).toHaveScreenshot({ maxDiffPixelRatio: 0 });

// Good: Allow reasonable tolerance
await expect(page).toHaveScreenshot({ maxDiffPixelRatio: 0.02 });
```

## Summary Checklist

- [ ] Use Page Object Models for test organization
- [ ] Prefer semantic selectors (getByRole, getByLabel)
- [ ] Capture screenshots at key interaction points
- [ ] Wait for network idle before screenshots
- [ ] Use auto-waiting instead of fixed timeouts
- [ ] Make tests independent and isolated
- [ ] Configure proper retry logic (2-3 retries in CI)
- [ ] Store authentication state for reuse
- [ ] Use trace viewer for debugging
- [ ] Review visual diffs before updating baselines
- [ ] Run tests in parallel for performance
- [ ] Enable screenshot/video on failure
- [ ] Store baselines in version control
- [ ] Use meaningful screenshot names with timestamps
- [ ] Configure appropriate visual diff thresholds

---

**References:**
- [Playwright Official Docs](https://playwright.dev/)
- [Best Practices Guide](https://playwright.dev/docs/best-practices)
- [Locators Guide](https://playwright.dev/docs/locators)
