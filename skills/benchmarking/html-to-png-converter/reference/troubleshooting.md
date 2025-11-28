# Troubleshooting Guide

## Common Issues and Solutions

### "Browser not found" / "Executable doesn't exist"

**Cause**: Playwright browsers not installed.

**Solution**:
```bash
# Install browsers
playwright install chromium

# Or install all browsers
playwright install
```

### "Command not found: playwright"

**Cause**: Playwright not installed globally.

**Solutions**:
```bash
# Option 1: Install globally
npm install -g playwright

# Option 2: Use via npx (no install needed)
npx playwright screenshot --full-page "file://$(pwd)/diagram.html" output.png
```

### Blank or White Image

**Cause**: File path not resolving correctly.

**Debug**:
```bash
# Check the file exists
ls -la diagram.html

# Check URL format (should be file://...)
echo "file://$(pwd)/diagram.html"
```

**Solution**: Ensure using `file://` protocol with absolute path.

### Image is 800x600 (Viewport Only)

**Cause**: Missing `--full-page` flag.

**Solution**:
```bash
# Add --full-page flag
playwright screenshot --full-page "file://$(pwd)/diagram.html" output.png
```

### Missing Images/CSS in Output

**Cause**: HTML uses relative paths that don't resolve in file:// context.

**Solutions**:

1. **Use absolute paths in HTML**:
```html
<!-- Instead of -->
<img src="images/logo.png">
<!-- Use -->
<img src="file:///Users/you/project/images/logo.png">
```

2. **Embed images as base64**:
```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANS...">
```

3. **Inline CSS**:
```html
<style>
  /* CSS inline instead of <link> */
</style>
```

### Fonts Not Rendering

**Cause**: Web fonts not loading in file:// context.

**Solutions**:

1. Use system fonts:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

2. Embed fonts as base64 in CSS.

### Slow Conversion

**Cause**: Browser startup overhead or large content.

**Solutions**:
```bash
# For batch operations, reuse browser (requires script)
# For single operations, ~3-5 seconds is normal

# If content is dynamic, reduce wait time
playwright screenshot --full-page --wait-for-timeout=500 "file://$(pwd)/diagram.html" output.png
```

### Permission Denied

**Cause**: Cannot write to output directory.

**Solution**:
```bash
# Check directory permissions
ls -la $(dirname output.png)

# Create directory if needed
mkdir -p docs/images
```

### Fuzzy/Blurry Text

**Cause**: Low DPI capture.

**Solution**:
```bash
# Use 2x scale for retina-quality output
playwright screenshot --full-page --scale=2 "file://$(pwd)/diagram.html" output.png
```

## Debug Mode

For detailed troubleshooting:

```bash
# Enable debug output
DEBUG=pw:api playwright screenshot --full-page "file://$(pwd)/diagram.html" output.png
```

## Getting Help

1. Check Playwright docs: https://playwright.dev/docs/cli
2. Verify HTML renders in browser: `open diagram.html`
3. Test with simple HTML first to isolate issue
