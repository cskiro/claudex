# Insight-to-Skill Generator

Transform your accumulated Claude Code explanatory insights into production-ready, reusable skills.

## Overview

The Insight-to-Skill Generator analyzes insights collected by the `extract-explanatory-insights` hook and converts them into well-structured Claude Code skills. It uses smart clustering to group related insights, guides you through interactive skill design, and generates complete skills following Anthropic's standards.

**Perfect for**:
- Reusing knowledge from previous Claude Code sessions
- Creating team-wide skills from project-specific learnings
- Building a library of domain-specific productivity tools
- Codifying best practices discovered through experience

## When to Use

Use this skill when you have insights stored in your project's `docs/lessons-learned/` directory and want to turn them into reusable skills.

**Trigger Phrases**:
- "create skill from insights"
- "generate skill from lessons learned"
- "turn my insights into a skill"
- "convert docs/lessons-learned to skill"

## Quick Start

### Prerequisites

1. Your project has the `extract-explanatory-insights` hook configured
2. You have insights stored in `docs/lessons-learned/` directory
3. You're using Claude Code with Explanatory output style

### Basic Usage

```
You: "I have a bunch of insights about testing in docs/lessons-learned/. Can you create a skill from them?"

Claude: [Activates insight-skill-generator]
- Scans your docs/lessons-learned/ directory
- Clusters related testing insights
- Proposes a "testing-best-practices" skill
- Guides you through customization
- Generates and installs the skill
```

### Example Workflow

1. **Discovery**: The skill finds 12 insights across 4 categories
2. **Clustering**: Groups them into 3 skill candidates:
   - "testing-strategy-guide" (5 insights)
   - "hook-debugging-helper" (4 insights)
   - "performance-optimization" (3 insights)
3. **Design**: You review and customize each skill proposal
4. **Generation**: Complete skills are created with SKILL.md, README, examples, etc.
5. **Installation**: You choose to install "testing-strategy-guide" globally, others project-specific

## Installation

### Standard Installation

```bash
# Clone or copy this skill to your Claude Code skills directory
cp -r insight-skill-generator ~/.claude/skills/

# The skill is now available in all your Claude Code sessions
```

### Project-Specific Installation

```bash
# Copy to project's .claude directory
cp -r insight-skill-generator /path/to/project/.claude/skills/
```

## What Gets Generated

For each skill created, you'll get:

**Minimal Skill** (1 simple insight):
- `SKILL.md` - Main skill instructions
- `README.md` - User documentation
- `plugin.json` - Marketplace metadata
- `CHANGELOG.md` - Version history

**Standard Skill** (2-4 insights):
- All of the above, plus:
- `data/insights-reference.md` - Original insights for reference
- `examples/usage-examples.md` - How to use the skill

**Complex Skill** (5+ insights):
- All of the above, plus:
- `examples/code-samples.md` - Code examples extracted from insights
- `templates/checklist.md` - Actionable checklist

## Features

### Smart Clustering
- Analyzes keywords, categories, and temporal proximity
- Groups related insights automatically
- Identifies standalone high-value insights
- Suggests optimal skill patterns (phase-based, mode-based, validation)

### Interactive Design
- Proposes skill names and descriptions
- Lets you customize every aspect
- Shows pattern trade-offs with examples
- Previews structure before generation

### Quality Assurance
- Validates YAML frontmatter syntax
- Checks against Anthropic's skill standards
- Ensures proper file structure
- Verifies all references are valid

### Flexible Installation
- Choose project-specific or global installation
- Detects naming conflicts
- Tests skill loading after installation
- Provides testing guidance

## Configuration

### Tuning Clustering

Edit `~/.claude/skills/insight-skill-generator/data/clustering-config.yaml`:

```yaml
thresholds:
  cluster_minimum: 0.6      # Lower = more aggressive clustering
  standalone_quality: 0.8   # Higher = fewer standalone skills
```

### Category Patterns

Customize skill patterns for your domain in `data/skill-templates-map.yaml`:

```yaml
category_patterns:
  testing:
    preferred_pattern: validation
    skill_name_suffix: "testing-guide"
```

## Examples

See [examples/example-clustering-output.md](examples/example-clustering-output.md) for sample cluster analysis.

See [examples/example-generated-skill/](examples/example-generated-skill/) for a complete generated skill.

## Tips

- **Filter quality**: Not every insight should become a skill. Focus on actionable, reusable knowledge
- **Start minimal**: It's easier to expand a skill later than to simplify a complex one
- **Test thoroughly**: Use all trigger phrases to ensure the skill works as expected
- **Version control**: Commit generated skills to git for team sharing
- **Iterate**: Skills can evolve. Version 0.1.0 is just the start

## Troubleshooting

### No insights found
- Verify `docs/lessons-learned/` exists in your project
- Check that the extract-explanatory-insights hook is configured
- Ensure insight files match the naming pattern: `YYYY-MM-DD-*.md`

### Clustering produces weird results
- Adjust thresholds in `data/clustering-config.yaml`
- Manually split or combine clusters in Phase 2
- Try increasing similarity threshold for tighter clusters

### Generated skill doesn't load
- Check YAML frontmatter syntax (no tabs, proper format)
- Verify skill name is lowercase kebab-case
- Restart Claude Code session
- Check file permissions

## Learn More

For detailed workflow documentation, see [SKILL.md](SKILL.md).

## License

Created by Connor for use with Claude Code. Part of the Claude Code skills ecosystem.

## Contributing

Have ideas for improving insight-to-skill generation? Open an issue or submit suggestions through your project's Claude Code configuration.

---

**Version**: 0.1.0
**Category**: Productivity
**Integration**: extract-explanatory-insights hook
