# Mode 1: Git Worktree Isolation

## When to Use

**Best for:**
- Read-only skills or skills with minimal file operations
- Quick validation during development
- Skills that don't require system package installation
- Testing iterations where speed matters

**Not suitable for:**
- Skills that install system packages (npm install, apt-get, brew, etc.)
- Skills that modify system configurations
- Skills that require a clean Node.js environment

**Risk Level**: Low complexity skills only

## Advantages

- ⚡ **Fast**: Creates worktree in seconds
- 💾 **Efficient**: Shares git history, minimal disk space
- 🔄 **Repeatable**: Easy to create, test, and destroy
- 🛠️ **Familiar**: Same git tools you already know

## Limitations

- ❌ Shares system packages (node_modules, global npm packages)
- ❌ Shares environment variables and configs
- ❌ Same OS user and permissions
- ❌ Cannot test system-level dependencies
- ⚠️ Not true isolation - just a separate git checkout

## Prerequisites

1. Must be in a git repository
2. Git worktree feature available (Git 2.5+)
3. Clean working directory (or willing to proceed with uncommitted changes)
4. Sufficient disk space for additional worktree

## Workflow

### Step 1: Validate Environment

```bash
# Check if in git repo
git rev-parse --is-inside-work-tree

# Check for uncommitted changes
git status --porcelain

# Get current repo name
basename $(git rev-parse --show-toplevel)
```

If dirty working directory → warn user but allow proceeding (isolation is separate)

### Step 2: Create Isolation Worktree

**Generate unique branch name:**
```bash
BRANCH_NAME="test-skill-$(date +%s)"  # e.g., test-skill-1699876543
```

**Create worktree:**
```bash
WORKTREE_PATH="../$(basename $(pwd))-${BRANCH_NAME}"
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
```

Example result: `/Users/connor/claude-test-skill-1699876543/`

### Step 3: Copy Skill to Worktree

```bash
# Copy skill directory to worktree's .claude/skills/
cp -r ~/.claude/skills/[skill-name] "$WORKTREE_PATH/.claude/skills/"

# Or if skill is in current repo
cp -r ./skills/[skill-name] "$WORKTREE_PATH/.claude/skills/"
```

**Verify copy:**
```bash
ls -la "$WORKTREE_PATH/.claude/skills/[skill-name]/"
```

### Step 4: Setup Development Environment

**Install dependencies if needed:**
```bash
cd "$WORKTREE_PATH"

# Detect package manager
if [ -f "pnpm-lock.yaml" ]; then
  pnpm install
elif [ -f "yarn.lock" ]; then
  yarn install
elif [ -f "package-lock.json" ]; then
  npm install
fi
```

**Copy environment files (optional):**
```bash
# Only if skill needs .env for testing
cp ../.env "$WORKTREE_PATH/.env"
```

### Step 5: Take "Before" Snapshot

```bash
# List all files in worktree
find "$WORKTREE_PATH" -type f > /tmp/before-files.txt

# List running processes (for comparison later)
ps aux > /tmp/before-processes.txt

# Current disk usage
du -sh "$WORKTREE_PATH" > /tmp/before-disk.txt
```

### Step 6: Execute Skill in Worktree

**Open new Claude Code session in worktree:**
```bash
cd "$WORKTREE_PATH"
claude
```

**Run skill with test trigger:**
- User manually tests skill with trigger phrases
- OR: Use Claude CLI to run skill programmatically (if available)

**Monitor execution:**
- Watch for errors in output
- Note execution time
- Check resource usage

### Step 7: Take "After" Snapshot

```bash
# List all files after execution
find "$WORKTREE_PATH" -type f > /tmp/after-files.txt

# Compare before/after
diff /tmp/before-files.txt /tmp/after-files.txt > /tmp/file-changes.txt

# Check for new processes
ps aux > /tmp/after-processes.txt
diff /tmp/before-processes.txt /tmp/after-processes.txt > /tmp/process-changes.txt

# Check disk usage
du -sh "$WORKTREE_PATH" > /tmp/after-disk.txt
```

### Step 8: Analyze Results

**Check for side effects:**
```bash
# Files created
grep ">" /tmp/file-changes.txt | wc -l

# Files deleted
grep "<" /tmp/file-changes.txt | wc -l

# New processes (filter out expected ones)
# Look for processes related to skill
```

**Validate cleanup:**
```bash
# Check for leftover temp files
find "$WORKTREE_PATH" -name "*.tmp" -o -name "*.temp" -o -name ".cache"

# Check for orphaned processes
# Look for processes still running from skill
```

### Step 9: Generate Report

**Execution Results:**
- ✅ Skill completed successfully / ❌ Skill failed with error
- ⏱️ Execution time: Xs
- 📊 Resource usage: XMB disk, X% CPU

**Side Effects:**
- Files created: [count] (list if < 10)
- Files modified: [count]
- Processes created: [count]
- Temporary files remaining: [count]

**Dependency Analysis:**
- Required tools: [list tools used by skill]
- Hardcoded paths: [list any absolute paths found]
- Environment variables: [list any ENV vars referenced]

### Step 10: Cleanup

**Ask user:**
```
Test complete. Worktree location: $WORKTREE_PATH

Options:
1. Keep worktree for debugging
2. Remove worktree and branch
3. Remove worktree, keep branch

Your choice?
```

**Cleanup commands:**
```bash
# Option 2: Full cleanup
git worktree remove "$WORKTREE_PATH"
git branch -D "$BRANCH_NAME"

# Option 3: Keep branch
git worktree remove "$WORKTREE_PATH"
```

## Interpreting Results

### ✅ **PASS** - Ready for git worktree environments
- Skill completed without errors
- No unexpected file modifications
- No orphaned processes
- No hardcoded paths detected
- Temporary files cleaned up

### ⚠️ **WARNING** - Works but has minor issues
- Skill works but left temporary files
- Uses some hardcoded paths (but non-critical)
- Performance could be improved
- Missing some documentation

### ❌ **FAIL** - Not ready
- Skill crashed or hung
- Requires system packages not installed
- Modifies files outside skill directory without permission
- Creates orphaned processes
- Has critical hardcoded paths

## Common Issues

### Issue: "Skill not found in Claude"
**Cause**: Skill wasn't copied to worktree's .claude/skills/
**Fix**: Verify copy command and path

### Issue: "Permission denied" errors
**Cause**: Skill trying to write to protected directories
**Fix**: Identify problematic paths, suggest using /tmp or skill directory

### Issue: "Command not found"
**Cause**: Skill depends on system tool not installed
**Fix**: Document dependency, suggest adding to skill README

### Issue: Test results different from main directory
**Cause**: Different node_modules or configs
**Fix**: This is expected - worktree shares some state, not true isolation

## Best Practices

1. **Always take before/after snapshots** for accurate comparison
2. **Test multiple times** to ensure consistency
3. **Check temp directories** (`/tmp`, `/var/tmp`) for leftover files
4. **Monitor processes** for at least 30s after skill completes
5. **Document all dependencies** found during testing
6. **Use relative paths** in skill code, never absolute
7. **Cleanup worktrees** regularly to avoid clutter

## Quick Command Reference

```bash
# Create test worktree
git worktree add ../test-branch -b test-branch

# List all worktrees
git worktree list

# Remove worktree
git worktree remove ../test-branch

# Remove worktree and branch
git worktree remove ../test-branch && git branch -D test-branch

# Find temp files created
find /tmp -name "*skill-name*" -mtime -1
```

---

**Remember:** Git worktree provides quick, lightweight isolation but is NOT true isolation. Use for low-risk skills or fast iteration during development. For skills that modify system state, use Docker or VM modes.
