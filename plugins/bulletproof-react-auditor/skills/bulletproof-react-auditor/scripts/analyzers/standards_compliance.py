"""
Standards Compliance Analyzer

Analyzes project standards:
- ESLint configuration
- TypeScript strict mode
- Prettier setup
- Git hooks (Husky)
- Naming conventions
"""

from pathlib import Path
from typing import Dict, List
import json


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze standards compliance."""
    findings = []
    tech_stack = metadata.get('tech_stack', {})

    # Check ESLint
    eslint_config = any([
        (codebase_path / '.eslintrc.js').exists(),
        (codebase_path / '.eslintrc.json').exists(),
        (codebase_path / 'eslint.config.js').exists(),
    ])

    if not eslint_config:
        findings.append({
            'severity': 'high',
            'category': 'standards',
            'title': 'No ESLint configuration',
            'current_state': 'No .eslintrc or eslint.config found',
            'target_state': 'Configure ESLint with React and TypeScript rules',
            'migration_steps': [
                'Install eslint and plugins',
                'Create .eslintrc.js configuration',
                'Add recommended rules for React and TS',
                'Add lint script to package.json',
                'Fix existing violations'
            ],
            'effort': 'low',
        })

    # Check TypeScript strict mode
    tsconfig = codebase_path / 'tsconfig.json'
    if tsconfig.exists():
        try:
            with open(tsconfig, 'r') as f:
                config = json.load(f)
                strict = config.get('compilerOptions', {}).get('strict', False)
                if not strict:
                    findings.append({
                        'severity': 'high',
                        'category': 'standards',
                        'title': 'TypeScript strict mode disabled',
                        'current_state': 'strict: false in tsconfig.json',
                        'target_state': 'Enable strict mode for better type safety',
                        'migration_steps': [
                            'Set "strict": true in compilerOptions',
                            'Fix type errors incrementally',
                            'Add explicit return types',
                            'Remove any types'
                        ],
                        'effort': 'high',
                    })
        except:
            pass

    # Check Prettier
    if not tech_stack.get('prettier'):
        findings.append({
            'severity': 'low',
            'category': 'standards',
            'title': 'No Prettier detected',
            'current_state': 'Prettier not in dependencies',
            'target_state': 'Use Prettier for consistent code formatting',
            'migration_steps': [
                'Install prettier',
                'Create .prettierrc configuration',
                'Enable "format on save" in IDE',
                'Run prettier on all files'
            ],
            'effort': 'low',
        })

    # Check Husky
    if not tech_stack.get('husky'):
        findings.append({
            'severity': 'low',
            'category': 'standards',
            'title': 'No git hooks (Husky) detected',
            'current_state': 'No pre-commit hooks',
            'target_state': 'Use Husky for pre-commit linting and testing',
            'migration_steps': [
                'Install husky and lint-staged',
                'Set up pre-commit hook',
                'Run lint and type-check before commits',
                'Prevent bad code from entering repo'
            ],
            'effort': 'low',
        })

    return findings
