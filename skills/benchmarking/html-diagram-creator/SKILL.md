---
name: html-diagram-creator
version: 0.1.0
description: Use PROACTIVELY when user needs publication-quality architecture diagrams for research papers, documentation, or presentations. Triggers on "architecture diagram", "pipeline diagram", "figure for paper", "academic diagram", "benchmark visualization", or "publication-ready figure". Generates HTML diagrams following academic paper conventions (HELM, BetterBench, EleutherAI) with proper color coding, rounded corners, figure numbering, and export to PNG. Not for ASCII diagrams or flowcharts.
---

# HTML Diagram Creator

## Overview

This skill generates **publication-quality architecture diagrams** as HTML files that can be screenshotted or exported to PNG for use in research papers, documentation, and presentations. Diagrams follow academic conventions from major ML benchmark papers (HELM, BetterBench, EleutherAI Evaluation Harness).

**Key Capabilities**:
- **Academic styling**: Rounded corners, subtle shadows, proper figure numbering
- **Color-coded components**: Stage-based color differentiation (Data/Execution/Analysis)
- **TikZ-inspired design**: Follows LaTeX academic paper conventions
- **Browser-based**: HTML output viewable in any browser, exportable to PNG
- **Stage grouping**: Visual brackets and labels for pipeline phases
- **Legend generation**: Automatic color legend for accessibility
- **Metadata support**: Figure numbering and detailed captions

## When to Use This Skill

**Trigger Phrases**:
- "create an architecture diagram"
- "make a pipeline diagram for my paper"
- "publication-ready figure"
- "academic diagram"
- "benchmark visualization"
- "figure 1 showing..."

**Use PROACTIVELY when**:
- User is writing research documentation or papers
- User needs diagrams for README or technical docs
- User mentions "publication", "paper", "academic"
- User requests "PNG diagram" or "exportable diagram"
- User is documenting benchmark or evaluation pipelines

**Do NOT use when**:
- User wants ASCII/terminal-compatible diagrams (use ascii-diagram-creator)
- User needs interactive flowcharts (use Mermaid)
- User wants UML diagrams (use dedicated UML tools)
- Simple bullet lists would suffice

## Academic Design Standards

Based on analysis of HELM, BetterBench, EleutherAI Evaluation Harness, and Evalverse papers:

### Color Palette (Stage-Based)

| Stage | Fill Color | Border Color | Usage |
|-------|------------|--------------|-------|
| Data Preparation | `#E3F2FD` | `#1976D2` | Input processing, loaders, parsers |
| Execution | `#E8F5E9` | `#388E3C` | API calls, model inference, runtime |
| Analysis | `#FFF3E0` | `#F57C00` | Evaluation, scoring, statistics |
| Terminals | `#FF6B6B` | `#FF6B6B` | Input/Output markers (coral) |
| Arrows | `#546E7A` | - | Dark slate for visibility |

### Visual Elements

| Element | Academic Standard | Implementation |
|---------|-------------------|----------------|
| Corners | Rounded (3-6pt) | `border-radius: 6px` |
| Shadows | Subtle drop shadow | `box-shadow: 0 2px 4px rgba(0,0,0,0.08)` |
| Borders | 1px, darker than fill | `border: 1px solid [border-color]` |
| Arrows | Dark, triangular heads | SVG with polygon arrowheads |
| Figure label | "Figure N" format | Positioned above title |
| Caption | Descriptive, below diagram | Italicized, explains the flow |

### Typography

| Element | Style |
|---------|-------|
| Title | 18px, semi-bold, dark (#24292f) |
| Component names | 12px, semi-bold, centered |
| Technology notes | 9px, italic, gray (#57606a) |
| Data labels | 9px, monospace, gray |
| Stage labels | 10px, uppercase, letter-spacing |

## Workflow

### Phase 1: Requirements Gathering

1. **Identify components**: What boxes/stages need to be shown?
2. **Determine flow**: Linear pipeline? Branching? Multi-path?
3. **Categorize stages**: Which components are Data/Execution/Analysis?
4. **Note data types**: What flows between components?

### Phase 2: HTML Generation

Generate a standalone HTML file with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Diagram Title]</title>
  <style>
    /* Academic styling CSS */
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure [N]</div>
    <h2 class="diagram-title">[Title]</h2>
    <!-- Pipeline components -->
    <p class="figure-caption">[Descriptive caption]</p>
    <div class="legend"><!-- Color legend --></div>
  </div>
</body>
</html>
```

### Phase 3: Component Layout

Structure components using flexbox for proper alignment:

```html
<div class="pipeline">
  <div class="component">
    <span class="data-label">[input type]</span>
    <div class="component-box [stage-class]">
      <span class="component-name">[Name]</span>
      <span class="component-tech">[Technology]</span>
    </div>
  </div>
  <div class="arrow"><!-- SVG arrow --></div>
  <!-- More components... -->
</div>
```

### Phase 4: Output & Export

1. **Save HTML file** to appropriate location (e.g., `docs/`)
2. **Open in browser**: `open [filename].html`
3. **Export to PNG** (recommended: use html-to-png-converter skill):
   ```bash
   # Retina quality (recommended for publications)
   npx playwright screenshot --full-page --device-scale-factor=2 "file://$(pwd)/diagram.html" diagram@2x.png

   # Standard resolution
   npx playwright screenshot --full-page "file://$(pwd)/diagram.html" diagram.png
   ```
4. **Alternative export methods**:
   - Screenshot: Cmd+Shift+4 (macOS)
   - Print to PDF: Cmd+P > Save as PDF

## Copy-Paste Templates

### Linear Pipeline (3 boxes)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Pipeline Diagram</title>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 2em; background: #f8f9fa; }
    .diagram-container { max-width: 900px; margin: 0 auto; background: white; padding: 2em; border-radius: 8px; }
    .figure-label { font-size: 12px; color: #57606a; margin-bottom: 0.5em; }
    .diagram-title { font-size: 18px; font-weight: 600; color: #24292f; margin: 0 0 1.5em 0; }
    .pipeline { display: flex; align-items: center; justify-content: center; gap: 0; }
    .component-box { padding: 1em 1.5em; border-radius: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.08); min-width: 120px; }
    .component-name { font-size: 12px; font-weight: 600; display: block; }
    .component-tech { font-size: 9px; font-style: italic; color: #57606a; }
    .data-prep { background: #E3F2FD; border: 1px solid #1976D2; }
    .execution { background: #E8F5E9; border: 1px solid #388E3C; }
    .analysis { background: #FFF3E0; border: 1px solid #F57C00; }
    .arrow { width: 40px; height: 2px; background: #546E7A; position: relative; margin: 0 -1px; }
    .arrow::after { content: ''; position: absolute; right: -6px; top: -4px; border: 5px solid transparent; border-left: 6px solid #546E7A; }
    .figure-caption { font-style: italic; color: #57606a; text-align: center; margin-top: 1.5em; font-size: 14px; }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure 1</div>
    <h2 class="diagram-title">Pipeline Architecture</h2>
    <div class="pipeline">
      <div class="component-box data-prep">
        <span class="component-name">Data Loader</span>
        <span class="component-tech">JSON/CSV</span>
      </div>
      <div class="arrow"></div>
      <div class="component-box execution">
        <span class="component-name">Processor</span>
        <span class="component-tech">Node.js</span>
      </div>
      <div class="arrow"></div>
      <div class="component-box analysis">
        <span class="component-name">Analyzer</span>
        <span class="component-tech">Statistics</span>
      </div>
    </div>
    <p class="figure-caption">Data flows through preparation, execution, and analysis stages.</p>
  </div>
</body>
</html>
```

### Branching Architecture (Y-split)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Branching Diagram</title>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 2em; background: #f8f9fa; }
    .diagram-container { max-width: 700px; margin: 0 auto; background: white; padding: 2em; border-radius: 8px; }
    .figure-label { font-size: 12px; color: #57606a; }
    .diagram-title { font-size: 18px; font-weight: 600; color: #24292f; margin: 0.5em 0 1.5em 0; }
    .component-box { padding: 1em 1.5em; border-radius: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.08); }
    .component-name { font-size: 12px; font-weight: 600; display: block; }
    .input { background: #E3F2FD; border: 1px solid #1976D2; width: fit-content; margin: 0 auto 1em auto; }
    .branch-a { background: #E8F5E9; border: 1px solid #388E3C; }
    .branch-b { background: #FFF3E0; border: 1px solid #F57C00; }
    .branches { display: flex; justify-content: center; gap: 3em; margin-top: 1em; }
    .branch { text-align: center; }
    .vertical-arrow { width: 2px; height: 30px; background: #546E7A; margin: 0 auto; position: relative; }
    .vertical-arrow::after { content: ''; position: absolute; bottom: -6px; left: -4px; border: 5px solid transparent; border-top: 6px solid #546E7A; }
    .figure-caption { font-style: italic; color: #57606a; text-align: center; margin-top: 1.5em; font-size: 14px; }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure 2</div>
    <h2 class="diagram-title">Branching Architecture</h2>
    <div class="component-box input"><span class="component-name">Input Router</span></div>
    <div class="branches">
      <div class="branch">
        <div class="vertical-arrow"></div>
        <div class="component-box branch-a"><span class="component-name">Path A</span></div>
      </div>
      <div class="branch">
        <div class="vertical-arrow"></div>
        <div class="component-box branch-b"><span class="component-name">Path B</span></div>
      </div>
    </div>
    <p class="figure-caption">Input is routed to parallel processing paths.</p>
  </div>
</body>
</html>
```

### Comparison (Before/After)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Comparison Diagram</title>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 2em; background: #f8f9fa; }
    .diagram-container { max-width: 800px; margin: 0 auto; background: white; padding: 2em; border-radius: 8px; }
    .figure-label { font-size: 12px; color: #57606a; }
    .diagram-title { font-size: 18px; font-weight: 600; color: #24292f; margin: 0.5em 0 1.5em 0; }
    .comparison { display: flex; gap: 2em; justify-content: center; }
    .side { flex: 1; max-width: 300px; }
    .side-label { font-size: 14px; font-weight: 600; text-align: center; margin-bottom: 1em; padding: 0.5em; border-radius: 4px; }
    .before-label { background: #ffebee; color: #c62828; }
    .after-label { background: #e8f5e9; color: #2e7d32; }
    .component-box { padding: 0.8em 1em; border-radius: 6px; text-align: center; margin-bottom: 0.5em; font-size: 12px; }
    .old { background: #fafafa; border: 1px solid #ccc; color: #666; }
    .new { background: #E3F2FD; border: 1px solid #1976D2; }
    .figure-caption { font-style: italic; color: #57606a; text-align: center; margin-top: 1.5em; font-size: 14px; }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure 3</div>
    <h2 class="diagram-title">Architecture Comparison</h2>
    <div class="comparison">
      <div class="side">
        <div class="side-label before-label">Before</div>
        <div class="component-box old">Legacy Component A</div>
        <div class="component-box old">Legacy Component B</div>
        <div class="component-box old">Legacy Component C</div>
      </div>
      <div class="side">
        <div class="side-label after-label">After</div>
        <div class="component-box new">Modern Service</div>
        <div class="component-box new">Unified API</div>
      </div>
    </div>
    <p class="figure-caption">Migration consolidates three legacy components into two modern services.</p>
  </div>
</body>
</html>
```

## Arrow SVG Snippets

### Horizontal Arrow (right)
```html
<div class="arrow" style="width: 40px; height: 2px; background: #546E7A; position: relative;">
  <div style="position: absolute; right: -6px; top: -4px; border: 5px solid transparent; border-left: 6px solid #546E7A;"></div>
</div>
```

### Horizontal Arrow (left)
```html
<div class="arrow" style="width: 40px; height: 2px; background: #546E7A; position: relative;">
  <div style="position: absolute; left: -6px; top: -4px; border: 5px solid transparent; border-right: 6px solid #546E7A;"></div>
</div>
```

### Vertical Arrow (down)
```html
<div style="width: 2px; height: 30px; background: #546E7A; margin: 0 auto; position: relative;">
  <div style="position: absolute; bottom: -6px; left: -4px; border: 5px solid transparent; border-top: 6px solid #546E7A;"></div>
</div>
```

### Vertical Arrow (up)
```html
<div style="width: 2px; height: 30px; background: #546E7A; margin: 0 auto; position: relative;">
  <div style="position: absolute; top: -6px; left: -4px; border: 5px solid transparent; border-bottom: 6px solid #546E7A;"></div>
</div>
```

### Bidirectional Arrow (horizontal)
```html
<div style="width: 40px; height: 2px; background: #546E7A; position: relative; margin: 0 8px;">
  <div style="position: absolute; left: -6px; top: -4px; border: 5px solid transparent; border-right: 6px solid #546E7A;"></div>
  <div style="position: absolute; right: -6px; top: -4px; border: 5px solid transparent; border-left: 6px solid #546E7A;"></div>
</div>
```

## Reference Materials

See [reference/templates.md](reference/templates.md) for:
- Additional pipeline templates
- Branching architecture variants
- Multi-stage evaluation layouts

## CSS Reference

See [reference/css-components.md](reference/css-components.md) for:
- Complete CSS class definitions
- Color scheme variations
- Responsive adjustments

## Examples

See [examples/](examples/) for:
- Benchmark pipeline (HELM-style)
- Evaluation harness (EleutherAI-style)
- Before/after comparison

## Mandatory Completion Checklist

```markdown
## Diagram Generation Complete

### Outputs
- [ ] HTML file generated with academic styling
- [ ] Figure numbering applied
- [ ] Color-coded by component stage
- [ ] Legend included

### Quality Checks
- [ ] Rounded corners (6px)
- [ ] Subtle drop shadows
- [ ] Dark arrows with proper heads
- [ ] Stage grouping labels/brackets
- [ ] No overlapping text

### Export Guidance
- [ ] File opened in browser
- [ ] Export method explained (screenshot/PDF)
- [ ] Recommended filename: [suggested path]
```

## Related Skills

- **html-to-png-converter**: Export HTML diagrams to PNG with retina support
- **markdown-to-pdf-converter**: Embed PNG diagrams in professional PDFs
- **ascii-diagram-creator**: Terminal-compatible text diagrams

**Documentation Pipeline**: Create diagram (this skill) → Export to PNG (html-to-png-converter) → Embed in markdown → Generate PDF (markdown-to-pdf-converter)

## Metadata

**Category**: documentation
**Version**: 1.0.0
**Based on**: HELM, BetterBench, EleutherAI Evaluation Harness, Evalverse
**Export recommendation**: Use `--device-scale-factor=2` for publication-quality PNG output
