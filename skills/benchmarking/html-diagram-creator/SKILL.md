---
name: html-diagram-creator
version: 0.1.0
description: Use PROACTIVELY when user needs publication-quality architecture diagrams for research papers, documentation, or presentations. Triggers on "architecture diagram", "pipeline diagram", "figure for paper", "academic diagram", "benchmark visualization", or "publication-ready figure". Generates HTML diagrams following academic paper conventions (HELM, BetterBench, EleutherAI) with proper color coding, rounded corners, figure numbering, and export to PNG. Not for ASCII diagrams or flowcharts.
---

# HTML Diagram Creator

## Overview

Generates **publication-quality architecture diagrams** as HTML files for research papers, documentation, and presentations. Follows academic conventions from HELM, BetterBench, and EleutherAI papers.

**Key Capabilities**:
- Academic styling (rounded corners, shadows, figure numbering)
- Color-coded components (Data/Execution/Analysis stages)
- Browser-based with PNG export via Playwright
- Stage grouping with labels and legends

## When to Use This Skill

**Trigger Phrases**:
- "create an architecture diagram"
- "make a pipeline diagram for my paper"
- "publication-ready figure"
- "academic diagram"
- "benchmark visualization"

**Use PROACTIVELY when**:
- User is writing research documentation or papers
- User mentions "publication", "paper", "academic"
- User requests "PNG diagram" or "exportable diagram"

**Do NOT use when**:
- User wants ASCII diagrams (use ascii-diagram-creator)
- User needs interactive flowcharts (use Mermaid)
- User wants UML diagrams

## Quick Reference

### Color Palette

| Stage | Fill | Border | Usage |
|-------|------|--------|-------|
| Data Preparation | `#E3F2FD` | `#1976D2` | Input processing, loaders |
| Execution | `#E8F5E9` | `#388E3C` | API calls, inference |
| Analysis | `#FFF3E0` | `#F57C00` | Evaluation, scoring |
| Terminals | `#FF6B6B` | `#FF6B6B` | Input/Output markers |

### Visual Standards

| Element | Implementation |
|---------|----------------|
| Corners | `border-radius: 6px` |
| Shadows | `box-shadow: 0 2px 4px rgba(0,0,0,0.08)` |
| Arrows | Dark slate `#546E7A` with triangular heads |
| Figure label | "Figure N" format above title |

## Workflow

| Phase | Description | Details |
|-------|-------------|---------|
| 1 | Requirements Gathering | Identify components, flow type, stage categories |
| 2 | HTML Generation | Create standalone HTML with academic CSS |
| 3 | Component Layout | Structure with flexbox alignment |
| 4 | Export | PNG via Playwright or screenshot |

### Phase 1: Requirements

1. **Identify components**: What boxes/stages need to be shown?
2. **Determine flow**: Linear pipeline? Branching? Multi-path?
3. **Categorize stages**: Data (blue), Execution (green), Analysis (orange)

### Phase 2: HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Diagram Title]</title>
  <style>/* Academic styling */</style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure [N]</div>
    <h2 class="diagram-title">[Title]</h2>
    <!-- Pipeline components -->
    <p class="figure-caption">[Caption]</p>
  </div>
</body>
</html>
```

### Phase 3: Component Layout

```html
<div class="pipeline">
  <div class="component-box data-prep">
    <span class="component-name">[Name]</span>
    <span class="component-tech">[Tech]</span>
  </div>
  <div class="arrow"></div>
  <!-- More components -->
</div>
```

### Phase 4: Export

```bash
# Retina quality (recommended)
npx playwright screenshot --full-page --device-scale-factor=2 \
  "file://$(pwd)/diagram.html" diagram@2x.png

# Standard resolution
npx playwright screenshot --full-page "file://$(pwd)/diagram.html" diagram.png
```

## Templates

Copy-paste ready templates available in [reference/html-templates.md](reference/html-templates.md):
- **Linear Pipeline**: 3-box horizontal flow
- **Branching Architecture**: Y-split parallel paths
- **Comparison**: Before/After side-by-side
- **Arrow Snippets**: Horizontal, vertical, bidirectional

## Reference

- [HTML Templates](reference/html-templates.md) - Copy-paste ready diagrams
- [CSS Components](reference/css-components.md) - Complete class definitions
- [Additional Templates](reference/templates.md) - More pipeline variants

## Completion Checklist

- [ ] HTML file generated with academic styling
- [ ] Figure numbering applied
- [ ] Color-coded by stage
- [ ] Rounded corners (6px) and shadows
- [ ] Export method explained

## Related Skills

- **html-to-png-converter**: Export HTML to PNG with retina support
- **markdown-to-pdf-converter**: Embed diagrams in PDFs
- **ascii-diagram-creator**: Terminal-compatible text diagrams

**Pipeline**: Create diagram → Export to PNG → Embed in markdown → Generate PDF
