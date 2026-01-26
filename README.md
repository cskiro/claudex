# Claudex - Claude Code Marketplace

> Skills and hooks for [Claude Code](https://claude.com/claude-code) - code quality analysis, testing automation, productivity tools, and DevOps workflows

## Quick Start

### Install via Marketplace

```bash
# Add the marketplace
/plugin marketplace add cskiro/claudex

# Install individual plugins
/plugin install accessibility-audit@claudex
/plugin install codebase-auditor@claudex
/plugin install skill-creator@claudex
# ... or any other plugin
```

Each skill is its own plugin - install only what you need.

---

## Repository Structure

Follows Anthropic's official `anthropics/claude-code/plugins/` pattern:

```
claudex/
├── .claude-plugin/
│   └── marketplace.json        # Plugin registry (single source of truth)
├── plugins/                    # 22 plugins (1 per skill)
│   ├── accessibility-audit/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   └── accessibility-audit/
│   │   └── README.md
│   ├── cc-insights/            # Includes hooks
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   └── cc-insights/
│   │   ├── hooks/
│   │   │   ├── hooks.json
│   │   │   └── extract-explanatory-insights.sh
│   │   └── README.md
│   └── ...
└── docs/                       # Documentation
```

---

## Available Plugins

All plugins follow the `plugin-name@claudex` installation pattern.

### API & Structured Outputs

| Plugin | Description |
|--------|-------------|
| **structured-outputs-advisor** | Expert advisor for choosing between JSON outputs and strict tool use modes |
| **json-outputs-implementer** | Implement JSON outputs mode with guaranteed schema compliance |
| **strict-tool-implementer** | Implement strict tool use mode with guaranteed parameter validation |

### Code Analysis

| Plugin | Description |
|--------|-------------|
| **codebase-auditor** | Comprehensive codebase analysis against 2024-25 SDLC standards |
| **bulletproof-react-auditor** | React codebase auditing against Bulletproof React architecture |
| **accessibility-audit** | WCAG 2.2 Level AA compliance auditing with MUI awareness |

### Claude Code Ecosystem

| Plugin | Description |
|--------|-------------|
| **cc-insights** | RAG-powered conversation analysis with semantic search and insight reports |
| **sub-agent-creator** | Generate Claude Code sub-agents following Anthropic's official patterns |
| **mcp-server-creator** | Create Model Context Protocol servers with TypeScript/Python SDKs |
| **claude-md-auditor** | Validate CLAUDE.md files against official standards and best practices |
| **otel-monitoring-setup** | Automated OpenTelemetry setup with Docker stack and Grafana dashboards |

### Skill Development

| Plugin | Description |
|--------|-------------|
| **skill-creator** | Generate skills following Claudex marketplace standards |
| **skill-isolation-tester** | Test skills in isolated environments (worktree, Docker, VMs) |
| **insight-skill-generator** | Generate skills from clustered insight patterns |

### Testing

| Plugin | Description |
|--------|-------------|
| **e2e-testing** | LLM-powered e2e testing with visual debugging and regression testing |
| **mutation-testing** | Test suite quality assessment via mutation analysis (Stryker, mutmut) |

> **Deprecated**: `test-driven-development` has been removed in favor of a `~/.claude/rules/` configuration. TDD is better enforced as a development rule than a skill.

### DevOps & Infrastructure

| Plugin | Description |
|--------|-------------|
| **react-project-scaffolder** | React project setup (sandbox, enterprise, mobile modes) |
| **github-repo-setup** | GitHub repository creation with security, CI/CD, and governance |
| **git-worktree-setup** | Parallel Claude Code sessions via git worktrees |

### Release & Documentation

| Plugin | Description |
|--------|-------------|
| **adr-generator** | Architecture Decision Records creation with standard templates |
| **ascii-diagram-creator** | ASCII diagram generation for architecture and data flows |
| **benchmark-report-creator** | Academic benchmark reports with diagrams and PDF export |
| **semantic-release-tagger** | Automated git tagging with conventional commit analysis |

### Hooks

The `cc-insights` plugin includes:

| Hook | Description |
|------|-------------|
| **extract-explanatory-insights** | Auto-extracts `★ Insight` blocks from Explanatory responses |

---

## Prerequisites

- **Claude Code** - Latest version ([Download](https://claude.com/claude-code))
- **Git** - For marketplace integration
- **Python** 3.8+ - For validation scripts and Python-based skills
- **jq** 1.6+ - For hooks (install via `brew install jq` on macOS)

---

## Features

- **23 Skills** distributed as individual plugins
- **1 Hook** for automated insight extraction (bundled with cc-insights)
- **Anthropic-aligned structure** - Mirrors official `anthropics/claude-code/plugins/` pattern
- **Modular installation** - Install only what you need
- **Cross-platform** - macOS, Linux, Windows (WSL2)

---

## Team Configuration

Add to `.claude/settings.json` for automatic installation:

```json
{
  "extraKnownMarketplaces": {
    "claudex": {
      "source": {
        "source": "github",
        "repo": "cskiro/claudex"
      }
    }
  },
  "enabledPlugins": [
    "codebase-auditor@claudex",
    "skill-creator@claudex",
    "semantic-release-tagger@claudex"
  ]
}
```

---

## Migration from v5.x

If upgrading from v5.x (grouped plugin structure):

```bash
# 1. Uninstall old plugins
/plugin uninstall claudex@claudex

# 2. Clear plugin cache
rm -rf ~/.claude/plugins/claudex*

# 3. Update marketplace and install individual plugins
/plugin marketplace update claudex
/plugin install codebase-auditor@claudex
/plugin install skill-creator@claudex
# ... install other plugins as needed
```
---

## Validation

```bash
# Validate marketplace.json schema
python3 scripts/validate-marketplace.py

# Validate all skills
python3 scripts/validate-skills.py plugins/

# Pre-release validation suite
python3 scripts/validate-pre-release.py
```

---

## License

Apache 2.0

---

**Maintained by**: Connor
**Current Version**: v6.0.0
**Last Updated**: 2026-01-24

*Skills and hooks for extending Claude Code capabilities across the software development lifecycle.*
