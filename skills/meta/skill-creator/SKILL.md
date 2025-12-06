---
name: skill-creator
version: 0.2.0
description: Use PROACTIVELY when creating new Claude Code skills from scratch. Automated generation tool following Claudex marketplace standards with intelligent templates, pattern detection, and quality validation. Supports guided creation, quick start templates, clone-and-modify, and validation-only modes. Not for modifying existing skills or non-skill Claude Code configurations.
---

# Skill Creator

Automates creation of Claude Code skills through interactive guidance, template generation, and quality validation.

## When to Use

**Trigger Phrases**:
- "create a new skill for [purpose]"
- "generate a skill called [name]"
- "scaffold a [type] skill"
- "set up a new skill"

**Use Cases**:
- Creating new skills from scratch
- Following Claudex marketplace standards
- Learning skill structure through examples

## Quick Decision Matrix

| User Request | Mode | Action |
|--------------|------|--------|
| "create skill for [purpose]" | Guided | Interactive creation |
| "create [type] skill" | Quick Start | Template-based |
| "skill like [existing]" | Clone | Copy pattern |
| "validate skill" | Validate | Quality check |

## Mode 1: Guided Creation (Default)

**Use when**: User wants full guidance and customization

**Process**:
1. Gather basic info (name, description, author)
2. Define purpose, category, triggers
3. Assess complexity → determine skill type
4. Customize directory structure
5. Select pattern (mode-based, phase-based, validation, data-processing)
6. Generate files from templates
7. Run quality validation
8. Provide installation and next steps

**Workflow**: `workflow/guided-creation.md`

## Mode 2: Quick Start

**Use when**: User specifies skill type directly (minimal, standard, complex)

**Process**:
1. Confirm skill type
2. Gather minimal required info
3. Generate with standardized defaults
4. Flag ALL customization points

**Advantages**: Fast, minimal questions
**Trade-off**: More TODO sections to customize

## Mode 3: Clone & Modify

**Use when**: User wants to base skill on existing one

**Process**:
1. Read existing skill's structure
2. Extract organizational pattern (not content)
3. Generate new skill with same structure
4. Clear example-specific content

**Advantages**: Proven structure, familiar patterns

## Mode 4: Validation Only

**Use when**: User wants to check existing skill quality

**Process**:
1. Read existing skill files
2. Run quality checklist
3. Generate validation report
4. Offer to fix issues automatically

**Use Case**: Before submission, after modifications

## Skill Types

| Type | Complexity | Directories | Pattern |
|------|------------|-------------|---------|
| Minimal | Low | SKILL.md, README.md only | phase-based |
| Standard | Medium | + data/, examples/ | phase-based or validation |
| Complex (mode) | High | + modes/, templates/ | mode-based |
| Complex (data) | High | + scripts/, data/ | data-processing |

## Generated Files

**Required** (all skills):
- `SKILL.md` - Main skill manifest
- `README.md` - User documentation
- `plugin.json` - Marketplace metadata
- `CHANGELOG.md` - Version history

**Optional** (based on type):
- `modes/` - Mode-specific workflows
- `data/` - Reference materials
- `examples/` - Example outputs
- `templates/` - Reusable templates
- `scripts/` - Automation scripts

## Quality Validation

Validates against `data/quality-checklist.md`:

- File existence (all required files)
- Syntax (YAML frontmatter, JSON)
- Content completeness
- Security (no secrets)
- Naming conventions (kebab-case)
- Quality grade (A-F)

## Success Criteria

- [ ] All required files generated
- [ ] Valid YAML frontmatter
- [ ] Valid JSON in plugin.json
- [ ] No security issues
- [ ] Kebab-case naming
- [ ] Version 0.1.0 for new skills
- [ ] At least 3 trigger phrases
- [ ] Quality grade C or better

## Reference Materials

### Templates
- `templates/SKILL.md.j2` - Main manifest
- `templates/README.md.j2` - Documentation
- `templates/plugin.json.j2` - Metadata
- `templates/CHANGELOG.md.j2` - History

### Patterns
- `patterns/mode-based.md` - Multi-mode skills
- `patterns/phase-based.md` - Sequential workflows
- `patterns/validation.md` - Audit skills
- `patterns/data-processing.md` - Data analysis

### Reference Data
- `data/categories.yaml` - Valid categories
- `data/skill-types.yaml` - Type definitions
- `data/quality-checklist.md` - Validation criteria

### Examples
- `examples/minimal-skill/`
- `examples/standard-skill/`
- `examples/complex-skill/`

## Quick Commands

```bash
# Check existing skills
ls ~/.claude/skills/

# View skill structure
tree ~/.claude/skills/[skill-name]/

# Validate frontmatter
head -20 ~/.claude/skills/[skill-name]/SKILL.md

# Validate JSON
python -m json.tool ~/.claude/skills/[skill-name]/plugin.json
```

## Error Handling

| Error | Solution |
|-------|----------|
| Name exists | Suggest alternatives or confirm overwrite |
| Invalid name | Explain kebab-case, provide corrected suggestion |
| Permission denied | Check ~/.claude/skills/ write access |
| Template fails | Fallback to manual creation with guidance |

---

**Version**: 0.1.0 | **Author**: Connor
