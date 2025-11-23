---
name: playwright-e2e-automation
description: Use PROACTIVELY when setting up e2e testing, debugging UI issues, or creating regression test suites. Automated Playwright framework with LLM-powered visual analysis, screenshot capture, and fix recommendations with file:line references. Zero-setup for React/Vite, Node.js, static sites, and full-stack applications. Not for unit testing, API-only testing, or mobile native apps.
---

# Playwright E2E Automation

## Overview

This skill automates the complete Playwright e2e testing lifecycle with LLM-powered visual debugging. It detects your app type, installs Playwright, generates tests, captures screenshots, analyzes for UI bugs, and produces fix recommendations with file paths and line numbers.

**Key Capabilities**:
- Zero-setup automation with multi-framework support
- Visual debugging with screenshot capture and LLM analysis
- Regression testing with baseline comparison
- Actionable fix recommendations with file:line references
- CI/CD ready test suite export

## When to Use This Skill

**Trigger Phrases**:
- "set up playwright testing for my app"
- "help me debug UI issues with screenshots"
- "create e2e tests with visual regression"
- "analyze my app's UI with screenshots"
- "generate playwright tests for [my app]"

**Use Cases**:
- Setting up Playwright testing from scratch
- Debugging visual/UI bugs hard to describe in text
- Creating screenshot-based regression testing
- Generating e2e test suites for new applications
- Identifying accessibility issues through visual inspection

**NOT for**:
- Unit testing or component testing (use Vitest/Jest)
- API-only testing without UI
- Performance/load testing
- Mobile native app testing (use Detox/Appium)

## Response Style

- **Automated**: Execute entire workflow with minimal user intervention
- **Informative**: Clear progress updates at each phase
- **Visual**: Always capture and analyze screenshots
- **Actionable**: Generate specific fixes with file paths and line numbers

## Quick Decision Matrix

| User Request | Action | Reference |
|--------------|--------|-----------|
| "set up playwright" | Full setup workflow | `workflow/phase-1-discovery.md` → `phase-2-setup.md` |
| "debug UI issues" | Capture + Analyze | `workflow/phase-4-capture.md` → `phase-5-analysis.md` |
| "check for regressions" | Compare baselines | `workflow/phase-6-regression.md` |
| "generate fix recommendations" | Analyze + Generate | `workflow/phase-7-fixes.md` |
| "export test suite" | Package for CI/CD | `workflow/phase-8-export.md` |

## Workflow Overview

### Phase 1: Application Discovery
Detect app type, framework versions, and optimal configuration.
→ **Details**: `workflow/phase-1-discovery.md`

### Phase 2: Playwright Setup
Install Playwright and generate configuration.
→ **Details**: `workflow/phase-2-setup.md`

### Phase 2.5: Pre-flight Health Check
Validate app loads correctly before full test suite.
→ **Details**: `workflow/phase-2.5-preflight.md`

### Phase 3: Test Generation
Create screenshot-enabled tests for critical workflows.
→ **Details**: `workflow/phase-3-generation.md`

### Phase 4: Screenshot Capture
Run tests and capture visual data.
→ **Details**: `workflow/phase-4-capture.md`

### Phase 5: Visual Analysis
LLM-powered analysis to identify UI bugs.
→ **Details**: `workflow/phase-5-analysis.md`

### Phase 6: Regression Detection
Compare screenshots against baselines.
→ **Details**: `workflow/phase-6-regression.md`

### Phase 7: Fix Generation
Map issues to source code with actionable fixes.
→ **Details**: `workflow/phase-7-fixes.md`

### Phase 8: Test Suite Export
Package production-ready test suite.
→ **Details**: `workflow/phase-8-export.md`

## Important Reminders

1. **Capture before AND after interactions** - Provides context for visual debugging
2. **Use semantic selectors** - Prefer getByRole, getByLabel over CSS selectors
3. **Baseline management is critical** - Keep in sync with intentional UI changes
4. **LLM analysis is supplementary** - Use alongside automated assertions
5. **Test critical paths first** - Focus on user journeys that matter most (80/20 rule)
6. **Screenshots are large** - Consider .gitignore for screenshots/, use CI artifacts
7. **Run tests in CI** - Catch visual regressions before production
8. **Update baselines deliberately** - Review diffs carefully before accepting

## Limitations

- Requires Node.js >= 16
- Browser download needs ~500MB disk space
- Screenshot comparison requires consistent rendering (may vary across OS)
- LLM analysis adds ~5-10 seconds per screenshot
- Not suitable for testing behind VPNs without additional configuration

## Reference Materials

| Resource | Purpose |
|----------|---------|
| `workflow/*.md` | Detailed phase instructions |
| `reference/troubleshooting.md` | Common issues and fixes |
| `reference/ci-cd-integration.md` | GitHub Actions, GitLab CI examples |
| `data/framework-versions.yaml` | Version compatibility database |
| `data/error-patterns.yaml` | Known error patterns with recovery |
| `templates/` | Config and test templates |
| `examples/` | Sample setups for different frameworks |

## Success Criteria

- [ ] Playwright installed with browsers
- [ ] Configuration generated for app type
- [ ] Test suite created (3-5 critical journey tests)
- [ ] Screenshots captured and organized
- [ ] Visual analysis completed with issue categorization
- [ ] Regression comparison performed
- [ ] Fix recommendations generated
- [ ] Test suite exported with documentation
- [ ] All tests executable via `npm run test:e2e`

---

**Total time**: ~5-8 minutes (excluding one-time Playwright install)
