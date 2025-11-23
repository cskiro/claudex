# Troubleshooting

## Tag creation fails with "already exists"

**Symptoms**: `git tag` returns error "tag 'component@1.0.0' already exists"

**Solution**:
1. Check if tag exists: `git tag -l "component@1.0.0"`
2. If exists locally but wrong, delete: `git tag -d component@1.0.0`
3. If exists remotely, coordinate with team before deleting
4. Choose next version number instead (e.g., 1.0.1)

**Prevention**: Always check latest version before creating tags: `git tag -l "component@*" --sort=-v:refname | head -1`

---

## Tag pushed but GitHub release not visible

**Symptoms**: `git tag` exists but doesn't show in GitHub releases page

**Solution**:
1. Verify tag pushed to remote: `git ls-remote --tags origin | grep component@1.0.0`
2. Create GitHub release manually: `gh release create component@1.0.0`
3. Or use GitHub web UI: Releases → "Draft a new release" → Choose tag

**Prevention**: Git tags and GitHub releases are separate. Tags don't automatically create releases.

---

## CI/CD not triggering on tag push

**Symptoms**: Pushed tag but workflow didn't run

**Solution**:
1. Check workflow tag pattern: Does `marketplace@*` match your tag format?
2. Verify trigger configured:
   ```yaml
   on:
     push:
       tags:
         - 'marketplace@*'
   ```
3. Test pattern locally: `echo "marketplace@1.0.0" | grep -E "marketplace@.*"`

**Prevention**: Document and test tag patterns before setting up automation

---

## Monorepo tags confusing (which component version?)

**Symptoms**: Hard to tell which version applies to which component

**Solution**:
1. Always use namespaced tags: `component@X.Y.Z`
2. Never use flat tags (`v1.0.0`) in monorepos
3. List tags by component: `git tag -l "component@*"`
4. Update README with tagging convention

**Prevention**: Establish and document tag namespace convention early in project
