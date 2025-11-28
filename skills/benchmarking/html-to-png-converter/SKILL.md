---
name: html-to-png-converter
description: Use PROACTIVELY when user needs to convert HTML diagrams, charts, or documents to PNG images for papers, presentations, or documentation. Automates Playwright's screenshot command with proper file:// protocol handling, full-page capture, and output organization. Triggers on "convert HTML to PNG", "export diagram to image", "screenshot HTML file", or "make PNG from HTML". Not for live website screenshots, PDF generation, or image format conversions.
version: 0.1.0
author: Connor
category: documentation
---

# HTML to PNG Converter

## Overview

This skill automates HTML-to-PNG conversion using Playwright's CLI screenshot functionality. It handles file protocol URLs, full-page capture, and output path management for academic papers, documentation, and presentations.

**Key Capabilities**:
- **Zero-browser-launch**: Uses Playwright CLI (no script required)
- **Full-page capture**: Captures entire document, not just viewport
- **File protocol handling**: Properly constructs `file://` URLs from paths
- **Batch conversion**: Convert multiple HTML files in one operation
- **Output organization**: Consistent naming and directory structure

## When to Use This Skill

**Trigger Phrases**:
- "convert this HTML to PNG"
- "export the diagram as an image"
- "screenshot the HTML file"
- "make a PNG from the HTML"
- "turn diagram.html into diagram.png"

**Use Cases**:
- Converting HTML architecture diagrams to PNG for papers
- Exporting HTML charts/visualizations for presentations
- Creating static images from HTML reports
- Batch converting multiple HTML files to images
- Generating figures for academic publications

**NOT for**:
- Capturing live websites (use browser or dedicated tools)
- PDF generation (use Print to PDF or wkhtmltopdf)
- Image format conversions (use ImageMagick)
- Animated/interactive content capture
- Screenshots of running web applications

## Quick Reference

### Single File Conversion

```bash
# Basic usage (npx for portability)
npx playwright screenshot --full-page "file://$(pwd)/path/to/diagram.html" output.png

# Retina/high-DPI output (2x resolution for publications)
npx playwright screenshot --full-page --device-scale-factor=2 "file://$(pwd)/diagram.html" output@2x.png

# Custom viewport size (default is 1280x720)
npx playwright screenshot --full-page --viewport-size=1920,1080 "file://$(pwd)/diagram.html" output.png

# With absolute path
npx playwright screenshot --full-page "file:///Users/you/project/diagram.html" diagram.png
```

### Batch Conversion

```bash
# Convert all HTML files in a directory
for f in docs/*.html; do
  npx playwright screenshot --full-page "file://$(pwd)/$f" "${f%.html}.png"
done

# Batch with retina quality
for f in docs/*.html; do
  npx playwright screenshot --full-page --device-scale-factor=2 "file://$(pwd)/$f" "${f%.html}@2x.png"
done
```

### Common Viewport Sizes

| Size | Use Case |
|------|----------|
| `1280,720` | Default, standard diagrams |
| `1920,1080` | Full HD presentations |
| `800,600` | Compact figures |
| `2560,1440` | Large architecture diagrams |

## Workflow

### Phase 1: Prerequisite Check
Verify Playwright is installed with browsers.
→ **Details**: `workflow/phase-1-prerequisites.md`

### Phase 2: Path Resolution
Construct proper file:// URLs from relative/absolute paths.
→ **Details**: `workflow/phase-2-paths.md`

### Phase 3: Screenshot Capture
Execute Playwright screenshot command with options.
→ **Details**: `workflow/phase-3-capture.md`

### Phase 4: Output Verification
Verify PNG was created and check dimensions/quality.
→ **Details**: `workflow/phase-4-verification.md`

## Important Reminders

1. **Always use file:// protocol** - Playwright requires full URLs
2. **Use --full-page flag** - Without it, only captures viewport (800x600)
3. **Absolute paths are safer** - Use `$(pwd)` or full paths to avoid issues
4. **Check browser installation** - Run `playwright install` if needed
5. **HTML must be self-contained** - External resources need absolute paths

## Troubleshooting Quick Reference

| Issue | Cause | Solution |
|-------|-------|----------|
| "Browser not found" | Browsers not installed | `npx playwright install` |
| Blank/white image | File path wrong | Check file:// URL format |
| Partial capture | Missing --full-page | Add `--full-page` flag |
| Missing images/CSS | Relative paths in HTML | Use absolute paths or embed |
| Command not found | Playwright not in PATH | Use `npx playwright screenshot` |
| Image too small/blurry | Standard resolution | Add `--device-scale-factor=2` for retina |
| Wrong dimensions | Default viewport | Use `--viewport-size=WIDTH,HEIGHT` |

→ **Full troubleshooting**: `reference/troubleshooting.md`

## Success Criteria

- [ ] Playwright installed and accessible
- [ ] HTML file path correctly resolved
- [ ] file:// URL properly constructed
- [ ] Screenshot command executed successfully
- [ ] PNG file created at expected location
- [ ] Image dimensions match content (not 800x600 viewport)
- [ ] All visual elements rendered correctly

## Limitations

- Requires Node.js and Playwright installed
- First run downloads browsers (~500MB)
- Cannot capture dynamic/animated content
- External resources in HTML may not load correctly
- Very large HTML files may take longer to render

## Related Skills

- **html-diagram-creator**: Create HTML diagrams for conversion to PNG
- **markdown-to-pdf-converter**: Full document pipeline (diagrams embedded in PDFs)

## Reference Materials

| Resource | Purpose |
|----------|---------|
| `workflow/*.md` | Detailed phase instructions |
| `reference/troubleshooting.md` | Common issues and fixes |
| `reference/playwright-cli.md` | Full CLI options reference |
| `examples/` | Sample conversion commands |

---

**Total time**: ~5 seconds per conversion (after initial setup)
