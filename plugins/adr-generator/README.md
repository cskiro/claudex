# ADR Generator Plugin

Architecture Decision Records (ADRs) creation with standard templates and structured documentation.

## Installation

```bash
/plugin marketplace add cskiro/claudex --plugin adr-generator
```

## Usage

Invoke the skill when making significant architectural decisions:

```
Create an ADR for choosing PostgreSQL over MongoDB for our persistence layer
```

```
Document the architecture decision to adopt event sourcing
```

```
New ADR: implementing CQRS pattern for read/write separation
```

## Triggers

- "create ADR"
- "document architecture decision"
- "new ADR"
- "record decision"
- "architecture decision record"

## What This Skill Does

1. **Identifies** the architectural decision to document
2. **Gathers** context, constraints, and stakeholder concerns
3. **Lists** options considered with pros/cons analysis
4. **Documents** the decision with clear rationale
5. **Saves** to standard `docs/adr/` directory structure

## ADR Format

Generated ADRs follow the standard format:

- **Status**: Proposed, Accepted, Deprecated, or Superseded
- **Context**: The issue motivating this decision
- **Decision**: The change being proposed/implemented
- **Consequences**: Positive, negative, and neutral impacts

## When to Use

- Choosing between technologies or frameworks
- Defining API design patterns
- Selecting architectural patterns
- Making security-related decisions
- Establishing coding standards that affect architecture

## When NOT to Use

- Code documentation (use docstrings/JSDoc)
- README files
- Implementation details
- Trivial decisions that don't affect architecture

## Version

0.1.0
