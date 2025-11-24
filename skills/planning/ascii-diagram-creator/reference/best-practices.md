# Best Practices

Guidelines for creating clear, effective ASCII diagrams.

## Formatting Rules

### Width Constraints

**Maximum line width: 80 characters**

This ensures compatibility with:
- Terminal windows
- Code review tools
- Markdown rendering
- Email clients

```
# Good - fits in 80 chars
┌──────────────────────────────────────────────────────────────────────────┐

# Bad - exceeds 80 chars, will wrap
┌────────────────────────────────────────────────────────────────────────────────────┐
```

### Alignment

**Vertical alignment** creates visual hierarchy:

```
# Good - aligned centers
┌─────────┐
│ Step 1  │
└─────────┘
     │
     ▼
┌─────────┐
│ Step 2  │
└─────────┘

# Bad - misaligned
┌─────────┐
│ Step 1  │
└─────────┘
        │
        ▼
   ┌─────────┐
   │ Step 2  │
   └─────────┘
```

**Horizontal alignment** for side-by-side comparisons:

```
# Good - columns aligned
BEFORE:                    AFTER:
├── file1.js        ──►    ├── file1.ts
└── file2.js        ──►    └── file2.ts

# Bad - uneven columns
BEFORE:          AFTER:
├── file1.js ──► ├── file1.ts
└── file2.js   ──►   └── file2.ts
```

### Spacing

Use blank lines to separate logical sections:

```
┌─────────────────────────────────────────────┐
│           MIGRATION PLAN                     │
└─────────────────────────────────────────────┘

PHASE 1: Analysis
┌──────────────────┐
│ Analyze current  │
└──────────────────┘

PHASE 2: Migration
┌──────────────────┐
│ Execute changes  │
└──────────────────┘
```

## Clarity Guidelines

### Use Consistent Box Sizes

Keep related boxes the same width:

```
# Good - consistent widths
┌──────────────────┐    ┌──────────────────┐
│ Component A      │    │ Component B      │
└──────────────────┘    └──────────────────┘

# Bad - inconsistent
┌────────┐    ┌────────────────────────┐
│ Comp A │    │ Component B            │
└────────┘    └────────────────────────┘
```

### Include Legends

When using symbols, explain them:

```
┌──────────────────┐
│ ✓ Database       │
│ ⏳ API           │
│ ✗ Legacy         │
└──────────────────┘

Legend:
✓ = Complete
⏳ = In Progress
✗ = Removed
```

### Group Related Items

Use visual proximity to show relationships:

```
┌─────────────────────────────────────────┐
│          FRONTEND LAYER                  │
├─────────────────────────────────────────┤
│ • React Components                       │
│ • State Management                       │
│ • Routing                                │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│          BACKEND LAYER                   │
├─────────────────────────────────────────┤
│ • API Endpoints                          │
│ • Business Logic                         │
│ • Database Access                        │
└─────────────────────────────────────────┘
```

## Information Density

### Include Status Indicators

Show progress at a glance:

```
│ ✓ Step 1: Setup          │
│ ✓ Step 2: Configuration  │
│ ⏳ Step 3: Migration     │
│   Step 4: Validation     │
```

### Show Counts When Relevant

Provide context with numbers:

```
┌──────────────────┐
│ Current State    │
│ 11 directories   │
│ 47 files         │
│ 3 duplicates     │
└──────────────────┘
```

### Add Brief Descriptions

Clarify purpose without cluttering:

```
┌──────────────────┐
│ Auth Service     │──► Handles JWT tokens
│ 3 endpoints      │──► Login, logout, refresh
└──────────────────┘
```

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Exceeding 80 chars | Wrapping breaks diagram | Split or abbreviate |
| No legend | Symbols are confusing | Always include legend |
| Inconsistent boxes | Looks unprofessional | Standardize widths |
| Too much detail | Overwhelming | Simplify or split |
| No spacing | Hard to read | Add blank lines |
| Misaligned arrows | Confusing flow | Check alignment |
