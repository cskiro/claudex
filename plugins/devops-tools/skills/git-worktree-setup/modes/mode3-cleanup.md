# Mode 3: Worktree Cleanup

## Overview

This mode safely removes git worktrees after work is complete. It includes safety checks for uncommitted changes, optional branch deletion, and cleanup verification.

## When to Use

- User says "remove worktree [name]"
- User wants to "clean up worktrees"
- User mentions "delete" or "cleanup" with "worktree"
- After feature is merged and branch is no longer needed

## Workflow

### Phase 0: Prerequisites & Context

#### Step 0.1: Verify Git Repository

```bash
git rev-parse --is-inside-work-tree
```

**Expected Output:**
```
true
```

**If fails:**
- Stop immediately
- Error: "Not in a git repository"

#### Step 0.2: List Current Worktrees

```bash
git worktree list
```

**Purpose:**
- Show user all available worktrees
- Help identify what to remove
- Detect if worktrees exist

**Expected Output:**
```
/Users/connor/myapp               abc123 [main]
/Users/connor/myapp-feature-a     def456 [feature-a]
/Users/connor/myapp-bugfix-123    ghi789 [bugfix-123]
```

**If only one worktree (main):**
- Message: "No additional worktrees to remove"
- Stop (nothing to cleanup)

---

### Phase 1: Identify Target Worktrees

#### Step 1.1: Determine Cleanup Scope

**Parse user request:**
- "remove worktree **feature-a**" → Single worktree
- "remove **all** worktrees" → All non-main worktrees
- "clean up worktrees" → All or let user select?
- "remove worktree at **/path**" → By path

**Extract:**
- `CLEANUP_MODE`: "single" | "all" | "selective"
- `TARGET`: branch name or path

#### Step 1.2: Map to Worktree Paths

**For single worktree:**
```bash
# If user provided branch name
TARGET_BRANCH="feature-a"
TARGET_PATH=$(git worktree list | grep "\[$TARGET_BRANCH\]" | awk '{print $1}')

# If user provided path
TARGET_PATH="/Users/connor/myapp-feature-a"
TARGET_BRANCH=$(git worktree list | grep "$TARGET_PATH" | grep -oP '\[\K[^\]]+')
```

**Verify target exists:**
```bash
if [ -z "$TARGET_PATH" ]; then
  echo "Error: Worktree not found"
  exit 1
fi
```

**For all worktrees:**
```bash
# Get all non-main worktrees
MAIN_PATH=$(git rev-parse --show-toplevel)
mapfile -t ALL_WORKTREES < <(git worktree list | grep -v "$MAIN_PATH" | awk '{print $1}')
```

#### Step 1.3: Show Cleanup Plan

**For single:**
```
Planning to remove:
  Branch: feature-a
  Path: /Users/connor/myapp-feature-a
  Status: [to be determined in next step]
```

**For all:**
```
Planning to remove all worktrees:
  feature-a → /Users/connor/myapp-feature-a
  bugfix-123 → /Users/connor/myapp-bugfix-123

Main worktree will be preserved:
  main → /Users/connor/myapp
```

**Confirm:**
"Proceed with cleanup? (yes/no)"

---

### Phase 2: Safety Checks

#### Step 2.1: Check for Uncommitted Changes

**For each target worktree:**
```bash
cd "$WORKTREE_PATH"
CHANGES=$(git status --porcelain)

if [ -n "$CHANGES" ]; then
  echo "⚠️  Uncommitted changes detected"
  git status --short
fi
```

**If changes found:**
```
⚠️  Warning: feature-a has uncommitted changes:

M  src/auth.ts
?? src/new-file.ts

Options:
1. Abort cleanup (save your work first)
2. Show diff and decide
3. Continue anyway (DANGER: changes will be lost)
4. Stash changes automatically
```

**Recommended:** Abort and let user save work

**If user chooses stash:**
```bash
cd "$WORKTREE_PATH"
git stash push -m "Auto-stash before worktree removal $(date)"
STASH_CREATED=true
```

**Record stash location:**
```
✓ Changes stashed in main repository
  To recover: git stash list
  Stash name: stash@{0}: Auto-stash before worktree removal...
```

#### Step 2.2: Check Branch Merge Status

**Determine if branch is merged:**
```bash
BRANCH_NAME=$(cd "$WORKTREE_PATH" && git branch --show-current)
BASE_BRANCH="main"  # or detect from git config

# Check if merged to base
if git branch --merged "$BASE_BRANCH" | grep -q "$BRANCH_NAME"; then
  MERGE_STATUS="merged"
else
  MERGE_STATUS="unmerged"
fi
```

**Report status:**
```
Branch status:
  ✓ feature-a: Merged to main
  ⚠️  bugfix-123: NOT merged to main
```

**If unmerged:**
```
⚠️  Warning: bugfix-123 is not merged to main

Unmerged commits:
  [Show last few commits unique to this branch]

Options:
1. Abort cleanup (merge first)
2. Create backup branch (bugfix-123-backup)
3. Continue and delete branch
4. Remove worktree but keep branch
```

#### Step 2.3: Check Active Processes

**Check if worktree is in use:**
```bash
# Check for running processes in worktree
lsof +D "$WORKTREE_PATH" 2>/dev/null

# Check for open editors
if lsof +D "$WORKTREE_PATH" | grep -q "vim\|nvim\|code\|claude"; then
  echo "⚠️  Active processes detected in worktree"
fi
```

**If processes found:**
```
⚠️  Warning: Processes are using this worktree:
  - VS Code (PID: 12345)
  - Claude Code (PID: 67890)

Please close these applications first, or force cleanup (not recommended).
```

---

### Phase 3: Execute Cleanup

#### Step 3.1: Remove Worktree

**Standard removal:**
```bash
git worktree remove "$WORKTREE_PATH"
```

**If removal fails (locked):**
```bash
# Try with force
git worktree remove --force "$WORKTREE_PATH"
```

**Expected Output:**
```
✓ Removed worktree: /Users/connor/myapp-feature-a
```

**Verify removal:**
```bash
if ! git worktree list | grep -q "$WORKTREE_PATH"; then
  echo "✓ Worktree removed from git"
fi

if [ ! -d "$WORKTREE_PATH" ]; then
  echo "✓ Directory removed"
fi
```

#### Step 3.2: Handle Branch Deletion

**Ask user:**
```
Worktree removed successfully.

Delete branch 'feature-a' too? (yes/no/backup)

Options:
  yes    - Delete branch permanently
  no     - Keep branch (can checkout later)
  backup - Create backup branch before deleting
```

**If yes:**
```bash
git branch -d "$BRANCH_NAME"
```

**If force needed (unmerged):**
```bash
# Warn user first
echo "⚠️  Branch is unmerged. Use -D to force delete."
read -p "Force delete? (yes/no): " force

if [ "$force" == "yes" ]; then
  git branch -D "$BRANCH_NAME"
fi
```

**If backup:**
```bash
# Create backup branch
BACKUP_NAME="${BRANCH_NAME}-backup-$(date +%Y%m%d)"
git branch "$BACKUP_NAME" "$BRANCH_NAME"

echo "✓ Created backup: $BACKUP_NAME"

# Then delete original
git branch -d "$BRANCH_NAME"
```

#### Step 3.3: Cleanup Verification

**Verify complete removal:**
```bash
# Check worktree list
if git worktree list | grep -q "$WORKTREE_PATH"; then
  echo "✗ Worktree still in git worktree list"
  ERROR=true
fi

# Check directory
if [ -d "$WORKTREE_PATH" ]; then
  echo "✗ Directory still exists"
  ERROR=true
fi

# Check branch (if deleted)
if [ "$DELETE_BRANCH" == "yes" ]; then
  if git branch | grep -q "$BRANCH_NAME"; then
    echo "✗ Branch still exists"
    ERROR=true
  fi
fi
```

**Success confirmation:**
```
✓ Cleanup verified:
  ✓ Worktree removed from git
  ✓ Directory deleted
  ✓ Branch deleted (if requested)
```

---

### Phase 4: Batch Cleanup (If Multiple Worktrees)

**For cleanup mode "all":**

#### Step 4.1: Process Each Worktree

```bash
REMOVED=()
FAILED=()
KEPT_BRANCHES=()
DELETED_BRANCHES=()

for worktree in "${ALL_WORKTREES[@]}"; do
  echo "Processing: $worktree"

  # Get branch name
  BRANCH=$(git worktree list | grep "$worktree" | grep -oP '\[\K[^\]]+')

  # Safety checks
  cd "$worktree"
  if [ -n "$(git status --porcelain)" ]; then
    echo "  ⚠️  Uncommitted changes - skipping"
    FAILED+=("$worktree (uncommitted changes)")
    continue
  fi

  # Remove worktree
  if git worktree remove "$worktree"; then
    REMOVED+=("$worktree")
    echo "  ✓ Removed"

    # Ask about branch (or use default policy)
    if git branch --merged main | grep -q "$BRANCH"; then
      git branch -d "$BRANCH"
      DELETED_BRANCHES+=("$BRANCH")
      echo "  ✓ Deleted merged branch: $BRANCH"
    else
      KEPT_BRANCHES+=("$BRANCH")
      echo "  ℹ️  Kept unmerged branch: $BRANCH"
    fi
  else
    FAILED+=("$worktree")
    echo "  ✗ Failed"
  fi
done
```

#### Step 4.2: Batch Cleanup Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Batch Cleanup Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Removed: ${#REMOVED[@]} worktrees
Failed:  ${#FAILED[@]} worktrees

Successfully removed:
  ✓ /Users/connor/myapp-feature-a
  ✓ /Users/connor/myapp-feature-b

Failed to remove:
  ✗ /Users/connor/myapp-bugfix-123 (uncommitted changes)

Branches deleted:
  ✓ feature-a (merged)
  ✓ feature-b (merged)

Branches kept:
  ℹ️  bugfix-123 (unmerged)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Phase 5: Post-Cleanup Actions

#### Step 5.1: Show Remaining Worktrees

```bash
git worktree list
```

**Output:**
```
Remaining worktrees:
  /Users/connor/myapp (main) ← current
  /Users/connor/myapp-bugfix-123 (bugfix-123) ← has uncommitted changes
```

#### Step 5.2: Cleanup Orphaned References

**Prune removed worktrees:**
```bash
git worktree prune
```

**Purpose:**
- Remove administrative files for deleted worktrees
- Clean up .git/worktrees directory

**Output:**
```
✓ Pruned orphaned worktree references
```

#### Step 5.3: Show Recovery Information

**If changes were stashed:**
```
📦 Stashed Changes:

Your uncommitted changes are saved in git stash:
  Stash: stash@{0}
  Message: Auto-stash before worktree removal 2025-09-04

To recover:
  git stash list          # List all stashes
  git stash show stash@{0}  # Preview changes
  git stash pop stash@{0}   # Apply and remove stash
  git stash apply stash@{0} # Apply but keep stash
```

**If branches were backed up:**
```
💾 Backed Up Branches:

Created backup branches before deletion:
  feature-a-backup-20250904
  feature-b-backup-20250904

To restore:
  git checkout feature-a-backup-20250904
  git branch feature-a  # Recreate original branch

To remove backups:
  git branch -D feature-a-backup-20250904
```

#### Step 5.4: Disk Space Reclaimed

**Calculate space saved:**
```bash
# Estimate space freed (approximate)
echo "Disk space reclaimed: ~$(du -sh $WORKTREE_PATH 2>/dev/null || echo 'N/A')"
```

**Show before/after:**
```
Disk Space Summary:
  Before: 2.4 GB (3 worktrees)
  After:  800 MB (1 worktree)
  Reclaimed: ~1.6 GB
```

---

## Safety Protocols

### Before Removal

**Mandatory checks:**
- [ ] Worktree exists in git worktree list
- [ ] Not removing main/current worktree
- [ ] Checked for uncommitted changes
- [ ] Checked for unmerged commits
- [ ] Confirmed with user

### During Removal

**Safe removal process:**
- [ ] Use `git worktree remove` (not rm -rf)
- [ ] Verify removal succeeded
- [ ] Handle locked worktrees appropriately
- [ ] Preserve stashes if needed

### After Removal

**Verification:**
- [ ] Worktree not in git worktree list
- [ ] Directory removed
- [ ] Branch handled per user request
- [ ] Stashes accessible (if created)
- [ ] Backups created (if requested)

---

## Error Handling

### Error: Uncommitted Changes

```
Error: Cannot remove worktree with uncommitted changes

Current changes in feature-a:
  M  src/auth.ts
  ?? src/new-file.ts

Solutions:
1. Commit changes:
   cd /path/to/worktree
   git add .
   git commit -m "Save work"

2. Stash changes:
   Let me stash them automatically

3. Force remove (DANGER):
   Changes will be lost forever
```

### Error: Worktree Locked

```
Error: Worktree is locked

Reason: Usually means processes are using it

Solutions:
1. Close all applications using this worktree
2. Check: lsof +D /path/to/worktree
3. Force remove: git worktree remove --force
```

### Error: Branch Checkout Elsewhere

```
Error: Cannot delete branch - checked out elsewhere

Branch 'feature-a' is checked out at:
  /other/path/to/worktree

Solution:
1. Remove that worktree first
2. Or skip branch deletion (keep branch)
```

### Error: Unmerged Commits

```
Error: Branch has unmerged commits

Commits not in main:
  abc123 feat: Add new feature
  def456 fix: Bug fix

Options:
1. Merge first: git merge feature-a
2. Create backup: feature-a-backup
3. Force delete: git branch -D feature-a
```

---

## Advanced Features

### Feature 1: Smart Cleanup

**Auto-detect removable worktrees:**
```bash
# Find merged branches
git for-each-ref --format='%(refname:short)' refs/heads/ |
  while read branch; do
    if git branch --merged main | grep -q "$branch" &&
       [ "$branch" != "main" ]; then
      echo "Removable: $branch (merged)"
    fi
  done
```

**Offer cleanup:**
```
Found 3 worktrees with merged branches:
  feature-a (merged 3 days ago)
  feature-b (merged 1 week ago)
  bugfix-old (merged 2 weeks ago)

Clean up all merged worktrees? (yes/select/no)
```

### Feature 2: Archive Instead of Delete

**Create archive before removal:**
```bash
ARCHIVE_DIR="$HOME/.git-worktree-archives"
ARCHIVE_NAME="${BRANCH_NAME}-$(date +%Y%m%d-%H%M%S).tar.gz"

# Archive worktree
tar -czf "$ARCHIVE_DIR/$ARCHIVE_NAME" -C "$(dirname $WORKTREE_PATH)" "$(basename $WORKTREE_PATH)"

echo "✓ Archived to: $ARCHIVE_DIR/$ARCHIVE_NAME"
echo "  To restore: tar -xzf $ARCHIVE_NAME"
```

### Feature 3: Cleanup Report

**Generate detailed report:**
```markdown
# Worktree Cleanup Report
Date: 2025-09-04 15:30:00

## Removed Worktrees
- feature-a (merged, 15 commits, 3 days old)
- feature-b (merged, 8 commits, 1 week old)

## Branches Deleted
- feature-a (merged to main)
- feature-b (merged to main)

## Disk Space Reclaimed
- Total: 1.6 GB
- Per worktree: ~800 MB

## Stashes Created
- stash@{0}: Auto-stash feature-a
- stash@{1}: Auto-stash feature-b

## Recommendations
- Review stashes and apply if needed
- Consider cleanup policy for future
- Monitor disk usage regularly
```

---

## Stop Conditions

**Stop immediately if:**
- [ ] Not in a git repository
- [ ] Target worktree doesn't exist
- [ ] User cancels during confirmation
- [ ] Trying to remove main worktree
- [ ] Uncommitted changes and user aborts

**Continue with warnings if:**
- [ ] Some worktrees fail in batch mode
- [ ] Branch deletion fails
- [ ] Prune operation fails

---

## Success Criteria

- [ ] Worktree removed from git worktree list
- [ ] Directory deleted from filesystem
- [ ] Branch handled per user request (deleted/kept/backed up)
- [ ] No uncommitted changes lost
- [ ] Cleanup verified
- [ ] Recovery information provided (if applicable)

---

## Example: Complete Flow

```
User: Remove the feature-authentication worktree

Claude:
Checking worktree: feature-authentication
Location: /Users/connor/myapp-feature-authentication

Safety checks:
  ✓ No uncommitted changes
  ✓ Branch merged to main
  ✓ No active processes

Proceed with removal? (yes/no)

User: yes

Claude:
Removing worktree...
  ✓ Worktree removed from git
  ✓ Directory deleted

Delete branch 'feature-authentication' too? (yes/no/backup)

User: yes

Claude:
  ✓ Branch deleted (was merged to main)

Cleanup complete!

Remaining worktrees:
  /Users/connor/myapp (main) ← current

Disk space reclaimed: ~800 MB
```
