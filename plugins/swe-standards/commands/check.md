---
description: Verify installation health and compliance status
---

You are the swe-standards check command. Verify the health of the user's swe-standards installation.

## Context

Rules are installed at `~/.claude/rules/swe-standards/` and tracked via a manifest at `~/.claude/swe-standards.json`. The upstream source rules live at `${CLAUDE_PLUGIN_ROOT}/rules/`.

## Execution Steps

### Step 1: Check Installation Exists

1. Check if `~/.claude/rules/swe-standards/` directory exists
2. Check if `~/.claude/swe-standards.json` manifest exists

If neither exists, report that swe-standards is not installed and suggest running `/swe-standards:init`.

If directory exists but manifest doesn't (or vice versa), report the inconsistency.

### Step 2: Read Manifest

Parse `~/.claude/swe-standards.json` and extract:
- Version
- Installation date
- Last sync date
- Active profiles
- Expected files and their hashes

### Step 3: Verify Files

For each file in the manifest:

1. Check if the file exists at `~/.claude/rules/swe-standards/<filename>`
2. If it exists, compute MD5 hash and compare against manifest
3. Categorize as: Present (matching) | Modified (hash differs) | Missing

### Step 4: Check for Orphan Files

List all `.md` files in `~/.claude/rules/swe-standards/` and identify any files NOT in the manifest. These are either:
- Manually added rules (fine, report as custom)
- Leftover from a previous profile (suggest cleanup)

### Step 5: Check Dependencies

Check if required external plugins are installed:

1. **pr-review-toolkit** (required for Quality profile):
   - Check if the plugin is installed by running: look for `pr-review-toolkit` in the user's installed plugins
   - If not installed, report as missing and suggest: `Install pr-review-toolkit from Anthropic's plugin marketplace to enable Quality profile agents`
   - This is an external Anthropic plugin, not part of the claudex marketplace

2. **adr-generator** (recommended, in claudex marketplace):
   - Check if installed by looking for its directory
   - If not installed, suggest: `/plugin install adr-generator@claudex`

Report installation status for each.

### Step 6: Report Health Summary

Display a status report:

```
SWE Standards Health Check
========================

Installation: ✅ Installed
Version:      0.1.0
Installed:    2025-01-15T10:30:00Z
Last Sync:    2025-01-20T14:00:00Z

Active Profiles: Core, TypeScript, Testing, Quality

Rules Status:
  ✅ Present (matching):  10
  ⚠️  Modified locally:    2
  ❌ Missing:              0
  📄 Custom (not managed): 1

Dependencies:
  ✅ pr-review-toolkit: installed (external — Anthropic marketplace)
  ⚠️  adr-generator: not installed (run: /plugin install adr-generator@claudex)

Overall: ✅ Healthy (2 locally modified rules)
```

Use appropriate status indicators:
- All files present and matching → "Healthy"
- Some files modified → "Healthy (N locally modified rules)"
- Any files missing → "Needs attention (N missing rules)"
- No installation found → "Not installed"
