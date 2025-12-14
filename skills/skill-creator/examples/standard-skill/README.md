# Standard Skill Structure Example

This example shows the standard structure used by most skills in the marketplace.

## Directory Structure

```
standard-skill/
├── SKILL.md           # Agent manifest (required)
├── README.md          # User documentation (required)
├── plugin.json        # Marketplace metadata (required)
├── CHANGELOG.md       # Version history (required)
├── data/              # Reference materials, standards (optional)
│   ├── best-practices.md
│   ├── standards.yaml
│   └── references.md
├── examples/          # Sample outputs (optional)
│   ├── example-1.md
│   └── example-2.md
└── templates/         # Reusable templates (optional)
    ├── report-template.md
    └── output-template.json
```

## When to Use Standard Structure

Use this structure when:
- Sequential workflow with clear phases
- Needs reference materials or standards
- Provides templates for outputs
- Examples help users understand
- Medium complexity

## Examples of Standard Skills

- **Codebase Auditor**: Analyzes code against standards
- **CLAUDE.md Auditor**: Validates configuration files
- **Documentation Generator**: Creates docs from code

## Characteristics

- **Complexity**: Medium
- **Files**: 4 required + 3 optional directories
- **Pattern**: Phase-based or validation
- **Modes**: Usually single mode, sequential phases
- **Scripts**: Rarely needed (pure LLM skill)
- **Dependencies**: Minimal

## SKILL.md Template

```markdown
---
name: skill-name
version: 0.1.0
description: Brief description of what this skill does
author: Your Name
---

# Skill Name

## Overview

Detailed description of capabilities.

## When to Use This Skill

**Trigger Phrases:**
- "phrase 1"
- "phrase 2"
- "phrase 3"

**Use Cases:**
- Use case 1
- Use case 2
- Use case 3

## Workflow

### Phase 1: Discovery
- Identify scope
- Gather context
- Validate prerequisites

### Phase 2: Analysis
- Apply standards from data/
- Check compliance
- Detect issues

### Phase 3: Reporting
- Generate report using templates/
- Provide examples from examples/
- Offer recommendations

### Phase 4: Remediation
- Guide user through fixes
- Verify improvements
- Update documentation

## Success Criteria

- [ ] All phases completed
- [ ] Report generated
- [ ] Recommendations provided

## Reference Materials

- `data/` - Standards and best practices
- `examples/` - Sample outputs
- `templates/` - Reusable templates
```

## Directory Purposes

### data/
Contains reference materials the skill consults:
- Standards documents (YAML, MD)
- Best practices guides
- Lookup tables
- Configuration defaults

### examples/
Shows users what to expect:
- Sample outputs
- Before/after comparisons
- Success stories
- Common scenarios

### templates/
Reusable output formats:
- Report templates (Jinja2 or Markdown)
- JSON schemas
- Configuration files
- Document structures

## Best Practices

1. **Organized references**: Put all standards in data/
2. **Concrete examples**: Show real usage in examples/
3. **Reusable templates**: DRY principle for outputs
4. **Progressive disclosure**: Start simple, add detail as needed
5. **Clear phases**: Each phase has specific purpose
6. **Documentation**: Reference materials are well-documented
