# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# PR Review Toolkit Workflow (Universal)

**Purpose**: Comprehensive pre-PR quality review using specialized AI agents.

---

## Overview

The PR Review Toolkit provides 6 specialized agents for automated code review:

| Agent | Model | Purpose |
|-------|-------|---------|
| `code-reviewer` | Opus | Guidelines compliance, bug detection, security issues |
| `code-simplifier` | Opus | Code clarity, refactoring, maintainability |
| `comment-analyzer` | Adaptive | Comment accuracy, JSDoc/docstring validation |
| `pr-test-analyzer` | Adaptive | Test coverage quality, missing test scenarios |
| `silent-failure-hunter` | Adaptive | Error handling audit, unhandled exceptions |
| `type-design-analyzer` | Adaptive | Type design quality, TypeScript patterns |

---

## When to Use

### Proactive Triggers

Proactively offer PR review when:
- Saying "ready for PR", "ready to create PR", "can you review before I commit"
- Completing a feature branch and all tests pass
- Asking for code review before merging

### Decision Matrix

| Task Type | Recommended Agents |
|-----------|-------------------|
| Standard feature PR | `code-reviewer` → `pr-test-analyzer` → `code-simplifier` |
| Bug fix PR | `code-reviewer` → `silent-failure-hunter` → `code-simplifier` |
| TypeScript refactoring | `code-reviewer` → `type-design-analyzer` → `code-simplifier` |
| Documentation heavy | `comment-analyzer` → docs-check |
| Security-sensitive | `code-reviewer` → `silent-failure-hunter` |
| New API endpoints | `code-reviewer` → `type-design-analyzer` → `pr-test-analyzer` |

---

## Workflow Integration

### Full Pre-PR Quality Flow

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│   Tests    │──▶│   Review   │──▶│  Simplify  │──▶│    Docs    │
│   Pass     │   │   Agents   │   │   Agent    │   │   Check    │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  code-   │  │  pr-test │  │  silent- │
   │ reviewer │  │ analyzer │  │ failure  │
   └──────────┘  └──────────┘  └──────────┘
    (parallel)    (parallel)    (parallel)
```

### Parallel vs Sequential

**Run in Parallel** (independent analysis):
- `code-reviewer` + `pr-test-analyzer` + `silent-failure-hunter`
- `type-design-analyzer` + `comment-analyzer`

**Run Sequentially** (dependent on previous):
- `code-simplifier` - Run **last** after all issues resolved

---

## Invocation Quick Reference

| Agent | subagent_type | Primary Focus |
|-------|---------------|---------------|
| code-reviewer | `pr-review-toolkit:code-reviewer` | Bugs, guidelines, security |
| code-simplifier | `pr-review-toolkit:code-simplifier` | Clarity, maintainability |
| comment-analyzer | `pr-review-toolkit:comment-analyzer` | Comment accuracy |
| pr-test-analyzer | `pr-review-toolkit:pr-test-analyzer` | Test coverage quality |
| silent-failure-hunter | `pr-review-toolkit:silent-failure-hunter` | Error handling |
| type-design-analyzer | `pr-review-toolkit:type-design-analyzer` | TypeScript patterns |

---

## Pre-PR Checklist

```
┌────────────────────────────────────────────────────────────────┐
│  PRE-PR QUALITY CHECKLIST                                      │
├────────────────────────────────────────────────────────────────┤
│  [ ] All acceptance criteria met                               │
│  [ ] Tests pass                                                │
│  [ ] code-reviewer: Guidelines compliance, bugs               │
│  [ ] pr-test-analyzer: Test coverage adequate                 │
│  [ ] silent-failure-hunter: Error handling (if applicable)    │
│  [ ] type-design-analyzer: Type design (if new types)         │
│  [ ] comment-analyzer: Comments accurate (if docs added)      │
│  [ ] code-simplifier: Final refinements                       │
│  [ ] Documentation current                                     │
└────────────────────────────────────────────────────────────────┘
```

---

## When to Skip

Skip full toolkit review for:
- Trivial changes (typos, version bumps, config tweaks)
- Documentation-only PRs (use `comment-analyzer` only)
- Emergency hotfixes (document skip reason in PR)
- Auto-generated files (migrations, lockfiles)
