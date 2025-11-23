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
│   └── devops/          # Infrastructure & project automation
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

| Skill | Description |
|-------|-------------|
| **structured-outputs-advisor** | Expert advisor for choosing between JSON outputs and strict tool use modes |
| **json-outputs-implementer** | Implement JSON outputs mode with guaranteed schema compliance |
| **strict-tool-implementer** | Implement strict tool use mode with guaranteed parameter validation |

### Analysis Tools

**`analysis-tools`** - Code quality, security, and architecture analysis

| Skill | Description |
|-------|-------------|
| **codebase-auditor** | Comprehensive codebase analysis against 2024-25 SDLC standards (OWASP, WCAG, DORA) |
| **bulletproof-react-auditor** | React application auditor based on Bulletproof React architecture patterns |

### Claude Code Tools

**`claude-code-tools`** - Enhance and extend the Claude Code ecosystem

| Skill | Description |
|-------|-------------|
| **cc-insights** | RAG-powered conversation analysis with semantic search and insight reports |
| **sub-agent-creator** | Generate Claude Code sub-agents following Anthropic's official patterns |
| **mcp-server-creator** | Create Model Context Protocol servers with TypeScript/Python SDKs |
| **claude-md-auditor** | Validate CLAUDE.md files against official standards and best practices |
| **otel-monitoring-setup** | Automated OpenTelemetry setup with Docker stack and Grafana dashboards |

### Meta Tools

**`meta-tools`** - Create and test Claude Code skills

| Skill | Description |
|-------|-------------|
| **skill-creator** | Generate skills following Claudex marketplace standards |
| **skill-isolation-tester** | Test skills in isolated environments (worktree, Docker, VMs) |

### Release Management

**`release-management`** - Automated release workflows and versioning

| Skill | Description |
|-------|-------------|
| **semantic-release-tagger** | Automated git tagging agent with conventional commit parsing and GitHub release integration |

### Testing Tools

**`testing-tools`** - Automated testing frameworks

| Skill | Description |
|-------|-------------|
| **playwright-e2e-automation** | LLM-powered e2e testing with visual debugging and regression testing |
| **tdd-automation** | Automated TDD enforcement for LLM-assisted development |

### DevOps Tools

**`devops-tools`** - Infrastructure automation and project scaffolding

| Skill | Description |
|-------|-------------|
| **react-project-scaffolder** | React project setup (sandbox, enterprise, mobile modes) |
| **github-repo-setup** | GitHub repository creation with security, CI/CD, and governance |
| **git-worktree-setup** | Parallel Claude Code sessions via git worktrees |

### Productivity Hooks

**`productivity-hooks`** - Automated insight extraction and learning

| Hook | Description |
|------|-------------|
| **extract-explanatory-insights** | Auto-extracts `★ Insight` blocks from Explanatory responses to categorized docs |

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

- **18 Skills** across 7 categories (api, analysis, claude-code, meta, release-management, testing, devops)
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
    "productivity-hooks@claudex"
  ]
}
```

When team members trust your repository, plugins install automatically.

---

## License

Apache 2.0

---

**Maintained by**: Connor
**Current Version**: v1.3.0
**Last Updated**: 2025-11-23

*Skills and hooks for extending Claude Code capabilities across the software development lifecycle.*
