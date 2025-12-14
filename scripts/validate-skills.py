#!/usr/bin/env python3
"""
Skills Validation Script for claudex

Validates individual skills against Anthropic's official skill specification and quality standards.
Based on:
  - Official Spec: github.com/anthropics/skills/spec/agent-skills-spec.md
  - docs/standards/skill-anatomy.md (comprehensive guide)
  - docs/standards/skill-structure.md (claudex standards)

Usage:
    python3 scripts/validate-skills.py                    # Validate all skills
    python3 scripts/validate-skills.py skills/analysis    # Validate specific directory
    python3 scripts/validate-skills.py --verbose          # Show detailed output

Exit Codes:
    0 - All validations passed
    1 - Validation errors found
"""

import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class SkillValidator:
    """Validates a single skill against Anthropic standards."""

    # Anthropic Spec Limits (from official spec)
    MAX_NAME_LENGTH = 64           # Official spec limit
    MAX_DESCRIPTION_LENGTH = 1024  # Official spec limit (~100 words)

    # Best Practice Limits
    MAX_SKILL_MD_LINES = 200       # Recommended for progressive disclosure
    MIN_DESCRIPTION_LENGTH = 50    # Minimum for meaningful description
    RECOMMENDED_DESC_WORDS = 100   # Optimal for indexing

    # Scoring weights
    WEIGHTS = {
        'file_structure': 0.10,
        'frontmatter': 0.15,        # Increased - spec compliance is critical
        'spec_compliance': 0.15,    # NEW - Anthropic spec checks
        'description_quality': 0.20,
        'progressive_disclosure': 0.20,
        'main_instructions': 0.10,
        'testing_invocation': 0.10
    }

    def __init__(self, skill_path: Path, verbose: bool = False):
        self.skill_path = skill_path
        self.verbose = verbose
        self.skill_name = skill_path.name
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.scores: Dict[str, float] = {}
        self.skill_md_content = ""
        self.frontmatter = {}

    def validate(self) -> Tuple[bool, float]:
        """Run all validations. Returns (passed, score)."""
        # Load SKILL.md first
        if not self._load_skill_md():
            return (False, 0.0)

        # Run all validation checks
        self.scores['file_structure'] = self._validate_file_structure()
        self.scores['frontmatter'] = self._validate_frontmatter()
        self.scores['spec_compliance'] = self._validate_spec_compliance()  # NEW
        self.scores['description_quality'] = self._validate_description_quality()
        self.scores['progressive_disclosure'] = self._validate_progressive_disclosure()
        self.scores['main_instructions'] = self._validate_main_instructions()
        self.scores['testing_invocation'] = self._validate_testing_invocation()

        # Calculate weighted score
        total_score = sum(
            self.scores[key] * self.WEIGHTS[key]
            for key in self.scores
        )

        # Passed if no errors and score >= 70
        passed = len(self.errors) == 0 and total_score >= 70

        return (passed, total_score)

    def _load_skill_md(self) -> bool:
        """Load and parse SKILL.md file."""
        skill_md_path = self.skill_path / "SKILL.md"

        if not skill_md_path.exists():
            self.errors.append("Missing SKILL.md file")
            return False

        try:
            with open(skill_md_path, 'r') as f:
                self.skill_md_content = f.read()
        except Exception as e:
            self.errors.append(f"Could not read SKILL.md: {e}")
            return False

        # Parse frontmatter
        self._parse_frontmatter()

        return True

    def _parse_frontmatter(self):
        """Extract YAML frontmatter from SKILL.md."""
        content = self.skill_md_content

        if not content.startswith('---'):
            self.errors.append("SKILL.md must start with YAML frontmatter (---)")
            return

        # Find closing ---
        end_match = re.search(r'\n---\n', content[3:])
        if not end_match:
            self.errors.append("Invalid frontmatter: missing closing ---")
            return

        frontmatter_text = content[3:end_match.start() + 3]
        lines = frontmatter_text.split('\n')

        # Parse YAML with support for multi-line block scalars (>- and |-)
        current_key = None
        current_value_lines = []
        in_multiline = False
        indent_level = 0

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                if in_multiline and current_key:
                    current_value_lines.append('')
                continue

            # Check if this is a new key: value pair at root level
            if not line.startswith(' ') and ':' in stripped and not in_multiline:
                # Save previous multi-line value if any
                if current_key and current_value_lines:
                    self.frontmatter[current_key] = ' '.join(current_value_lines).strip()
                    current_value_lines = []

                key, value = stripped.split(':', 1)
                current_key = key.strip()
                value = value.strip()

                # Check for multi-line block scalar indicator
                if value in ('>-', '|-', '>', '|'):
                    in_multiline = True
                    indent_level = 2  # Standard YAML indent
                    current_value_lines = []
                elif value.startswith('>-') or value.startswith('|-'):
                    in_multiline = True
                    indent_level = 2
                    current_value_lines = []
                else:
                    in_multiline = False
                    # Handle quoted strings
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    # Handle arrays (basic)
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]

                    self.frontmatter[current_key] = value
                    current_key = None

            elif in_multiline and current_key:
                # This is a continuation of a multi-line value
                if line.startswith(' '):
                    current_value_lines.append(stripped)
                else:
                    # End of multi-line block
                    self.frontmatter[current_key] = ' '.join(current_value_lines).strip()
                    current_value_lines = []
                    in_multiline = False
                    # Re-process this line as a new key
                    if ':' in stripped:
                        key, value = stripped.split(':', 1)
                        current_key = key.strip()
                        value = value.strip()
                        if value and value not in ('>-', '|-', '>', '|'):
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            elif value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]
                            self.frontmatter[current_key] = value
                            current_key = None

        # Don't forget the last multi-line value
        if current_key and current_value_lines:
            self.frontmatter[current_key] = ' '.join(current_value_lines).strip()

    def _validate_file_structure(self) -> float:
        """Validate required files and directory structure. Returns score 0-100."""
        score = 100

        # Required files
        required_files = ['SKILL.md', 'README.md', 'CHANGELOG.md']
        for filename in required_files:
            if not (self.skill_path / filename).exists():
                self.errors.append(f"Missing required file: {filename}")
                score -= 20

        # Recommended directories (bonus if present)
        recommended_dirs = ['workflow', 'reference', 'examples', 'templates', 'data', 'modes']
        dirs_present = sum(1 for d in recommended_dirs if (self.skill_path / d).is_dir())

        if dirs_present == 0:
            self.info.append("No progressive disclosure directories found (workflow/, reference/, examples/)")
        elif dirs_present >= 2:
            self.info.append(f"Good progressive disclosure: {dirs_present} supporting directories")

        # Anti-patterns
        if (self.skill_path / 'plugin.json').exists():
            self.warnings.append("Contains plugin.json (not required by Anthropic schema)")
            score -= 5

        return max(0, score)

    def _validate_frontmatter(self) -> float:
        """Validate frontmatter structure. Returns score 0-100."""
        score = 100

        # Required fields
        if 'name' not in self.frontmatter:
            self.errors.append("Frontmatter missing required field: name")
            score -= 30
        else:
            name = self.frontmatter['name']
            # Check kebab-case
            if not re.match(r'^[a-z][a-z0-9-]*$', name):
                self.warnings.append(f"Name '{name}' should be lowercase with hyphens (kebab-case)")
                score -= 10

        if 'description' not in self.frontmatter:
            self.errors.append("Frontmatter missing required field: description")
            score -= 30

        # Optional fields (info only)
        optional_fields = ['version', 'author', 'category', 'tags', 'license']
        present_optional = [f for f in optional_fields if f in self.frontmatter]
        if present_optional and self.verbose:
            self.info.append(f"Optional frontmatter fields: {', '.join(present_optional)}")

        return max(0, score)

    def _validate_spec_compliance(self) -> float:
        """Validate against Anthropic's official skill specification. Returns score 0-100."""
        score = 100

        # 1. Name length check (spec: ≤64 chars)
        if 'name' in self.frontmatter:
            name = self.frontmatter['name']
            if len(name) > self.MAX_NAME_LENGTH:
                self.errors.append(f"Name exceeds spec limit: {len(name)}/{self.MAX_NAME_LENGTH} chars")
                score -= 30

            # 2. Name must match directory name (spec requirement)
            dir_name = self.skill_path.name
            if name != dir_name:
                self.errors.append(f"Name '{name}' does not match directory '{dir_name}' (spec requirement)")
                score -= 25

        # 3. Description length check (spec: ≤1024 chars)
        if 'description' in self.frontmatter:
            desc = self.frontmatter['description']
            if len(desc) > self.MAX_DESCRIPTION_LENGTH:
                self.errors.append(f"Description exceeds spec limit: {len(desc)}/{self.MAX_DESCRIPTION_LENGTH} chars")
                score -= 20

            # Check word count (best practice: ~100 words)
            word_count = len(desc.split())
            if word_count > 150:
                self.warnings.append(f"Description has {word_count} words (recommended: ~{self.RECOMMENDED_DESC_WORDS})")
                score -= 5

        # 4. Version field check (recommended for marketplace)
        if 'version' not in self.frontmatter:
            self.warnings.append("Missing 'version' field in frontmatter (recommended for marketplace)")
            score -= 10

        # 5. Check referenced files exist
        self._check_referenced_files()

        # 6. Check script permissions
        self._check_script_permissions()

        return max(0, score)

    def _check_referenced_files(self):
        """Check that markdown links to local files actually exist."""
        # Extract markdown links: [text](path)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', self.skill_md_content)

        for text, path in links:
            # Skip external URLs and anchors
            if path.startswith('http') or path.startswith('#'):
                continue

            # Resolve relative to skill directory
            full_path = self.skill_path / path
            if not full_path.exists():
                self.warnings.append(f"Referenced file not found: {path}")

    def _check_script_permissions(self):
        """Check that shell scripts have execute permissions."""
        scripts_dir = self.skill_path / 'scripts'
        if not scripts_dir.exists():
            return

        for script in scripts_dir.glob('**/*.sh'):
            if not os.access(script, os.X_OK):
                self.warnings.append(f"Script missing execute permission: {script.name}")

    def _validate_description_quality(self) -> float:
        """Validate description quality (most critical). Returns score 0-100."""
        score = 100

        if 'description' not in self.frontmatter:
            return 0

        description = self.frontmatter['description']

        # Length check
        if len(description) < self.MIN_DESCRIPTION_LENGTH:
            self.warnings.append(f"Description too short ({len(description)} chars, min {self.MIN_DESCRIPTION_LENGTH})")
            score -= 15
        elif len(description) > self.MAX_DESCRIPTION_LENGTH:
            self.warnings.append(f"Description too long ({len(description)} chars, max {self.MAX_DESCRIPTION_LENGTH})")
            score -= 10

        # Check for proactive trigger pattern (info only - not required by Anthropic spec)
        # Official pattern: "[Capabilities]. When Claude needs to [context]."
        # Claudex convention: "Use PROACTIVELY when [context]. [Capabilities]."
        if description.lower().startswith('use proactively'):
            if self.verbose:
                self.info.append("Uses Claudex proactive trigger convention")
        elif 'when' in description.lower() or 'for' in description.lower():
            if self.verbose:
                self.info.append("Uses standard trigger context pattern")
        else:
            self.warnings.append("Consider adding trigger context ('When...' or 'Use when...')")
            score -= 10

        # Check for action verbs
        action_verbs = ['validates', 'generates', 'creates', 'audits', 'analyzes',
                       'automates', 'detects', 'provides', 'extracts', 'configures',
                       'transforms', 'builds', 'processes', 'enables', 'supports']
        verbs_found = [v for v in action_verbs if v in description.lower()]

        if not verbs_found:
            self.warnings.append("Description lacks specific action verbs (validates, generates, creates, etc.)")
            score -= 15
        elif len(verbs_found) >= 2:
            if self.verbose:
                self.info.append(f"Good action verbs: {', '.join(verbs_found[:3])}")

        # Check for boundaries/limitations
        boundary_patterns = ['not for', 'not suitable', 'cannot', "doesn't", 'limitations']
        has_boundaries = any(p in description.lower() for p in boundary_patterns)

        if not has_boundaries:
            self.warnings.append("Description should state what the skill is NOT for (boundaries)")
            score -= 10

        # Check for use cases
        use_case_patterns = ['when', 'for', 'use case', 'use for']
        has_use_cases = any(p in description.lower() for p in use_case_patterns)

        if not has_use_cases:
            self.warnings.append("Description should include specific use cases")
            score -= 10

        return max(0, score)

    def _validate_progressive_disclosure(self) -> float:
        """Validate progressive disclosure pattern. Returns score 0-100."""
        score = 100

        # Count lines in SKILL.md
        lines = self.skill_md_content.split('\n')
        line_count = len(lines)

        if line_count > self.MAX_SKILL_MD_LINES:
            over_by = line_count - self.MAX_SKILL_MD_LINES
            self.warnings.append(f"SKILL.md has {line_count} lines (target <= {self.MAX_SKILL_MD_LINES}, over by {over_by})")
            # Penalty scales with how far over
            penalty = min(30, over_by // 10 * 5)
            score -= penalty
        else:
            if self.verbose:
                self.info.append(f"Good SKILL.md size: {line_count} lines")

        # Check for references to subdirectories (progressive disclosure)
        has_workflow_refs = bool(re.search(r'workflow/|modes/', self.skill_md_content))
        has_reference_refs = bool(re.search(r'reference/', self.skill_md_content))
        has_example_refs = bool(re.search(r'examples/', self.skill_md_content))

        refs_count = sum([has_workflow_refs, has_reference_refs, has_example_refs])

        if refs_count == 0 and line_count > 150:
            self.warnings.append("Large SKILL.md without references to workflow/, reference/, or examples/")
            score -= 20
        elif refs_count >= 2:
            if self.verbose:
                self.info.append("Good progressive disclosure with file references")

        return max(0, score)

    def _validate_main_instructions(self) -> float:
        """Validate main instruction content. Returns score 0-100."""
        score = 100
        content_lower = self.skill_md_content.lower()

        # Check for required sections
        required_sections = [
            ('overview', ['## overview', '# overview']),
            ('when to use', ['## when to use', 'trigger phrase', 'use case'])
        ]

        for section_name, patterns in required_sections:
            found = any(p in content_lower for p in patterns)
            if not found:
                self.warnings.append(f"Missing recommended section: {section_name}")
                score -= 15

        # Check for markdown structure
        has_headers = bool(re.search(r'^#{1,3} ', self.skill_md_content, re.MULTILINE))
        has_bullets = bool(re.search(r'^[\s]*[-*] ', self.skill_md_content, re.MULTILINE))
        has_tables = bool(re.search(r'\|.*\|', self.skill_md_content))

        if not has_headers:
            self.warnings.append("SKILL.md lacks markdown headers for structure")
            score -= 10

        if has_tables or has_bullets:
            if self.verbose:
                self.info.append("Good use of markdown formatting (tables/bullets)")

        # Check for limitations section
        if 'limitation' not in content_lower and 'not for' not in content_lower:
            self.warnings.append("Missing limitations or 'NOT for' section")
            score -= 10

        return max(0, score)

    def _validate_testing_invocation(self) -> float:
        """Validate testing and invocation documentation. Returns score 0-100."""
        score = 100
        content_lower = self.skill_md_content.lower()

        # Check for trigger phrases
        trigger_patterns = ['trigger phrase', 'trigger', '"', "'"]
        has_triggers = any(p in content_lower for p in trigger_patterns[:2])

        if not has_triggers:
            self.warnings.append("Missing trigger phrases documentation")
            score -= 30

        # Check for examples
        has_examples = 'example' in content_lower or '```' in self.skill_md_content

        if not has_examples:
            self.warnings.append("No usage examples found")
            score -= 20

        # Check for success criteria
        has_criteria = 'success criteria' in content_lower or '- [ ]' in self.skill_md_content

        if has_criteria and self.verbose:
            self.info.append("Has success criteria checklist")

        return max(0, score)

    def get_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


class SkillsValidator:
    """Validates all skills in the marketplace."""

    def __init__(self, repo_root: Path, target_path: Path = None, verbose: bool = False):
        self.repo_root = repo_root
        self.target_path = target_path
        self.verbose = verbose
        self.results: List[Tuple[str, bool, float, SkillValidator]] = []

    def _find_skills_recursive(self, base_path: Path) -> List[Path]:
        """Recursively find all skill directories (those containing SKILL.md)."""
        skill_dirs = []
        for item in base_path.iterdir():
            if item.is_dir():
                if (item / "SKILL.md").exists():
                    skill_dirs.append(item)
                else:
                    # Recurse into subdirectories
                    skill_dirs.extend(self._find_skills_recursive(item))
        return skill_dirs

    def validate(self) -> bool:
        """Validate all skills. Returns True if all passed."""
        print(f"{Colors.BOLD}🔍 Validating skills against Anthropic standards...{Colors.RESET}\n")

        # Support both old (skills/) and new (plugins/) structures
        plugins_dir = self.repo_root / "plugins"
        skills_dir = self.repo_root / "skills"

        # Determine which structure exists
        if plugins_dir.exists():
            base_dir = plugins_dir
            structure = "plugins"
        elif skills_dir.exists():
            base_dir = skills_dir
            structure = "skills"
        else:
            print(f"{Colors.RED}Error: Neither plugins/ nor skills/ directory found{Colors.RESET}")
            return False

        # Get skill directories
        if self.target_path:
            if self.target_path.is_dir():
                if (self.target_path / "SKILL.md").exists():
                    # Target is a skill directory
                    skill_dirs = [self.target_path]
                else:
                    # Target is a category directory - recursively find skills
                    skill_dirs = self._find_skills_recursive(self.target_path)
            else:
                print(f"{Colors.RED}Error: {self.target_path} is not a directory{Colors.RESET}")
                return False
        else:
            # Find all skill directories based on structure
            skill_dirs = []
            if structure == "plugins":
                # New structure: plugins/{plugin-name}/skills/{skill-name}/
                for plugin_dir in base_dir.iterdir():
                    if plugin_dir.is_dir():
                        plugin_skills = plugin_dir / "skills"
                        if plugin_skills.exists():
                            skill_dirs.extend(self._find_skills_recursive(plugin_skills))
            else:
                # Old structure: skills/{category}/{skill-name}/
                skill_dirs = self._find_skills_recursive(base_dir)

        if not skill_dirs:
            print(f"{Colors.YELLOW}No skills found to validate{Colors.RESET}")
            return True

        # Sort by path for consistent output
        skill_dirs.sort(key=lambda x: str(x))

        # Validate each skill
        for skill_dir in skill_dirs:
            validator = SkillValidator(skill_dir, self.verbose)
            passed, score = validator.validate()

            # Get relative path for display
            try:
                rel_path = skill_dir.relative_to(self.repo_root)
            except ValueError:
                rel_path = skill_dir

            self.results.append((str(rel_path), passed, score, validator))

        # Print results
        self._print_results()

        # Return True if all passed
        return all(passed for _, passed, _, _ in self.results)

    def _print_results(self):
        """Print validation results."""
        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}Skills Validation Results{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

        passed_count = 0
        total_score = 0

        for rel_path, passed, score, validator in self.results:
            grade = validator.get_grade(score)

            if passed:
                status = f"{Colors.GREEN}PASS{Colors.RESET}"
                passed_count += 1
            else:
                status = f"{Colors.RED}FAIL{Colors.RESET}"

            # Color code grade
            if grade in ['A', 'B']:
                grade_color = Colors.GREEN
            elif grade == 'C':
                grade_color = Colors.YELLOW
            else:
                grade_color = Colors.RED

            print(f"{status} {grade_color}{grade}{Colors.RESET} ({score:.0f}%) {Colors.CYAN}{rel_path}{Colors.RESET}")

            # Print errors and warnings if any
            if validator.errors:
                for error in validator.errors:
                    print(f"     {Colors.RED}✗ {error}{Colors.RESET}")

            if validator.warnings and (self.verbose or not passed):
                for warning in validator.warnings[:3]:  # Limit to 3 warnings unless verbose
                    print(f"     {Colors.YELLOW}⚠ {warning}{Colors.RESET}")
                if len(validator.warnings) > 3 and not self.verbose:
                    print(f"     {Colors.YELLOW}... and {len(validator.warnings) - 3} more warnings{Colors.RESET}")

            if self.verbose and validator.info:
                for info_msg in validator.info:
                    print(f"     {Colors.BLUE}ℹ {info_msg}{Colors.RESET}")

            total_score += score

        # Summary
        avg_score = total_score / len(self.results) if self.results else 0
        avg_grade = SkillValidator(Path('.')).get_grade(avg_score)

        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}Summary{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"Total skills:  {len(self.results)}")
        print(f"Passed:        {passed_count}/{len(self.results)}")
        print(f"Average score: {avg_score:.0f}% (Grade {avg_grade})")

        if passed_count == len(self.results):
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All skills passed validation!{Colors.RESET}")
        else:
            failed_count = len(self.results) - passed_count
            print(f"\n{Colors.RED}{Colors.BOLD}❌ {failed_count} skill(s) failed validation{Colors.RESET}")

        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Validate Claude Code skills against Anthropic standards')
    parser.add_argument('path', nargs='?', help='Path to skill or category directory (optional)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    # Determine repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    # Determine target path
    target_path = None
    if args.path:
        target_path = Path(args.path)
        if not target_path.is_absolute():
            target_path = repo_root / target_path

    validator = SkillsValidator(repo_root, target_path, args.verbose)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
