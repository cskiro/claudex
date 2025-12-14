# Git Worktree Setup Skill

Automated git worktree creation for parallel Claude Code sessions. Work on multiple branches simultaneously without conflicts or context switching.

## Quick Start

### Single Worktree

```
User: Create a worktree for feature-authentication
```

Claude will:
1. Verify prerequisites
2. Create worktree at `../project-feature-authentication`
3. Set up development environment
4. Provide commands to start working

### Multiple Worktrees

```
User: Set up worktrees for feature-a, feature-b, and hotfix-123
```

Claude creates all three worktrees in parallel with full setup.

### List Worktrees

```
User: Show me my worktrees
```

Claude displays all active worktrees and their status.

### Cleanup

```
User: Remove the feature-authentication worktree
```

Claude safely removes the worktree after checking for uncommitted changes.

## Features

### Automatic Prerequisite Checking
- Verifies git repository
- Checks for uncommitted changes
- Validates branch existence
- Ensures no directory conflicts
- Confirms sufficient disk space

### Smart Defaults
- **Location:** `../repo-name-branch-name`
- **Branch type:** Auto-detects new vs. existing
- **Dev setup:** Automatically runs if package.json exists
- **Package manager:** Detects pnpm/yarn/bun/npm from lockfiles

### Development Environment Setup
- Detects package manager automatically
- Runs installation commands
- Optionally copies `.env` files
- Verifies setup succeeded

### Safe Cleanup
- Confirms before removing worktrees
- Checks for uncommitted changes
- Option to delete branch too
- Provides rollback instructions

### Clear Guidance
- Shows worktree path and status
- Provides navigation commands
- Explains how to start Claude Code
- Lists all worktrees for reference

## Usage Examples

### Example 1: New Feature Branch

**Scenario:** You want to start a new feature while keeping your current work.

```
User: Create a worktree for feature-user-profiles

Claude:
✓ Checking prerequisites...
✓ Repository: myapp
✓ Creating worktree at: /Users/connor/myapp-feature-user-profiles
✓ Created new branch: feature-user-profiles
✓ Running npm install...
✓ Development environment ready

Next steps:
  cd ../myapp-feature-user-profiles
  claude

All worktrees:
  /Users/connor/myapp (main) ← current
  /Users/connor/myapp-feature-user-profiles (feature-user-profiles) ← new
```

### Example 2: Work on Existing Branch

**Scenario:** You need to review a colleague's branch without switching your current work.

```
User: Set up a worktree for the existing bugfix-payment branch

Claude:
✓ Checking prerequisites...
✓ Found existing branch: bugfix-payment
✓ Creating worktree at: /Users/connor/myapp-bugfix-payment
✓ Checked out: bugfix-payment
✓ Running pnpm install...
✓ Ready for review

Navigate to worktree:
  cd ../myapp-bugfix-payment
  claude
```

### Example 3: Multiple Worktrees for Testing

**Scenario:** You need to test multiple features simultaneously.

```
User: Create worktrees for feature-dashboard, feature-reports, and feature-export

Claude:
✓ Creating 3 worktrees...

✓ feature-dashboard → /Users/connor/myapp-feature-dashboard
✓ feature-reports → /Users/connor/myapp-feature-reports
✓ feature-export → /Users/connor/myapp-feature-export

✓ Installing dependencies in all worktrees...
✓ All environments ready

Start working:
  cd ../myapp-feature-dashboard && claude
  cd ../myapp-feature-reports && claude
  cd ../myapp-feature-export && claude
```

### Example 4: Emergency Hotfix

**Scenario:** Production issue needs immediate attention, but you're mid-feature.

```
User: I need a worktree for hotfix-login-redirect from main

Claude:
✓ Creating hotfix worktree from main...
✓ Worktree: /Users/connor/myapp-hotfix-login-redirect
✓ Branch: hotfix-login-redirect (from main)
✓ Dependencies installed
✓ Ready for emergency fix

Your current work in /Users/connor/myapp is untouched.

Fix the issue in:
  cd ../myapp-hotfix-login-redirect
  claude
```

### Example 5: Cleanup After Merge

**Scenario:** Your feature is merged, time to clean up.

```
User: Remove the feature-user-profiles worktree

Claude:
Checking /Users/connor/myapp-feature-user-profiles...
✓ No uncommitted changes
✓ Branch already merged to main

Remove worktree and delete branch? [yes/no]

User: yes

Claude:
✓ Removed worktree: /Users/connor/myapp-feature-user-profiles
✓ Deleted branch: feature-user-profiles

Remaining worktrees:
  /Users/connor/myapp (main) ← current
```

## How It Works

### Worktree Creation Flow

```
User Request
     ↓
Check Prerequisites
     ├─ Git repository? ✓
     ├─ Clean working dir? ⚠️ (warn if dirty)
     ├─ Branch exists? ✓
     └─ Target dir available? ✓
     ↓
Gather Information
     ├─ Branch name (from request)
     ├─ Location (default: ../repo-branch)
     └─ Dev setup? (yes if package.json exists)
     ↓
Create Worktree
     ├─ New branch: git worktree add path -b branch
     └─ Existing: git worktree add path branch
     ↓
Setup Environment
     ├─ Detect package manager (lockfiles)
     ├─ Run installation
     └─ Copy .env (optional)
     ↓
Verify & Report
     ├─ Check worktree list
     ├─ Show path and commands
     └─ List all worktrees
```

### Package Manager Detection

The skill automatically detects your package manager:

| Lockfile           | Package Manager |
|--------------------|-----------------|
| pnpm-lock.yaml     | pnpm            |
| yarn.lock          | yarn            |
| bun.lockb          | bun             |
| package-lock.json  | npm             |

## Benefits

### Parallel Development
- Work on multiple features simultaneously
- No context switching overhead
- Each worktree is isolated
- All share git history

### Risk Mitigation
- Keep stable main branch untouched
- Test risky changes in isolation
- Easy rollback - just remove worktree
- No stashing required

### Enhanced Productivity
- Run multiple Claude Code sessions
- Compare implementations side-by-side
- Test across branches
- Review PRs without switching

### Team Collaboration
- Review teammate's code without disruption
- Test integration of multiple features
- Maintain clean working directories
- Easy handoff between sessions

## Common Workflows

### Feature Development
1. Start new feature worktree
2. Implement in parallel with other work
3. Test in isolation
4. Merge when ready
5. Clean up worktree

### Code Review
1. Create worktree from PR branch
2. Review in Claude Code
3. Test changes
4. Remove worktree after approval

### Hotfix Management
1. Create worktree from main
2. Fix critical issue
3. Deploy hotfix
4. Clean up without affecting feature work

### Integration Testing
1. Create worktrees for all feature branches
2. Test interactions
3. Identify integration issues
4. Fix in respective worktrees

## Troubleshooting

### "Not in a git repository"
**Solution:** Navigate to your git repository root before requesting worktree.

### "Branch already checked out"
**Solution:** Remove existing worktree first: `User: remove worktree [name]`

### "Directory already exists"
**Solution:** Choose different location or remove existing directory.

### Package installation fails
**Solution:** Check network connection, or manually run install in worktree.

### Uncommitted changes warning
**Solution:** Commit or stash changes, or confirm to continue anyway.

## Best Practices

### Naming Conventions
- **Features:** `feature-descriptive-name`
- **Bugfixes:** `bugfix-issue-description`
- **Hotfixes:** `hotfix-critical-issue`
- **Experiments:** `experiment-idea-name`

### Worktree Management
- Clean up merged branches regularly
- Use descriptive branch names
- Keep worktrees focused on single tasks
- Commit often in each worktree

### Resource Management
- Limit active worktrees to ~5 simultaneously
- Each worktree consumes disk space
- Dependencies installed in each worktree
- Monitor disk usage for large projects

### Safety
- Always check for uncommitted changes before removing
- Use `git worktree list` to see all active worktrees
- Keep main worktree clean and stable
- Back up important work before experimenting

## Advanced Usage

### Custom Locations
```
User: Create worktree for feature-x at ~/projects/feature-x
```

### Skip Dev Setup
```
User: Create worktree for feature-y without installing dependencies
```

### Specific Base Branch
```
User: Create worktree for hotfix-z from the production branch
```

### Batch Operations
```
User: Create worktrees for all open PRs
```

## Integration with Claude Code

### Starting Sessions
After worktree creation:
```bash
cd /path/to/worktree
claude
```

### Parallel Sessions
Run Claude Code in multiple terminals:
```bash
# Terminal 1
cd ~/myapp-feature-a && claude

# Terminal 2
cd ~/myapp-feature-b && claude

# Terminal 3
cd ~/myapp-main && claude
```

### Session Handoff
Use `/handoff` in each session for context preservation:
```
# In worktree session
/handoff to document progress before switching
```

## Related Documentation

- [Git Worktree Official Docs](https://git-scm.com/docs/git-worktree)
- [Claude Code Parallel Sessions](https://docs.claude.com/en/docs/claude-code/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)
- Troubleshooting: `data/troubleshooting.md`
- Best Practices: `data/best-practices.md`
- Example Workflows: `examples/sample-workflows.md`

## Support

### Skill Information
- **Version:** 1.0.0
- **Author:** Connor
- **Skill Type:** Automation/DevOps

### Getting Help
```
User: How do I use git worktrees?
User: Show me worktree examples
User: What are the benefits of worktrees?
```

---

**Ready to work in parallel?** Just ask Claude to create a worktree!
