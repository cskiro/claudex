"""
Code Quality Analyzer

Analyzes code for:
- Cyclomatic complexity
- Code duplication
- Code smells
- File/function length
- Language-specific issues (TypeScript/JavaScript)
"""

import re
from pathlib import Path
from typing import Dict, List


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze codebase for code quality issues.

    Args:
        codebase_path: Path to codebase
        metadata: Project metadata from discovery phase

    Returns:
        List of findings with severity, location, and remediation info
    """
    findings = []

    # Determine which languages to analyze
    tech_stack = metadata.get('tech_stack', {})

    if tech_stack.get('javascript') or tech_stack.get('typescript'):
        findings.extend(analyze_javascript_typescript(codebase_path))

    if tech_stack.get('python'):
        findings.extend(analyze_python(codebase_path))

    # General analysis (language-agnostic)
    findings.extend(analyze_file_sizes(codebase_path))
    findings.extend(analyze_dead_code(codebase_path, tech_stack))

    return findings


def analyze_javascript_typescript(codebase_path: Path) -> List[Dict]:
    """Analyze JavaScript/TypeScript specific quality issues."""
    findings = []
    extensions = {'.js', '.jsx', '.ts', '.tsx'}
    exclude_dirs = {'node_modules', '.git', 'dist', 'build', '.next', 'coverage'}

    for file_path in codebase_path.rglob('*'):
        if (file_path.suffix in extensions and
            not any(excluded in file_path.parts for excluded in exclude_dirs)):

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                    # Check for TypeScript 'any' type
                    if file_path.suffix in {'.ts', '.tsx'}:
                        findings.extend(check_any_usage(file_path, content, lines))

                    # Check for 'var' keyword
                    findings.extend(check_var_usage(file_path, content, lines))

                    # Check for console.log statements
                    findings.extend(check_console_log(file_path, content, lines))

                    # Check for loose equality
                    findings.extend(check_loose_equality(file_path, content, lines))

                    # Check cyclomatic complexity (simplified)
                    findings.extend(check_complexity(file_path, content, lines))

                    # Check function length
                    findings.extend(check_function_length(file_path, content, lines))

            except Exception as e:
                # Skip files that can't be read
                pass

    return findings


def check_any_usage(file_path: Path, content: str, lines: List[str]) -> List[Dict]:
    """Check for TypeScript 'any' type usage."""
    findings = []

    # Pattern to match 'any' type (excluding comments)
    any_pattern = re.compile(r':\s*any\b|<any>|Array<any>|\bany\[\]')

    for line_num, line in enumerate(lines, start=1):
        # Skip comments
        if line.strip().startswith('//') or line.strip().startswith('/*') or line.strip().startswith('*'):
            continue

        if any_pattern.search(line):
            findings.append({
                'severity': 'medium',
                'category': 'code_quality',
                'subcategory': 'typescript_strict_mode',
                'title': "Use of 'any' type violates TypeScript strict mode",
                'description': f"Found 'any' type on line {line_num}",
                'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                'line': line_num,
                'code_snippet': line.strip(),
                'impact': 'Reduces type safety and defeats the purpose of TypeScript',
                'remediation': 'Replace "any" with specific types or use "unknown" with type guards',
                'effort': 'low',
            })

    return findings


def check_var_usage(file_path: Path, content: str, lines: List[str]) -> List[Dict]:
    """Check for 'var' keyword usage."""
    findings = []

    var_pattern = re.compile(r'\bvar\s+\w+')

    for line_num, line in enumerate(lines, start=1):
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            continue

        if var_pattern.search(line):
            findings.append({
                'severity': 'low',
                'category': 'code_quality',
                'subcategory': 'modern_javascript',
                'title': "Use of 'var' keyword is deprecated",
                'description': f"Found 'var' keyword on line {line_num}",
                'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                'line': line_num,
                'code_snippet': line.strip(),
                'impact': 'Function-scoped variables can lead to bugs; block-scoped (let/const) is preferred',
                'remediation': "Replace 'var' with 'const' (for values that don't change) or 'let' (for values that change)",
                'effort': 'low',
            })

    return findings


def check_console_log(file_path: Path, content: str, lines: List[str]) -> List[Dict]:
    """Check for console.log statements in production code."""
    findings = []

    # Skip if it's in a test file
    if 'test' in file_path.name or 'spec' in file_path.name or '__tests__' in str(file_path):
        return findings

    console_pattern = re.compile(r'\bconsole\.(log|debug|info|warn|error)\(')

    for line_num, line in enumerate(lines, start=1):
        if line.strip().startswith('//'):
            continue

        if console_pattern.search(line):
            findings.append({
                'severity': 'medium',
                'category': 'code_quality',
                'subcategory': 'production_code',
                'title': 'Console statement in production code',
                'description': f"Found console statement on line {line_num}",
                'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                'line': line_num,
                'code_snippet': line.strip(),
                'impact': 'Console statements should not be in production code; use proper logging',
                'remediation': 'Remove console statement or replace with proper logging framework',
                'effort': 'low',
            })

    return findings


def check_loose_equality(file_path: Path, content: str, lines: List[str]) -> List[Dict]:
    """Check for loose equality operators (== instead of ===)."""
    findings = []

    loose_eq_pattern = re.compile(r'[^!<>]==[^=]|[^!<>]!=[^=]')

    for line_num, line in enumerate(lines, start=1):
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            continue

        if loose_eq_pattern.search(line):
            findings.append({
                'severity': 'low',
                'category': 'code_quality',
                'subcategory': 'code_smell',
                'title': 'Loose equality operator used',
                'description': f"Found '==' or '!=' on line {line_num}, should use '===' or '!=='",
                'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                'line': line_num,
                'code_snippet': line.strip(),
                'impact': 'Loose equality can lead to unexpected type coercion bugs',
                'remediation': "Replace '==' with '===' and '!=' with '!=='",
                'effort': 'low',
            })

    return findings


def check_complexity(file_path: Path, content: str, lines: List[str]) -> List[Dict]:
    """
    Check cyclomatic complexity (simplified).

    Counts decision points: if, else, while, for, case, catch, &&, ||, ?
    """
    findings = []

    # Find function declarations
    func_pattern = re.compile(r'(function\s+\w+|const\s+\w+\s*=\s*\([^)]*\)\s*=>|\w+\s*\([^)]*\)\s*{)')

    current_function = None
    current_function_line = 0
    brace_depth = 0
    complexity = 0

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track braces to find function boundaries
        brace_depth += stripped.count('{') - stripped.count('}')

        # New function started
        if func_pattern.search(line) and brace_depth >= 1:
            # Save previous function if exists
            if current_function and complexity > 10:
                severity = 'critical' if complexity > 20 else 'high' if complexity > 15 else 'medium'
                findings.append({
                    'severity': severity,
                    'category': 'code_quality',
                    'subcategory': 'complexity',
                    'title': f'High cyclomatic complexity ({complexity})',
                    'description': f'Function has complexity of {complexity}',
                    'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                    'line': current_function_line,
                    'code_snippet': current_function,
                    'impact': 'High complexity makes code difficult to understand, test, and maintain',
                    'remediation': 'Refactor into smaller functions, extract complex conditions',
                    'effort': 'medium' if complexity < 20 else 'high',
                })

            # Start new function
            current_function = stripped
            current_function_line = line_num
            complexity = 1  # Base complexity

        # Count complexity contributors
        if current_function:
            complexity += stripped.count('if ')
            complexity += stripped.count('else if')
            complexity += stripped.count('while ')
            complexity += stripped.count('for ')
            complexity += stripped.count('case ')
            complexity += stripped.count('catch ')
            complexity += stripped.count('&&')
            complexity += stripped.count('||')
            complexity += stripped.count('?')

    return findings


def check_function_length(file_path: Path, content: str, lines: List[str]) -> List[Dict]:
    """Check for overly long functions."""
    findings = []

    func_pattern = re.compile(r'(function\s+\w+|const\s+\w+\s*=\s*\([^)]*\)\s*=>|\w+\s*\([^)]*\)\s*{)')

    current_function = None
    current_function_line = 0
    function_lines = 0
    brace_depth = 0

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        if func_pattern.search(line):
            # Check previous function
            if current_function and function_lines > 50:
                severity = 'high' if function_lines > 100 else 'medium'
                findings.append({
                    'severity': severity,
                    'category': 'code_quality',
                    'subcategory': 'function_length',
                    'title': f'Long function ({function_lines} lines)',
                    'description': f'Function is {function_lines} lines long (recommended: < 50)',
                    'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                    'line': current_function_line,
                    'code_snippet': current_function,
                    'impact': 'Long functions are harder to understand, test, and maintain',
                    'remediation': 'Extract smaller functions for distinct responsibilities',
                    'effort': 'medium',
                })

            current_function = stripped
            current_function_line = line_num
            function_lines = 0
            brace_depth = 0

        if current_function:
            function_lines += 1
            brace_depth += stripped.count('{') - stripped.count('}')

            if brace_depth == 0 and function_lines > 1:
                # Function ended
                current_function = None

    return findings


def analyze_python(codebase_path: Path) -> List[Dict]:
    """Analyze Python-specific quality issues."""
    findings = []
    # Python analysis to be implemented
    # Would check: PEP 8 violations, complexity, type hints, etc.
    return findings


def analyze_file_sizes(codebase_path: Path) -> List[Dict]:
    """Check for overly large files."""
    findings = []
    exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__'}
    code_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', '.rs'}

    for file_path in codebase_path.rglob('*'):
        if (file_path.is_file() and
            file_path.suffix in code_extensions and
            not any(excluded in file_path.parts for excluded in exclude_dirs)):

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())

                    if lines > 500:
                        severity = 'high' if lines > 1000 else 'medium'
                        findings.append({
                            'severity': severity,
                            'category': 'code_quality',
                            'subcategory': 'file_length',
                            'title': f'Large file ({lines} lines)',
                            'description': f'File has {lines} lines (recommended: < 500)',
                            'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                            'line': 1,
                            'code_snippet': None,
                            'impact': 'Large files are difficult to navigate and understand',
                            'remediation': 'Split into multiple smaller, focused modules',
                            'effort': 'high',
                        })
            except:
                pass

    return findings


def analyze_dead_code(codebase_path: Path, tech_stack: Dict) -> List[Dict]:
    """Detect potential dead code (commented-out code blocks)."""
    findings = []
    exclude_dirs = {'node_modules', '.git', 'dist', 'build'}

    extensions = set()
    if tech_stack.get('javascript') or tech_stack.get('typescript'):
        extensions.update({'.js', '.jsx', '.ts', '.tsx'})
    if tech_stack.get('python'):
        extensions.add('.py')

    for file_path in codebase_path.rglob('*'):
        if (file_path.suffix in extensions and
            not any(excluded in file_path.parts for excluded in exclude_dirs)):

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                    # Count consecutive commented lines with code-like content
                    comment_block_size = 0
                    block_start_line = 0

                    for line_num, line in enumerate(lines, start=1):
                        stripped = line.strip()

                        # Check if line is commented code
                        if (stripped.startswith('//') and
                            any(keyword in stripped for keyword in ['function', 'const', 'let', 'var', 'if', 'for', 'while', '{', '}', ';'])):
                            if comment_block_size == 0:
                                block_start_line = line_num
                            comment_block_size += 1
                        else:
                            # End of comment block
                            if comment_block_size >= 5:  # 5+ lines of commented code
                                findings.append({
                                    'severity': 'low',
                                    'category': 'code_quality',
                                    'subcategory': 'dead_code',
                                    'title': f'Commented-out code block ({comment_block_size} lines)',
                                    'description': f'Found {comment_block_size} lines of commented code',
                                    'file': str(file_path.relative_to(file_path.parents[len(file_path.parts) - file_path.parts.index('annex') - 2])),
                                    'line': block_start_line,
                                    'code_snippet': None,
                                    'impact': 'Commented code clutters codebase and reduces readability',
                                    'remediation': 'Remove commented code (it\'s in version control if needed)',
                                    'effort': 'low',
                                })
                            comment_block_size = 0

            except:
                pass

    return findings
