---
name: swe-standards
description: Software engineering standards navigator and scaffolder for Claude Code projects. This skill should be used when users want to install, configure, or navigate production-grade engineering rules for TDD, git flow, security, and code quality. Supports 6 installable profiles (Core, TypeScript, Python, Testing, Quality, Security) for incremental adoption. Common triggers include "set up engineering standards", "what standards apply to this file", "configure Claude Code rules", "install TDD workflow", "add TypeScript standards", "git branching rules", "code quality standards", "show my installed profiles", "update my standards", "help me set up project rules", "what rules should I use".
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
| **Core** | 5 rules | Fail-fast, XP principles, git branching, git narrative, visual docs |
| **TypeScript** | 2 rules | Strict types, React patterns, Vitest CPU protection (shared with Testing) |
| **Python** | 1 rule | Type hints, Black/Ruff/mypy, Google docstrings |
| **Testing** | 2 rules | TDD red-green-refactor, Testing Trophy, Vitest CPU protection (shared with TypeScript) |
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

See [workflow/setup-guide.md](workflow/setup-guide.md) for step-by-step adoption instructions.

## Companion Plugins

See [workflow/setup-guide.md](workflow/setup-guide.md#companion-plugins) for recommended companion plugins (`pr-review-toolkit`, `adr-generator`, `ascii-diagram-creator`).

## Limitations

- Rules are scaffolded to `~/.claude/rules/`, not to project-level rules
- Profile selection is per-machine, not per-project (planned for future)
- Hook enforcement (branch validation) deferred to future release
