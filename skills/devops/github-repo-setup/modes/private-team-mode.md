# Private/Team Mode

**Purpose**: Internal collaboration with CODEOWNERS and governance (~90 seconds)

## Features Included

- All Quick Mode features
- ✅ Private visibility
- ✅ CODEOWNERS file
- ✅ GOVERNANCE.md
- ✅ Branch protection rules
- ✅ Team access configuration
- ✅ Issue and PR templates
- ✅ Review requirements

## When to Use

- Internal team projects
- Company repositories
- Private client work
- Projects with access controls

## CODEOWNERS Configuration

```
# .github/CODEOWNERS

# Default owners for everything
* @team-leads

# Specific paths
/src/ @development-team
/docs/ @documentation-team
/.github/ @devops-team
/security/ @security-team
```

## Team Access

```bash
# Add team with write access
gh api -X PUT /orgs/{org}/teams/{team}/repos/{owner}/{repo} \
  -f permission=write

# Add individual collaborator
gh repo add-collaborator <username> --permission write
```

## Governance Documentation

### GOVERNANCE.md

```markdown
# Governance

## Decision Making
- Technical decisions: Development team lead
- Product decisions: Product manager
- Security decisions: Security team lead

## Code Review Requirements
- All PRs require 1 approval
- Security-sensitive changes require security team review
- Breaking changes require team lead approval

## Release Process
1. Create release branch
2. Run full test suite
3. Get release approval
4. Tag and deploy
```

## Next Steps After Setup

1. Invite team members
2. Configure team permissions
3. Set up project milestones
4. Document team workflows
