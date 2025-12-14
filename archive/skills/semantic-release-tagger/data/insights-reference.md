# Insights Reference - Git Tagging & Versioning Strategy

This document consolidates all source insights used to generate the git-tagging-strategy skill.

## Overview

- **Total Insights**: 7
- **Date Range**: 2025-11-14 to 2025-11-15
- **Categories**: version-control
- **Sessions**: 3 unique sessions
- **Source Directory**: `docs/lessons-learned/version-control/`

---

## Insight 1: Semantic Git Tagging Strategy

**Source**: `2025-11-14-semantic-git-tagging-strategy.md`
**Session**: 63c56792-8274-4f35-8800-0f7ed2fe422a
**Date**: 2025-11-14

### Content

Using hierarchical tag namespaces (`marketplace/v1.0.0`, `hook/{name}/v2.1.0`) provides semantic organization for multi-component repositories:

**Benefits**:
1. **Component-specific versioning** - Each component can evolve independently
2. **Clear ownership** - Tag prefix indicates what's being versioned
3. **Git tag filtering** - `git tag -l "hook/*"` lists all hook versions
4. **Release automation** - CI/CD can trigger on specific tag patterns

**Convention**:
- `marketplace/vX.Y.Z` - Overall marketplace/plugin structure version
- `hook/{name}/vX.Y.Z` - Individual hook versions
- `skill/{name}/vX.Y.Z` - Individual skill versions
- `agent/{name}/vX.Y.Z` - Individual agent versions

This scales better than flat versioning (`v1.0.0`, `v2.0.0`) in monorepos with multiple independently-versioned components.

### Skill Integration

- **Phase 1**: Informs slash-based namespace option
- **Phase 5**: Provides tag filtering examples

---

## Insight 2: NPM-Style Git Tagging Convention

**Source**: `2025-11-14-npm-style-git-tagging-convention.md`
**Session**: 63c56792-8274-4f35-8800-0f7ed2fe422a
**Date**: 2025-11-14

### Content

Using `@` instead of `/v` for version separators (`package@1.0.0` vs `package/v1.0.0`) aligns with npm's scoped package convention and provides cleaner semantics:

**Advantages of `@` convention**:
1. **npm familiarity** - Developers recognize `@scope/package@version` pattern
2. **Cleaner URLs** - `tag/marketplace@1.0.0` vs `tag/marketplace/v1.0.0`
3. **Semantic clarity** - `@` clearly separates name from version
4. **Path safety** - No confusion with directory separators

**Version numbering**:
- Start at `0.1.0` for initial public releases (not 1.0.0 or 2.1.0)
- Component version ≠ internal script version
- Follows semver: MAJOR.MINOR.PATCH

The `v` prefix is optional with `@` convention since the separator itself indicates versioning, keeping tags minimal and readable.

### Skill Integration

- **Phase 1**: Informs npm-style @ separator option
- **Phase 2**: Provides version numbering guidance (start at 0.1.0)

---

## Insight 3: Git Tags vs GitHub Releases

**Source**: `2025-11-14-git-tags-vs-github-releases-git-tags-are-lightweig.md`
**Session**: 1b1069bf-67be-45a3-ae42-dc32fd30d2ee
**Date**: 2025-11-14

### Content

Git tags are lightweight version markers in your repository history, while GitHub releases are feature-rich with changelog generation, asset uploads, and notification systems. Tags are required for releases, but releases add discoverability and user-friendly documentation on the GitHub interface.

**Tag Naming Convention**: Using `v1.1.1` (with v prefix) is a common convention that distinguishes version tags from other tags, though your existing releases use `marketplace@1.1.0` format for namespace clarity.

### Skill Integration

- **Phase 4**: Explains git tags vs GitHub releases trade-offs
- **Important Reminders**: "Git tags ≠ GitHub releases"

---

## Insight 4: Namespace Tag Conventions

**Source**: `2025-11-14-namespace-tag-conventions-the-marketplacexyz-forma.md`
**Session**: 1b1069bf-67be-45a3-ae42-dc32fd30d2ee
**Date**: 2025-11-14

### Content

The `marketplace@X.Y.Z` format provides namespace clarity in monorepos or multi-component projects, making it immediately clear which part of the system the version applies to. This is especially valuable when a repository might have multiple releasable components (marketplace, CLI tools, libraries, etc.).

### Skill Integration

- **Phase 1**: Reinforces namespace clarity benefit
- **Troubleshooting**: "Monorepo tags confusing" section

---

## Insight 5: Semantic Versioning

**Source**: `2025-11-14-semantic-versioning-the-patch-version-bump-110-111.md`
**Session**: 1b1069bf-67be-45a3-ae42-dc32fd30d2ee
**Date**: 2025-11-14

### Content

The patch version bump (1.1.0 → 1.1.1) correctly signals a bug fix release per SemVer conventions. This communicates to users that the changes are backward-compatible fixes without new features or breaking changes.

**PR Workflow**: Pushing additional commits to a PR branch automatically updates the PR and triggers CI re-runs if configured, enabling iterative refinement before merge.

### Skill Integration

- **Phase 2**: Provides semantic versioning rules and examples
- **Version bump table**: PATCH example (1.2.3 → 1.2.4)

---

## Insight 6: Fast-Forward Merges

**Source**: `2025-11-15-fast-forward-merges-the-fast-forward-message-indic.md`
**Session**: 1b1069bf-67be-45a3-ae42-dc32fd30d2ee
**Date**: 2025-11-15

### Content

The "Fast-forward" message indicates GitHub merged these PRs by moving the main branch pointer forward without creating merge commits, keeping a linear history. This happens when the PR branch is directly ahead of main with no conflicting changes.

### Skill Integration

- **Phase 5**: Fast-forward merge awareness
- **Important Reminders**: "Fast-forward merges preserve history"

---

## Insight 7: Tagging Convention

**Source**: `2025-11-14-tagging-convention-your-versioning-follows-a-clear.md`
**Session**: 43c2ed05-2280-4184-ae3d-27a30297634d
**Date**: 2025-11-14

### Content

Your versioning follows a clear pattern:
- Marketplace: `marketplace@<semver>`
- Skills: `<skill-name>@<semver>`

This enables independent versioning of skills while tracking the overall marketplace evolution. The tags serve as immutable release markers for users and automated deployment systems.

**Release Readiness**: With both PR merge and tags complete, the JSON Structured Outputs skill suite is now:
- Discoverable in the marketplace
- Versioned for dependency management
- Ready for distribution/installation

### Skill Integration

- **Phase 1**: Real-world example of @ convention
- **Important Reminders**: "Tags are immutable"

---

## Insight-to-Skill Mapping

| Insight | SKILL.md Section | Contribution |
|---------|------------------|--------------|
| Semantic Git Tagging | Phase 1, Phase 5 | Slash-based namespace option, tag filtering |
| NPM-Style Convention | Phase 1, Phase 2 | @ separator option, version numbering rules |
| Git Tags vs Releases | Phase 4, Reminders | Trade-offs explanation, relationship clarity |
| Namespace Conventions | Phase 1, Troubleshooting | Namespace clarity benefits, monorepo guidance |
| Semantic Versioning | Phase 2 | Version bump rules, PATCH example |
| Fast-Forward Merges | Phase 5, Reminders | Linear history awareness |
| Tagging Convention | Phase 1, Reminders | Real-world example, immutability principle |

---

## Clustering Analysis

**Similarity Score**: 0.82 (high cohesion)

**Common Keywords**:
- git, tag, version, semantic, namespace, release, convention, monorepo

**Temporal Proximity**:
- 6 of 7 insights from 2025-11-14 (same day)
- 1 insight from 2025-11-15 (next day)

**Category Alignment**:
- All from version-control category (100%)

**Workflow Coherence**:
- All insights relate to the tag creation and management lifecycle
- Natural progression: Choose convention → Calculate version → Create tag → Manage history

---

## Quality Assessment

- ✅ **Actionable**: All insights provide concrete guidance
- ✅ **Non-redundant**: Each insight covers unique aspect of tagging
- ✅ **Production-tested**: Insights from real release workflows
- ✅ **Well-documented**: Clear examples and rationale provided
- ✅ **Complementary**: Insights build on each other cohesively

---

## Future Enhancements

Potential additions to this skill based on related insights:
- GitHub Actions workflow examples for automated tagging
- Integration with changelog generation tools
- Pre-commit hooks for tag validation
- Tag protection rules configuration
