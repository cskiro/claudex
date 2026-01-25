# Mode-Based Skill Pattern

Use this pattern when your skill has **multiple distinct operating modes** based on user intent.

## When to Use

- Skill performs fundamentally different operations based on context
- Each mode has its own workflow and outputs
- User intent determines which mode to activate
- Examples: git-worktree-setup (single/batch/cleanup/list modes)

## Structure

### Quick Decision Matrix

Create a clear mapping of user requests to modes:

```
User Request                → Mode          → Action
───────────────────────────────────────────────────────────
"trigger phrase 1"          → Mode 1        → High-level action
"trigger phrase 2"          → Mode 2        → High-level action
"trigger phrase 3"          → Mode 3        → High-level action
```

### Mode Detection Logic

Provide clear logic for mode selection:

```javascript
// Mode 1: [Name]
if (userMentions("keyword1", "keyword2")) {
  return "mode1-name";
}

// Mode 2: [Name]
if (userMentions("keyword3", "keyword4")) {
  return "mode2-name";
}

// Ambiguous - ask user
return askForClarification();
```

### Separate Mode Documentation

For complex skills, create separate files for each mode:

```
skill-name/
├── SKILL.md                 # Overview and mode detection
├── modes/
│   ├── mode1-name.md       # Detailed workflow for mode 1
│   ├── mode2-name.md       # Detailed workflow for mode 2
│   └── mode3-name.md       # Detailed workflow for mode 3
```

## Example: Git Worktree Setup

**Modes:**
1. Single Worktree - Create one worktree
2. Batch Worktrees - Create multiple worktrees
3. Cleanup - Remove worktrees
4. List/Manage - Show worktree status

**Detection Logic:**
- "create worktree for X" → Single mode
- "create worktrees for A, B, C" → Batch mode
- "remove worktree" → Cleanup mode
- "list worktrees" → List mode

## Best Practices

1. **Clear Mode Boundaries**: Each mode should be distinct and non-overlapping
2. **Explicit Detection**: Provide clear rules for mode selection
3. **Clarification Path**: Always have a fallback to ask user when ambiguous
4. **Mode Independence**: Each mode should work standalone
5. **Shared Prerequisites**: Extract common validation to reduce duplication
