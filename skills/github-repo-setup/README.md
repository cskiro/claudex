# GitHub Repository Setup Skill

> **Automated GitHub repository creation following official best practices and modern standards**

## Overview

This skill automates the setup of GitHub repositories with four distinct modes tailored to different use cases. Each mode follows GitHub's official best practices, implementing appropriate security features, documentation standards, and workflow automation.

## Features

### Four Modes

1. **Quick Mode** (~30s)
   - Fast public repo setup
   - Essential files: README, LICENSE, .gitignore
   - Perfect for experiments and prototypes

2. **Enterprise Mode** (~120s)
   - Production-ready setup
   - Full security features (Dependabot, secret scanning, CodeQL)
   - CI/CD workflows with GitHub Actions
   - Branch protection with required reviews
   - Automated testing and deployment

3. **Open Source Mode** (~90s)
   - Community-focused configuration
   - Community health files (CODE_OF_CONDUCT, CONTRIBUTING)
   - Issue and PR templates
   - GitHub form schema integration
   - Contributor guidelines

4. **Private/Team Mode** (~90s)
   - Internal collaboration setup
   - CODEOWNERS configuration
   - Governance documentation
   - Team access controls
   - Review requirements

### Security Features (Based on GitHub Official Best Practices)

- ✅ Dependabot alerts and automated security fixes
- ✅ Secret scanning with push protection
- ✅ Code scanning with CodeQL (enterprise mode)
- ✅ SECURITY.md with vulnerability reporting
- ✅ Branch protection rules
- ✅ Required status checks

### Documentation Standards

- ✅ Comprehensive README with badges
- ✅ Appropriate LICENSE selection
- ✅ Technology-specific .gitignore
- ✅ Community health files
- ✅ Contributing guidelines
- ✅ Support resources

### CI/CD Automation

- ✅ GitHub Actions workflows
- ✅ Automated testing
- ✅ Linting and code quality checks
- ✅ Security scanning
- ✅ Deployment pipelines (optional)

## Prerequisites

- **GitHub CLI** (`gh`) - [Installation guide](https://cli.github.com/)
- **Git** - Configured with user.name and user.email
- **GitHub Account** - Authenticated via `gh auth login`
- **Permissions** - Repository creation access (organization admin for org repos)

## Usage

### Quick Examples

```bash
# Quick mode - minimal setup
"Create a quick GitHub repo for testing"

# Enterprise mode - full production setup
"Set up an enterprise GitHub repository with CI/CD"

# Open source mode - community project
"Create an open source GitHub project"

# Private/team mode - internal collaboration
"Set up a private team repository with governance"
```

### Detailed Workflow

1. **Invoke the skill** with your request
2. **Select mode** (or let AI detect from your request)
3. **Provide repository details**:
   - Name
   - Description
   - Visibility (public/private/internal)
   - Technology stack (for .gitignore)
   - License preference
4. **Review configuration** and confirm
5. **Skill executes** setup automatically
6. **Receive** validation report and next steps

## What Gets Created

### All Modes
- Repository with proper visibility
- README.md with project info
- LICENSE file
- .gitignore for tech stack
- Initial git setup with main branch

### Additional (Enterprise/Open Source/Team)
- Security features enabled
- CI/CD workflows configured
- Issue and PR templates
- Branch protection rules
- Community health files
- CODEOWNERS (team mode)

## Example Output

```
✅ Repository Setup Complete: myorg/my-project

## Enabled Features
- ✅ Repository created (public)
- ✅ Dependabot alerts enabled
- ✅ Secret scanning active
- ✅ Branch protection configured
- ✅ CI workflow created
- ✅ Issue templates added
- ✅ Community files complete

## Quick Start
gh repo clone myorg/my-project
cd my-project
git checkout -b feature/initial-code
# Add your code
git commit -m "feat: initial implementation"
git push -u origin feature/initial-code
gh pr create

## Repository URL
https://github.com/myorg/my-project
```

## Best Practices Applied

This skill implements GitHub's official best practices:

1. **Security First** - Dependabot, secret scanning, and push protection enabled by default
2. **Documentation Standards** - README, LICENSE, and community health files
3. **Branch Protection** - Protected main branch with required reviews
4. **CI/CD Integration** - Automated testing and quality checks
5. **Collaboration Workflow** - PR-based development with templates
6. **Access Control** - CODEOWNERS for critical files
7. **Community Guidelines** - Clear contribution and conduct standards

## Customization

After initial setup, you can customize:

- Modify CI/CD workflows in `.github/workflows/`
- Adjust branch protection rules via GitHub settings
- Update issue templates in `.github/ISSUE_TEMPLATE/`
- Edit CODEOWNERS for review requirements
- Configure additional integrations

## Troubleshooting

### Authentication Issues
```bash
# Check auth status
gh auth status

# Re-authenticate
gh auth login
```

### Permission Errors
- Ensure you have repository creation permissions
- For organization repos, confirm admin access
- Check organization security settings

### CLI Not Found
```bash
# Install GitHub CLI
brew install gh  # macOS
# Or visit: https://cli.github.com/
```

## References

- [GitHub Best Practices for Repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [Community Health Files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

## License

Apache-2.0

## Version

v0.1.0 - Initial release
