# Changelog

All notable changes to the benchmark-report-creator skill.

## [0.1.2] - 2025-12-14

### Changed
- Restored from archive to active marketplace (v5.0.0)
- Moved from `archive/skills/` to flat `skills/` directory

## [0.1.1] - 2025-12-05

### Changed
- Updated description to PROACTIVE format for improved skill triggering
- Clarified use cases (research reports, whitepapers) and scope limitations

## [0.1.0] - 2024-11-30

### Added
- Initial release as unified orchestrator skill
- SKILL.md with complete pipeline documentation
- `scripts/capture-diagram.js` - Working high-res PNG capture (2x deviceScaleFactor)
- `templates/pdf-style.css` - Academic CSS from empathy v1.0/v2.0
- `reference/report-template.md` - Full academic report structure
- `reference/html-templates.md` - Copy-paste diagram templates
- `reference/command-reference.md` - Complete command sequences

### Changed
- Consolidates 4 previous skills into single orchestrator:
  - `report-creator` (structure)
  - `html-diagram-creator` (diagrams)
  - `html-to-png-converter` (capture)
  - `markdown-to-pdf-converter` (export)

### Fixed
- High-res PNG capture - Playwright CLI lacks `--device-scale-factor`, now uses Node.js API
- CSS template completeness - Full empathy v1.0/v2.0 styling included

### Notes
- Previous 4 skills removed from marketplace (replaced by this orchestrator)
- Users with component skills in `~/.claude/skills/` can still use them directly
