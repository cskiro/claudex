---
name: adr-generator
version: 0.1.0
description: Creates Architecture Decision Records (ADRs) following standard templates. Documents architectural decisions with context, options considered, and rationale. TRIGGERS - "create ADR", "document architecture decision", "new ADR", "record decision", "architecture decision record". Use when making significant architectural choices that should be documented. NOT for code documentation or README files.
---

# ADR Generator

Create Architecture Decision Records following the standard ADR format.

## Quick Start

1. Identify the architectural decision to document
2. Gather context and constraints
3. List options considered with pros/cons
4. Document the decision and rationale
5. Save to `docs/adr/` or `adr/` directory

## ADR Template

```markdown
# ADR-NNNN: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

[What is the issue that we're seeing that is motivating this decision or change?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Neutral
- [Side effect that is neither positive nor negative]
```

## Workflow

| Step | Action | Output |
|------|--------|--------|
| 1 | Identify decision | Clear problem statement |
| 2 | Research options | List of alternatives |
| 3 | Evaluate tradeoffs | Pros/cons for each option |
| 4 | Document decision | ADR file |
| 5 | Get approval | Status -> Accepted |

## Naming Convention

```
docs/adr/
├── 0001-use-postgresql-for-persistence.md
├── 0002-adopt-event-sourcing.md
├── 0003-implement-cqrs-pattern.md
└── README.md (index of all ADRs)
```

## When to Create ADRs

- Choosing between technologies or frameworks
- Defining API design patterns
- Selecting architectural patterns (microservices, monolith, etc.)
- Making security-related decisions
- Establishing coding standards that affect architecture

## Limitations

- ADRs document decisions, not implementation details
- Keep ADRs focused on a single decision
- Link related ADRs rather than combining them
