# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Code Simplifier Workflow (Universal)

**Purpose**: Ensure code clarity and maintainability before PR creation.

---

## When to Use

Run the `code-simplifier` agent as the **final quality gate** before creating a PR:

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Feature   │──▶│   Tests    │──▶│   Code     │──▶│  Create    │
│  Complete  │   │   Pass     │   │ Simplifier │   │    PR      │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
```

**Trigger conditions** (all must be true):
- All acceptance criteria met
- Lint, test, and build pass
- Ready to create PR or commit final changes

---

## How to Invoke

```
subagent_type: "pr-review-toolkit:code-simplifier"
```

### Example Prompt

```
Review and simplify the recently modified files:

1. `path/to/file1.ts` - Brief description
2. `path/to/file2.ts` - Brief description

Focus on:
- Code clarity and maintainability
- Removing unnecessary complexity
- Consistent patterns
- Preserving all functionality

Do NOT change security-sensitive code or undo intentional patterns.
```

---

## What It Does

| Refinement | Example |
|------------|---------|
| Extract named functions | Inline logic -> `buildLabels()`, `isDuplicate()` |
| Simplify array operations | `.filter()[0]` -> `.find()` |
| Improve cleanup patterns | Nested try/catch -> `finally` block |
| Enhance variable naming | `x` -> `canAutoRemediate` |
| Consolidate patterns | Extend existing conventions |

**Preserved by default:**
- Security fixes (CodeQL patterns, input validation)
- Intentional complexity (performance optimizations)
- External API contracts

---

## When to Skip

Skip code-simplifier for:
- Trivial changes (typos, version bumps, config tweaks)
- Emergency hotfixes (document skip reason)
- Auto-generated files (migrations, lockfiles)
- Files with no logic changes (pure additions)

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Better Approach |
|--------------|----------------|-----------------|
| Skip simplifier "to save time" | Technical debt compounds | Always run before PR |
| Run on entire codebase | Scope creep, unrelated changes | Target modified files only |
| Undo security fixes | Reintroduces vulnerabilities | Exclude security patterns |
| Run before tests pass | May simplify broken code | Verify first, simplify second |
