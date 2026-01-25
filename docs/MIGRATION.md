# Migration Guide: v5.x to v6.0.0

## Overview

Version 6.0.0 consolidates the marketplace from 10 separate plugins into a single `claudex` plugin. This fixes the skill duplication bug where Claude Code was showing all 23 skills under each plugin namespace (230 entries instead of 23).

## Breaking Changes

| Change | Before (v5.x) | After (v6.0.0) |
|--------|---------------|----------------|
| Plugin count | 10 plugins | 1 plugin |
| Skill namespace | `api-tools:skill-name` | `claudex:skill-name` |
| Install command | Multiple `/plugin install` | Single `/plugin install claudex@claudex` |
| Total entries | 230 (10 × 23 duplicated) | 23 (no duplication) |

## Migration Steps

### Step 1: Uninstall Old Plugins

Run these commands in Claude Code:

```
/plugin uninstall api-tools@claudex
/plugin uninstall analysis-tools@claudex
/plugin uninstall claude-code-tools@claudex
/plugin uninstall meta-tools@claudex
/plugin uninstall testing-tools@claudex
/plugin uninstall devops-tools@claudex
/plugin uninstall release-management@claudex
/plugin uninstall planning-tools@claudex
/plugin uninstall benchmarking@claudex
/plugin uninstall productivity-hooks@claudex
```

### Step 2: Clear Plugin Cache

```bash
rm -rf ~/.claude/plugins/claudex*
rm -rf ~/.claude/skills-disabled/
```

### Step 3: Update Marketplace

```
/plugin marketplace update claudex
```

### Step 4: Install New Plugin

```
/plugin install claudex@claudex
```

### Step 5: Verify Installation

Run `/plugin` and verify:
- Only 23 skills appear (not 230)
- All skills use `claudex:` namespace
- No duplicate entries

## Skill Namespace Changes

All skills are now prefixed with `claudex:` instead of their old plugin name:

| Before (v5.x) | After (v6.0.0) |
|---------------|----------------|
| `api-tools:structured-outputs-advisor` | `claudex:structured-outputs-advisor` |
| `analysis-tools:codebase-auditor` | `claudex:codebase-auditor` |
| `claude-code-tools:cc-insights` | `claudex:cc-insights` |
| `meta-tools:skill-creator` | `claudex:skill-creator` |
| `testing-tools:e2e-testing` | `claudex:e2e-testing` |
| `devops-tools:github-repo-setup` | `claudex:github-repo-setup` |
| `release-management:semantic-release-tagger` | `claudex:semantic-release-tagger` |
| `planning-tools:ascii-diagram-creator` | `claudex:ascii-diagram-creator` |
| `benchmarking:benchmark-report-creator` | `claudex:benchmark-report-creator` |

## Team Configuration Update

Update `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claudex": {
      "source": {
        "source": "github",
        "repo": "cskiro/claudex"
      }
    }
  },
  "enabledPlugins": [
    "claudex@claudex"
  ]
}
```

**Remove** any old plugin references like:
- `api-tools@claudex`
- `analysis-tools@claudex`
- `claude-code-tools@claudex`
- etc.

## Troubleshooting

### Skills Still Duplicated

If you still see duplicated skills after migration:

1. Completely remove the marketplace:
   ```
   /plugin marketplace remove claudex
   ```

2. Clear all caches:
   ```bash
   rm -rf ~/.claude/plugins/claudex*
   rm -rf ~/.claude/marketplaces/claudex*
   ```

3. Re-add and reinstall:
   ```
   /plugin marketplace add cskiro/claudex
   /plugin install claudex@claudex
   ```

### Old Skills Still Appearing

If old namespaced skills (like `api-tools:skill-name`) still appear:

1. Check for stale entries in `~/.claude/plugins/installed_plugins.json`
2. Remove any claudex-related entries manually
3. Restart Claude Code

### Skills Not Loading

If skills fail to load after migration:

1. Verify the skill exists in the `skills/` directory
2. Check that `SKILL.md` has valid frontmatter
3. Run validation:
   ```bash
   python3 scripts/validate-skills.py skills/skill-name
   ```

## Rollback

If you need to rollback to v5.x:

1. Uninstall current plugin:
   ```
   /plugin uninstall claudex@claudex
   ```

2. Remove marketplace:
   ```
   /plugin marketplace remove claudex
   ```

3. Add marketplace at v5.0.0 tag:
   ```
   /plugin marketplace add cskiro/claudex@marketplace@5.0.0
   ```

4. Reinstall old plugins as needed.

## Why This Change?

Claude Code's plugin system copies the entire `source` directory for each plugin. When multiple plugins use `source: "./"`, the same skills directory gets copied multiple times. The `skills` array filtering wasn't being respected, causing all 23 skills to appear under each of the 10 plugin namespaces.

By consolidating to a single plugin, we ensure:
- Each skill appears exactly once
- No cache bloat from duplicate files
- Simpler installation and management
- Consistent `claudex:` namespace for all skills

## Questions?

Open an issue at [github.com/cskiro/claudex/issues](https://github.com/cskiro/claudex/issues).
