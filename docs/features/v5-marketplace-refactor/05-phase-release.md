# Phase 5: Release

## Objective

Release v5.0.0 with all restored skills and updated documentation.

## Pre-Release Checklist

### Code Changes
- [ ] All 7 skills restored to `skills/`
- [ ] `marketplace.json` updated with 10 plugins, 23 skills
- [ ] Version bumped to `5.0.0`
- [ ] Validation scripts pass

### Documentation
- [ ] `README.md` updated with new skill count
- [ ] `archive/README.md` updated to reflect restoration
- [ ] `CHANGELOG.md` updated with v5.0.0 changes
- [ ] Migration guide for v4.0.0 users added

### Testing
- [ ] All plugins install without errors
- [ ] No "Plugin not found" errors
- [ ] Skills trigger correctly

## Release Steps

### 1. Final Validation
```bash
python3 scripts/validate-marketplace.py
python3 scripts/validate-skills.py --all
```

### 2. Commit Changes
```bash
git add .
git commit -m "feat: Restore archived skills for v5.0.0 marketplace

- Restore 7 archived skills to skills/ directory
- Re-add analysis-tools, release-management, planning-tools, benchmarking plugins
- Add insight-skill-generator to meta-tools
- Bump marketplace version to 5.0.0
- Update documentation and migration guide

BREAKING CHANGE: None (backwards compatible with v3.0.0)

Fixes plugin errors for users upgrading from v3.0.0"
```

### 3. Create Pull Request
```bash
gh pr create --title "feat: v5.0.0 - Restore archived skills" --body "..."
```

### 4. After Merge - Create Release
```bash
git tag -a "marketplace@5.0.0" -m "Release v5.0.0 - Restored skills marketplace"
git push origin marketplace@5.0.0
gh release create marketplace@5.0.0 --title "v5.0.0 - Restored Skills" --notes "..."
```

## Release Notes Template

```markdown
# Claudex v5.0.0 - Restored Skills Marketplace

## What's New

This release restores all skills that were archived in v4.0.0, providing a comprehensive 23-skill marketplace.

### Restored Plugins
- **analysis-tools**: codebase-auditor, bulletproof-react-auditor, accessibility-audit
- **release-management**: semantic-release-tagger
- **planning-tools**: ascii-diagram-creator
- **benchmarking**: benchmark-report-creator
- **meta-tools**: Added insight-skill-generator

### Statistics
- **10 plugins** (up from 6)
- **23 skills** (up from 16)
- **1 hook**

## Upgrading

### From v4.0.0
No action required. Previously removed plugins are now available again.

### From v3.0.0
If you had plugin errors after v4.0.0, clear your cache and reinstall:

\`\`\`bash
rm -rf ~/.claude/plugins/cache/claudex
/plugin marketplace remove claudex
/plugin marketplace add cskiro/claudex
\`\`\`

## Full Changelog
- Restored 7 archived skills
- Re-added 4 removed plugins
- Updated marketplace.json to v5.0.0
- Added migration documentation
```

## Post-Release

- [ ] Verify release on GitHub
- [ ] Test fresh installation
- [ ] Update any external documentation
- [ ] Announce in relevant channels
