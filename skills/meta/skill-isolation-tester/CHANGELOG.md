# Changelog

All notable changes to the Skill Isolation Tester skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- CI/CD integration examples
- Support for Podman as Docker alternative
- Parallel testing across multiple environments
- Custom test scenario definitions
- Integration with skill-creator for automatic testing
- Performance benchmarking mode
- Network isolation testing
- Multi-OS testing (Ubuntu, Debian, Fedora)

## [0.1.0] - 2025-11-01

### Added
- Initial release of Skill Isolation Tester
- Three isolation modes: Git Worktree, Docker, VM
- Automatic risk assessment and mode detection
- Comprehensive side-effect validation
- Dependency analysis and detection
- Detailed test report generation
- Support for git worktrees (fast iteration)
- Docker container isolation (balanced approach)
- VM isolation via Multipass/UTM/VirtualBox (maximum security)
- Before/after snapshot comparison
- Process and filesystem monitoring
- Hardcoded path detection
- Cleanup verification
- Mode-specific documentation
- Risk assessment guidelines
- Side-effect checklist
- Test report templates
- Example test results

### Features
- **Git Worktree Mode**: Lightweight isolation for quick testing
- **Docker Mode**: Full OS isolation with reproducible environments
- **VM Mode**: Complete isolation for high-risk skills
- **Auto-detection**: Analyzes skill and suggests appropriate mode
- **Comprehensive Reports**: Detailed findings with actionable recommendations
- **Multiple Platforms**: macOS, Linux support (Windows via VM mode)

### Documentation
- Complete SKILL.md with mode detection logic
- Detailed mode-specific workflows
- Quick start guide and examples
- Troubleshooting section
- Best practices guide
- Architecture overview

### Known Limitations
- Docker mode requires Docker daemon running
- VM mode is resource-intensive (8GB+ RAM recommended)
- Git worktree mode has limited isolation (shares system packages)
- Manual intervention required for interactive skills
- No automated fix application (reports only)

## [0.0.1] - 2025-11-01

### Added
- Initial project structure
- Basic documentation skeleton

---

## Version History Legend

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

## Upgrade Guide

### From 0.0.x to 0.1.0

This is the first stable release. No upgrade needed.

## Support

For issues, questions, or contributions:
- Review documentation in modes/ directory
- Check examples/ for sample outputs
- Refer to troubleshooting section in README.md

---

**Note**: This skill is in active development. Expect breaking changes in 0.x versions. Stable API guaranteed from 1.0.0 onwards.
