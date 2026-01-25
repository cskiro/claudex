# HTML Diagram Templates

Copy-paste ready templates for publication-quality diagrams.

## Linear Pipeline (3-box)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Pipeline Diagram</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      padding: 40px;
      background: white;
    }
    .diagram-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 30px;
    }
    .figure-label {
      text-align: center;
      font-size: 12px;
      color: #666;
      margin-bottom: 8px;
    }
    .diagram-title {
      text-align: center;
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 30px 0;
    }
    .pipeline {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 20px;
    }
    .component-box {
      padding: 20px 30px;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
      text-align: center;
      min-width: 140px;
    }
    .component-name {
      display: block;
      font-weight: 600;
      font-size: 14px;
      margin-bottom: 4px;
    }
    .component-tech {
      display: block;
      font-size: 12px;
      color: #666;
    }
    /* Stage colors */
    .data-prep {
      background: #E3F2FD;
      border: 2px solid #1976D2;
    }
    .execution {
      background: #E8F5E9;
      border: 2px solid #388E3C;
    }
    .analysis {
      background: #FFF3E0;
      border: 2px solid #F57C00;
    }
    /* Arrows */
    .arrow {
      width: 40px;
      height: 2px;
      background: #546E7A;
      position: relative;
    }
    .arrow::after {
      content: '';
      position: absolute;
      right: 0;
      top: -4px;
      border: 5px solid transparent;
      border-left: 8px solid #546E7A;
    }
    .figure-caption {
      text-align: center;
      font-style: italic;
      font-size: 14px;
      color: #555;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure 1</div>
    <h2 class="diagram-title">Pipeline Architecture</h2>

    <div class="pipeline">
      <div class="component-box data-prep">
        <span class="component-name">Data Loader</span>
        <span class="component-tech">JSON Parser</span>
      </div>
      <div class="arrow"></div>
      <div class="component-box execution">
        <span class="component-name">API Client</span>
        <span class="component-tech">Claude API</span>
      </div>
      <div class="arrow"></div>
      <div class="component-box analysis">
        <span class="component-name">Evaluator</span>
        <span class="component-tech">Scoring Logic</span>
      </div>
    </div>

    <p class="figure-caption">
      Three-stage pipeline showing data preparation, execution, and analysis phases.
    </p>
  </div>
</body>
</html>
```

## Branching Architecture (Y-split)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Branching Architecture</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      padding: 40px;
      background: white;
    }
    .diagram-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 30px;
    }
    .figure-label {
      text-align: center;
      font-size: 12px;
      color: #666;
      margin-bottom: 8px;
    }
    .diagram-title {
      text-align: center;
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 30px 0;
    }
    .architecture {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
    }
    .row {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 40px;
    }
    .component-box {
      padding: 20px 30px;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
      text-align: center;
      min-width: 140px;
    }
    .component-name {
      display: block;
      font-weight: 600;
      font-size: 14px;
    }
    .data-prep {
      background: #E3F2FD;
      border: 2px solid #1976D2;
    }
    .execution {
      background: #E8F5E9;
      border: 2px solid #388E3C;
    }
    .analysis {
      background: #FFF3E0;
      border: 2px solid #F57C00;
    }
    .arrow-down {
      width: 2px;
      height: 30px;
      background: #546E7A;
      position: relative;
    }
    .arrow-down::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: -4px;
      border: 5px solid transparent;
      border-top: 8px solid #546E7A;
    }
    .branch-connector {
      display: flex;
      align-items: flex-start;
      justify-content: center;
    }
    .branch-line {
      width: 100px;
      height: 2px;
      background: #546E7A;
      margin-top: 15px;
    }
    .figure-caption {
      text-align: center;
      font-style: italic;
      font-size: 14px;
      color: #555;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure 2</div>
    <h2 class="diagram-title">Branching Architecture</h2>

    <div class="architecture">
      <div class="component-box data-prep">
        <span class="component-name">Input Handler</span>
      </div>
      <div class="arrow-down"></div>
      <div class="row">
        <div class="component-box execution">
          <span class="component-name">Path A</span>
        </div>
        <div class="component-box execution">
          <span class="component-name">Path B</span>
        </div>
      </div>
      <div class="arrow-down"></div>
      <div class="component-box analysis">
        <span class="component-name">Aggregator</span>
      </div>
    </div>

    <p class="figure-caption">
      Y-split architecture with parallel processing paths converging to aggregation.
    </p>
  </div>
</body>
</html>
```

## Comparison (Before/After)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Before/After Comparison</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      padding: 40px;
      background: white;
    }
    .diagram-container {
      max-width: 1000px;
      margin: 0 auto;
      padding: 30px;
    }
    .figure-label {
      text-align: center;
      font-size: 12px;
      color: #666;
      margin-bottom: 8px;
    }
    .diagram-title {
      text-align: center;
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 30px 0;
    }
    .comparison {
      display: flex;
      justify-content: center;
      gap: 60px;
    }
    .side {
      flex: 1;
      max-width: 400px;
    }
    .side-label {
      text-align: center;
      font-weight: 600;
      font-size: 14px;
      margin-bottom: 20px;
      padding: 8px;
      border-radius: 4px;
    }
    .before .side-label {
      background: #FFEBEE;
      color: #C62828;
    }
    .after .side-label {
      background: #E8F5E9;
      color: #2E7D32;
    }
    .component-box {
      padding: 15px 20px;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
      text-align: center;
      margin: 10px 0;
    }
    .before .component-box {
      background: #FFEBEE;
      border: 2px solid #EF9A9A;
    }
    .after .component-box {
      background: #E8F5E9;
      border: 2px solid #81C784;
    }
    .arrow-down {
      width: 2px;
      height: 20px;
      background: #546E7A;
      margin: 0 auto;
    }
    .figure-caption {
      text-align: center;
      font-style: italic;
      font-size: 14px;
      color: #555;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure 3</div>
    <h2 class="diagram-title">Architecture Comparison</h2>

    <div class="comparison">
      <div class="side before">
        <div class="side-label">BEFORE</div>
        <div class="component-box">Monolithic Handler</div>
        <div class="arrow-down"></div>
        <div class="component-box">Direct Processing</div>
        <div class="arrow-down"></div>
        <div class="component-box">Single Output</div>
      </div>

      <div class="side after">
        <div class="side-label">AFTER</div>
        <div class="component-box">Request Router</div>
        <div class="arrow-down"></div>
        <div class="component-box">Parallel Workers</div>
        <div class="arrow-down"></div>
        <div class="component-box">Aggregated Output</div>
      </div>
    </div>

    <p class="figure-caption">
      Side-by-side comparison showing architectural improvements.
    </p>
  </div>
</body>
</html>
```

## Color Reference

| Stage | Fill | Border | CSS Class |
|-------|------|--------|-----------|
| Data Preparation | `#E3F2FD` | `#1976D2` | `.data-prep` |
| Execution | `#E8F5E9` | `#388E3C` | `.execution` |
| Analysis | `#FFF3E0` | `#F57C00` | `.analysis` |
| Input/Output | `#FF6B6B` | `#FF6B6B` | `.terminal` |
| Error/Before | `#FFEBEE` | `#EF9A9A` | `.error` |
| Success/After | `#E8F5E9` | `#81C784` | `.success` |

## Visual Standards

| Element | Value |
|---------|-------|
| Border radius | `6px` |
| Box shadow | `0 2px 4px rgba(0,0,0,0.08)` |
| Arrow color | `#546E7A` |
| Arrow width | `2px` line, `8px` head |
| Font | System UI stack |
| Component padding | `20px 30px` |
| Gap between elements | `20px` |

## Capture Command

```bash
# High-res PNG capture (2x retina)
node scripts/capture-diagram.js diagram.html output.png
```

**Note**: Use the provided Node.js script, not Playwright CLI (which lacks `--device-scale-factor` support).
