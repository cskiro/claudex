# CSS Components Reference

Complete CSS class definitions for academic-style diagrams.

## Base Container

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #ffffff;
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
```

## Typography

```css
.figure-label {
  font-size: 12px;
  color: #57606a;
  margin-bottom: 8px;
  font-weight: 500;
}

.diagram-title {
  font-size: 18px;
  font-weight: 600;
  color: #24292f;
  text-align: center;
  margin-bottom: 30px;
}

.figure-caption {
  text-align: center;
  margin-top: 25px;
  font-size: 12px;
  color: #57606a;
  font-style: italic;
}
```

## Stage Labels

```css
.stage-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 30px;
  margin-bottom: 15px;
}

.stage-label {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6e7781;
  text-align: center;
}
```

## Component Boxes

```css
.component {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.component-box {
  width: 130px;
  height: 72px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  border: 1px solid;
}

.component-name {
  font-size: 12px;
  font-weight: 600;
  color: #24292f;
  line-height: 1.3;
}

.component-tech {
  font-size: 9px;
  color: #57606a;
  margin-top: 4px;
  font-style: italic;
}
```

## Color-Coded Stages

```css
/* Data Preparation - Blue */
.component-box.data-prep {
  background: #e3f2fd;
  border-color: #1976d2;
}

/* Execution - Green */
.component-box.execution {
  background: #e8f5e9;
  border-color: #388e3c;
}

/* Analysis - Orange */
.component-box.analysis {
  background: #fff3e0;
  border-color: #f57c00;
}
```

## Data Labels

```css
.data-label {
  font-size: 9px;
  color: #57606a;
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
  margin-bottom: 6px;
  white-space: nowrap;
  height: 14px;
}
```

## Terminal Circles

```css
.terminal {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.terminal.input {
  background: #fff;
  border: 3px solid #ff6b6b;
  color: #ff6b6b;
}

.terminal.output {
  background: #ff6b6b;
  border: 3px solid #ff6b6b;
  color: #fff;
}
```

## Arrows

```css
.arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  flex-shrink: 0;
  padding-top: 20px;
}

.arrow svg {
  width: 40px;
  height: 16px;
}

.arrow path {
  fill: none;
  stroke: #546e7a;
  stroke-width: 2;
}

.arrow polygon {
  fill: #546e7a;
}
```

**Arrow SVG Template**:
```html
<svg viewBox="0 0 40 16">
  <path d="M0,8 L30,8" />
  <polygon points="30,4 38,8 30,12" />
</svg>
```

## Stage Brackets

```css
.stage-brackets {
  display: flex;
  justify-content: center;
  padding: 0 30px;
  margin-top: 5px;
}

.bracket {
  height: 12px;
  border-left: 2px solid #d0d7de;
  border-right: 2px solid #d0d7de;
  border-bottom: 2px solid #d0d7de;
  border-radius: 0 0 4px 4px;
}
```

## Legend

```css
.legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e1e4e8;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  color: #57606a;
}

.legend-swatch {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  border: 1px solid;
}
```

## Alternative Color Schemes

### Monochrome (Print-Friendly)

```css
.component-box.data-prep { background: #f5f5f5; border-color: #9e9e9e; }
.component-box.execution { background: #e0e0e0; border-color: #757575; }
.component-box.analysis { background: #bdbdbd; border-color: #616161; }
```

### Dark Theme

```css
.diagram-container { background: #1e1e1e; border-color: #333; }
.diagram-title { color: #e0e0e0; }
.component-box.data-prep { background: #1e3a5f; border-color: #42a5f5; }
.component-box.execution { background: #1b5e20; border-color: #66bb6a; }
.component-box.analysis { background: #e65100; border-color: #ffa726; }
```
