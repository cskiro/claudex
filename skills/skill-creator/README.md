# Skill Creator

Automated skill generation tool that creates production-ready Claude Code skills following Claudex marketplace standards with intelligent templates, pattern detection, and quality validation.

## Quick Start

```
User: "Create a new skill for validating API responses"
```

Claude will:
1. Guide you through interactive questions
2. Detect appropriate skill type and pattern
3. Generate all required files with templates
4. Install to ~/.claude/skills/
5. Provide testing guidance and next steps

## Features

### Feature 1: Intelligent Skill Generation
- Interactive guided creation with smart defaults
- Automatic skill type detection (minimal/standard/complex)
- Pattern selection based on skill purpose
- Jinja2-based template population
- Quality validation before finalization

### Feature 2: Multiple Creation Modes
- **Guided Creation**: Full interactive process with questions
- **Quick Start**: Template-based for fast setup
- **Clone & Modify**: Base on existing skill patterns
- **Validation Only**: Check existing skill quality

### Feature 3: Comprehensive Structure
- All required files (SKILL.md, README.md, plugin.json, CHANGELOG.md)
- Optional directories based on complexity (data/, examples/, templates/, modes/, scripts/)
- Pattern-specific templates and guidance
- Clear TODO markers for customization

### Feature 4: Quality Assurance
- Built-in quality checklist validation
- Security checks (no secrets or sensitive data)
- Syntax validation (YAML, JSON, Markdown)
- Naming convention enforcement
- Grade-based scoring (A-F)

## Installation

```bash
# Already installed in your .claude directory!
# Located at: ~/.claude/skills/skill-creator/
```

Or install manually:

```bash
cp -r skill-creator ~/.claude/skills/
```

## Usage Examples

### Example 1: Create Analysis Skill

**Scenario:** Create a skill that audits React components for performance issues

```
User: "Create a new skill for auditing React components"
```

**Claude will ask:**
1. Skill name: "react-performance-auditor"
2. Description: "Analyzes React components for performance anti-patterns"
3. Category: analysis (auto-suggested)
4. Trigger phrases: (auto-generated + user confirms)
5. Complexity: Standard (has reference materials)

**Result:**
- Complete skill directory created
- Standard structure with data/ for anti-patterns reference
- Validation pattern applied
- Quality report: Grade A
- Ready for customization

### Example 2: Create Multi-Mode Skill

**Scenario:** Create a skill that manages environment variables (create/update/delete/list)

```
User: "Create a skill for managing environment variables with multiple modes"
```

**Claude will ask:**
1. Basic info (name, description, author)
2. Confirms: Complex skill with modes
3. How many modes? 4 (create, update, delete, list)
4. For each mode: name and trigger phrase
5. Structure: Creates modes/ directory

**Result:**
- Complex skill with mode-based pattern
- Separate workflow files for each mode
- Mode detection logic in SKILL.md
- Quick decision matrix included
- Ready for mode-specific customization

### Example 3: Create Data Processing Skill

**Scenario:** Create a skill that analyzes git commit history

```
User: "Create a skill that analyzes git commit patterns"
```

**Claude will detect:**
- Data processing skill (analyzes git data)
- Needs scripts/ directory
- Should generate reports

**Result:**
- Complex data-processing structure
- scripts/ directory with placeholder scripts
- Data pipeline architecture documented
- Report templates included
- Performance characteristics section

### Example 4: Quick Start with Template

**Scenario:** Quickly scaffold a minimal skill

```
User: "Create a minimal skill called code-formatter"
```

**Claude will:**
1. Recognize "minimal" keyword
2. Ask only essential questions (name, description)
3. Use minimal template from examples/
4. Generate with defaults
5. Flag customization points

**Result:**
- Minimal structure (4 required files only)
- Fast generation (<1 minute)
- All customization points marked with TODO
- Simple phase-based workflow template

### Example 5: Clone Existing Pattern

**Scenario:** Create skill with same structure as codebase-auditor

```
User: "Create a skill similar to codebase-auditor for database schemas"
```

**Claude will:**
1. Read codebase-auditor structure
2. Extract pattern (validation, phase-based)
3. Ask for new skill details
4. Generate with same organizational structure
5. Clear codebase-specific content

**Result:**
- Same directory structure as codebase-auditor
- Validation pattern applied
- data/ and examples/ directories included
- Content cleared, ready for customization

### Example 6: Validate Existing Skill

**Scenario:** Check quality of skill you're working on

```
User: "Validate my custom-skill"
```

**Claude will:**
1. Locate skill at ~/.claude/skills/custom-skill/
2. Run quality checklist
3. Check all files and syntax
4. Generate detailed report
5. Provide remediation steps

**Result:**
```markdown
# Quality Report: custom-skill

## Grade: B (85/100)

### Issues Found:
⚠️ HIGH: Missing usage examples in README.md
📋 MEDIUM: Could use more trigger phrases (only 2, recommend 3-5)
ℹ️ LOW: CHANGELOG could include more detail

### Remediation:
1. Add 2-3 concrete examples to README.md
2. Add 1-2 more trigger phrases to SKILL.md
3. Expand CHANGELOG Added section

### Security: ✅ PASS (no issues)
### Syntax: ✅ PASS (all valid)
```

## Requirements

- Claude Code with Skills support
- Write access to ~/.claude/skills/ directory
- Python 3.8+ (for Jinja2 templates, if using scripts)

## Configuration

No additional configuration required. The skill uses:
- Built-in templates from `templates/`
- Pattern libraries from `patterns/`
- Reference data from `data/`
- Examples from `examples/`

## Troubleshooting

### Issue 1: Skill name already exists
**Problem:** Directory ~/.claude/skills/[name]/ already exists
**Solution:**
- Choose a different name, or
- Backup existing skill and remove directory, or
- Use validation mode to check existing skill instead

### Issue 2: Permission denied
**Problem:** Cannot write to ~/.claude/skills/
**Solution:**
```bash
# Check permissions
ls -la ~/.claude/

# Fix permissions if needed
chmod 755 ~/.claude/skills/

# Verify
ls -la ~/.claude/skills/
```

### Issue 3: Generated skill won't load
**Problem:** Claude Code doesn't recognize new skill
**Solution:**
1. Check YAML frontmatter syntax in SKILL.md
2. Verify plugin.json is valid JSON
3. Restart Claude Code session
4. Check skill appears in skill list

### Issue 4: Templates not rendering
**Problem:** Jinja2 template errors during generation
**Solution:**
- Verify templates/ directory exists
- Check template syntax
- Report issue with specific error message

## Best Practices

1. **Start Simple**: Use minimal structure, grow as needed
2. **Clear Trigger Phrases**: Make them intuitive and specific
3. **Concrete Examples**: Show real usage scenarios in README
4. **Test Early**: Try trigger phrases immediately after generation
5. **Iterate**: Customize, test, refine workflow
6. **Validate Often**: Run validation after changes
7. **Reference Examples**: Look at existing skills for inspiration
8. **Document Well**: Future you will thank you

## Limitations

- Cannot automatically implement skill logic (only scaffolding)
- Jinja2 templates are opinionated (based on Claudex standards)
- Assumes standard skill structure (may not fit all use cases)
- Quality validation is structural (doesn't test functionality)
- Mode detection requires clear user intent

## Contributing

See [CONTRIBUTING.md](https://github.com/cskiro/claudex/blob/main/CONTRIBUTING.md) for contribution guidelines.

## License

Apache 2.0

## Version History

See [CHANGELOG.md](./CHANGELOG.md) for version history.

## Quick Reference

### Skill Types
- **Minimal**: Simple automation, single workflow (4 files)
- **Standard**: Sequential phases, reference materials (4 files + 3 dirs)
- **Complex (Mode-Based)**: Multiple distinct modes (4 files + modes/)
- **Complex (Data Processing)**: Data analysis, reports (4 files + scripts/)

### Patterns
- **Phase-Based**: Sequential workflow with clear stages
- **Mode-Based**: Multiple workflows based on user intent
- **Validation**: Audit/compliance checking pattern
- **Data Processing**: Ingest → Process → Analyze → Report

### Categories
- **analysis**: Code analysis, auditing, quality checking
- **tooling**: Development tools, configuration validators
- **productivity**: Workflow, automation, insights
- **devops**: Infrastructure, deployment, monitoring

### Creation Modes
- **Guided**: Full interactive (most control)
- **Quick Start**: Template-based (fastest)
- **Clone**: Copy existing pattern (proven structure)
- **Validate**: Check existing quality (QA)

## Support

For questions or issues:
1. Check this README for common scenarios
2. Review examples/ directory for structure guidance
3. Consult patterns/ for pattern-specific guidance
4. Read data/quality-checklist.md for validation criteria
5. Open a discussion on GitHub

## Related Skills

- **claude-md-auditor**: Validates SKILL.md files specifically
- **codebase-auditor**: General code quality analysis
- All skills in ~/.claude/skills/ serve as examples

---

**Remember**: This skill handles the boring scaffolding work so you can focus on the creative and domain-specific parts of your skill!
