---
description: Update installed rules from upstream plugin source
---

You are the swe-standards sync command. Update the user's installed rules to match the latest upstream plugin source.

## Context

Rules are installed at `~/.claude/rules/swe-standards/` and tracked via a manifest at `~/.claude/swe-standards.json`. The upstream source rules live at `${CLAUDE_PLUGIN_ROOT}/rules/`.

## Execution Steps

### Step 1: Read Manifest

Read `~/.claude/swe-standards.json`. If it doesn't exist, tell the user to run `/swe-standards:init` first and stop.

### Step 2: Compare Files

For each file in the manifest:

1. Read the installed file at `~/.claude/rules/swe-standards/<filename>`
2. Compute its current MD5 hash: `md5 -q <file>` (macOS) or `md5sum <file>` (Linux)
3. Compare against the manifest's stored hash to detect local modifications
4. Read the upstream source file at `${CLAUDE_PLUGIN_ROOT}/rules/<source-path>`
5. Compare upstream content against installed content

Categorize each file:
- **Up to date**: Installed matches upstream, hash matches manifest → no action
- **Upstream changed**: Installed matches manifest hash (no local edits), but upstream differs → safe to update
- **Locally modified**: Installed hash differs from manifest (user edited it) → needs conflict resolution
- **Both changed**: Local edits AND upstream changes → needs conflict resolution
- **Missing**: In manifest but not on disk → needs reinstall

### Step 3: Apply Updates

For each category:

**Up to date**: Skip, report as current.

**Upstream changed** (no local edits): Overwrite silently. Update manifest hash.

**Locally modified** (no upstream changes): Keep as-is. Report as locally modified.

**Both changed**: Show the user a summary of differences and ask:
- **Keep mine** — preserve local version, update manifest hash to match local
- **Take upstream** — overwrite with upstream, update manifest hash
- **Skip** — do nothing, revisit later

**Missing**: Copy from upstream source, update manifest hash.

### Step 4: Check for New Rules

If the user's installed profiles include rules that weren't in their original manifest (new rules added to a profile since they last synced), offer to install them.

### Step 5: Update Manifest

Update `~/.claude/swe-standards.json`:
- Set `updated_at` to current ISO timestamp
- Update file hashes for any changed files
- Add entries for any new files installed

### Step 6: Report Summary

Show:
- Files updated (count)
- Files skipped (locally modified, count)
- Files with conflicts resolved (count)
- New files added (count)
- Suggest restarting Claude Code session if any rules changed
