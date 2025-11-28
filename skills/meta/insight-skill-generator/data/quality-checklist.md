# Quality Validation Checklist

Generated skills must pass all validation criteria before installation. This checklist ensures compliance with Anthropic's skill standards and Connor's quality requirements.

## 1. YAML Frontmatter Validation

### Required Fields
- [ ] `name` field present and valid
  - Max 64 characters
  - Lowercase, numbers, hyphens only
  - No reserved words (skill, claude, anthropic)
  - Matches directory name

- [ ] `description` field present and valid
  - Max 1024 characters
  - Non-empty
  - No XML/HTML tags
  - Action-oriented (starts with verb)

### Description Quality
- [ ] Contains trigger phrase
  - "Use PROACTIVELY when..." OR
  - "Use when..." OR
  - "Guides..." OR
  - "Analyzes..." OR
  - Similar action verb

- [ ] Describes clear value/benefit
  - What problem does it solve?
  - What outcome does it produce?

- [ ] Appropriate for skill category
  - Aligns with insight category
  - Matches skill type (tooling/analysis/productivity)

### Optional Fields (if present)
- [ ] `allowed-tools` (Claude Code only)
  - Valid tool names only
  - No duplicates

- [ ] Custom fields are reasonable
  - `version`, `author`, `category` are common

## 2. File Structure Validation

### Required Files
- [ ] `SKILL.md` exists and is non-empty
- [ ] `README.md` exists and is non-empty
- [ ] `plugin.json` exists and is valid JSON
- [ ] `CHANGELOG.md` exists with v0.1.0 entry

### Optional Files (based on complexity)
- [ ] `data/` directory if complexity >= standard
- [ ] `data/insights-reference.md` if multiple insights
- [ ] `examples/` directory if code examples present
- [ ] `templates/` directory if actionable checklists exist

### File Size Limits
- [ ] SKILL.md < 500 lines (recommend splitting if larger)
- [ ] No single file > 1000 lines
- [ ] Total skill size < 1MB

## 3. SKILL.md Content Quality

### Structure
- [ ] Clear heading hierarchy (h1 → h2 → h3)
- [ ] No skipped heading levels
- [ ] Consistent formatting throughout

### Required Sections
- [ ] Overview/Introduction
  - What the skill does
  - When to use it

- [ ] Workflow or Phases
  - Clear step-by-step instructions
  - Numbered or bulleted steps
  - Logical progression

- [ ] Examples (if applicable)
  - Concrete use cases
  - Expected outputs

### Content Quality
- [ ] Clear, concise language
- [ ] No ambiguous pronouns ("it", "this", "that" without context)
- [ ] Consistent terminology (no mixing synonyms)
- [ ] Action-oriented instructions (imperative mood)

### Progressive Disclosure
- [ ] SKILL.md serves as table of contents
- [ ] Detailed content in separate files (data/, examples/)
- [ ] References are one level deep (no nested references)

## 4. Insight Integration Quality

### Insight Attribution
- [ ] Original insights preserved in `data/insights-reference.md`
- [ ] Insights properly dated and sourced
- [ ] Session metadata included

### Content Transformation
- [ ] Insights converted to actionable workflow steps
- [ ] Problem-solution structure maintained
- [ ] Code examples extracted to examples/
- [ ] Best practices highlighted in Important Reminders

### Deduplication
- [ ] No duplicate content between skill files
- [ ] Cross-references used instead of duplication
- [ ] Consolidated similar points

## 5. Pattern Adherence

### Selected Pattern (phase-based/mode-based/validation)
- [ ] Pattern choice justified by insight content
- [ ] Pattern correctly implemented
- [ ] Section structure matches pattern conventions

### Workflow Logic
- [ ] Phases/modes are sequential or parallel as appropriate
- [ ] Each phase has clear purpose
- [ ] Prerequisites stated upfront
- [ ] Expected outputs defined

### Error Handling
- [ ] Common pitfalls documented
- [ ] Troubleshooting guidance included
- [ ] Failure recovery steps provided

## 6. README.md Quality

### Required Sections
- [ ] Brief overview (1-2 sentences)
- [ ] When to use (trigger phrases)
- [ ] Quick start example
- [ ] Installation instructions (if not standard)

### Clarity
- [ ] User-focused (not developer-focused)
- [ ] Examples are copy-pasteable
- [ ] Screenshots/diagrams if beneficial

## 7. plugin.json Validation

### JSON Validity
- [ ] Valid JSON syntax
- [ ] No trailing commas
- [ ] Proper escaping

### Required Fields
- [ ] `name` matches SKILL.md frontmatter
- [ ] `version` follows semver (0.1.0 for new skills)
- [ ] `description` matches SKILL.md frontmatter
- [ ] `type` is "skill"

### Optional Fields (if present)
- [ ] `author` is reasonable string
- [ ] `category` is valid (tooling/analysis/productivity/devops)
- [ ] `tags` are relevant keywords

## 8. Code Quality (if skill includes examples)

### Code Examples
- [ ] Syntax highlighting specified (```language)
- [ ] Code is complete and runnable
- [ ] No placeholder variables (unless clearly marked)
- [ ] Comments explain non-obvious logic

### Best Practices
- [ ] Follows language conventions
- [ ] No security vulnerabilities
- [ ] No hardcoded credentials
- [ ] Error handling demonstrated

## 9. Accessibility & Usability

### Trigger Phrases
- [ ] Multiple trigger phrases provided
- [ ] Phrases are natural language
- [ ] Covers different ways users might ask
- [ ] PROACTIVELY triggers are specific (not too broad)

### Searchability
- [ ] Skill name reflects function
- [ ] Description contains relevant keywords
- [ ] Tags (if present) aid discovery

### User Guidance
- [ ] Clear next steps after each phase
- [ ] Decision points clearly marked
- [ ] Optional vs. required steps distinguished

## 10. Edge Cases & Robustness

### Input Handling
- [ ] Handles missing/malformed input gracefully
- [ ] Validates prerequisites before execution
- [ ] Provides helpful error messages

### Project Variability
- [ ] Handles different project structures
- [ ] Works with monorepos and single packages
- [ ] Adapts to different tech stacks

### Maintenance
- [ ] No hardcoded paths (use relative or user-provided)
- [ ] No assumptions about environment
- [ ] Graceful degradation if optional tools unavailable

## 11. Insight-Specific Validation

### Quality Filter
- [ ] Only high-quality insights converted
  - Actionable (not just informational)
  - Generally applicable (not project-specific)
  - Valuable (solves real problem)

### Relevance
- [ ] Skill solves problem not covered by existing skills
- [ ] No duplication with skill-creator, sub-agent-creator, etc.
- [ ] Unique value proposition clear

### Scope
- [ ] Skill is focused (does one thing well)
- [ ] Not too broad (overwhelming)
- [ ] Not too narrow (trivial)

## Scoring

### Critical (must pass all)
All items in sections 1-2 (Frontmatter, File Structure)

### High Priority (must pass 90%+)
Sections 3-5 (Content Quality, Insight Integration, Pattern Adherence)

### Medium Priority (must pass 80%+)
Sections 6-9 (README, plugin.json, Code Quality, Usability)

### Optional (nice to have)
Sections 10-11 (Edge Cases, Insight-Specific)

## Auto-Fix Opportunities

Some issues can be auto-corrected:
- [ ] Trim description to 1024 chars
- [ ] Convert skill name to lowercase kebab-case
- [ ] Add missing CHANGELOG.md with v0.1.0
- [ ] Generate basic README.md from SKILL.md overview
- [ ] Validate and pretty-print JSON files

## Manual Review Required

Some issues require user decision:
- Ambiguous trigger phrases
- Pattern selection uncertainty
- Multiple valid skill name options
- Content organization choices
- Category assignment conflicts
