#!/bin/bash
# JSON Reporter for Skill Isolation Tester
# Generates structured JSON output for CI/CD integration

# ============================================================================
# JSON Output Generator
# ============================================================================

# Initialize JSON report structure
# Usage: json_init "test-name" "skill-name"
json_init() {
    local test_name="$1"
    local skill_name="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat > "$JSON_REPORT_FILE" <<EOF
{
  "test_name": "$test_name",
  "skill_name": "$skill_name",
  "timestamp": "$timestamp",
  "test_id": "$TEST_ID",
  "status": "running",
  "duration_seconds": 0,
  "exit_code": null,
  "environment": {
    "os": "$(uname -s)",
    "os_version": "$(uname -r)",
    "architecture": "$(uname -m)",
    "docker_version": "$(docker --version 2>/dev/null || echo 'not installed')"
  },
  "metrics": {},
  "changes": {},
  "issues": [],
  "recommendations": []
}
EOF
}

# Update JSON field
# Usage: json_set_field "path.to.field" "value"
json_set_field() {
    local field_path="$1"
    local value="$2"

    if [[ ! -f "$JSON_REPORT_FILE" ]]; then
        echo "ERROR: JSON report file not initialized" >&2
        return 1
    fi

    # Use jq to update field (requires jq to be installed)
    if command -v jq &> /dev/null; then
        local temp_file="${JSON_REPORT_FILE}.tmp"
        jq "$field_path = $value" "$JSON_REPORT_FILE" > "$temp_file"
        mv "$temp_file" "$JSON_REPORT_FILE"
    else
        echo "WARNING: jq not installed, skipping JSON update" >&2
    fi
}

# Add metric to report
# Usage: json_add_metric "metric_name" "value" "unit"
json_add_metric() {
    local metric_name="$1"
    local value="$2"
    local unit="${3:-}"

    if command -v jq &> /dev/null; then
        local temp_file="${JSON_REPORT_FILE}.tmp"

        if [[ -n "$unit" ]]; then
            jq ".metrics[\"$metric_name\"] = {\"value\": $value, \"unit\": \"$unit\"}" \
                "$JSON_REPORT_FILE" > "$temp_file"
        else
            jq ".metrics[\"$metric_name\"] = $value" \
                "$JSON_REPORT_FILE" > "$temp_file"
        fi

        mv "$temp_file" "$JSON_REPORT_FILE"
    fi
}

# Add issue to report
# Usage: json_add_issue "severity" "category" "description"
json_add_issue() {
    local severity="$1"  # error, warning, info
    local category="$2"
    local description="$3"

    if command -v jq &> /dev/null; then
        local temp_file="${JSON_REPORT_FILE}.tmp"
        local issue_json=$(cat <<EOF
{
  "severity": "$severity",
  "category": "$category",
  "description": "$description"
}
EOF
)

        jq ".issues += [$issue_json]" "$JSON_REPORT_FILE" > "$temp_file"
        mv "$temp_file" "$JSON_REPORT_FILE"
    fi
}

# Add recommendation to report
# Usage: json_add_recommendation "title" "description"
json_add_recommendation() {
    local title="$1"
    local description="$2"

    if command -v jq &> /dev/null; then
        local temp_file="${JSON_REPORT_FILE}.tmp"
        local rec_json=$(cat <<EOF
{
  "title": "$title",
  "description": "$description"
}
EOF
)

        jq ".recommendations += [$rec_json]" "$JSON_REPORT_FILE" > "$temp_file"
        mv "$temp_file" "$JSON_REPORT_FILE"
    fi
}

# Finalize JSON report with test results
# Usage: json_finalize exit_code duration_seconds
json_finalize() {
    local exit_code="$1"
    local duration_seconds="$2"
    local status="passed"

    if [[ $exit_code -ne 0 ]]; then
        status="failed"
    fi

    if command -v jq &> /dev/null; then
        local temp_file="${JSON_REPORT_FILE}.tmp"
        jq ".status = \"$status\" | .exit_code = $exit_code | .duration_seconds = $duration_seconds" \
            "$JSON_REPORT_FILE" > "$temp_file"
        mv "$temp_file" "$JSON_REPORT_FILE"
    fi
}

# Generate JUnit XML format (common in CI/CD systems)
# Usage: json_to_junit input.json output.xml
json_to_junit() {
    local json_file="$1"
    local xml_file="$2"

    if [[ ! -f "$json_file" ]]; then
        echo "ERROR: JSON file not found: $json_file" >&2
        return 1
    fi

    if ! command -v jq &> /dev/null; then
        echo "ERROR: jq not installed" >&2
        return 1
    fi

    local test_name=$(jq -r '.test_name' "$json_file")
    local skill_name=$(jq -r '.skill_name' "$json_file")
    local duration=$(jq -r '.duration_seconds' "$json_file")
    local status=$(jq -r '.status' "$json_file")
    local exit_code=$(jq -r '.exit_code' "$json_file")
    local issues=$(jq -r '.issues | length' "$json_file")

    cat > "$xml_file" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="skill-isolation-tests" tests="1" failures="$([[ $status == "failed" ]] && echo "1" || echo "0")" errors="0" time="$duration">
    <testcase name="$skill_name" classname="$test_name" time="$duration">
EOF

    if [[ $status == "failed" ]]; then
        local failure_msg=$(jq -r '.issues[] | select(.severity == "error") | .description' "$json_file" | head -1)
        cat >> "$xml_file" <<EOF
      <failure message="Test failed with exit code $exit_code">$failure_msg</failure>
EOF
    fi

    # Add warnings as system-out
    if [[ $issues -gt 0 ]]; then
        cat >> "$xml_file" <<EOF
      <system-out>
EOF
        jq -r '.issues[] | "[\(.severity | ascii_upcase)] \(.category): \(.description)"' "$json_file" >> "$xml_file"
        cat >> "$xml_file" <<EOF
      </system-out>
EOF
    fi

    cat >> "$xml_file" <<EOF
    </testcase>
  </testsuite>
</testsuites>
EOF

    echo "JUnit XML report generated: $xml_file"
}

# Generate GitHub Actions summary format
# Usage: json_to_github_summary input.json
json_to_github_summary() {
    local json_file="$1"

    if [[ ! -f "$json_file" ]]; then
        echo "ERROR: JSON file not found: $json_file" >&2
        return 1
    fi

    if ! command -v jq &> /dev/null; then
        echo "ERROR: jq not installed" >&2
        return 1
    fi

    local status=$(jq -r '.status' "$json_file")
    local skill_name=$(jq -r '.skill_name' "$json_file")
    local duration=$(jq -r '.duration_seconds' "$json_file")

    cat <<EOF
## 🧪 Skill Isolation Test: $skill_name

**Status:** $([[ $status == "passed" ]] && echo "✅ PASSED" || echo "❌ FAILED")
**Duration:** ${duration}s

### Metrics
EOF

    jq -r '.metrics | to_entries[] | "- **\(.key)**: \(.value.value // .value)\(.value.unit // "")"' "$json_file"

    local issue_count=$(jq -r '.issues | length' "$json_file")
    if [[ $issue_count -gt 0 ]]; then
        cat <<EOF

### Issues Found ($issue_count)
EOF
        jq -r '.issues[] | "- \(if .severity == "error" then "❌" elif .severity == "warning" then "⚠️" else "ℹ️" end) **\(.category)**: \(.description)"' "$json_file"
    fi

    local rec_count=$(jq -r '.recommendations | length' "$json_file")
    if [[ $rec_count -gt 0 ]]; then
        cat <<EOF

### Recommendations
EOF
        jq -r '.recommendations[] | "- **\(.title)**: \(.description)"' "$json_file"
    fi
}

# Export all reports in multiple formats
# Usage: export_all_formats base_name
export_all_formats() {
    local base_name="$1"
    local json_file="${base_name}.json"
    local junit_file="${base_name}.junit.xml"
    local summary_file="${base_name}.md"

    if [[ ! -f "$json_file" ]]; then
        echo "ERROR: JSON report not found: $json_file" >&2
        return 1
    fi

    echo "Exporting test results in multiple formats..."

    # JUnit XML
    json_to_junit "$json_file" "$junit_file"

    # GitHub Summary
    json_to_github_summary "$json_file" > "$summary_file"

    echo "Reports generated:"
    echo "  - JSON: $json_file"
    echo "  - JUnit XML: $junit_file"
    echo "  - Markdown: $summary_file"

    # If running in GitHub Actions, add to job summary
    if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
        json_to_github_summary "$json_file" >> "$GITHUB_STEP_SUMMARY"
        echo "GitHub Actions summary updated"
    fi
}

# ============================================================================
# Usage Example
# ============================================================================

# Example usage in a test script:
#
# #!/bin/bash
# source "$(dirname "$0")/lib/json-reporter.sh"
#
# # Initialize
# export JSON_REPORT_FILE="/tmp/test-report.json"
# export TEST_ID="$(date +%s)"
# json_init "docker-skill-test" "my-skill"
#
# # Record metrics during test
# START_TIME=$(date +%s)
#
# json_add_metric "containers_created" 3
# json_add_metric "images_built" 1
# json_add_metric "disk_usage_mb" 1500 "MB"
#
# # Add issues found
# json_add_issue "warning" "cleanup" "Found 2 orphaned containers"
# json_add_issue "error" "security" "API key found in logs"
#
# # Add recommendations
# json_add_recommendation "Cleanup" "Implement automatic container cleanup"
#
# # Finalize
# END_TIME=$(date +%s)
# DURATION=$((END_TIME - START_TIME))
# json_finalize 0 "$DURATION"
#
# # Export all formats
# export_all_formats "/tmp/test-report"
