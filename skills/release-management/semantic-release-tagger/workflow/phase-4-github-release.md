# Phase 4: Create GitHub Release

**Purpose**: Create user-friendly GitHub release with auto-generated changelog from commits.

## Steps

### 1. Check if GitHub CLI is Available

```bash
# Verify gh CLI installed
gh --version

# Check authentication
gh auth status
```

### 2. Auto-generate Changelog from Commits

```bash
# Get commits between tags
git log marketplace@1.1.3..marketplace@1.1.4 --oneline --format="- %s"

# Group by conventional commit type
# feat: → ### Features
# fix: → ### Bug Fixes
# chore: → ### Maintenance
```

Example generated changelog:
```markdown
## What's Changed

### Maintenance
- chore: Update README.md with new examples

**Full Changelog**: https://github.com/user/repo/compare/marketplace@1.1.3...marketplace@1.1.4
```

### 3. Present Release Preview to User

```
📋 GitHub Release Preview:

Tag: marketplace@1.1.4
Title: "Marketplace v1.1.4"
Pre-release: No (version >= 1.0.0)

Changelog (auto-generated):
### Maintenance
- chore: Update README.md with new examples

Create GitHub release now? [Yes/No/Edit changelog]
```

### 4. Execute Release Creation (after confirmation)

```bash
# Determine if pre-release (version < 1.0.0)
PRERELEASE_FLAG=""
if [[ "1.1.4" =~ ^0\. ]]; then
  PRERELEASE_FLAG="--prerelease"
fi

# Create release with auto-generated notes
gh release create marketplace@1.1.4 \
  --title "Marketplace v1.1.4" \
  --notes "$(cat /tmp/changelog.md)" \
  ${PRERELEASE_FLAG}
```

### 5. Verify Release Created

```bash
# Check release exists
gh release view marketplace@1.1.4

# Get release URL
gh release view marketplace@1.1.4 --json url -q .url
```

### 6. Present Success Confirmation

```
✅ GitHub Release created successfully!

Release: marketplace@1.1.4
URL: https://github.com/user/repo/releases/tag/marketplace@1.1.4
Pre-release: No
Published: Yes
Notifications: Sent to watchers

Next steps:
- View release on GitHub: [Open URL]
- Tag another component? [Yes/No]
- Done
```

## Output

GitHub release published with auto-generated changelog.

## Automation Features

- ✅ **Auto-generated changelog**: Parsed from conventional commits
- ✅ **Smart pre-release detection**: Versions < 1.0.0 marked as pre-release
- ✅ **gh CLI integration**: One-command release creation
- ✅ **Changelog grouping**: Commits grouped by type (feat/fix/chore)
- ✅ **Full changelog link**: Comparison URL auto-included

## Common Issues

- **gh CLI not installed**: Warn user, provide installation instructions, fallback to web UI
- **Not authenticated**: Guide user through `gh auth login`
- **Empty changelog**: Use default message "Release vX.Y.Z" if no conventional commits
