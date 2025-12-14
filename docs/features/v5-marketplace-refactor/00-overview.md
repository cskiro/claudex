# v5.0.0 Marketplace Refactor - Overview

## Goal

Restore archived skills from v4.0.0, creating a comprehensive 23-skill marketplace, then analyze overlaps and reorganize for optimal structure.

## Problem Statement

v4.0.0 archived 7 skills and removed 4 plugins, causing plugin errors for users with existing installations:
- `analysis-tools@claudex` - Plugin not found
- `productivity-tools@claudex` - Plugin not found
- `release-management@claudex` - Plugin not found
- `planning-tools@claudex` - Plugin not found
- `benchmarking@claudex` - Plugin not found

## Solution

1. Restore all archived skills to the flat `skills/` directory (v4.0.0 structure)
2. Re-add removed plugin definitions to `marketplace.json`
3. Analyze skill overlaps and reorganization opportunities
4. Release as v5.0.0 with comprehensive documentation

## Success Criteria

- [ ] All 23 skills accessible via marketplace
- [ ] All 10 plugins install without errors
- [ ] Validation scripts pass
- [ ] No regression in existing v4.0.0 functionality

## Timeline

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Documentation Setup | In Progress |
| 1 | Restore Archived Skills | Pending |
| 2 | Validate & Test | Pending |
| 3 | Overlap Analysis | Pending |
| 4 | Reorganization | Pending |
| 5 | Release | Pending |

## References

- [Plan File](/Users/connor/.claude/plans/quiet-frolicking-cocoa.md)
- [v4.0.0 Commit](https://github.com/cskiro/claudex/commit/5e5c7fed2d4b4f31c67906724ad1b3c01d064fc4)
