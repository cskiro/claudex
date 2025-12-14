# Accessibility Audit

WCAG 2.2 Level AA accessibility auditing with risk-based severity scoring for React/TypeScript applications.

## Overview

This skill provides comprehensive accessibility auditing that goes beyond simple WCAG conformance checking. It uses a **risk-based severity model** where Severity = Impact x Likelihood, meaning a Level A failure can be LOW severity while a Level AA failure can be CRITICAL.

## Key Features

- **Risk-based severity scoring** - Prioritizes issues by real user impact
- **MUI framework awareness** - Avoids false positives on built-in accessibility features
- **Multi-layer analysis** - Static (ESLint), runtime (jest-axe, Playwright), and manual validation
- **Actionable output** - Gap reports with remediation priorities

## Quick Start

```bash
# Install required tooling
npm install --save-dev eslint-plugin-jsx-a11y jest-axe @axe-core/playwright

# Run audit
# Use trigger: "Run accessibility audit on [component/page]"
```

## Trigger Phrases

- "accessibility audit"
- "WCAG compliance"
- "a11y review"
- "screen reader"
- "keyboard navigation"
- "color contrast"

## Severity Levels

| Severity | Impact | Examples |
|----------|--------|----------|
| Critical | Blocks access | Keyboard traps, missing alt on actions |
| High | Significantly degrades UX | Poor contrast on CTAs, no skip navigation |
| Medium | Minor usability impact | Missing autocomplete, unclear link text |
| Low | Best practice | Could add tooltips, more descriptive titles |

## Related Skills

- `codebase-auditor` - General code quality analysis
- `bulletproof-react-auditor` - React architecture review

## Documentation

See [SKILL.md](SKILL.md) for the complete workflow and reference materials.
