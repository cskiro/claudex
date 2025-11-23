---
name: git-worktree-setup
description: Automated git worktree setup for parallel Claude Code sessions with prerequisite checking, development environment initialization, and safe cleanup. Use when working on multiple branches simultaneously.
---

# Git Worktree Setup

Automates git worktree creation for parallel Claude Code sessions without conflicts.

## When to Use

**Trigger Phrases**:
- "create a worktree for [branch-name]"
- "set up worktree for [feature]"
- "create worktrees for [branch1], [branch2]"
- "remove worktree [name]"
- "list my worktrees"

**Use Cases**:
- Working on multiple features simultaneously
- Parallel Claude Code sessions on different branches
- Code review while continuing development
- Emergency hotfixes without interrupting work

## Quick Decision Matrix

| Request | Mode | Action |
|---------|------|--------|
| "create worktree for X" | Single | Create one worktree |
| "set up worktrees for X, Y" | Batch | Create multiple |
| "remove worktree X" | Cleanup | Remove specific |
| "list worktrees" | List | Display status |

## Workflow Overview

### Phase 0: Prerequisites (Mandatory)
```bash
# Verify git repo
git rev-parse --is-inside-work-tree

# Check uncommitted changes
git status --porcelain

# Get repo name
basename $(git rev-parse --show-toplevel)
```

### Phase 1: Gather Information
- Branch name (required)
- New or existing branch
- Location (default: `../repo-branch`)
- Setup dev environment

### Phase 2: Create Worktree
```bash
# New branch
git worktree add ../project-feature -b feature

# Existing branch
git worktree add ../project-bugfix bugfix
```

### Phase 3: Dev Environment Setup
- Detect package manager
- Run install
- Copy .env files

### Phase 4: Next Steps
- Show worktree path
- Provide navigation commands
- List all worktrees

## Quick Reference Commands

```bash
# Create with new branch
git worktree add ../project-branch -b branch-name

# Create from existing
git worktree add ../project-branch branch-name

# List all
git worktree list

# Remove worktree
git worktree remove ../project-branch

# Remove worktree and branch
git worktree remove ../project-branch
git branch -D branch-name
```

## Package Manager Detection

| Lock File | Manager |
|-----------|---------|
| pnpm-lock.yaml | pnpm |
| yarn.lock | yarn |
| bun.lockb | bun |
| package-lock.json | npm |

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "invalid reference" | Branch doesn't exist | Use `-b` for new |
| "already exists" | Directory exists | Choose different location |
| "uncommitted changes" | Dirty working dir | Commit or stash |

## Safety Protocols

**Before Creating**:
- [ ] Verify git repository
- [ ] Check clean working directory
- [ ] Validate target directory available

**Before Cleanup**:
- [ ] Confirm user intent
- [ ] Check for uncommitted changes
- [ ] Warn about permanent branch deletion

## Example Output

```
✓ Worktree created: /Users/connor/myapp-feature-auth
✓ Branch: feature-auth (new)
✓ Dependencies installed

Next steps:
  cd ../myapp-feature-auth
  claude

All worktrees:
- /path/to/main (main) ← current
- /path/to/worktree (feature-auth) ← new
```

## Success Criteria

- [ ] Worktree in correct location
- [ ] Branch checked out properly
- [ ] Files visible in directory
- [ ] Dev environment ready
- [ ] Appears in `git worktree list`
- [ ] User can start Claude Code

## Reference Materials

- `modes/` - Detailed mode workflows
- `templates/` - Setup script templates
- `data/best-practices.md`
- `data/troubleshooting.md`

---

**Version**: 1.0.0 | **Author**: Connor
