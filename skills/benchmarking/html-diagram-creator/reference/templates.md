# Diagram Templates

Ready-to-use HTML templates for common diagram patterns.

## Linear Pipeline Template

Standard left-to-right data flow (most common for benchmarks).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[TITLE]</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #fff;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 40px;
    }
    .diagram-container {
      background: #fafbfc;
      border: 1px solid #e1e4e8;
      border-radius: 8px;
      padding: 40px 50px;
      max-width: 1200px;
    }
    .figure-label { font-size: 12px; color: #57606a; margin-bottom: 8px; font-weight: 500; }
    .diagram-title { font-size: 18px; font-weight: 600; color: #24292f; text-align: center; margin-bottom: 30px; }
    .pipeline { display: flex; align-items: center; justify-content: center; }
    .component { display: flex; flex-direction: column; align-items: center; }
    .component-box {
      width: 130px; height: 72px; border-radius: 6px;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      text-align: center; padding: 10px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08); border: 1px solid;
    }
    .component-box.data-prep { background: #e3f2fd; border-color: #1976d2; }
    .component-box.execution { background: #e8f5e9; border-color: #388e3c; }
    .component-box.analysis { background: #fff3e0; border-color: #f57c00; }
    .component-name { font-size: 12px; font-weight: 600; color: #24292f; line-height: 1.3; }
    .component-tech { font-size: 9px; color: #57606a; margin-top: 4px; font-style: italic; }
    .data-label { font-size: 9px; color: #57606a; font-family: monospace; margin-bottom: 6px; height: 14px; }
    .terminal {
      width: 44px; height: 44px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 11px; font-weight: 600;
    }
    .terminal.input { background: #fff; border: 3px solid #ff6b6b; color: #ff6b6b; }
    .terminal.output { background: #ff6b6b; border: 3px solid #ff6b6b; color: #fff; }
    .arrow { display: flex; align-items: center; justify-content: center; width: 50px; padding-top: 20px; }
    .arrow svg { width: 40px; height: 16px; }
    .arrow path { fill: none; stroke: #546e7a; stroke-width: 2; }
    .arrow polygon { fill: #546e7a; }
    .figure-caption { text-align: center; margin-top: 25px; font-size: 12px; color: #57606a; font-style: italic; }
    .legend { display: flex; justify-content: center; gap: 24px; margin-top: 20px; padding-top: 15px; border-top: 1px solid #e1e4e8; }
    .legend-item { display: flex; align-items: center; gap: 6px; font-size: 10px; color: #57606a; }
    .legend-swatch { width: 16px; height: 16px; border-radius: 3px; border: 1px solid; }
    .legend-swatch.data-prep { background: #e3f2fd; border-color: #1976d2; }
    .legend-swatch.execution { background: #e8f5e9; border-color: #388e3c; }
    .legend-swatch.analysis { background: #fff3e0; border-color: #f57c00; }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="figure-label">Figure [N]</div>
    <h2 class="diagram-title">[TITLE]</h2>
    <div class="pipeline">
      <!-- Input Terminal -->
      <div class="component">
        <span class="data-label">&nbsp;</span>
        <div class="terminal input">In</div>
      </div>
      <div class="arrow"><svg viewBox="0 0 40 16"><path d="M0,8 L30,8"/><polygon points="30,4 38,8 30,12"/></svg></div>

      <!-- Component 1 -->
      <div class="component">
        <span class="data-label">[data_type_1]</span>
        <div class="component-box data-prep">
          <span class="component-name">[Name 1]</span>
          <span class="component-tech">[Technology]</span>
        </div>
      </div>
      <div class="arrow"><svg viewBox="0 0 40 16"><path d="M0,8 L30,8"/><polygon points="30,4 38,8 30,12"/></svg></div>

      <!-- Component 2 -->
      <div class="component">
        <span class="data-label">[data_type_2]</span>
        <div class="component-box execution">
          <span class="component-name">[Name 2]</span>
          <span class="component-tech">[Technology]</span>
        </div>
      </div>
      <div class="arrow"><svg viewBox="0 0 40 16"><path d="M0,8 L30,8"/><polygon points="30,4 38,8 30,12"/></svg></div>

      <!-- Component 3 -->
      <div class="component">
        <span class="data-label">[data_type_3]</span>
        <div class="component-box analysis">
          <span class="component-name">[Name 3]</span>
          <span class="component-tech">[Technology]</span>
        </div>
      </div>
      <div class="arrow"><svg viewBox="0 0 40 16"><path d="M0,8 L30,8"/><polygon points="30,4 38,8 30,12"/></svg></div>

      <!-- Output Terminal -->
      <div class="component">
        <span class="data-label">Results</span>
        <div class="terminal output">Out</div>
      </div>
    </div>
    <p class="figure-caption">[CAPTION - Describe what the diagram shows]</p>
    <div class="legend">
      <div class="legend-item"><div class="legend-swatch data-prep"></div><span>Data Preparation</span></div>
      <div class="legend-item"><div class="legend-swatch execution"></div><span>Execution</span></div>
      <div class="legend-item"><div class="legend-swatch analysis"></div><span>Analysis</span></div>
    </div>
  </div>
</body>
</html>
```

## Branching Architecture Template

For systems with parallel processing or multiple output paths.

```html
<!-- Add to body after pipeline -->
<div class="branch-container">
  <div class="branch-label">Branch A</div>
  <div class="pipeline branch">
    <!-- Branch A components -->
  </div>
  <div class="branch-label">Branch B</div>
  <div class="pipeline branch">
    <!-- Branch B components -->
  </div>
</div>

<style>
  .branch-container { margin-top: 20px; }
  .branch-label {
    font-size: 10px; font-weight: 600;
    color: #57606a; margin: 10px 0 5px 50px;
  }
  .pipeline.branch {
    padding-left: 50px;
    border-left: 2px solid #d0d7de;
  }
</style>
```

## Multi-Stage with Grouping Template

For showing distinct phases with visual grouping.

```html
<!-- Add stage labels above pipeline -->
<div class="stage-labels">
  <span class="stage-label" style="width: 280px;">Data Preparation</span>
  <span class="stage-label" style="width: 140px;">Execution</span>
  <span class="stage-label" style="width: 280px;">Analysis</span>
</div>

<!-- Add brackets below pipeline -->
<div class="stage-brackets">
  <div class="bracket" style="width: 340px; margin-right: 10px;"></div>
  <div class="bracket" style="width: 130px; margin-right: 10px;"></div>
  <div class="bracket" style="width: 340px;"></div>
</div>

<style>
  .stage-labels {
    display: flex; justify-content: space-between;
    padding: 0 30px; margin-bottom: 15px;
  }
  .stage-label {
    font-size: 10px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
    color: #6e7781; text-align: center;
  }
  .stage-brackets {
    display: flex; justify-content: center;
    padding: 0 30px; margin-top: 5px;
  }
  .bracket {
    height: 12px;
    border-left: 2px solid #d0d7de;
    border-right: 2px solid #d0d7de;
    border-bottom: 2px solid #d0d7de;
    border-radius: 0 0 4px 4px;
  }
</style>
```

## Vertical Stack Template

For systems with top-to-bottom flow.

```html
<style>
  .pipeline.vertical {
    flex-direction: column;
    gap: 0;
  }
  .arrow.vertical {
    transform: rotate(90deg);
    height: 50px;
    width: auto;
    padding: 0 20px;
  }
</style>
```

## Usage Notes

1. **Replace placeholders**: `[TITLE]`, `[N]`, `[Name]`, `[Technology]`, `[data_type]`, `[CAPTION]`
2. **Adjust widths**: Modify `.stage-label` and `.bracket` widths to match component count
3. **Add/remove components**: Copy component blocks as needed
4. **Change stages**: Use appropriate class (`data-prep`, `execution`, `analysis`)
