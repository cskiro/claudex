# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Documentation Check Workflow (Universal)

**Purpose**: Ensure critical documentation stays current with code changes before PR creation.

---

## When to Apply

Run documentation check:
- **Before creating a PR** - Verify docs reflect your changes
- **After significant feature work** - Before marking task complete
- **When touching core systems** - Architecture, auth, data models, APIs

---

## Critical Docs Checklist

Before PR creation, verify these docs are current:

```
┌────────────────────────────────────────────────────────────────┐
│  DOCUMENTATION CHECK                                           │
├────────────────────────────────────────────────────────────────┤
│  [ ] CLAUDE.md - Build commands, patterns, standards current?  │
│  [ ] README.md - Setup steps, usage examples accurate?         │
│  [ ] CHANGELOG.md - Changes documented for release?            │
│  [ ] Architecture diagrams - Still reflect current design?     │
│  [ ] ADRs - New technical decisions recorded?                  │
│  [ ] package.json - Scripts/deps match documentation?          │
└────────────────────────────────────────────────────────────────┘
```

---

## What Triggers Doc Updates

| Change Type | Docs to Update |
|-------------|----------------|
| New build/test command | CLAUDE.md, README.md |
| New feature | CHANGELOG.md, README.md (if user-facing) |
| Architecture change | Architecture docs, ADR |
| New dependency | README.md if setup changes |
| Bug fix | CHANGELOG.md |
| API change | API docs, README.md examples |
| Technical decision | ADR |

---

## Integration with PR Workflow

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│   Tests    │──▶│    Code    │──▶│    Docs    │──▶│  Create    │
│   Pass     │   │ Simplifier │   │   Check    │   │    PR      │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Better Approach |
|--------------|----------------|-----------------|
| "I'll update docs later" | Docs become stale, context lost | Update docs as you code |
| Documenting everything | Travel Light principle violated | Focus on critical docs only |
| Orphan docs | Clutter, misleading info | Delete when code changes |
| Docs only in markdown | Hard to keep in sync | Prefer docs-in-code (JSDoc, docstrings) |
