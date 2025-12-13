# Minimal Skill Structure Example

This example shows the minimal required structure for a simple skill.

## Directory Structure

```
minimal-skill/
├── SKILL.md           # Agent manifest (required)
├── README.md          # User documentation (required)
├── plugin.json        # Marketplace metadata (required)
└── CHANGELOG.md       # Version history (required)
```

## When to Use Minimal Structure

Use this structure when:
- Skill has a single straightforward workflow
- No multiple modes or complex branching
- Minimal configuration needed
- No external dependencies or scripts
- Simple automation or transformation task

## Examples of Minimal Skills

- **Code Formatter**: Applies consistent formatting to code files
- **Template Generator**: Creates files from simple templates
- **Single-Purpose Validator**: Checks one specific thing

## Characteristics

- **Complexity**: Low
- **Files**: 4 required only
- **Pattern**: Usually phase-based with 2-3 simple phases
- **Modes**: None (single workflow)
- **Scripts**: None
- **Dependencies**: None or minimal

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

What this skill does in detail.

## When to Use This Skill

**Trigger Phrases:**
- "phrase 1"
- "phrase 2"

**Use Cases:**
- Use case 1
- Use case 2

## Workflow

### Phase 1: Setup
1. Validate inputs
2. Gather context

### Phase 2: Execute
1. Perform main action
2. Verify result

### Phase 3: Completion
1. Report results
2. Provide next steps

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

## Best Practices

1. **Keep it simple**: Don't add structure you don't need
2. **Clear workflow**: 2-4 phases maximum
3. **Explicit success criteria**: User knows when it's done
4. **Good examples**: Show concrete usage in README
5. **Test thoroughly**: Minimal doesn't mean untested
