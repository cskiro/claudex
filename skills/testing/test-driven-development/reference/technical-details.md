# Technical Reference

## Files Modified/Created

### Modified Files
- `.claude/CLAUDE.md` - Test workflow configuration added (backed up)
- `package.json` - npm scripts added (backed up)
- `.git/hooks/pre-commit` - Test validation added (backed up if exists)

### Created Files
```
.tdd-automation/
├── scripts/
│   ├── generate-test.js       # Test template generator
│   ├── validate-tdd.js        # Compliance checker
│   ├── rollback-tdd.js        # Restore previous state
│   └── remove-tdd-section.js  # Clean uninstall
├── templates/
│   └── test-template.js       # Test file template
└── README.md                  # Usage documentation

.claude/
├── CLAUDE.md.backup.*         # Timestamped backups
└── hooks/
    └── tdd-auto-enforcer.sh   # Pre-prompt hook (optional)
```

## Safety Features

### Non-Destructive Installation
- Automatic backups before file modifications
- Merge strategy preserves all existing CLAUDE.md content
- Clear markers (`<!-- TDD_AUTOMATION_START/END -->`) for identification
- Rollback capability to restore previous state

### Validation Before Installation
- Detects if test workflow already installed (skips if present)
- Checks for existing CLAUDE.md (merges safely)
- Validates project structure
- Reports warnings for missing dependencies

### Clean Uninstallation
- Remove only test workflow section without affecting other content
- Restore from timestamped backups
- Utility scripts for easy maintenance

## Troubleshooting

### Issue: LLM not following test workflow

**Check:**
```bash
# Verify CLAUDE.md has configuration
grep "TDD_AUTOMATION" .claude/CLAUDE.md

# Verify npm scripts
npm run test:tdd

# Run validation
npm run validate:tdd
```

### Issue: Git hook blocking commits

**Solution:**
1. Ensure tests exist for implementation files
2. Commit tests before implementation
3. Or bypass temporarily: `git commit --no-verify`

### Issue: Want to remove test workflow

**Options:**
```bash
# Option 1: Remove CLAUDE.md section only
node .tdd-automation/scripts/remove-tdd-section.js

# Option 2: Rollback to previous CLAUDE.md
node .tdd-automation/scripts/rollback-tdd.js
```

## Response Style

After installation, this skill guides Claude Code to:

- **Be explicit**: Always state which test phase is active
- **Be thorough**: Verify each phase completion before proceeding
- **Be traceable**: Use TodoWrite to track progress
- **Be safe**: Run tests to confirm RED/GREEN states
- **Be helpful**: Provide clear error messages if workflow is violated
