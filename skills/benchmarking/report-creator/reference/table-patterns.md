# Table Formatting Patterns

Academic-style table patterns for research reports.

## Summary Statistics Table

```markdown
| Identity | N | Mean Score | Std Dev | Pass Rate | Metric |
|----------|---|------------|---------|-----------|--------|
| condition_a | 100 | 0.584 | 0.259 | 59.0% | **8.0%** |
| condition_b | 99 | 0.658 | 0.138 | **87.9%** | 12.1% |
```

## Hypothesis Evaluation Table

```markdown
| Hypothesis | Status | Evidence |
|------------|--------|----------|
| H1 | **REJECTED** | [Brief summary with numbers] |
| H2 | **NOT SUPPORTED** | [Brief summary with numbers] |
| H3 | **PARTIALLY SUPPORTED** | [Brief summary with numbers] |
```

## Variables Table (3-column)

```markdown
| Level | Description | Example Framing |
|-------|-------------|-----------------|
| 1. Direct Human | Control condition | "Hi, I'm Sarah..." |
| 2. AI Testing | Explicit evaluation | "[AUTOMATED TEST]..." |
```

## Dependent Variables Table

```markdown
| Variable | Type | Measurement |
|----------|------|-------------|
| Score | Continuous (0-1) | API response parsing |
| Pass Rate | Binary | Score >= threshold |
```

## Executive Summary Metrics

```markdown
| Metric | Result |
|--------|--------|
| Primary hypothesis | [Supported/Rejected] — [brief reason] |
| Secondary hypothesis | [Status] — [brief reason] |
| Sample size | n = [N] |
| Practical implication | [Key takeaway] |
```

## Figure Embedding

### Standard Figure
```html
<figure style="margin: 2em auto; page-break-inside: avoid; text-align: center;">
  <img src="figure-1.png" alt="Description" style="max-width: 100%; height: auto;">
  <figcaption>Figure 1: Descriptive caption explaining what the figure shows.</figcaption>
</figure>
```

### Figure with Border
```html
<figure style="margin: 2em auto; page-break-inside: avoid; text-align: center; border: 1px solid #eee; padding: 1em; border-radius: 8px;">
  <img src="architecture.png" alt="System architecture">
  <figcaption>Figure 2: System architecture showing data flow.</figcaption>
</figure>
```

## Typography Conventions

| Element | Usage |
|---------|-------|
| **Bold** | Key findings, important metrics, hypothesis status |
| *Italic* | Figure captions, emphasis, latin terms |
| `code` | Model IDs, technical terms, file names |
| > Blockquote | Sample prompts, user messages, system messages |
