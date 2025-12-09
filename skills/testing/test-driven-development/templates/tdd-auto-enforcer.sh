#!/bin/bash

###############################################################################
# TDD Auto-Enforcer Hook
#
# Claude Code hook that automatically guides LLM to follow TDD workflow
# when implementing features.
#
# Installed by: tdd-automation skill
###############################################################################

# Get user's prompt
USER_PROMPT="$1"

# Keywords that indicate implementation work
IMPLEMENTATION_KEYWORDS="implement|add|create|build|feature|write.*code|develop|make.*function|make.*component"

# Check if prompt is about implementing something
if echo "$USER_PROMPT" | grep -qiE "$IMPLEMENTATION_KEYWORDS"; then

  cat <<'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  TDD ENFORCEMENT ACTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are about to implement code. You MUST follow TDD red-green-refactor:

📋 Required Workflow:

  1. 🔴 RED Phase (First - DO NOT SKIP)
     └─ Write a FAILING test before any implementation
     └─ Run test to verify it fails: npm run test:red <test-file>
     └─ Use TodoWrite to track this phase

  2. 🟢 GREEN Phase (After RED verified)
     └─ Write MINIMAL code to make test pass
     └─ Run test to verify it passes: npm run test:green <test-file>
     └─ Use TodoWrite to track this phase

  3. 🔵 REFACTOR Phase (After GREEN verified)
     └─ Improve code quality while keeping tests green
     └─ Run all tests: npm run test:tdd
     └─ Use TodoWrite to track this phase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ❌ NEVER write implementation code before writing the test
  ❌ NEVER skip RED phase verification (must see test fail)
  ❌ NEVER skip GREEN phase verification (must see test pass)
  ✅ ALWAYS use TodoWrite to track RED-GREEN-REFACTOR phases
  ✅ ALWAYS run tests to verify each phase transition

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 TodoWrite Template (Use This)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create a todo list with these phases before starting:

  [ ] RED: Write failing test for [feature name]
  [ ] Verify test fails with expected error
  [ ] GREEN: Implement minimal code to pass test
  [ ] Verify test passes
  [ ] REFACTOR: Improve code quality
  [ ] Verify all tests still pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Start with RED phase. Create the test file first.

EOF

fi

# Exit successfully (allow prompt to continue)
exit 0
