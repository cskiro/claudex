# Archived Skills

Skills archived during toolset consolidation. These files are kept for reference but are no longer active.

**Archived:** 2025-12-13
**Reason:** Toolset overlap reduction per TOOLSET-OVERLAP-ANALYSIS.md

## Archived Skills

| Skill | Reason | Replacement |
|-------|--------|-------------|
| codebase-auditor | Covered by code-quality-reviewer agent | Agent does deeper analysis |
| bulletproof-react-auditor | Niche, low expected usage | General architecture guidance |
| accessibility-audit | Overlaps with ui-component-designer | Skill covers a11y specs |
| benchmark-report-creator | Niche, low expected usage | Manual documentation |
| ascii-diagram-creator | Built into rules (01-universal.md) | Rules provide guidance |
| insight-skill-generator | Overlaps with skill-creator | skill-creator is canonical |
| semantic-release-tagger | Niche, native git/npm handles this | Native tooling |

## Restoration

To restore an archived skill:

1. Move the skill folder back to `skills/{category}/`
2. Update `.claude-plugin/marketplace.json` to include the skill path
3. Clear plugin cache: `rm -rf ~/.claude/plugins/cache/claudex`
4. Restart Claude Code
