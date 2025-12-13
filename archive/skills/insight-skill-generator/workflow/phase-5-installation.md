# Phase 5: Installation and Testing

**Purpose**: Install the skill and provide testing guidance.

## Steps

### 1. Ask installation location
Present options:
- **Project-specific**: `[project]/.claude/skills/[skill-name]/`
  - Pros: Version controlled with project, only available in this project
  - Cons: Not available in other projects
- **Global**: `~/.claude/skills/[skill-name]/`
  - Pros: Available in all projects
  - Cons: Not version controlled (unless user manages ~/.claude with git)

### 2. Check for conflicts
- Verify chosen location doesn't already have a skill with same name
- If conflict found:
  - Show existing skill details
  - Offer options: Choose different name, Overwrite (with confirmation), Cancel

### 3. Copy skill files
- Create target directory
- Copy all generated files preserving structure
- Set appropriate permissions
- Verify all files copied successfully

### 4. Re-validate installed skill
- Read SKILL.md from install location
- Verify frontmatter is still valid
- Check file references work from install location
- Confirm no corruption during copy

### 5. Test skill loading
- Attempt to trigger skill using one of the trigger phrases
- Verify Claude Code recognizes the skill
- Check skill appears in available skills list
- Report results to user

### 6. Provide testing guidance
Show trigger phrases to test:
```
Try these phrases to test your new skill:
- "[trigger phrase 1]"
- "[trigger phrase 2]"
- "[trigger phrase 3]"
```

Suggest test scenarios based on skill purpose and explain expected behavior.

### 7. Offer refinement suggestions
Based on skill characteristics, suggest potential improvements:
- Add more examples if skill is complex
- Refine trigger phrases if they're too broad/narrow
- Split into multiple skills if scope is too large
- Add troubleshooting section if skill has edge cases

Ask if user wants to iterate on the skill.

### 8. Document the skill
Offer to add skill to project documentation:
```markdown
### [Skill Name]
**Location**: [path]
**Purpose**: [description]
**Trigger**: "[main trigger phrase]"
**Source**: Generated from [X] insights ([categories])
```

### 9. Next steps
Suggest:
- Test the skill with real scenarios
- Share with team if relevant
- Iterate based on usage (version 0.2.0)
- Generate more skills from other insight clusters

Ask if user wants to generate another skill from remaining insights.

## Output

Installed, validated skill with testing guidance and refinement suggestions.

## Common Issues

- **Installation permission errors**: Check directory permissions, suggest sudo if needed
- **Skill not recognized**: Verify frontmatter format, check Claude Code skill discovery
- **Trigger phrases don't work**: Suggest broadening or clarifying phrases
- **Conflicts with existing skills**: Help user choose unique name or merge functionality
