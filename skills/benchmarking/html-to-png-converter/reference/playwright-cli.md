# Playwright CLI Reference

## Screenshot Command

```bash
playwright screenshot [options] <url> <output>
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--full-page` | Capture full scrollable page | Off (viewport only) |
| `--viewport-size=WxH` | Set viewport size | 800x600 |
| `--scale=N` | Device scale factor | 1 |
| `--wait-for-timeout=ms` | Wait before screenshot | 0 |
| `--wait-for-selector=sel` | Wait for element | None |
| `--color-scheme=mode` | `light` or `dark` | System |
| `--device=name` | Emulate device | None |
| `--timeout=ms` | Navigation timeout | 30000 |
| `--browser=name` | Browser to use | chromium |

## Browser Options

```bash
# Use specific browser
playwright screenshot --browser=firefox "file://$(pwd)/diagram.html" output.png
playwright screenshot --browser=webkit "file://$(pwd)/diagram.html" output.png
playwright screenshot --browser=chromium "file://$(pwd)/diagram.html" output.png
```

## Device Emulation

```bash
# Emulate specific device
playwright screenshot --device="iPhone 12" "file://$(pwd)/diagram.html" output.png
playwright screenshot --device="iPad Pro" "file://$(pwd)/diagram.html" output.png
```

List all devices:
```bash
playwright devices
```

## Examples

### Basic Full Page

```bash
playwright screenshot --full-page "file://$(pwd)/diagram.html" output.png
```

### High Resolution (2x)

```bash
playwright screenshot --full-page --scale=2 "file://$(pwd)/diagram.html" output@2x.png
```

### Dark Mode

```bash
playwright screenshot --full-page --color-scheme=dark "file://$(pwd)/diagram.html" dark.png
```

### Custom Viewport

```bash
playwright screenshot --viewport-size=1920x1080 "file://$(pwd)/diagram.html" output.png
```

### Wait for Content

```bash
# Wait 2 seconds for dynamic content
playwright screenshot --full-page --wait-for-timeout=2000 "file://$(pwd)/diagram.html" output.png

# Wait for specific element
playwright screenshot --full-page --wait-for-selector=".loaded" "file://$(pwd)/diagram.html" output.png
```

## PDF Generation (Alternative)

For PDF output instead of PNG:

```bash
playwright pdf "file://$(pwd)/document.html" output.pdf
```

PDF-specific options:
- `--format=Letter|A4|...`
- `--landscape`
- `--margin=top,right,bottom,left`
- `--print-background`

## Installation Commands

```bash
# Install Playwright
npm install -g playwright

# Install browsers
playwright install              # All browsers
playwright install chromium     # Chromium only
playwright install firefox      # Firefox only
playwright install webkit       # WebKit only

# Check version
playwright --version
```
