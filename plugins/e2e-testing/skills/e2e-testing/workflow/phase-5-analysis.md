# Phase 5: Visual Analysis

**Purpose**: Use LLM vision capabilities to analyze screenshots and identify issues

## Steps

### 1. Batch screenshot analysis

Read all captured screenshots and ask LLM to identify:
- UI bugs (broken layouts, overlapping elements, cut-off text)
- Accessibility issues (low contrast, missing labels, improper heading hierarchy)
- Responsive problems (elements not scaling, overflow issues)
- Missing or misaligned elements
- Unexpected visual artifacts

### 2. Categorize findings

- **Critical**: App is broken/unusable (crashes, white screen, no content)
- **High**: Major UI bugs affecting core functionality
- **Medium**: Visual inconsistencies that impact UX
- **Low**: Minor alignment or styling issues

### 3. Generate issue descriptions

For each issue:
- Natural language description
- Screenshot reference with highlighted problem area
- Affected viewport/browser if relevant
- User impact assessment

## Output

Structured list of visual issues with severity ratings:

```markdown
## Visual Issues Found

### Critical (1)
- White screen on mobile viewport - App fails to render

### High (2)
- Button text cut off at 375px width
- Form labels overlap input fields

### Medium (3)
- Header alignment inconsistent
- ...
```

## Performance

~5-10 seconds per screenshot for LLM analysis

## Common Issues

**Analysis fails**
- Retry analysis
- Skip corrupted images
- Validate PNG format

**Too many false positives**
- Adjust analysis prompts
- Focus on critical issues first

## Transition

Proceed to Phase 6 (Regression Detection)
