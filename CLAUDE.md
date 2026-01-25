# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Claudex is a **Claude Code marketplace** that distributes skills and hooks through a plugin-based architecture. This is NOT a traditional application codebase - it's a marketplace distribution system following Anthropic's official plugin schema.

### Architecture Model

```
marketplace.json (Single Source of Truth)
    ↓
1 Plugin (claudex) → 23 Skills + 1 Hook
    ↓
Each skill: SKILL.md (agent manifest) + supporting files
```

**Key Principle**: The `.claude-plugin/marketplace.json` file is the **single source of truth** for all marketplace metadata. Individual `plugin.json` files in skill directories are NOT used and should NOT be created.

## Repository Structure

Follows Anthropic's official `anthropics/skills` pattern with flat skill directories:

```
claudex/
├── .claude-plugin/
│   └── marketplace.json           # SINGLE SOURCE OF TRUTH
├── scripts/
│   ├── validate-marketplace.py    # Schema validation
│   └── validate-skills.py         # Skill quality validation
├── skills/                        # FLAT skill directory (Anthropic pattern)
│   ├── accessibility-audit/
│   ├── ascii-diagram-creator/
│   ├── benchmark-report-creator/
│   ├── bulletproof-react-auditor/
│   ├── cc-insights/
│   ├── claude-md-auditor/
│   ├── codebase-auditor/
│   ├── e2e-testing/
│   ├── git-worktree-setup/
│   ├── github-repo-setup/
│   ├── insight-skill-generator/
│   ├── json-outputs-implementer/
│   ├── mcp-server-creator/
│   ├── mutation-testing/
│   ├── otel-monitoring-setup/
│   ├── react-project-scaffolder/
│   ├── semantic-release-tagger/
│   ├── skill-creator/
│   ├── skill-isolation-tester/
│   ├── strict-tool-implementer/
│   ├── structured-outputs-advisor/
│   ├── sub-agent-creator/
│   └── test-driven-development/
├── hooks/
│   └── hooks.json                 # Hook registry
└── archive/                       # Archived skills (not in marketplace)
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

**IMPORTANT**: Do NOT create `plugin.json` files in skill directories. They are not required by Anthropic schema.

## Marketplace Integration

### marketplace.json Schema (Anthropic Pattern)

```json
{
  "name": "claudex",
  "metadata": {
    "version": "6.0.0"
  },
  "plugins": [
    {
      "name": "claudex",
      "description": "Complete skill suite: code quality, testing, API tools, DevOps, productivity",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/skill-name",
        ...
      ],
      "hooks": "./hooks/hooks.json"
    }
  ]
}
```

**Note**: All skills are in a single `claudex` plugin using `source: "./"`. This prevents the duplication issue where skills were copied across multiple plugin namespaces.

### Adding a New Skill

1. **Create skill directory** in flat skills folder:
   ```bash
   mkdir -p skills/skill-name
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
   - Add skill path to the `claudex` plugin's `skills` array
   - Bump marketplace version (MINOR for new skills)

4. **Validate**:
   ```bash
   python3 scripts/validate-marketplace.py
   ```

## Automation

### Sensei Agent

The Sensei Agent automates skill improvements based on evaluation feedback. It is triggered via GitHub issues with the `agent-ready` label.

**Workflow:**
1. Create issue with evaluation feedback containing `**Skill**: \`skill-name\``
2. Add `agent-ready` label
3. Agent reads feedback, improves skill, creates PR
4. Label changes to `agent-completed` on success

**Files:**
- `.github/workflows/run-sensei-agent.yml` - GitHub Actions workflow
- `scripts/automation/sensei_agent.py` - Python agent script
- `docs/automation/sensei-agent.md` - Full documentation

**Safety:**
- Writes restricted to `skills/*` directory only
- Max 20 turns before automatic stop
- Remove `agent-ready` label to cancel

**Testing locally:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python scripts/automation/sensei_agent.py \
  --issue 123 --repo owner/claudex --skill skill-name --dry-run
```

**Required secret:** `ANTHROPIC_API_KEY` must be configured in repository settings.

## Development Commands

### Validation

```bash
# Validate marketplace.json schema
python3 scripts/validate-marketplace.py

# Validate all skills against Anthropic spec
python3 scripts/validate-skills.py skills/

# Validate specific skill
python3 scripts/validate-skills.py skills/skill-name
```

**Expected output:** ✅ passed, ⚠️ warnings, or ❌ errors. Exit code 0 = valid.

### Git Operations

```bash
# Create feature branch
git checkout -b feature/add-skill-name

# Conventional commit
git commit -m "feat: Add skill-name skill"

# Tag marketplace release
git tag -a "marketplace@X.Y.Z" -m "Release marketplace X.Y.Z"
git push origin marketplace@X.Y.Z
```

## Critical Constraints

### DO NOT:
- ❌ Create `plugin.json` files in skill directories
- ❌ Run npm/TypeScript commands (this is not a Node.js project)
- ❌ Add ESLint or testing frameworks
- ❌ Start skill versions at 1.0.0 (use 0.1.0 for initial releases)
- ❌ Use `/v` or flat `v` tags (use `@` separator: `name@version`)
- ❌ Modify marketplace.json without validation
- ❌ Create nested skill directories (use flat `skills/` structure)
- ❌ Create multiple plugins (single `claudex` plugin only)

### ALWAYS:
- ✅ Validate with `python3 scripts/validate-marketplace.py`
- ✅ Follow conventional commit format
- ✅ Use semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Update README.md when adding skills
- ✅ Include frontmatter in SKILL.md
- ✅ Start new skills at version 0.1.0
- ✅ Follow Anthropic's flat skill directory pattern
- ✅ Add skills to the single `claudex` plugin

## Skill Quality Standards

### SKILL.md Requirements

1. **Frontmatter** (required):
   ```yaml
   ---
   name: skill-name
   description: Clear description (max 1024 chars)
   ---
   ```

2. **Name must match directory** (Anthropic spec requirement)

3. **Sections** (recommended):
   - Overview
   - When to Use This Skill (trigger phrases)
   - Response Style
   - Workflow (phase-based approach)

### Version Management

- **0.1.0** - Initial proof of concept
- **0.x.x** - Pre-release iterations
- **1.0.0** - Production-ready (rare, requires extensive testing)

## Marketplace Version History

Current version: **6.0.0**

### Version 6.0.0
- **BREAKING**: Consolidated from 10 plugins to single `claudex` plugin
- Fixes skill duplication issue (230 entries → 23 entries)
- Skills now use `claudex:skill-name` namespace
- Migration required: see `docs/MIGRATION.md`

### Version 5.0.0
- Restored archived skills
- 10 plugin categories with 23 skills

### Version 4.0.0
- Aligned with Anthropic's official `anthropics/skills` structure
- Flat `skills/` directory (no nested plugin directories)
- All plugins use `source: "./"` following Anthropic pattern

**Total inventory:**
- 1 plugin (claudex)
- 23 skills
- 1 hook
