# Markdown to PDF Converter

A Claude Code skill for converting markdown documents to professional, print-ready PDFs using pandoc and weasyprint with academic styling.

## Overview

This skill automates the markdown-to-PDF pipeline with:
- Academic-style CSS (system fonts, proper tables, page breaks)
- HTML diagram capture via Playwright at retina quality
- Iterative refinement workflow for complex documents

## Prerequisites

```bash
# Required
brew install pandoc
pip install weasyprint

# Optional (for diagram capture)
npm install playwright
npx playwright install chromium
```

## Usage

Trigger the skill with phrases like:
- "convert this markdown to PDF"
- "generate a PDF from this document"
- "create a professional PDF report"

## Key Features

### Academic Table Styling
Tables use traditional academic formatting with top/bottom borders on headers and clean cell spacing.

### Smart Page Breaks
- Headings stay with following content
- Tables and figures don't split across pages
- Manual page breaks via `<div style="page-break-before: always;"></div>`

### Figure Centering
Proper figure centering that works in weasyprint (not all CSS properties are supported).

### Retina-Quality Diagrams
Playwright captures HTML diagrams at 2x resolution for crisp print output.

## File Structure

```
markdown-to-pdf-converter/
├── SKILL.md           # Main skill instructions
├── README.md          # This file
├── CHANGELOG.md       # Version history
├── templates/
│   ├── pdf-style.css          # Academic CSS stylesheet
│   └── capture-diagrams.js    # Playwright screenshot script
├── examples/
│   └── report-template.md     # Example markdown structure
├── reference/
│   └── weasyprint-notes.md    # CSS compatibility notes
└── workflow/
    └── iterative-refinement.md # Page break tuning process
```

## Version

1.0.0 - Initial release based on paralleLLM empathy-experiment-v1.0.pdf

## Author

Connor Skiro
