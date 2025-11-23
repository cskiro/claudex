# Phase 3: Create Git Tags

**Purpose**: Execute tag creation commands after user confirmation.

## Steps

### 1. Prepare Tag Details

```
Tag name: marketplace@1.1.4
Tag message: "Release marketplace 1.1.4"
Tag type: Annotated (with metadata)
```

### 2. Show Exact Commands to be Executed

```bash
# Commands that will run:
git tag -a "marketplace@1.1.4" -m "Release marketplace 1.1.4"
git push origin marketplace@1.1.4
```

### 3. Request User Confirmation

```
Ready to create and push tag marketplace@1.1.4?
- This will create an annotated tag on current HEAD
- Tag will be pushed to remote origin
- Tag cannot be easily modified once pushed

[Yes, create tag] [No, cancel] [Customize message]
```

### 4. Execute Commands (after user confirms)

```bash
# Create annotated tag
git tag -a "marketplace@1.1.4" -m "Release marketplace 1.1.4"

# Verify tag created
git show marketplace@1.1.4 --quiet

# Push to remote
git push origin marketplace@1.1.4
```

### 5. Verify and Report Results

```bash
# Check tag exists locally
git tag -l "marketplace@1.1.4"

# Check tag pushed to remote
git ls-remote --tags origin | grep marketplace@1.1.4

# Show tag details
git show marketplace@1.1.4
```

### 6. Present Success Confirmation

```
✅ Tag created successfully!

Tag: marketplace@1.1.4
Commit: abc123de (current HEAD)
Pushed to: origin
Tagger: Connor <connor@example.com>
Date: 2025-11-16 10:51:00

View on GitHub:
https://github.com/user/repo/releases/tag/marketplace@1.1.4

Next steps:
- Create GitHub release? [Yes/No]
- Tag another component? [Yes/No]
```

## Output

Git tag created, pushed to remote, and verified.

## Automation Features

- ✅ **Auto-generates tag message** from component name and version
- ✅ **Pre-flight checks**: Verifies tag doesn't already exist
- ✅ **Atomic execution**: Tag creation + push in sequence
- ✅ **Error handling**: Rolls back local tag if push fails
- ✅ **Verification**: Confirms tag exists both locally and remotely

## Common Issues

- **Tag already exists**: Check before creation, prompt to overwrite or choose new version
- **Push fails**: Keep local tag, warn user, offer retry
- **Wrong commit**: Ask user to confirm current HEAD before tagging
