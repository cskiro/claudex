"""
Security Practices Analyzer

Analyzes React security patterns:
- JWT with HttpOnly cookies
- Input sanitization
- XSS prevention
"""

from pathlib import Path
from typing import Dict, List
import re


def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze security practices."""
    findings = []
    src_dir = codebase_path / 'src'

    if not src_dir.exists():
        return findings

    # Check for localStorage token storage (security risk)
    localstorage_auth = []
    for file in src_dir.rglob('*.{ts,tsx,js,jsx}'):
        try:
            with open(file, 'r') as f:
                content = f.read()
                if re.search(r'localStorage\.(get|set)Item\s*\(\s*[\'"].*token.*[\'"]\s*\)', content, re.IGNORECASE):
                    localstorage_auth.append(str(file.relative_to(src_dir)))
        except:
            pass

    if localstorage_auth:
        findings.append({
            'severity': 'high',
            'category': 'security',
            'title': f'Tokens stored in localStorage ({len(localstorage_auth)} files)',
            'current_state': 'Authentication tokens in localStorage (XSS vulnerable)',
            'target_state': 'Use HttpOnly cookies for JWT storage',
            'migration_steps': [
                'Configure API to set tokens in HttpOnly cookies',
                'Remove localStorage token storage',
                'Use credentials: "include" in fetch requests',
                'Implement CSRF protection'
            ],
            'effort': 'medium',
            'affected_files': localstorage_auth[:3],
        })

    # Check for dangerouslySetInnerHTML
    dangerous_html = []
    for file in src_dir.rglob('*.{tsx,jsx}'):
        try:
            with open(file, 'r') as f:
                content = f.read()
                if 'dangerouslySetInnerHTML' in content:
                    dangerous_html.append(str(file.relative_to(src_dir)))
        except:
            pass

    if dangerous_html:
        findings.append({
            'severity': 'high',
            'category': 'security',
            'title': f'dangerouslySetInnerHTML usage ({len(dangerous_html)} files)',
            'current_state': 'Using dangerouslySetInnerHTML (XSS risk)',
            'target_state': 'Sanitize HTML input with DOMPurify',
            'migration_steps': [
                'Install dompurify',
                'Sanitize HTML before rendering',
                'Prefer safe alternatives when possible',
                'Add security review for HTML rendering'
            ],
            'effort': 'low',
            'affected_files': dangerous_html[:3],
        })

    return findings
