# Changelog

All notable changes to the ASCII Diagram Creator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2025-11-23

### Added

- **Mandatory Completion Checklist**: Template that must be output before skill is complete
- **CRITICAL markers**: Phase 4 marked as MANDATORY in workflow table
- **Explicit Phase 4 enforcement**: Execution pattern now lists all required Phase 4 steps

### Changed

- Execution pattern step 6 now explicitly lists all Phase 4 integration options
- Workflow table highlights Phase 4 as mandatory with warning callout
- Added "skill is NOT complete until" enforcement language

### Fixed

- Prevents LLM from skipping Phase 4 (Output & Integration) steps
- Ensures CLAUDE.md directive setup is always offered

## [0.3.0] - 2025-11-23

### Added

- **Mermaid Export**: Convert ASCII diagrams to Mermaid syntax for graphical rendering in GitHub, GitLab, Notion
- **Git-Aware Staleness Detection**: Automatically detect outdated diagrams based on git history and source file changes
- **PR Template Integration**: Auto-suggest diagram inclusion in PR descriptions and update PR templates
- **CLAUDE.md Directive Setup**: Interactive step to configure proactive diagram suggestions in user's CLAUDE.md
- **Phase 4 (Output & Integration)**: New workflow phase covering all output formats and integration options
- **Mermaid Export Reference Guide**: Comprehensive guide for ASCII-to-Mermaid conversion rules and examples

### Changed

- Workflow now includes 5 phases (added Output & Integration)
- Key capabilities expanded from 8 to 12 features
- Removed "Future Enhancements" section (all features now implemented)

### Documentation

- Added Version History section to README
- Updated all feature descriptions with version tags (v0.3.0)
- Added conversion examples and platform support matrix for Mermaid export

## [0.2.0] - 2025-11-23

### Added

- **Codebase Auto-Discovery Mode**: Automatically scan project structure, detect architecture patterns, and populate diagrams (reduces 50% manual exploration)
- **Project-Type Templates**: Pre-built templates for Bulletproof React, Next.js App Router, Express API, and Monorepo architectures
- **Diagram Versioning Metadata**: Track diagram freshness with `created`, `last-verified`, `source-patterns`, and `stale-after` fields
- **Workflow Automation Examples**: Hook-based auto-triggers, CLAUDE.md directives, and sub-agent integration patterns
- **Fifth Diagram Type**: Relationship/Synergy diagrams for showing how elements interact or complement each other
- **Project-Type Templates Reference**: New reference file with complete templates for each architecture type

### Changed

- Enhanced Phase 0 (Context Analysis) with auto-discovery commands
- Updated Quick Reference to include all five diagram types
- Improved key capabilities list in SKILL.md overview

### Documentation

- Added Workflow Automation section to README with three integration options
- Expanded feature documentation with version tags (v0.2.0)

## [0.1.0] - 2025-01-23

### Added

- Initial skill release
- Four diagram types: Architecture, Before/After, Phased Migration, Data Flow
- Visual elements: box-drawing characters, arrows, status indicators
- Phase-based workflow (context analysis, selection, generation, refinement)
- Reference materials for visual elements, best practices, and templates
- Example diagrams for each diagram type
- 80-character max width formatting for terminal compatibility
