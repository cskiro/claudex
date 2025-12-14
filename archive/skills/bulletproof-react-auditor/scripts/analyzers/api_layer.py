"""
API Layer Analyzer

Analyzes API organization against Bulletproof React patterns:
- Centralized API client
- Type-safe request declarations
- Colocated in features/
- Data fetching hooks
"""

from pathlib import Path
from typing import Dict, List
import re


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze API layer architecture."""
    findings = []
    src_dir = codebase_path / 'src'

    if not src_dir.exists():
        return findings

    # Check for centralized API client
    has_api_config = (src_dir / 'lib').exists() or any(src_dir.rglob('**/api-client.*'))
    if not has_api_config:
        findings.append({
            'severity': 'medium',
            'category': 'api',
            'title': 'No centralized API client detected',
            'current_state': 'No api-client configuration found in src/lib/',
            'target_state': 'Create single configured API client instance',
            'migration_steps': [
                'Create src/lib/api-client.ts with axios or fetch wrapper',
                'Configure base URL, headers, interceptors',
                'Export configured client',
                'Use in all API calls'
            ],
            'effort': 'low',
        })

    # Check for scattered fetch calls
    scattered_fetches = []
    for file in src_dir.rglob('*.{ts,tsx,js,jsx}'):
        if 'test' in str(file) or 'spec' in str(file):
            continue
        try:
            with open(file, 'r') as f:
                content = f.read()
                if re.search(r'\bfetch\s*\(', content) and 'api' not in str(file).lower():
                    scattered_fetches.append(str(file.relative_to(src_dir)))
        except:
            pass

    if len(scattered_fetches) > 3:
        findings.append({
            'severity': 'high',
            'category': 'api',
            'title': f'Scattered fetch calls in {len(scattered_fetches)} files',
            'current_state': 'fetch() calls throughout components',
            'target_state': 'Centralize API calls in feature api/ directories',
            'migration_steps': [
                'Create api/ directory in each feature',
                'Move API calls to dedicated functions',
                'Create custom hooks wrapping API calls',
                'Use React Query or SWR for data fetching'
            ],
            'effort': 'high',
            'affected_files': scattered_fetches[:5],
        })

    return findings
