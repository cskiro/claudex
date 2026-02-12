# SWE Standards Plugin

Production-grade software engineering standards for Claude Code, packaged as installable rule profiles.

## Installation

```bash
/plugin install swe-standards@claudex
```

## Usage

After installing the plugin, run the guided setup:

```
/swe-standards:init
```

This detects your project type and scaffolds the appropriate rules into `~/.claude/rules/swe-standards/` where Claude Code auto-loads them natively.

### Commands

| Command | Purpose |
|---------|---------|
| `/swe-standards:init` | Guided first-time setup with profile selection |
| `/swe-standards:sync` | Update rules from upstream plugin source |
| `/swe-standards:check` | Verify installation health and compliance |
| `/swe-standards:profile` | Show active profiles and installed rules |

## Profiles

Standards are organized into 6 profiles for incremental adoption:

| Profile | What You Get |
|---------|-------------|
| **Core** | Fail-fast principles, XP methodology, git branching, narrative commits, visual documentation |
| **TypeScript** | Strict types, React patterns, naming conventions |
| **Python** | Type hints, Black/Ruff/mypy, Google docstrings, functional patterns |
| **Testing** | TDD red-green-refactor, Testing Trophy (70% integration) |
| **Quality** | PR review toolkit workflow, code simplifier, docs freshness checks |
| **Security** | OWASP Top 10, auth patterns, secrets management, security headers |

**Core** is always included. Add profiles based on your stack:

- TypeScript project: Core + TypeScript + Testing + Quality
- Python project: Core + Python + Testing + Quality
- Full stack: Core + TypeScript + Python + Testing + Quality + Security

## How It Works

```
Plugin Source (rules/)          User Machine
┌─────────────────────┐        ┌─────────────────────────┐
│ core/               │  /init │ ~/.claude/rules/         │
│   core.md           │───────▶│   swe-standards/         │
│   xp-principles.md  │        │     core.md              │
│ methodology/        │        │     xp-principles.md     │
│   git-branching.md  │        │     git-branching.md     │
│   ...               │        │     ...                  │
│ language/           │        │                          │
│   typescript.md     │        │ ~/.claude/               │
│   python.md         │        │   swe-standards.json     │
│ quality/            │        │   (manifest with hashes) │
│   ...               │        └─────────────────────────┘
└─────────────────────┘
```

1. **`/init`** copies selected profile rules from the plugin to `~/.claude/rules/swe-standards/`
2. Claude Code auto-discovers and loads rules from `~/.claude/rules/`
3. A manifest (`~/.claude/swe-standards.json`) tracks versions and file hashes
4. **`/sync`** compares hashes and updates changed files (with conflict resolution)

## Dependencies

For the full standards experience:

- **pr-review-toolkit** *(external — Anthropic marketplace)* — Required for Quality profile's review agents. Install from Anthropic's plugin marketplace.
- **adr-generator** *(claudex marketplace)* — Architecture Decision Records. Install: `/plugin install adr-generator@claudex`
- **ascii-diagram-creator** *(claudex marketplace)* — Visual documentation standards. Install: `/plugin install ascii-diagram-creator@claudex`

## What's Included

### 12 Rule Files

| Category | Rules |
|----------|-------|
| Core | `core.md` (fail-fast, no silent failures), `xp-principles.md` (Kent Beck's 16 principles) |
| Methodology | `git-branching.md`, `git-flow-narrative.md`, `testing.md` |
| Domain | `security.md`, `visual-documentation.md` |
| Language | `typescript.md`, `python.md` |
| Quality | `pr-review-toolkit-workflow.md`, `code-simplifier-workflow.md`, `docs-check-workflow.md` |

### 4 Commands

Slash commands for managing your standards installation.

## Skill Documentation

See [`skills/swe-standards/SKILL.md`](./skills/swe-standards/SKILL.md) for detailed usage instructions.

## License

MIT
