#!/usr/bin/env python3
"""
Codebase Audit Engine

Orchestrates comprehensive codebase analysis using multiple specialized analyzers.
Generates detailed audit reports and remediation plans based on modern SDLC best practices.

Usage:
    python audit_engine.py /path/to/codebase --output report.md
    python audit_engine.py /path/to/codebase --format json --output report.json
    python audit_engine.py /path/to/codebase --scope security,quality
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import importlib.util

# Import analyzers dynamically to support progressive loading
ANALYZERS = {
    'quality': 'analyzers.code_quality',
    'testing': 'analyzers.test_coverage',
    'security': 'analyzers.security_scan',
    'dependencies': 'analyzers.dependencies',
    'performance': 'analyzers.performance',
    'technical_debt': 'analyzers.technical_debt',
}


class AuditEngine:
    """
    Core audit engine that orchestrates codebase analysis.

    Uses progressive disclosure: loads only necessary analyzers based on scope.
    """

    def __init__(self, codebase_path: Path, scope: Optional[List[str]] = None):
        """
        Initialize audit engine.

        Args:
            codebase_path: Path to the codebase to audit
            scope: Optional list of analysis categories to run (e.g., ['security', 'quality'])
                  If None, runs all analyzers.
        """
        self.codebase_path = Path(codebase_path).resolve()
        self.scope = scope or list(ANALYZERS.keys())
        self.findings: Dict[str, List[Dict]] = {}
        self.metadata: Dict = {}

        if not self.codebase_path.exists():
            raise FileNotFoundError(f"Codebase path does not exist: {self.codebase_path}")

    def discover_project(self) -> Dict:
        """
        Phase 1: Initial project discovery (lightweight scan).

        Returns:
            Dictionary containing project metadata
        """
        print("🔍 Phase 1: Discovering project structure...")

        metadata = {
            'path': str(self.codebase_path),
            'scan_time': datetime.now().isoformat(),
            'tech_stack': self._detect_tech_stack(),
            'project_type': self._detect_project_type(),
            'total_files': self._count_files(),
            'total_lines': self._count_lines(),
            'git_info': self._get_git_info(),
        }

        self.metadata = metadata
        return metadata

    def _detect_tech_stack(self) -> Dict[str, bool]:
        """Detect languages and frameworks used in the project."""
        tech_stack = {
            'javascript': (self.codebase_path / 'package.json').exists(),
            'typescript': self._file_exists_with_extension('.ts') or self._file_exists_with_extension('.tsx'),
            'python': (self.codebase_path / 'setup.py').exists() or
                     (self.codebase_path / 'pyproject.toml').exists() or
                     self._file_exists_with_extension('.py'),
            'react': self._check_dependency('react'),
            'vue': self._check_dependency('vue'),
            'angular': self._check_dependency('@angular/core'),
            'node': (self.codebase_path / 'package.json').exists(),
            'docker': (self.codebase_path / 'Dockerfile').exists(),
        }
        return {k: v for k, v in tech_stack.items() if v}

    def _detect_project_type(self) -> str:
        """Determine project type (web app, library, CLI, etc.)."""
        if (self.codebase_path / 'package.json').exists():
            try:
                with open(self.codebase_path / 'package.json', 'r') as f:
                    pkg = json.load(f)
                    if pkg.get('private') is False:
                        return 'library'
                    if 'bin' in pkg:
                        return 'cli'
                    return 'web_app'
            except:
                pass

        if (self.codebase_path / 'setup.py').exists():
            return 'python_package'

        return 'unknown'

    def _count_files(self) -> int:
        """Count total files in codebase (excluding common ignore patterns)."""
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        count = 0

        for path in self.codebase_path.rglob('*'):
            if path.is_file() and not any(excluded in path.parts for excluded in exclude_dirs):
                count += 1

        return count

    def _count_lines(self) -> int:
        """Count total lines of code (excluding empty lines and comments)."""
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        code_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', '.rs', '.rb'}
        total_lines = 0

        for path in self.codebase_path.rglob('*'):
            if (path.is_file() and
                path.suffix in code_extensions and
                not any(excluded in path.parts for excluded in exclude_dirs)):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        total_lines += sum(1 for line in f if line.strip() and not line.strip().startswith(('//', '#', '/*', '*')))
                except:
                    pass

        return total_lines

    def _get_git_info(self) -> Optional[Dict]:
        """Get git repository information."""
        git_dir = self.codebase_path / '.git'
        if not git_dir.exists():
            return None

        try:
            import subprocess
            result = subprocess.run(
                ['git', '-C', str(self.codebase_path), 'log', '--oneline', '-10'],
                capture_output=True,
                text=True,
                timeout=5
            )

            commit_count = subprocess.run(
                ['git', '-C', str(self.codebase_path), 'rev-list', '--count', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
                'is_git_repo': True,
                'recent_commits': result.stdout.strip().split('\n') if result.returncode == 0 else [],
                'total_commits': int(commit_count.stdout.strip()) if commit_count.returncode == 0 else 0,
            }
        except:
            return {'is_git_repo': True, 'error': 'Could not read git info'}

    def _file_exists_with_extension(self, extension: str) -> bool:
        """Check if any file with given extension exists."""
        return any(self.codebase_path.rglob(f'*{extension}'))

    def _check_dependency(self, dep_name: str) -> bool:
        """Check if a dependency exists in package.json."""
        pkg_json = self.codebase_path / 'package.json'
        if not pkg_json.exists():
            return False

        try:
            with open(pkg_json, 'r') as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                return dep_name in deps
        except:
            return False

    def run_analysis(self, phase: str = 'full') -> Dict:
        """
        Phase 2: Deep analysis using specialized analyzers.

        Args:
            phase: 'quick' for lightweight scan, 'full' for comprehensive analysis

        Returns:
            Dictionary containing all findings
        """
        print(f"🔬 Phase 2: Running {phase} analysis...")

        for category in self.scope:
            if category not in ANALYZERS:
                print(f"⚠️  Unknown analyzer category: {category}, skipping...")
                continue

            print(f"  Analyzing {category}...")
            analyzer_findings = self._run_analyzer(category)
            if analyzer_findings:
                self.findings[category] = analyzer_findings

        return self.findings

    def _run_analyzer(self, category: str) -> List[Dict]:
        """
        Run a specific analyzer module.

        Args:
            category: Analyzer category name

        Returns:
            List of findings from the analyzer
        """
        module_path = ANALYZERS.get(category)
        if not module_path:
            return []

        try:
            # Import analyzer module dynamically
            analyzer_file = Path(__file__).parent / f"{module_path.replace('.', '/')}.py"

            if not analyzer_file.exists():
                print(f"    ⚠️  Analyzer not yet implemented: {category}")
                return []

            spec = importlib.util.spec_from_file_location(module_path, analyzer_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Each analyzer should have an analyze() function
            if hasattr(module, 'analyze'):
                return module.analyze(self.codebase_path, self.metadata)
            else:
                print(f"    ⚠️  Analyzer missing analyze() function: {category}")
                return []

        except Exception as e:
            print(f"    ❌ Error running analyzer {category}: {e}")
            return []

    def calculate_scores(self) -> Dict[str, float]:
        """
        Calculate health scores for each category and overall.

        Returns:
            Dictionary of scores (0-100 scale)
        """
        scores = {}

        # Calculate score for each category based on findings severity
        for category, findings in self.findings.items():
            if not findings:
                scores[category] = 100.0
                continue

            # Weighted scoring based on severity
            severity_weights = {'critical': 10, 'high': 5, 'medium': 2, 'low': 1}
            total_weight = sum(severity_weights.get(f.get('severity', 'low'), 1) for f in findings)

            # Score decreases based on weighted issues
            # Formula: 100 - (total_weight / num_findings * penalty_factor)
            penalty = min(total_weight, 100)
            scores[category] = max(0, 100 - penalty)

        # Overall score is weighted average
        if scores:
            scores['overall'] = sum(scores.values()) / len(scores)
        else:
            scores['overall'] = 100.0

        return scores

    def generate_summary(self) -> Dict:
        """
        Generate executive summary of audit results.

        Returns:
            Summary dictionary
        """
        critical_count = sum(
            1 for findings in self.findings.values()
            for f in findings
            if f.get('severity') == 'critical'
        )

        high_count = sum(
            1 for findings in self.findings.values()
            for f in findings
            if f.get('severity') == 'high'
        )

        scores = self.calculate_scores()

        return {
            'overall_score': round(scores.get('overall', 0), 1),
            'category_scores': {k: round(v, 1) for k, v in scores.items() if k != 'overall'},
            'critical_issues': critical_count,
            'high_issues': high_count,
            'total_issues': sum(len(findings) for findings in self.findings.values()),
            'metadata': self.metadata,
        }


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Comprehensive codebase auditor based on modern SDLC best practices (2024-25)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        'codebase',
        type=str,
        help='Path to the codebase to audit'
    )

    parser.add_argument(
        '--scope',
        type=str,
        help='Comma-separated list of analysis categories (quality,testing,security,dependencies,performance,technical_debt)',
        default=None
    )

    parser.add_argument(
        '--phase',
        type=str,
        choices=['quick', 'full'],
        default='full',
        help='Analysis depth: quick (Phase 1 only) or full (Phase 1 + 2)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['markdown', 'json', 'html'],
        default='markdown',
        help='Output format for the report'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: stdout)',
        default=None
    )

    args = parser.parse_args()

    # Parse scope
    scope = args.scope.split(',') if args.scope else None

    # Initialize engine
    try:
        engine = AuditEngine(args.codebase, scope=scope)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Run audit
    print("🚀 Starting codebase audit...")
    print(f"   Codebase: {args.codebase}")
    print(f"   Scope: {scope or 'all'}")
    print(f"   Phase: {args.phase}")
    print()

    # Phase 1: Discovery
    metadata = engine.discover_project()
    print(f"   Detected: {', '.join(metadata['tech_stack'].keys())}")
    print(f"   Files: {metadata['total_files']}")
    print(f"   Lines of code: {metadata['total_lines']:,}")
    print()

    # Phase 2: Analysis (if not quick mode)
    if args.phase == 'full':
        findings = engine.run_analysis()

    # Generate summary
    summary = engine.generate_summary()

    # Output results
    print()
    print("📊 Audit complete!")
    print(f"   Overall score: {summary['overall_score']}/100")
    print(f"   Critical issues: {summary['critical_issues']}")
    print(f"   High issues: {summary['high_issues']}")
    print(f"   Total issues: {summary['total_issues']}")
    print()

    # Generate report (to be implemented in report_generator.py)
    if args.output:
        print(f"📝 Report generation will be implemented in report_generator.py")
        print(f"   Format: {args.format}")
        print(f"   Output: {args.output}")


if __name__ == '__main__':
    main()
