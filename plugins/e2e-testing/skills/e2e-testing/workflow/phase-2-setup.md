# Phase 2: Playwright Installation & Setup

**Purpose**: Install Playwright and generate optimal configuration

## Steps

### 1. Install Playwright

```bash
npm init playwright@latest -- --yes
# Installs Playwright, test runners, and browsers (Chromium, Firefox, WebKit)
```

### 2. Generate playwright.config.ts

Configure based on app type:
- Set base URL (http://localhost:5173 for Vite, etc.)
- Configure viewport sizes:
  - Desktop: 1280x720
  - Tablet: 768x1024
  - Mobile: 375x667
- Set screenshot directory: `screenshots/{test-name}/{timestamp}/`
- Enable trace on failure for debugging
- Configure retries (2 attempts) and timeout (30s)

### 3. Set up directory structure

```
tests/
├── setup/
│   └── global-setup.ts    # Start dev server
├── pages/
│   └── *.page.ts         # Page object models
├── specs/
│   └── *.spec.ts         # Test specifications
└── utils/
    └── screenshot-helper.ts

screenshots/
├── baselines/            # Reference images
├── current/              # Latest test run
└── diffs/                # Visual comparisons
```

### 4. Integrate with existing test setup

- Add playwright scripts to package.json
- Configure alongside Vitest/Jest (no conflicts)
- Set up TypeScript types for Playwright

## Output

Fully configured Playwright environment with version-appropriate templates

## Performance

~2-3 minutes for installation and setup (one-time)

## Common Issues

**Installation fails**
- Check Node version (>=16)
- Retry with --force
- Suggest manual installation if network issues

**Browser download fails**
- Check disk space (~500MB needed)
- Try installing specific browser: `npx playwright install chromium`

## Transition

Proceed to Phase 2.5 (Pre-flight Health Check)
