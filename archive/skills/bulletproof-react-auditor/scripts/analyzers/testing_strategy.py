"""
Testing Strategy Analyzer

Analyzes React testing against Bulletproof React and Connor's standards:
- Testing trophy distribution (70% integration, 20% unit, 10% E2E)
- 80%+ coverage requirement
- Semantic queries (getByRole preferred)
- User behavior testing (not implementation details)
- Test naming ("should X when Y")
"""

import json
import re
from pathlib import Path
from typing import Dict, List


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze testing strategy and quality.

    Args:
        codebase_path: Path to React codebase
        metadata: Project metadata from discovery phase

    Returns:
        List of findings with severity and migration guidance
    """
    findings = []

    tech_stack = metadata.get('tech_stack', {})
    src_dir = codebase_path / 'src'

    if not src_dir.exists():
        return findings

    # Check for testing framework
    findings.extend(check_testing_framework(tech_stack))

    # Check test coverage
    findings.extend(check_test_coverage(codebase_path))

    # Analyze test distribution (unit vs integration vs E2E)
    findings.extend(analyze_test_distribution(codebase_path))

    # Check test quality patterns
    findings.extend(check_test_quality(codebase_path))

    return findings


def check_testing_framework(tech_stack: Dict) -> List[Dict]:
    """Check for modern testing setup."""
    findings = []

    has_test_framework = tech_stack.get('vitest') or tech_stack.get('jest')
    has_testing_library = tech_stack.get('testing-library')

    if not has_test_framework:
        findings.append({
            'severity': 'critical',
            'category': 'testing',
            'title': 'No testing framework detected',
            'current_state': 'No Vitest or Jest found',
            'target_state': 'Use Vitest (modern, fast) or Jest for testing',
            'migration_steps': [
                'Install Vitest (recommended for Vite) or Jest',
                'Install @testing-library/react',
                'Configure test setup file',
                'Add test scripts to package.json',
                'Set up coverage reporting'
            ],
            'effort': 'medium',
        })

    if not has_testing_library:
        findings.append({
            'severity': 'high',
            'category': 'testing',
            'title': 'Testing Library not found',
            'current_state': 'No @testing-library/react detected',
            'target_state': 'Use Testing Library for user-centric testing',
            'migration_steps': [
                'Install @testing-library/react',
                'Install @testing-library/jest-dom for assertions',
                'Use render() and semantic queries (getByRole)',
                'Follow testing-library principles (test behavior, not implementation)'
            ],
            'effort': 'low',
        })

    return findings


def check_test_coverage(codebase_path: Path) -> List[Dict]:
    """Check test coverage if available."""
    findings = []

    # Look for coverage reports
    coverage_file = codebase_path / 'coverage' / 'coverage-summary.json'

    if coverage_file.exists():
        try:
            with open(coverage_file, 'r') as f:
                coverage_data = json.load(f)
                total_coverage = coverage_data.get('total', {})
                line_coverage = total_coverage.get('lines', {}).get('pct', 0)
                branch_coverage = total_coverage.get('branches', {}).get('pct', 0)

                if line_coverage < 80:
                    findings.append({
                        'severity': 'high',
                        'category': 'testing',
                        'title': f'Test coverage below 80% ({line_coverage:.1f}%)',
                        'current_state': f'Line coverage: {line_coverage:.1f}%, Branch coverage: {branch_coverage:.1f}%',
                        'target_state': 'Maintain 80%+ test coverage on all code',
                        'migration_steps': [
                            'Identify untested files and functions',
                            'Prioritize testing critical paths (authentication, payment, data processing)',
                            'Write integration tests first (70% of tests)',
                            'Add unit tests for complex business logic',
                            'Configure coverage thresholds in test config'
                        ],
                        'effort': 'high',
                    })
                elif line_coverage < 90:
                    findings.append({
                        'severity': 'medium',
                        'category': 'testing',
                        'title': f'Test coverage at {line_coverage:.1f}%',
                        'current_state': f'Coverage is good but could be excellent (current: {line_coverage:.1f}%)',
                        'target_state': 'Aim for 90%+ coverage for production-ready code',
                        'migration_steps': [
                            'Identify remaining untested code paths',
                            'Focus on edge cases and error handling',
                            'Ensure all critical features have 100% coverage'
                        ],
                        'effort': 'medium',
                    })
        except:
            pass
    else:
        findings.append({
            'severity': 'high',
            'category': 'testing',
            'title': 'No coverage report found',
            'current_state': 'Cannot find coverage/coverage-summary.json',
            'target_state': 'Generate coverage reports to track test coverage',
            'migration_steps': [
                'Configure coverage in vitest.config.ts or jest.config.js',
                'Add --coverage flag to test script',
                'Set coverage thresholds (lines: 80, branches: 75)',
                'Add coverage/ to .gitignore',
                'Review coverage reports regularly'
            ],
            'effort': 'low',
        })

    return findings


def analyze_test_distribution(codebase_path: Path) -> List[Dict]:
    """Analyze testing trophy distribution."""
    findings = []

    # Count test files by type
    unit_tests = 0
    integration_tests = 0
    e2e_tests = 0

    test_patterns = {
        'e2e': ['e2e/', '.e2e.test.', '.e2e.spec.', 'playwright/', 'cypress/'],
        'integration': ['.test.tsx', '.test.jsx', '.spec.tsx', '.spec.jsx'],  # Component tests
        'unit': ['.test.ts', '.test.js', '.spec.ts', '.spec.js'],  # Logic tests
    }

    for test_file in codebase_path.rglob('*.{test,spec}.{ts,tsx,js,jsx}'):
        test_path_str = str(test_file)

        # E2E tests
        if any(pattern in test_path_str for pattern in test_patterns['e2e']):
            e2e_tests += 1
        # Integration tests (component tests with TSX/JSX)
        elif any(pattern in test_path_str for pattern in test_patterns['integration']):
            integration_tests += 1
        # Unit tests (pure logic, no JSX)
        else:
            unit_tests += 1

    total_tests = unit_tests + integration_tests + e2e_tests

    if total_tests > 0:
        int_pct = (integration_tests / total_tests) * 100
        unit_pct = (unit_tests / total_tests) * 100
        e2e_pct = (e2e_tests / total_tests) * 100

        # Testing Trophy: 70% integration, 20% unit, 10% E2E
        if int_pct < 50:  # Should be ~70%
            findings.append({
                'severity': 'medium',
                'category': 'testing',
                'title': 'Testing pyramid instead of testing trophy',
                'current_state': f'Distribution: {int_pct:.0f}% integration, {unit_pct:.0f}% unit, {e2e_pct:.0f}% E2E',
                'target_state': 'Testing Trophy: 70% integration, 20% unit, 10% E2E',
                'migration_steps': [
                    'Write more integration tests (component + hooks + context)',
                    'Test user workflows, not implementation details',
                    'Reduce excessive unit tests of simple functions',
                    'Keep E2E tests for critical user journeys only',
                    'Use Testing Library for integration tests'
                ],
                'effort': 'medium',
            })

        if unit_pct > 40:  # Should be ~20%
            findings.append({
                'severity': 'low',
                'category': 'testing',
                'title': 'Too many unit tests',
                'current_state': f'{unit_pct:.0f}% unit tests (target: ~20%)',
                'target_state': 'Focus on integration tests that provide more confidence',
                'migration_steps': [
                    'Review unit tests - many could be integration tests',
                    'Combine related unit tests into integration tests',
                    'Keep unit tests only for complex business logic',
                    'Test components with their hooks and context'
                ],
                'effort': 'low',
            })

    return findings


def check_test_quality(codebase_path: Path) -> List[Dict]:
    """Check for test quality anti-patterns."""
    findings = []

    brittle_test_patterns = []
    bad_query_usage = []
    bad_naming = []

    for test_file in codebase_path.rglob('*.{test,spec}.{ts,tsx,js,jsx}'):
        try:
            with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Check for brittle tests (testing implementation)
                if 'getByTestId' in content:
                    bad_query_usage.append(str(test_file))

                # Check for testing exact counts (brittle)
                if re.search(r'expect\([^)]+\)\.toHaveLength\(\d+\)', content):
                    brittle_test_patterns.append(str(test_file))

                # Check test naming ("should X when Y")
                test_names = re.findall(r'(?:it|test)\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
                for name in test_names:
                    if not (name.startswith('should ') or 'when' in name.lower()):
                        bad_naming.append((str(test_file), name))
        except:
            pass

    if bad_query_usage:
        findings.append({
            'severity': 'medium',
            'category': 'testing',
            'title': f'Using getByTestId in {len(bad_query_usage)} test files',
            'current_state': 'Tests use getByTestId instead of semantic queries',
            'target_state': 'Use semantic queries: getByRole, getByLabelText, getByText',
            'migration_steps': [
                'Replace getByTestId with getByRole (most preferred)',
                'Use getByLabelText for form inputs',
                'Use getByText for user-visible content',
                'Only use getByTestId as last resort',
                'Add eslint-plugin-testing-library for enforcement'
            ],
            'effort': 'medium',
            'affected_files': bad_query_usage[:5],
        })

    if brittle_test_patterns:
        findings.append({
            'severity': 'low',
            'category': 'testing',
            'title': f'Brittle test patterns in {len(brittle_test_patterns)} files',
            'current_state': 'Tests check exact counts and DOM structure',
            'target_state': 'Test user behavior and outcomes, not exact DOM structure',
            'migration_steps': [
                'Avoid testing exact element counts',
                'Focus on user-visible behavior',
                'Test functionality, not implementation',
                'Allow flexibility in DOM structure'
            ],
            'effort': 'low',
        })

    if len(bad_naming) > 5:  # More than 5 tests with poor naming
        findings.append({
            'severity': 'low',
            'category': 'testing',
            'title': f'{len(bad_naming)} tests with unclear naming',
            'current_state': 'Test names don\'t follow "should X when Y" pattern',
            'target_state': 'Use descriptive names: "should display error when API fails"',
            'migration_steps': [
                'Rename tests to describe expected behavior',
                'Use pattern: "should [expected behavior] when [condition]"',
                'Make tests self-documenting',
                'Tests should read like requirements'
            ],
            'effort': 'low',
        })

    return findings
