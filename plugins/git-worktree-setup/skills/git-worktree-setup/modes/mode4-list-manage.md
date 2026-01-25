# Mode 4: List and Manage Worktrees

## Overview

This mode provides visibility into existing worktrees with detailed status information, health checks, and management utilities. Use this for monitoring, troubleshooting, and understanding the current worktree state.

## When to Use

- User says "list worktrees" or "show worktrees"
- User asks "what worktrees do I have?"
- User wants "worktree status"
- User needs to "check worktrees"
- Diagnostic/troubleshooting scenarios

## Workflow

### Phase 0: Prerequisites

#### Step 0.1: Verify Git Repository

```bash
git rev-parse --is-inside-work-tree
```

**Expected Output:**
```
true
```

**If fails:**
- Message: "Not in a git repository"
- Suggest: Navigate to project root
- Stop

---

### Phase 1: Gather Worktree Information

#### Step 1.1: Get Basic Worktree List

```bash
git worktree list
```

**Expected Output:**
```
/Users/connor/myapp               abc123 [main]
/Users/connor/myapp-feature-a     def456 [feature-a]
/Users/connor/myapp-bugfix-123    ghi789 [bugfix-123]
```

**Parse into structured data:**
```bash
while read -r line; do
  PATH=$(echo "$line" | awk '{print $1}')
  COMMIT=$(echo "$line" | awk '{print $2}')
  BRANCH=$(echo "$line" | grep -oP '\[\K[^\]]+')

  WORKTREES["$BRANCH"]="$PATH"
  COMMITS["$BRANCH"]="$COMMIT"
done < <(git worktree list)
```

#### Step 1.2: Enhance with Status Information

**For each worktree:**
```bash
for branch in "${!WORKTREES[@]}"; do
  path="${WORKTREES[$branch]}"

  # Get git status
  cd "$path"
  STATUS=$(git status --porcelain)
  AHEAD_BEHIND=$(git rev-list --left-right --count origin/$branch...$branch 2>/dev/null)

  # Check if clean
  if [ -z "$STATUS" ]; then
    CLEAN[$branch]=true
  else
    CLEAN[$branch]=false
    CHANGE_COUNT[$branch]=$(echo "$STATUS" | wc -l)
  fi

  # Check ahead/behind
  if [ -n "$AHEAD_BEHIND" ]; then
    BEHIND=$(echo "$AHEAD_BEHIND" | awk '{print $1}')
    AHEAD=$(echo "$AHEAD_BEHIND" | awk '{print $2}')
    SYNC[$branch]="behind:$BEHIND ahead:$AHEAD"
  fi

  # Get last commit info
  LAST_COMMIT[$branch]=$(git log -1 --format="%h %s" 2>/dev/null)
  LAST_COMMIT_DATE[$branch]=$(git log -1 --format="%ar" 2>/dev/null)

  # Check if merged
  if git branch --merged main | grep -q "^[* ]*$branch$"; then
    MERGED[$branch]=true
  else
    MERGED[$branch]=false
  fi

  # Check directory size
  SIZE[$branch]=$(du -sh "$path" 2>/dev/null | awk '{print $1}')
done
```

#### Step 1.3: Detect Current Worktree

```bash
CURRENT_PATH=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git branch --show-current)
```

---

### Phase 2: Display Worktree Information

#### Step 2.1: Formatted List View

**Standard view:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Git Worktrees (3 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

● main                                ← current
  /Users/connor/myapp
  Clean working directory
  Up to date with origin/main
  Size: 850 MB

○ feature-a
  /Users/connor/myapp-feature-a
  3 uncommitted changes
  2 commits ahead of origin
  Last commit: feat: Add authentication (2 hours ago)
  Size: 920 MB

○ bugfix-123
  /Users/connor/myapp-bugfix-123
  Clean working directory
  Merged to main
  Last commit: fix: Login redirect (1 day ago)
  Size: 880 MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total disk usage: 2.65 GB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Step 2.2: Detailed View (Optional)

**With --detailed flag or user request:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Worktree: main
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Location:        /Users/connor/myapp
Branch:          main
Commit:          abc123def
Status:          Clean
Sync:            Up to date with origin/main
Last Commit:     chore: Update dependencies (3 hours ago)
Commits:         1,234 total
Contributors:    5 active
Size:            850 MB
Node Modules:    145,234 packages
Created:         3 months ago (2025-06-04)

Health:          ✓ Healthy
  ✓ No uncommitted changes
  ✓ Synced with remote
  ✓ Dependencies installed
  ✓ No conflicts

─────────────────────────────────────────────

Worktree: feature-a
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Location:        /Users/connor/myapp-feature-a
Branch:          feature-a
Base Branch:     main
Commit:          def456ghi
Status:          Modified (3 files)
Sync:            2 commits ahead, 0 behind
Last Commit:     feat: Add authentication (2 hours ago)
Branch Age:      3 days
Size:            920 MB
Node Modules:    145,234 packages

Changes:
  M  src/auth/login.ts
  M  src/auth/register.ts
  ?? src/auth/types.ts

Health:          ⚠️  Needs attention
  ⚠️  Uncommitted changes
  ⚠️  Not pushed to remote
  ✓ Dependencies up to date
  ✓ No conflicts with main

Recommendations:
  - Commit changes: git add . && git commit
  - Push to remote: git push origin feature-a
  - Consider opening PR (3 commits ready)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Step 2.3: Table View

**Compact comparison:**
```
┌─────────────┬──────────────┬────────┬────────┬────────────┐
│ Branch      │ Status       │ Ahead  │ Behind │ Size       │
├─────────────┼──────────────┼────────┼────────┼────────────┤
│ main *      │ Clean        │ 0      │ 0      │ 850 MB     │
│ feature-a   │ Modified (3) │ 2      │ 0      │ 920 MB     │
│ bugfix-123  │ Clean        │ 0      │ 0      │ 880 MB     │
└─────────────┴──────────────┴────────┴────────┴────────────┘

* Current worktree
```

#### Step 2.4: Status Icons

**Visual indicators:**
```
● main             [clean] [synced] [active]
○ feature-a        [modified] [ahead] [needs-push]
○ bugfix-123       [clean] [merged] [ready-to-cleanup]
```

**Icon legend:**
- `●` Current worktree
- `○` Other worktrees
- `✓` Healthy status
- `⚠️` Needs attention
- `✗` Error/problem

---

### Phase 3: Health Checks

#### Step 3.1: Check Worktree Health

**For each worktree:**
```bash
check_health() {
  local path=$1
  local branch=$2
  local issues=()

  cd "$path"

  # Check 1: Uncommitted changes
  if [ -n "$(git status --porcelain)" ]; then
    issues+=("Uncommitted changes")
  fi

  # Check 2: Not synced with remote
  if ! git diff --quiet @{u} 2>/dev/null; then
    issues+=("Out of sync with remote")
  fi

  # Check 3: Merge conflicts
  if git ls-files -u | grep -q .; then
    issues+=("Has merge conflicts")
  fi

  # Check 4: Dependencies outdated
  if [ -f "package.json" ]; then
    if [ ! -d "node_modules" ]; then
      issues+=("Dependencies not installed")
    fi
  fi

  # Check 5: Behind main
  behind=$(git rev-list --count HEAD..main 2>/dev/null)
  if [ "$behind" -gt 10 ]; then
    issues+=("Far behind main ($behind commits)")
  fi

  # Check 6: Stale branch (no activity)
  last_commit_age=$(git log -1 --format=%ct 2>/dev/null)
  current_time=$(date +%s)
  days_old=$(( (current_time - last_commit_age) / 86400 ))
  if [ "$days_old" -gt 30 ]; then
    issues+=("Stale branch ($days_old days old)")
  fi

  if [ ${#issues[@]} -eq 0 ]; then
    echo "✓ Healthy"
  else
    echo "⚠️ Issues: ${issues[*]}"
  fi
}
```

#### Step 3.2: Generate Health Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Worktree Health Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Healthy: 1 worktree
  ✓ main

Needs Attention: 1 worktree
  ⚠️ feature-a
    - Uncommitted changes
    - Not pushed to remote

Ready for Cleanup: 1 worktree
  ○ bugfix-123
    - Merged to main
    - No uncommitted changes
    - Last activity: 1 week ago

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Phase 4: Management Actions

#### Step 4.1: Offer Actions

**Based on worktree states:**
```
Available Actions:

1. Clean up merged worktrees (1 candidate)
2. Sync all worktrees with remote
3. Check for stale worktrees (30+ days)
4. Show disk usage breakdown
5. Generate maintenance script
6. Navigate to specific worktree

What would you like to do?
```

#### Step 4.2: Quick Navigation

**Provide navigation commands:**
```bash
# For each worktree
echo "Navigate to $branch:"
echo "  cd ${WORKTREES[$branch]}"
```

**Example output:**
```
Quick Navigation:

  Main:
    cd /Users/connor/myapp

  Feature A:
    cd /Users/connor/myapp-feature-a

  Bugfix 123:
    cd /Users/connor/myapp-bugfix-123
```

#### Step 4.3: Sync All Worktrees

**If user requests sync:**
```bash
for branch in "${!WORKTREES[@]}"; do
  path="${WORKTREES[$branch]}"
  echo "Syncing $branch..."

  cd "$path"

  # Fetch latest
  git fetch origin

  # Check if can fast-forward
  if git merge-base --is-ancestor HEAD @{u} 2>/dev/null; then
    git merge --ff-only @{u}
    echo "  ✓ Updated to latest"
  else
    echo "  ⚠️ Cannot fast-forward (manual merge needed)"
  fi
done
```

#### Step 4.4: Disk Usage Analysis

```
Disk Usage Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository Files:      150 MB per worktree
Node Modules:          700 MB per worktree
Build Artifacts:       50 MB per worktree
Total per worktree:    ~900 MB

Current worktrees: 3
Total disk usage:  2.65 GB

Potential savings if cleaned up:
  - Remove bugfix-123: Save 880 MB
  - Shared dependencies: Not possible (git worktrees)

Recommendations:
  - Clean up merged branches regularly
  - Use pnpm for better dependency management
  - Remove build artifacts: npm run clean
```

---

### Phase 5: Advanced Features

#### Feature 5.1: Dependency Check

**Check for outdated dependencies:**
```bash
for branch in "${!WORKTREES[@]}"; do
  path="${WORKTREES[$branch]}"
  cd "$path"

  if [ -f "package.json" ]; then
    echo "Checking $branch..."

    # Check if outdated
    outdated=$(npm outdated --json 2>/dev/null || echo "{}")

    if [ "$outdated" != "{}" ]; then
      count=$(echo "$outdated" | jq 'length')
      echo "  ⚠️ $count outdated packages"
    else
      echo "  ✓ Dependencies up to date"
    fi
  fi
done
```

#### Feature 5.2: Find Specific Files

**Search across all worktrees:**
```bash
find_in_worktrees() {
  local filename=$1

  for branch in "${!WORKTREES[@]}"; do
    path="${WORKTREES[$branch]}"

    if [ -f "$path/$filename" ]; then
      echo "$branch: $path/$filename"

      # Show diff from main if different
      if diff -q "$path/$filename" "${WORKTREES[main]}/$filename" &>/dev/null; then
        echo "  (same as main)"
      else
        echo "  (modified from main)"
      fi
    fi
  done
}
```

#### Feature 5.3: Compare Worktrees

**Side-by-side comparison:**
```
Comparing: feature-a vs main
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files changed: 15
  Modified: 12
  Added: 3
  Removed: 0

Commits ahead: 5
  feat: Add authentication
  feat: Add user registration
  test: Add auth tests
  docs: Update API docs
  chore: Update dependencies

Lines changed:
  +450 additions
  -120 deletions

Dependencies changed: 3
  + passport@0.6.0
  + bcrypt@5.1.0
  + jsonwebtoken@9.0.0
```

#### Feature 5.4: Activity Timeline

**Show recent activity across worktrees:**
```
Recent Activity Across All Worktrees:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Today:
  feature-a: feat: Add authentication (2 hours ago)
  main: chore: Update dependencies (3 hours ago)

Yesterday:
  bugfix-123: fix: Login redirect (1 day ago)

This Week:
  feature-a: Created worktree (3 days ago)

Last Week:
  bugfix-123: Created worktree (8 days ago)
```

---

### Phase 6: Generate Management Scripts

#### Script 6.1: Status Check Script

```bash
#!/bin/bash
# worktree-status.sh
# Generated by git-worktree-setup skill

echo "Checking worktree status..."

git worktree list --porcelain | while read -r line; do
  if [[ $line == worktree* ]]; then
    path=${line#worktree }
    cd "$path"

    branch=$(git branch --show-current)
    status=$(git status --short | wc -l)

    echo "$branch: $status changes"
  fi
done
```

#### Script 6.2: Sync All Script

```bash
#!/bin/bash
# sync-all-worktrees.sh

for worktree in $(git worktree list | awk '{print $1}'); do
  echo "Syncing $worktree..."
  cd "$worktree"

  git fetch origin
  git merge --ff-only @{u} 2>/dev/null && echo "  ✓ Updated" || echo "  ⚠️ Manual merge needed"
done
```

#### Script 6.3: Cleanup Helper

```bash
#!/bin/bash
# cleanup-merged-worktrees.sh

git worktree list | grep -v "$(git rev-parse --show-toplevel)" | while read -r line; do
  path=$(echo "$line" | awk '{print $1}')
  branch=$(echo "$line" | grep -oP '\[\K[^\]]+')

  if git branch --merged main | grep -q "^[* ]*$branch$"; then
    echo "Removing merged worktree: $branch"
    git worktree remove "$path"
    git branch -d "$branch"
  fi
done
```

---

## Output Formats

### Format 1: Simple List

```
main (current)
feature-a
bugfix-123
```

### Format 2: With Paths

```
main → /Users/connor/myapp (current)
feature-a → /Users/connor/myapp-feature-a
bugfix-123 → /Users/connor/myapp-bugfix-123
```

### Format 3: With Status

```
main [clean] (current)
feature-a [3 changes] [ahead 2]
bugfix-123 [clean] [merged]
```

### Format 4: JSON (for scripts)

```json
{
  "worktrees": [
    {
      "branch": "main",
      "path": "/Users/connor/myapp",
      "current": true,
      "clean": true,
      "ahead": 0,
      "behind": 0,
      "merged": false
    },
    {
      "branch": "feature-a",
      "path": "/Users/connor/myapp-feature-a",
      "current": false,
      "clean": false,
      "changes": 3,
      "ahead": 2,
      "behind": 0,
      "merged": false
    }
  ]
}
```

---

## Information Hierarchy

**Level 1: Quick glance**
- Branch names
- Current indicator
- Basic status (clean/modified)

**Level 2: Detailed status**
- Paths
- Ahead/behind counts
- Last commit info
- Merge status

**Level 3: Deep inspection**
- File-level changes
- Dependency status
- Health checks
- Recommendations

**User chooses depth based on need**

---

## Error Handling

### No Worktrees Found

```
No additional worktrees found.

You only have the main worktree:
  /Users/connor/myapp (main)

To create a worktree:
  "Create a worktree for [branch-name]"
```

### Corrupted Worktree

```
⚠️ Worktree corruption detected: feature-a

Issues:
  - Path doesn't exist: /Users/connor/myapp-feature-a
  - Still in git worktree list

Fix:
  git worktree prune
  git worktree repair
```

### Permissions Issues

```
✗ Cannot access worktree: /path/to/worktree

Error: Permission denied

Solution:
  Check file permissions:
  ls -la /path/to/worktree
```

---

## Success Criteria

- [ ] All worktrees listed successfully
- [ ] Accurate status for each worktree
- [ ] Health checks completed
- [ ] Management options provided
- [ ] User can navigate/act on information

---

## Example: Complete Flow

```
User: Show me my worktrees

Claude:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Git Worktrees (3 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

● main (current)
  /Users/connor/myapp
  ✓ Clean, synced

○ feature-a
  /Users/connor/myapp-feature-a
  ⚠️ 3 changes, 2 commits ahead

○ bugfix-123
  /Users/connor/myapp-bugfix-123
  ✓ Merged to main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
  - Commit changes in feature-a
  - Clean up bugfix-123 (merged)

Would you like more details? (yes/no)
```
