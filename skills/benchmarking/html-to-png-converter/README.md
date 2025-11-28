# HTML to PNG Converter

A Claude Code skill for converting HTML files to PNG images using Playwright's CLI screenshot functionality.

## Purpose

Automates the conversion of HTML diagrams, charts, and documents to PNG images for use in:
- Academic papers and research publications
- Technical documentation
- Presentations and slide decks
- README files and project docs

## Prerequisites

- Node.js >= 16
- Playwright (`npm install -g playwright` or use via `npx`)

## Quick Start

```bash
# Install Playwright (if not already installed)
npm install -g playwright
playwright install chromium

# Convert HTML to PNG
playwright screenshot --full-page "file://$(pwd)/diagram.html" diagram.png
```

## Usage

### Single File

```bash
playwright screenshot --full-page "file:///absolute/path/to/file.html" output.png
```

### Batch Conversion

```bash
for f in docs/*.html; do
  playwright screenshot --full-page "file://$(pwd)/$f" "${f%.html}.png"
done
```

## Key Options

| Option | Description |
|--------|-------------|
| `--full-page` | Capture entire document (not just viewport) |
| `--viewport-size=WxH` | Set viewport dimensions (e.g., `1920x1080`) |
| `--wait-for-timeout=ms` | Wait before screenshot (for dynamic content) |

## Troubleshooting

See `reference/troubleshooting.md` for common issues and solutions.

## Related Skills

- **png-diagram-creator**: Creates HTML diagrams with academic styling
- **ascii-diagram-creator**: Terminal-compatible text diagrams

## License

MIT
