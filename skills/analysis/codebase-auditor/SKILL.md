---
name: codebase-auditor
description: Comprehensive codebase audit tool analyzing software engineering practices, security vulnerabilities, and technical debt using modern SDLC best practices (2024-25 standards). Use for code reviews, production readiness, or legacy codebase evaluation.
---

# Codebase Auditor

Comprehensive codebase audits using modern software engineering standards with actionable remediation plans.

## When to Use

- Audit codebase for quality, security, maintainability
- Assess technical debt and estimate remediation
- Prepare production readiness report
- Evaluate legacy codebase for modernization

## Audit Phases

### Phase 1: Initial Assessment
- Project discovery (tech stack, frameworks, tools)
- Quick health check (LOC, docs, git practices)
- Red flag detection (secrets, massive files)

### Phase 2: Deep Analysis
Load on demand based on Phase 1 findings.

### Phase 3: Report Generation
Comprehensive report with scores and priorities.

### Phase 4: Remediation Planning
Prioritized action plan with effort estimates.

## Analysis Categories

| Category | Key Checks |
|----------|------------|
| Code Quality | Complexity, duplication, code smells |
| Testing | Coverage (80% min), trophy distribution, quality |
| Security | OWASP Top 10, dependencies, secrets |
| Architecture | SOLID, patterns, modularity |
| Performance | Build time, bundle size, runtime |
| Documentation | JSDoc, README, ADRs |
| DevOps | CI/CD maturity, DORA metrics |
| Accessibility | WCAG 2.1 AA compliance |

## Technical Debt Rating (SQALE)

| Grade | Remediation Effort |
|-------|-------------------|
| A | <= 5% of dev time |
| B | 6-10% |
| C | 11-20% |
| D | 21-50% |
| E | > 50% |

## Usage Examples

```
# Basic audit
Audit this codebase using the codebase-auditor skill.

# Security focused
Run a security-focused audit on this codebase.

# Quick health check
Give me a quick health check (Phase 1 only).

# Custom scope
Audit focusing on test coverage and security.
```

## Output Formats

1. **Markdown Report** - Human-readable for PR comments
2. **JSON Report** - Machine-readable for CI/CD
3. **HTML Dashboard** - Interactive visualization
4. **Remediation Plan** - Prioritized action items

## Priority Levels

| Priority | Examples | Timeline |
|----------|----------|----------|
| P1 Critical | Security vulns, data loss risks | Immediate |
| P2 High | Coverage gaps, performance issues | This sprint |
| P3 Medium | Code smells, doc gaps | Next quarter |
| P4 Low | Stylistic, minor optimizations | Backlog |

## Best Practices

1. Run incrementally for large codebases
2. Focus on critical paths first
3. Baseline before major releases
4. Track metrics over time
5. Integrate with CI/CD

## Integrations

Complements: SonarQube, ESLint, Jest/Vitest, npm audit, Lighthouse, GitHub Actions

## Limitations

- Static analysis only (no runtime profiling)
- Requires source code access
- Internet needed for CVE data
- Large codebases need chunked analysis

## References

See `reference/` for:
- Complete audit criteria checklist
- Severity matrix and scoring rubric
- 2024-25 SDLC best practices guide
