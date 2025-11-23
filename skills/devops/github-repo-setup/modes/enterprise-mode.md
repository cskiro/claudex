# Enterprise Mode

**Purpose**: Production-ready with security features, CI/CD, and branch protection (~120 seconds)

## Features Included

- All Quick Mode features
- ✅ Dependabot alerts and security updates
- ✅ Secret scanning with push protection
- ✅ CodeQL code scanning
- ✅ Branch protection rules
- ✅ CI/CD workflows
- ✅ Issue and PR templates
- ✅ SECURITY.md
- ✅ Required status checks

## When to Use

- Production applications
- Client projects
- Enterprise software
- Any project requiring security compliance

## Security Configuration

```bash
# Enable Dependabot
gh api -X PUT /repos/{owner}/{repo}/vulnerability-alerts
gh api -X PUT /repos/{owner}/{repo}/automated-security-fixes

# Enable secret scanning
gh api -X PUT /repos/{owner}/{repo}/secret-scanning
gh api -X PUT /repos/{owner}/{repo}/secret-scanning-push-protection
```

## Branch Protection

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null
}
```

## CI/CD Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Next Steps After Setup

1. Configure environment secrets
2. Set up deployment pipeline
3. Add team members with appropriate permissions
4. Review security alerts dashboard
