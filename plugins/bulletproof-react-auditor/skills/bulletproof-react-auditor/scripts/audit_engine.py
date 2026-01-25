#!/usr/bin/env python3
"""
Bulletproof React Audit Engine

Orchestrates comprehensive React/TypeScript codebase analysis against Bulletproof
React architecture principles. Generates detailed audit reports and migration plans.

Usage:
    python audit_engine.py /path/to/react-app --output report.md
    python audit_engine.py /path/to/react-app --format json --output report.json
    python audit_engine.py /path/to/react-app --migration-plan --output migration.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import importlib.util

# Bulletproof React specific analyzers
ANALYZERS = {
    'structure': 'analyzers.project_structure',
    'components': 'analyzers.component_architecture',
    'state': 'analyzers.state_management',
    'api': 'analyzers.api_layer',
    'testing': 'analyzers.testing_strategy',
    'styling': 'analyzers.styling_patterns',
    'errors': 'analyzers.error_handling',
    'performance': 'analyzers.performance_patterns',
    'security': 'analyzers.security_practices',
    'standards': 'analyzers.standards_compliance',
}


class BulletproofAuditEngine:
    """
    Core audit engine for Bulletproof React compliance analysis.

    Uses progressive disclosure: loads only necessary analyzers based on scope.
    """

    def __init__(self, codebase_path: Path, scope: Optional[List[str]] = None):
        """
        Initialize Bulletproof React audit engine.

        Args:
            codebase_path: Path to the React codebase to audit
            scope: Optional list of analysis categories to run
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
        Phase 1: Initial React project discovery (lightweight scan).

        Returns:
            Dictionary containing React project metadata
        """
        print("🔍 Phase 1: Discovering React project structure...")

        metadata = {
            'path': str(self.codebase_path),
            'scan_time': datetime.now().isoformat(),
            'is_react': self._detect_react(),
            'tech_stack': self._detect_tech_stack(),
            'structure_type': self._detect_structure_type(),
            'total_files': self._count_files(),
            'total_lines': self._count_lines(),
            'git_info': self._get_git_info(),
        }

        if not metadata['is_react']:
            print("⚠️  Warning: This does not appear to be a React project!")
            print("   Bulletproof React audit is designed for React applications.")

        self.metadata = metadata
        return metadata

    def _detect_react(self) -> bool:
        """Check if this is a React project."""
        pkg_json = self.codebase_path / 'package.json'
        if not pkg_json.exists():
            return False

        try:
            with open(pkg_json, 'r') as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                return 'react' in deps or 'react-dom' in deps
        except:
            return False

    def _detect_tech_stack(self) -> Dict[str, bool]:
        """Detect React ecosystem tools and libraries."""
        pkg_json = self.codebase_path / 'package.json'
        tech_stack = {}

        if pkg_json.exists():
            try:
                with open(pkg_json, 'r') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                    # Core
                    tech_stack['react'] = 'react' in deps
                    tech_stack['typescript'] = 'typescript' in deps or (self.codebase_path / 'tsconfig.json').exists()

                    # Build tools
                    tech_stack['vite'] = 'vite' in deps
                    tech_stack['create-react-app'] = 'react-scripts' in deps
                    tech_stack['next'] = 'next' in deps

                    # State management
                    tech_stack['redux'] = 'redux' in deps or '@reduxjs/toolkit' in deps
                    tech_stack['zustand'] = 'zustand' in deps
                    tech_stack['jotai'] = 'jotai' in deps
                    tech_stack['mobx'] = 'mobx' in deps

                    # Data fetching
                    tech_stack['react-query'] = '@tanstack/react-query' in deps or 'react-query' in deps
                    tech_stack['swr'] = 'swr' in deps
                    tech_stack['apollo'] = '@apollo/client' in deps
                    tech_stack['rtk-query'] = '@reduxjs/toolkit' in deps

                    # Forms
                    tech_stack['react-hook-form'] = 'react-hook-form' in deps
                    tech_stack['formik'] = 'formik' in deps

                    # Styling
                    tech_stack['tailwind'] = 'tailwindcss' in deps or (self.codebase_path / 'tailwind.config.js').exists()
                    tech_stack['styled-components'] = 'styled-components' in deps
                    tech_stack['emotion'] = '@emotion/react' in deps
                    tech_stack['chakra-ui'] = '@chakra-ui/react' in deps
                    tech_stack['mui'] = '@mui/material' in deps
                    tech_stack['radix-ui'] = any('@radix-ui' in dep for dep in deps.keys())

                    # Testing
                    tech_stack['vitest'] = 'vitest' in deps
                    tech_stack['jest'] = 'jest' in deps
                    tech_stack['testing-library'] = '@testing-library/react' in deps
                    tech_stack['playwright'] = '@playwright/test' in deps
                    tech_stack['cypress'] = 'cypress' in deps

                    # Routing
                    tech_stack['react-router'] = 'react-router-dom' in deps

                    # Error tracking
                    tech_stack['sentry'] = '@sentry/react' in deps

                    # Code quality
                    tech_stack['eslint'] = 'eslint' in deps
                    tech_stack['prettier'] = 'prettier' in deps
                    tech_stack['husky'] = 'husky' in deps

            except:
                pass

        return {k: v for k, v in tech_stack.items() if v}

    def _detect_structure_type(self) -> str:
        """Determine project structure pattern (feature-based vs flat)."""
        src_dir = self.codebase_path / 'src'
        if not src_dir.exists():
            return 'no_src_directory'

        features_dir = src_dir / 'features'
        components_dir = src_dir / 'components'
        app_dir = src_dir / 'app'

        # Count files in different locations
        features_files = len(list(features_dir.rglob('*.{js,jsx,ts,tsx}'))) if features_dir.exists() else 0
        components_files = len(list(components_dir.rglob('*.{js,jsx,ts,tsx}'))) if components_dir.exists() else 0

        if features_dir.exists() and app_dir.exists():
            if features_files > components_files * 2:
                return 'feature_based'
            else:
                return 'mixed'
        elif features_dir.exists():
            return 'partial_feature_based'
        else:
            return 'flat'

    def _count_files(self) -> int:
        """Count total files in React codebase."""
        exclude_dirs = {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'coverage'}
        count = 0

        for path in self.codebase_path.rglob('*'):
            if path.is_file() and not any(excluded in path.parts for excluded in exclude_dirs):
                count += 1

        return count

    def _count_lines(self) -> int:
        """Count total lines of code in React files."""
        exclude_dirs = {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'coverage'}
        code_extensions = {'.js', '.jsx', '.ts', '.tsx'}
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

    def run_analysis(self, phase: str = 'full') -> Dict:
        """
        Phase 2: Deep Bulletproof React analysis using specialized analyzers.

        Args:
            phase: 'quick' for lightweight scan, 'full' for comprehensive analysis

        Returns:
            Dictionary containing all findings
        """
        print(f"🔬 Phase 2: Running {phase} Bulletproof React analysis...")

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
        Run a specific Bulletproof React analyzer module.

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
        Calculate Bulletproof React compliance scores for each category.

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
            severity_weights = {'critical': 15, 'high': 8, 'medium': 3, 'low': 1}
            total_weight = sum(severity_weights.get(f.get('severity', 'low'), 1) for f in findings)

            # Score decreases based on weighted issues
            penalty = min(total_weight * 2, 100)  # Each point = 2% penalty
            scores[category] = max(0, 100 - penalty)

        # Overall score is weighted average
        if scores:
            scores['overall'] = sum(scores.values()) / len(scores)
        else:
            scores['overall'] = 100.0

        return scores

    def calculate_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90: return 'A'
        if score >= 80: return 'B'
        if score >= 70: return 'C'
        if score >= 60: return 'D'
        return 'F'

    def generate_summary(self) -> Dict:
        """
        Generate executive summary of Bulletproof React audit results.

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
        overall_score = scores.get('overall', 0)

        # Estimate migration effort in person-days
        effort_map = {'low': 0.5, 'medium': 2, 'high': 5}
        total_effort = sum(
            effort_map.get(f.get('effort', 'medium'), 2)
            for findings in self.findings.values()
            for f in findings
        )

        return {
            'compliance_score': round(overall_score, 1),
            'grade': self.calculate_grade(overall_score),
            'category_scores': {k: round(v, 1) for k, v in scores.items() if k != 'overall'},
            'critical_issues': critical_count,
            'high_issues': high_count,
            'total_issues': sum(len(findings) for findings in self.findings.values()),
            'migration_effort_days': round(total_effort, 1),
            'structure_type': self.metadata.get('structure_type', 'unknown'),
            'metadata': self.metadata,
        }


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Bulletproof React audit tool for React/TypeScript applications',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        'codebase',
        type=str,
        help='Path to the React codebase to audit'
    )

    parser.add_argument(
        '--scope',
        type=str,
        help='Comma-separated list of analysis categories (structure,components,state,api,testing,styling,errors,performance,security,standards)',
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

    parser.add_argument(
        '--migration-plan',
        action='store_true',
        help='Generate migration plan in addition to audit report'
    )

    args = parser.parse_args()

    # Parse scope
    scope = args.scope.split(',') if args.scope else None

    # Initialize engine
    try:
        engine = BulletproofAuditEngine(args.codebase, scope=scope)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Run audit
    print("🚀 Starting Bulletproof React audit...")
    print(f"   Codebase: {args.codebase}")
    print(f"   Scope: {scope or 'all'}")
    print(f"   Phase: {args.phase}")
    print()

    # Phase 1: Discovery
    metadata = engine.discover_project()
    if metadata['is_react']:
        print(f"   React detected: ✅")
        print(f"   TypeScript: {'✅' if metadata['tech_stack'].get('typescript') else '❌'}")
        print(f"   Structure type: {metadata['structure_type']}")
        print(f"   Files: {metadata['total_files']}")
        print(f"   Lines of code: {metadata['total_lines']:,}")
    else:
        print(f"   React detected: ❌")
        print("   Continuing audit anyway...")
    print()

    # Phase 2: Analysis (if not quick mode)
    if args.phase == 'full':
        findings = engine.run_analysis()

    # Generate summary
    summary = engine.generate_summary()

    # Output results
    print()
    print("📊 Bulletproof React Audit Complete!")
    print(f"   Compliance score: {summary['compliance_score']}/100 (Grade: {summary['grade']})")
    print(f"   Critical issues: {summary['critical_issues']}")
    print(f"   High issues: {summary['high_issues']}")
    print(f"   Total issues: {summary['total_issues']}")
    print(f"   Estimated migration effort: {summary['migration_effort_days']} person-days")
    print()

    # Generate report (to be implemented in report_generator.py)
    if args.output:
        print(f"📝 Report generation will be implemented in report_generator.py")
        print(f"   Format: {args.format}")
        print(f"   Output: {args.output}")
        if args.migration_plan:
            print(f"   Migration plan: {args.output.replace('.md', '_migration.md')}")


if __name__ == '__main__':
    main()
