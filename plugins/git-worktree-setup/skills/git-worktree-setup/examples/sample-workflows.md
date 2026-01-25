# Git Worktree Sample Workflows

Real-world examples of using git worktrees with Claude Code for parallel development.

## Table of Contents

1. [Daily Development Workflows](#daily-development-workflows)
2. [Code Review Workflows](#code-review-workflows)
3. [Emergency Hotfix Workflows](#emergency-hotfix-workflows)
4. [Experimentation Workflows](#experimentation-workflows)
5. [Team Collaboration Workflows](#team-collaboration-workflows)
6. [Testing and QA Workflows](#testing-and-qa-workflows)
7. [Advanced Workflows](#advanced-workflows)

---

## Daily Development Workflows

### Workflow 1: Parallel Feature Development

**Scenario:** You're working on feature A when a new urgent feature B request comes in.

**Steps:**

```bash
# Currently working on feature-authentication
cd ~/projects/myapp
git branch  # Shows: * feature-authentication

# New request: add dashboard feature
# Create worktree instead of switching branches

User: "Create a worktree for feature-dashboard"

Claude:
✓ Creating worktree...
  Location: ~/projects/myapp-feature-dashboard
  Branch: feature-dashboard (new)
  Dependencies: Installing...
  ✓ Ready!

# Open new Claude Code session
cd ~/projects/myapp-feature-dashboard
claude

# Now have two parallel sessions:
# Terminal 1: Working on authentication
# Terminal 2: Working on dashboard
```

**Benefits:**
- No context switching
- No stashing required
- Independent testing
- Parallel Claude Code sessions

---

### Workflow 2: Bug Investigation During Feature Work

**Scenario:** Mid-feature development, you need to investigate a production bug.

**Steps:**

```bash
# Current state: Working on feature-redesign with uncommitted changes

User: "Create a worktree from main for bugfix-login-error"

Claude:
Checking prerequisites...
⚠️  You have uncommitted changes in current worktree
Continue? (Current work won't be affected)

User: "yes"

Claude:
✓ Creating worktree from main...
  Location: ~/projects/myapp-bugfix-login-error
  Branch: bugfix-login-error (from main)
  ✓ Clean state (no redesign changes)
  ✓ Ready!

# Investigate bug in clean environment
cd ~/projects/myapp-bugfix-login-error
claude

# After fix:
git add .
git commit -m "fix: resolve login redirect issue"
git push

# Create PR for bugfix
gh pr create --title "Fix: Login redirect error"

# Return to feature work
cd ~/projects/myapp-feature-redesign

# Feature work still intact with all uncommitted changes
```

**Key Points:**
- Bug investigated in clean environment
- Feature work undisturbed
- Easy context switching
- Independent commits and PRs

---

## Code Review Workflows

### Workflow 3: PR Review Without Interruption

**Scenario:** Teammate requests review while you're coding.

**Steps:**

```bash
# Current: Working on feature-payments

# Teammate: "Can you review PR #456?"

User: "Create a worktree for PR 456 review"

Claude:
Fetching PR #456...
PR Branch: feature-user-settings
Author: @teammate

Creating review worktree...
✓ Location: ~/projects/myapp-review-456
✓ Checked out: feature-user-settings
✓ Installing dependencies...
✓ Ready for review!

# Review in fresh environment
cd ~/projects/myapp-review-456
claude

# In Claude Code, review changes:
# - Read code
# - Run tests: npm test
# - Check build: npm run build
# - Test locally: npm run dev

# Leave feedback on GitHub
gh pr review 456 --comment --body "LGTM! Tests pass, code looks good."

# Clean up review worktree
cd ~/projects/myapp
User: "Remove the review-456 worktree"

Claude:
✓ No uncommitted changes
✓ Removed worktree
✓ Disk space freed: ~850MB

# Back to feature work
cd ~/projects/myapp-feature-payments
# Continue where you left off
```

**Benefits:**
- Review in pristine environment
- Your work stays untouched
- Run tests without affecting your code
- Quick cleanup after review

---

### Workflow 4: Compare Multiple PR Approaches

**Scenario:** Two PRs propose different solutions to the same problem.

**Steps:**

```bash
User: "Create worktrees for PR 123 and PR 124 to compare"

Claude:
Creating comparison worktrees...

✓ PR #123 (approach-a): ~/projects/myapp-pr-123
✓ PR #124 (approach-b): ~/projects/myapp-pr-124

Installing dependencies in parallel...
✓ Both environments ready!

# Test approach A
cd ~/projects/myapp-pr-123
npm test
npm run benchmark

# Test approach B
cd ~/projects/myapp-pr-124
npm test
npm run benchmark

# Compare results:
# Approach A: 250ms, cleaner code
# Approach B: 180ms, more complex

# Decision: Approve approach B, suggest code cleanup

# Clean up both
User: "Clean up PR worktrees"

Claude:
✓ Removed: myapp-pr-123
✓ Removed: myapp-pr-124
```

**Use Case:**
- A/B testing different implementations
- Performance comparison
- Side-by-side code review
- Data-driven decisions

---

## Emergency Hotfix Workflows

### Workflow 5: Production Hotfix During Feature Development

**Scenario:** Critical production bug needs immediate fix.

**Steps:**

```bash
# Current: Deep in feature development with many uncommitted changes

# Alert: Production is down!

User: "Create emergency hotfix worktree from production branch"

Claude:
🚨 Creating emergency hotfix...

✓ Source: production branch
✓ Location: ~/projects/myapp-hotfix-critical
✓ Branch: hotfix-api-timeout (from production)
✓ Clean slate (production code)
✓ Dependencies: Installing...
✓ Ready in 15 seconds!

Next: cd ~/projects/myapp-hotfix-critical && claude

# Fix in isolated environment
cd ~/projects/myapp-hotfix-critical
claude

# In Claude Code:
# 1. Identify issue
# 2. Write fix
# 3. Test thoroughly
# 4. Deploy

git add .
git commit -m "hotfix: increase API timeout to 30s"
git push origin hotfix-api-timeout

# Deploy to production
./deploy-hotfix.sh

# Merge to main
git checkout main
git merge hotfix-api-timeout
git push

# Merge to feature branch too (avoid conflicts later)
cd ~/projects/myapp-feature-redesign
git merge main

# Clean up hotfix worktree
User: "Remove hotfix worktree"

Claude:
✓ Hotfix merged to main and feature branch
✓ Production fixed
✓ Removed worktree
✓ Back to feature development
```

**Critical Benefits:**
- Instant context switch
- Production code isolated
- No stashing complex changes
- Merge back to all branches easily

---

### Workflow 6: Multiple Simultaneous Hotfixes

**Scenario:** Multiple production issues at once.

**Steps:**

```bash
User: "Create hotfix worktrees for login-bug, payment-error, and api-timeout"

Claude:
Creating 3 hotfix worktrees from production...

✓ hotfix-login-bug → ~/projects/myapp-hotfix-login
✓ hotfix-payment-error → ~/projects/myapp-hotfix-payment
✓ hotfix-api-timeout → ~/projects/myapp-hotfix-api

Installing dependencies in parallel...
All ready!

Assign to team:
  Developer 1: cd ~/projects/myapp-hotfix-login
  Developer 2: cd ~/projects/myapp-hotfix-payment
  Developer 3: cd ~/projects/myapp-hotfix-api

# Each developer works in isolation
# Fixes don't conflict
# Deploy independently
# Merge back when done
```

**Team Benefits:**
- Parallel hotfix development
- No branch conflicts
- Independent testing
- Fast resolution

---

## Experimentation Workflows

### Workflow 7: Test Radical Architecture Change

**Scenario:** Want to try a major refactor without risking main work.

**Steps:**

```bash
User: "Create an experiment worktree for testing GraphQL migration"

Claude:
Creating experiment worktree...
✓ Location: ~/projects/myapp-experiment-graphql
✓ Branch: experiment-graphql-migration
✓ Based on: main
✓ Ready for experimentation!

cd ~/projects/myapp-experiment-graphql
claude

# Implement radical changes:
# - Replace REST with GraphQL
# - New schema design
# - Different data layer

# Test the experiment
npm test
npm run benchmark

# Results look promising!
# Migrate learnings to feature branch

# Or if experiment fails:
User: "Remove experiment worktree"

Claude:
✓ No harm done to main codebase
✓ Learnings documented
✓ Removed worktree
```

**Experimentation Benefits:**
- Safe to fail
- No polluting main branch
- Easy to abandon
- Document learnings

---

### Workflow 8: Performance Comparison

**Scenario:** Test if optimization actually improves performance.

**Steps:**

```bash
User: "Create worktrees for baseline and optimization comparison"

Claude:
Creating comparison environment...

✓ Baseline: ~/projects/myapp-baseline (current main)
✓ Optimization: ~/projects/myapp-optimized (new branch)

# Test baseline
cd ~/projects/myapp-baseline
npm run benchmark > baseline-results.txt

# Implement optimization
cd ~/projects/myapp-optimized
claude
# (Make optimization changes)

npm run benchmark > optimized-results.txt

# Compare results
diff baseline-results.txt optimized-results.txt

# Baseline: 450ms avg
# Optimized: 220ms avg
# Improvement: 51% faster ✓

# Optimization validated - merge it!
git checkout main
git merge experiment-optimized

# Clean up
User: "Remove comparison worktrees"
```

---

## Team Collaboration Workflows

### Workflow 9: Pair Programming Setup

**Scenario:** Pair programming with screen sharing.

**Steps:**

```bash
# Developer 1 (driver)
User: "Create pairing worktree for feature-checkout"

Claude:
✓ Created: ~/projects/myapp-pairing-checkout
✓ Fresh environment
✓ Ready for pairing session

cd ~/projects/myapp-pairing-checkout
claude

# Share screen, develop together
# Commit frequently

git add .
git commit -m "WIP: checkout flow"
git push

# Developer 2 (navigator) checks out same worktree later
git worktree add ~/projects/myapp-pairing-checkout pairing-checkout
cd ~/projects/myapp-pairing-checkout
# Continue from where Dev 1 left off

# After pairing session
User: "Merge pairing work to main feature branch"

Claude:
✓ Merged pairing-checkout → feature-checkout
✓ Removed pairing worktree
✓ Clean state
```

---

### Workflow 10: Integration Testing Multiple Features

**Scenario:** Test how three features work together before merging.

**Steps:**

```bash
# Current state:
# - feature-auth (ready)
# - feature-dashboard (ready)
# - feature-reports (ready)

User: "Create integration worktree combining auth, dashboard, and reports"

Claude:
Creating integration environment...

✓ Base: main branch
✓ Location: ~/projects/myapp-integration-test
✓ Branch: integration-test

Merging features...
✓ Merged: feature-auth
✓ Merged: feature-dashboard
✓ Merged: feature-reports

Running tests...
⚠️  2 integration test failures detected

# Fix integration issues in integration worktree
cd ~/projects/myapp-integration-test
claude

# Fix conflicts and integration issues
git add .
git commit -m "fix: resolve feature integration conflicts"

# All tests pass!
npm test
# ✓ All 156 tests passing

# Now safe to merge features to main
git checkout main
git merge feature-auth
git merge feature-dashboard
git merge feature-reports

# Clean up
User: "Remove integration test worktree"
```

---

## Testing and QA Workflows

### Workflow 11: Test Across Multiple Node Versions

**Scenario:** Ensure compatibility with Node 16, 18, and 20.

**Steps:**

```bash
User: "Create worktrees for testing Node 16, 18, and 20"

Claude:
Creating test environments...

✓ node16: ~/projects/myapp-test-node16
✓ node18: ~/projects/myapp-test-node18
✓ node20: ~/projects/myapp-test-node20

# Terminal 1: Node 16
cd ~/projects/myapp-test-node16
nvm use 16
npm install
npm test
# Result: 3 failures (deprecated API)

# Terminal 2: Node 18
cd ~/projects/myapp-test-node18
nvm use 18
npm install
npm test
# Result: All pass ✓

# Terminal 3: Node 20
cd ~/projects/myapp-test-node20
nvm use 20
npm install
npm test
# Result: All pass ✓

# Fix Node 16 compatibility in separate worktree
cd ~/projects/myapp-test-node16
claude
# Fix deprecated API usage

# All versions pass!
```

---

### Workflow 12: Regression Testing

**Scenario:** Test new feature doesn't break existing functionality.

**Steps:**

```bash
# Have feature branch with changes

User: "Create worktrees for regression testing: baseline and feature"

Claude:
Setting up regression test...

✓ Baseline: ~/projects/myapp-baseline (main branch)
✓ Feature: ~/projects/myapp-feature-new-ui

# Run tests in baseline
cd ~/projects/myapp-baseline
npm test -- --coverage > baseline-coverage.txt

# Run tests in feature
cd ~/projects/myapp-feature-new-ui
npm test -- --coverage > feature-coverage.txt

# Compare
diff baseline-coverage.txt feature-coverage.txt

# Baseline: 142/142 tests pass, 87% coverage
# Feature: 156/156 tests pass, 89% coverage
# Added: 14 new tests ✓
# Coverage improved ✓
# No regressions ✓

# Safe to merge!
```

---

## Advanced Workflows

### Workflow 13: Dependency Update Testing

**Scenario:** Test major dependency update before applying to all branches.

**Steps:**

```bash
User: "Create worktree to test React 19 upgrade"

Claude:
✓ Created: ~/projects/myapp-react19-test
✓ Branch: test-react19-upgrade

cd ~/projects/myapp-react19-test
claude

# Upgrade React
npm install react@19 react-dom@19

# Update code for breaking changes
# Run tests
npm test

# Some failures - fix them
# Document migration steps

# Once stable, apply to feature branches
cd ~/projects/myapp-feature-auth
npm install react@19 react-dom@19
# Apply same fixes

# Repeat for other worktrees
```

---

### Workflow 14: Database Migration Testing

**Scenario:** Test database schema changes safely.

**Steps:**

```bash
User: "Create worktree for testing database migration"

Claude:
✓ Created: ~/projects/myapp-db-migration-test
✓ Using test database

cd ~/projects/myapp-db-migration-test

# Point to test database
echo "DATABASE_URL=postgresql://localhost/myapp_test" > .env

# Run migration
npm run migrate:up

# Test application with new schema
npm test
npm run dev

# Migration successful!

# Apply to staging/production
# Clean up test worktree
```

---

## Complete Real-World Example

### Full Development Day with Worktrees

```bash
# 9:00 AM - Start day, check tasks
git worktree list
# Just main worktree

# 9:15 AM - Start planned feature
User: "Create worktree for feature-notifications"
# Work on notifications...

# 11:30 AM - Urgent: Review teammate's PR
User: "Create worktree for reviewing PR 234"
# Review, approve, remove worktree

# 1:00 PM - Production bug reported
User: "Create hotfix worktree from production"
# Fix bug, deploy, merge back

# 2:30 PM - Back to notifications feature
cd ~/projects/myapp-feature-notifications
# Continue where I left off

# 3:00 PM - PM requests quick prototype
User: "Create experiment worktree for dashboard prototype"
# Build prototype, demo to PM
# Not approved - remove worktree

# 4:00 PM - Finish notifications feature
git add .
git commit -m "feat: add push notifications"
git push

# Create PR
gh pr create --title "Feature: Push Notifications"

# 4:30 PM - Clean up
User: "Show my worktrees"

Claude:
Current worktrees:
  main (clean)
  feature-notifications (PR created)
  hotfix-production (merged and deployed)

User: "Clean up merged worktrees"

Claude:
✓ Removed: hotfix-production
✓ Kept: feature-notifications (PR pending)

# End of day - organized workspace
```

---

## Summary

Git worktrees enable:
- **Parallel development** without context switching
- **Safe experimentation** without risk
- **Fast emergency responses** without disruption
- **Efficient code reviews** in isolation
- **Comprehensive testing** across environments
- **Team collaboration** with shared workflows

**Key Principles:**
1. Create worktrees liberally - they're cheap
2. Clean up regularly - avoid clutter
3. Use descriptive names - future you will thank you
4. Document team conventions - consistency matters
5. Automate common patterns - save time

**Remember:** Worktrees are a tool. Use them when they add value. Don't overcomplicate simple tasks.
