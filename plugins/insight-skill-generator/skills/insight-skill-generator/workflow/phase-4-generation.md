# Phase 4: Skill Generation

**Purpose**: Create all skill files following the approved design.

## Steps

### 1. Prepare generation workspace
- Create temporary directory for skill assembly
- Load templates from `templates/` directory

### 2. Generate SKILL.md
- Create frontmatter with name and description
- Add h1 heading
- Generate Overview section (what, based on X insights, capabilities)
- Generate "When to Use" section (trigger phrases, use cases, anti-use cases)
- Generate Response Style section
- Generate workflow sections based on pattern:
  - Phase-based: Phase 1, Phase 2, etc. with Purpose, Steps, Output, Common Issues
  - Mode-based: Mode 1, Mode 2, etc. with When to use, Steps, Output
  - Validation: Analysis → Detection → Recommendations
- Generate Reference Materials section
- Generate Important Reminders
- Generate Best Practices
- Generate Troubleshooting
- Add Metadata section with source insight attribution

### 3. Generate README.md
- Brief overview (1-2 sentences)
- Installation instructions (standard)
- Quick start example
- Trigger phrases list
- Link to SKILL.md for details

### 4. Generate plugin.json
```json
{
  "name": "[skill-name]",
  "version": "0.1.0",
  "description": "[description]",
  "type": "skill",
  "author": "Connor",
  "category": "[category from clustering-config]",
  "tags": ["insights", "lessons-learned", "[domain]"]
}
```

### 5. Generate CHANGELOG.md
Initialize with v0.1.0 and list key features.

### 6. Generate data/insights-reference.md (if complexity >= standard)
- Add overview (insight count, date range, categories)
- For each insight: title, metadata, original content, code examples, related insights
- Add clustering analysis section
- Add insight-to-skill mapping explanation

### 7. Generate examples/ (if needed)
- Extract and organize code blocks by language or topic
- Add explanatory context
- Create usage examples showing example prompts and expected behaviors

### 8. Generate templates/ (if needed)
- Create templates/checklist.md from actionable items
- Organize items by section
- Add verification steps
- Include common mistakes section

### 9. Validate all generated files
- Check YAML frontmatter syntax
- Validate JSON syntax
- Check file references are valid
- Verify no broken markdown links
- Run quality checklist
- Report validation results to user

### 10. Preview generated skill
- Show file tree
- Show key sections from SKILL.md
- Show README.md preview
- Highlight any validation warnings

## Output

Complete, validated skill in temporary workspace, ready for installation.

## Common Issues

- **Validation failures**: Fix automatically if possible, otherwise ask user
- **Missing code examples**: Offer to generate placeholder or skip examples/ directory
- **Large SKILL.md** (>500 lines): Suggest splitting content into separate files
