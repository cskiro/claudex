# Claudex - Claude Code Marketplace

> Skills and hooks for [Claude Code](https://claude.com/claude-code) - code quality analysis, testing automation, productivity tools, and DevOps workflows

## Quick Start

### Install via Marketplace

```bash
# Add the marketplace
/plugin marketplace add cskiro/claudex

# Install plugin bundles
/plugin install api-tools@claudex
/plugin install analysis-tools@claudex
/plugin install claude-code-tools@claudex
/plugin install meta-tools@claudex
/plugin install release-management@claudex
/plugin install testing-tools@claudex
/plugin install devops-tools@claudex
/plugin install planning-tools@claudex
/plugin install benchmarking@claudex

# (Optional) Install productivity hooks
/plugin install productivity-hooks@claudex
```

### Updating from v0.x

If you previously installed claudex v0.2.0 or earlier:

```bash
# Update the marketplace
/plugin marketplace update claudex

# Your installed plugins will automatically use the new structure
```

---

## Repository Structure

```
claudex/
├── skills/              # Invokable agent skills
│   ├── analysis/        # Code quality & architecture analysis
│   ├── claude-code/     # Claude Code ecosystem tools
│   ├── meta/            # Tools for creating/testing skills
│   ├── testing/         # Testing frameworks
│   ├── devops/          # Infrastructure & project automation
│   ├── planning/        # Visual planning and diagrams
│   ├── release-management/  # Versioning and releases
│   └── benchmarking/    # Academic reports and diagrams
├── hooks/               # Event-driven automation
│   └── extract-explanatory-insights/
├── commands/            # (Future) Custom slash commands
├── agents/              # (Future) Custom agent workflows
└── .claude-plugin/      # Marketplace configuration
```

---

## Available Plugins

### API Tools

**`api-tools`** - Leverage Anthropic API features like structured outputs

| Skill | Version | Description |
|-------|---------|-------------|
| **structured-outputs-advisor** | 0.2.0 | Expert advisor for choosing between JSON outputs and strict tool use modes |
| **json-outputs-implementer** | 0.2.0 | Implement JSON outputs mode with guaranteed schema compliance |
| **strict-tool-implementer** | 0.2.0 | Implement strict tool use mode with guaranteed parameter validation |

### Analysis Tools

**`analysis-tools`** - Code quality, security, and architecture analysis

| Skill | Version | Description |
|-------|---------|-------------|
| **codebase-auditor** | 0.2.0 | Comprehensive codebase analysis against 2024-25 SDLC standards (OWASP, WCAG, DORA) |
| **bulletproof-react-auditor** | 0.2.0 | React application auditor based on Bulletproof React architecture patterns |
| **accessibility-audit** | 0.1.0 | WCAG 2.2 Level AA accessibility auditing with risk-based severity scoring |

### Claude Code Tools

**`claude-code-tools`** - Enhance and extend the Claude Code ecosystem

| Skill | Version | Description |
|-------|---------|-------------|
| **cc-insights** | 0.2.0 | RAG-powered conversation analysis with semantic search and insight reports |
| **sub-agent-creator** | 0.2.0 | Generate Claude Code sub-agents following Anthropic's official patterns |
| **mcp-server-creator** | 0.2.0 | Create Model Context Protocol servers with TypeScript/Python SDKs |
| **claude-md-auditor** | 0.2.0 | Validate CLAUDE.md files against official standards and best practices |
| **otel-monitoring-setup** | 0.2.0 | Automated OpenTelemetry setup with Docker stack and Grafana dashboards |

### Meta Tools

**`meta-tools`** - Create and test Claude Code skills

| Skill | Version | Description |
|-------|---------|-------------|
| **skill-creator** | 0.2.0 | Generate skills following Claudex marketplace standards |
| **skill-isolation-tester** | 0.2.0 | Test skills in isolated environments (worktree, Docker, VMs) |
| **insight-skill-generator** | 0.1.0 | Transform Claude Code explanatory insights into production-ready skills |

### Release Management

**`release-management`** - Automated release workflows and versioning

| Skill | Version | Description |
|-------|---------|-------------|
| **semantic-release-tagger** | 0.2.0 | Automated git tagging agent with conventional commit parsing and GitHub release integration |

### Testing Tools

**`testing-tools`** - Automated testing frameworks

| Skill | Version | Description |
|-------|---------|-------------|
| **playwright-e2e-automation** | 0.3.0 | LLM-powered e2e testing with visual debugging and regression testing |
| **tdd-automation** | 0.2.0 | Automated TDD enforcement for LLM-assisted development |

### DevOps Tools

**`devops-tools`** - Infrastructure automation and project scaffolding

| Skill | Version | Description |
|-------|---------|-------------|
| **react-project-scaffolder** | 0.2.0 | React project setup (sandbox, enterprise, mobile modes) |
| **github-repo-setup** | 0.2.0 | GitHub repository creation with security, CI/CD, and governance |
| **git-worktree-setup** | 0.2.0 | Parallel Claude Code sessions via git worktrees |

### Planning Tools

**`planning-tools`** - Visual planning and documentation tools

| Skill | Version | Description |
|-------|---------|-------------|
| **ascii-diagram-creator** | 0.4.0 | Terminal-compatible ASCII diagrams for architecture, migrations, and data flows |

### Benchmarking

**`benchmarking`** - End-to-end benchmark report creation for AI/ML research

| Skill | Version | Description |
|-------|---------|-------------|
| **benchmark-report-creator** | 0.1.0 | Complete pipeline orchestrator: structure, diagrams, hi-res PNG capture, and PDF export |

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
- **Node.js** 18+ - For marketplace infrastructure
- **Python** 3.8+ - For Python-based skills
- **jq** 1.6+ - For hooks (install via `brew install jq` on macOS)

### Optional (Skill-Specific)
- **Docker Desktop** - For `otel-monitoring-setup`
- **Python packages** - Install per skill's `requirements.txt`

---

## Features

- **22 Skills** across 10 categories (api, analysis, claude-code, meta, release-management, testing, devops, planning, benchmarking)
- **1 Hook** for automated insight extraction
- **Semantic categorization** - Skills organized by purpose, not theme
- **Multi-feature support** - Skills, hooks, commands (future), agents (future)
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
    "analysis-tools@claudex",
    "claude-code-tools@claudex",
    "meta-tools@claudex",
    "testing-tools@claudex",
    "devops-tools@claudex",
    "planning-tools@claudex",
    "benchmarking@claudex",
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

**Cause:** In marketplace v1.1.3 (November 2025), `productivity-tools` was renamed to `claude-code-tools` to better reflect its purpose.

**Solution:** Update your Claude Code settings to use the new plugin name:

1. **Check user settings** (`~/.claude/settings.json`):
   ```json
   {
     "enabledPlugins": [
       "claude-code-tools@claudex"  // ← was "productivity-tools@claudex"
     ]
   }
   ```

2. **Check project settings** (`.claude/settings.json` in your project):
   ```json
   {
     "enabledPlugins": [
       "claude-code-tools@claudex"  // ← was "productivity-tools@claudex"
     ]
   }
   ```

3. **Update the marketplace** to ensure you have the latest plugin structure:
   ```bash
   /plugin marketplace update claudex
   ```

---

## License

Apache 2.0

---

**Maintained by**: Connor
**Current Version**: v2.0.0
**Last Updated**: 2025-12-05

*Skills and hooks for extending Claude Code capabilities across the software development lifecycle.*
