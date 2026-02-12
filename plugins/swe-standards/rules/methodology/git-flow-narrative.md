# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Git Flow with Narrative Templates (Universal)

**Purpose**: Ensure commits and PRs tell a coherent story of human-AI collaboration.

---

## When This Applies

Use narrative templates for:
- Feature implementation with AI assistance
- Refactoring sessions
- Bug investigations where diagnosis process matters
- Configuration/tooling changes with non-obvious rationale
- Any multi-commit PR where context matters for future readers

**Skip for**: Trivial fixes (typos, version bumps), automated commits, emergency hotfixes.

---

## Branch Naming

Pattern: `<type>/<descriptive-name>`

| Type | Use Case |
|------|----------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `hotfix/` | Production hotfixes |
| `refactor/` | Code refactoring |
| `docs/` | Documentation |
| `chore/` | Maintenance tasks |

### Rules

1. **One branch = One scope**: Each branch addresses exactly ONE feature or ONE GitHub issue
2. **Descriptive names**: Use clear, explicit names that describe the change
3. **No opaque identifiers**: Never use phase/batch/round numbering, bare issue numbers, or vague labels

---

## Commit Template

```
<type>(<scope>): <brief action> [TICKET-ID]

Intent: <what the user wanted to accomplish>
Interpretation: <how the model understood the request>
Action: <what was done and why>
Insight: <key learning or pattern discovered>

Co-Authored-By: Claude <model> <noreply@anthropic.com>
```

### Constraints
- **Total length**: ≤100 words (excluding header line)
- **Voice**: Past tense, active voice
- **Tone**: Conversational but technical

### Section Guidelines

| Section | Purpose | Length |
|---------|---------|--------|
| Intent | User's goal, not technical ask | 1-2 sentences |
| Interpretation | How AI translated intent to approach | 1-2 sentences |
| Action | What was done, key decisions, outcomes | 2-3 sentences |
| Insight | Pattern, lesson, or discovery | 1-2 sentences |

---

## PR Description Template

```markdown
## Chapter: <descriptive title>

### The Ask
<What did the user want to accomplish? What problem were they solving?>

### The Journey
<Narrative summary of how the work unfolded—key decisions, pivots, discoveries>

### The Architecture
<ASCII diagram if structural changes occurred, otherwise omit>

### The Outcome
<What was delivered? Measurable results where applicable>

### The Lessons
<Insights distilled from the work—patterns discovered, gotchas encountered>

### Commit Narrative
<Brief annotation of each commit's role in the story>

### References
Closes #<GitHub-issue-number>

---

Generated with [Claude Code](https://claude.ai/code)
```

---

## Quick Reference

### Commit Example

```
refactor(cleanup): remove orphan files [PROAI-206]

Intent: User wanted to reduce codebase size by removing unused files.
Interpretation: Leveraged Knip baseline to identify files with zero imports.
Action: Removed 31 source files, 29 test files, and 11 empty directories.
Verified through typecheck, lint, tests (2,579 passing), and build.
Insight: Orphan files often form interconnected islands—dependency graph
analysis from entry points catches these where file-level linting cannot.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## Narrative Flow

When reading git log, commits should flow like chapters:

```
┌─────────────────────────────────────────────────────────────────────┐
│  COMMIT 1: "User wanted X. Interpreted as Y. Did Z. Learned W."    │
│                              |                                      │
│  COMMIT 2: "Building on W, user wanted A. Approached via B..."     │
│                              |                                      │
│  COMMIT 3: "Discovery from B revealed C. Adjusted approach..."     │
└─────────────────────────────────────────────────────────────────────┘
```

Each commit references or builds on insights from previous commits when relevant.

---

## Pre-Commit Hooks

Recommended hooks for quality gates:

| Hook | Purpose |
|------|---------|
| Formatters | Black (Python), Prettier (JS/TS) |
| Linters | Ruff (Python), ESLint (JS/TS) |
| Type checking | mypy, tsc --noEmit |
| Secret scanning | git-secrets, detect-secrets |
