---
description: Show active profiles and installed rules
argument-hint: [profile-name]
---

You are the swe-standards profile command. Show the user their active profiles and which rules are installed for each.

## Context

Rules are installed at `~/.claude/rules/swe-standards/` and tracked via a manifest at `~/.claude/swe-standards.json`. The upstream source rules live at `${CLAUDE_PLUGIN_ROOT}/rules/`.

## Profile Definitions

**Core**: 00-core.md, xp-principles.md, git-branching.md, git-flow-narrative.md, visual-documentation.md
**TypeScript**: typescript.md, vitest-cpu-protection.md
**Python**: python.md
**Testing**: testing.md, vitest-cpu-protection.md
**Quality**: pr-review-toolkit-workflow.md, code-simplifier-workflow.md, docs-check-workflow.md
**Security**: security.md

## Execution Steps

### If No Arguments

Show all installed profiles with their rules:

1. Read `~/.claude/swe-standards.json` manifest
2. If manifest doesn't exist, report not installed and suggest `/swe-standards:init`
3. For each active profile, list the rules with status:

```
Active Profiles
===============

Core (5 rules)
  ✅ 00-core.md
  ✅ xp-principles.md
  ✅ git-branching.md
  ⚠️  git-flow-narrative.md (modified locally)
  ✅ visual-documentation.md

TypeScript (2 rules)
  ✅ typescript.md
  ✅ vitest-cpu-protection.md

Testing (2 rules)
  ✅ testing.md
  ✅ vitest-cpu-protection.md (shared with TypeScript)

Quality (3 rules)
  ✅ pr-review-toolkit-workflow.md
  ✅ code-simplifier-workflow.md
  ✅ docs-check-workflow.md

Inactive Profiles: Python, Security
```

### If Profile Name Provided ($ARGUMENTS)

Show detailed information about the specific profile:

1. Map $ARGUMENTS to a profile name (case-insensitive)
2. List all rules in that profile with:
   - Installation status (installed / not installed)
   - Modification status (original / modified)
   - Brief description of what the rule covers
3. If the profile is not installed, show what it would add and suggest:
   ```
   To add this profile, run: /swe-standards:init <profile-name>
   ```

### Available Profiles Summary

Also show available profiles that aren't currently installed, with a brief description of what each provides, so the user can decide whether to add them.
