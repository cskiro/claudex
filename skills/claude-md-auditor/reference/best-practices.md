# Community Best Practices

Field-tested recommendations from practitioners. These are suggestions, not requirements.

## Size Recommendations

### Target Range
- **Optimal**: 100-300 lines
- **Acceptable**: Up to 500 lines with @imports
- **Warning**: > 500 lines indicates need for splitting

### Token Budget
- **Recommended**: < 3,000 tokens
- **Maximum**: 5,000 tokens before significant context cost
- **Measure**: Use `wc -w` as rough estimate (tokens ≈ words × 1.3)

## Content Organization

### 80/20 Rule
- 80% essential, immediately-applicable guidance
- 20% supporting context and edge cases

### Section Priority
1. **Critical** (MUST follow): Security, breaking patterns
2. **Important** (SHOULD follow): Core standards, conventions
3. **Recommended** (COULD follow): Optimizations, preferences

### Header Hierarchy
```markdown
# Project Name
## Build Commands (most used first)
## Architecture Overview
## Coding Standards
## Testing Requirements
## Common Patterns
```

## Import Strategies

### When to Import
- Detailed documentation > 50 lines
- Shared standards across projects
- Frequently updated content

### Import Organization
```markdown
## Core Standards
@standards/typescript.md
@standards/testing.md

## Project-Specific
@docs/architecture.md
@docs/api-patterns.md
```

## Version Control Practices

### Commit Discipline
- Commit CLAUDE.md changes separately
- Use descriptive messages: "docs: update testing standards in CLAUDE.md"
- Review in PRs like any other code

### Change Tracking
```markdown
---
**Last Updated**: 2025-10-26
**Version**: 1.2.0
**Changes**: Added memory retrieval patterns
---
```

## Maintenance Cadence

### Regular Reviews
- **Weekly**: Check for outdated commands
- **Monthly**: Review against actual practices
- **Quarterly**: Full audit and optimization

### Staleness Indicators
- Commands that no longer work
- References to removed files
- Outdated dependency versions
- Patterns no longer used

## Multi-Project Strategies

### Shared Base
```
~/.claude/CLAUDE.md           # Personal defaults
~/.claude/standards/          # Shared standards
  ├── typescript.md
  ├── testing.md
  └── security.md
```

### Project Override
```markdown
# Project CLAUDE.md

## Override user defaults
@~/.claude/standards/typescript.md

## Project-specific additions
...
```

## Anti-Pattern Avoidance

### Don't Duplicate
- If it's in official docs, don't repeat it
- If it's in your codebase comments, reference don't copy

### Don't Over-Specify
- Trust Claude's knowledge
- Focus on YOUR project's quirks
- Specify deviations from standards, not standards themselves

### Don't Neglect Updates
- Outdated CLAUDE.md is worse than none
- Schedule regular maintenance
- Delete rather than leave stale
