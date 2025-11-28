---
name: accessibility-audit
version: 0.1.0
description: WCAG 2.2 Level AA accessibility auditing with risk-based severity scoring
author: Connor
created: 2025-10-04
updated: 2025-11-24
triggers:
  - accessibility audit
  - WCAG compliance
  - a11y review
  - screen reader
  - keyboard navigation
  - color contrast
  - aria attributes
---

# Accessibility Audit Skill

Comprehensive WCAG 2.2 Level AA accessibility auditing for React/TypeScript applications with MUI framework awareness.

## Quick Reference

| Severity | Impact | Examples |
|----------|--------|----------|
| **Critical** | Blocks access completely | Keyboard traps, missing alt on actions, no focus visible |
| **High** | Significantly degrades UX | Poor contrast on CTAs, no skip navigation, small touch targets |
| **Medium** | Minor usability impact | Missing autocomplete, unclear link text |
| **Low** | Best practice enhancement | Could add tooltips, more descriptive titles |

## Key Principle

> **Severity = Impact x Likelihood**, NOT WCAG conformance level.
> A Level A failure can be LOW severity; a Level AA failure can be CRITICAL.

## Required Tooling

```bash
# Install required tools
npm install --save-dev eslint-plugin-jsx-a11y jest-axe @axe-core/playwright

# Configure ESLint
# Add to .eslintrc: extends: ['plugin:jsx-a11y/recommended']
```

## Workflow

1. **[Setup & Preparation](workflow/setup.md)** - Install tooling, create output directories
2. **[Static Analysis](workflow/static-analysis.md)** - ESLint jsx-a11y scan
3. **[Runtime Analysis](workflow/runtime-analysis.md)** - jest-axe and Playwright
4. **[Manual Validation](workflow/manual-validation.md)** - Keyboard, screen reader, contrast
5. **[Report Generation](workflow/reporting.md)** - JSON + Markdown outputs

## Reference

- **[Severity Rubric](reference/severity-rubric.md)** - Impact x Likelihood calculation
- **[WCAG Criteria](reference/wcag-criteria.md)** - All 60 Level AA criteria with interpretations
- **[MUI Framework](reference/mui-awareness.md)** - Built-in accessibility features (avoid false positives)
- **[Tooling Guide](reference/tooling.md)** - ESLint, jest-axe, Playwright configuration
- **[Output Schemas](reference/output-schemas.md)** - JSON schema for gap reports

## Examples

- **[Gap Report](examples/gap-report.md)** - Sample accessibility findings
- **[Remediation Plan](examples/remediation-plan.md)** - Prioritized fix list

## Common False Positives to Avoid

| Component | Built-in Behavior | Don't Flag |
|-----------|-------------------|------------|
| MUI `<SvgIcon>` | Auto `aria-hidden="true"` | Icons without titleAccess |
| MUI `<Alert>` | Default `role="alert"` | Missing role attribute |
| MUI `<Button>` | 36.5px min height | Target size < 44px |
| MUI `<TextField>` | Auto label association | Missing label |
| MUI `<Autocomplete>` | Manages ARIA attrs | Missing aria-expanded |

## Quick Audit Command

```
Run accessibility audit on [component/page] following WCAG 2.2 AA standards
```

---

**Source**: Migrated from `~/.claude/protocols/ACCESSIBILITY_AUDIT.yaml` v2.0.0
