# Phase 3: Screenshot Capture

## Overview

Execute the Playwright screenshot command with appropriate options for your use case.

## Basic Command

```bash
playwright screenshot --full-page "file://$(pwd)/diagram.html" output.png
```

## Command Options

| Option | Purpose | Example |
|--------|---------|---------|
| `--full-page` | Capture entire document | Required for most diagrams |
| `--viewport-size=WxH` | Set initial viewport | `--viewport-size=1920x1080` |
| `--wait-for-timeout=ms` | Wait before capture | `--wait-for-timeout=1000` |
| `--device=name` | Emulate device | `--device="iPhone 12"` |
| `--color-scheme=mode` | Light/dark mode | `--color-scheme=dark` |

## Common Patterns

### Academic Diagrams (Most Common)

```bash
# Full page capture - lets content determine size
playwright screenshot --full-page "file://$(pwd)/docs/architecture.html" docs/architecture.png
```

### Fixed Width Output

```bash
# Set specific width, full page height
playwright screenshot --full-page --viewport-size=1200x800 "file://$(pwd)/diagram.html" output.png
```

### Wait for Dynamic Content

```bash
# Wait 2 seconds for animations/rendering
playwright screenshot --full-page --wait-for-timeout=2000 "file://$(pwd)/diagram.html" output.png
```

### Dark Mode Diagram

```bash
playwright screenshot --full-page --color-scheme=dark "file://$(pwd)/diagram.html" output-dark.png
```

## Batch Conversion

```bash
# Convert all HTML files in docs/ to PNG
for f in docs/*.html; do
  output="${f%.html}.png"
  playwright screenshot --full-page "file://$(pwd)/$f" "$output"
  echo "Converted: $f -> $output"
done
```

## Output Location

- **Same directory**: Just use filename (`output.png`)
- **Different directory**: Use path (`docs/images/output.png`)
- **Ensure directory exists**: `mkdir -p docs/images` before running

## Next Phase

Proceed to **Phase 4: Output Verification** to validate the result.
