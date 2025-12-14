# Claudex - Claude Code Marketplace

> Skills and hooks for [Claude Code](https://claude.com/claude-code) - code quality analysis, testing automation, productivity tools, and DevOps workflows

## Quick Start

### Install via Marketplace

```bash
# Add the marketplace
/plugin marketplace add cskiro/claudex

# Install plugin bundles
/plugin install api-tools@claudex
/plugin install claude-code-tools@claudex
/plugin install meta-tools@claudex
/plugin install testing-tools@claudex
/plugin install devops-tools@claudex

# (Optional) Install productivity hooks
/plugin install productivity-hooks@claudex
```

### Updating from v3.x

If you previously installed claudex v3.x or earlier:

```bash
# Update the marketplace
/plugin marketplace update claudex

# Note: Some plugins were archived in v4.0.0
# - analysis-tools (use analysis-tools from main marketplace)
# - release-management (archived)
# - planning-tools (archived)
# - benchmarking (archived)
```

---

## Repository Structure

```
claudex/
├── plugins/                    # Plugin bundles with isolated sources
│   ├── api-tools/skills/       # Anthropic API features
│   ├── claude-code-tools/skills/   # Claude Code ecosystem
│   ├── meta-tools/skills/      # Skill creation tools
│   ├── testing-tools/skills/   # Testing frameworks
│   └── devops-tools/skills/    # Infrastructure automation
├── hooks/                      # Event-driven automation
│   └── hooks.json              # Hook registry
├── archive/                    # Archived skills (not in marketplace)
└── .claude-plugin/             # Marketplace configuration
    └── marketplace.json        # Single source of truth
```

---

## Available Plugins

### API Tools

**`api-tools`** - Leverage Anthropic API features like structured outputs

| Skill | Version | Description |
|-------|---------|-------------|
| **structured-outputs-advisor** | 0.2.1 | Expert advisor for choosing between JSON outputs and strict tool use modes |
| **json-outputs-implementer** | 0.2.1 | Implement JSON outputs mode with guaranteed schema compliance |
| **strict-tool-implementer** | 0.2.1 | Implement strict tool use mode with guaranteed parameter validation |

### Claude Code Tools

**`claude-code-tools`** - Enhance and extend the Claude Code ecosystem

| Skill | Version | Description |
|-------|---------|-------------|
| **cc-insights** | 0.2.1 | RAG-powered conversation analysis with semantic search and insight reports |
| **sub-agent-creator** | 0.2.1 | Generate Claude Code sub-agents following Anthropic's official patterns |
| **mcp-server-creator** | 0.2.1 | Create Model Context Protocol servers with TypeScript/Python SDKs |
| **claude-md-auditor** | 0.2.1 | Validate CLAUDE.md files against official standards and best practices |
| **otel-monitoring-setup** | 0.2.1 | Automated OpenTelemetry setup with Docker stack and Grafana dashboards |

### Meta Tools

**`meta-tools`** - Create and test Claude Code skills

| Skill | Version | Description |
|-------|---------|-------------|
| **skill-creator** | 0.2.1 | Generate skills following Claudex marketplace standards |
| **skill-isolation-tester** | 0.2.1 | Test skills in isolated environments (worktree, Docker, VMs) |

### Testing Tools

**`testing-tools`** - Automated testing frameworks

| Skill | Version | Description |
|-------|---------|-------------|
| **e2e-testing** | 0.4.1 | LLM-powered e2e testing with visual debugging and regression testing |
| **test-driven-development** | 0.3.1 | Automated TDD enforcement for LLM-assisted development |
| **mutation-testing** | 0.1.1 | Test suite quality assessment via mutation analysis (Stryker, mutmut) |

### DevOps Tools

**`devops-tools`** - Infrastructure automation and project scaffolding

| Skill | Version | Description |
|-------|---------|-------------|
| **react-project-scaffolder** | 0.2.1 | React project setup (sandbox, enterprise, mobile modes) |
| **github-repo-setup** | 0.2.1 | GitHub repository creation with security, CI/CD, and governance |
| **git-worktree-setup** | 0.2.1 | Parallel Claude Code sessions via git worktrees |

### Productivity Hooks

**`productivity-hooks`** - Automated insight extraction and learning

| Hook | Version | Description |
|------|---------|-------------|
| **extract-explanatory-insights** | 0.1.0 | Auto-extracts `★ Insight` blocks from Explanatory responses to categorized docs |

**Usage:**
1. Install: `/plugin install productivity-hooks@claudex`
2. Enable Explanatory style: `/output-style explanatory`
3. Insights auto-save to `docs/lessons-learned/{category}/insights.md`

---

## Prerequisites

- **Claude Code** - Latest version ([Download](https://claude.com/claude-code))
- **Git** - For marketplace integration
- **Python** 3.8+ - For validation scripts and Python-based skills
- **jq** 1.6+ - For hooks (install via `brew install jq` on macOS)

### Optional (Skill-Specific)
- **Docker Desktop** - For `otel-monitoring-setup`
- **Python packages** - Install per skill's `requirements.txt`

---

## Features

- **16 Skills** across 5 plugin categories
- **1 Hook** for automated insight extraction
- **Source isolation** - Each plugin has isolated source paths to prevent cache duplication
- **Semantic categorization** - Skills organized by purpose
- **Cross-platform** - macOS, Linux, Windows (WSL2)
- **Marketplace ready** - Standard directory structure following Anthropic patterns

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
    "api-tools@claudex",
    "claude-code-tools@claudex",
    "meta-tools@claudex",
    "testing-tools@claudex",
    "devops-tools@claudex",
    "productivity-hooks@claudex"
  ]
}
```

When team members trust your repository, plugins install automatically.

---

## Troubleshooting

### Plugin Not Found: productivity-tools

**Error:**
```
✘ productivity-tools@claudex
   Plugin 'productivity-tools' not found in marketplace 'claudex'
```

**Cause:** In marketplace v1.1.3 (November 2025), `productivity-tools` was renamed to `claude-code-tools`.

**Solution:** Update your settings to use `claude-code-tools@claudex`.

### Plugin Not Found: analysis-tools, planning-tools, etc.

**Error:**
```
✘ analysis-tools@claudex
   Plugin 'analysis-tools' not found in marketplace 'claudex'
```

**Cause:** In marketplace v4.0.0 (December 2025), several plugins were archived to reduce duplication with the main Anthropic marketplace.

**Archived plugins:**
- `analysis-tools` - Use analysis skills from the main marketplace
- `release-management` - Archived
- `planning-tools` - Archived
- `benchmarking` - Archived

**Solution:** Remove these plugins from your settings and use alternatives from the main marketplace.

---

## Validation

Validate marketplace integrity before committing:

```bash
# Validate marketplace.json schema
python3 scripts/validate-marketplace.py

# Validate all skills
python3 scripts/validate-skills.py plugins/
```

---

## License

Apache 2.0

---

**Maintained by**: Connor
**Current Version**: v4.0.0
**Last Updated**: 2025-12-13

*Skills and hooks for extending Claude Code capabilities across the software development lifecycle.*
