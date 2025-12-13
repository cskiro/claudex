#!/usr/bin/env python3
"""
Marketplace Validation Script for claudex

Validates the marketplace.json file and skill integrity for Claude Code plugin marketplace.
Follows Anthropic's official schema from anthropics/skills repository.

Usage:
    python3 scripts/validate-marketplace.py

Exit Codes:
    0 - All validations passed
    1 - Validation errors found
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class MarketplaceValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate(self) -> bool:
        """Run all validations and return True if successful."""
        print(f"{Colors.BOLD}🔍 Validating claudex marketplace (Anthropic schema)...{Colors.RESET}\n")

        # Check marketplace.json exists
        if not self.marketplace_path.exists():
            self.errors.append(f"marketplace.json not found at {self.marketplace_path}")
            return False

        # Load and parse marketplace.json
        try:
            with open(self.marketplace_path, 'r') as f:
                self.marketplace = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in marketplace.json: {e}")
            return False

        # Run validation checks (Anthropic schema)
        self._validate_marketplace_structure()
        self._validate_owner()
        self._validate_metadata()
        self._validate_plugins()
        self._validate_source_isolation()  # NEW: Prevent cache duplication
        self._validate_skill_references()
        self._validate_skill_files()

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _validate_marketplace_structure(self):
        """Validate required top-level fields per Anthropic schema."""
        required_fields = ['name', 'owner', 'metadata', 'plugins']

        for field in required_fields:
            if field not in self.marketplace:
                self.errors.append(f"Missing required field: '{field}'")

    def _validate_owner(self):
        """Validate owner structure per Anthropic schema."""
        if 'owner' not in self.marketplace:
            return

        owner = self.marketplace['owner']

        if not isinstance(owner, dict):
            self.errors.append("'owner' must be an object")
            return

        # Required fields per Anthropic schema
        if 'name' not in owner:
            self.errors.append("'owner.name' is required")

        # Email is required in Anthropic schema
        if 'email' not in owner:
            self.warnings.append("'owner.email' is recommended (required in Anthropic schema)")

    def _validate_metadata(self):
        """Validate metadata structure per Anthropic schema."""
        if 'metadata' not in self.marketplace:
            self.warnings.append("'metadata' is recommended")
            return

        metadata = self.marketplace['metadata']

        if not isinstance(metadata, dict):
            self.errors.append("'metadata' must be an object")
            return

        # Recommended fields per Anthropic schema
        if 'description' not in metadata:
            self.warnings.append("'metadata.description' is recommended")

        if 'version' not in metadata:
            self.warnings.append("'metadata.version' is recommended")
        else:
            version = metadata['version']
            if not self._is_valid_semver(version):
                self.warnings.append(f"Version '{version}' doesn't follow semantic versioning (e.g., 1.0.0)")

    def _validate_plugins(self):
        """Validate plugin entries per Anthropic schema."""
        if 'plugins' not in self.marketplace:
            return

        plugins = self.marketplace['plugins']

        if not isinstance(plugins, list):
            self.errors.append("'plugins' must be an array")
            return

        if len(plugins) == 0:
            self.warnings.append("No plugins defined in marketplace")
            return

        plugin_names: Set[str] = set()

        for idx, plugin in enumerate(plugins):
            self._validate_plugin_entry(plugin, idx, plugin_names)

    def _validate_plugin_entry(self, plugin: Dict, idx: int, plugin_names: Set[str]):
        """Validate a single plugin entry per Anthropic schema."""
        # Check required fields per Anthropic schema
        required_fields = ['name', 'description', 'source', 'strict', 'skills']

        plugin_name = plugin.get('name', f'Plugin #{idx}')

        for field in required_fields:
            if field not in plugin:
                self.errors.append(f"Plugin '{plugin_name}': Missing required field '{field}'")

        # Check for duplicate names
        if 'name' in plugin:
            name = plugin['name']
            if name in plugin_names:
                self.errors.append(f"Plugin '{name}': Duplicate plugin name")
            plugin_names.add(name)

        # Validate source field
        if 'source' in plugin:
            source = plugin['source']
            if not isinstance(source, str):
                self.errors.append(f"Plugin '{plugin_name}': 'source' must be a string")
            elif not source.startswith('./'):
                self.warnings.append(f"Plugin '{plugin_name}': Source should start with './' (Anthropic pattern)")

        # Validate strict field (boolean)
        if 'strict' in plugin:
            if not isinstance(plugin['strict'], bool):
                self.errors.append(f"Plugin '{plugin_name}': 'strict' must be a boolean")

        # Validate skills array
        if 'skills' in plugin:
            skills = plugin['skills']
            if not isinstance(skills, list):
                self.errors.append(f"Plugin '{plugin_name}': 'skills' must be an array")
            elif len(skills) == 0:
                self.warnings.append(f"Plugin '{plugin_name}': Empty skills array")

    def _validate_source_isolation(self):
        """Validate that plugins use isolated source paths to prevent cache duplication.

        Root cause of 10x cache duplication: when plugins share `source: "./"`,
        Claude Code caches the entire repository for each plugin instead of
        isolated subdirectories.

        Valid patterns:
          - "./plugins/plugin-name" (isolated subdirectory)
          - "./skills/category/skill-name" (skill-specific isolation)

        Invalid patterns:
          - "./" (shares entire repo - causes cache duplication)
          - "." (same as above)

        Exception: Hooks-only plugins (empty skills array) get a warning instead
        of an error since cache duplication primarily affects skill loading.
        """
        if 'plugins' not in self.marketplace:
            return

        plugins = self.marketplace['plugins']
        if not isinstance(plugins, list):
            return

        root_source_with_skills = []
        root_source_hooks_only = []

        for plugin in plugins:
            if 'name' not in plugin or 'source' not in plugin:
                continue

            plugin_name = plugin['name']
            source = plugin['source']
            skills = plugin.get('skills', [])
            has_skills = isinstance(skills, list) and len(skills) > 0

            # Check for root-level source paths that cause cache duplication
            if source in ['./', '.', '']:
                if has_skills:
                    root_source_with_skills.append(plugin_name)
                else:
                    root_source_hooks_only.append(plugin_name)

        # Error for plugins with skills using root source
        if root_source_with_skills:
            self.errors.append(
                f"Cache duplication risk: Plugin(s) [{', '.join(root_source_with_skills)}] "
                f"use root source './' - this causes 10x cache duplication. "
                f"Use isolated paths like './plugins/{{name}}' instead."
            )

        # Warning for hooks-only plugins using root source
        if root_source_hooks_only:
            self.warnings.append(
                f"Plugin(s) [{', '.join(root_source_hooks_only)}] use root source './'. "
                f"Consider using isolated paths for consistency."
            )

    def _validate_skill_references(self):
        """Validate that skill paths are correctly formatted."""
        if 'plugins' not in self.marketplace:
            return

        all_skill_paths: Set[str] = set()

        for plugin in self.marketplace['plugins']:
            if 'name' not in plugin or 'skills' not in plugin:
                continue

            plugin_name = plugin['name']
            skills = plugin['skills']

            if not isinstance(skills, list):
                continue

            for skill_path in skills:
                if not isinstance(skill_path, str):
                    self.errors.append(f"Plugin '{plugin_name}': Skill path must be a string, got {type(skill_path)}")
                    continue

                if not skill_path.startswith('./'):
                    self.warnings.append(f"Plugin '{plugin_name}': Skill path '{skill_path}' should start with './'")

                # Check for duplicates across all plugins
                if skill_path in all_skill_paths:
                    self.warnings.append(f"Skill '{skill_path}' is referenced in multiple plugins")
                all_skill_paths.add(skill_path)

    def _validate_skill_files(self):
        """Validate that skill directories and SKILL.md files exist."""
        if 'plugins' not in self.marketplace:
            return

        for plugin in self.marketplace['plugins']:
            if 'name' not in plugin or 'skills' not in plugin:
                continue

            plugin_name = plugin['name']
            skills = plugin['skills']

            if not isinstance(skills, list):
                continue

            for skill_path in skills:
                if not isinstance(skill_path, str):
                    continue

                # Resolve skill directory path
                if skill_path.startswith('./'):
                    skill_dir = self.repo_root / skill_path.lstrip('./')
                else:
                    skill_dir = self.repo_root / skill_path

                # Check directory exists
                if not skill_dir.exists():
                    self.errors.append(f"Plugin '{plugin_name}': Skill directory not found: {skill_path}")
                    continue

                if not skill_dir.is_dir():
                    self.errors.append(f"Plugin '{plugin_name}': Skill path is not a directory: {skill_path}")
                    continue

                # Check SKILL.md exists (Anthropic pattern - NO plugin.json)
                skill_md_path = skill_dir / "SKILL.md"
                if not skill_md_path.exists():
                    self.errors.append(f"Plugin '{plugin_name}': Missing SKILL.md at {skill_path}/SKILL.md")
                    continue

                # Validate SKILL.md has content
                try:
                    with open(skill_md_path, 'r') as f:
                        content = f.read()
                        if len(content.strip()) == 0:
                            self.errors.append(f"Plugin '{plugin_name}': SKILL.md is empty in {skill_path}")
                        elif len(content) < 100:
                            self.warnings.append(f"Plugin '{plugin_name}': SKILL.md seems very short in {skill_path} ({len(content)} chars)")
                except Exception as e:
                    self.errors.append(f"Plugin '{plugin_name}': Could not read SKILL.md in {skill_path}: {e}")

                # Warn if plugin.json exists (not part of Anthropic pattern)
                plugin_json_path = skill_dir / "plugin.json"
                if plugin_json_path.exists():
                    self.warnings.append(f"Skill '{skill_path}': Contains plugin.json (not required in Anthropic schema, marketplace.json is single source of truth)")

    def _is_valid_semver(self, version: str) -> bool:
        """Check if version follows semantic versioning format."""
        import re
        # Basic semver pattern: X.Y.Z[-prerelease][+build]
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
        return bool(re.match(pattern, version))

    def _print_results(self):
        """Print validation results with color coding."""
        print()

        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}❌ Errors ({len(self.errors)}):{Colors.RESET}")
            for error in self.errors:
                print(f"  {Colors.RED}• {error}{Colors.RESET}")
            print()

        if self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Warnings ({len(self.warnings)}):{Colors.RESET}")
            for warning in self.warnings:
                print(f"  {Colors.YELLOW}• {warning}{Colors.RESET}")
            print()

        if self.info:
            print(f"{Colors.BLUE}{Colors.BOLD}ℹ️  Info ({len(self.info)}):{Colors.RESET}")
            for info_msg in self.info:
                print(f"  {Colors.BLUE}• {info_msg}{Colors.RESET}")
            print()

        # Final summary
        if len(self.errors) == 0:
            plugin_count = len(self.marketplace.get('plugins', []))

            # Count total skills
            total_skills = 0
            for plugin in self.marketplace.get('plugins', []):
                if 'skills' in plugin and isinstance(plugin['skills'], list):
                    total_skills += len(plugin['skills'])

            print(f"{Colors.GREEN}{Colors.BOLD}✅ Validation passed!{Colors.RESET}")
            print(f"   Marketplace: {self.marketplace.get('name', 'unknown')}")
            print(f"   Plugin groups: {plugin_count}")
            print(f"   Total skills: {total_skills}")
            print(f"   Warnings: {len(self.warnings)}")
            print()
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ Validation failed with {len(self.errors)} error(s){Colors.RESET}")
            print()

def main():
    """Main entry point."""
    # Determine repository root (parent of .claude-plugin directory)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    validator = MarketplaceValidator(repo_root)
    success = validator.validate()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
