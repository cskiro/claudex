# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Claudex is a **Claude Code marketplace** that distributes skills and hooks through a plugin-based architecture. This is NOT a traditional application codebase - it's a marketplace distribution system following Anthropic's plugin schema.

### Architecture Model

```
marketplace.json (Single Source of Truth)
    ↓
8 Plugin Categories → 18 Skills + 1 Hook
    ↓
Each skill: SKILL.md (agent manifest) + supporting files
```

**Key Principle**: The `.claude-plugin/marketplace.json` file is the **single source of truth** for all marketplace metadata. Individual `plugin.json` files in skill directories are NOT used and should NOT be created.

## Semantic Guidance - When to Use Project Skills

### Release Workflow (After PR Merge to Main)

**Context**: When a PR has been merged to main and you need to create a release (tag + GitHub release).

**Use**: `semantic-release-tagger` skill (skills/release-management/semantic-release-tagger/)

**Why**: This skill automates the entire release workflow following established repository conventions:
- Analyzes repository state and detects existing tag patterns (`@` separator convention)
- Parses conventional commits since last tag to determine version bump (MAJOR/MINOR/PATCH)
- Calculates next version automatically (e.g., marketplace@1.2.0 → marketplace@1.2.1)
- Creates annotated git tags with proper naming (`marketplace@X.Y.Z` for marketplace, `skill-name@X.Y.Z` for skills)
- Generates concise release notes (≤200 words) from conventional commits
- Pushes tags and creates GitHub release automatically after confirmation

**Trigger phrases**:
- "The PR was merged, create a release"
- "Tag this release"
- "Create marketplace release for version X.Y.Z"

**Expected behavior**: The skill will run Phase 0 auto-analysis, present findings with recommended version, request confirmation, then execute tag creation and GitHub release publishing. You don't need to manually run git tag or gh release commands.

**Benefit**: Eliminates manual tag creation errors, enforces naming consistency, prevents version conflicts, and generates proper release notes automatically.

### Skill Creation (New Skill Development)

**Context**: When you need to create a new skill for the marketplace.

**Use**: `skill-creator` skill (skills/meta/skill-creator/)

**Why**: Automates skill scaffolding following marketplace standards:
- Generates required files (SKILL.md with frontmatter, README.md, CHANGELOG.md)
- Creates proper directory structure with data/ and examples/ folders
- Enforces version 0.1.0 for initial releases
- Validates skill metadata and structure
- Updates marketplace.json with new skill path

**Trigger phrases**:
- "Create a new skill for [purpose]"
- "Generate a skill called [name]"
- "Set up a new skill"

**Expected behavior**: Interactive workflow asking for skill name, category, description, then generates all required files with proper templates.

**Benefit**: Ensures structural consistency, prevents missing required files, eliminates manual template errors.

### Marketplace Validation (Before Committing Changes)

**Context**: When you've modified marketplace.json, added/removed skills, or need to verify marketplace integrity.

**Use**: Validation scripts in `scripts/`:
- `scripts/validate-marketplace.py` - Schema and path validation
- `scripts/validate-skills.py` - Individual skill quality validation

**Why**: Ensures Anthropic schema compliance before committing:
- Validates marketplace.json structure and required fields
- Verifies all skill paths resolve to existing directories
- Checks plugin category consistency
- Detects missing SKILL.md files
- Validates individual skills against Anthropic spec (name, description, version)

**Trigger phrases**:
- "Validate the marketplace"
- "Check if marketplace.json is valid"
- "Run validation before committing"
- "Validate the skills"

**Expected behavior**: Scripts output validation status with green checkmarks for passes, yellow warnings, or red errors if critical issues found. Exit code 0 = passed.

**Benefit**: Prevents invalid marketplace.json from being committed, catches broken skill paths early, ensures skill quality.

## Validation & Testing

### Marketplace Validation

**Primary validation commands:**
```bash
# Validate marketplace.json schema
python3 scripts/validate-marketplace.py

# Validate individual skills against Anthropic spec
python3 scripts/validate-skills.py --all

# Validate specific category
python3 scripts/validate-skills.py skills/analysis
```

**Expected output:**
- ✅ Validation passed
- ⚠️  1 warning about `productivity-hooks` empty skills array (expected - hooks-only plugin)

**What it validates:**
- Anthropic schema compliance
- Skill path resolution
- Plugin category structure
- Metadata consistency

### No Traditional Testing

This repository does NOT have:
- npm test commands
- TypeScript compilation
- ESLint/Prettier
- Coverage requirements

Skills are **Claude Code agent manifests** (markdown files), not executable code. Validation is structural, not functional.

## Repository Structure

```
claudex/
├── .claude-plugin/
│   ├── marketplace.json           # SINGLE SOURCE OF TRUTH
│   └── validate-marketplace.py    # Validation script
├── skills/                         # 7 categories of skills
│   ├── api/                        # Anthropic API features
│   ├── analysis/                   # Code quality auditing
│   ├── claude-code/                # Claude Code ecosystem
│   ├── devops/                     # Infrastructure automation
│   ├── meta/                       # Skill creation tools
│   ├── release-management/         # Versioning and releases
│   └── testing/                    # Testing frameworks
├── hooks/
│   ├── hooks.json                  # Hook registry
│   └── extract-explanatory-insights.sh
└── docs/lessons-learned/           # Categorized insights (auto-generated by hook)
```

### Skill Directory Structure

**Required files for every skill:**
```
skill-name/
├── SKILL.md           # Agent manifest (frontmatter + workflow)
├── README.md          # User documentation
└── CHANGELOG.md       # Version history
```

**Recommended files:**
```
skill-name/
├── data/              # Reference materials, insights
├── examples/          # Sample outputs
├── scripts/           # Implementation code (Python/Bash)
├── reference/         # Standards, best practices
└── requirements.txt   # Python dependencies (if applicable)
```

**IMPORTANT**: Do NOT create `plugin.json` files in skill directories. They are not required by Anthropic schema and will trigger validation warnings.

## Marketplace Integration

### marketplace.json Schema

```json
{
  "name": "claudex",
  "metadata": {
    "version": "X.Y.Z"    // Marketplace version (semantic versioning)
  },
  "plugins": [
    {
      "name": "category-name",
      "description": "Category description",
      "skills": [
        "./skills/category/skill-name"  // Path to skill directory
      ]
    }
  ]
}
```

### Adding a New Skill

1. **Create skill directory** under appropriate category:
   ```bash
   mkdir -p skills/category-name/skill-name
   ```

2. **Create required files**:
   - `SKILL.md` with frontmatter:
     ```yaml
     ---
     name: skill-name
     description: Brief description
     ---
     ```
   - `README.md` with quick start
   - `CHANGELOG.md` starting at v0.1.0

3. **Update marketplace.json**:
   - Add skill path to appropriate plugin category
   - If creating new category, add entire plugin object
   - Bump marketplace version (MINOR for new skills)

4. **Validate**:
   ```bash
   python3 .claude-plugin/validate-marketplace.py
   ```

5. **Update README.md**:
   - Add skill to appropriate category table
   - Update skill count
   - Update installation commands if new category

## Git Workflow

### Branch Naming

```
feature/component-name     # New skills or features
bugfix/component-name      # Bug fixes
chore/component-name       # Maintenance
docs/component-name        # Documentation
```

### Commit Conventions

**Use conventional commits:**
```bash
feat: Add new skill or feature
fix: Bug fixes
docs: Documentation updates
chore: Maintenance tasks
```

### Tagging Strategy

**Two tag namespaces:**

1. **Marketplace releases** (use `@` separator):
   ```bash
   marketplace@1.2.0
   ```

2. **Individual skill releases** (use `@` separator):
   ```bash
   skill-name@0.1.0
   ```

**Version bumping rules:**
- New skill → Marketplace MINOR bump (1.1.0 → 1.2.0)
- Skill update → Marketplace PATCH bump (1.2.0 → 1.2.1)
- Breaking change → Marketplace MAJOR bump (1.2.0 → 2.0.0)

## Lessons-Learned System

### Auto-Generated Insights

The `extract-explanatory-insights` hook automatically extracts `★ Insight` blocks from Claude Code responses when Explanatory output style is active.

**Categories** (in `docs/lessons-learned/`):
- architecture
- configuration
- context-management
- deployment
- devops
- general
- gitflow
- hooks-and-events
- performance
- react
- version-control

**Flow:**
1. Claude provides response with `★ Insight ─────────────────`
2. Hook triggers on Stop event
3. Bash script parses insight and category
4. Insight appended to `docs/lessons-learned/{category}/YYYY-MM-DD-*.md`

**These files are SOURCE MATERIAL for skills** - several skills reference insights as documentation.

## Development Commands

### Marketplace Operations

```bash
# Validate marketplace schema
python3 .claude-plugin/validate-marketplace.py

# Add marketplace (for users)
/plugin marketplace add cskiro/claudex

# Install plugin category
/plugin install category-name@claudex

# Update marketplace
/plugin marketplace update claudex
```

### Git Operations

```bash
# Create feature branch
git checkout -b feature/add-skill-name

# Conventional commit
git commit -m "feat: Add skill-name skill and category-name category"

# Tag marketplace release
git tag -a "marketplace@X.Y.Z" -m "Release marketplace X.Y.Z"
git push origin marketplace@X.Y.Z

# Tag skill release
git tag -a "skill-name@X.Y.Z" -m "Release skill-name X.Y.Z"
git push origin skill-name@X.Y.Z
```

### Python Skill Development

```bash
# Install dependencies for a skill
pip install -r skills/category/skill-name/requirements.txt

# Run skill script (varies by skill)
python3 skills/category/skill-name/scripts/main.py
```

## Critical Constraints

### DO NOT:
- ❌ Create `plugin.json` files in skill directories
- ❌ Run npm/TypeScript commands (this is not a Node.js project)
- ❌ Add ESLint or testing frameworks
- ❌ Start skill versions at 1.0.0 (use 0.1.0 for initial releases)
- ❌ Use `/v` or flat `v` tags (use `@` separator: `name@version`)
- ❌ Modify marketplace.json without validation

### ALWAYS:
- ✅ Validate with `python3 .claude-plugin/validate-marketplace.py`
- ✅ Follow conventional commit format
- ✅ Use semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Update README.md when adding skills
- ✅ Include frontmatter in SKILL.md
- ✅ Start new skills at version 0.1.0

## Skill Quality Standards

### SKILL.md Requirements

1. **Frontmatter** (required):
   ```yaml
   ---
   name: skill-name
   description: Clear description
   ---
   ```

2. **Sections** (recommended):
   - Overview
   - When to Use This Skill (trigger phrases)
   - Response Style
   - Workflow (phase-based approach)
   - Troubleshooting
   - Metadata

### Documentation Standards

- **Clear trigger phrases**: Show users how to invoke the skill
- **Executable workflows**: Phase-based, actionable steps
- **Real examples**: Include `examples/` directory with scenarios
- **Source attribution**: Link to insights or references if applicable

### Version Management

- **0.1.0** - Initial proof of concept
- **0.x.x** - Pre-release iterations
- **1.0.0** - Production-ready (rare, requires extensive testing)

## Marketplace Version History

Current version: **1.3.0** (as of 2025-11-23)

**Version timeline:**
- `marketplace@1.0.0` - Initial multi-feature marketplace
- `marketplace@1.1.0` - Added API Tools category (3 skills)
- `marketplace@1.1.1` - Hook schema fixes
- `marketplace@1.1.2` - Hook schema nested array fix
- `marketplace@1.1.3` - Anthropic schema alignment, **renamed `productivity-tools` → `claude-code-tools`**
- `marketplace@1.2.0` - Added Release Management category (1 skill)
- `marketplace@1.3.0` - Optimized skill context loading

**Plugin Renames:**
| Version | Old Name | New Name | Reason |
|---------|----------|----------|--------|
| 1.1.3 | `productivity-tools` | `claude-code-tools` | Better reflects ecosystem-focused purpose |

> **Migration Note:** Users with `productivity-tools@claudex` in their settings must update to `claude-code-tools@claudex`. See README.md Troubleshooting section.

**Total inventory:**
- 8 plugin categories
- 18 skills
- 1 hook
