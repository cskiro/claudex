# Phase 4: Output Verification

## Overview

After conversion, verify the PNG was created correctly with expected dimensions and content.

## Verification Steps

### 4.1 Check File Exists

```bash
# Verify file was created
test -f output.png && echo "PNG created successfully" || echo "ERROR: PNG not found"
```

### 4.2 Check File Size

```bash
# Non-zero file size indicates content
ls -lh output.png

# If file is very small (<1KB), something may be wrong
```

### 4.3 Check Dimensions (macOS)

```bash
# Using sips (built into macOS)
sips -g pixelHeight -g pixelWidth output.png
```

**Expected output**:
```
  pixelHeight: 1200
  pixelWidth: 800
```

**Warning signs**:
- 800x600 = viewport-only capture (missing `--full-page`)
- Very small dimensions = content not rendering

### 4.4 Visual Inspection

```bash
# Open in default image viewer (macOS)
open output.png

# Or in Preview specifically
open -a Preview output.png
```

## Common Issues and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| 800x600 dimensions | No `--full-page` | Add `--full-page` flag |
| Blank/white image | Wrong file path | Check `file://` URL |
| Missing images | Relative paths in HTML | Use absolute paths or embed base64 |
| Cut off content | Viewport too small | Use `--full-page` or increase viewport |
| Fuzzy text | Low DPI | Add `--scale=2` for retina |

## Quality Checks

- [ ] File exists and has reasonable size (>10KB for diagrams)
- [ ] Dimensions match content (not 800x600)
- [ ] All visual elements rendered (text, colors, borders)
- [ ] No blank areas or missing components
- [ ] Text is readable and sharp

## Retina/High-DPI Output

For sharper images (publications):

```bash
# 2x scale for retina
playwright screenshot --full-page --scale=2 "file://$(pwd)/diagram.html" diagram@2x.png
```

## Cleanup

```bash
# Remove test files if any
rm -f test.png
```
