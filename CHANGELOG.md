# Changelog

All notable changes to the Claudex marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.1] - 2025-11-23

### Added
- Troubleshooting section in README for `productivity-tools` → `claude-code-tools` migration
- CHANGELOG.md with full marketplace version history

## [1.3.0] - 2025-11-23

### Changed
- Optimized skill context loading with 70% reduction in token usage
- Skills now use lean SKILL.md manifests with progressive disclosure pattern

## [1.2.0] - 2025-11-16

### Added
- **Release Management** category with `semantic-release-tagger` skill
- Automated versioning workflow following repository conventions

## [1.1.3] - 2025-11-15

### Changed
- **BREAKING**: Renamed `productivity-tools` plugin to `claude-code-tools`
- Aligned marketplace schema with Anthropic plugin standards

### Migration Required
Users with `productivity-tools@claudex` in their settings must update to `claude-code-tools@claudex`:

```json
// Before
"enabledPlugins": {
  "productivity-tools@claudex": true
}

// After
"enabledPlugins": {
  "claude-code-tools@claudex": true
}
```

See [README Troubleshooting](README.md#troubleshooting) for detailed instructions.

## [1.1.2] - 2025-11-14

### Fixed
- Added required nested hooks array in hooks.json schema

## [1.1.1] - 2025-11-14

### Fixed
- Corrected hooks.json schema structure
- Fixed marketplace skill paths

## [1.1.0] - 2025-11-14

### Added
- **API Tools** category with 3 skills:
  - `structured-outputs-advisor` - Expert guidance for Anthropic's structured outputs
  - `json-outputs-implementer` - JSON schema implementation
  - `strict-tool-implementer` - Strict tool use patterns

## [1.0.0] - 2025-11-14

### Added
- Initial marketplace release with 8 plugin categories
- 18 skills across analysis, testing, devops, claude-code, and meta categories
- `extract-explanatory-insights` hook for automatic insight capture
- Lessons-learned documentation system

### Categories
- **Analysis Tools**: `codebase-auditor`, `bulletproof-react-auditor`
- **Testing Tools**: `playwright-e2e-automation`, `tdd-automation`
- **DevOps Tools**: `react-project-scaffolder`, `github-repo-setup`, `git-worktree-setup`
- **Claude Code Tools**: `cc-insights`, `sub-agent-creator`, `mcp-server-creator`, `claude-md-auditor`, `otel-monitoring-setup`
- **Meta Tools**: `skill-creator`, `skill-isolation-tester`

[Unreleased]: https://github.com/cskiro/claudex/compare/marketplace@1.3.1...HEAD
[1.3.1]: https://github.com/cskiro/claudex/compare/marketplace@1.3.0...marketplace@1.3.1
[1.3.0]: https://github.com/cskiro/claudex/compare/marketplace@1.2.0...marketplace@1.3.0
[1.2.0]: https://github.com/cskiro/claudex/compare/marketplace@1.1.3...marketplace@1.2.0
[1.1.3]: https://github.com/cskiro/claudex/compare/marketplace@1.1.2...marketplace@1.1.3
[1.1.2]: https://github.com/cskiro/claudex/compare/marketplace@1.1.1...marketplace@1.1.2
[1.1.1]: https://github.com/cskiro/claudex/compare/marketplace@1.1.0...marketplace@1.1.1
[1.1.0]: https://github.com/cskiro/claudex/compare/marketplace@1.0.0...marketplace@1.1.0
[1.0.0]: https://github.com/cskiro/claudex/releases/tag/marketplace@1.0.0
