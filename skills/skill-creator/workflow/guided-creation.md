# Guided Creation Workflow

Detailed step-by-step process for Mode 1: Interactive skill creation.

## Step 1: Basic Information

Ask user for:

### Skill Name
- Format: kebab-case (lowercase, hyphens)
- Validate: no spaces, descriptive
- Examples: "code-formatter", "test-generator", "api-validator"
- Check: name doesn't conflict with existing skills

### Brief Description
- 1-2 sentences for metadata
- Used in plugin.json and SKILL.md frontmatter
- Should clearly state what skill does

### Author Name
- Default: Connor
- Used in all metadata files

## Step 2: Skill Purpose & Category

### Detailed Description
- 2-4 sentences for SKILL.md Overview
- Explains full capabilities

### Category Selection
Present options from `data/categories.yaml`:
- **analysis**: Code analysis, auditing, quality checking
- **tooling**: Development tools, configuration validators
- **productivity**: Developer workflow, automation, insights
- **devops**: Infrastructure, deployment, monitoring

Suggest category based on skill purpose, allow user to confirm/change.

### Trigger Phrases
- Ask for 3-5 phrases users might say
- Provide examples based on similar skills
- Generate suggestions if needed

### Use Cases
- 3-5 concrete scenarios
- Specific, actionable situations

## Step 3: Complexity Assessment

Determine skill type through questions:

**Question 1**: "Does this skill have multiple distinct modes or workflows?"
- Yes → Complex (mode-based)
- No → Continue

**Question 2**: "Does this skill process data from files or generate reports?"
- Yes → Complex (data-processing)
- No → Continue

**Question 3**: "Does this skill need reference materials?"
- Yes → Standard
- No → Minimal

Reference: `data/skill-types.yaml`

## Step 4: Structure Customization

Based on type, ask about optional directories:

### For Standard or Complex skills:
- "Will you need reference data files?" → create data/
- "Will you need example outputs?" → create examples/
- "Will you need reusable templates?" → create templates/

### For Complex (mode-based) skills:
- "How many modes does this skill have?" (2-5 typical)
- For each mode:
  - Mode name
  - When to use (trigger phrases)
  - Primary action

### For Complex (data-processing) skills:
- "What data sources will you process?"
- "What output formats do you need?"
- Always create scripts/ directory

## Step 5: Pattern Selection

Select from `patterns/` based on skill type:
- Minimal → phase-based.md
- Standard → phase-based.md or validation.md
- Complex (mode-based) → mode-based.md
- Complex (data-processing) → data-processing.md

Present pattern to user: "I'll use the [pattern] pattern, which means..."

## Step 6: Generation

### Create Directory Structure
```bash
mkdir -p ~/.claude/skills/[skill-name]/{required,optional-dirs}
```

### Generate Files from Templates
Using Jinja2 templates:
- SKILL.md from `templates/SKILL.md.j2`
- README.md from `templates/README.md.j2`
- plugin.json from `templates/plugin.json.j2`
- CHANGELOG.md from `templates/CHANGELOG.md.j2`

### Apply Pattern-Specific Content
- Include pattern guidance in sections
- Add pattern templates if needed
- Create mode files if mode-based

### Mark Customization Points
- Add TODO comments where needed
- Provide inline guidance
- Reference examples/

## Step 7: Quality Validation

Run validation using `data/quality-checklist.md`:

1. **File Existence**: Verify all required files
2. **Syntax Validation**: Check YAML/JSON
3. **Content Completeness**: No empty required sections
4. **Security Check**: No secrets
5. **Naming Conventions**: Verify kebab-case
6. **Quality Score**: Calculate A-F grade

### Validation Report Format

```markdown
# Skill Quality Report: [skill-name]

## Status: [PASS/NEEDS WORK]

### Files Generated
✅ SKILL.md
✅ README.md
✅ plugin.json
✅ CHANGELOG.md

### Quality Score: [Grade]

### Items Needing Customization
- [ ] SKILL.md: Complete "Response Style" section
- [ ] SKILL.md: Fill in workflow details
- [ ] README.md: Add concrete usage examples

### Validation Results
✅ No security issues
✅ Valid YAML frontmatter
✅ Valid JSON in plugin.json
✅ Proper naming conventions
```

## Step 8: Installation & Next Steps

### Verify Installation
```bash
ls -la ~/.claude/skills/[skill-name]/
```

### Testing Guidance
```markdown
## Test Your Skill

Try these trigger phrases in a new Claude session:
1. "[trigger-phrase-1]"
2. "[trigger-phrase-2]"
3. "[trigger-phrase-3]"

Expected behavior: [What should happen]
```

### Customization TODO List
- List all sections marked with TODO
- Prioritize by importance
- Provide examples for each

### Next Steps
```markdown
## Next Steps

1. Review generated files in ~/.claude/skills/[skill-name]/
2. Customize sections marked with TODO
3. Add reference materials to data/ (if applicable)
4. Create example outputs in examples/ (if applicable)
5. Test trigger phrases in new Claude session
6. Iterate on description and workflow
7. Run validation again
8. Ready to use or submit to marketplace!
```

## Information Summary

By end of guided creation, you should have:

| Field | Source | Used In |
|-------|--------|---------|
| Skill name | User input | Directory, all files |
| Brief description | User input | plugin.json, frontmatter |
| Detailed description | User input | SKILL.md Overview |
| Author | User input (default: Connor) | All metadata |
| Category | User selection | plugin.json |
| Trigger phrases | User input | SKILL.md |
| Use cases | User input | SKILL.md |
| Skill type | Assessment | Structure decisions |
| Pattern | Auto-selected | SKILL.md structure |
| Optional dirs | User input | Directory structure |
