# Severity Matrix & Issue Prioritization

This document defines how to categorize and prioritize issues found during codebase audits.

## Severity Levels

### Critical (P0) - Fix Immediately

**Definition**: Issues that pose immediate risk to security, data integrity, or production stability.

**Characteristics**:
- Security vulnerabilities with known exploits (CVE scores >= 9.0)
- Secrets or credentials exposed in code
- Data loss or corruption risks
- Production-breaking bugs
- Authentication/authorization bypasses
- SQL injection or XSS vulnerabilities
- Compliance violations (GDPR, HIPAA, etc.)

**Timeline**: Must be fixed within 24 hours
**Effort vs Impact**: Fix immediately regardless of effort
**Deployment**: Requires immediate hotfix release

**Examples**:
- API key committed to repository
- SQL injection vulnerability in production endpoint
- Authentication bypass allowing unauthorized access
- Critical CVE in production dependency (e.g., log4shell)
- Unencrypted PII being transmitted over HTTP
- Memory leak causing production crashes

---

### High (P1) - Fix This Sprint

**Definition**: Significant issues that impact quality, security, or user experience but don't pose immediate production risk.

**Characteristics**:
- Medium-severity security vulnerabilities (CVE scores 7.0-8.9)
- Critical path missing test coverage
- Performance bottlenecks affecting user experience
- WCAG AA accessibility violations
- TypeScript strict mode violations in critical code
- High cyclomatic complexity (> 20) in business logic
- Missing error handling in critical operations

**Timeline**: Fix within current sprint (2 weeks)
**Effort vs Impact**: Prioritize high-impact, low-effort fixes first
**Deployment**: Include in next regular release

**Examples**:
- Payment processing code with 0% test coverage
- Page load time > 3 seconds
- Form inaccessible to screen readers
- 500+ line function with complexity of 45
- Unhandled promise rejections in checkout flow
- Dependency with moderate CVE (6.5 score)

---

### Medium (P2) - Fix Next Quarter

**Definition**: Issues that reduce code maintainability, developer productivity, or future scalability but don't immediately impact users.

**Characteristics**:
- Code smells and duplication
- Low-severity security issues (CVE scores 4.0-6.9)
- Test coverage between 60-80%
- Documentation gaps
- Minor performance optimizations
- Outdated dependencies (no CVEs)
- Moderate complexity (10-20)
- Technical debt accumulation

**Timeline**: Fix within next quarter (3 months)
**Effort vs Impact**: Plan during sprint planning, batch similar fixes
**Deployment**: Include in planned refactoring releases

**Examples**:
- 15% code duplication across services
- Missing JSDoc for public API
- God class with 25 public methods
- Build time of 5 minutes
- Test suite takes 10 minutes to run
- Dependency 2 major versions behind (stable)

---

### Low (P3) - Backlog

**Definition**: Minor improvements, stylistic issues, or optimizations that have minimal impact on functionality or quality.

**Characteristics**:
- Stylistic inconsistencies
- Minor code smells
- Documentation improvements
- Nice-to-have features
- Long-term architectural improvements
- Code coverage 80-90% (already meets minimum)
- Low complexity optimizations (< 10)

**Timeline**: Address when time permits or during dedicated tech debt sprints
**Effort vs Impact**: Only fix if effort is minimal or during slow periods
**Deployment**: Bundle with feature releases

**Examples**:
- Inconsistent variable naming (camelCase vs snake_case)
- Missing comments on simple functions
- Single-character variable names in non-critical code
- Console.log in development-only code
- README could be more detailed
- Opportunity to refactor small utility function

---

## Scoring Rubric

Use this matrix to assign severity levels:

| Impact | Effort Low | Effort Medium | Effort High |
|--------|------------|---------------|-------------|
| **Critical** | P0 | P0 | P0 |
| **High** | P1 | P1 | P1 |
| **Medium** | P1 | P2 | P2 |
| **Low** | P2 | P3 | P3 |

### Impact Assessment

**Critical Impact**:
- Security breach
- Data loss/corruption
- Production outage
- Legal/compliance violation

**High Impact**:
- User experience degraded
- Performance issues
- Accessibility barriers
- Development velocity reduced significantly

**Medium Impact**:
- Code maintainability reduced
- Technical debt accumulating
- Future changes more difficult
- Developer productivity slightly reduced

**Low Impact**:
- Minimal user/developer effect
- Cosmetic issues
- Future-proofing
- Best practice deviations

### Effort Estimation

**Low Effort**: < 4 hours
- Simple configuration change
- One-line fix
- Update dependency version

**Medium Effort**: 4 hours - 2 days
- Refactor single module
- Add test coverage for feature
- Implement security fix with tests

**High Effort**: > 2 days
- Architectural changes
- Major refactoring
- Migration to new framework/library
- Comprehensive security overhaul

---

## Category-Specific Severity Guidelines

### Security Issues

| Finding | Severity |
|---------|----------|
| Known exploit in production | Critical |
| Secrets in code | Critical |
| Authentication bypass | Critical |
| SQL injection | Critical |
| XSS vulnerability | High |
| CSRF vulnerability | High |
| Outdated dependency (CVE 7-9) | High |
| Outdated dependency (CVE 4-7) | Medium |
| Missing security headers | Medium |
| Weak encryption algorithm | Medium |

### Code Quality Issues

| Finding | Severity |
|---------|----------|
| Complexity > 50 | High |
| Complexity 20-50 | Medium |
| Complexity 10-20 | Low |
| Duplication > 20% | High |
| Duplication 10-20% | Medium |
| Duplication 5-10% | Low |
| File > 1000 LOC | Medium |
| File > 500 LOC | Low |
| Dead code (unused for > 6 months) | Low |

### Test Coverage Issues

| Finding | Severity |
|---------|----------|
| Critical path untested | High |
| Coverage < 50% | High |
| Coverage 50-80% | Medium |
| Coverage 80-90% | Low |
| Flaky tests | Medium |
| Slow tests (> 10 min) | Medium |
| No E2E tests | Medium |
| Missing edge case tests | Low |

### Performance Issues

| Finding | Severity |
|---------|----------|
| Page load > 5s | High |
| Page load 3-5s | Medium |
| Memory leak | High |
| O(n²) in hot path | High |
| Bundle size > 5MB | Medium |
| Build time > 10 min | Medium |
| Unoptimized images | Low |

### Accessibility Issues

| Finding | Severity |
|---------|----------|
| No keyboard navigation | High |
| Contrast ratio < 3:1 | High |
| Missing ARIA labels | High |
| Heading hierarchy broken | Medium |
| Missing alt text | Medium |
| Focus indicators absent | Medium |
| Color-only information | Low |

---

## Remediation Priority Formula

Use this formula to calculate a priority score:

```
Priority Score = (Impact × 10) + (Frequency × 5) - (Effort × 2)
```

Where:
- **Impact**: 1-10 (10 = critical)
- **Frequency**: 1-10 (10 = affects all users/code)
- **Effort**: 1-10 (10 = requires months of work)

Sort issues by priority score (highest first) to create your remediation plan.

### Example Calculations

**Example 1**: SQL Injection in Login
- Impact: 10 (critical security issue)
- Frequency: 10 (affects all users)
- Effort: 3 (straightforward fix with prepared statements)
- Score: (10 × 10) + (10 × 5) - (3 × 2) = **144** → **P0**

**Example 2**: Missing Tests on Helper Utility
- Impact: 4 (low risk, helper function)
- Frequency: 2 (rarely used)
- Effort: 2 (quick to test)
- Score: (4 × 10) + (2 × 5) - (2 × 2) = **46** → **P3**

**Example 3**: Performance Bottleneck in Search
- Impact: 7 (user experience degraded)
- Frequency: 8 (common feature)
- Effort: 6 (requires algorithm optimization)
- Score: (7 × 10) + (8 × 5) - (6 × 2) = **98** → **P1**

---

## Escalation Criteria

Escalate to leadership when:
- 5+ Critical issues found
- 10+ High issues in production code
- SQALE rating of D or E
- Security issues require disclosure
- Compliance violations detected
- Technical debt > 50% of development capacity

---

## Review Cycles

Recommended audit frequency based on project type:

| Project Type | Audit Frequency | Focus Areas |
|-------------|-----------------|-------------|
| Production SaaS | Monthly | Security, Performance, Uptime |
| Enterprise Software | Quarterly | Compliance, Security, Quality |
| Internal Tools | Semi-annually | Technical Debt, Maintainability |
| Open Source | Per major release | Security, Documentation, API stability |
| Startup MVP | Before funding rounds | Security, Scalability, Technical Debt |

---

**Last Updated**: 2024-25 Standards
**Version**: 1.0
