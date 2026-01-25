# Mode 2: Batch Worktree Creation

## Overview

This mode creates multiple git worktrees in a single operation. Use this when the user wants to work on several branches simultaneously or needs to set up multiple environments at once.

## When to Use

- User mentions "multiple worktrees"
- User provides comma-separated list of branches
- User says "set up worktrees for X, Y, and Z"
- User wants to create worktrees for multiple PRs/issues

## Workflow

### Phase 0: Prerequisites & Validation

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
- Error: "Not in a git repository. Please navigate to your project root and try again."

#### Step 0.2: Get Repository Information

```bash
# Get repository name
REPO_NAME=$(basename $(git rev-parse --show-toplevel))

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
```

#### Step 0.3: Check Working Directory Status

```bash
git status --porcelain
```

**If output exists:**
- **Warning:** "You have uncommitted changes. This won't affect worktree creation, but be aware."
- Continue (batch operations should be robust)

#### Step 0.4: List Current Worktrees

```bash
git worktree list
```

**Purpose:**
- Show baseline state
- Detect potential conflicts
- Track for final summary

---

### Phase 1: Gather Information

#### Step 1.1: Extract Branch List

**From user request patterns:**
- "create worktrees for **feature-a, feature-b, feature-c**"
- "set up worktrees for **bug-123, bug-456**"
- "I need worktrees for **feat-x and feat-y**"

**Parse into array:**
```bash
BRANCHES=("feature-a" "feature-b" "feature-c")
```

**Normalize:**
- Trim whitespace
- Remove "and", commas
- Handle various separators

**Validate:**
- Must have at least 2 branches
- If 1 branch → Redirect to Mode 1
- If 0 branches → Ask user

#### Step 1.2: Determine Branch Types

**For each branch, check existence:**
```bash
for branch in "${BRANCHES[@]}"; do
  if git show-ref --verify refs/heads/$branch 2>/dev/null; then
    BRANCH_TYPES[$branch]="existing"
  else
    BRANCH_TYPES[$branch]="new"
  fi
done
```

**Show summary:**
```
Planning to create 3 worktrees:
  feature-a (new)
  feature-b (existing)
  feature-c (new)
```

**Confirm with user:**
"Create these worktrees? (yes/no)"

#### Step 1.3: Determine Locations

**For each branch, generate default location:**
```bash
for branch in "${BRANCHES[@]}"; do
  LOCATIONS[$branch]="../$REPO_NAME-$branch"
done
```

**Show locations:**
```
Worktree locations:
  feature-a → ../myapp-feature-a
  feature-b → ../myapp-feature-b
  feature-c → ../myapp-feature-c
```

**Ask:**
"Use these locations? (yes/customize)"

**If customize:**
- Ask for pattern or specific paths
- Support patterns like `../worktrees/{branch}`

#### Step 1.4: Check Directory Conflicts

```bash
CONFLICTS=()
for branch in "${BRANCHES[@]}"; do
  location="${LOCATIONS[$branch]}"
  if [ -d "$location" ]; then
    CONFLICTS+=("$branch → $location")
  fi
done
```

**If conflicts:**
```
Warning: These directories already exist:
  feature-a → ../myapp-feature-a
  feature-c → ../myapp-feature-c

Options:
1. Skip conflicting worktrees
2. Remove and recreate
3. Use different locations
```

**Handle based on user choice**

#### Step 1.5: Development Environment Setup

**Ask once for all worktrees:**
"Setup development environment in all worktrees? (yes/no)"

**Default:** yes (if package.json exists)

**Store:**
- `SETUP_DEV_ALL`: true/false

---

### Phase 2: Create Worktrees (Parallel Processing)

#### Step 2.1: Create Execution Plan

**Build command list:**
```bash
COMMANDS=()
for branch in "${BRANCHES[@]}"; do
  location="${LOCATIONS[$branch]}"
  branch_type="${BRANCH_TYPES[$branch]}"

  if [ "$branch_type" == "new" ]; then
    COMMANDS+=("git worktree add $location -b $branch")
  else
    COMMANDS+=("git worktree add $location $branch")
  fi
done
```

**Show plan:**
```
Execution plan:
1. git worktree add ../myapp-feature-a -b feature-a
2. git worktree add ../myapp-feature-b feature-b
3. git worktree add ../myapp-feature-c -b feature-c
```

#### Step 2.2: Execute Worktree Creations

**Sequential execution with progress tracking:**

```bash
CREATED=()
FAILED=()
TOTAL=${#BRANCHES[@]}
CURRENT=0

for branch in "${BRANCHES[@]}"; do
  ((CURRENT++))
  echo "[$CURRENT/$TOTAL] Creating worktree for $branch..."

  location="${LOCATIONS[$branch]}"
  branch_type="${BRANCH_TYPES[$branch]}"

  # Execute creation
  if [ "$branch_type" == "new" ]; then
    if git worktree add "$location" -b "$branch" 2>&1; then
      CREATED+=("$branch")
      echo "  ✓ Success: $branch"
    else
      FAILED+=("$branch")
      echo "  ✗ Failed: $branch"
    fi
  else
    if git worktree add "$location" "$branch" 2>&1; then
      CREATED+=("$branch")
      echo "  ✓ Success: $branch"
    else
      FAILED+=("$branch")
      echo "  ✗ Failed: $branch"
    fi
  fi
done
```

**Progress output:**
```
[1/3] Creating worktree for feature-a...
  ✓ Success: feature-a

[2/3] Creating worktree for feature-b...
  ✓ Success: feature-b

[3/3] Creating worktree for feature-c...
  ✗ Failed: feature-c (branch already checked out)
```

#### Step 2.3: Verify Creations

```bash
git worktree list
```

**Count created worktrees:**
```bash
VERIFIED=0
for branch in "${CREATED[@]}"; do
  location="${LOCATIONS[$branch]}"
  if git worktree list | grep -q "$location"; then
    ((VERIFIED++))
  fi
done
```

**Report:**
```
Verification: $VERIFIED/$TOTAL worktrees created successfully
```

#### Step 2.4: Handle Failures

**If any failed:**
```
Failed to create worktrees for:
  feature-c: Branch already checked out at /other/path

Options:
1. Continue with successful worktrees
2. Retry failed worktrees
3. Clean up and start over
```

**Recommended:** Continue with successful ones

---

### Phase 3: Setup Development Environments (Batch)

**Only if `SETUP_DEV_ALL` is true**

#### Step 3.1: Detect Package Manager

```bash
# Check in repository root (same for all worktrees)
if [ -f "pnpm-lock.yaml" ]; then
  PKG_MANAGER="pnpm"
  INSTALL_CMD="pnpm install"
elif [ -f "yarn.lock" ]; then
  PKG_MANAGER="yarn"
  INSTALL_CMD="yarn install"
elif [ -f "bun.lockb" ]; then
  PKG_MANAGER="bun"
  INSTALL_CMD="bun install"
elif [ -f "package-lock.json" ]; then
  PKG_MANAGER="npm"
  INSTALL_CMD="npm install"
else
  PKG_MANAGER="npm"
  INSTALL_CMD="npm install"
fi
```

**Output:**
```
Using $PKG_MANAGER for all worktrees
```

#### Step 3.2: Install Dependencies (Parallel)

**For each created worktree:**
```bash
INSTALL_SUCCESS=()
INSTALL_FAILED=()

for branch in "${CREATED[@]}"; do
  location="${LOCATIONS[$branch]}"
  echo "Installing dependencies in $branch..."

  # Run in subshell
  (
    cd "$location" && $INSTALL_CMD > /tmp/install-$branch.log 2>&1
  ) &

  # Store PID for tracking
  INSTALL_PIDS[$branch]=$!
done

# Wait for all installations
for branch in "${CREATED[@]}"; do
  pid=${INSTALL_PIDS[$branch]}
  if wait $pid; then
    INSTALL_SUCCESS+=("$branch")
    echo "  ✓ $branch: Dependencies installed"
  else
    INSTALL_FAILED+=("$branch")
    echo "  ✗ $branch: Installation failed (see /tmp/install-$branch.log)"
  fi
done
```

**Progress:**
```
Installing dependencies in all worktrees...

  ✓ feature-a: Dependencies installed (12.3s)
  ✓ feature-b: Dependencies installed (11.8s)
  ✗ feature-c: Installation failed (network error)

Successfully installed: 2/3
```

#### Step 3.3: Copy Environment Files (Optional)

**Check for .env:**
```bash
if [ -f ".env" ]; then
  echo "Found .env file"
  read -p "Copy .env to all worktrees? (yes/no): " copy_env

  if [ "$copy_env" == "yes" ]; then
    for branch in "${CREATED[@]}"; do
      location="${LOCATIONS[$branch]}"
      cp .env "$location/.env"
      echo "  ✓ Copied .env to $branch"
    done
  fi
fi
```

#### Step 3.4: Summary of Dev Setup

```
Development Environment Setup Complete:

  feature-a:
    ✓ Dependencies installed ($PKG_MANAGER)
    ✓ Environment ready

  feature-b:
    ✓ Dependencies installed ($PKG_MANAGER)
    ✓ Environment ready

  feature-c:
    ✗ Skipped (worktree creation failed)
```

---

### Phase 4: Provide Comprehensive Guidance

#### Step 4.1: Generate Summary Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Batch Worktree Creation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created: ${#CREATED[@]}/${#BRANCHES[@]} worktrees
Failed:  ${#FAILED[@]}/${#BRANCHES[@]} worktrees

Success:
  ✓ feature-a → ../myapp-feature-a (new branch)
  ✓ feature-b → ../myapp-feature-b (existing branch)

Failed:
  ✗ feature-c: Branch already checked out

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Step 4.2: Provide Navigation Commands

**For each successful worktree:**
```
Start working on feature-a:
  cd ../myapp-feature-a
  claude

Start working on feature-b:
  cd ../myapp-feature-b
  claude
```

#### Step 4.3: Show All Worktrees

```bash
git worktree list
```

**Format:**
```
All Worktrees:
  /Users/connor/myapp               (main)          ← current
  /Users/connor/myapp-feature-a     (feature-a)     ← new
  /Users/connor/myapp-feature-b     (feature-b)     ← new
```

#### Step 4.4: Provide Batch Management Commands

```
Batch Management:

  List all worktrees:
    git worktree list

  Remove specific worktree:
    git worktree remove ../myapp-feature-a

  Remove all new worktrees:
    git worktree remove ../myapp-feature-a
    git worktree remove ../myapp-feature-b

  Generate cleanup script:
    Would you like me to create a cleanup script?
```

#### Step 4.5: Offer Script Generation

**Ask user:**
"Generate a script to manage these worktrees? (yes/no)"

**If yes, create:**
- Start scripts for each worktree
- Cleanup script for all worktrees
- Status check script

---

### Phase 5: Post-Creation Verification

#### Step 5.1: Comprehensive Verification

```bash
# Verify all created worktrees
for branch in "${CREATED[@]}"; do
  location="${LOCATIONS[$branch]}"

  # Check in worktree list
  if ! git worktree list | grep -q "$location"; then
    echo "✗ $branch: Not in worktree list"
    continue
  fi

  # Check directory exists
  if [ ! -d "$location" ]; then
    echo "✗ $branch: Directory not found"
    continue
  fi

  # Check .git file
  if [ ! -f "$location/.git" ]; then
    echo "✗ $branch: Missing .git file"
    continue
  fi

  # Check has files
  if [ -z "$(ls -A $location)" ]; then
    echo "✗ $branch: Empty directory"
    continue
  fi

  echo "✓ $branch: All checks passed"
done
```

#### Step 5.2: Success Checklist

```
Verification Results:

feature-a:
  ✓ Worktree in git worktree list
  ✓ Directory exists with files
  ✓ .git file present
  ✓ Development environment ready
  ✓ Ready for Claude Code session

feature-b:
  ✓ Worktree in git worktree list
  ✓ Directory exists with files
  ✓ .git file present
  ✓ Development environment ready
  ✓ Ready for Claude Code session
```

---

## Advanced Features

### Feature 1: Smart Branch Detection

**Auto-detect from PRs:**
```bash
# Get open PR branches
gh pr list --json headRefName --jq '.[].headRefName'
```

**Offer to user:**
"Found 5 open PRs. Create worktrees for all? (yes/select/no)"

### Feature 2: Parallel Claude Code Sessions

**Generate tmux/screen setup:**
```bash
#!/bin/bash
# Start parallel Claude Code sessions

tmux new-session -d -s worktrees

tmux split-window -h
tmux split-window -v

tmux send-keys -t 0 "cd ../myapp-feature-a && claude" C-m
tmux send-keys -t 1 "cd ../myapp-feature-b && claude" C-m
tmux send-keys -t 2 "cd ../myapp && claude" C-m

tmux attach-session -t worktrees
```

### Feature 3: Dependency Sharing

**Optimize with shared node_modules:**
```
Note: Each worktree has separate node_modules.
Disk usage: ~500MB per worktree

Consider using:
  - pnpm (with content-addressable storage)
  - yarn with workspaces
  - Shared cache configurations
```

### Feature 4: Custom Patterns

**Support location patterns:**
```
User: Create worktrees in ~/worktrees/{branch}

Result:
  feature-a → ~/worktrees/feature-a
  feature-b → ~/worktrees/feature-b
  feature-c → ~/worktrees/feature-c
```

---

## Error Handling

### Error: Mixed Success/Failure

**Strategy: Continue with successful ones**

```
2 of 3 worktrees created successfully.

✓ feature-a: Ready
✓ feature-b: Ready
✗ feature-c: Failed (branch conflict)

You can:
1. Start working with feature-a and feature-b
2. Resolve feature-c issue separately
3. Use Mode 1 to retry feature-c
```

### Error: All Creations Failed

```
Failed to create any worktrees.

Common causes:
- Branch names conflict with existing worktrees
- Directories already exist
- Branch doesn't exist and can't create

Review errors above and try again with corrections.
```

### Error: Some Installations Failed

```
Worktrees created but some installations failed:

✓ feature-a: Ready
✗ feature-b: Installation failed (network error)

You can:
1. Use feature-a immediately
2. Manually install in feature-b:
   cd ../myapp-feature-b
   npm install
```

---

## Performance Considerations

### Parallel vs. Sequential

**Worktree Creation:**
- **Sequential** (current approach)
- Reason: Git operations may conflict
- Time: ~1s per worktree

**Dependency Installation:**
- **Parallel** (recommended)
- Reason: Independent operations
- Time: ~12s total (vs. 36s sequential for 3)

### Disk Space

**Estimate before creation:**
```bash
# Repository size
du -sh .

# Per worktree: ~(repo size + node_modules size)
# Example: 50MB + 500MB = 550MB per worktree
# 3 worktrees = 1.65GB
```

**Warn if:**
- Creating > 5 worktrees
- Available disk space < 5GB

---

## Stop Conditions

**Stop immediately if:**
- [ ] Not in a git repository
- [ ] All worktree creations fail
- [ ] User cancels during confirmation

**Continue with warnings if:**
- [ ] Some worktree creations fail (partial success)
- [ ] Dependency installations fail
- [ ] Environment file copy fails

---

## Success Criteria

- [ ] At least one worktree created successfully
- [ ] All created worktrees verified
- [ ] Development environments ready (if requested)
- [ ] User provided with clear next steps for each worktree
- [ ] Summary report generated
- [ ] Cleanup instructions provided

---

## Example: Complete Flow

```
User: Create worktrees for feature-auth, feature-dashboard, and bugfix-login