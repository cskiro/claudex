#!/bin/bash

###############################################################################
# TDD_AUTOMATION: Git Pre-Commit Hook
#
# Validates that tests exist for implementation files before allowing commit.
# Ensures TDD workflow (test-first) is followed.
#
# Installed by: tdd-automation skill
###############################################################################

echo "🔍 TDD Validation: Checking test-first compliance..."

# Get list of new implementation files being committed
IMPL_FILES=$(git diff --cached --name-only --diff-filter=A | grep -E "^src/.*\.(ts|js|tsx|jsx)$" | grep -v ".test." | grep -v ".spec.")

if [ -z "$IMPL_FILES" ]; then
  echo "✅ No new implementation files detected"
  exit 0
fi

VIOLATIONS=0

# Check each implementation file
while IFS= read -r impl_file; do
  if [ -z "$impl_file" ]; then
    continue
  fi

  # Determine expected test file name
  dir=$(dirname "$impl_file")
  filename=$(basename "$impl_file")
  base="${filename%.*}"
  ext="${filename##*.}"

  # Try multiple test file patterns
  test_patterns=(
    "$dir/$base.test.$ext"
    "$dir/$base.spec.$ext"
    "${impl_file%.*}.test.$ext"
    "${impl_file%.*}.spec.$ext"
  )

  test_exists=false
  for test_file in "${test_patterns[@]}"; do
    if [ -f "$test_file" ]; then
      test_exists=true

      # Check if test file was committed first (git log timestamps)
      test_commit_time=$(git log --diff-filter=A --format="%at" --follow -- "$test_file" 2>/dev/null | head -1)
      impl_commit_time=$(date +%s)  # Current time for uncommitted file

      # If test file exists in git history, it was committed first - good!
      if [ -n "$test_commit_time" ]; then
        echo "✅ $impl_file -> Test exists: $test_file"
        break
      else
        # Test file exists but not committed yet
        if git diff --cached --name-only | grep -q "$test_file"; then
          echo "✅ $impl_file -> Test being committed: $test_file"
          break
        fi
      fi
    fi
  done

  if [ "$test_exists" = false ]; then
    echo "❌ TDD VIOLATION: No test file found for $impl_file"
    echo "   Expected one of:"
    for pattern in "${test_patterns[@]}"; do
      echo "     - $pattern"
    done
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
done <<< "$IMPL_FILES"

# Check for test files in commit
TEST_FILES=$(git diff --cached --name-only | grep -E "\.(test|spec)\.(ts|js|tsx|jsx)$")

if [ -n "$TEST_FILES" ]; then
  echo ""
  echo "📝 Test files in this commit:"
  echo "$TEST_FILES" | while IFS= read -r test_file; do
    echo "   ✓ $test_file"
  done
fi

echo ""

if [ $VIOLATIONS -gt 0 ]; then
  echo "❌ TDD Validation Failed: $VIOLATIONS violation(s) found"
  echo ""
  echo "TDD requires writing tests BEFORE implementation."
  echo ""
  echo "To fix:"
  echo "  1. Create test file(s) for the implementation"
  echo "  2. Commit tests first: git add <test-files> && git commit -m 'Add tests for [feature]'"
  echo "  3. Then commit implementation: git add <impl-files> && git commit -m 'Implement [feature]'"
  echo ""
  echo "Or use: npm run generate:test <impl-file> to create a test template"
  echo ""
  echo "To bypass this check (not recommended):"
  echo "  git commit --no-verify"
  echo ""
  exit 1
fi

echo "✅ TDD Validation Passed: All implementation files have tests"
echo ""
exit 0
