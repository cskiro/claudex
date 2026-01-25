# Validation/Audit Skill Pattern

Use this pattern when your skill **validates, audits, or checks** artifacts against standards.

## When to Use

- Skill checks compliance against defined standards
- Detects issues and provides remediation guidance
- Generates reports with severity levels
- Examples: claude-md-auditor, codebase-auditor

## Structure

### Validation Sources

Clearly define what you're validating against:

```markdown
## Validation Sources

### 1. ✅ Official Standards
- **Source**: [Authority/documentation]
- **Authority**: Highest (requirements)
- **Examples**: [List key standards]

### 2. 💡 Best Practices
- **Source**: Community/field experience
- **Authority**: Medium (recommendations)
- **Examples**: [List practices]

### 3. 🔬 Research/Optimization
- **Source**: Academic research
- **Authority**: Medium (evidence-based)
- **Examples**: [List findings]
```

### Finding Structure

Use consistent structure for all findings:

```markdown
**Severity**: Critical | High | Medium | Low
**Category**: [Type of issue]
**Location**: [File:line or context]
**Description**: [What the issue is]
**Impact**: [Why it matters]
**Remediation**: [How to fix]
**Effort**: [Time estimate]
**Source**: Official | Community | Research
```

### Severity Levels

Define clear severity criteria:

- **Critical**: Security risk, production-blocking (fix immediately)
- **High**: Significant quality issue (fix this sprint)
- **Medium**: Moderate improvement (schedule for next quarter)
- **Low**: Minor optimization (backlog)

### Score Calculation

Provide quantitative scoring:

```
Overall Health Score (0-100):
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- 40-59: Poor
- 0-39: Critical

Category Scores:
- Security: Should always be 100
- Compliance: Aim for 80+
- Best Practices: 70+ is good
```

## Example: CLAUDE.md Auditor

**Validation Against:**
1. Official Anthropic documentation (docs.claude.com)
2. Community best practices (field experience)
3. Academic research (LLM context optimization)

**Finding Categories:**
- Security (secrets, sensitive data)
- Official Compliance (Anthropic guidelines)
- Best Practices (community recommendations)
- Structure (organization, formatting)

**Output Modes:**
1. Audit Report - Detailed findings
2. JSON Report - Machine-readable for CI/CD
3. Refactored File - Production-ready output

## Validation Workflow

### Step 1: Discovery
- Locate target artifact(s)
- Calculate metrics (size, complexity)
- Read content for analysis

### Step 2: Analysis
Run validators in priority order:
1. Security Validation (CRITICAL)
2. Official Compliance
3. Best Practices
4. Optimization Opportunities

### Step 3: Scoring
- Calculate overall health score
- Generate category-specific scores
- Count findings by severity

### Step 4: Reporting
- Generate human-readable report
- Provide machine-readable output
- Offer remediation options

## Best Practices

1. **Prioritize Security**: Always check security first
2. **Source Attribution**: Label each finding with its source
3. **Actionable Remediation**: Provide specific fix instructions
4. **Multiple Output Formats**: Support markdown, JSON, HTML
5. **Incremental Improvement**: Don't overwhelm with all issues
6. **Track Over Time**: Support baseline comparisons
7. **CI/CD Integration**: Provide exit codes and JSON output

## Report Structure

```markdown
# [Artifact] Audit Report

## Executive Summary
- Overall health score: [X/100]
- Critical findings: [count]
- High findings: [count]
- Top 3 priorities

## File Metrics
- [Relevant size/complexity metrics]

## Detailed Findings

### Critical Issues
[Grouped by category]

### High Priority Issues
[Grouped by category]

### Medium Priority Issues
[Grouped by category]

## Remediation Plan
- P0: IMMEDIATE (critical)
- P1: THIS SPRINT (high)
- P2: NEXT QUARTER (medium)
- P3: BACKLOG (low)
```

## Success Criteria Template

```markdown
A well-validated [artifact] should achieve:

- ✅ Security Score: 100/100
- ✅ Compliance Score: 80+/100
- ✅ Overall Health: 75+/100
- ✅ Zero CRITICAL findings
- ✅ < 3 HIGH findings
- ✅ [Artifact-specific criteria]
```
