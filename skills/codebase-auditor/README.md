# Codebase Auditor Skill

> Comprehensive codebase audit tool based on modern SDLC best practices (2024-25 standards)

An Anthropic Skill that analyzes codebases for quality issues, security vulnerabilities, technical debt, and generates prioritized remediation plans.

## Features

- **Progressive Disclosure**: Three-phase analysis (Discovery → Deep Analysis → Report)
- **Multi-Language Support**: JavaScript, TypeScript, Python (extensible)
- **Comprehensive Analysis**:
  - Code Quality (complexity, duplication, code smells)
  - Security (secrets detection, OWASP Top 10, dependency vulnerabilities)
  - Testing (coverage analysis, testing trophy distribution)
  - Technical Debt (SQALE rating, remediation estimates)
- **Multiple Report Formats**: Markdown, JSON, HTML dashboard
- **Prioritized Remediation Plans**: P0-P3 severity with effort estimates
- **Industry Standards**: Based on 2024-25 SDLC best practices

## Installation

1. Copy the `codebase-auditor` directory to your Claude skills directory
2. Ensure Python 3.8+ is installed
3. No additional dependencies required (uses Python standard library)

## Usage with Claude Code

### Basic Audit

```
Audit this codebase using the codebase-auditor skill.
```

### Focused Audit

```
Run a security-focused audit on this codebase.
```

### Quick Health Check

```
Give me a quick health check of this codebase (Phase 1 only).
```

### Custom Scope

```
Audit this codebase focusing on:
- Test coverage and quality
- Security vulnerabilities
- Code complexity
```

## Direct Script Usage

```bash
# Full audit with Markdown report
python scripts/audit_engine.py /path/to/codebase --output report.md

# Security-focused audit
python scripts/audit_engine.py /path/to/codebase --scope security --output security-report.md

# JSON output for CI/CD integration
python scripts/audit_engine.py /path/to/codebase --format json --output report.json

# Quick health check only (Phase 1)
python scripts/audit_engine.py /path/to/codebase --phase quick
```

## Output Formats

### Markdown (Default)
Human-readable report with detailed findings and recommendations. Suitable for:
- Pull request comments
- Documentation
- Team reviews

### JSON
Machine-readable format for CI/CD integration. Includes:
- Structured findings
- Metrics and scores
- Full metadata

### HTML
Interactive dashboard with:
- Visual metrics
- Filterable findings
- Color-coded severity levels

## Audit Criteria

The skill audits based on 10 key categories:

1. **Code Quality**: Complexity, duplication, code smells, file/function length
2. **Testing**: Coverage, test quality, testing trophy distribution
3. **Security**: Secrets detection, OWASP Top 10, dependency vulnerabilities
4. **Architecture**: SOLID principles, design patterns, modularity
5. **Performance**: Build times, bundle size, runtime efficiency
6. **Documentation**: Code docs, README, architecture docs
7. **DevOps & CI/CD**: Pipeline maturity, deployment frequency, DORA metrics
8. **Dependencies**: Outdated packages, license compliance, CVEs
9. **Accessibility**: WCAG 2.1 AA compliance
10. **TypeScript Strict Mode**: Type safety, strict mode violations

See [`reference/audit_criteria.md`](reference/audit_criteria.md) for complete checklist.

## Severity Levels

- **Critical (P0)**: Fix immediately (within 24 hours)
  - Security vulnerabilities, secrets exposure, production-breaking bugs

- **High (P1)**: Fix this sprint (within 2 weeks)
  - Significant quality/security issues, critical path test gaps

- **Medium (P2)**: Fix next quarter (within 3 months)
  - Code smells, documentation gaps, moderate technical debt

- **Low (P3)**: Backlog
  - Stylistic issues, minor optimizations

See [`reference/severity_matrix.md`](reference/severity_matrix.md) for detailed criteria.

## Examples

See the [`examples/`](examples/) directory for:
- Sample audit report
- Sample remediation plan

## Architecture

```
codebase-auditor/
├── SKILL.md                      # Skill definition (Claude loads this)
├── README.md                     # This file
├── scripts/
│   ├── audit_engine.py          # Core orchestrator
│   ├── analyzers/               # Specialized analyzers
│   │   ├── code_quality.py      # Complexity, duplication, smells
│   │   ├── test_coverage.py     # Coverage analysis
│   │   ├── security_scan.py     # Security vulnerabilities
│   │   ├── dependencies.py      # Dependency health
│   │   ├── performance.py       # Performance analysis
│   │   └── technical_debt.py    # SQALE rating
│   ├── report_generator.py      # Multi-format reports
│   └── remediation_planner.py   # Prioritized action plans
├── reference/
│   ├── audit_criteria.md        # Complete audit checklist
│   ├── severity_matrix.md       # Issue prioritization
│   └── best_practices_2025.md   # SDLC standards
└── examples/
    ├── sample_report.md
    └── remediation_plan.md
```

## Extending the Skill

### Adding a New Analyzer

1. Create `scripts/analyzers/your_analyzer.py`
2. Implement `analyze(codebase_path, metadata)` function that returns findings list
3. Add to `ANALYZERS` dict in `audit_engine.py`

Example:
```python
def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    findings = []

    # Your analysis logic here

    findings.append({
        'severity': 'high',
        'category': 'your_category',
        'subcategory': 'specific_issue',
        'title': 'Issue title',
        'description': 'What was found',
        'file': 'path/to/file.js',
        'line': 42,
        'code_snippet': 'problematic code',
        'impact': 'Why it matters',
        'remediation': 'How to fix it',
        'effort': 'low|medium|high',
    })

    return findings
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Code Audit

on: [pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Codebase Audit
        run: |
          python codebase-auditor/scripts/audit_engine.py . \
            --format json \
            --output audit-report.json
      - name: Check for Critical Issues
        run: |
          CRITICAL=$(jq '.summary.critical_issues' audit-report.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Found $CRITICAL critical issues"
            exit 1
          fi
```

## Best Practices

1. **Run Incrementally**: For large codebases, use progressive disclosure
2. **Focus on Critical Paths**: Audit authentication, payment, data processing first
3. **Baseline Before Releases**: Establish quality gates before major releases
4. **Track Over Time**: Compare audits to measure improvement
5. **Integrate with CI/CD**: Automate for continuous monitoring
6. **Customize Thresholds**: Adjust severity based on project maturity

## Limitations

- Static analysis only (no runtime profiling)
- Requires source code access
- Dependency data requires internet access (for vulnerability databases)
- Large codebases may need chunked analysis

## Version

**1.0.0** - Initial release

## Standards Compliance

Based on:
- DORA State of DevOps Report 2024
- OWASP Top 10 (2024 Edition)
- WCAG 2.1 Guidelines
- Kent C. Dodds Testing Trophy
- SonarQube Quality Gates

## License

Apache 2.0 (example skill for demonstration)

---

**Built with**: Python 3.8+
**Anthropic Skill Version**: 1.0
**Last Updated**: 2024-10-21
