# Playwright E2E Automation

> Automated Playwright e2e testing framework with LLM-powered visual debugging, screenshot analysis, and regression testing

## Quick Start

### Trigger Phrases

Simply ask Claude Code:

```
"set up playwright testing for my app"
"help me debug UI issues with screenshots"
"create e2e tests with visual regression"
"analyze my app's UI with screenshots"
```

### What Happens

This skill will automatically:

1. **Detect your application** - Identifies React/Vite, Node.js, static sites, or full-stack apps
2. **Detect framework versions** (NEW) - Determines Tailwind v3 vs v4, React version, etc.
3. **Pre-flight validation** (NEW) - Checks app loads before running tests, catches config errors early
4. **Install Playwright** - Runs `npm init playwright@latest` with optimal configuration
5. **Generate test suite** - Creates screenshot-enabled tests with version-appropriate templates
6. **Capture screenshots** - Takes full-page screenshots at key interaction points
7. **Analyze visually** - Uses LLM vision to identify UI bugs, layout issues, accessibility problems
8. **Detect regressions** - Compares against baselines to find unexpected visual changes
9. **Generate fixes** - Produces actionable code recommendations with file:line references
10. **Export test suite** - Provides production-ready tests you can run independently

**Total time**: ~5-8 minutes (one-time setup)
**New in v0.2.0**: Version detection and pre-flight validation prevent configuration errors

## Features

### Zero-Setup Automation

No configuration required. The skill:

- Detects your framework automatically (React, Vite, Next.js, Express, etc.)
- Installs Playwright and browsers without prompts
- Generates optimal configuration based on your app type
- Creates tests following best practices
- Runs everything end-to-end

### Multi-Framework Support

Works with:

- **React/Vite** - Modern React apps with Vite dev server
- **Next.js** - Server-side rendered React applications
- **Node.js/Express** - Backend services with HTML responses
- **Static HTML/CSS/JS** - Traditional web applications
- **Full-stack** - Combined frontend + backend applications

### Version-Aware Configuration (NEW in v0.2.0)

The skill now detects installed framework versions and adapts automatically:

**Tailwind CSS**:
- **v3.x**: Uses `@tailwind base; @tailwind components; @tailwind utilities;` syntax
- **v4.x**: Uses `@import "tailwindcss";` syntax and `@tailwindcss/postcss` plugin

**React**:
- **v17**: Classic JSX transform (requires React import)
- **v18+**: Automatic JSX transform (no import needed)

**Detection Process**:
1. Reads `package.json` dependencies
2. Matches versions against compatibility database
3. Selects appropriate templates (CSS, PostCSS config, etc.)
4. Warns about breaking changes or unknown versions

**Pre-flight Validation**:
- Loads app in browser before running tests
- Monitors console for critical errors
- Matches errors against known patterns (Tailwind v4 syntax, PostCSS plugin, etc.)
- Provides specific fix steps with file:line references
- **Prevents cascade failures**: One config error won't fail all 10 tests

**Example Error Detection**:
```
❌ Pre-flight check failed: Tailwind CSS v4 syntax mismatch

Root cause: CSS file uses @tailwind directives but v4 requires @import

Fix:
1. Update src/index.css:
   Change from: @tailwind base; @tailwind components; @tailwind utilities;
   Change to: @import "tailwindcss";

2. Update postcss.config.js:
   Change from: plugins: { tailwindcss: {} }
   Change to: plugins: { '@tailwindcss/postcss': {} }

3. Restart dev server: npm run dev
```

### LLM-Powered Visual Analysis

Automatically identifies:

- **UI Bugs** - Broken layouts, overlapping elements, cut-off text
- **Accessibility Issues** - Color contrast, missing labels, improper heading hierarchy
- **Responsive Problems** - Elements not scaling, overflow on mobile
- **Visual Regressions** - Unexpected changes from baseline screenshots
- **Missing Elements** - Expected UI components not rendered

### Actionable Fix Recommendations

Generates specific fixes with:

- File paths and line numbers (`src/components/Button.tsx:45`)
- Current code snippets showing the issue
- Recommended code changes
- Explanation of why the fix works
- Priority level (critical, high, medium, low)

### Production-Ready Test Suite

Exports include:

- Organized test files following best practices
- Page object models for maintainability
- Screenshot helpers and utilities
- npm scripts for test execution
- README with usage instructions
- CI/CD integration examples

## Usage Examples

### Example 1: Initial Setup for React App

```
User: "Set up Playwright testing for my Vite React app"

Claude (via skill):
✅ Detected React + Vite application
✅ Installing Playwright...
✅ Generated playwright.config.ts with base URL http://localhost:5173
✅ Created 5 test specs covering critical journeys
✅ Captured 23 screenshots across desktop, tablet, mobile viewports
✅ Visual analysis complete: Found 3 issues (1 high, 2 medium)
✅ Generated fix recommendations in fix-recommendations.md
✅ Test suite exported to tests/e2e/

Next steps:
- Review fix-recommendations.md
- Run tests: npm run test:e2e
- Update baselines after fixes: npm run test:e2e:update-snapshots
```

### Example 2: Visual Regression Detection

```
User: "Check for visual regressions after my recent changes"

Claude (via skill):
✅ Running existing Playwright test suite...
✅ Captured 23 screenshots
✅ Comparing against baselines...

⚠️  Found 4 visual changes:
  - Home page hero section: Layout shift detected (12% difference)
  - Navigation menu: New dropdown added (expected change)
  - Contact form: Button text color changed (2% difference)
  - Footer: Logo size increased (5% difference)

📊 Visual regression report: screenshots/diffs/report.html

Would you like to:
1. Accept these changes as new baseline
2. Review specific diffs
3. Get fix recommendations for unintended changes
```

### Example 3: Bug Investigation

```
User: "Users report the checkout button is cut off on mobile"

Claude (via skill):
✅ Generating mobile viewport test...
✅ Captured screenshot: screenshots/current/checkout-mobile.png
✅ Visual analysis complete

🐛 Issue confirmed: Button text truncated on 375px viewport

Location: src/components/CheckoutButton.tsx:28

Current code:
```tsx
<button className="px-6 py-3 text-xl font-bold">
  Complete Purchase
</button>
```

Recommended fix:
```tsx
<button className="px-4 py-2 text-sm sm:text-base md:text-xl font-bold max-w-full">
  Complete Purchase
</button>
```

Reasoning: Fixed padding and font size cause overflow on narrow screens.
Added responsive sizing and max-width constraint.

Test added: tests/e2e/checkout-responsive.spec.ts
```

## What Gets Generated

After running this skill, you'll have:

```
your-project/
├── playwright.config.ts          # Playwright configuration
├── tests/
│   └── e2e/
│       ├── setup/
│       │   └── global-setup.ts   # Dev server startup
│       ├── pages/
│       │   └── *.page.ts         # Page object models
│       ├── specs/
│       │   └── *.spec.ts         # Test specifications
│       └── utils/
│           └── screenshot-helper.ts
├── screenshots/
│   ├── baselines/                # Reference images
│   ├── current/                  # Latest run
│   └── diffs/                    # Visual comparisons
├── fix-recommendations.md        # Generated fix suggestions
├── visual-analysis-report.md     # LLM analysis results
└── package.json                  # Updated with test scripts
```

## Performance

**Typical execution time** (React app with 5 critical journeys):

- Application detection: ~5 seconds
- Playwright installation: ~2-3 minutes (one-time)
- Test generation: ~30 seconds
- Test execution: ~30-60 seconds
- Visual analysis: ~1-2 minutes
- Regression comparison: ~10 seconds
- Fix generation: ~30 seconds

**Total**: ~5-8 minutes (excluding one-time Playwright install)

## CI/CD Integration

### GitHub Actions

The skill generates GitHub Actions workflow examples. Basic setup:

```yaml
name: Playwright E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-screenshots
          path: screenshots/
```

### Baseline Management

**In CI**:
- Store baselines in repository: `git add screenshots/baselines/`
- Tests fail if visual diffs exceed threshold
- Review artifacts before merging

**Locally**:
- Update baselines: `npm run test:e2e:update-snapshots`
- Commit updated baselines after review

## Advanced Usage

### Custom Test Generation

After initial setup, you can:

1. **Add more tests** - Follow the pattern in generated specs
2. **Customize viewports** - Edit playwright.config.ts
3. **Add custom assertions** - Extend screenshot helpers
4. **Configure browsers** - Enable Firefox/WebKit in config
5. **Adjust thresholds** - Modify visual diff sensitivity

### Visual Analysis Customization

The skill's analysis focuses on:

- WCAG 2.1 AA accessibility compliance (see `data/accessibility-checks.md`)
- Common UI bug patterns (see `data/common-ui-bugs.md`)
- Framework-specific best practices

### Integration with Existing Tests

This skill complements your existing test suite:

- **Unit tests** (Vitest/Jest) - Test logic and calculations
- **Integration tests** - Test component interaction
- **E2E tests** (Playwright) - Test full user workflows + visual regression

All three work together without conflicts.

## Troubleshooting

### "Application not detected"

**Solution**: Specify manually
```
"Set up Playwright for my [framework] app running on port [port]"
```

### "Dev server not running"

**Solution**: The skill will attempt to start it automatically. If that fails:
```bash
npm run dev  # Start your dev server first
```
Then re-run the skill.

### "Screenshot capture timeout"

**Solution**: Increase timeout in playwright.config.ts:
```typescript
timeout: 60000, // 60 seconds instead of default 30
```

### "Visual analysis found too many false positives"

**Solution**: Adjust the visual diff threshold:
```typescript
expect(await page.screenshot()).toMatchSnapshot({
  maxDiffPixelRatio: 0.05, // Allow 5% difference
});
```

## Requirements

- **Node.js**: >=16.0.0
- **npm**: >=7.0.0
- **Disk space**: ~500MB for Playwright browsers (one-time)
- **Memory**: ~500MB during test execution

## Best Practices

1. **Baseline management** - Commit baselines to git, update deliberately
2. **Screenshot organization** - Use .gitignore for current/diffs, keep baselines
3. **Test critical paths** - Focus on user journeys that matter (80/20 rule)
4. **Run in CI** - Catch regressions before production
5. **Review diffs carefully** - Not all changes are bugs
6. **Use semantic selectors** - Prefer getByRole over CSS selectors
7. **Capture context** - Take screenshots before AND after interactions

## Learn More

- [Playwright Documentation](https://playwright.dev/)
- [Visual Regression Testing Guide](https://playwright.dev/docs/test-snapshots)
- [Accessibility Testing](https://playwright.dev/docs/accessibility-testing)
- [CI/CD Integration](https://playwright.dev/docs/ci)

## Support

Issues with this skill? Please report at:
- [Claude Code Issues](https://github.com/anthropics/claude-code/issues)

---

**Created with**: skill-creator v0.1.0
**Skill Version**: 0.1.0
**Last Updated**: 2025-11-01
