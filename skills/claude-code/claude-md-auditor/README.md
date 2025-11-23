# CLAUDE.md Auditor

> Comprehensive validation and optimization tool for CLAUDE.md memory files in Claude Code

An Anthropic Skill that analyzes CLAUDE.md configuration files against **official Anthropic documentation**, **community best practices**, and **academic research** on LLM context optimization.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-stable-green.svg)]()

---

## Quick Start

### With Claude Code (Recommended)

```bash
# 1. Copy skill to your skills directory
cp -r claude-md-auditor ~/.claude/skills/

# 2. Use in Claude Code
claude
> Audit my CLAUDE.md using the claude-md-auditor skill
```

### Direct Script Usage

```bash
# Markdown audit report
python claude-md-auditor/scripts/analyzer.py ./CLAUDE.md

# JSON report (for CI/CD)
python claude-md-auditor/scripts/report_generator.py ./CLAUDE.md json > audit.json

# Generate refactored CLAUDE.md
python claude-md-auditor/scripts/report_generator.py ./CLAUDE.md refactored > CLAUDE_refactored.md
```

---

## What Does It Do?

### Validates Against Three Sources

| Source | Authority | Examples |
|--------|-----------|----------|
| **✅ Official Anthropic Docs** | Highest | Memory hierarchy, import syntax, "keep them lean" |
| **💡 Community Best Practices** | Medium | 100-300 line target, 80/20 rule, maintenance cadence |
| **🔬 Academic Research** | Medium | "Lost in the middle" positioning, token optimization |

### Detects Issues

- **🚨 CRITICAL**: Secrets (API keys, passwords), security vulnerabilities
- **⚠️ HIGH**: Generic content, excessive verbosity, vague instructions
- **📋 MEDIUM**: Outdated info, broken links, duplicate sections
- **ℹ️ LOW**: Formatting issues, organizational improvements

### Generates Output

1. **Markdown Report**: Human-readable audit with detailed findings
2. **JSON Report**: Machine-readable for CI/CD integration
3. **Refactored CLAUDE.md**: Production-ready improved version

---

## Features

### 🔒 Security Validation (CRITICAL)

Detects exposed secrets using pattern matching:

- API keys (OpenAI, AWS, generic)
- Tokens and passwords
- Database connection strings
- Private keys (PEM format)
- Internal IP addresses

**Why Critical**: CLAUDE.md files are often committed to git. Exposed secrets can leak through history, PRs, logs, or backups.

### ✅ Official Compliance

Validates against [docs.claude.com](https://docs.claude.com) guidance:

- File length ("keep them lean")
- Generic content (Claude already knows basic programming)
- Import syntax (`@path/to/import`, max 5 hops)
- Vague instructions (specific vs. ambiguous)
- Proper markdown structure

### 💡 Best Practices

Evaluates community recommendations:

- Optimal file length (100-300 lines)
- Token usage (< 3,000 tokens / <2% of 200K context)
- Organization (sections, headers, priority markers)
- Maintenance (update dates, version info)
- Duplicate or conflicting content

### 🔬 Research Optimization

Applies academic insights:

- **"Lost in the Middle"** positioning (critical info at top/bottom)
- Token efficiency and context utilization
- Chunking and information architecture
- Attention pattern optimization

**Based On**:
- "Lost in the Middle" (Liu et al., 2023, TACL)
- Claude-specific performance studies
- Context awareness research (MIT/Google Cloud AI, 2024)

---

## Installation

### Option 1: Claude Code Skills (Recommended)

```bash
# Clone or copy to your skills directory
mkdir -p ~/.claude/skills
cp -r claude-md-auditor ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/claude-md-auditor/SKILL.md
```

### Option 2: Standalone Scripts

```bash
# Clone repository
git clone https://github.com/cskiro/annex.git
cd annex/claude-md-auditor

# Run directly (Python 3.8+ required, no dependencies)
python scripts/analyzer.py path/to/CLAUDE.md
```

### Requirements

- **Python**: 3.8 or higher
- **Dependencies**: None (uses standard library only)
- **Claude Code**: Any version with Skills support (optional)

---

## Usage

### Basic Audit

**With Claude Code**:
```
Audit my CLAUDE.md using the claude-md-auditor skill.
```

**Direct**:
```bash
python scripts/analyzer.py ./CLAUDE.md
```

**Output**:
```
============================================================
CLAUDE.md Audit Results: ./CLAUDE.md
============================================================

Overall Health Score: 78/100
Security Score: 100/100
Official Compliance Score: 75/100
Best Practices Score: 70/100
Research Optimization Score: 85/100

============================================================
Findings Summary:
  🚨 Critical: 0
  ⚠️  High: 2
  📋 Medium: 3
  ℹ️  Low: 5
============================================================
```

### Generate JSON Report

**For CI/CD Integration**:

```bash
python scripts/report_generator.py ./CLAUDE.md json > audit.json
```

**Example Output**:
```json
{
  "metadata": {
    "file": "./CLAUDE.md",
    "generated_at": "2025-10-26 10:30:00",
    "tier": "Project"
  },
  "scores": {
    "overall": 78,
    "security": 100,
    "official_compliance": 75,
    "critical_count": 0,
    "high_count": 2
  },
  "findings": [...]
}
```

### Generate Refactored File

**Create improved CLAUDE.md**:

```bash
python scripts/report_generator.py ./CLAUDE.md refactored > CLAUDE_refactored.md
```

This generates a production-ready file with:
- ✅ Optimal structure (critical at top, reference at bottom)
- ✅ Research-based positioning ("lost in the middle" mitigation)
- ✅ All security issues removed
- ✅ Best practices applied
- ✅ Inline comments for maintenance

---

## Output Examples

### Markdown Report Structure

```markdown
# CLAUDE.md Audit Report

## Executive Summary
- Overall health: 78/100 (Good)
- Status: ⚠️ **HIGH PRIORITY** - Address this sprint
- Total findings: 10 (0 critical, 2 high, 3 medium, 5 low)

## Score Dashboard
| Category | Score | Status |
|----------|-------|--------|
| Security | 100/100 | ✅ Excellent |
| Official Compliance | 75/100 | 🟢 Good |
| Best Practices | 70/100 | 🟢 Good |

## Detailed Findings

### ⚠️ HIGH Priority

#### 1. Generic Programming Content Detected
**Category**: Official Compliance
**Source**: Official Guidance

**Description**: File contains generic React documentation

**Impact**: Wastes context window. Official guidance:
"Don't include basic programming concepts Claude already understands"

**Remediation**: Remove generic content. Focus on project-specific standards.

---
```

### JSON Report Structure

```json
{
  "metadata": {
    "file_path": "./CLAUDE.md",
    "line_count": 245,
    "token_estimate": 3240,
    "context_usage_200k": 1.62,
    "tier": "Project"
  },
  "scores": {
    "overall": 78,
    "security": 100,
    "official_compliance": 75,
    "best_practices": 70,
    "research_optimization": 85
  },
  "findings": [
    {
      "severity": "high",
      "category": "official_compliance",
      "title": "Generic Programming Content Detected",
      "description": "File contains generic React documentation",
      "line_number": 42,
      "source": "official",
      "remediation": "Remove generic content..."
    }
  ]
}
```

---

## Reference Documentation

### Complete Validation Criteria

All checks are documented in the `reference/` directory:

| Document | Content | Source |
|----------|---------|--------|
| **official_guidance.md** | Complete official Anthropic documentation | docs.claude.com |
| **best_practices.md** | Community recommendations and field experience | Practitioners |
| **research_insights.md** | Academic research on LLM context optimization | Peer-reviewed papers |
| **anti_patterns.md** | Catalog of common mistakes and violations | Field observations |

### Key References

- [Memory Management](https://docs.claude.com/en/docs/claude-code/memory) - Official docs
- ["Lost in the Middle"](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/) - Academic paper
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic blog

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: CLAUDE.md Audit

on:
  pull_request:
    paths:
      - '**/CLAUDE.md'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run CLAUDE.md Audit
        run: |
          python claude-md-auditor/scripts/analyzer.py CLAUDE.md \
            --format json \
            --output audit.json

      - name: Check Critical Issues
        run: |
          CRITICAL=$(python -c "import json; print(json.load(open('audit.json'))['summary']['critical'])")

          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Critical issues found in CLAUDE.md"
            exit 1
          fi

          echo "✅ CLAUDE.md validation passed"
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q "CLAUDE.md"; then
  echo "Validating CLAUDE.md..."

  python claude-md-auditor/scripts/analyzer.py CLAUDE.md > /tmp/audit.txt

  # Check exit code or parse output
  if grep -q "🚨 Critical: [1-9]" /tmp/audit.txt; then
    echo "❌ CLAUDE.md has critical issues"
    cat /tmp/audit.txt
    exit 1
  fi

  echo "✅ CLAUDE.md validation passed"
fi
```

### VS Code Task

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Audit CLAUDE.md",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/claude-md-auditor/scripts/analyzer.py",
        "${workspaceFolder}/CLAUDE.md"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

---

## Understanding Scores

### Overall Health Score (0-100)

| Range | Status | Action |
|-------|--------|--------|
| 90-100 | ✅ Excellent | Minor optimizations only |
| 75-89 | 🟢 Good | Some improvements recommended |
| 60-74 | 🟡 Fair | Schedule improvements this quarter |
| 40-59 | 🟠 Poor | Significant issues to address |
| 0-39 | 🔴 Critical | Immediate action required |

### Severity Levels

- **🚨 CRITICAL**: Security risks (fix immediately, within 24 hours)
- **⚠️ HIGH**: Significant issues (fix this sprint, within 2 weeks)
- **📋 MEDIUM**: Moderate improvements (schedule for next quarter)
- **ℹ️ LOW**: Minor optimizations (backlog)

### Category Scores

- **Security**: Should always be 100 (any security issue is critical)
- **Official Compliance**: Aim for 80+ (follow Anthropic guidance)
- **Best Practices**: 70+ is good (community recommendations are flexible)
- **Research Optimization**: 60+ is acceptable (optimizations, not requirements)

---

## Real-World Examples

### Example 1: Security Violation

**Before** (Anti-Pattern):
```markdown
# CLAUDE.md

## API Configuration
- API Key: sk-1234567890abcdefghijklmnop
- Database: postgres://admin:pass@10.0.1.42/db
```

**Audit Finding**:
```
🚨 CRITICAL: API Key Detected
Line: 4
Impact: Security breach risk. Secrets exposed in git history.
Remediation:
1. Remove the API key immediately
2. Rotate the compromised credential
3. Use environment variables (.env file)
4. Clean git history if committed
```

**After** (Fixed):
```markdown
# CLAUDE.md

## API Configuration
- API keys: Stored in .env (see .env.example for template)
- Database: Use AWS Secrets Manager connection string
- Access: Contact team lead for credentials
```

### Example 2: Generic Content

**Before** (Anti-Pattern):
```markdown
## React Best Practices

React is a JavaScript library for building user interfaces.
It was created by Facebook in 2013. React uses a virtual
DOM for efficient updates...

[200 lines of React documentation]
```

**Audit Finding**:
```
⚠️ HIGH: Generic Programming Content Detected
Impact: Wastes context window. Claude already knows React basics.
Remediation: Remove generic content. Focus on project-specific patterns.
```

**After** (Fixed):
```markdown
## React Standards (Project-Specific)

- Functional components only (no class components)
- Custom hooks location: /src/hooks
- Co-location pattern: Component + test + styles in same directory
- Props interface naming: [ComponentName]Props
```

### Example 3: Optimal Structure

**Generated Refactored File**:
```markdown
# MyApp

## 🚨 CRITICAL: Must-Follow Standards

<!-- Top position = highest attention -->

- Security: Never commit secrets to git
- TypeScript strict mode: No `any` types
- Testing: 80% coverage on all new code

## 📋 Project Overview

**Tech Stack**: React, TypeScript, Vite, PostgreSQL
**Architecture**: Feature-based modules, clean architecture
**Purpose**: Enterprise CRM system

## 🔧 Development Workflow

### Git
- Branches: `feature/{name}`, `bugfix/{name}`
- Commits: Conventional format required
- PRs: Tests + review + passing CI

## 📝 Code Standards

[Project-specific rules here]

## 📌 REFERENCE: Common Tasks

<!-- Bottom position = recency attention -->

```bash
npm run build        # Build production
npm test            # Run tests
npm run deploy      # Deploy to staging
```

### Key Files
- Config: `/config/app.config.ts`
- Types: `/src/types/index.ts`
```

---

## FAQ

### Q: Will this skill automatically fix my CLAUDE.md?

**A**: No, but it can generate a refactored version. You need to review and apply changes manually to ensure they fit your project.

### Q: Are all recommendations mandatory?

**A**: No. Check the **source** field:
- **Official**: Follow Anthropic documentation (highest priority)
- **Community**: Recommended best practices (flexible)
- **Research**: Evidence-based optimizations (optional)

### Q: What if I disagree with a finding?

**A**: That's okay! Best practices are guidelines, not requirements. Official guidance should be followed, but community and research recommendations can be adapted to your context.

### Q: How often should I audit CLAUDE.md?

**A**:
- **On every change**: Before committing (use pre-commit hook)
- **Quarterly**: Regular maintenance audit
- **Before major releases**: Ensure standards are up-to-date
- **When onboarding**: Validate project configuration

### Q: Can I use this in my CI/CD pipeline?

**A**: Yes! Use JSON output mode and check for critical findings. Example provided in CI/CD Integration section.

### Q: Does this validate that Claude actually follows the standards?

**A**: No, this only validates the CLAUDE.md structure and content. To test effectiveness, start a new Claude session and verify standards are followed without re-stating them.

---

## Limitations

### What This Skill CANNOT Do

- ❌ Automatically fix security issues (manual remediation required)
- ❌ Test if Claude follows standards (behavioral testing needed)
- ❌ Validate imported files beyond path existence
- ❌ Detect circular imports (requires graph traversal)
- ❌ Verify standards match actual codebase
- ❌ Determine if standards are appropriate for your project

### Known Issues

- Import depth validation (max 5 hops) not yet implemented
- Circular import detection not yet implemented
- Cannot read contents of imported files for validation

---

## Roadmap

### v1.1 (Planned)

- [ ] Import graph traversal (detect circular imports)
- [ ] Import depth validation (max 5 hops)
- [ ] Content validation of imported files
- [ ] Interactive CLI for guided fixes
- [ ] HTML dashboard report format

### v1.2 (Planned)

- [ ] Effectiveness testing (test if Claude follows standards)
- [ ] Diff mode (compare before/after audits)
- [ ] Metrics tracking over time
- [ ] Custom rule definitions
- [ ] Integration with popular IDEs

---

## Contributing

This skill is based on three authoritative sources:

1. **Official Anthropic Documentation** (docs.claude.com)
2. **Peer-Reviewed Academic Research** (MIT, Google Cloud AI, TACL)
3. **Community Field Experience** (practitioner reports)

To propose changes:

1. Identify which category (official/community/research)
2. Provide source documentation or evidence
3. Explain rationale and expected impact
4. Update relevant reference documentation

---

## License

Apache 2.0 - Example skill for demonstration purposes

---

## Version

**Current Version**: 1.0.0
**Last Updated**: 2025-10-26
**Python**: 3.8+
**Status**: Stable

---

## Credits

**Developed By**: Connor (based on Anthropic Skills framework)

**Research Sources**:
- Liu et al. (2023) - "Lost in the Middle" (TACL/MIT Press)
- MIT/Google Cloud AI (2024) - Attention calibration research
- Anthropic Engineering (2023-2025) - Claude documentation and blog

**Special Thanks**: Anthropic team for Claude Code and Skills framework

---

**🔗 Links**:
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Memory Management Guide](https://docs.claude.com/en/docs/claude-code/memory)

---

*Generated by claude-md-auditor v1.0.0*
