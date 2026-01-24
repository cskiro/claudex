#!/bin/bash

# Generate Skill from GitHub Issue
# Automates skill creation from pattern detection issues
# Part of Pattern Suggestion Pipeline
#
# Follows Anthropic's official skill structure:
# - SKILL.md (required, 100-200 lines max)
# - reference/ (supporting documentation)
# - scripts/ (if needed)

set -euo pipefail

# Configuration
CLAUDEX_REPO="cskiro/claudex"
CLAUDEX_PATH="${CLAUDEX_PATH:-$HOME/Desktop/Development/claudex}"
LOG_FILE="$HOME/.claude/logs/skill-generation.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log_message() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to extract value from issue body
extract_field() {
    local issue_body="$1"
    local field_name="$2"

    # Match pattern: **Field Name:** `value` or **Field Name:** value
    echo "$issue_body" | grep -o "\*\*${field_name}:\*\* \`[^\`]*\`" | sed "s/\*\*${field_name}:\*\* \`//; s/\`//" || \
    echo "$issue_body" | grep -o "\*\*${field_name}:\*\* [^*]*" | sed "s/\*\*${field_name}:\*\* //" | head -1
}

# Function to extract metrics table value
extract_metric() {
    local issue_body="$1"
    local metric_name="$2"

    echo "$issue_body" | grep "| ${metric_name}" | grep -oE "[0-9]+[×%]" | head -1 | tr -d '×%'
}

# Function to parse issue and extract pattern metadata
parse_issue() {
    local issue_number="$1"

    log_message "PARSE: Fetching issue #${issue_number} from ${CLAUDEX_REPO}"

    # Fetch issue body
    local issue_body=$(gh issue view "$issue_number" --repo "$CLAUDEX_REPO" --json body --jq '.body' 2>&1)

    if [ -z "$issue_body" ]; then
        echo -e "${RED}❌ Error: Could not fetch issue #${issue_number}${NC}" >&2
        return 1
    fi

    # Extract fields
    PATTERN_TEXT=$(extract_field "$issue_body" "Pattern")
    SUGGESTED_NAME=$(extract_field "$issue_body" "Suggested Skill Name")
    DOMAIN=$(extract_field "$issue_body" "Domain")
    USAGE_COUNT=$(extract_metric "$issue_body" "Usage Count")
    SUCCESS_RATE=$(extract_metric "$issue_body" "Success Rate")

    # Validate extracted data
    if [ -z "$SUGGESTED_NAME" ] || [ -z "$PATTERN_TEXT" ]; then
        echo -e "${RED}❌ Error: Failed to parse required fields from issue${NC}" >&2
        log_message "ERROR: Missing required fields (suggested_name or pattern_text)"
        return 1
    fi

    log_message "PARSE: Successfully extracted pattern metadata"
    log_message "  Pattern: ${PATTERN_TEXT}"
    log_message "  Skill Name: ${SUGGESTED_NAME}"
    log_message "  Domain: ${DOMAIN}"

    return 0
}

# Function to check if skill already exists
check_skill_exists() {
    local skill_name="$1"
    local skill_dir="$CLAUDEX_PATH/skills/$skill_name"

    if [ -d "$skill_dir" ]; then
        echo -e "${YELLOW}⚠️  Warning: Skill directory already exists: ${skill_dir}${NC}" >&2
        log_message "WARNING: Skill already exists at ${skill_dir}"
        return 1
    fi

    return 0
}

# Function to generate skill files (Anthropic-compliant structure)
generate_skill_files() {
    local skill_name="$1"
    local pattern_text="$2"
    local usage_count="$3"
    local success_rate="$4"
    local domain="$5"
    local issue_number="$6"
    local skill_dir="$CLAUDEX_PATH/skills/$skill_name"

    log_message "GENERATE: Creating skill directory: ${skill_dir}"
    mkdir -p "$skill_dir"
    mkdir -p "$skill_dir/reference"

    # Generate SKILL.md (Anthropic-compliant, 100-200 lines max)
    cat > "$skill_dir/SKILL.md" <<EOF
---
name: $skill_name
description: >-
  Use PROACTIVELY when ${pattern_text,,}. Automates best practice
  detected from ${usage_count} successful applications with ${success_rate}%
  success rate. Domain: ${domain}. Not for unrelated tasks or manual overrides.
---

# ${skill_name//-/ }

Automates the detected best practice pattern for consistent, reliable execution.

## When to Use This Skill

**Trigger Phrases**:
- "$pattern_text"
- "apply ${skill_name//-/ } pattern"
- "run ${skill_name//-/ } check"

**Use Cases**:
- Automating repetitive validations
- Ensuring best practices are followed
- Reducing manual errors in ${domain,,} workflows

**NOT for**:
- Tasks unrelated to this specific pattern
- When manual control is explicitly needed
- Experimental or one-off operations

## Response Style

- **Proactive**: Check conditions before acting
- **Informative**: Explain what's being validated and why
- **Helpful**: Provide clear next steps on success or failure

## Workflow Overview

### Phase 1: Detection
**Purpose**: Identify when this pattern applies

1. Analyze current context
2. Check if pattern conditions are met
3. Confirm applicability

**Output**: Decision to proceed or skip

→ **Details**: \`reference/detection.md\`

### Phase 2: Execution
**Purpose**: Apply the best practice pattern

1. Execute validation/check
2. Handle success case
3. Handle error case with helpful message

**Output**: Validation result with next steps

→ **Details**: \`reference/execution.md\`

## Important Reminders

- Pattern detected from real-world usage data
- Success rate: ${success_rate}%
- Usage count: ${usage_count}×
- Review and enhance as needed before production use

## Limitations

- Only applies to specific pattern context
- May require manual review for edge cases
- Generated template needs customization

## Reference Materials

| Resource | Purpose |
|----------|---------|
| \`reference/detection.md\` | Pattern detection details |
| \`reference/execution.md\` | Execution workflow |

## Metadata

**Version**: 0.1.0
**Created**: $(date '+%Y-%m-%d')
**Source**: Pattern Suggestion Pipeline (Issue #${issue_number})
**Category**: ${domain}
EOF

    # Generate reference/detection.md
    cat > "$skill_dir/reference/detection.md" <<EOF
# Detection Phase

## Pattern Recognition

This skill activates when the following pattern is detected:

> "$pattern_text"

## Context Analysis

Before applying this pattern, verify:

1. **Environment Check**
   - Relevant files/context are present
   - No conflicting operations in progress

2. **Applicability Confirmation**
   - Pattern matches current situation
   - No explicit override from user

## Decision Criteria

| Condition | Action |
|-----------|--------|
| Pattern matches, no conflicts | Proceed to execution |
| Partial match | Ask for clarification |
| No match | Skip silently |
| User override | Respect user preference |
EOF

    # Generate reference/execution.md
    cat > "$skill_dir/reference/execution.md" <<EOF
# Execution Phase

## Workflow Steps

### Step 1: Prepare
- Gather required context
- Validate preconditions

### Step 2: Execute
- Apply the pattern
- Monitor for issues

### Step 3: Verify
- Confirm successful execution
- Report results to user

## Error Handling

| Error Type | Recovery Action |
|------------|-----------------|
| Precondition failed | Inform user, suggest fixes |
| Execution error | Rollback if possible, report details |
| Partial success | Complete what's possible, document gaps |

## Success Criteria

- Pattern applied without errors
- User informed of results
- Next steps provided if applicable
EOF

    log_message "GENERATE: Skill files created successfully"
    echo -e "${GREEN}✅ Generated skill files:${NC}"
    echo "   - SKILL.md (Anthropic-compliant)"
    echo "   - reference/detection.md"
    echo "   - reference/execution.md"

    return 0
}

# Function to create feature branch and commit
commit_skill() {
    local skill_name="$1"
    local pattern_text="$2"
    local success_rate="$3"
    local usage_count="$4"
    local issue_number="$5"
    local branch_name="feature/pattern-${skill_name}"

    cd "$CLAUDEX_PATH"

    # Ensure we're on main and up to date
    log_message "GIT: Ensuring main branch is up to date"
    git checkout main 2>&1 | tee -a "$LOG_FILE"
    git pull origin main 2>&1 | tee -a "$LOG_FILE"

    # Check if branch already exists
    if git rev-parse --verify "$branch_name" &>/dev/null; then
        echo -e "${YELLOW}⚠️  Warning: Branch ${branch_name} already exists${NC}" >&2
        log_message "WARNING: Branch already exists: ${branch_name}"

        # Delete existing branch
        git branch -D "$branch_name" 2>&1 | tee -a "$LOG_FILE"
        log_message "GIT: Deleted existing branch"
    fi

    # Create new branch
    log_message "GIT: Creating feature branch: ${branch_name}"
    git checkout -b "$branch_name" 2>&1 | tee -a "$LOG_FILE"

    # Stage changes
    git add "skills/$skill_name"

    # Commit with detailed message
    log_message "GIT: Committing skill files"
    git commit -m "$(cat <<EOF
feat($skill_name): Add pattern-detected skill

Pattern: $pattern_text
Success Rate: ${success_rate}%
Usage Count: ${usage_count}×

Generated by Pattern Suggestion Pipeline
Closes #${issue_number}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)" 2>&1 | tee -a "$LOG_FILE"

    echo -e "${GREEN}✅ Changes committed to branch${NC}"
    log_message "GIT: Commit successful"

    return 0
}

# Function to push branch and create PR
create_pull_request() {
    local skill_name="$1"
    local pattern_text="$2"
    local issue_number="$3"
    local branch_name="feature/pattern-${skill_name}"

    cd "$CLAUDEX_PATH"

    # Push branch
    log_message "GIT: Pushing branch to origin"
    git push -u origin "$branch_name" 2>&1 | tee -a "$LOG_FILE"

    # Create PR
    log_message "PR: Creating pull request"

    local pr_url=$(gh pr create \
        --repo "$CLAUDEX_REPO" \
        --base main \
        --head "$branch_name" \
        --title "feat($skill_name): Add pattern-detected skill" \
        --body "$(cat <<EOF
## Summary

Auto-generated skill from pattern detection.

**Pattern**: $pattern_text

## Generated Files

| File | Purpose |
|------|---------|
| \`skills/$skill_name/SKILL.md\` | Agent manifest (Anthropic-compliant) |
| \`skills/$skill_name/reference/detection.md\` | Pattern detection workflow |
| \`skills/$skill_name/reference/execution.md\` | Execution workflow |

## Test Plan

- [ ] Run validation: \`python3 scripts/validate-skills.py skills/$skill_name\`
- [ ] Review SKILL.md structure and content
- [ ] Test skill invocation with trigger phrases
- [ ] Update marketplace.json to include skill

## Next Steps

1. Review generated files for quality
2. Customize templates as needed
3. Add to appropriate plugin in marketplace.json
4. Merge if approved

---

Closes #${issue_number}

Generated by Pattern Suggestion Pipeline
EOF
)" 2>&1)

    if [ -z "$pr_url" ]; then
        echo -e "${RED}❌ Error: Failed to create pull request${NC}" >&2
        log_message "ERROR: PR creation failed"
        return 1
    fi

    log_message "PR: Successfully created: ${pr_url}"
    echo -e "${GREEN}✅ Pull request created:${NC}"
    echo "   $pr_url"

    return 0
}

# Main execution
main() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <issue-number>"
        echo ""
        echo "Example:"
        echo "  $0 13"
        exit 1
    fi

    local issue_number="$1"

    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Auto-Generating Skill from Issue #${issue_number}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    # Validate claudex path
    if [ ! -d "$CLAUDEX_PATH" ]; then
        echo -e "${RED}❌ Error: claudex repository not found at: $CLAUDEX_PATH${NC}"
        echo "   Set CLAUDEX_PATH environment variable to correct location"
        exit 1
    fi

    # Parse issue
    if ! parse_issue "$issue_number"; then
        exit 1
    fi

    echo ""
    echo -e "${GREEN}📋 Pattern Details:${NC}"
    echo "   Pattern: $PATTERN_TEXT"
    echo "   Skill Name: $SUGGESTED_NAME"
    echo "   Domain: $DOMAIN"
    echo "   Success Rate: ${SUCCESS_RATE}%"
    echo "   Usage Count: ${USAGE_COUNT}×"
    echo ""

    # Check if skill already exists
    if ! check_skill_exists "$SUGGESTED_NAME"; then
        echo -e "${YELLOW}   Overwriting existing skill...${NC}"
        rm -rf "$CLAUDEX_PATH/skills/$SUGGESTED_NAME"
    fi

    # Generate skill files
    if ! generate_skill_files "$SUGGESTED_NAME" "$PATTERN_TEXT" "$USAGE_COUNT" "$SUCCESS_RATE" "$DOMAIN" "$issue_number"; then
        exit 1
    fi

    echo ""

    # Commit changes
    if ! commit_skill "$SUGGESTED_NAME" "$PATTERN_TEXT" "$SUCCESS_RATE" "$USAGE_COUNT" "$issue_number"; then
        exit 1
    fi

    echo ""

    # Create PR
    if ! create_pull_request "$SUGGESTED_NAME" "$PATTERN_TEXT" "$issue_number"; then
        exit 1
    fi

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Skill Generation Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"

    log_message "SUCCESS: Skill generation completed for issue #${issue_number}"
}

# Run main
main "$@"
