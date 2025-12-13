# Open Source Mode

**Purpose**: Community-focused with templates and contribution guidelines (~90 seconds)

## Features Included

- All Quick Mode features
- ✅ CODE_OF_CONDUCT.md (Contributor Covenant)
- ✅ CONTRIBUTING.md
- ✅ Issue templates (bug, feature, question)
- ✅ PR template
- ✅ SUPPORT.md
- ✅ Dependabot alerts
- ✅ Basic CI workflow

## When to Use

- Open source projects
- Community-driven software
- Public libraries/tools
- Projects accepting contributions

## Community Health Files

### CODE_OF_CONDUCT.md

Use Contributor Covenant v2.1:
```markdown
# Contributor Covenant Code of Conduct

## Our Pledge
We pledge to make participation in our community a harassment-free experience...
```

### CONTRIBUTING.md

```markdown
# Contributing

Thank you for your interest in contributing!

## How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Code of Conduct
Please read our [Code of Conduct](CODE_OF_CONDUCT.md)
```

## Issue Templates

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug
body:
  - type: textarea
    id: description
    label: Describe the bug
    validations:
      required: true
  - type: textarea
    id: reproduction
    label: Steps to reproduce
```

## Next Steps After Setup

1. Add comprehensive README with badges
2. Set up project board for issue tracking
3. Configure Discussions for community Q&A
4. Add CHANGELOG.md
