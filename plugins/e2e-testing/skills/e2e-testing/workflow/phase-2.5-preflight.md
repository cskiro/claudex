# Phase 2.5: Pre-flight Health Check

**Purpose**: Validate app loads correctly before running full test suite - catches configuration errors early

## Steps

### 1. Launch browser and attempt to load app

```typescript
const browser = await chromium.launch();
const page = await browser.newPage();

try {
  const response = await page.goto(baseURL, { timeout: 30000 });

  if (!response || !response.ok()) {
    throw new Error(`App returned ${response?.status()}`);
  }
} catch (error) {
  // Analyze error and provide guidance
}
```

### 2. Monitor console for critical errors

- Listen for console errors during page load
- Collect all error messages for pattern analysis
- Wait 2-3 seconds to let errors surface

### 3. Analyze errors against known patterns

Load `data/error-patterns.yaml` error database and match against known patterns:

**Example patterns detected**:
- Tailwind v4 syntax mismatch: "Cannot apply unknown utility class"
- PostCSS plugin error: "Plugin tailwindcss not found"
- Missing dependencies: "Module not found"

### 4. Provide actionable diagnostics

```
❌ Pre-flight check failed: Critical errors detected

Issue: Tailwind CSS v4 syntax mismatch
Root cause: CSS file uses @tailwind directives but v4 requires @import

Fix:
1. Update src/index.css (or globals.css):
   Change from: @tailwind base; @tailwind components; @tailwind utilities;
   Change to: @import "tailwindcss";

2. Update postcss.config.js:
   Change from: plugins: { tailwindcss: {} }
   Change to: plugins: { '@tailwindcss/postcss': {} }

3. Restart dev server: npm run dev

Documentation: https://tailwindcss.com/docs/upgrade-guide
```

### 5. Auto-fix if possible, otherwise halt with guidance

- For known issues with clear fixes, offer to fix automatically
- For ambiguous issues, halt and require user intervention
- Prevent running 10+ tests that will all fail due to one config issue

## Error Pattern Analysis

```typescript
function analyzeErrors(consoleErrors) {
  const errorPatterns = parseYAML('data/error-patterns.yaml');
  const issues = [];

  for (const error of consoleErrors) {
    for (const [name, pattern] of Object.entries(errorPatterns.css_errors)) {
      if (pattern.pattern.test(error) ||
          pattern.alternative_patterns?.some(alt => alt.test(error))) {
        issues.push({
          name,
          severity: pattern.severity,
          diagnosis: pattern.diagnosis,
          recovery_steps: pattern.recovery_steps,
          documentation: pattern.documentation,
        });
      }
    }
  }

  return {
    critical: issues.filter(i => i.severity === 'critical'),
    allIssues: issues,
  };
}
```

## Benefits

- **Fast feedback**: 2-3 seconds vs 30+ seconds for full test suite
- **Clear guidance**: Specific fix steps, not generic "tests failed"
- **Prevents cascade failures**: One config error won't fail all 10 tests
- **Educational**: Explains what went wrong and why

## Output

Health check passed, or detailed error diagnostics with fix steps

## Performance

~2-5 seconds

## Transition

If health check passes, proceed to Phase 3 (Test Generation). If fails, provide fixes and halt.
