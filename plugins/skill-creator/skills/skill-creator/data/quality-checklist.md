# Skill Quality Checklist

Use this checklist to validate skill quality before submission or installation.

## Required Files (Critical)

- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] `README.md` exists with usage examples
- [ ] `plugin.json` exists with valid JSON
- [ ] `CHANGELOG.md` exists with v0.1.0 entry

## SKILL.md Validation

### Frontmatter
- [ ] `name` field present (kebab-case)
- [ ] `version` field present (0.1.0 for new skills)
- [ ] `description` field present (1-2 sentences)
- [ ] `author` field present

### Required Sections
- [ ] "Overview" section describes skill capabilities
- [ ] "When to Use This Skill" with trigger phrases
- [ ] "When to Use This Skill" with use cases (3-5 items)
- [ ] "Core Responsibilities" or "Workflow" section
- [ ] "Success Criteria" or similar completion checklist

### Content Quality
- [ ] No placeholder text like "[TODO]" or "[FILL IN]" (unless marked for user customization)
- [ ] Trigger phrases are specific and actionable
- [ ] Use cases clearly describe when to activate skill
- [ ] Workflow or responsibilities are detailed
- [ ] No generic programming advice (Claude already knows this)

## README.md Validation

### Structure
- [ ] Title matches skill name
- [ ] Brief description (1-2 sentences) at top
- [ ] "Quick Start" section with example
- [ ] "Installation" instructions
- [ ] At least 2 usage examples

### Content Quality
- [ ] Examples are concrete and actionable
- [ ] Installation instructions are clear
- [ ] Requirements section lists dependencies
- [ ] Troubleshooting section addresses common issues

## plugin.json Validation

### Required Fields
- [ ] `name` matches skill directory name
- [ ] `version` is valid semver (0.1.0 for new skills)
- [ ] `description` matches SKILL.md frontmatter
- [ ] `author` present
- [ ] `license` is "Apache-2.0"
- [ ] `homepage` URL is correct
- [ ] `repository` object present with type and url

### Components
- [ ] `components.agents` array present
- [ ] At least one agent with `name` and `manifestPath`
- [ ] `manifestPath` points to "SKILL.md"

### Metadata
- [ ] `metadata.category` is one of: analysis, tooling, productivity, devops
- [ ] `metadata.status` is "proof-of-concept" for new skills
- [ ] `metadata.tested` describes testing scope

### Keywords
- [ ] At least 3 keywords present
- [ ] Keywords are relevant and specific
- [ ] Keywords aid discoverability (not too generic)

## CHANGELOG.md Validation

- [ ] Follows "Keep a Changelog" format
- [ ] Has section for version 0.1.0
- [ ] Date is present and correct
- [ ] "Added" section lists initial features
- [ ] Status section describes testing level
- [ ] Link to release tag at bottom

## Security Validation (Critical)

- [ ] No API keys, tokens, or passwords in any file
- [ ] No database connection strings with credentials
- [ ] No private keys (PEM format)
- [ ] No internal IP addresses or infrastructure details
- [ ] No hardcoded secrets of any kind

## Version Control

- [ ] `.gitignore` present if skill generates files (like .processed/)
- [ ] No generated files committed (build artifacts, logs, etc.)
- [ ] No large binary files (> 1MB)

## Naming Conventions

- [ ] Skill name is kebab-case (e.g., "skill-name")
- [ ] Directory name matches skill name
- [ ] No spaces in names
- [ ] Name is descriptive and not too generic

## Documentation Quality

- [ ] All sections are complete (no stubs)
- [ ] Examples are realistic and helpful
- [ ] Technical terms are explained or linked
- [ ] Grammar and spelling are correct
- [ ] Markdown formatting is valid

## Pattern Consistency

If skill uses specific pattern:

### Mode-Based Skills
- [ ] "Quick Decision Matrix" present
- [ ] "Mode Detection Logic" present
- [ ] Each mode has clear trigger phrases
- [ ] Modes are distinct and non-overlapping

### Phase-Based Skills
- [ ] Phases are numbered and named
- [ ] Each phase has clear purpose
- [ ] Dependencies between phases are documented
- [ ] Transition criteria are explicit

### Validation Skills
- [ ] Validation sources are documented
- [ ] Finding structure is consistent
- [ ] Severity levels are defined
- [ ] Score calculation is explained

### Data Processing Skills
- [ ] Data flow architecture is documented
- [ ] Storage strategy is explained
- [ ] Performance characteristics are listed
- [ ] Helper scripts are provided

## Testing Validation

- [ ] Skill can be loaded without errors
- [ ] Trigger phrases activate the skill
- [ ] Example workflows complete successfully
- [ ] No obvious bugs or crashes

## User Experience

- [ ] Skill purpose is immediately clear
- [ ] Trigger phrases are intuitive
- [ ] Workflow is logical and easy to follow
- [ ] Error messages are helpful
- [ ] Success criteria are measurable

## Scoring

**Critical Issues** (Must fix before use):
- Missing required files
- Invalid JSON/YAML
- Security issues (exposed secrets)
- Skill fails to load

**High Priority** (Fix before submission):
- Incomplete documentation
- Missing examples
- Unclear trigger phrases
- Invalid metadata

**Medium Priority** (Improve when possible):
- Inconsistent formatting
- Missing optional sections
- Could use more examples
- Documentation could be clearer

**Low Priority** (Nice to have):
- Additional examples
- More detailed explanations
- Enhanced formatting
- Extra reference materials

## Overall Quality Score

Calculate a quality score:

```
Critical Issues: 0 required (any critical issue = fail)
High Priority: 0-2 acceptable (> 2 needs work)
Medium Priority: 0-5 acceptable (> 5 needs improvement)
Low Priority: Any number acceptable

Overall Grade:
- A (90-100): Production ready, excellent quality
- B (80-89): Good quality, minor improvements
- C (70-79): Acceptable, some improvements needed
- D (60-69): Needs work before submission
- F (< 60): Significant issues, do not submit
```

## Pre-Submission Final Check

Before submitting to marketplace:

1. [ ] Run through entire checklist
2. [ ] Test in fresh Claude Code session
3. [ ] Get peer review if possible
4. [ ] Verify all links work
5. [ ] Check for typos and errors
6. [ ] Confirm no sensitive data
7. [ ] Verify version is correct
8. [ ] Update CHANGELOG if needed
