# Changelog

## 0.2.1

- Relocated to `plugins/claude-code-tools/skills/` for source isolation (marketplace v4.0.0)
- Prevents cache duplication in Claude Code plugin system

## 0.2.0

- Refactored to Anthropic progressive disclosure pattern
- Updated description with "Use PROACTIVELY when..." format
- Removed version/author from frontmatter (CHANGELOG is source of truth)

## 0.1.0

- Initial release with 5-phase sub-agent creation workflow
- Security-first tool configuration with minimal access defaults
- Model selection guidance (inherit, sonnet, opus, haiku)
- Reference materials: models, tools, templates
- Example sub-agents: code-reviewer, debugger, data-scientist
