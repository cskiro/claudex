# Tag Creation Examples

Real-world tagging scenarios with complete commands and explanations.

---

## Scenario 1: First Release of a New Project

**Context**: You've built a new CLI tool and want to create the first release.

**Recommended Convention**: Flat tags (`vX.Y.Z`) since single component

**Steps**:

```bash
# 1. Verify no existing tags
git tag -l
# Output: (empty)

# 2. Choose version: 0.1.0 (initial public release)

# 3. Create annotated tag
git tag -a "v0.1.0" -m "Release v0.1.0 - Initial public release"

# 4. Verify tag
git show v0.1.0
# Shows tag metadata and commit details

# 5. Push tag to remote
git push origin v0.1.0

# 6. Create GitHub release
gh release create v0.1.0 \
  --title "CLI Tool v0.1.0" \
  --notes "Initial release with core functionality"
```

**Result**: Tag `v0.1.0` created and pushed, GitHub release published

---

## Scenario 2: Monorepo with Multiple Components (npm-style)

**Context**: Monorepo with marketplace, hooks, and skills. Using npm-style `@` separator.

**Recommended Convention**: `component@X.Y.Z`

**Steps**:

```bash
# 1. Check existing tags
git tag -l "marketplace@*" --sort=-v:refname | head -3
# Output:
# marketplace@1.1.0
# marketplace@1.0.0
# marketplace@0.1.0

# 2. Analyze changes since 1.1.0
git log marketplace@1.1.0..HEAD --oneline
# Shows: 2 commits with bug fixes

# 3. Determine version: 1.1.1 (PATCH bump for bug fixes)

# 4. Create annotated tag
git tag -a "marketplace@1.1.1" -m "Release marketplace 1.1.1"

# 5. Push tag
git push origin marketplace@1.1.1

# 6. Tag a hook in same repo
git tag -a "extract-insights@2.0.0" -m "Release extract-insights hook 2.0.0"
git push origin extract-insights@2.0.0
```

**Result**: Two components versioned independently in same repository

---

## Scenario 3: Monorepo with Multiple Components (slash-based)

**Context**: Monorepo with multiple services. Using slash-based namespaces.

**Recommended Convention**: `component/vX.Y.Z`

**Steps**:

```bash
# 1. List all hook tags
git tag -l "hook/*"
# Output:
# hook/user-auth/v1.0.0
# hook/logging/v0.5.0

# 2. Check latest logging hook version
git tag -l "hook/logging/*" --sort=-v:refname | head -1
# Output: hook/logging/v0.5.0

# 3. Analyze changes (added new feature)
git log hook/logging/v0.5.0..HEAD -- src/hooks/logging/

# 4. Determine version: 0.6.0 (MINOR bump for new feature)

# 5. Create tag
git tag -a "hook/logging/v0.6.0" -m "Release logging hook v0.6.0"

# 6. Push tag
git push origin hook/logging/v0.6.0

# 7. Set up CI/CD trigger (GitHub Actions)
cat << 'EOF' > .github/workflows/deploy-hook.yml
name: Deploy Hook
on:
  push:
    tags:
      - 'hook/*/v*'  # Trigger on any hook tag
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: echo "Deploying hook..."
EOF
```

**Result**: Logging hook versioned independently, CI/CD configured

---

## Scenario 4: Breaking Change Requiring MAJOR Bump

**Context**: API library with breaking changes (removed deprecated methods).

**Recommended Convention**: Flat tags (`vX.Y.Z`) for single-component library

**Steps**:

```bash
# 1. Check current version
git tag -l "v*" --sort=-v:refname | head -1
# Output: v2.3.5

# 2. Analyze changes (breaking: removed deprecated auth methods)
git log v2.3.5..HEAD --oneline --grep="BREAKING"
# Shows commits with breaking changes

# 3. Determine version: 3.0.0 (MAJOR bump)

# 4. Create tag
git tag -a "v3.0.0" -m "Release v3.0.0 - BREAKING: Removed deprecated auth methods"

# 5. Push tag
git push origin v3.0.0

# 6. Create GitHub release with migration guide
gh release create v3.0.0 \
  --title "v3.0.0 - Major Release" \
  --notes "$(cat <<'NOTES'
## Breaking Changes

- Removed deprecated `basicAuth()` method
- Replaced with `tokenAuth()` in all examples

## Migration Guide

**Before**:
```js
client.basicAuth(username, password)
```

**After**:
```js
client.tokenAuth(token)
```

See full migration guide in MIGRATION.md
NOTES
)"
```

**Result**: Major version bump with clear breaking change communication

---

## Scenario 5: Pre-release / Beta Version

**Context**: Testing new feature before official release.

**Recommended Convention**: Append pre-release identifier to semver

**Steps**:

```bash
# 1. Check current stable version
git tag -l "v*" --sort=-v:refname | grep -v "beta" | head -1
# Output: v1.5.0

# 2. Create beta tag
git tag -a "v1.6.0-beta.1" -m "Release v1.6.0-beta.1 - Testing new dashboard"

# 3. Push tag
git push origin v1.6.0-beta.1

# 4. Create pre-release on GitHub
gh release create v1.6.0-beta.1 \
  --title "v1.6.0-beta.1 (Pre-release)" \
  --notes "Beta release for testing new dashboard. Not production-ready." \
  --prerelease

# 5. After testing, create stable release
git tag -a "v1.6.0" -m "Release v1.6.0 - New dashboard (stable)"
git push origin v1.6.0
gh release create v1.6.0 \
  --title "v1.6.0" \
  --notes "Stable release with new dashboard feature"
```

**Result**: Beta version tested separately from stable releases

---

## Scenario 6: Automating Tag Creation from CI/CD

**Context**: Want to automatically create tags on PR merge to main.

**Recommended Convention**: Extract version from package.json or VERSION file

**Steps**:

```yaml
# .github/workflows/auto-tag.yml
name: Auto Tag on Merge
on:
  push:
    branches:
      - main
jobs:
  tag:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Fetch all tags

      - name: Get version from package.json
        id: version
        run: |
          VERSION=$(jq -r .version package.json)
          echo "version=v$VERSION" >> $GITHUB_OUTPUT

      - name: Check if tag exists
        id: check
        run: |
          if git rev-parse "${{ steps.version.outputs.version }}" >/dev/null 2>&1; then
            echo "exists=true" >> $GITHUB_OUTPUT
          else
            echo "exists=false" >> $GITHUB_OUTPUT
          fi

      - name: Create tag
        if: steps.check.outputs.exists == 'false'
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git tag -a "${{ steps.version.outputs.version }}" \
            -m "Release ${{ steps.version.outputs.version }}"
          git push origin "${{ steps.version.outputs.version }}"

      - name: Create GitHub release
        if: steps.check.outputs.exists == 'false'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh release create "${{ steps.version.outputs.version }}" \
            --title "${{ steps.version.outputs.version }}" \
            --generate-notes
```

**Result**: Tags automatically created when version bumped in package.json

---

## Scenario 7: Filtering and Listing Tags

**Context**: Need to find specific tags or latest versions.

**Commands**:

```bash
# List all tags
git tag -l

# List tags with pattern (marketplace only)
git tag -l "marketplace@*"

# List tags sorted by version (latest first)
git tag -l "v*" --sort=-v:refname

# Get latest marketplace version
git tag -l "marketplace@*" --sort=-v:refname | head -1

# Extract version number only
git tag -l "marketplace@*" --sort=-v:refname | head -1 | cut -d'@' -f2

# List tags with commit messages
git tag -l -n1 "v*"

# Find all tags containing a specific commit
git tag --contains abc123

# List tags created in last week
git log --tags --simplify-by-decoration --pretty="format:%ai %d" | grep "tag:" | head -n 7
```

---

## Scenario 8: Fixing a Mistake (Deleting and Recreating Tag)

**Context**: Created tag on wrong commit, need to fix.

**⚠️ WARNING**: Only do this if tag not yet pushed or used by others!

**Steps**:

```bash
# 1. Delete local tag
git tag -d v1.0.0

# 2. If already pushed (coordinate with team first!)
git push origin :refs/tags/v1.0.0

# 3. Create tag on correct commit
git tag -a v1.0.0 abc123 -m "Release v1.0.0"

# 4. Push corrected tag
git push origin v1.0.0

# 5. Force-push if needed (DANGEROUS)
git push origin v1.0.0 --force
```

**Prevention**: Always verify commit before pushing tags!

---

## Quick Reference Commands

```bash
# Create annotated tag
git tag -a "v1.0.0" -m "Release v1.0.0"

# Create tag on specific commit
git tag -a "v1.0.0" abc123 -m "Release v1.0.0"

# Push single tag
git push origin v1.0.0

# Push all tags (use cautiously)
git push origin --tags

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# List tags sorted
git tag -l --sort=-v:refname

# Show tag details
git show v1.0.0

# Latest tag for pattern
git tag -l "marketplace@*" --sort=-v:refname | head -1

# Create GitHub release from tag
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes"
```
