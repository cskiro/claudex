---
name: swe-standards
description: Software engineering standards navigator and scaffolder. Install production-grade TDD, git flow, security, and code quality rules into any project. Supports profiles (Core, TypeScript, Python, Testing, Quality, Security) for incremental adoption. TRIGGERS - "engineering standards", "what standards apply", "setup standards", "TDD workflow", "git branching rules", "code quality standards", "install swe standards". Use when adopting or navigating engineering standards for Claude Code projects.
---

# Software Engineering Standards

Production-grade engineering standards for Claude Code projects, packaged as installable rule profiles.

## Quick Start

```
/swe-standards:init     # Guided first-time setup
/swe-standards:check    # Verify installation health
/swe-standards:sync     # Update rules from upstream
/swe-standards:profile  # Show active profiles and rules
```

## What This Skill Provides

### 6 Standards Profiles

| Profile | Rules | Covers |
|---------|-------|--------|
| **Core** | 4 rules | Fail-fast, XP principles, git branching, git narrative, visual docs |
| **TypeScript** | 2 rules | Strict types, React patterns, Vitest CPU protection |
| **Python** | 1 rule | Type hints, Black/Ruff/mypy, Google docstrings |
| **Testing** | 2 rules | TDD red-green-refactor, Testing Trophy, Vitest CPU protection |
| **Quality** | 3 rules | PR review toolkit, code simplifier, docs freshness |
| **Security** | 1 rule | OWASP Top 10, auth patterns, secrets management |

### How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│  /swe-       │────▶│  Select      │────▶│  Rules scaffolded   │
│  standards:  │     │  profiles    │     │  to ~/.claude/rules/ │
│  init        │     │  (guided)    │     │  swe-standards/      │
└─────────────┘     └──────────────┘     └─────────────────────┘
```

1. **`/init`** detects your project type and recommends profiles
2. Selected rules are copied to `~/.claude/rules/swe-standards/`
3. Claude Code auto-loads them via its native rules system
4. **`/sync`** updates rules when upstream changes
5. **`/check`** verifies everything is healthy

## When to Use This Skill

- Setting up a new project with engineering standards
- Asking "what standards apply to this file?"
- Wanting to adopt TDD, git flow, or security practices
- Checking if your standards installation is healthy
- Updating to the latest version of standards

## Profiles in Detail

See [reference/profile-matrix.md](reference/profile-matrix.md) for the full mapping of which rules belong to which profiles.

See [reference/rule-catalog.md](reference/rule-catalog.md) for summaries of every rule.

## Adoption Guide

See [workflow/phase-1-setup.md](workflow/phase-1-setup.md) for step-by-step adoption instructions.

## Companion Plugins

These Claudex plugins work alongside swe-standards:

| Plugin | Purpose |
|--------|---------|
| `pr-review-toolkit` | Automated PR review agents (referenced by Quality profile) |
| `adr-generator` | Architecture Decision Records (referenced by XP principles) |

## Limitations

- Rules are scaffolded to `~/.claude/rules/`, not to project-level rules
- Profile selection is per-machine, not per-project (planned for future)
- Hook enforcement (branch validation) deferred to future release
