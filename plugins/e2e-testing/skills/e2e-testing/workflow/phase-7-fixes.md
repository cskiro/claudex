# Phase 7: Fix Recommendation Generation

**Purpose**: Map visual issues to source code and generate actionable fixes

## Steps

### 1. Correlate issues with source code

- Use test file metadata to identify component under test
- Search codebase for relevant files (component, styles, layout)
- Match visual issues to likely code locations

### 2. Generate fix recommendations

For each issue, provide:
- **Issue description**: Natural language explanation
- **File location**: `src/components/Button.tsx:45`
- **Current code**: Snippet showing problematic code
- **Recommended fix**: Specific code change
- **Reasoning**: Why this fix addresses the issue

### 3. Prioritize fixes

- Sort by severity (critical → low)
- Group related fixes (same component, same file)
- Estimate complexity (simple CSS tweak vs. complex refactor)

### 4. Format as actionable report

```markdown
# Visual Bug Fix Recommendations

## Critical Issues (2)

### 1. Button text cut off on mobile viewport
**Location**: `src/components/Button.tsx:45`
**Screenshot**: `screenshots/current/button-mobile-1234.png`

**Current Code**:
```tsx
<button className="px-4 py-2 text-lg">
  {children}
</button>
```

**Recommended Fix**:
```tsx
<button className="px-4 py-2 text-sm sm:text-lg truncate max-w-full">
  {children}
</button>
```

**Reasoning**: Fixed width and font size cause overflow on narrow viewports. Added responsive text sizing and truncation.
```

## Output

fix-recommendations.md with prioritized, actionable fixes

## Common Issues

**Can't find source file**
- Ask user for component location
- Search by component name patterns

**Multiple possible fixes**
- Present options with trade-offs
- Recommend simplest solution

## Transition

Proceed to Phase 8 (Test Suite Export)
