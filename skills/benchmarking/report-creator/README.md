# Report Creator

Publication-quality academic research report templates with professional structure and PDF export optimization.

## Overview

This skill provides templates for creating research reports, experiment writeups, technical whitepapers, and empirical studies. Templates follow academic paper conventions with proper structure, table formatting, and PDF export optimization.

## Key Features

- **Academic structure**: Abstract, Executive Summary, numbered sections, Appendices
- **Professional tables**: Academic-style borders (2px top/bottom on headers)
- **Figure support**: Centered figures with captions, page-break protection
- **PDF-optimized CSS**: Proper page breaks, orphan/widow control, margins

## Quick Start

```bash
# Trigger the skill
"Create a research report for [your experiment]"

# Convert to PDF (after markdown is generated)
pandoc report.md --standalone --css=pdf-style.css -t html | weasyprint - report.pdf
```

## Trigger Phrases

- "create a research report"
- "write up my experiment results"
- "technical whitepaper template"
- "empirical study format"
- "academic report structure"

## Document Structure

1. Title and Metadata
2. Abstract (150-250 words)
3. Executive Summary with metrics table
4. Background and Motivation
5. Methodology
6. Results
7. Analysis and Discussion
8. Limitations
9. Future Work
10. Conclusion
11. Appendices

## Related Skills

- `html-diagram-creator` - Create publication-quality figures
- `html-to-png-converter` - Export diagrams to PNG
- `markdown-to-pdf-converter` - Convert markdown to PDF

## Documentation

See [SKILL.md](SKILL.md) for complete templates, CSS styling, and formatting guidelines.
