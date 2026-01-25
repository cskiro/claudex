"""
Security Scanner

Analyzes codebase for:
- Secrets in code (API keys, tokens, passwords)
- Dependency vulnerabilities
- Common security anti-patterns
- OWASP Top 10 issues
"""

import re
import json
from pathlib import Path
from typing import Dict, List


# Common patterns for secrets
SECRET_PATTERNS = {
    'api_key': re.compile(r'(api[_-]?key|apikey)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', re.IGNORECASE),
    'aws_key': re.compile(r'AKIA[0-9A-Z]{16}'),
    'generic_secret': re.compile(r'(secret|password|passwd|pwd)\s*[=:]\s*["\']([^"\'\s]{8,})["\']', re.IGNORECASE),
    'private_key': re.compile(r'-----BEGIN (RSA |)PRIVATE KEY-----'),
    'jwt': re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'),
    'github_token': re.compile(r'gh[pousr]_[A-Za-z0-9_]{36}'),
    'slack_token': re.compile(r'xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,32}'),
}


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """
    Analyze codebase for security issues.

    Args:
        codebase_path: Path to codebase
        metadata: Project metadata from discovery phase

    Returns:
        List of security findings
    """
    findings = []

    # Scan for secrets
    findings.extend(scan_for_secrets(codebase_path))

    # Scan dependencies for vulnerabilities
    if metadata.get('tech_stack', {}).get('javascript'):
        findings.extend(scan_npm_dependencies(codebase_path))

    # Check for common security anti-patterns
    findings.extend(scan_security_antipatterns(codebase_path, metadata))

    return findings


def scan_for_secrets(codebase_path: Path) -> List[Dict]:
    """Scan for hardcoded secrets in code."""
    findings = []
    exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.venv', 'venv'}
    exclude_files = {'.env.example', 'package-lock.json', 'yarn.lock'}

    # File extensions to scan
    code_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', '.rb', '.php', '.yml', '.yaml', '.json', '.env'}

    for file_path in codebase_path.rglob('*'):
        if (file_path.is_file() and
            file_path.suffix in code_extensions and
            file_path.name not in exclude_files and
            not any(excluded in file_path.parts for excluded in exclude_dirs)):

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                    for pattern_name, pattern in SECRET_PATTERNS.items():
                        matches = pattern.finditer(content)

                        for match in matches:
                            # Find line number
                            line_num = content[:match.start()].count('\n') + 1

                            # Skip if it's clearly a placeholder or example
                            matched_text = match.group(0)
                            if is_placeholder(matched_text):
                                continue

                            findings.append({
                                'severity': 'critical',
                                'category': 'security',
                                'subcategory': 'secrets',
                                'title': f'Potential {pattern_name.replace("_", " ")} found in code',
                                'description': f'Found potential secret on line {line_num}',
                                'file': str(file_path.relative_to(codebase_path)),
                                'line': line_num,
                                'code_snippet': lines[line_num - 1].strip() if line_num <= len(lines) else '',
                                'impact': 'Exposed secrets can lead to unauthorized access and data breaches',
                                'remediation': 'Remove secret from code and use environment variables or secret management tools',
                                'effort': 'low',
                            })

            except:
                pass

    return findings


def is_placeholder(text: str) -> bool:
    """Check if a potential secret is actually a placeholder."""
    placeholders = [
        'your_api_key', 'your_secret', 'example', 'placeholder', 'test',
        'dummy', 'sample', 'xxx', '000', 'abc123', 'changeme', 'replace_me',
        'my_api_key', 'your_key_here', 'insert_key_here'
    ]

    text_lower = text.lower()
    return any(placeholder in text_lower for placeholder in placeholders)


def scan_npm_dependencies(codebase_path: Path) -> List[Dict]:
    """Scan npm dependencies for known vulnerabilities."""
    findings = []

    package_json = codebase_path / 'package.json'
    if not package_json.exists():
        return findings

    try:
        with open(package_json, 'r') as f:
            pkg = json.load(f)

        deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

        # Check for commonly vulnerable packages (simplified - in production use npm audit)
        vulnerable_packages = {
            'lodash': ('< 4.17.21', 'Prototype pollution vulnerability'),
            'axios': ('< 0.21.1', 'SSRF vulnerability'),
            'node-fetch': ('< 2.6.7', 'Information exposure vulnerability'),
        }

        for pkg_name, (vulnerable_version, description) in vulnerable_packages.items():
            if pkg_name in deps:
                findings.append({
                    'severity': 'high',
                    'category': 'security',
                    'subcategory': 'dependencies',
                    'title': f'Potentially vulnerable dependency: {pkg_name}',
                    'description': f'{description} (version: {deps[pkg_name]})',
                    'file': 'package.json',
                    'line': None,
                    'code_snippet': f'"{pkg_name}": "{deps[pkg_name]}"',
                    'impact': 'Vulnerable dependencies can be exploited by attackers',
                    'remediation': f'Update {pkg_name} to version {vulnerable_version.replace("< ", ">= ")} or later',
                    'effort': 'low',
                })

    except:
        pass

    return findings


def scan_security_antipatterns(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Scan for common security anti-patterns."""
    findings = []

    if metadata.get('tech_stack', {}).get('javascript') or metadata.get('tech_stack', {}).get('typescript'):
        findings.extend(scan_js_security_issues(codebase_path))

    return findings


def scan_js_security_issues(codebase_path: Path) -> List[Dict]:
    """Scan JavaScript/TypeScript for security anti-patterns."""
    findings = []
    extensions = {'.js', '.jsx', '.ts', '.tsx'}
    exclude_dirs = {'node_modules', '.git', 'dist', 'build'}

    # Dangerous patterns
    patterns = {
        'eval': (
            re.compile(r'\beval\s*\('),
            'Use of eval() is dangerous',
            'eval() can execute arbitrary code and is a security risk',
            'Refactor to avoid eval(), use safer alternatives like Function constructor with specific scope'
        ),
        'dangerouslySetInnerHTML': (
            re.compile(r'dangerouslySetInnerHTML'),
            'Use of dangerouslySetInnerHTML without sanitization',
            'Can lead to XSS attacks if not properly sanitized',
            'Sanitize HTML content or use safer alternatives'
        ),
        'innerHTML': (
            re.compile(r'\.innerHTML\s*='),
            'Direct assignment to innerHTML',
            'Can lead to XSS attacks if content is not sanitized',
            'Use textContent for text or sanitize HTML before assigning'
        ),
        'document.write': (
            re.compile(r'document\.write\s*\('),
            'Use of document.write()',
            'Can be exploited for XSS and causes page reflow',
            'Use DOM manipulation methods instead'
        ),
    }

    for file_path in codebase_path.rglob('*'):
        if (file_path.suffix in extensions and
            not any(excluded in file_path.parts for excluded in exclude_dirs)):

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                    for pattern_name, (pattern, title, impact, remediation) in patterns.items():
                        for line_num, line in enumerate(lines, start=1):
                            if pattern.search(line):
                                findings.append({
                                    'severity': 'high',
                                    'category': 'security',
                                    'subcategory': 'code_security',
                                    'title': title,
                                    'description': f'Found on line {line_num}',
                                    'file': str(file_path.relative_to(codebase_path)),
                                    'line': line_num,
                                    'code_snippet': line.strip(),
                                    'impact': impact,
                                    'remediation': remediation,
                                    'effort': 'medium',
                                })

            except:
                pass

    return findings
