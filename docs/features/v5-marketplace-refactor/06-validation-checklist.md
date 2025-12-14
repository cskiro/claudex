# v5.0.0 Validation Checklist

Complete validation guide for the v5.0.0 marketplace release.

## Automated Validation

### 1. Run Pre-Release Check Suite

```bash
# Full validation
python3 scripts/pre-release-check.py

# Quick validation (skip slow checks)
python3 scripts/pre-release-check.py --quick

# Verbose output
python3 scripts/pre-release-check.py --verbose
```

**Expected Output:**
- All 13 automated checks pass
- Marketplace validation passes (10 plugins, 23 skills)
- Skills validation passes (23/23, 97%+ average)

### 2. Individual Validation Scripts

```bash
# Marketplace schema validation
python3 scripts/validate-marketplace.py

# Skills quality validation
python3 scripts/validate-skills.py skills/

# Validate specific skill
python3 scripts/validate-skills.py skills/codebase-auditor --verbose
```

---

## Manual Validation

### Phase 1: Fresh Installation Test

**Purpose:** Verify clean installation has no errors.

```bash
# 1. Clear plugin cache
rm -rf ~/.claude/plugins/cache/claudex

# 2. Remove marketplace
# In Claude Code: /plugin marketplace remove claudex

# 3. Reinstall marketplace
# In Claude Code: /plugin marketplace add cskiro/claudex
```

**Verify:**
- [ ] No "plugin not found" errors
- [ ] No "skill not found" errors
- [ ] Installation completes successfully

### Phase 2: Plugin Menu Verification

**Purpose:** Verify all plugins appear correctly.

```
In Claude Code: /plugin
```

**Verify all 10 plugins appear:**
- [ ] `api-tools` (3 skills)
- [ ] `analysis-tools` (3 skills) ← RESTORED
- [ ] `claude-code-tools` (5 skills)
- [ ] `meta-tools` (3 skills)
- [ ] `testing-tools` (3 skills)
- [ ] `devops-tools` (3 skills)
- [ ] `release-management` (1 skill) ← RESTORED
- [ ] `planning-tools` (1 skill) ← RESTORED
- [ ] `benchmarking` (1 skill) ← RESTORED
- [ ] `productivity-hooks` (1 hook)

**Total:** 10 plugins, 23 skills, 1 hook

### Phase 3: Restored Skill Triggering

**Purpose:** Verify restored skills trigger correctly with semantic matching.

| Test Prompt | Expected Skill | Pass |
|-------------|----------------|------|
| "audit my codebase for issues" | codebase-auditor | [ ] |
| "check React best practices" | bulletproof-react-auditor | [ ] |
| "audit accessibility of my app" | accessibility-audit | [ ] |
| "create an ASCII diagram" | ascii-diagram-creator | [ ] |
| "create a semantic release tag" | semantic-release-tagger | [ ] |
| "create a benchmark report" | benchmark-report-creator | [ ] |
| "generate a skill from insights" | insight-skill-generator | [ ] |

### Phase 4: Existing Skill Regression Test

**Purpose:** Verify v4.0.0 skills still work correctly.

| Test Prompt | Expected Skill | Pass |
|-------------|----------------|------|
| "set up e2e testing" | e2e-testing | [ ] |
| "create a new skill" | skill-creator | [ ] |
| "set up TDD" | test-driven-development | [ ] |
| "create a React project" | react-project-scaffolder | [ ] |
| "audit my CLAUDE.md" | claude-md-auditor | [ ] |

### Phase 5: Anthropic Alignment Verification

**Purpose:** Ensure structure matches Anthropic's official patterns.

```bash
# Compare with official Anthropic skills repo
gh repo view anthropics/skills --json defaultBranchRef

# Check structure alignment
ls -la skills/                    # Should be flat (no nested categories)
cat .claude-plugin/marketplace.json | jq '.plugins[].source' # All should be "./"
```

**Verify:**
- [ ] Flat `skills/` directory (no nested categories)
- [ ] All plugins use `source: "./"`
- [ ] `marketplace.json` at `.claude-plugin/marketplace.json`
- [ ] Each skill has `SKILL.md` with frontmatter

---

## Validation Report Template

After completing all checks, document results:

```markdown
## v5.0.0 Validation Report

**Date:** YYYY-MM-DD
**Validator:** [Name]

### Automated Checks
- [ ] pre-release-check.py: PASS/FAIL
- [ ] validate-marketplace.py: PASS/FAIL
- [ ] validate-skills.py: PASS/FAIL (Score: __%)

### Manual Checks
- [ ] Fresh installation: PASS/FAIL
- [ ] Plugin menu (10 plugins): PASS/FAIL
- [ ] Restored skills trigger: __/7 PASS
- [ ] Existing skills regression: __/5 PASS
- [ ] Anthropic alignment: PASS/FAIL

### Issues Found
1. [Issue description]
2. [Issue description]

### Sign-off
- [ ] Ready for release
```

---

## Rollback Plan

If critical issues are found after release:

```bash
# 1. Revert to previous version
git revert HEAD
git push origin main

# 2. Users can clear cache
rm -rf ~/.claude/plugins/cache/claudex

# 3. Reinstall previous version
/plugin marketplace remove claudex
/plugin marketplace add cskiro/claudex@4.0.0  # If tag exists
```

---

## Success Criteria

All of the following must be true before release:

1. **Zero errors** in automated validation
2. **Fresh installation** completes without errors
3. **All 10 plugins** appear in `/plugin` menu
4. **All 7 restored skills** trigger correctly
5. **No regressions** in existing v4.0.0 skills
6. **Follows Anthropic patterns** (flat structure, root source)
