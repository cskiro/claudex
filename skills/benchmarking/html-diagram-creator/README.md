# HTML Diagram Creator

Publication-quality architecture diagrams as HTML files following academic paper conventions.

## Overview

This skill generates HTML-based diagrams styled after major ML benchmark papers (HELM, BetterBench, EleutherAI Evaluation Harness). Output can be exported to PNG for embedding in research papers, documentation, and presentations.

## Key Features

- **Academic styling**: Rounded corners, subtle shadows, figure numbering
- **Color-coded stages**: Data Preparation (blue), Execution (green), Analysis (orange)
- **TikZ-inspired design**: Follows LaTeX academic paper conventions
- **Export-ready**: HTML viewable in browser, exportable to PNG via Playwright

## Quick Start

```bash
# Trigger the skill
"Create an architecture diagram for [your pipeline]"

# Export to PNG (after HTML is generated)
npx playwright screenshot --full-page --device-scale-factor=2 "file://$(pwd)/diagram.html" diagram@2x.png
```

## Trigger Phrases

- "create an architecture diagram"
- "make a pipeline diagram for my paper"
- "publication-ready figure"
- "academic diagram"
- "benchmark visualization"

## Templates Available

- **Linear Pipeline**: 3-box horizontal flow
- **Branching Architecture**: Y-split parallel paths
- **Comparison**: Before/After side-by-side

## Related Skills

- `html-to-png-converter` - Export HTML diagrams to PNG
- `markdown-to-pdf-converter` - Embed PNG in professional PDFs
- `ascii-diagram-creator` - Terminal-compatible text diagrams

## Documentation

See [SKILL.md](SKILL.md) for complete templates, CSS reference, and workflow details.
