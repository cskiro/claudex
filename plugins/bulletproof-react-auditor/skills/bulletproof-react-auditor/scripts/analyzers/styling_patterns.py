"""
Styling Patterns Analyzer

Analyzes styling approach against Bulletproof React:
- Consistent styling method
- Component library usage
- Colocated styles
"""

from pathlib import Path
from typing import Dict, List


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze styling patterns."""
    findings = []
    tech_stack = metadata.get('tech_stack', {})

    # Check for styling approach
    styling_tools = []
    if tech_stack.get('tailwind'): styling_tools.append('Tailwind CSS')
    if tech_stack.get('styled-components'): styling_tools.append('styled-components')
    if tech_stack.get('emotion'): styling_tools.append('Emotion')
    if tech_stack.get('chakra-ui'): styling_tools.append('Chakra UI')
    if tech_stack.get('mui'): styling_tools.append('Material UI')
    if tech_stack.get('radix-ui'): styling_tools.append('Radix UI')

    if not styling_tools:
        findings.append({
            'severity': 'low',
            'category': 'styling',
            'title': 'No component library or utility CSS detected',
            'current_state': 'No Tailwind, Chakra UI, Radix UI, or other styling system',
            'target_state': 'Use component library (Chakra, Radix) or utility CSS (Tailwind)',
            'migration_steps': [
                'Choose styling approach based on needs',
                'Install Tailwind CSS (utility-first) or Chakra UI (component library)',
                'Configure theme and design tokens',
                'Migrate components gradually'
            ],
            'effort': 'medium',
        })
    elif len(styling_tools) > 2:
        findings.append({
            'severity': 'medium',
            'category': 'styling',
            'title': f'Multiple styling approaches ({len(styling_tools)})',
            'current_state': f'Using: {", ".join(styling_tools)}',
            'target_state': 'Standardize on single styling approach',
            'migration_steps': [
                'Choose primary styling system',
                'Create migration plan',
                'Update style guide',
                'Refactor components incrementally'
            ],
            'effort': 'high',
        })

    return findings
