# Phase 1: Restore Archived Skills

## Objective

Move all 7 archived skills from `archive/skills/` to the flat `skills/` directory.

## Skills to Restore

| Skill | Source Location | Target Location |
|-------|-----------------|-----------------|
| codebase-auditor | `archive/skills/codebase-auditor/` | `skills/codebase-auditor/` |
| bulletproof-react-auditor | `archive/skills/bulletproof-react-auditor/` | `skills/bulletproof-react-auditor/` |
| accessibility-audit | `archive/skills/accessibility-audit/` | `skills/accessibility-audit/` |
| benchmark-report-creator | `archive/skills/benchmark-report-creator/` | `skills/benchmark-report-creator/` |
| ascii-diagram-creator | `archive/skills/ascii-diagram-creator/` | `skills/ascii-diagram-creator/` |
| insight-skill-generator | `archive/skills/insight-skill-generator/` | `skills/insight-skill-generator/` |
| semantic-release-tagger | `archive/skills/semantic-release-tagger/` | `skills/semantic-release-tagger/` |

## Steps

1. [ ] Verify archive structure exists
2. [ ] Move each skill directory to `skills/`
3. [ ] Verify SKILL.md exists in each restored skill
4. [ ] Update `archive/README.md` to reflect restoration

## Commands

```bash
# Move skills from archive to skills/
mv archive/skills/codebase-auditor skills/
mv archive/skills/bulletproof-react-auditor skills/
mv archive/skills/accessibility-audit skills/
mv archive/skills/benchmark-report-creator skills/
mv archive/skills/ascii-diagram-creator skills/
mv archive/skills/insight-skill-generator skills/
mv archive/skills/semantic-release-tagger skills/

# Verify restoration
ls -la skills/
```

## Validation

- [ ] All 7 skills directories exist in `skills/`
- [ ] Each skill has a valid `SKILL.md` file
- [ ] No broken symlinks or missing files
