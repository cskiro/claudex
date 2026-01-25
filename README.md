# Claudex - Claude Code Marketplace

> Skills and hooks for [Claude Code](https://claude.com/claude-code) - code quality analysis, testing automation, productivity tools, and DevOps workflows

## Quick Start

### Install via Marketplace

```bash
# Add the marketplace
/plugin marketplace add cskiro/claudex

# Install all skills and hooks
/plugin install claudex@claudex
```

That's it! All 23 skills and hooks are now available.

---

## Repository Structure

Follows Anthropic's official `anthropics/skills` pattern:

```
claudex/
├── .claude-plugin/
│   └── marketplace.json        # Plugin registry (single source of truth)
├── skills/                     # Flat skill directory (23 skills)
│   ├── accessibility-audit/
│   ├── ascii-diagram-creator/
│   ├── benchmark-report-creator/
│   ├── bulletproof-react-auditor/
│   ├── cc-insights/
│   ├── claude-md-auditor/
│   ├── codebase-auditor/
│   ├── ...
├── hooks/                      # Event-driven automation
│   └── hooks.json
└── docs/                       # Documentation
```

---

## Available Skills

All skills use the `claudex:skill-name` namespace.

### API & Structured Outputs

| Skill | Version | Description |
|-------|---------|-------------|
| **structured-outputs-advisor** | 0.2.1 | Expert advisor for choosing between JSON outputs and strict tool use modes |
| **json-outputs-implementer** | 0.2.1 | Implement JSON outputs mode with guaranteed schema compliance |
| **strict-tool-implementer** | 0.2.1 | Implement strict tool use mode with guaranteed parameter validation |

### Code Analysis

| Skill | Version | Description |
|-------|---------|-------------|
| **codebase-auditor** | 0.3.1 | Comprehensive codebase analysis against 2024-25 SDLC standards |
| **bulletproof-react-auditor** | 0.2.1 | React codebase auditing against Bulletproof React architecture |
| **accessibility-audit** | 0.1.2 | WCAG 2.2 Level AA compliance auditing with MUI awareness |

### Claude Code Ecosystem

| Skill | Version | Description |
|-------|---------|-------------|
| **cc-insights** | 0.2.1 | RAG-powered conversation analysis with semantic search and insight reports |
| **sub-agent-creator** | 0.2.1 | Generate Claude Code sub-agents following Anthropic's official patterns |
| **mcp-server-creator** | 0.2.1 | Create Model Context Protocol servers with TypeScript/Python SDKs |
| **claude-md-auditor** | 0.2.1 | Validate CLAUDE.md files against official standards and best practices |
| **otel-monitoring-setup** | 0.2.1 | Automated OpenTelemetry setup with Docker stack and Grafana dashboards |

### Skill Development

| Skill | Version | Description |
|-------|---------|-------------|
| **skill-creator** | 0.2.1 | Generate skills following Claudex marketplace standards |
| **skill-isolation-tester** | 0.2.1 | Test skills in isolated environments (worktree, Docker, VMs) |
| **insight-skill-generator** | 0.1.1 | Generate skills from clustered insight patterns |

### Testing

| Skill | Version | Description |
|-------|---------|-------------|
| **e2e-testing** | 0.4.1 | LLM-powered e2e testing with visual debugging and regression testing |
| **test-driven-development** | 0.3.1 | Automated TDD enforcement for LLM-assisted development |
| **mutation-testing** | 0.1.1 | Test suite quality assessment via mutation analysis (Stryker, mutmut) |

### DevOps & Infrastructure

| Skill | Version | Description |
|-------|---------|-------------|
| **react-project-scaffolder** | 0.2.1 | React project setup (sandbox, enterprise, mobile modes) |
| **github-repo-setup** | 0.2.1 | GitHub repository creation with security, CI/CD, and governance |
| **git-worktree-setup** | 0.2.1 | Parallel Claude Code sessions via git worktrees |

### Release & Documentation

| Skill | Version | Description |
|-------|---------|-------------|
| **semantic-release-tagger** | 0.2.1 | Automated git tagging with conventional commit analysis |
| **ascii-diagram-creator** | 0.4.1 | ASCII diagram generation for architecture and data flows |
| **benchmark-report-creator** | 0.1.2 | Academic benchmark reports with diagrams and PDF export |

### Hooks

| Hook | Version | Description |
|------|---------|-------------|
| **extract-explanatory-insights** | 0.1.0 | Auto-extracts `★ Insight` blocks from Explanatory responses |

---

## Prerequisites

- **Claude Code** - Latest version ([Download](https://claude.com/claude-code))
- **Git** - For marketplace integration
- **Python** 3.8+ - For validation scripts and Python-based skills
- **jq** 1.6+ - For hooks (install via `brew install jq` on macOS)

---

## Features

- **23 Skills** in a single unified plugin
- **1 Hook** for automated insight extraction
- **Anthropic-aligned structure** - Follows official `anthropics/skills` patterns
- **No duplication** - Single namespace prevents skill cloning issues
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
    "claudex@claudex"
  ]
}
```

---

## Migration from v5.x

If upgrading from v5.x (multi-plugin structure):

```bash
# 1. Uninstall old plugins
/plugin uninstall api-tools@claudex
/plugin uninstall analysis-tools@claudex
/plugin uninstall claude-code-tools@claudex
/plugin uninstall meta-tools@claudex
/plugin uninstall testing-tools@claudex
/plugin uninstall devops-tools@claudex
/plugin uninstall release-management@claudex
/plugin uninstall planning-tools@claudex
/plugin uninstall benchmarking@claudex
/plugin uninstall productivity-hooks@claudex

# 2. Clear plugin cache
rm -rf ~/.claude/plugins/claudex*

# 3. Update marketplace and install
/plugin marketplace update claudex
/plugin install claudex@claudex
```

See [docs/MIGRATION.md](docs/MIGRATION.md) for full migration guide.

---

## Validation

```bash
# Validate marketplace.json schema
python3 scripts/validate-marketplace.py

# Validate all skills
python3 scripts/validate-skills.py skills/

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
