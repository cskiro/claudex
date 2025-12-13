"""
Project Structure Analyzer

Analyzes React project structure against Bulletproof React patterns:
- Feature-based organization (src/features/)
- Unidirectional dependencies (shared → features → app)
- No cross-feature imports
- Proper folder hierarchy
"""

import re
from pathlib import Path
from typing import Dict, List, Set


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze project structure for Bulletproof React compliance.

    Args:
        codebase_path: Path to React codebase
        metadata: Project metadata from discovery phase

    Returns:
        List of findings with severity and migration guidance
    """
    findings = []

    src_dir = codebase_path / 'src'
    if not src_dir.exists():
        findings.append({
            'severity': 'critical',
            'category': 'structure',
            'title': 'Missing src/ directory',
            'current_state': 'No src/ directory found',
            'target_state': 'All source code should be in src/ directory',
            'migration_steps': [
                'Create src/ directory',
                'Move all source files to src/',
                'Update import paths',
                'Update build configuration'
            ],
            'effort': 'medium',
        })
        return findings

    # Check for Bulletproof structure
    findings.extend(check_bulletproof_structure(src_dir))

    # Check for cross-feature imports
    findings.extend(check_cross_feature_imports(src_dir))

    # Analyze features/ organization
    findings.extend(analyze_features_directory(src_dir))

    # Check shared code organization
    findings.extend(check_shared_code_organization(src_dir))

    # Check for architectural violations
    findings.extend(check_architectural_violations(src_dir))

    return findings


def check_bulletproof_structure(src_dir: Path) -> List[Dict]:
    """Check for presence of Bulletproof React folder structure."""
    findings = []

    # Required top-level directories for Bulletproof React
    bulletproof_dirs = {
        'app': 'Application layer (routes, app.tsx, provider.tsx, router.tsx)',
        'features': 'Feature modules (80%+ of code should be here)',
    }

    # Recommended directories
    recommended_dirs = {
        'components': 'Shared components used across multiple features',
        'hooks': 'Shared custom hooks',
        'lib': 'Third-party library configurations',
        'utils': 'Shared utility functions',
        'types': 'Shared TypeScript types',
    }

    # Check required directories
    for dir_name, description in bulletproof_dirs.items():
        dir_path = src_dir / dir_name
        if not dir_path.exists():
            findings.append({
                'severity': 'critical' if dir_name == 'features' else 'high',
                'category': 'structure',
                'title': f'Missing {dir_name}/ directory',
                'current_state': f'No {dir_name}/ directory found',
                'target_state': f'{dir_name}/ directory should exist: {description}',
                'migration_steps': [
                    f'Create src/{dir_name}/ directory',
                    f'Organize code according to Bulletproof React {dir_name} pattern',
                    'Update imports to use new structure'
                ],
                'effort': 'high' if dir_name == 'features' else 'medium',
            })

    # Check recommended directories (lower severity)
    missing_recommended = []
    for dir_name, description in recommended_dirs.items():
        dir_path = src_dir / dir_name
        if not dir_path.exists():
            missing_recommended.append(f'{dir_name}/ ({description})')

    if missing_recommended:
        findings.append({
            'severity': 'medium',
            'category': 'structure',
            'title': 'Missing recommended directories',
            'current_state': f'Missing: {", ".join([d.split("/")[0] for d in missing_recommended])}',
            'target_state': 'Bulletproof React recommends these directories for shared code',
            'migration_steps': [
                'Create missing directories as needed',
                'Move shared code to appropriate directories',
                'Ensure proper separation between shared and feature-specific code'
            ],
            'effort': 'low',
        })

    return findings


def check_cross_feature_imports(src_dir: Path) -> List[Dict]:
    """Detect cross-feature imports (architectural violation)."""
    findings = []
    features_dir = src_dir / 'features'

    if not features_dir.exists():
        return findings

    # Get all feature directories
    feature_dirs = [d for d in features_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

    violations = []
    for feature_dir in feature_dirs:
        # Find all TypeScript/JavaScript files in this feature
        for file_path in feature_dir.rglob('*.{ts,tsx,js,jsx}'):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Check for imports from other features
                    import_pattern = re.compile(r'from\s+[\'"]([^\'\"]+)[\'"]')
                    imports = import_pattern.findall(content)

                    for imp in imports:
                        # Check if importing from another feature
                        if imp.startswith('../') or imp.startswith('@/features/'):
                            # Extract feature name from import path
                            if '@/features/' in imp:
                                imported_feature = imp.split('@/features/')[1].split('/')[0]
                            elif '../' in imp:
                                # Handle relative imports
                                parts = imp.split('/')
                                if 'features' in parts:
                                    idx = parts.index('features')
                                    if idx + 1 < len(parts):
                                        imported_feature = parts[idx + 1]
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                continue

                            # Check if importing from different feature
                            current_feature = feature_dir.name
                            if imported_feature != current_feature and imported_feature in [f.name for f in feature_dirs]:
                                violations.append({
                                    'file': str(file_path.relative_to(src_dir)),
                                    'from_feature': current_feature,
                                    'to_feature': imported_feature,
                                    'import': imp
                                })
            except:
                pass

    if violations:
        # Group violations by feature
        grouped = {}
        for v in violations:
            key = f"{v['from_feature']} → {v['to_feature']}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(v['file'])

        for import_path, files in grouped.items():
            findings.append({
                'severity': 'high',
                'category': 'structure',
                'title': f'Cross-feature import: {import_path}',
                'current_state': f'{len(files)} file(s) import from another feature',
                'target_state': 'Features should be independent. Shared code belongs in src/components/, src/hooks/, or src/utils/',
                'migration_steps': [
                    'Identify what code is being shared between features',
                    'Move truly shared code to src/components/, src/hooks/, or src/utils/',
                    'If code is feature-specific, duplicate it or refactor feature boundaries',
                    'Update imports to use shared code location'
                ],
                'effort': 'medium',
                'affected_files': files[:5],  # Show first 5 files
            })

    return findings


def analyze_features_directory(src_dir: Path) -> List[Dict]:
    """Analyze features/ directory structure."""
    findings = []
    features_dir = src_dir / 'features'

    if not features_dir.exists():
        return findings

    feature_dirs = [d for d in features_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

    if len(feature_dirs) == 0:
        findings.append({
            'severity': 'high',
            'category': 'structure',
            'title': 'Empty features/ directory',
            'current_state': 'features/ directory exists but contains no features',
            'target_state': '80%+ of application code should be organized in feature modules',
            'migration_steps': [
                'Identify distinct features in your application',
                'Create a directory for each feature in src/features/',
                'Move feature-specific code to appropriate feature directories',
                'Organize each feature with api/, components/, hooks/, stores/, types/, utils/ as needed'
            ],
            'effort': 'high',
        })
        return findings

    # Check each feature for proper internal structure
    for feature_dir in feature_dirs:
        feature_name = feature_dir.name

        # Recommended feature subdirectories
        feature_subdirs = ['api', 'components', 'hooks', 'stores', 'types', 'utils']
        has_subdirs = any((feature_dir / subdir).exists() for subdir in feature_subdirs)

        # Count files in feature root
        root_files = [f for f in feature_dir.iterdir() if f.is_file() and f.suffix in {'.ts', '.tsx', '.js', '.jsx'}]

        if len(root_files) > 5 and not has_subdirs:
            findings.append({
                'severity': 'medium',
                'category': 'structure',
                'title': f'Feature "{feature_name}" lacks internal organization',
                'current_state': f'{len(root_files)} files in feature root without subdirectories',
                'target_state': 'Features should be organized with api/, components/, hooks/, stores/, types/, utils/ subdirectories',
                'migration_steps': [
                    f'Create subdirectories in src/features/{feature_name}/',
                    'Move API calls to api/',
                    'Move components to components/',
                    'Move hooks to hooks/',
                    'Move types to types/',
                    'Move utilities to utils/'
                ],
                'effort': 'low',
            })

    return findings


def check_shared_code_organization(src_dir: Path) -> List[Dict]:
    """Check if shared code is properly organized."""
    findings = []

    components_dir = src_dir / 'components'
    features_dir = src_dir / 'features'

    if not components_dir.exists():
        return findings

    # Count components
    shared_components = list(components_dir.rglob('*.{tsx,jsx}'))
    shared_count = len(shared_components)

    # Count feature components
    feature_count = 0
    if features_dir.exists():
        feature_count = len(list(features_dir.rglob('**/components/**/*.{tsx,jsx}')))

    total_components = shared_count + feature_count

    if total_components > 0:
        shared_percentage = (shared_count / total_components) * 100

        # Bulletproof React recommends 80%+ code in features
        if shared_percentage > 40:
            findings.append({
                'severity': 'medium',
                'category': 'structure',
                'title': 'Too many shared components',
                'current_state': f'{shared_percentage:.1f}% of components are in src/components/ (shared)',
                'target_state': 'Most components should be feature-specific. Only truly shared components belong in src/components/',
                'migration_steps': [
                    'Review each component in src/components/',
                    'Identify components used by only one feature',
                    'Move feature-specific components to their feature directories',
                    'Keep only truly shared components in src/components/'
                ],
                'effort': 'medium',
            })

    return findings


def check_architectural_violations(src_dir: Path) -> List[Dict]:
    """Check for common architectural violations."""
    findings = []

    # Check for business logic in components/
    components_dir = src_dir / 'components'
    if components_dir.exists():
        large_components = []
        for component_file in components_dir.rglob('*.{tsx,jsx}'):
            try:
                with open(component_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
                    if lines > 200:
                        large_components.append((str(component_file.relative_to(src_dir)), lines))
            except:
                pass

        if large_components:
            findings.append({
                'severity': 'medium',
                'category': 'structure',
                'title': 'Large components in shared components/',
                'current_state': f'{len(large_components)} component(s) > 200 lines in src/components/',
                'target_state': 'Shared components should be simple and reusable. Complex components likely belong in features/',
                'migration_steps': [
                    'Review large shared components',
                    'Extract business logic to feature-specific hooks or utilities',
                    'Consider moving complex components to features/ if feature-specific',
                    'Keep shared components simple and focused'
                ],
                'effort': 'medium',
                'affected_files': [f[0] for f in large_components[:5]],
            })

    # Check for proper app/ structure
    app_dir = src_dir / 'app'
    if app_dir.exists():
        expected_app_files = ['app.tsx', 'provider.tsx', 'router.tsx']
        has_routing = any((app_dir / f).exists() or (app_dir / 'routes').exists() for f in ['router.tsx', 'routes.tsx'])

        if not has_routing:
            findings.append({
                'severity': 'low',
                'category': 'structure',
                'title': 'Missing routing configuration in app/',
                'current_state': 'No router.tsx or routes/ found in src/app/',
                'target_state': 'Bulletproof React recommends centralizing routing in src/app/router.tsx or src/app/routes/',
                'migration_steps': [
                    'Create src/app/router.tsx or src/app/routes/',
                    'Define all application routes in one place',
                    'Use code splitting for route-level lazy loading'
                ],
                'effort': 'low',
            })

    return findings
