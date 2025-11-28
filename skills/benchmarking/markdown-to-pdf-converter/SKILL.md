---
name: markdown-to-pdf-converter
description: "Use PROACTIVELY when converting markdown documents to professional PDFs. Automates the pandoc + weasyprint pipeline with academic-style CSS, proper page breaks, and HTML diagram capture via Playwright. Supports reports, papers, and technical documentation. Not for slides or complex layouts requiring InDesign."
version: "0.1.0"
author: "Connor Skiro"
---

# Markdown to PDF Converter

Converts markdown documents to professional, print-ready PDFs using pandoc and weasyprint with academic styling.

## Overview

This skill provides a complete pipeline for converting markdown to publication-quality PDFs:

1. **Markdown → HTML**: pandoc with standalone CSS
2. **HTML → PDF**: weasyprint with academic styling
3. **HTML → PNG**: Playwright for diagram capture (optional)

Key features: academic table borders, proper page breaks, figure centering, retina-quality diagram export.

## When to Use

**Trigger Phrases**:
- "convert this markdown to PDF"
- "generate a PDF from this document"
- "create a professional PDF report"
- "export markdown as PDF"

**Use Cases**:
- Technical reports and whitepapers
- Research papers and academic documents
- Project documentation
- Experiment analysis reports

**NOT for**:
- Presentation slides (use Marp or reveal.js)
- Complex multi-column layouts
- Documents requiring precise InDesign-level control

## Quick Start

```bash
# Prerequisites
brew install pandoc
pip install weasyprint
npm install playwright  # For diagram capture

# Verify installation
which pandoc weasyprint  # Both should return paths

# Basic conversion (two-step)
pandoc document.md -o document.html --standalone --css=pdf-style.css
weasyprint document.html document.pdf

# One-liner (pipe pandoc to weasyprint)
pandoc document.md --standalone --css=pdf-style.css -t html | weasyprint - document.pdf
```

## Workflow Modes

| Mode | Use Case | Process |
|------|----------|---------|
| Quick Convert | Simple docs | Markdown → HTML → PDF |
| Academic Report | Papers with figures | + CSS styling + diagram capture |
| Iterative | Complex layout | Review PDF, adjust page breaks, regenerate |

## Academic PDF Style Standards

### Typography
```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
  padding: 2em;
}
```

### Tables (Academic Style)
- Top border: 2px solid on header
- Bottom border: 2px solid on header AND last row
- Cell padding: 0.5em 0.75em
- Page break avoidance: `page-break-inside: avoid`

### Page Control
| Element | Rule |
|---------|------|
| Page margins | 2cm |
| Headings | `page-break-after: avoid` |
| Figures | `page-break-inside: avoid` |
| Tables | `page-break-inside: avoid` |
| Orphans/widows | 3 lines minimum |

### Figure Centering (Critical)
```html
<figure style="margin: 2em auto; page-break-inside: avoid; text-align: center;">
  <img src="diagram.png" alt="Description" style="max-width: 100%; height: auto; display: inline-block;">
  <figcaption style="text-align: center; font-style: italic; margin-top: 1em;">
    Figure 1: Caption text
  </figcaption>
</figure>
```

### Manual Page Breaks
```html
<div style="page-break-before: always;"></div>
```

## Diagram Capture with Playwright

For HTML diagrams that need PNG export:

```javascript
const { chromium } = require('playwright');

async function captureDiagram(htmlPath, pngPath) {
  const browser = await chromium.launch();
  const context = await browser.newContext({ deviceScaleFactor: 2 }); // Retina quality
  const page = await context.newPage();

  await page.goto(`file://${htmlPath}`);
  const element = await page.locator('.diagram-container');
  await element.screenshot({ path: pngPath, type: 'png' });

  await browser.close();
}
```

**Key settings**:
- `deviceScaleFactor: 2` for retina-quality PNGs
- Target `.diagram-container` selector for clean capture
- Use `max-width: 100%` in CSS, NOT `min-width`

## CSS Template Location

See `templates/pdf-style.css` for full academic stylesheet.

## Markdown Structure for Reports

```markdown
# Title

## Subtitle (optional)

**Metadata** (date, author, etc.)

---

## Abstract

Summary paragraph...

---

## 1. Section Title

### 1.1 Subsection

Content with tables, figures...

---

## Appendix A: Title

Supporting materials...
```

## Success Criteria

- [ ] PDF renders without weasyprint errors
- [ ] All images display correctly
- [ ] Tables don't split across pages
- [ ] Figures are centered with captions
- [ ] No orphaned headings at page bottoms
- [ ] Manual page breaks work as expected
- [ ] Text is readable (not cut off)

## Common Issues

| Issue | Solution |
|-------|----------|
| Image cut off | Remove `min-width`, use `max-width: 100%` |
| Image off-center | Add `margin: auto; text-align: center` to figure |
| Table split across pages | Add `page-break-inside: avoid` |
| Heading orphaned | CSS already handles with `page-break-after: avoid` |
| Too much whitespace | Remove unnecessary `<div style="page-break-before: always;">` |

## Weasyprint CSS Compatibility

Weasyprint does not support all CSS properties. The following will generate warnings (safe to ignore, but can be removed for cleaner output):

| Unsupported Property | Alternative |
|---------------------|-------------|
| `gap` | Use `margin` on child elements |
| `overflow-x` | Not needed for print |
| `user-select` | Not needed for print |
| `flex-gap` | Use `margin` instead |
| `backdrop-filter` | Not supported in print |
| `scroll-behavior` | Not needed for print |

**Clean CSS template tip**: Remove these properties from your stylesheet to avoid warning messages during conversion.

## Reference Files

- `templates/pdf-style.css` - Full CSS stylesheet
- `templates/capture-diagrams.js` - Playwright capture script
- `examples/report-template.md` - Example markdown structure
- `workflow/iterative-refinement.md` - Page break tuning process

## Related Skills

- **html-diagram-creator**: Create publication-quality HTML diagrams
- **html-to-png-converter**: Convert HTML diagrams to PNG for embedding

**Documentation Pipeline**: Create diagrams (html-diagram-creator) → Convert to PNG (html-to-png-converter) → Embed in markdown → Export to PDF (this skill)

---

**Based on**: paralleLLM empathy-experiment-v1.0.pdf
