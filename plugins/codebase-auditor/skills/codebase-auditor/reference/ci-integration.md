# CI/CD Integration Reference

GitHub Actions workflows for automated codebase auditing.

## Workflow Templates

### 1. PR Audit (Incremental)

Audit only changed files on pull requests.

```yaml
# .github/workflows/pr-audit.yml
name: PR Code Audit

on:
  pull_request:
    branches: [main, develop]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for diff

      - name: Get changed files
        id: changed
        run: |
          echo "files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -E '\.(js|ts|jsx|tsx|py)$' | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run incremental audit
        if: steps.changed.outputs.files != ''
        run: |
          python3 scripts/audit_engine.py \
            --files ${{ steps.changed.outputs.files }} \
            --output audit-report.json \
            --format json

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('audit-report.json'));

            let comment = '## Code Audit Results\n\n';
            comment += `| Severity | Count |\n|----------|-------|\n`;
            comment += `| Critical | ${report.critical || 0} |\n`;
            comment += `| High | ${report.high || 0} |\n`;
            comment += `| Medium | ${report.medium || 0} |\n`;
            comment += `| Low | ${report.low || 0} |\n`;

            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: comment
            });
```

### 2. Weekly Full Audit (Scheduled)

Complete codebase audit on schedule.

```yaml
# .github/workflows/weekly-audit.yml
name: Weekly Full Audit

on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 6 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  full-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run full audit
        run: |
          python3 scripts/audit_engine.py \
            --scope src/ \
            --output audit-report.json \
            --format json

      - name: Generate HTML report
        run: |
          python3 scripts/report_generator.py \
            --input audit-report.json \
            --output audit-report.html \
            --format html

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: audit-reports
          path: |
            audit-report.json
            audit-report.html

      - name: Update audit history
        run: |
          python3 scripts/update_history.py \
            --report audit-report.json \
            --database audit-history.db
```

### 3. Security Gate (Blocking)

Block merges with critical security issues.

```yaml
# .github/workflows/security-gate.yml
name: Security Gate

on:
  pull_request:
    branches: [main]

jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run security audit
        id: audit
        run: |
          python3 scripts/audit_engine.py \
            --scope src/ \
            --analyzers security \
            --output security-report.json

          CRITICAL=$(jq '.findings | map(select(.severity == "critical")) | length' security-report.json)
          echo "critical_count=$CRITICAL" >> $GITHUB_OUTPUT

      - name: Check security gate
        if: steps.audit.outputs.critical_count > 0
        run: |
          echo "::error::Security gate failed: ${{ steps.audit.outputs.critical_count }} critical vulnerabilities found"
          exit 1
```

## Quality Gates

### Configurable Thresholds

```yaml
# .audit-config.yml
quality_gates:
  # Fail if any of these thresholds exceeded
  critical_findings: 0
  high_findings: 5

  # Minimum scores (0-100)
  min_quality_score: 70
  min_security_score: 80
  min_test_coverage: 75

  # Maximum technical debt
  max_debt_ratio: 10  # % of dev time

  # SQALE rating (A-E)
  min_sqale_rating: B
```

### Gate Check Script

```python
#!/usr/bin/env python3
# scripts/check_gates.py

import json
import sys
import yaml

def check_gates(report_path, config_path):
    with open(report_path) as f:
        report = json.load(f)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    gates = config.get('quality_gates', {})
    failures = []

    # Check finding counts
    if report.get('critical', 0) > gates.get('critical_findings', 0):
        failures.append(f"Critical findings: {report['critical']} > {gates['critical_findings']}")

    if report.get('high', 0) > gates.get('high_findings', 999):
        failures.append(f"High findings: {report['high']} > {gates['high_findings']}")

    # Check scores
    if report.get('quality_score', 100) < gates.get('min_quality_score', 0):
        failures.append(f"Quality score: {report['quality_score']} < {gates['min_quality_score']}")

    if failures:
        print("Quality gate FAILED:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print("Quality gate PASSED")
    sys.exit(0)

if __name__ == '__main__':
    check_gates(sys.argv[1], sys.argv[2])
```

## PR Commenting

### Detailed Finding Comment

```javascript
// scripts/pr-comment.js
const formatFindings = (findings) => {
  let md = '## Audit Findings\n\n';

  const bySeverity = {
    critical: findings.filter(f => f.severity === 'critical'),
    high: findings.filter(f => f.severity === 'high'),
    medium: findings.filter(f => f.severity === 'medium'),
  };

  for (const [severity, items] of Object.entries(bySeverity)) {
    if (items.length === 0) continue;

    md += `### ${severity.toUpperCase()} (${items.length})\n\n`;

    for (const finding of items.slice(0, 10)) {  // Limit to 10 per severity
      md += `- **${finding.rule}** in \`${finding.file}:${finding.line}\`\n`;
      md += `  ${finding.message}\n`;
    }

    if (items.length > 10) {
      md += `\n_...and ${items.length - 10} more_\n`;
    }
    md += '\n';
  }

  return md;
};
```

## DORA Metrics Integration

Track deployment metrics alongside code quality:

```yaml
# Extend weekly audit to capture DORA metrics
- name: Calculate DORA metrics
  run: |
    # Deployment frequency
    DEPLOYS=$(gh release list --limit 30 | wc -l)

    # Lead time (avg days from commit to deploy)
    LEAD_TIME=$(git log --format='%H %ai' -30 | ... )

    # Change failure rate
    FAILURES=$(gh issue list --label "production-incident" --state closed | wc -l)

    echo "{\"deploys\": $DEPLOYS, \"lead_time\": $LEAD_TIME, \"failures\": $FAILURES}" > dora-metrics.json
```
