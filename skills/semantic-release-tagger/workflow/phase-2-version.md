# Phase 2: Determine Version Number

**Purpose**: Calculate the correct semantic version number following SemVer rules.

## Steps

### 1. Understand Semantic Versioning Format

`MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward-compatible additions
- **PATCH**: Bug fixes, backward-compatible fixes

### 2. Identify the Current Version

- Find latest tag: `git tag -l "component@*" --sort=-v:refname | head -1`
- If no tags exist, start at `0.1.0` (not `1.0.0`)
- Why `0.1.0`? Signals "initial public release, not production-ready"

### 3. Analyze Changes Since Last Tag

- Review commits: `git log <last-tag>..HEAD --oneline`
- Check for:
  - Breaking changes (MAJOR bump)
  - New features (MINOR bump)
  - Bug fixes only (PATCH bump)

### 4. Apply Version Bump Rules

| Change Type | Current | New Version |
|-------------|---------|-------------|
| Breaking change | `1.2.3` | `2.0.0` |
| New feature | `1.2.3` | `1.3.0` |
| Bug fix | `1.2.3` | `1.2.4` |
| First release | N/A | `0.1.0` |
| Production ready | `0.x.x` | `1.0.0` |

### 5. Special Version Bump Scenarios

- **Pre-1.0.0 versions**: Breaking changes still bump MINOR (0.2.0 → 0.3.0)
- **Multiple change types**: Use highest severity (feature + bug fix → MINOR)
- **No changes**: Don't create a tag (wait for actual changes)

### 6. Validate Version Number

- Confirm version doesn't already exist: `git tag -l "component@X.Y.Z"`
- Ensure version is higher than latest: `X.Y.Z > current version`

## Output

Calculated semantic version number ready for tagging.

## Common Issues

- **Starting at 1.0.0**: Reserve for production-ready releases. Use 0.1.0 for initial releases.
- **Skipping versions**: Don't skip (e.g., 1.0.0 → 1.2.0). Increment by 1 only.
- **Inconsistent component versioning**: Component version ≠ internal script version.
