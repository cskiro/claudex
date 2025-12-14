"""
Component Architecture Analyzer

Analyzes React component design against Bulletproof React principles:
- Component colocation (near where they're used)
- Limited props (< 7-10)
- Reasonable component size (< 300 LOC)
- No nested render functions
- Proper composition over excessive props
- Consistent naming (kebab-case files)
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze component architecture for Bulletproof React compliance.

    Args:
        codebase_path: Path to React codebase
        metadata: Project metadata from discovery phase

    Returns:
        List of findings with severity and migration guidance
    """
    findings = []

    src_dir = codebase_path / 'src'
    if not src_dir.exists():
        return findings

    # Analyze all React component files
    findings.extend(check_component_sizes(src_dir))
    findings.extend(check_component_props(src_dir))
    findings.extend(check_nested_render_functions(src_dir))
    findings.extend(check_file_naming_conventions(src_dir))
    findings.extend(check_component_colocation(src_dir))

    return findings


def check_component_sizes(src_dir: Path) -> List[Dict]:
    """Check for overly large components."""
    findings = []
    exclude_dirs = {'node_modules', 'dist', 'build', '.next', 'coverage'}

    large_components = []
    for component_file in src_dir.rglob('*.{tsx,jsx}'):
        if any(excluded in component_file.parts for excluded in exclude_dirs):
            continue

        try:
            with open(component_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                loc = len([line for line in lines if line.strip() and not line.strip().startswith('//')])

                if loc > 300:
                    large_components.append({
                        'file': str(component_file.relative_to(src_dir)),
                        'lines': loc,
                        'severity': 'critical' if loc > 500 else 'high' if loc > 400 else 'medium'
                    })
        except:
            pass

    if large_components:
        # Report the worst offenders
        large_components.sort(key=lambda x: x['lines'], reverse=True)

        for comp in large_components[:10]:  # Top 10 largest
            findings.append({
                'severity': comp['severity'],
                'category': 'components',
                'title': f'Large component ({comp["lines"]} LOC)',
                'current_state': f'{comp["file"]} has {comp["lines"]} lines',
                'target_state': 'Components should be < 300 lines. Large components are hard to understand and test.',
                'migration_steps': [
                    'Identify distinct responsibilities in the component',
                    'Extract smaller components for each UI section',
                    'Move business logic to custom hooks',
                    'Extract complex rendering logic to separate components',
                    'Consider splitting into multiple feature components'
                ],
                'effort': 'high' if comp['lines'] > 400 else 'medium',
                'file': comp['file'],
            })

    return findings


def check_component_props(src_dir: Path) -> List[Dict]:
    """Check for components with excessive props."""
    findings = []
    exclude_dirs = {'node_modules', 'dist', 'build', '.next', 'coverage'}

    components_with_many_props = []
    for component_file in src_dir.rglob('*.{tsx,jsx}'):
        if any(excluded in component_file.parts for excluded in exclude_dirs):
            continue

        try:
            with open(component_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Find component definitions with props
                # Pattern matches: function Component({ prop1, prop2, ... })
                # and: const Component = ({ prop1, prop2, ... }) =>
                props_pattern = re.compile(
                    r'(?:function|const)\s+(\w+)\s*(?:=\s*)?\(\s*\{([^}]+)\}',
                    re.MULTILINE
                )

                matches = props_pattern.findall(content)
                for component_name, props_str in matches:
                    # Count props (split by comma)
                    props = [p.strip() for p in props_str.split(',') if p.strip()]
                    # Filter out destructured nested props
                    actual_props = [p for p in props if not p.startswith('...')]
                    prop_count = len(actual_props)

                    if prop_count > 10:
                        components_with_many_props.append({
                            'file': str(component_file.relative_to(src_dir)),
                            'component': component_name,
                            'prop_count': prop_count,
                        })
        except:
            pass

    if components_with_many_props:
        for comp in components_with_many_props:
            findings.append({
                'severity': 'critical' if comp['prop_count'] > 15 else 'high',
                'category': 'components',
                'title': f'Component with {comp["prop_count"]} props: {comp["component"]}',
                'current_state': f'{comp["file"]} has {comp["prop_count"]} props',
                'target_state': 'Components should accept < 7-10 props. Too many props indicates insufficient composition.',
                'migration_steps': [
                    'Group related props into configuration objects',
                    'Use composition (children prop) instead of render props',
                    'Extract sub-components with their own props',
                    'Consider using Context for deeply shared state',
                    'Use compound component pattern for complex UIs'
                ],
                'effort': 'medium',
                'file': comp['file'],
            })

    return findings


def check_nested_render_functions(src_dir: Path) -> List[Dict]:
    """Check for nested render functions inside components."""
    findings = []
    exclude_dirs = {'node_modules', 'dist', 'build', '.next', 'coverage'}

    nested_render_functions = []
    for component_file in src_dir.rglob('*.{tsx,jsx}'):
        if any(excluded in component_file.parts for excluded in exclude_dirs):
            continue

        try:
            with open(component_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

                # Look for patterns like: const renderSomething = () => { ... }
                # or: function renderSomething() { ... }
                nested_render_pattern = re.compile(r'(?:const|function)\s+(render\w+)\s*[=:]?\s*\([^)]*\)\s*(?:=>)?\s*\{')

                for line_num, line in enumerate(lines, start=1):
                    if nested_render_pattern.search(line):
                        nested_render_functions.append({
                            'file': str(component_file.relative_to(src_dir)),
                            'line': line_num,
                        })
        except:
            pass

    if nested_render_functions:
        # Group by file
        files_with_nested = {}
        for item in nested_render_functions:
            file = item['file']
            if file not in files_with_nested:
                files_with_nested[file] = []
            files_with_nested[file].append(item['line'])

        for file, lines in files_with_nested.items():
            findings.append({
                'severity': 'medium',
                'category': 'components',
                'title': f'Nested render functions detected ({len(lines)} instances)',
                'current_state': f'{file} contains render functions inside component',
                'target_state': 'Extract nested render functions into separate components for better reusability and testing.',
                'migration_steps': [
                    'Identify each render function and its dependencies',
                    'Extract to separate component file',
                    'Pass necessary props to new component',
                    'Update tests to test new component in isolation',
                    'Remove render function from parent component'
                ],
                'effort': 'low',
                'file': file,
                'affected_lines': lines[:5],  # Show first 5
            })

    return findings


def check_file_naming_conventions(src_dir: Path) -> List[Dict]:
    """Check for consistent kebab-case file naming."""
    findings = []
    exclude_dirs = {'node_modules', 'dist', 'build', '.next', 'coverage'}

    non_kebab_files = []
    for file_path in src_dir.rglob('*.{ts,tsx,js,jsx}'):
        if any(excluded in file_path.parts for excluded in exclude_dirs):
            continue

        filename = file_path.stem  # filename without extension

        # Check if filename is kebab-case (lowercase with hyphens)
        # Allow: kebab-case.tsx, lowercase.tsx
        # Disallow: PascalCase.tsx, camelCase.tsx, snake_case.tsx
        is_kebab_or_lowercase = re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', filename)

        if not is_kebab_or_lowercase and filename not in ['index', 'App']:  # Allow common exceptions
            non_kebab_files.append(str(file_path.relative_to(src_dir)))

    if len(non_kebab_files) > 5:  # Only report if it's a pattern (>5 files)
        findings.append({
            'severity': 'low',
            'category': 'components',
            'title': f'Inconsistent file naming ({len(non_kebab_files)} files)',
            'current_state': f'{len(non_kebab_files)} files not using kebab-case naming',
            'target_state': 'Bulletproof React recommends kebab-case for all files (e.g., user-profile.tsx)',
            'migration_steps': [
                'Rename files to kebab-case format',
                'Update all import statements',
                'Run tests to ensure nothing broke',
                'Add ESLint rule to enforce kebab-case (unicorn/filename-case)'
            ],
            'effort': 'low',
            'affected_files': non_kebab_files[:10],  # Show first 10
        })

    return findings


def check_component_colocation(src_dir: Path) -> List[Dict]:
    """Check if components are colocated near where they're used."""
    findings = []

    components_dir = src_dir / 'components'
    if not components_dir.exists():
        return findings

    # Find components in shared components/ that are only used once
    single_use_components = []
    for component_file in components_dir.rglob('*.{tsx,jsx}'):
        try:
            component_name = component_file.stem

            # Search for imports of this component across codebase
            import_pattern = re.compile(rf'import.*{component_name}.*from.*[\'"]/|@/')
            usage_count = 0
            used_in_feature = None

            for search_file in src_dir.rglob('*.{ts,tsx,js,jsx}'):
                if search_file == component_file:
                    continue

                try:
                    with open(search_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if import_pattern.search(content):
                            usage_count += 1

                            # Check if used in a feature
                            if 'features' in search_file.parts:
                                features_index = search_file.parts.index('features')
                                if features_index + 1 < len(search_file.parts):
                                    feature_name = search_file.parts[features_index + 1]
                                    if used_in_feature is None:
                                        used_in_feature = feature_name
                                    elif used_in_feature != feature_name:
                                        used_in_feature = 'multiple'
                except:
                    pass

            # If used only in one feature, it should be colocated there
            if usage_count == 1 and used_in_feature and used_in_feature != 'multiple':
                single_use_components.append({
                    'file': str(component_file.relative_to(src_dir)),
                    'component': component_name,
                    'feature': used_in_feature,
                })
        except:
            pass

    if single_use_components:
        for comp in single_use_components[:5]:  # Top 5
            findings.append({
                'severity': 'low',
                'category': 'components',
                'title': f'Component used in only one feature: {comp["component"]}',
                'current_state': f'{comp["file"]} is in shared components/ but only used in {comp["feature"]} feature',
                'target_state': 'Components used by only one feature should be colocated in that feature directory.',
                'migration_steps': [
                    f'Move {comp["file"]} to src/features/{comp["feature"]}/components/',
                    'Update import in the feature',
                    'Run tests to verify',
                    'Remove from shared components/'
                ],
                'effort': 'low',
                'file': comp['file'],
            })

    return findings
