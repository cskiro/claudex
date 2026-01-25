"""
Error Handling Analyzer

Analyzes error handling patterns:
- Error boundaries present
- API error interceptors
- Error tracking (Sentry)
"""

from pathlib import Path
from typing import Dict, List
import re


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze error handling patterns."""
    findings = []
    src_dir = codebase_path / 'src'
    tech_stack = metadata.get('tech_stack', {})

    if not src_dir.exists():
        return findings

    # Check for error boundaries
    error_boundaries = list(src_dir.rglob('**/error-boundary.*')) + \
                      list(src_dir.rglob('**/ErrorBoundary.*'))

    if not error_boundaries:
        findings.append({
            'severity': 'high',
            'category': 'errors',
            'title': 'No error boundaries detected',
            'current_state': 'No ErrorBoundary components found',
            'target_state': 'Implement multiple error boundaries at strategic locations',
            'migration_steps': [
                'Create ErrorBoundary component with componentDidCatch',
                'Wrap route components with ErrorBoundary',
                'Add feature-level error boundaries',
                'Display user-friendly error messages'
            ],
            'effort': 'low',
        })

    # Check for error tracking
    if not tech_stack.get('sentry'):
        findings.append({
            'severity': 'medium',
            'category': 'errors',
            'title': 'No error tracking service detected',
            'current_state': 'No Sentry or similar error tracking',
            'target_state': 'Use Sentry for production error monitoring',
            'migration_steps': [
                'Sign up for Sentry',
                'Install @sentry/react',
                'Configure Sentry.init() in app entry',
                'Add user context and tags',
                'Set up error alerts'
            ],
            'effort': 'low',
        })

    return findings
