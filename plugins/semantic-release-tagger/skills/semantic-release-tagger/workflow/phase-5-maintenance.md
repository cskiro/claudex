# Phase 5: Maintain Tag History

**Purpose**: Keep tag history clean, organized, and automation-friendly.

## Steps

### 1. Filter Tags by Component (monorepos)

```bash
# List all marketplace tags
git tag -l "marketplace@*"

# List all hook tags
git tag -l "hook/*"

# List with sort (latest first)
git tag -l "component@*" --sort=-v:refname
```

### 2. Find Latest Version Programmatically

```bash
# Latest marketplace version
git tag -l "marketplace@*" --sort=-v:refname | head -1

# Extract version number only
git tag -l "marketplace@*" --sort=-v:refname | head -1 | cut -d'@' -f2
```

### 3. Set Up CI/CD Tag Triggers

GitHub Actions example:
```yaml
on:
  push:
    tags:
      - 'marketplace@*'  # Trigger on marketplace tags only
      - 'hook/*'         # Trigger on any hook tag
```

### 4. Clean Up Tags (use cautiously)

```bash
# Delete local tag
git tag -d old-tag-name

# Delete remote tag (DANGEROUS - coordinate with team)
git push origin :refs/tags/old-tag-name
```

### 5. Fast-forward Merge Awareness

- When GitHub shows "Fast-forward" on PR merge:
  - Main branch pointer moved forward without merge commit
  - Linear history maintained (no divergence)
  - Happens when PR branch is directly ahead of main
- Tags created after fast-forward merge will reference the correct commit

### 6. Tag Maintenance Best Practices

- Never modify published tags (immutable release markers)
- Document tag conventions in repository
- Use automation to enforce tag format
- Archive old tags in changelog, don't delete

## Output

Clean, organized tag history with automation support.

## Common Issues

- **Deleting published tags**: Avoid deleting tags that users may depend on
- **Inconsistent tag patterns**: Automation breaks if tags don't follow consistent format
- **Missing tag documentation**: Always document your tagging convention in README
