"""
State Management Analyzer

Analyzes React state management against Bulletproof React principles:
- Appropriate tool for each state type (component, app, server, form, URL)
- State localized when possible
- Server cache separated (React Query/SWR)
- No global state overuse
"""

import json
import re
from pathlib import Path
from typing import Dict, List


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze state management patterns.

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

    # Check for appropriate state management tools
    findings.extend(check_state_management_tools(tech_stack))

    # Check for data fetching library (server cache state)
    findings.extend(check_data_fetching_library(tech_stack))

    # Check for form state management
    findings.extend(check_form_state_management(src_dir, tech_stack))

    # Check for potential state management issues
    findings.extend(check_state_patterns(src_dir))

    return findings


def check_state_management_tools(tech_stack: Dict) -> List[Dict]:
    """Check for presence of appropriate state management tools."""
    findings = []

    # Check if any global state management is present
    has_state_mgmt = any([
        tech_stack.get('redux'),
        tech_stack.get('zustand'),
        tech_stack.get('jotai'),
        tech_stack.get('mobx')
    ])

    # If app has many features but no state management, might need it
    # (This is a heuristic - could be Context-based which is fine)
    if not has_state_mgmt:
        findings.append({
            'severity': 'low',
            'category': 'state',
            'title': 'No explicit global state management detected',
            'current_state': 'No Redux, Zustand, Jotai, or MobX found',
            'target_state': 'Consider Zustand or Jotai for global state if Context becomes complex. Start with Context + hooks.',
            'migration_steps': [
                'Evaluate if Context API is sufficient for your needs',
                'If Context becomes complex, consider Zustand (simple) or Jotai (atomic)',
                'Avoid Redux unless you need its ecosystem (Redux Toolkit simplifies it)',
                'Keep state as local as possible before going global'
            ],
            'effort': 'low',
        })

    return findings


def check_data_fetching_library(tech_stack: Dict) -> List[Dict]:
    """Check for React Query, SWR, or similar for server state."""
    findings = []

    has_data_fetching = any([
        tech_stack.get('react-query'),
        tech_stack.get('swr'),
        tech_stack.get('apollo'),
        tech_stack.get('rtk-query')
    ])

    if not has_data_fetching:
        findings.append({
            'severity': 'high',
            'category': 'state',
            'title': 'No data fetching library detected',
            'current_state': 'No React Query, SWR, Apollo Client, or RTK Query found',
            'target_state': 'Use React Query or SWR for server state management (caching, refetching, optimistic updates)',
            'migration_steps': [
                'Install React Query (@tanstack/react-query) or SWR',
                'Wrap app with QueryClientProvider (React Query) or SWRConfig (SWR)',
                'Convert fetch calls to useQuery hooks',
                'Replace manual loading/error states with library patterns',
                'Add staleTime, cacheTime configurations as needed'
            ],
            'effort': 'medium',
        })

    return findings


def check_form_state_management(src_dir: Path, tech_stack: Dict) -> List[Dict]:
    """Check for form state management."""
    findings = []

    has_form_lib = any([
        tech_stack.get('react-hook-form'),
        tech_stack.get('formik')
    ])

    # Look for form components without form library
    if not has_form_lib:
        form_files = []
        for file_path in src_dir.rglob('*.{tsx,jsx}'):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Look for <form> tags
                    if re.search(r'<form[>\s]', content, re.IGNORECASE):
                        form_files.append(str(file_path.relative_to(src_dir)))
            except:
                pass

        if len(form_files) > 3:  # More than 3 forms suggests need for form library
            findings.append({
                'severity': 'medium',
                'category': 'state',
                'title': f'No form library but {len(form_files)} forms detected',
                'current_state': f'{len(form_files)} form components without React Hook Form or Formik',
                'target_state': 'Use React Hook Form for performant form state management',
                'migration_steps': [
                    'Install react-hook-form',
                    'Replace controlled form state with useForm() hook',
                    'Use register() for input registration',
                    'Handle validation with yup or zod schemas',
                    'Reduce re-renders with uncontrolled inputs'
                ],
                'effort': 'medium',
                'affected_files': form_files[:5],
            })

    return findings


def check_state_patterns(src_dir: Path) -> List[Dict]:
    """Check for common state management anti-patterns."""
    findings = []

    # Look for large Context providers (potential performance issue)
    large_contexts = []
    for file_path in src_dir.rglob('*.{tsx,jsx}'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Look for Context creation with many values
                if 'createContext' in content:
                    # Count useState hooks in the provider
                    state_count = len(re.findall(r'useState\s*\(', content))
                    if state_count > 5:
                        large_contexts.append({
                            'file': str(file_path.relative_to(src_dir)),
                            'state_count': state_count
                        })
        except:
            pass

    if large_contexts:
        for ctx in large_contexts:
            findings.append({
                'severity': 'medium',
                'category': 'state',
                'title': f'Large Context with {ctx["state_count"]} state values',
                'current_state': f'{ctx["file"]} has many state values in one Context',
                'target_state': 'Split large Contexts into smaller, focused Contexts to prevent unnecessary re-renders',
                'migration_steps': [
                    'Identify which state values change together',
                    'Create separate Contexts for independent state',
                    'Use Context composition for related state',
                    'Consider Zustand/Jotai for complex global state'
                ],
                'effort': 'medium',
                'file': ctx['file'],
            })

    return findings
