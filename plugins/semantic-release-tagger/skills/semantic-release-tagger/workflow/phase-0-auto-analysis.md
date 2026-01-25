# Phase 0: Auto-Context Analysis

**Purpose**: Gather repository state without user interaction to provide intelligent recommendations.

**Steps** (execute immediately when skill activates):

## 1. Detect Repository Structure

```bash
# Check if git repository
git rev-parse --git-dir 2>/dev/null

# List all tags sorted by version
git tag -l --sort=-v:refname

# Count unique tag patterns
git tag -l | grep -E '@|/' | wc -l
```

## 2. Identify Existing Convention

- Parse tag patterns: Look for `@`, `/v`, or flat `v` patterns
- Detect most common convention (majority wins)
- Flag inconsistencies if multiple patterns found

Example output:
```
✅ Detected convention: npm-style @ separator
📊 Tags analyzed: 15
⚠️  Found inconsistency: 2 tags use /v separator (outdated)
```

## 3. Parse Latest Versions Per Component (if monorepo)

```bash
# For @ convention
git tag -l | grep '@' | cut -d'@' -f1 | sort -u

# For each component, get latest version
for component in $(git tag -l | grep '@' | cut -d'@' -f1 | sort -u); do
  git tag -l "${component}@*" --sort=-v:refname | head -1
done
```

## 4. Analyze Commits Since Last Tag

```bash
# Get latest tag for component (or overall)
LAST_TAG=$(git tag -l "marketplace@*" --sort=-v:refname | head -1)

# Get commits since last tag
git log ${LAST_TAG}..HEAD --oneline --format="%s"
```

## 5. Classify Changes Using Conventional Commits

- Parse commit prefixes: `feat:`, `fix:`, `chore:`, `BREAKING CHANGE:`
- Determine version bump type:
  - BREAKING CHANGE or `!` suffix → MAJOR
  - `feat:` → MINOR
  - `fix:` or `chore:` → PATCH
- Count commits by type for changelog

## 6. Calculate Recommended Next Version

```
Current: marketplace@1.1.3
Commits: 1 chore (README update)
Type: PATCH bump
Recommended: marketplace@1.1.4
```

## 7. Present Findings to User

```
📦 Repository Analysis:
- Convention: @ separator (npm-style)
- Latest tag: marketplace@1.1.3
- Commits since tag: 1
  • chore: Update README.md
- Change classification: PATCH (documentation only)

💡 Recommendation: marketplace@1.1.4

Proceed with tag creation? [Yes/No/Customize]
```

## Output

Complete repository context analysis with version recommendation.

## Common Issues

- **No existing tags**: Recommend starting at `component@0.1.0`
- **Mixed conventions**: Warn and recommend migration path
- **No conventional commits**: Fall back to user-guided version selection
