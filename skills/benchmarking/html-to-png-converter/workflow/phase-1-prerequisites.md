# Phase 1: Prerequisites Check

## Overview

Before converting HTML to PNG, verify Playwright is installed and browsers are available.

## Steps

### 1.1 Check Playwright Installation

```bash
# Check if playwright is available
playwright --version
```

**If not found**:
```bash
# Install globally
npm install -g playwright

# Or use via npx (no global install)
npx playwright --version
```

### 1.2 Install Browsers

```bash
# Install all browsers
playwright install

# Or just Chromium (smallest, ~150MB)
playwright install chromium
```

### 1.3 Verify Setup

```bash
# Quick test - should create a PNG of example.com
playwright screenshot https://example.com test.png && rm test.png
echo "Playwright setup verified!"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `command not found: playwright` | `npm install -g playwright` or use `npx playwright` |
| Browser not found | Run `playwright install chromium` |
| Permission denied | Use `sudo npm install -g playwright` or fix npm permissions |

## Next Phase

Once prerequisites are verified, proceed to **Phase 2: Path Resolution**.
