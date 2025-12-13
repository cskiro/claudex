# Sub-Agent Creator

Automates creation of Claude Code sub-agents following Anthropic's official patterns, with proper frontmatter, tool configuration, and system prompts.

## Overview

This skill guides users through creating production-ready sub-agents for Claude Code. It handles:
- YAML frontmatter generation with required fields (`name`, `description`)
- Tool permission configuration (security-focused minimal access)
- Model selection (inherit, sonnet, opus, haiku)
- System prompt structuring with role, approach, and constraints
- Validation and testing guidance

## When to Use

Use this skill when you need to:
- Create specialized sub-agents for specific tasks (code review, debugging, data analysis)
- Set up proactive agents that auto-trigger on task patterns
- Configure secure tool permissions for agents
- Build team-shared project-level agents (`.claude/agents/`)
- Create personal user-level agents (`~/.claude/agents/`)

## Trigger Phrases

- "create a sub-agent for [purpose]"
- "generate a new sub-agent"
- "set up a sub-agent to handle [task]"
- "build a specialized agent for [domain]"
- "help me create a sub-agent"
- "make a proactive agent that [behavior]"

## Features

### Interactive Workflow
Guides you through 5 phases:
1. **Information Gathering** - Purpose, name, description, location
2. **Technical Configuration** - Model, tools, system prompt components
3. **File Generation** - Create properly formatted sub-agent file
4. **Validation & Testing** - Verify configuration and provide test instructions
5. **Next Steps** - Guidance on refinement and best practices

### Security-First Tool Configuration
- Defaults to minimal tool access
- Warns about overly broad permissions
- Recommends read-only tools for analysis agents
- Requires explicit confirmation for "all tools" access

### Official Pattern Compliance
- Follows Anthropic's sub-agent specification exactly
- Proper YAML frontmatter with required fields
- Correct storage locations (project vs. user level)
- Proactive description patterns for auto-delegation

### Reference Materials
Includes examples of production-ready sub-agents:
- **code-reviewer** - Code quality, security, maintainability analysis
- **debugger** - Root cause analysis and error resolution
- **data-scientist** - SQL queries, statistical analysis, data visualization

## Prerequisites

None - this skill works in any project or environment. Sub-agents are created as standalone markdown files.

## Installation

This skill is available in the **claudex** marketplace.

### Local Installation (for development)
```bash
# Copy to local skills directory
cp -r sub-agent-creator ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/sub-agent-creator/SKILL.md
```

### Marketplace Installation
```json
// .claude/settings.json
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
    "sub-agent-creator@claudex"
  ]
}
```

## Usage Examples

### Example 1: Create a Code Reviewer

**User:** "Create a sub-agent for code review"

**Skill guides you through:**
1. Name suggestion: `code-reviewer`
2. Description: "Use PROACTIVELY to review code quality after significant changes"
3. Location: Project-level (`.claude/agents/`) for team sharing
4. Model: `inherit` (consistent with main session)
5. Tools: `Read, Grep, Glob, Bash` (read + search + execution)
6. System prompt: Focus on security, maintainability, best practices

**Result:** `.claude/agents/code-reviewer.md` ready to use

---

### Example 2: Create a Data Analysis Agent

**User:** "Set up a sub-agent to handle SQL queries"

**Skill guides you through:**
1. Name: `data-scientist`
2. Description: "Use PROACTIVELY when data analysis or SQL queries are requested"
3. Location: User-level (`~/.claude/agents/`) for personal use across projects
4. Model: `sonnet` (balanced performance for data tasks)
5. Tools: `Read, Write, Bash, Grep, Glob` (data access + output generation)
6. System prompt: SQL expertise, statistical analysis, visualization recommendations

**Result:** `~/.claude/agents/data-scientist.md` ready to use

---

### Example 3: Create a Debugging Specialist

**User:** "Build a specialized agent for debugging test failures"

**Skill guides you through:**
1. Name: `debugger`
2. Description: "Use PROACTIVELY when tests fail or errors occur"
3. Location: Project-level for team consistency
4. Model: `inherit`
5. Tools: `Read, Edit, Bash, Grep, Glob` (investigate + fix)
6. System prompt: Root cause analysis, hypothesis testing, minimal fixes

**Result:** `.claude/agents/debugger.md` ready to use

## File Structure

```
sub-agent-creator/
├── SKILL.md              # Main skill manifest
├── README.md             # This file
├── CHANGELOG.md          # Version history
├── data/
│   ├── models.yaml       # Available model options with guidance
│   └── tools.yaml        # Available tools with security notes
├── templates/
│   └── agent-template.md # System prompt structure template
└── examples/
    ├── code-reviewer.md  # Example: Code review sub-agent
    ├── debugger.md       # Example: Debugging sub-agent
    └── data-scientist.md # Example: Data analysis sub-agent
```

## Configuration

No configuration required - skill works out of the box.

## Best Practices

1. **Start with Minimal Tools** - Grant only necessary capabilities, expand as needed
2. **Use "PROACTIVELY" in Descriptions** - Enables automatic delegation
3. **Be Specific in System Prompts** - Include concrete examples and edge cases
4. **Test Before Deploy** - Verify agent loads and behaves correctly
5. **Iterate Based on Usage** - Refine after observing real-world behavior
6. **Document for Teams** - Project-level agents need clear usage guidance

## Validation

The skill performs these validation checks:
- ✅ YAML frontmatter is valid
- ✅ Required fields present (`name`, `description`)
- ✅ Tools list is valid (if specified)
- ✅ Model value is valid (if specified)
- ✅ No security issues (exposed secrets, overly broad permissions)
- ✅ Description is specific enough for auto-delegation

## Troubleshooting

### Agent doesn't load
```bash
# Check YAML syntax
cat ~/.claude/agents/agent-name.md | head -10

# Verify frontmatter
# Should show:
---
name: agent-name
description: ...
---
```

### Agent has incorrect tools
Edit the agent file and update the `tools:` field:
```yaml
---
name: my-agent
description: ...
tools: Read, Grep, Glob  # Add/remove tools here
---
```

### Agent triggers too aggressively
Refine the `description` field to be more specific:
```yaml
# Too broad
description: Use for code analysis

# Better
description: Use PROACTIVELY to analyze code quality when reviewing pull requests
```

## Official Resources

- **Anthropic Sub-Agent Docs:** https://docs.claude.com/en/docs/claude-code/sub-agents
- **Claude Code Documentation:** https://docs.claude.com
- **Claudex Marketplace:** https://github.com/cskiro/claudex

## Contributing

Found a bug or have a feature request? Open an issue in the [claudex repository](https://github.com/cskiro/claudex/issues).

## License

MIT License - see [LICENSE](https://github.com/cskiro/claudex/blob/main/LICENSE) for details.

## Version

**Current Version:** 0.1.0

See [CHANGELOG.md](./CHANGELOG.md) for version history and updates.

---

**Maintained by:** Connor
**Status:** Proof of Concept
**Last Updated:** 2025-11-02
