# Changelog

All notable changes to the insight-skill-generator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-12-14

### Changed
- Restored from archive to active marketplace (v5.0.0)
- Moved from `archive/skills/` to flat `skills/` directory
- Added to meta-tools plugin

## [0.1.0] - 2025-11-16

### Added

- **Phase 1: Insight Discovery and Parsing**
  - Automatic discovery of insights in `docs/lessons-learned/` directory
  - Parse insight files with session metadata extraction
  - Build structured inventory with keywords and categorization
  - Support for multiple insight categories (testing, architecture, hooks-and-events, etc.)

- **Phase 2: Smart Clustering**
  - Keyword-based similarity analysis
  - Multi-factor scoring (category, keywords, temporal proximity, content overlap)
  - Automatic cluster formation with configurable thresholds
  - Standalone high-quality insight detection
  - Sub-clustering for large insight groups
  - Interactive cluster review and customization

- **Phase 3: Interactive Skill Design**
  - Intelligent skill naming from insight keywords
  - Auto-generated descriptions with trigger phrases
  - Complexity assessment (minimal/standard/complex)
  - Pattern selection (phase-based/mode-based/validation/data-processing)
  - Content-to-structure mapping
  - Workflow/phase definition
  - Preview and customization before generation

- **Phase 4: Skill Generation**
  - Complete SKILL.md generation with proper frontmatter
  - README.md with usage examples
  - plugin.json with marketplace metadata
  - CHANGELOG.md initialization
  - data/insights-reference.md with original insights
  - examples/ directory with code samples
  - templates/ directory with actionable checklists
  - Comprehensive validation against Anthropic standards

- **Phase 5: Installation and Testing**
  - Flexible installation (project-specific or global)
  - Conflict detection and resolution
  - Post-installation validation
  - Skill loading verification
  - Testing guidance with trigger phrases
  - Refinement suggestions

- **Configuration System**
  - `data/clustering-config.yaml` - Tunable similarity rules and thresholds
  - `data/skill-templates-map.yaml` - Insight-to-pattern mappings
  - `data/quality-checklist.md` - Validation criteria

- **Template System**
  - `templates/insight-based-skill.md.j2` - SKILL.md structure reference
  - `templates/insight-reference.md.j2` - Insights consolidation pattern
  - `templates/insight-checklist.md.j2` - Actionable checklist pattern

- **Documentation**
  - Comprehensive SKILL.md with 5-phase workflow
  - User-friendly README.md with quick start guide
  - Troubleshooting section for common issues
  - Example outputs and generated skills

### Features

- **Smart Clustering**: Analyzes insights using keyword similarity, category matching, and temporal proximity
- **Hybrid Approach**: Generates standalone skills from single insights or comprehensive skills from clusters
- **Interactive Guided**: User reviews and customizes every design decision
- **Quality Validation**: Ensures generated skills meet Anthropic standards
- **Pattern Recognition**: Automatically selects appropriate skill pattern based on insight content
- **Deduplication**: Prevents creating skills that duplicate existing functionality

### Integration

- Integrates with `extract-explanatory-insights` hook
- Reads from `docs/lessons-learned/` directory structure
- Supports all insight categories from the hook (testing, configuration, hooks-and-events, security, performance, architecture, version-control, react, typescript, general)

### Supported Patterns

- **Phase-based**: Linear workflows with sequential steps
- **Mode-based**: Multiple distinct approaches for same domain
- **Validation**: Analysis and checking patterns
- **Data-processing**: Transform or analyze data patterns

### Complexity Levels

- **Minimal**: Single insight, basic structure (SKILL.md, README, plugin.json, CHANGELOG)
- **Standard**: 2-4 insights with reference materials and examples
- **Complex**: 5+ insights with comprehensive templates and multiple examples

### Known Limitations

- Requires `docs/lessons-learned/` directory structure from extract-explanatory-insights hook
- Clustering algorithm is keyword-based (not ML-powered)
- Templates use Jinja2 syntax for documentation reference only (not programmatically rendered)
- First release - patterns and thresholds may need tuning based on usage

### Notes

- Generated from research on extract-explanatory-insights hook
- Based on Anthropic's official skill creation patterns
- Follows skill-creator's guided creation approach
- Initial thresholds (cluster_minimum: 0.6, standalone_quality: 0.8) are starting points and may need adjustment

---

## Future Enhancements (Planned)

- Auto-detection of existing skill overlap to prevent duplication
- ML-based clustering for better semantic grouping
- Skill versioning support (updating existing skills with new insights)
- Team collaboration features (merging insights from multiple developers)
- Export skills to Claudex marketplace format
- Integration with cc-insights skill for enhanced pattern detection
- Batch generation mode for processing multiple projects
- Custom template support for organization-specific skill patterns
