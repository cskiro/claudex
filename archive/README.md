# Archive

This directory contains archived or deprecated content.

## v5.0.0 Update

**All previously archived skills have been restored** to the main `skills/` directory as of v5.0.0.

### Restoration Summary

The following skills that were archived in v4.0.0 are now active again:

| Skill | Plugin | Status |
|-------|--------|--------|
| codebase-auditor | analysis-tools | ✅ Restored |
| bulletproof-react-auditor | analysis-tools | ✅ Restored |
| accessibility-audit | analysis-tools | ✅ Restored |
| benchmark-report-creator | benchmarking | ✅ Restored |
| ascii-diagram-creator | planning-tools | ✅ Restored |
| insight-skill-generator | meta-tools | ✅ Restored |
| semantic-release-tagger | release-management | ✅ Restored |

### Why Restored?

The v4.0.0 archival caused plugin errors for users with existing installations. Analysis showed:
- Only 1 of 7 archived skills had a true replacement
- 3 skills had subagent "replacements" with different invocation models
- 3 skills had no replacement at all

v5.0.0 restores all skills to provide a comprehensive 23-skill marketplace while maintaining the flat directory structure introduced in v4.0.0.

## Archive Contents

This directory may contain:
- Old documentation
- Deprecated configurations
- Historical reference materials

## Related

- [v5 Refactor Documentation](../docs/features/v5-marketplace-refactor/)
- [marketplace.json](../.claude-plugin/marketplace.json)
