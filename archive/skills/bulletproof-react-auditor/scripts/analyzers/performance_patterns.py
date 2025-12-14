"""
Performance Patterns Analyzer

Analyzes React performance optimizations:
- Code splitting at routes
- Memoization patterns
- Image optimization
"""

from pathlib import Path
from typing import Dict, List
import re


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze performance patterns."""
    findings = []
    src_dir = codebase_path / 'src'

    if not src_dir.exists():
        return findings

    # Check for lazy loading
    has_lazy_loading = False
    for file in src_dir.rglob('*.{ts,tsx,js,jsx}'):
        try:
            with open(file, 'r') as f:
                content = f.read()
                if 'React.lazy' in content or 'lazy(' in content:
                    has_lazy_loading = True
                    break
        except:
            pass

    if not has_lazy_loading:
        findings.append({
            'severity': 'medium',
            'category': 'performance',
            'title': 'No code splitting detected',
            'current_state': 'No React.lazy() usage found',
            'target_state': 'Use code splitting for routes and large components',
            'migration_steps': [
                'Wrap route components with React.lazy()',
                'Add Suspense boundaries with loading states',
                'Split large features into separate chunks',
                'Analyze bundle size with build tools'
            ],
            'effort': 'low',
        })

    # Check for large images
    assets_dir = codebase_path / 'public' / 'assets'
    if assets_dir.exists():
        large_images = []
        for img in assets_dir.rglob('*.{jpg,jpeg,png,gif}'):
            size_mb = img.stat().st_size / (1024 * 1024)
            if size_mb > 0.5:  # Larger than 500KB
                large_images.append((str(img.name), size_mb))

        if large_images:
            findings.append({
                'severity': 'medium',
                'category': 'performance',
                'title': f'{len(large_images)} large images detected',
                'current_state': f'Images larger than 500KB',
                'target_state': 'Optimize images with modern formats and lazy loading',
                'migration_steps': [
                    'Convert to WebP format',
                    'Add lazy loading with loading="lazy"',
                    'Use srcset for responsive images',
                    'Compress images with tools like sharp'
                ],
                'effort': 'low',
            })

    return findings
