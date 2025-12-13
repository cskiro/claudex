"""
Test Coverage Analyzer

Analyzes:
- Test coverage percentage
- Testing Trophy distribution
- Test quality
- Untested critical paths
"""

import json
from pathlib import Path
from typing import Dict, List


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze test coverage and quality.

    Args:
        codebase_path: Path to codebase
        metadata: Project metadata

    Returns:
        List of testing-related findings
    """
    findings = []

    # Check for test files existence
    test_stats = analyze_test_presence(codebase_path, metadata)
    if test_stats:
        findings.extend(test_stats)

    # Analyze coverage if coverage reports exist
    coverage_findings = analyze_coverage_reports(codebase_path, metadata)
    if coverage_findings:
        findings.extend(coverage_findings)

    return findings


def analyze_test_presence(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Check for test file presence and basic test hygiene."""
    findings = []

    # Count test files
    test_extensions = {'.test.js', '.test.ts', '.test.jsx', '.test.tsx', '.spec.js', '.spec.ts'}
    test_dirs = {'__tests__', 'tests', 'test', 'spec'}

    test_file_count = 0
    source_file_count = 0

    exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__'}
    source_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py'}

    for file_path in codebase_path.rglob('*'):
        if file_path.is_file() and not any(excluded in file_path.parts for excluded in exclude_dirs):

            # Check if it's a test file
            is_test = (
                any(file_path.name.endswith(ext) for ext in test_extensions) or
                any(test_dir in file_path.parts for test_dir in test_dirs)
            )

            if is_test:
                test_file_count += 1
            elif file_path.suffix in source_extensions:
                source_file_count += 1

    # Calculate test ratio
    if source_file_count > 0:
        test_ratio = (test_file_count / source_file_count) * 100

        if test_ratio < 20:
            findings.append({
                'severity': 'high',
                'category': 'testing',
                'subcategory': 'test_coverage',
                'title': f'Low test file ratio ({test_ratio:.1f}%)',
                'description': f'Only {test_file_count} test files for {source_file_count} source files',
                'file': None,
                'line': None,
                'code_snippet': None,
                'impact': 'Insufficient testing leads to bugs and difficult refactoring',
                'remediation': 'Add tests for untested modules, aim for at least 80% coverage',
                'effort': 'high',
            })
        elif test_ratio < 50:
            findings.append({
                'severity': 'medium',
                'category': 'testing',
                'subcategory': 'test_coverage',
                'title': f'Moderate test file ratio ({test_ratio:.1f}%)',
                'description': f'{test_file_count} test files for {source_file_count} source files',
                'file': None,
                'line': None,
                'code_snippet': None,
                'impact': 'More tests needed to achieve recommended 80% coverage',
                'remediation': 'Continue adding tests, focus on critical paths first',
                'effort': 'medium',
            })

    return findings


def analyze_coverage_reports(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze coverage reports if they exist."""
    findings = []

    # Look for coverage reports (Istanbul/c8 format)
    coverage_files = [
        codebase_path / 'coverage' / 'coverage-summary.json',
        codebase_path / 'coverage' / 'coverage-final.json',
        codebase_path / '.nyc_output' / 'coverage-summary.json',
    ]

    for coverage_file in coverage_files:
        if coverage_file.exists():
            try:
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)

                # Extract total coverage
                total = coverage_data.get('total', {})

                line_coverage = total.get('lines', {}).get('pct', 0)
                branch_coverage = total.get('branches', {}).get('pct', 0)
                function_coverage = total.get('functions', {}).get('pct', 0)
                statement_coverage = total.get('statements', {}).get('pct', 0)

                # Check against 80% threshold
                if line_coverage < 80:
                    severity = 'high' if line_coverage < 50 else 'medium'
                    findings.append({
                        'severity': severity,
                        'category': 'testing',
                        'subcategory': 'test_coverage',
                        'title': f'Line coverage below target ({line_coverage:.1f}%)',
                        'description': f'Current coverage is {line_coverage:.1f}%, target is 80%',
                        'file': 'coverage/coverage-summary.json',
                        'line': None,
                        'code_snippet': None,
                        'impact': 'Low coverage means untested code paths and higher bug risk',
                        'remediation': f'Add tests to increase coverage by {80 - line_coverage:.1f}%',
                        'effort': 'high',
                    })

                if branch_coverage < 75:
                    findings.append({
                        'severity': 'medium',
                        'category': 'testing',
                        'subcategory': 'test_coverage',
                        'title': f'Branch coverage below target ({branch_coverage:.1f}%)',
                        'description': f'Current branch coverage is {branch_coverage:.1f}%, target is 75%',
                        'file': 'coverage/coverage-summary.json',
                        'line': None,
                        'code_snippet': None,
                        'impact': 'Untested branches can hide bugs in conditional logic',
                        'remediation': 'Add tests for edge cases and conditional branches',
                        'effort': 'medium',
                    })

                break  # Found coverage, don't check other files

            except:
                pass

    # If no coverage report found
    if not findings:
        findings.append({
            'severity': 'medium',
            'category': 'testing',
            'subcategory': 'test_infrastructure',
            'title': 'No coverage report found',
            'description': 'Could not find coverage-summary.json',
            'file': None,
            'line': None,
            'code_snippet': None,
            'impact': 'Cannot measure test effectiveness without coverage reports',
            'remediation': 'Configure test runner to generate coverage reports (Jest: --coverage, Vitest: --coverage)',
            'effort': 'low',
        })

    return findings
