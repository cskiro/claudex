#!/usr/bin/env python3
"""
Pre-Release Validation Suite for Claudex Marketplace

Comprehensive validation before releasing a new marketplace version.
Runs all automated checks and provides a checklist for manual validation.

Usage:
    python3 scripts/pre-release-check.py           # Full validation
    python3 scripts/pre-release-check.py --quick   # Quick validation (skip slow checks)
    python3 scripts/pre-release-check.py --verbose # Detailed output

Exit Codes:
    0 - All automated checks passed
    1 - Validation errors found
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


class PreReleaseValidator:
    """Comprehensive pre-release validation suite."""

    def __init__(self, repo_root: Path, quick: bool = False, verbose: bool = False):
        self.repo_root = repo_root
        self.quick = quick
        self.verbose = verbose
        self.marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
        self.marketplace = {}
        self.results: Dict[str, Tuple[bool, str]] = {}
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def run(self) -> bool:
        """Run all validation checks."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}║        CLAUDEX PRE-RELEASE VALIDATION SUITE                  ║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
        print(f"\n{Colors.DIM}Timestamp: {datetime.now().isoformat()}{Colors.RESET}")
        print(f"{Colors.DIM}Mode: {'Quick' if self.quick else 'Full'}{Colors.RESET}\n")

        # Load marketplace.json
        if not self._load_marketplace():
            return False

        # Run automated checks
        checks = [
            ("1. Marketplace Schema", self._check_marketplace_schema),
            ("2. Skill Paths Exist", self._check_skill_paths),
            ("3. SKILL.md Frontmatter", self._check_skill_frontmatter),
            ("4. Name-Directory Match", self._check_name_directory_match),
            ("5. No Duplicate Skills", self._check_no_duplicate_skills),
            ("6. Version Consistency", self._check_version_consistency),
            ("7. Required Files", self._check_required_files),
            ("8. No Plugin.json Files", self._check_no_plugin_json),
            ("9. Description Quality", self._check_description_quality),
            ("10. Anthropic Pattern Alignment", self._check_anthropic_alignment),
        ]

        if not self.quick:
            checks.extend([
                ("11. Internal Link Validation", self._check_internal_links),
                ("12. Script Permissions", self._check_script_permissions),
                ("13. Changelog Entries", self._check_changelog_entries),
            ])

        print(f"{Colors.BOLD}═══ AUTOMATED CHECKS ═══{Colors.RESET}\n")

        all_passed = True
        for name, check_func in checks:
            try:
                passed, message = check_func()
                self.results[name] = (passed, message)

                status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
                print(f"  {status}  {name}")

                if not passed:
                    all_passed = False
                    print(f"         {Colors.RED}{message}{Colors.RESET}")
                elif self.verbose and message:
                    print(f"         {Colors.DIM}{message}{Colors.RESET}")

            except Exception as e:
                self.results[name] = (False, str(e))
                print(f"  {Colors.RED}✗ ERROR{Colors.RESET}  {name}")
                print(f"         {Colors.RED}{e}{Colors.RESET}")
                all_passed = False

        # Run existing validation scripts
        print(f"\n{Colors.BOLD}═══ VALIDATION SCRIPTS ═══{Colors.RESET}\n")

        script_results = self._run_validation_scripts()
        all_passed = all_passed and script_results

        # Print summary
        self._print_summary(all_passed)

        # Print manual checklist
        self._print_manual_checklist()

        return all_passed

    def _load_marketplace(self) -> bool:
        """Load marketplace.json."""
        try:
            with open(self.marketplace_path, 'r') as f:
                self.marketplace = json.load(f)
            return True
        except Exception as e:
            print(f"{Colors.RED}Failed to load marketplace.json: {e}{Colors.RESET}")
            return False

    def _check_marketplace_schema(self) -> Tuple[bool, str]:
        """Check marketplace.json has required fields."""
        required = ['name', 'owner', 'metadata', 'plugins']
        missing = [f for f in required if f not in self.marketplace]

        if missing:
            return (False, f"Missing required fields: {', '.join(missing)}")

        version = self.marketplace.get('metadata', {}).get('version', 'unknown')
        return (True, f"Version {version}")

    def _check_skill_paths(self) -> Tuple[bool, str]:
        """Check all skill paths in marketplace.json exist."""
        missing = []
        total = 0

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                total += 1
                path = skill_path.lstrip('./')
                full_path = self.repo_root / path

                if not full_path.exists():
                    missing.append(skill_path)

        if missing:
            return (False, f"Missing: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}")

        return (True, f"All {total} skill paths exist")

    def _check_skill_frontmatter(self) -> Tuple[bool, str]:
        """Check all SKILL.md files have valid frontmatter."""
        issues = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                skill_md = self.repo_root / path / "SKILL.md"

                if not skill_md.exists():
                    continue

                content = skill_md.read_text()

                if not content.startswith('---'):
                    issues.append(f"{Path(path).name}: Missing frontmatter")
                    continue

                # Check for name and description
                if 'name:' not in content[:500]:
                    issues.append(f"{Path(path).name}: Missing name in frontmatter")
                if 'description:' not in content[:1000]:
                    issues.append(f"{Path(path).name}: Missing description in frontmatter")

        if issues:
            return (False, f"{len(issues)} issues: {issues[0]}")

        return (True, "All frontmatter valid")

    def _check_name_directory_match(self) -> Tuple[bool, str]:
        """Check skill names match directory names (Anthropic spec requirement)."""
        mismatches = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                dir_name = Path(path).name
                skill_md = self.repo_root / path / "SKILL.md"

                if not skill_md.exists():
                    continue

                content = skill_md.read_text()

                # Extract name from frontmatter
                name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
                if name_match:
                    skill_name = name_match.group(1).strip().strip('"\'')
                    if skill_name != dir_name:
                        mismatches.append(f"{dir_name} (frontmatter: {skill_name})")

        if mismatches:
            return (False, f"Mismatches: {', '.join(mismatches[:3])}")

        return (True, "All names match directories")

    def _check_no_duplicate_skills(self) -> Tuple[bool, str]:
        """Check no skill appears in multiple plugins."""
        seen: Dict[str, str] = {}
        duplicates = []

        for plugin in self.marketplace.get('plugins', []):
            plugin_name = plugin.get('name', 'unknown')
            for skill_path in plugin.get('skills', []):
                if skill_path in seen:
                    duplicates.append(f"{skill_path} (in {seen[skill_path]} and {plugin_name})")
                seen[skill_path] = plugin_name

        if duplicates:
            return (False, f"Duplicates: {duplicates[0]}")

        return (True, f"{len(seen)} unique skills")

    def _check_version_consistency(self) -> Tuple[bool, str]:
        """Check version follows semver and is updated."""
        version = self.marketplace.get('metadata', {}).get('version', '')

        if not version:
            return (False, "No version in metadata")

        # Check semver format
        if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$', version):
            return (False, f"Invalid semver: {version}")

        return (True, f"Version {version} is valid semver")

    def _check_required_files(self) -> Tuple[bool, str]:
        """Check all skills have required files."""
        required_files = ['SKILL.md', 'README.md', 'CHANGELOG.md']
        missing = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                skill_dir = self.repo_root / path

                for req_file in required_files:
                    if not (skill_dir / req_file).exists():
                        missing.append(f"{Path(path).name}/{req_file}")

        if missing:
            return (False, f"Missing: {missing[0]} (+{len(missing)-1} more)" if len(missing) > 1 else f"Missing: {missing[0]}")

        return (True, "All required files present")

    def _check_no_plugin_json(self) -> Tuple[bool, str]:
        """Check no skill has plugin.json (Anthropic pattern)."""
        found = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                plugin_json = self.repo_root / path / "plugin.json"

                if plugin_json.exists():
                    found.append(Path(path).name)

        if found:
            return (False, f"Found in: {', '.join(found[:3])}")

        return (True, "No plugin.json files (correct)")

    def _check_description_quality(self) -> Tuple[bool, str]:
        """Check descriptions meet quality standards."""
        issues = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                skill_md = self.repo_root / path / "SKILL.md"

                if not skill_md.exists():
                    continue

                content = skill_md.read_text()

                # Extract description
                desc_match = re.search(r'description:\s*>-?\s*\n((?:\s+.+\n?)+)', content)
                if not desc_match:
                    desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)

                if desc_match:
                    desc = desc_match.group(1).strip()

                    # Check length
                    if len(desc) > 1024:
                        issues.append(f"{Path(path).name}: Description > 1024 chars")
                    elif len(desc) < 50:
                        issues.append(f"{Path(path).name}: Description < 50 chars")

        if issues:
            return (False, issues[0])

        return (True, "All descriptions within limits")

    def _check_anthropic_alignment(self) -> Tuple[bool, str]:
        """Check alignment with Anthropic's official patterns."""
        issues = []

        # Check all plugins use root source
        for plugin in self.marketplace.get('plugins', []):
            source = plugin.get('source', '')
            if source not in ['./', '.', '']:
                issues.append(f"Plugin {plugin.get('name')}: Non-standard source '{source}'")

        # Check flat skill structure
        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                parts = Path(path).parts

                # Should be skills/<skill-name>, not skills/<category>/<skill-name>
                if len(parts) > 2:
                    issues.append(f"Nested structure: {skill_path}")

        if issues:
            return (False, issues[0])

        return (True, "Follows Anthropic patterns")

    def _check_internal_links(self) -> Tuple[bool, str]:
        """Check internal markdown links resolve."""
        broken = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                skill_dir = self.repo_root / path

                for md_file in skill_dir.rglob('*.md'):
                    content = md_file.read_text()

                    # Find markdown links
                    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

                    for text, link in links:
                        # Skip external URLs and anchors
                        if link.startswith('http') or link.startswith('#'):
                            continue

                        # Resolve relative path
                        target = md_file.parent / link
                        if not target.exists():
                            broken.append(f"{md_file.name}: {link}")

        if broken:
            return (False, f"{len(broken)} broken links")

        return (True, "All internal links valid")

    def _check_script_permissions(self) -> Tuple[bool, str]:
        """Check shell scripts have execute permissions."""
        issues = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                scripts_dir = self.repo_root / path / "scripts"

                if not scripts_dir.exists():
                    continue

                for script in scripts_dir.glob('**/*.sh'):
                    if not os.access(script, os.X_OK):
                        issues.append(script.name)

        if issues:
            return (False, f"Missing +x: {', '.join(issues[:3])}")

        return (True, "All scripts executable")

    def _check_changelog_entries(self) -> Tuple[bool, str]:
        """Check CHANGELOGs have entries."""
        empty = []

        for plugin in self.marketplace.get('plugins', []):
            for skill_path in plugin.get('skills', []):
                path = skill_path.lstrip('./')
                changelog = self.repo_root / path / "CHANGELOG.md"

                if changelog.exists():
                    content = changelog.read_text()
                    if len(content.strip()) < 50:
                        empty.append(Path(path).name)

        if empty:
            return (False, f"Empty changelogs: {', '.join(empty[:3])}")

        return (True, "All changelogs have content")

    def _run_validation_scripts(self) -> bool:
        """Run existing validation scripts."""
        scripts = [
            ("validate-marketplace.py", "Marketplace validation"),
            ("validate-skills.py skills/", "Skills validation"),
        ]

        all_passed = True

        for script, desc in scripts:
            try:
                result = subprocess.run(
                    f"python3 scripts/{script}",
                    shell=True,
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    print(f"  {Colors.GREEN}✓ PASS{Colors.RESET}  {desc}")

                    # Extract summary line
                    for line in result.stdout.split('\n'):
                        if 'passed' in line.lower() or 'total' in line.lower():
                            print(f"         {Colors.DIM}{line.strip()}{Colors.RESET}")
                            break
                else:
                    print(f"  {Colors.RED}✗ FAIL{Colors.RESET}  {desc}")
                    all_passed = False

                    # Show first error
                    for line in result.stdout.split('\n'):
                        if '✗' in line or 'error' in line.lower():
                            print(f"         {Colors.RED}{line.strip()}{Colors.RESET}")
                            break

            except subprocess.TimeoutExpired:
                print(f"  {Colors.YELLOW}⚠ TIMEOUT{Colors.RESET}  {desc}")
            except Exception as e:
                print(f"  {Colors.RED}✗ ERROR{Colors.RESET}  {desc}: {e}")
                all_passed = False

        return all_passed

    def _print_summary(self, all_passed: bool):
        """Print validation summary."""
        print(f"\n{Colors.BOLD}═══ SUMMARY ═══{Colors.RESET}\n")

        passed_count = sum(1 for p, _ in self.results.values() if p)
        total_count = len(self.results)

        # Get stats
        plugins = self.marketplace.get('plugins', [])
        total_skills = sum(len(p.get('skills', [])) for p in plugins)
        version = self.marketplace.get('metadata', {}).get('version', 'unknown')

        print(f"  Marketplace Version: {Colors.CYAN}{version}{Colors.RESET}")
        print(f"  Plugin Groups:       {len(plugins)}")
        print(f"  Total Skills:        {total_skills}")
        print(f"  Checks Passed:       {passed_count}/{total_count}")

        if all_passed:
            print(f"\n  {Colors.GREEN}{Colors.BOLD}✅ ALL AUTOMATED CHECKS PASSED{Colors.RESET}")
        else:
            print(f"\n  {Colors.RED}{Colors.BOLD}❌ SOME CHECKS FAILED - Review above{Colors.RESET}")

    def _print_manual_checklist(self):
        """Print manual validation checklist."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ MANUAL VALIDATION CHECKLIST ═══{Colors.RESET}\n")

        checklist = [
            ("Fresh Installation Test", [
                "rm -rf ~/.claude/plugins/cache/claudex",
                "/plugin marketplace remove claudex",
                "/plugin marketplace add cskiro/claudex",
                "Verify: No 'plugin not found' errors",
            ]),
            ("Plugin Menu Verification", [
                "Run /plugin in Claude Code",
                "Verify all 10 plugins appear",
                "Verify skill counts match",
            ]),
            ("Skill Triggering Test", [
                "Test restored skills trigger correctly:",
                "  - 'audit my codebase' → codebase-auditor",
                "  - 'check accessibility' → accessibility-audit",
                "  - 'create ASCII diagram' → ascii-diagram-creator",
                "  - 'create semantic release' → semantic-release-tagger",
            ]),
            ("Anthropic Repo Comparison", [
                "Compare with github.com/anthropics/skills",
                "Verify flat directory structure",
                "Verify marketplace.json schema match",
            ]),
            ("Regression Check", [
                "Test existing skills still work",
                "Verify no duplicate skill entries",
                "Check plugin descriptions render correctly",
            ]),
        ]

        for section, items in checklist:
            print(f"  {Colors.BOLD}[ ] {section}{Colors.RESET}")
            for item in items:
                print(f"      {Colors.DIM}{item}{Colors.RESET}")
            print()

        print(f"{Colors.YELLOW}Complete manual checks before merging PR!{Colors.RESET}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pre-release validation suite for Claudex')
    parser.add_argument('--quick', action='store_true', help='Skip slow checks')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    # Find repo root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    validator = PreReleaseValidator(repo_root, quick=args.quick, verbose=args.verbose)
    success = validator.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
