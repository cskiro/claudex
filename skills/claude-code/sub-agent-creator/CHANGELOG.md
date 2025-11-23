# Changelog

All notable changes to the sub-agent-creator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-02

### Added
- Initial release of sub-agent-creator skill
- Interactive 5-phase workflow for sub-agent creation
- Security-first tool configuration with minimal access defaults
- Model selection guidance (inherit, sonnet, opus, haiku)
- System prompt structuring with role, approach, and constraints
- YAML frontmatter validation
- Installation location selection (project-level vs. user-level)
- Proactive description pattern recommendations
- Reference materials:
  - `data/models.yaml` - Model options with decision matrix
  - `data/tools.yaml` - Tool catalog with security guidelines
  - `templates/agent-template.md` - System prompt template
- Example sub-agents:
  - `examples/code-reviewer.md` - Code quality analysis agent
  - `examples/debugger.md` - Error diagnosis and resolution agent
  - `examples/data-scientist.md` - SQL and data analysis agent
- Validation checks for security, syntax, and configuration
- Testing guidance with manual and proactive trigger instructions
- Comprehensive error handling for common failure scenarios
- Best practices documentation aligned with Anthropic official specs

### Features
- Validates against Anthropic's official sub-agent specification
- Generates proper YAML frontmatter with required fields (`name`, `description`)
- Configures optional fields (`tools`, `model`) with intelligent defaults
- Security warnings for overly broad tool access
- Category-based tool selection (read-only, code operations, full development)
- Automatic name generation from purpose using kebab-case
- Description optimization for proactive delegation behavior
- Complete system prompt structure with examples and constraints

### Documentation
- README.md with usage examples and troubleshooting
- Inline documentation in SKILL.md explaining workflow phases
- Reference materials for models, tools, and templates
- Three production-ready example sub-agents

### Validation
- ✅ Follows Anthropic official sub-agent patterns
- ✅ YAML frontmatter syntax validation
- ✅ Tool permission security checks
- ✅ Model value validation
- ✅ Description clarity assessment

### Testing
- Manual testing in multiple scenarios (code review, debugging, data analysis)
- Validation report generation with actionable feedback
- Testing guidance for both manual invocation and proactive triggers

## [Unreleased]

### Planned Features
- Batch sub-agent creation from templates
- Sub-agent composition patterns (agent chains)
- Integration with MCP server tools
- Advanced system prompt templates for specialized domains
- Performance optimization recommendations based on model selection
- Team rollout guidance for project-level agents

### Planned Improvements
- Interactive tool permission adjustment during testing
- Model performance comparison for different agent types
- System prompt library for common agent patterns
- Automated migration of sub-agents between project/user levels

---

**Note:** This skill follows Anthropic's official sub-agent specification as documented at https://docs.claude.com/en/docs/claude-code/sub-agents
