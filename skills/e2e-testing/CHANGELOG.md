# Changelog

## 0.4.1

- Relocated to `plugins/testing-tools/skills/` for source isolation (marketplace v4.0.0)
- Prevents cache duplication in Claude Code plugin system

## 0.4.0

- Renamed from `playwright-e2e-automation` to `e2e-testing` (purpose-based naming)
- Aligned with Anthropic skill naming conventions
- Updated description for broader semantic matching

## 0.3.0

- Refactored to Anthropic progressive disclosure pattern
- Updated description with "Use PROACTIVELY when..." format
- Removed version/author/category/tags from frontmatter

## 0.2.0

- Added framework version detection (Tailwind v3/v4, React 17-19, Next.js 13-14)
- Added pre-flight health check (Phase 2.5)
- Added error pattern recovery database
- Fixed Tailwind CSS v4 compatibility

## 0.1.0

- Initial release with zero-setup Playwright automation
- Multi-framework support: React/Vite, Next.js, Node.js, static
- LLM-powered visual analysis for UI bug detection
- Visual regression testing with baseline comparison
- Fix recommendations with file:line references
