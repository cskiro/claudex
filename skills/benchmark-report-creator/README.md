# Benchmark Report Creator

End-to-end orchestrator for creating publication-quality AI/ML benchmark reports with diagrams and PDF export.

## Overview

This skill coordinates the complete benchmark report pipeline:

1. **Structure** - Academic report template with proper sections
2. **Diagrams** - HTML diagrams with publication-quality styling
3. **Capture** - High-resolution PNG export (2x retina)
4. **Export** - Professional PDF via pandoc + weasyprint

## Quick Start

```bash
# 1. Install prerequisites
brew install pandoc
pip install weasyprint
npm install playwright && npx playwright install chromium

# 2. Create diagram and capture to PNG
node scripts/capture-diagram.js diagram.html figures/figure-1.png

# 3. Write report using reference/report-template.md

# 4. Generate PDF
pandoc report.md --standalone --css=templates/pdf-style.css -t html | weasyprint - report.pdf
```

## Key Features

- **Working hi-res capture script** - Fixes Playwright CLI limitations
- **Academic CSS template** - Based on empathy v1.0/v2.0 conventions
- **Complete command sequences** - Copy-paste ready
- **Orchestration, not duplication** - Links to component skills

## File Structure

```
benchmark-report-creator/
├── SKILL.md                    # Main orchestrator skill
├── templates/
│   └── pdf-style.css          # Academic PDF styling
├── scripts/
│   └── capture-diagram.js     # High-res PNG capture
├── reference/
│   ├── report-template.md     # Full markdown template
│   ├── html-templates.md      # Diagram HTML templates
│   └── command-reference.md   # All commands
└── examples/
    └── (sample reports)
```

## Why This Skill?

The benchmarking category previously had 4 separate skills:
- `report-creator` - Document templates
- `html-diagram-creator` - Diagram HTML
- `html-to-png-converter` - PNG export (broken CLI reference)
- `markdown-to-pdf-converter` - PDF pipeline

This orchestrator consolidates them into a single cohesive workflow, fixing the broken PNG capture and providing the exact templates from empathy v1.0/v2.0.

## Related Skills

If installed in user's `~/.claude/skills/`, component skills may still be available:
- `html-diagram-creator` - For single diagram creation
- `ascii-diagram-creator` - For terminal-compatible diagrams

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT
