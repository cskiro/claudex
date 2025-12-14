# Git Worktree Best Practices

A comprehensive guide to using git worktrees effectively for parallel development with Claude Code.

## Table of Contents

1. [Branch Naming Conventions](#branch-naming-conventions)
2. [Worktree Organization](#worktree-organization)
3. [Resource Management](#resource-management)
4. [Workflow Patterns](#workflow-patterns)
5. [Cleanup Strategies](#cleanup-strategies)
6. [Team Collaboration](#team-collaboration)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)

---

## Branch Naming Conventions

### Recommended Patterns

**Feature Branches:**
```
feature/descriptive-name
feature/user-authentication
feature/payment-integration
feature/dashboard-redesign
```

**Bugfix Branches:**
```
bugfix/issue-number-description
bugfix/123-login-redirect
bugfix/456-memory-leak
bugfix/789-validation-error
```

**Hotfix Branches:**
```
hotfix/critical-issue
hotfix/security-patch
hotfix/production-crash
```

**Experimental Branches:**
```
experiment/idea-name
experiment/new-architecture
experiment/performance-test
```

**Chore Branches:**
```
chore/dependency-updates
chore/refactor-auth
chore/update-docs
```

### Why Good Names Matter

- **Clarity:** Instantly understand the purpose
- **Organization:** Easy to group and filter
- **Cleanup:** Identify old branches quickly
- **Collaboration:** Team members know what's being worked on

### Naming Anti-Patterns

❌ **Avoid:**
- Vague names: `fix`, `update`, `changes`
- Personal names: `johns-branch`, `temp-work`
- Dates only: `2025-09-04`, `sept-changes`
- No context: `test`, `wip`, `tmp`

✅ **Use:**
- Descriptive: `feature/oauth-integration`
- Issue-linked: `bugfix/1234-payment-error`
- Purpose-clear: `experiment/graphql-migration`

---

## Worktree Organization

### Directory Structure

**Recommended: Sibling Directories**
```
~/projects/
├── myapp/                    # Main worktree
├── myapp-feature-auth/       # Feature worktree
├── myapp-bugfix-login/       # Bugfix worktree
└── myapp-experiment-ui/      # Experiment worktree
```

**Alternative: Dedicated Worktrees Directory**
```
~/projects/
├── myapp/                    # Main worktree
└── myapp-worktrees/          # All worktrees
    ├── feature-auth/
    ├── bugfix-login/
    └── experiment-ui/
```

**Team Shared Setup:**
```
~/work/
├── myapp/                    # Main (stable)
├── myapp-review/             # For PR reviews
├── myapp-hotfix/             # Emergency fixes
└── myapp-current/            # Active feature work
```

### Location Best Practices

✅ **Do:**
- Keep worktrees near main repo (faster operations)
- Use consistent naming pattern
- Group by purpose if many worktrees
- Document custom locations in team wiki

❌ **Don't:**
- Scatter worktrees across filesystem
- Use deep nested paths (slow operations)
- Mix worktrees with unrelated projects
- Create worktrees inside other worktrees

---

## Resource Management

### Disk Space

**Understanding Space Usage:**
```
Main repository: 150 MB
Each worktree:
  - Repository files: 150 MB
  - node_modules: 700 MB
  - Build artifacts: 50 MB
  Total: ~900 MB per worktree
```

**Space Management Strategies:**

1. **Limit Active Worktrees**
   - Keep 3-5 active worktrees maximum
   - Clean up merged branches weekly
   - Archive instead of keeping indefinitely

2. **Share When Possible**
   - Use pnpm for shared node_modules
   - Enable yarn's zero-installs
   - Share build caches

3. **Clean Build Artifacts**
   ```bash
   # Clean before removing worktree
   cd worktree-path
   npm run clean
   rm -rf dist/ build/ .next/
   ```

4. **Monitor Disk Usage**
   ```bash
   # Check worktree sizes
   du -sh ../myapp-*

   # Find largest directories
   du -sh */ | sort -hr | head -10
   ```

### Memory Considerations

**Running Multiple Claude Code Sessions:**
- Each session: ~500MB RAM
- 3 parallel sessions: ~1.5GB RAM
- Keep system RAM usage < 80%

**Tips:**
- Close unused sessions
- Restart sessions periodically
- Use `/handoff` to preserve context
- Monitor system performance

### CPU Management

**Avoid Parallel Builds:**
```bash
# Bad: Running builds in all worktrees simultaneously
cd worktree1 && npm run build &
cd worktree2 && npm run build &
cd worktree3 && npm run build &

# Good: Sequential or limited parallel
npm run build  # One at a time
```

**Use Build Queues:**
- Serialize resource-intensive operations
- Limit concurrent processes
- Use tools like `make -j2` for controlled parallelism

---

## Workflow Patterns

### Pattern 1: Feature Development

```
1. Create worktree for feature
   └─ git worktree add ../myapp-feature-x -b feature-x

2. Develop in isolation
   └─ cd ../myapp-feature-x && claude

3. Test independently
   └─ npm test && npm run build

4. Merge when ready
   └─ git checkout main && git merge feature-x

5. Clean up
   └─ git worktree remove ../myapp-feature-x
```

### Pattern 2: PR Review

```
1. Create worktree from PR branch
   └─ git worktree add ../myapp-review pr-branch

2. Review code with Claude Code
   └─ cd ../myapp-review && claude

3. Test changes
   └─ npm install && npm test

4. Leave feedback
   └─ (Review in Claude Code)

5. Remove when done
   └─ git worktree remove ../myapp-review
```

### Pattern 3: Hotfix While Developing

```
Current state: Working on feature-x in worktree

1. Create hotfix worktree from main
   └─ git worktree add ../myapp-hotfix -b hotfix-critical

2. Fix issue in hotfix worktree
   └─ cd ../myapp-hotfix && claude

3. Test and deploy
   └─ npm test && deploy

4. Continue feature work
   └─ cd ../myapp-feature-x

5. Merge hotfix to both main and feature
   └─ git checkout feature-x && git merge main
```

### Pattern 4: Integration Testing

```
1. Create worktrees for all features
   └─ Batch create: feature-a, feature-b, feature-c

2. Test each independently
   └─ Parallel Claude Code sessions

3. Create integration worktree
   └─ git worktree add ../myapp-integration -b integration

4. Merge all features to integration
   └─ git merge feature-a feature-b feature-c

5. Test combined functionality
   └─ npm test && npm run e2e

6. Clean up all worktrees after merge
```

### Pattern 5: Comparison Testing

```
1. Keep main worktree as baseline
2. Create feature worktree for new implementation
3. Run same tests in both
4. Compare results side-by-side
5. Make decision based on data
```

---

## Cleanup Strategies

### Daily Cleanup

**Check merged branches:**
```bash
# List merged branches
git branch --merged main | grep -v "main"

# Remove worktrees for merged branches
for branch in $(git branch --merged main | grep -v "main"); do
  git worktree remove ../myapp-$branch 2>/dev/null || true
  git branch -d $branch
done
```

### Weekly Cleanup

**Review all worktrees:**
```bash
# List all worktrees with age
git worktree list | while read path commit branch; do
  cd "$path"
  age=$(git log -1 --format=%ar)
  echo "$branch: last activity $age"
done
```

**Remove stale worktrees (30+ days):**
```bash
# Manual review first, then remove
git worktree list | grep -v main | while read path; do
  cd "$path"
  last_commit=$(git log -1 --format=%ct)
  current_time=$(date +%s)
  days_old=$(( (current_time - last_commit) / 86400 ))

  if [ $days_old -gt 30 ]; then
    echo "Stale: $path ($days_old days old)"
  fi
done
```

### Automated Cleanup

**Git hooks for cleanup:**
```bash
# .git/hooks/post-merge
#!/bin/bash
# Auto-cleanup merged branches

CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "main" ]; then
  echo "Checking for merged worktrees..."

  git branch --merged main | grep -v "main" | while read branch; do
    # Check if worktree exists
    if git worktree list | grep -q "\\[$branch\\]"; then
      echo "Found merged worktree: $branch"
      echo "Run: git worktree remove /path/to/$branch"
    fi
  done
fi
```

### Cleanup Checklist

Before removing a worktree:
- [ ] No uncommitted changes
- [ ] Branch merged or backed up
- [ ] No important local files
- [ ] Dependencies can be reinstalled
- [ ] No running processes

---

## Team Collaboration

### Shared Worktree Conventions

**Team Standards Document:**
```markdown
# Worktree Standards

## Naming
- Features: feature/{jira-id}-{description}
- Bugfixes: bugfix/{issue-id}-{description}
- Reviews: review-{pr-number}

## Location
- All worktrees in ~/projects/myapp-worktrees/

## Lifecycle
- Create: Before starting work
- Update: Sync with main daily
- Remove: Within 24h of merge

## Resources
- Max 3 active worktrees per developer
- Clean up merged branches in daily standup
```

### Communication

**Notify team of worktrees:**
```bash
# In team chat
Working on worktrees:
- feature-auth (for AUTH-123)
- bugfix-login (for BUG-456)
- review-pr-789 (reviewing Sarah's PR)

Will clean up by EOD.
```

### Shared Scripts

**Team cleanup script:**
```bash
#!/bin/bash
# team-worktree-status.sh

echo "Worktree Status for $(whoami)"
echo "================================"

git worktree list | while read path commit branch; do
  cd "$path"
  status=$(git status --porcelain | wc -l)
  behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "N/A")

  echo "$branch:"
  echo "  Changes: $status"
  echo "  Behind main: $behind"
  echo "  Path: $path"
  echo ""
done
```

---

## Performance Optimization

### Git Operations

**Fetch Once, Use Everywhere:**
```bash
# In main worktree
git fetch --all

# All worktrees automatically have access
# No need to fetch in each worktree
```

**Shallow Clones for Reviews:**
```bash
# For temporary review worktrees
git worktree add --detach ../review-pr HEAD
cd ../review-pr
git fetch origin pull/123/head:pr-123
git checkout pr-123
```

### Build Performance

**Share Build Caches:**
```bash
# In main repo
export TURBO_CACHE_DIR=/shared/turbo-cache

# All worktrees use same cache
# Builds are faster after first run
```

**Incremental Builds:**
```bash
# Don't clean between branches
npm run build  # Uses previous cache

# Only clean when needed
npm run clean && npm run build
```

### Dependency Management

**pnpm (Recommended for Worktrees):**
```bash
# Global store, minimal duplication
pnpm install

# All worktrees reference same packages
# Saves ~80% disk space
```

**npm/yarn (Standard):**
```bash
# Each worktree has full node_modules
# More disk space, complete isolation
npm install
```

---

## Security Considerations

### Environment Variables

**Never commit .env:**
```bash
# Each worktree needs own .env
cp ../.env .env

# Add to .gitignore (should already be there)
echo ".env" >> .gitignore
```

**Worktree-specific configs:**
```bash
# Different API endpoints per worktree
# main: production API
# feature-x: staging API
# experiment: local API

# .env in each worktree
API_URL=https://staging.api.example.com
```

### Credentials

**Don't share credentials between worktrees:**
- Separate SSH keys if needed
- Different tokens per environment
- Revoke credentials in removed worktrees

**Clean credentials before removal:**
```bash
# Before removing worktree
cd worktree-path
rm -f .env .env.local
rm -f config/credentials.json

# Then remove
git worktree remove $(pwd)
```

### Access Control

**Workspace Permissions:**
```bash
# Ensure proper permissions
chmod 700 ~/projects/myapp-*

# No group/other access to sensitive worktrees
```

---

## Advanced Tips

### Worktree Templates

**Quick setup script:**
```bash
#!/bin/bash
# new-worktree.sh

BRANCH=$1
PATH=../myapp-$BRANCH

git worktree add $PATH -b $BRANCH
cd $PATH
cp ../.env .
pnpm install
code .  # Open in editor

echo "Worktree ready: $PATH"
```

### Automation

**Auto-sync worktrees:**
```bash
# cron job: daily sync
0 9 * * * cd ~/projects/myapp && git fetch && \
  for wt in $(git worktree list | awk '{print $1}'); do \
    cd $wt && git pull --rebase 2>/dev/null; \
  done
```

### Monitoring

**Disk space alerts:**
```bash
# Alert when worktrees exceed threshold
TOTAL=$(du -sm ~/projects/myapp-* | awk '{sum+=$1} END {print sum}')

if [ $TOTAL -gt 10000 ]; then
  echo "Warning: Worktrees using ${TOTAL}MB"
fi
```

---

## Quick Reference

### Commands

```bash
# Create
git worktree add ../myapp-branch -b branch

# List
git worktree list

# Remove
git worktree remove ../myapp-branch

# Prune orphaned
git worktree prune

# Repair if corrupted
git worktree repair

# Move worktree
git worktree move old-path new-path

# Lock (prevent removal)
git worktree lock path

# Unlock
git worktree unlock path
```

### Aliases

```bash
# Add to ~/.gitconfig
[alias]
  wt = worktree
  wtl = worktree list
  wta = "!f() { git worktree add ../$(basename $(pwd))-$1 -b $1; }; f"
  wtr = worktree remove
  wtp = worktree prune
```

**Usage:**
```bash
git wta feature-x          # Creates ../myapp-feature-x
git wtl                    # Lists all worktrees
git wtr ../myapp-feature-x # Removes worktree
```

---

## Summary

**Key Takeaways:**

1. **Use descriptive branch names** - Future you will thank you
2. **Keep worktrees organized** - Consistent location pattern
3. **Monitor disk space** - Limit active worktrees
4. **Clean up regularly** - Don't hoard merged branches
5. **Document team conventions** - Everyone follows same patterns
6. **Optimize for performance** - Use pnpm, shared caches
7. **Secure sensitive data** - Clean .env before removal
8. **Automate repetitive tasks** - Scripts for common operations

**Remember:** Git worktrees are powerful tools for parallel development. Used well, they enhance productivity. Used poorly, they create chaos. Follow these best practices for worktree success!
