# Git Worktree Troubleshooting Guide

Comprehensive troubleshooting for common git worktree issues, errors, and edge cases.

## Table of Contents

1. [Creation Errors](#creation-errors)
2. [Permission Issues](#permission-issues)
3. [Corruption and Repair](#corruption-and-repair)
4. [Branch Conflicts](#branch-conflicts)
5. [Directory Issues](#directory-issues)
6. [Performance Problems](#performance-problems)
7. [Dependency Installation](#dependency-installation)
8. [Git Operations](#git-operations)
9. [Cleanup Issues](#cleanup-issues)
10. [Advanced Debugging](#advanced-debugging)

---

## Creation Errors

### Error: "fatal: invalid reference"

**Full Error:**
```
fatal: invalid reference: feature-x
```

**Cause:**
Branch doesn't exist (typo or branch not created yet).

**Solutions:**

1. **Create new branch:**
   ```bash
   git worktree add ../myapp-feature-x -b feature-x
   ```

2. **Check branch name:**
   ```bash
   git branch -a  # List all branches
   git branch | grep feature  # Search for branch
   ```

3. **Track remote branch:**
   ```bash
   git worktree add ../myapp-feature-x -b feature-x --track origin/feature-x
   ```

---

### Error: "fatal: 'path' already exists"

**Full Error:**
```
fatal: '../myapp-feature-x' already exists
```

**Cause:**
Directory already exists at target path.

**Solutions:**

1. **Remove directory:**
   ```bash
   rm -rf ../myapp-feature-x
   git worktree add ../myapp-feature-x -b feature-x
   ```

2. **Use different location:**
   ```bash
   git worktree add ../myapp-feature-x-v2 -b feature-x
   ```

3. **Check if it's a forgotten worktree:**
   ```bash
   git worktree list  # If not listed, safe to remove
   ```

---

### Error: "fatal: 'branch' is already checked out"

**Full Error:**
```
fatal: 'feature-x' is already checked out at '/Users/connor/myapp-feature-x'
```

**Cause:**
Branch is already checked out in another worktree.

**Solutions:**

1. **Navigate to existing worktree:**
   ```bash
   git worktree list  # Find existing worktree
   cd /path/to/existing/worktree
   ```

2. **Remove existing worktree:**
   ```bash
   git worktree remove /path/to/existing/worktree
   # Then create new one
   git worktree add ../myapp-feature-x feature-x
   ```

3. **Use different branch:**
   ```bash
   git worktree add ../myapp-feature-x-new -b feature-x-new
   ```

---

### Error: "fatal: not a git repository"

**Full Error:**
```
fatal: not a git repository (or any of the parent directories): .git
```

**Cause:**
Not in a git repository.

**Solutions:**

1. **Navigate to repository:**
   ```bash
   cd /path/to/your/git/repo
   git worktree add ../worktree-name -b branch-name
   ```

2. **Verify git repository:**
   ```bash
   git status  # Should not error
   ls -la .git  # Should exist
   ```

3. **Initialize if needed:**
   ```bash
   git init  # Only if starting new repo
   ```

---

## Permission Issues

### Error: "Permission denied"

**Full Error:**
```
error: unable to create file: Permission denied
```

**Cause:**
Insufficient permissions to create worktree directory.

**Solutions:**

1. **Check parent directory permissions:**
   ```bash
   ls -ld $(dirname /path/to/worktree)
   ```

2. **Fix permissions:**
   ```bash
   chmod 755 /path/to/parent
   ```

3. **Use location you own:**
   ```bash
   git worktree add ~/worktrees/myapp-feature-x -b feature-x
   ```

4. **Check disk quota:**
   ```bash
   df -h  # Check disk space
   quota -s  # Check user quota (if applicable)
   ```

---

### Error: "Operation not permitted"

**Cause:**
macOS security restrictions or readonly filesystem.

**Solutions:**

1. **Grant Full Disk Access:**
   - System Preferences → Security & Privacy → Privacy
   - Full Disk Access → Add Terminal/IDE

2. **Check filesystem mount:**
   ```bash
   mount | grep "$(pwd)"
   # If shows 'ro' (readonly), remount:
   # sudo mount -uw /
   ```

3. **Use different location:**
   ```bash
   # Use home directory (always writable)
   git worktree add ~/worktrees/myapp-feature-x -b feature-x
   ```

---

## Corruption and Repair

### Error: "Worktree path doesn't exist but listed"

**Symptoms:**
```
git worktree list
# Shows: /path/to/missing/worktree abc123 [branch]
# But: ls /path/to/missing/worktree
# No such file or directory
```

**Cause:**
Worktree directory manually deleted without `git worktree remove`.

**Solutions:**

1. **Prune orphaned references:**
   ```bash
   git worktree prune
   git worktree list  # Verify removed
   ```

2. **Force remove:**
   ```bash
   git worktree remove --force /path/to/missing/worktree
   ```

3. **Manual cleanup:**
   ```bash
   # Check administrative files
   ls .git/worktrees/
   # Remove specific worktree directory
   rm -rf .git/worktrees/branch-name
   git worktree prune
   ```

---

### Error: "Corrupt worktree"

**Symptoms:**
- Can't checkout files
- Git commands fail in worktree
- Missing .git file in worktree

**Solutions:**

1. **Repair worktree:**
   ```bash
   git worktree repair
   ```

2. **Check .git file:**
   ```bash
   cat worktree-path/.git
   # Should show: gitdir: /path/to/main/.git/worktrees/branch
   ```

3. **Recreate .git file:**
   ```bash
   # If corrupt, recreate
   echo "gitdir: $(git rev-parse --git-dir)/worktrees/branch-name" > worktree-path/.git
   ```

4. **Last resort - recreate worktree:**
   ```bash
   # Backup any changes
   cp -r worktree-path worktree-path-backup

   # Remove and recreate
   git worktree remove --force worktree-path
   git worktree add worktree-path branch-name

   # Restore changes
   cp worktree-path-backup/* worktree-path/
   ```

---

## Branch Conflicts

### Error: "Cannot delete branch checked out in worktree"

**Full Error:**
```
error: Cannot delete branch 'feature-x' checked out at '/path/to/worktree'
```

**Cause:**
Trying to delete branch that's checked out in a worktree.

**Solutions:**

1. **Remove worktree first:**
   ```bash
   git worktree remove /path/to/worktree
   git branch -d feature-x
   ```

2. **Force delete (if sure):**
   ```bash
   # This will remove worktree administrative files
   git worktree remove --force /path/to/worktree
   git branch -D feature-x
   ```

3. **Switch branch in worktree:**
   ```bash
   cd /path/to/worktree
   git checkout different-branch
   # Now can delete feature-x in main repo
   ```

---

### Error: "Reference is not a tree"

**Full Error:**
```
fatal: reference is not a tree: abc123
```

**Cause:**
Commit reference doesn't exist or is corrupted.

**Solutions:**

1. **Fetch latest:**
   ```bash
   git fetch --all
   git worktree add ../worktree branch-name
   ```

2. **Use specific commit:**
   ```bash
   git worktree add ../worktree commit-hash
   ```

3. **Check object exists:**
   ```bash
   git cat-file -t abc123  # Should show 'commit'
   git fsck  # Check repository health
   ```

---

## Directory Issues

### Error: "Disk quota exceeded"

**Full Error:**
```
error: unable to create file: Disk quota exceeded
```

**Cause:**
Not enough disk space or quota exceeded.

**Solutions:**

1. **Check disk space:**
   ```bash
   df -h
   du -sh /path/to/worktrees
   ```

2. **Clean up old worktrees:**
   ```bash
   git worktree list
   git worktree remove /path/to/old/worktree
   ```

3. **Clean build artifacts:**
   ```bash
   cd worktree
   rm -rf node_modules dist build .next
   npm install  # Reinstall only what's needed
   ```

4. **Use different partition:**
   ```bash
   git worktree add /other/partition/worktree -b branch
   ```

---

### Error: "Worktree directory not empty"

**Symptoms:**
Directory exists with files but not a git worktree.

**Solutions:**

1. **Remove conflicting directory:**
   ```bash
   # Backup if needed
   mv /path/to/directory /path/to/directory-backup

   # Create worktree
   git worktree add /path/to/directory -b branch
   ```

2. **Merge contents:**
   ```bash
   # Create worktree elsewhere
   git worktree add /temp/location -b branch

   # Copy existing files
   cp -r /path/to/directory/* /temp/location/

   # Move worktree
   git worktree move /temp/location /path/to/directory
   ```

---

## Performance Problems

### Problem: "Slow git operations in worktree"

**Symptoms:**
- `git status` takes 10+ seconds
- `git checkout` is very slow
- High CPU usage

**Solutions:**

1. **Check filesystem performance:**
   ```bash
   # Test read speed
   time cat large-file.txt > /dev/null

   # Test write speed
   time dd if=/dev/zero of=test.img bs=1M count=1024
   ```

2. **Disable status optimizations:**
   ```bash
   # If on network drive
   git config core.fsmonitor false
   git config core.untrackedCache false
   ```

3. **Use sparse checkout:**
   ```bash
   git sparse-checkout init --cone
   git sparse-checkout set src/ tests/
   ```

4. **Move to local disk:**
   ```bash
   # Network drives are slow
   git worktree add ~/local-worktrees/feature-x -b feature-x
   ```

---

### Problem: "High disk usage"

**Symptoms:**
- Each worktree uses 1GB+
- Running out of disk space

**Solutions:**

1. **Use pnpm:**
   ```bash
   npm install -g pnpm
   # pnpm uses content-addressable storage
   # Saves ~70% disk space for node_modules
   ```

2. **Share node_modules:**
   ```bash
   # In main repo
   pnpm install

   # In worktree
   pnpm install --prefer-offline
   # Uses shared cache
   ```

3. **Clean build artifacts:**
   ```bash
   # Add to package.json
   "scripts": {
     "clean": "rm -rf dist build .next coverage"
   }

   # Run before removing worktree
   npm run clean
   ```

4. **Limit worktrees:**
   ```bash
   # Keep only 3-4 active worktrees
   # Remove old ones regularly
   ```

---

## Dependency Installation

### Error: "npm install fails in worktree"

**Symptoms:**
```
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /path/to/worktree/package.json
```

**Solutions:**

1. **Verify package.json exists:**
   ```bash
   ls -la worktree-path/package.json
   ```

2. **Check file permissions:**
   ```bash
   chmod 644 worktree-path/package.json
   ```

3. **Copy from main repo:**
   ```bash
   cp main-repo/package.json worktree-path/
   cp main-repo/package-lock.json worktree-path/
   ```

4. **Reinstall:**
   ```bash
   cd worktree-path
   rm -rf node_modules package-lock.json
   npm install
   ```

---

### Error: "Lockfile conflict"

**Symptoms:**
```
npm ERR! Cannot read property 'match' of undefined
```

**Cause:**
Lockfile from different package manager or corrupted.

**Solutions:**

1. **Match package manager:**
   ```bash
   # Check main repo
   ls main-repo/*lock*

   # If pnpm-lock.yaml:
   pnpm install

   # If yarn.lock:
   yarn install

   # If package-lock.json:
   npm install
   ```

2. **Remove and regenerate:**
   ```bash
   rm package-lock.json
   npm install  # Creates fresh lockfile
   ```

3. **Copy lockfile from main:**
   ```bash
   cp main-repo/package-lock.json worktree/
   npm ci  # Clean install from lockfile
   ```

---

## Git Operations

### Error: "Cannot merge in worktree"

**Symptoms:**
```
error: Your local changes would be overwritten by merge
```

**Solutions:**

1. **Commit or stash changes:**
   ```bash
   git add .
   git commit -m "WIP: save changes"
   # Or:
   git stash push -m "WIP before merge"
   ```

2. **Merge with strategy:**
   ```bash
   git merge --no-commit --no-ff branch-name
   # Review changes, then commit
   ```

3. **Rebase instead:**
   ```bash
   git rebase main
   # Replay commits on top of main
   ```

---

### Error: "Detached HEAD in worktree"

**Symptoms:**
```
You are in 'detached HEAD' state
```

**Cause:**
Checked out specific commit instead of branch.

**Solutions:**

1. **Create branch from current state:**
   ```bash
   git checkout -b new-branch-name
   ```

2. **Checkout existing branch:**
   ```bash
   git checkout branch-name
   ```

3. **Return to main branch:**
   ```bash
   git checkout main
   ```

---

## Cleanup Issues

### Error: "Cannot remove worktree - dirty"

**Full Error:**
```
error: repository is dirty, please commit or stash your changes
```

**Cause:**
Worktree has uncommitted changes.

**Solutions:**

1. **Commit changes:**
   ```bash
   cd worktree-path
   git add .
   git commit -m "Final changes before removal"
   git push  # Push if needed

   # Now remove
   git worktree remove $(pwd)
   ```

2. **Stash changes:**
   ```bash
   cd worktree-path
   git stash push -m "Saved before worktree removal"
   # Stash is available in main repo

   git worktree remove $(pwd)
   ```

3. **Force remove (lose changes):**
   ```bash
   git worktree remove --force worktree-path
   # ⚠️ WARNING: All uncommitted changes lost!
   ```

---

### Error: "Worktree locked"

**Full Error:**
```
error: 'worktree-path' is locked; use 'unlock' to override, or 'remove --force'
```

**Cause:**
Worktree manually locked to prevent removal.

**Solutions:**

1. **Unlock and remove:**
   ```bash
   git worktree unlock worktree-path
   git worktree remove worktree-path
   ```

2. **Force remove:**
   ```bash
   git worktree remove --force worktree-path
   ```

3. **Check why locked:**
   ```bash
   cat .git/worktrees/branch-name/locked
   # Shows reason for lock
   ```

---

## Advanced Debugging

### Diagnostic Commands

**Check worktree health:**
```bash
# List all worktrees
git worktree list

# Check git database
git fsck

# Verify repository integrity
git status
git branch -vv

# Check worktree administrative files
ls -la .git/worktrees/

# Detailed worktree info
git worktree list --porcelain
```

**Debug specific worktree:**
```bash
cd worktree-path

# Check git configuration
git config --list --local

# Check remote tracking
git branch -vv

# Check what's tracked
git ls-files

# Check for corruption
git fsck --full
```

---

### Enable Debug Logging

**Git verbose mode:**
```bash
GIT_TRACE=1 git worktree add ../debug -b debug
# Shows all git commands executed
```

**Trace specific operations:**
```bash
# Trace file operations
GIT_TRACE_PACK_ACCESS=1 git status

# Trace setup
GIT_TRACE_SETUP=1 git worktree list

# Trace performance
GIT_TRACE_PERFORMANCE=1 git status
```

---

### Recovery Procedures

**Recover deleted worktree:**
```bash
# If worktree removed but branch still exists
git worktree add ../recovered branch-name

# If branch deleted too
git reflog  # Find commit
git worktree add ../recovered commit-hash
git checkout -b branch-name
```

**Recover from backup:**
```bash
# If you have time machine / backup
cp -r /backup/path/to/worktree /current/path/

# Repair git references
git worktree repair
```

**Nuclear option - start fresh:**
```bash
# Backup important changes
cp -r worktree-path/src ~/backup/

# Remove all worktrees
git worktree list | grep -v "$(git rev-parse --show-toplevel)" | \
  awk '{print $1}' | xargs -I{} git worktree remove --force {}

# Clean up administrative files
git worktree prune

# Recreate from scratch
git worktree add ../fresh-start branch-name

# Restore backed up changes
cp -r ~/backup/* ../fresh-start/src/
```

---

## Getting Help

### Before Asking for Help

**Collect diagnostic information:**
```bash
#!/bin/bash
# worktree-diagnostics.sh

echo "=== Git Version ==="
git --version

echo -e "\n=== Worktree List ==="
git worktree list

echo -e "\n=== Repository Status ==="
git status

echo -e "\n=== Branch Info ==="
git branch -vv

echo -e "\n=== Remote Info ==="
git remote -v

echo -e "\n=== Worktree Admin Files ==="
ls -la .git/worktrees/

echo -e "\n=== Disk Space ==="
df -h .

echo -e "\n=== File Permissions ==="
ls -ld .git
ls -ld .git/worktrees/

# Save to file
# ./worktree-diagnostics.sh > diagnostics.txt
```

### Common Support Channels

- **Git Documentation:** `git help worktree`
- **GitHub Issues:** Check git/git repository
- **Stack Overflow:** Tag: `git-worktree`
- **Git Mailing List:** git@vger.kernel.org

---

## Quick Reference

### Most Common Issues

1. **Directory exists:** `rm -rf path && git worktree add path branch`
2. **Branch checked out:** `git worktree remove old-path && git worktree add new-path branch`
3. **Orphaned worktree:** `git worktree prune`
4. **Permission denied:** `chmod 755 parent-dir`
5. **Can't remove (dirty):** `git stash && git worktree remove path`

### Essential Commands

```bash
# Diagnose
git worktree list
git fsck
git worktree prune

# Repair
git worktree repair
git worktree unlock path

# Force operations (use with caution)
git worktree remove --force path
git branch -D branch-name
```

---

## Summary

Most git worktree issues fall into these categories:
1. **Creation conflicts** - Directory or branch conflicts
2. **Permission issues** - Filesystem restrictions
3. **Corruption** - Manual deletions or crashes
4. **Cleanup problems** - Uncommitted changes or locks

**General troubleshooting approach:**
1. Read error message carefully
2. Check `git worktree list` for current state
3. Use `git worktree prune` to clean orphans
4. Use `--force` flags only when necessary
5. Document unusual issues for team

**Remember:** Git worktrees are just checkouts in different directories. Most git commands work the same way - when in doubt, treat it like a normal git repository!
