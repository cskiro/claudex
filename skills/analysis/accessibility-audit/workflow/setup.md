# Phase 1: Setup & Preparation

## Required Tooling Installation

### Static Analysis (Required)
```bash
npm install --save-dev eslint-plugin-jsx-a11y
```

Configure `.eslintrc.js`:
```javascript
module.exports = {
  extends: ['plugin:jsx-a11y/recommended'],
  // ... other config
};
```

### Runtime Analysis (Required)
```bash
npm install --save-dev jest-axe @axe-core/react
```

### E2E Analysis (Required)
```bash
npm install --save-dev @axe-core/playwright
```

### Optional Tools
```bash
npm install --save-dev @storybook/addon-a11y pa11y-ci
```

## Verification Commands

```bash
# Verify installations
npm list eslint-plugin-jsx-a11y jest-axe @axe-core/playwright

# Check ESLint config
grep -l "jsx-a11y" .eslintrc* 2>/dev/null || echo "jsx-a11y not configured"
```

## Output Directory Setup

```bash
mkdir -p docs/accessibility
```

## Prepare Report Templates

### Gap Report JSON Structure
```json
{
  "meta": {
    "project": "PROJECT_NAME",
    "auditDate": "YYYY-MM-DD",
    "auditor": "Claude Code",
    "protocolVersion": "2.0.0",
    "wcagVersion": "2.2",
    "wcagLevel": "AA"
  },
  "summary": {
    "totalCriteria": 60,
    "passing": 0,
    "failing": 0,
    "notApplicable": 0,
    "compliancePercentage": 0,
    "severityBreakdown": {
      "critical": 0,
      "high": 0,
      "medium": 0,
      "low": 0
    }
  },
  "findings": []
}
```

## Pre-Audit Checklist

- [ ] eslint-plugin-jsx-a11y installed and configured
- [ ] jest-axe available for component tests
- [ ] @axe-core/playwright available for E2E tests
- [ ] docs/accessibility/ directory exists
- [ ] Project uses React + TypeScript (protocol optimized for this stack)

## Next Step

Proceed to [Static Analysis](static-analysis.md)
