---
name: sub-agent-creator
description: Use PROACTIVELY when creating specialized Claude Code sub-agents for task delegation. Automates agent creation following Anthropic's official patterns with proper frontmatter, tool configuration, and system prompts. Generates domain-specific agents, proactive auto-triggering agents, and security-sensitive agents with limited tools. Not for modifying existing agents or general prompt engineering.
---

# Sub-Agent Creator

Automates creation of Claude Code sub-agents with proper configuration and proactive behavior.

## When to Use

**Trigger Phrases**:
- "create a sub-agent for [purpose]"
- "generate a new sub-agent"
- "set up a sub-agent to handle [task]"
- "make a proactive agent that [behavior]"

**Use Cases**:
- Domain-specific agents (code reviewer, debugger)
- Proactive agents that auto-trigger on patterns
- Security-sensitive agents with limited tools
- Team-shared project-level agents

## Workflow

### Phase 1: Information Gathering
1. **Purpose**: What task/domain should agent specialize in?
2. **Name**: Auto-generate kebab-case from purpose
3. **Description**: Template: "Use PROACTIVELY to [action] when [condition]"
4. **Location**: Project (.claude/agents/) or User (~/.claude/agents/)

### Phase 2: Technical Configuration
1. **Model**: inherit (default), sonnet, opus, haiku
2. **Tools**: Read-only, Code ops, Execution, All, Custom
3. **System Prompt**: Role, approach, priorities, constraints

### Phase 3: File Generation
- Build YAML frontmatter
- Structure system prompt with templates
- Write to correct location

### Phase 4: Validation & Testing
- Validate YAML, tools, model
- Generate testing guidance
- List customization points

## Frontmatter Structure

```yaml
---
name: agent-name
description: Use PROACTIVELY to [action] when [condition]
tools: Read, Grep, Glob  # Omit for all tools
model: sonnet             # Omit to inherit
---
```

## Model Options

| Model | Use Case |
|-------|----------|
| inherit | Same as main conversation (default) |
| sonnet | Balanced performance |
| opus | Maximum capability |
| haiku | Fast/economical |

## Tool Access Patterns

| Pattern | Tools | Use Case |
|---------|-------|----------|
| Read-only | Read, Grep, Glob | Safe analysis |
| Code ops | Read, Edit, Write | Modifications |
| Execution | Bash | Running commands |
| All | * | Full access (cautious) |

## Installation Locations

| Location | Path | Use Case |
|----------|------|----------|
| Project | .claude/agents/ | Team-shared, versioned |
| User | ~/.claude/agents/ | Personal, all projects |

## Success Criteria

- [ ] Valid YAML frontmatter
- [ ] Agent file in correct location
- [ ] Description includes "PROACTIVELY"
- [ ] System prompt has role, approach, constraints
- [ ] Appropriate tool restrictions
- [ ] Clear testing instructions

## Security Best Practices

- Default to minimal tool access
- Require confirmation for "all tools"
- Validate tool list against available tools
- Warn about overly broad permissions

## Reference Materials

- `data/models.yaml` - Model options
- `data/tools.yaml` - Available tools
- `templates/agent-template.md` - Prompt structure
- `examples/` - Sample agents (code-reviewer, debugger)

## Testing Your Agent

### Manual Invocation
```
Use the [agent-name] sub-agent to [task]
```

### Proactive Trigger
Perform action matching the description to test auto-delegation.

### Debugging
```bash
# Check file
cat .claude/agents/[agent-name].md | head -10

# Verify location
ls .claude/agents/
```

---

**Version**: 0.1.0 | **Author**: Connor

**Docs**: https://docs.claude.com/en/docs/claude-code/sub-agents
