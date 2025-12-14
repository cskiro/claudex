# Troubleshooting Guide

## Framework Version Errors

### Tailwind CSS v4 Syntax Mismatch

**Symptom**: Console error "Cannot apply unknown utility class" or "Utilities must be known at build time"

**Cause**: Tailwind v4 installed but CSS uses old v3 `@tailwind` directive syntax

**Root Cause**: Breaking change in Tailwind v4 - changed from `@tailwind` to `@import` syntax

**Detection**: Pre-flight health check catches this before running tests

**Auto-fix Available**: Yes - skill detects version and uses correct template

**Manual Fix**:
```css
// Old (v3):
@tailwind base;
@tailwind components;
@tailwind utilities;

// New (v4):
@import "tailwindcss";
```

**Also Update**: `postcss.config.js` - change `tailwindcss: {}` to `'@tailwindcss/postcss': {}`

**Prevention**: Skill consults `data/framework-versions.yaml` and selects appropriate template

**Documentation**: https://tailwindcss.com/docs/upgrade-guide

---

### PostCSS Plugin Not Found

**Symptom**: Build error "Plugin tailwindcss not found" or "Cannot find module 'tailwindcss'"

**Cause**: Tailwind v4 renamed PostCSS plugin but config uses old name

**Root Cause**: PostCSS plugin changed from `tailwindcss` to `@tailwindcss/postcss` in v4

**Detection**: Pre-flight check or build error

**Auto-fix Available**: Yes - version detection selects correct PostCSS template

**Manual Fix**:
```javascript
// postcss.config.js
// Old (v3):
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

// New (v4):
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
};
```

**Verification**: Run `npm list @tailwindcss/postcss` to confirm installation

**Prevention**: Skill uses `templates/configs/postcss-tailwind-v4.js` for Tailwind v4

---

### Version Incompatibility Warning

**Symptom**: Skill warns "Unknown version detected" or "Version outside known ranges"

**Cause**: Framework version not in compatibility database

**Impact**: Skill may use outdated templates or incorrect syntax

**Solution**:
1. Check `data/framework-versions.yaml` for supported versions
2. If version is newer, skill uses latest known template (may need manual adjustment)
3. If version is older, skill may suggest upgrading

**Reporting**: Please report unknown versions as GitHub issues to improve skill

**Workaround**: Manually specify template paths if needed

---

## Common Issues

### Application not detected

**Cause**: Unrecognized framework or missing package.json

**Solution**: Ask user to specify app type and dev server command manually

**Fallback**: Use generic static site configuration

---

### Dev server not running

**Cause**: Application not started before running tests

**Solution**: Attempt to start server automatically using detected script (npm run dev)

**Fallback**: Prompt user to start server manually

---

### Playwright installation fails

**Cause**: Network issues, permissions, incompatible Node version

**Solution**:
- Check Node version (>=16)
- Retry with --force
- Suggest manual installation

**Debugging**: Show full error output, check npm logs

---

### Screenshot capture fails

**Cause**: Timeout waiting for page load, element not found, navigation error

**Solution**:
- Increase timeout
- Add explicit waits
- Capture partial screenshot on failure

**Recovery**: Continue with other tests, report failure with details

---

### No baselines exist for comparison

**Cause**: First test run, baselines deleted

**Solution**: Current screenshots become baselines automatically

**Message**: "No baselines found. Current screenshots saved as baselines."

---

### Visual analysis fails

**Cause**: LLM API error, screenshot file corruption, unsupported format

**Solution**:
- Retry analysis
- Skip corrupted images
- Validate PNG format

**Fallback**: Provide raw screenshots for manual inspection

---

## Performance Characteristics

### Execution Times (Typical React App)

| Phase | Time |
|-------|------|
| Application detection | ~5 seconds |
| Playwright installation | ~2-3 minutes (one-time) |
| Configuration generation | ~10 seconds |
| Test generation | ~30 seconds |
| Test execution (5 tests) | ~30-60 seconds |
| Screenshot capture | ~1-2 seconds per screenshot |
| Visual analysis (10 screenshots) | ~1-2 minutes |
| Regression comparison | ~10 seconds |
| Fix generation | ~30 seconds |

**Total end-to-end time**: ~5-8 minutes (excluding Playwright install)

### Resource Usage

- **Disk space**: ~500MB (Playwright browsers)
- **Memory**: ~500MB during test execution
- **Screenshots**: ~1-2MB per full-page screenshot
