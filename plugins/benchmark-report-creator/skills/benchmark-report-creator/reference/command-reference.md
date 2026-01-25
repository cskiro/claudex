# Command Reference

Complete command sequences for the benchmark report pipeline.

## Prerequisites

```bash
# Install all dependencies (one-time setup)
brew install pandoc
pip install weasyprint
npm install playwright
npx playwright install chromium

# Verify installation
which pandoc weasyprint
npx playwright --version
```

## Phase 1: Create Diagram HTML

Use html-diagram-creator patterns or copy from `html-templates.md`.

Save as `diagram.html` with `.diagram-container` class on main element.

## Phase 2: Capture to High-Res PNG

### Using the Bundled Script (Recommended)

```bash
# Single file - retina quality (2x)
node scripts/capture-diagram.js diagram.html figures/figure-1.png

# Batch capture all diagrams in directory
node scripts/capture-diagram.js ./diagrams

# Auto-capture all *diagram*.html in current directory
node scripts/capture-diagram.js
```

### Why Not Playwright CLI?

```bash
# THIS DOES NOT WORK - flag doesn't exist
npx playwright screenshot --device-scale-factor=2 ...  # ❌ INVALID

# The CLI only supports these flags:
npx playwright screenshot --help
# --full-page, --viewport-size, --wait-for-selector (no scale factor)

# Use the Node.js script instead which sets deviceScaleFactor in context
```

## Phase 3: Write Markdown Report

Copy template from `reference/report-template.md`.

### Embedding Figures

```html
<figure style="margin: 2em auto; page-break-inside: avoid; text-align: center;">
  <img src="figures/figure-1.png" alt="Pipeline architecture" style="max-width: 100%; height: auto;">
  <figcaption style="text-align: center; font-style: italic; margin-top: 1em;">
    Figure 1: Pipeline architecture showing data preparation, execution, and analysis phases.
  </figcaption>
</figure>
```

### Manual Page Breaks

```html
<div style="page-break-before: always;"></div>
```

## Phase 4: Convert to PDF

### Two-Step (Debugging)

```bash
# Step 1: Markdown to HTML
pandoc report.md -o report.html --standalone --css=templates/pdf-style.css

# Step 2: HTML to PDF
weasyprint report.html report.pdf
```

### One-Liner (Production)

```bash
pandoc report.md --standalone --css=templates/pdf-style.css -t html | weasyprint - report.pdf
```

### With Absolute CSS Path

```bash
# If CSS isn't found, use absolute path
CSS_PATH="$(pwd)/templates/pdf-style.css"
pandoc report.md --standalone --css="$CSS_PATH" -t html | weasyprint - report.pdf
```

## Complete Pipeline Example

```bash
# 1. Create project structure
mkdir -p benchmark-report/{figures,diagrams}
cd benchmark-report

# 2. Copy templates
cp /path/to/skills/benchmark-report-creator/templates/pdf-style.css .
cp /path/to/skills/benchmark-report-creator/scripts/capture-diagram.js .
cp /path/to/skills/benchmark-report-creator/reference/report-template.md report.md

# 3. Create diagram (edit the HTML)
# ... create diagrams/pipeline-diagram.html ...

# 4. Capture diagram to PNG
node capture-diagram.js diagrams/pipeline-diagram.html figures/figure-1.png

# 5. Edit report.md with your content
# ... add your research data ...

# 6. Generate PDF
pandoc report.md --standalone --css=pdf-style.css -t html | weasyprint - report.pdf

# 7. Open and review
open report.pdf  # macOS
```

## Troubleshooting Commands

### Check Installations

```bash
# Pandoc
pandoc --version
# Should show: pandoc 3.x.x

# Weasyprint
weasyprint --version
# Should show: weasyprint 60.x

# Playwright
npx playwright --version
# Should show: Version 1.x.x

# Chromium installed?
npx playwright install chromium --dry-run
```

### Debug PNG Capture

```bash
# Check if HTML renders correctly
open diagram.html  # View in browser first

# Check for .diagram-container selector
grep -o 'diagram-container' diagram.html
# Should output: diagram-container

# Verbose capture (modify script or add console.log)
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ deviceScaleFactor: 2 });
  const page = await context.newPage();
  await page.goto('file://$(pwd)/diagram.html');
  console.log('Page loaded');
  const element = await page.locator('.diagram-container');
  console.log('Found elements:', await element.count());
  await browser.close();
})();
"
```

### Debug PDF Generation

```bash
# Check intermediate HTML
pandoc report.md -o debug.html --standalone --css=pdf-style.css
open debug.html  # View in browser

# Check weasyprint errors
weasyprint debug.html debug.pdf 2>&1 | grep -i error

# Common weasyprint warnings (safe to ignore)
# - "Unsupported property: gap"
# - "Unsupported property: overflow-x"
```

## File Organization

Recommended project structure:

```
benchmark-report/
├── report.md               # Main markdown document
├── pdf-style.css          # CSS template (copy from skill)
├── capture-diagram.js     # Capture script (copy from skill)
├── figures/
│   ├── figure-1.png       # Captured diagrams
│   └── figure-2.png
├── diagrams/
│   ├── pipeline-diagram.html
│   └── comparison-diagram.html
└── output/
    └── report.pdf         # Final output
```
