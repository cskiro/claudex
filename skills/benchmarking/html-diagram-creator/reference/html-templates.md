# HTML Diagram Templates

Copy-paste ready HTML templates for common diagram types.

## Linear Pipeline (3 boxes)

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

## Branching Architecture (Y-split)

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

## Comparison (Before/After)

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
