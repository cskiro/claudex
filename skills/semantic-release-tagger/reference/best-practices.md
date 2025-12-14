# Best Practices & Important Reminders

## Core Principles

- **Start at 0.1.0, not 1.0.0**: Reserve 1.0.0 for production-ready releases
- **Consistency is critical**: Pick one tag convention and stick to it across the entire repository
- **Tags are immutable**: Once pushed, don't modify or delete tags (users may depend on them)
- **Annotated tags preferred**: Use `git tag -a` for all releases (stores metadata)
- **Push tags explicitly**: `git push` doesn't push tags automatically, use `git push origin <tagname>`
- **Namespace for monorepos**: Even if you have one "main" component, use namespaced tags for future scalability
- **Git tags ≠ GitHub releases**: Tags are required, releases are optional but add discoverability
- **Fast-forward merges preserve history**: Linear history makes tagging cleaner and more predictable

## Warnings

- ⚠️  **Don't mix tag conventions** (e.g., `marketplace/v1.0.0` and `marketplace@2.0.0`)
- ⚠️  **Don't skip version numbers** (e.g., 1.0.0 → 1.2.0). Always increment by 1
- ⚠️  **Don't delete published tags** without team coordination (breaks dependencies)
- ⚠️  **Don't use lightweight tags for releases** (use annotated tags with `-a` flag)

## Related Skills

- `release-management` - For changelog generation and deployment
- `monorepo-workflow` - For managing multi-component repositories
