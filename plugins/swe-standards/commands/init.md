---
description: Guided first-time setup — detects project type, selects profiles, scaffolds rules
argument-hint: [profile-names...]
---

You are the swe-standards initialization command. Help the user set up engineering standards for their Claude Code environment.

## Context

The swe-standards plugin provides 12 engineering rule files organized into 6 profiles. Rules are scaffolded to `~/.claude/rules/swe-standards/` where Claude Code auto-loads them natively.

The plugin source rules live at: `${CLAUDE_PLUGIN_ROOT}/rules/`

## Profile Definitions

Each profile includes specific rule files:

**Core** (always included):
- `core/core.md` — Fail-fast, no silent failures, conventional commits
- `core/xp-principles.md` — Kent Beck's 16 XP principles
- `methodology/git-branching.md` — Branch naming and workflow
- `methodology/git-flow-narrative.md` — Narrative commit/PR templates
- `domain/visual-documentation.md` — ASCII diagram standards

**TypeScript**:
- `language/typescript.md` — Strict types, React patterns, naming

**Python**:
- `language/python.md` — Type hints, Black/Ruff/mypy, Google docstrings

**Testing**:
- `methodology/testing.md` — TDD red-green-refactor, Testing Trophy

**Quality**:
- `quality/pr-review-toolkit-workflow.md` — 6 specialized review agents
- `quality/code-simplifier-workflow.md` — Final pre-PR quality gate
- `quality/docs-check-workflow.md` — Documentation freshness

**Security**:
- `domain/security.md` — OWASP Top 10, auth patterns, secrets management

## Execution Steps

### Step 1: Detect Project Type

Look in the current working directory for:
- `tsconfig.json` or `*.ts` files → suggest TypeScript profile
- `pyproject.toml`, `setup.py`, `requirements.txt`, or `*.py` files → suggest Python profile
- `vitest.config.*` or `jest.config.*` or test directories → suggest Testing profile
- `package.json` → check for relevant dependencies
- `.github/workflows/` → suggest Quality profile
- Auth/security related directories → suggest Security profile

### Step 2: Present Profile Selection

If the user provided arguments ($ARGUMENTS), use those as pre-selected profiles. Otherwise, present the detection results and recommend profiles.

Always include Core. Recommend additional profiles based on detection:
- TypeScript project detected → Core + TypeScript + Testing + Quality
- Python project detected → Core + Python + Testing + Quality
- Both detected → Core + TypeScript + Python + Testing + Quality

Ask the user to confirm or adjust the selection.

### Step 3: Scaffold Rules

For each selected profile, copy the rule files:

1. Create directory `~/.claude/rules/swe-standards/` if it doesn't exist
2. For each rule file in the selected profiles:
   - Read source from `${CLAUDE_PLUGIN_ROOT}/rules/<path>`
   - Write to `~/.claude/rules/swe-standards/<filename>`
   - Note: Flatten the directory structure — all rules go directly in `swe-standards/` (Claude Code loads all `.md` files in rules subdirectories)

### Step 4: Write Manifest

Create `~/.claude/swe-standards.json` with:

```json
{
  "version": "0.1.0",
  "installed_at": "<ISO timestamp>",
  "updated_at": "<ISO timestamp>",
  "profiles": ["core", "typescript", "testing", "quality"],
  "files": {
    "core.md": {
      "source": "core/core.md",
      "profile": "core",
      "hash": "<md5 hash of file contents>"
    }
  }
}
```

Compute MD5 hash for each file with: `md5 -q <file>` (macOS) or `md5sum <file>` (Linux).

### Step 5: Check Dependencies

If the user selected the **Quality** profile, check if `pr-review-toolkit` is installed (it's an external Anthropic plugin, not part of claudex). The Quality profile's rules reference its 6 specialized review agents.

- If not installed, inform the user: "The Quality profile references pr-review-toolkit agents. Install it from Anthropic's plugin marketplace for the full experience."
- Do not block installation — the rules still work as guidance even without the agents.

If the user selected any profile, check if `adr-generator` is installed (it IS in the claudex marketplace):
- If not installed, suggest: `/plugin install adr-generator@claudex`

### Step 6: Confirm Success

Show the user:
- Number of rules installed
- Profiles activated
- Path where rules were scaffolded
- Any missing dependencies noted above
- Suggest running `/swe-standards:check` to verify
- Remind them to start a new Claude Code session for rules to take effect

## Important Notes

- Never overwrite existing rules without asking — if `~/.claude/rules/swe-standards/` already exists, ask if they want to re-initialize
- If a manifest already exists, warn that this will reset their installation
- Core profile is mandatory and cannot be deselected
