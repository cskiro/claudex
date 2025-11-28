---
name: report-creator
description: "Use PROACTIVELY when user needs to create research reports, experiment writeups, technical whitepapers, or empirical studies. Provides templates with professional structure, CSS styling for PDF export, and proper figure/table formatting. Currently supports: Academic Research Report. Based on publication-quality standards."
version: "0.1.0"
author: "Connor Skiro"
category: documentation
---

# Report Creator

## Overview

Provides templates for creating publication-quality research reports with professional structure, styling, and PDF export optimization.

**Available Templates**:
- **Academic Research Report**: Full empirical study format

**Key Capabilities**:
- Academic structure (Abstract, Methodology, Results, Discussion)
- Professional tables with academic borders
- Figure support with captions and page-break protection
- PDF-optimized CSS via pandoc + weasyprint

## When to Use

**Trigger Phrases**:
- "create a research report"
- "write up my experiment results"
- "technical whitepaper template"
- "empirical study format"

**Use Cases**:
- AI/ML experiment reports
- Benchmark evaluation writeups
- Technical research documentation
- Empirical study publications

**NOT for**:
- Blog posts or casual documentation
- API documentation
- Presentation slides
- Quick README files

## Document Structure

| Section | Content |
|---------|---------|
| Abstract | 150-250 word summary |
| Executive Summary | Key finding + metrics table |
| 1. Background | Research context, hypotheses |
| 2. Methodology | Design, variables, protocol |
| 3. Results | Statistics, observations |
| 4. Discussion | Hypothesis evaluation, implications |
| 5. Limitations | Methodological, dataset, evaluation |
| 6. Future Work | Research directions |
| 7. Conclusion | Synthesis, bottom line |
| Appendices | Supporting materials |

## Quick Start

1. Copy template from [reference/report-template.md](reference/report-template.md)
2. Fill in sections with your research data
3. Add figures using HTML figure tags
4. Export to PDF:

```bash
# One-liner conversion
pandoc report.md --standalone --css=pdf-style.css -t html | weasyprint - report.pdf
```

## Reference Files

| File | Content |
|------|---------|
| [report-template.md](reference/report-template.md) | Full markdown template |
| [pdf-style.css](reference/pdf-style.css) | Academic CSS styling |
| [table-patterns.md](reference/table-patterns.md) | Table and figure patterns |

## Key Formatting Patterns

### Tables (Academic Style)
- 2px borders on header top/bottom
- 1px borders between rows
- 2px border on final row
- `page-break-inside: avoid`

### Figures
```html
<figure style="margin: 2em auto; page-break-inside: avoid; text-align: center;">
  <img src="figure-1.png" alt="Description" style="max-width: 100%;">
  <figcaption>Figure 1: Caption text.</figcaption>
</figure>
```

### Typography
| Element | Usage |
|---------|-------|
| **Bold** | Key findings, hypothesis status |
| *Italic* | Figure captions, emphasis |
| `code` | Model IDs, file names |
| > Quote | Sample prompts, messages |

## Conversion Commands

```bash
# Prerequisites
which pandoc weasyprint  # Both required

# Two-step
pandoc report.md -o report.html --standalone --css=pdf-style.css
weasyprint report.html report.pdf

# One-liner
pandoc report.md --standalone --css=pdf-style.css -t html | weasyprint - report.pdf
```

## Completion Checklist

- [ ] All 7 main sections present
- [ ] Abstract summarizes question, method, findings
- [ ] Executive summary has metrics table
- [ ] Tables have academic borders
- [ ] Figures have numbered captions
- [ ] No orphaned headings at page bottoms

## Related Skills

- **html-diagram-creator**: Create figures for embedding
- **html-to-png-converter**: Export diagrams to PNG
- **markdown-to-pdf-converter**: General markdown conversion

---

**Based on**: paralleLLM empathy-experiment-v1.0.pdf (17 pages, November 2024)
