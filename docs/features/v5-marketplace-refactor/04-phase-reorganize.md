# Phase 4: Reorganization (Optional)

## Objective

Based on overlap analysis, implement any necessary reorganization changes.

## Scope for v5.0.0

**Minimal changes** - Focus on restoration and stability, defer major reorganization to v6.0.0.

## Changes to Implement

### 1. Update Skill Descriptions

Ensure restored skills have clear "NOT for" sections:

#### codebase-auditor
```markdown
**NOT for:**
- Quick code reviews (use code-quality-reviewer agent instead)
- Single-file analysis
```

#### accessibility-audit
```markdown
**NOT for:**
- Full UI/UX design (use ui-ux-designer agent instead)
- Component creation
```

#### insight-skill-generator
```markdown
**NOT for:**
- Creating skills from scratch (use skill-creator instead)
- Skills without existing insight patterns
```

### 2. Update marketplace.json Descriptions

Ensure plugin descriptions differentiate from agents:

```json
{
  "name": "analysis-tools",
  "description": "Workflow-based code quality analysis with checklists and progressive disclosure. For quick reviews, use built-in agents instead.",
  ...
}
```

## Deferred to v6.0.0

| Change | Reason for Deferral |
|--------|---------------------|
| Merge insight-skill-generator into skill-creator | Requires workflow redesign |
| Consolidate single-skill plugins | Breaking change for users |
| Rename analysis-tools to code-quality | Breaking change |

## Implementation Checklist

- [ ] Update codebase-auditor SKILL.md with "NOT for" section
- [ ] Update accessibility-audit SKILL.md with "NOT for" section
- [ ] Update insight-skill-generator SKILL.md with "NOT for" section
- [ ] Review all restored skill descriptions for clarity
- [ ] Run validation after changes

## Validation

```bash
# Validate after each change
python3 scripts/validate-marketplace.py

# Test skill triggering
# (Manual testing in Claude Code)
```
