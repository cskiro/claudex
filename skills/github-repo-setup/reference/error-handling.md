# Error Handling

## Common Issues

### GitHub CLI not authenticated

**Detect**: `gh auth status` fails

**Solution**:
```bash
gh auth login
# Follow prompts to authenticate
```

### Repository name conflicts

**Detect**: API error for existing repo

**Solution**:
- Check availability: `gh repo view <owner>/<name>`
- Suggest alternative names
- Offer to use different organization

### Insufficient permissions

**Detect**: 403 errors from API

**Solution**:
- Verify organization membership
- Check repository permissions
- Contact organization admin for elevated access

### Missing git configuration

**Detect**: `git config` returns empty

**Solution**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Rate limiting

**Detect**: 429 errors from API

**Solution**:
- Wait for rate limit reset
- Check limit: `gh api /rate_limit`
- Retry with exponential backoff

## Success Criteria

- [ ] Repository created with appropriate visibility
- [ ] Security features enabled (Dependabot, secret scanning)
- [ ] Complete documentation (README, LICENSE, community files)
- [ ] CI/CD workflows configured and functional
- [ ] Issue and PR templates set up
- [ ] Branch protection rules active (enterprise/team modes)
- [ ] CODEOWNERS configured (team mode)
- [ ] Repository accessible and cloneable
- [ ] Validation checks pass
- [ ] User has clear next steps
