#!/usr/bin/env python3
"""
CLAUDE.md Analyzer
Comprehensive validation engine for CLAUDE.md configuration files.

Validates against three categories:
1. Official Anthropic guidance (docs.claude.com)
2. Community best practices
3. Research-based optimizations
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    """Finding severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Category(Enum):
    """Finding categories"""
    SECURITY = "security"
    OFFICIAL_COMPLIANCE = "official_compliance"
    BEST_PRACTICES = "best_practices"
    RESEARCH_OPTIMIZATION = "research_optimization"
    STRUCTURE = "structure"
    MAINTENANCE = "maintenance"


@dataclass
class Finding:
    """Represents a single audit finding"""
    severity: Severity
    category: Category
    title: str
    description: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    impact: str = ""
    remediation: str = ""
    source: str = ""  # "official", "community", or "research"


@dataclass
class AuditResults:
    """Container for all audit results"""
    findings: List[Finding] = field(default_factory=list)
    scores: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, any] = field(default_factory=dict)

    def add_finding(self, finding: Finding):
        """Add a finding to results"""
        self.findings.append(finding)

    def calculate_scores(self):
        """Calculate health scores"""
        # Count findings by severity
        critical = sum(1 for f in self.findings if f.severity == Severity.CRITICAL)
        high = sum(1 for f in self.findings if f.severity == Severity.HIGH)
        medium = sum(1 for f in self.findings if f.severity == Severity.MEDIUM)
        low = sum(1 for f in self.findings if f.severity == Severity.LOW)

        # Calculate category scores (0-100)
        total_issues = max(critical * 20 + high * 10 + medium * 5 + low * 2, 1)
        base_score = max(0, 100 - total_issues)

        # Category-specific scores
        security_issues = [f for f in self.findings if f.category == Category.SECURITY]
        official_issues = [f for f in self.findings if f.category == Category.OFFICIAL_COMPLIANCE]
        best_practice_issues = [f for f in self.findings if f.category == Category.BEST_PRACTICES]
        research_issues = [f for f in self.findings if f.category == Category.RESEARCH_OPTIMIZATION]

        self.scores = {
            "overall": base_score,
            "security": max(0, 100 - len(security_issues) * 25),
            "official_compliance": max(0, 100 - len(official_issues) * 10),
            "best_practices": max(0, 100 - len(best_practice_issues) * 5),
            "research_optimization": max(0, 100 - len(research_issues) * 3),
            "critical_count": critical,
            "high_count": high,
            "medium_count": medium,
            "low_count": low,
        }


class CLAUDEMDAnalyzer:
    """Main analyzer for CLAUDE.md files"""

    # Secret patterns (CRITICAL violations)
    SECRET_PATTERNS = [
        (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}', 'API Key'),
        (r'(?i)(secret|password|passwd|pwd)\s*[=:]\s*["\']?[^\s"\']{8,}', 'Password/Secret'),
        (r'(?i)(token|auth[_-]?token)\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}', 'Auth Token'),
        (r'(?i)sk-[a-zA-Z0-9]{20,}', 'OpenAI API Key'),
        (r'(?i)AKIA[0-9A-Z]{16}', 'AWS Access Key'),
        (r'(?i)(-----BEGIN.*PRIVATE KEY-----)', 'Private Key'),
        (r'(?i)(postgres|mysql|mongodb)://[^:]+:[^@]+@', 'Database Connection String'),
    ]

    # Generic content indicators (HIGH violations)
    GENERIC_PATTERNS = [
        r'(?i)React is a (JavaScript|JS) library',
        r'(?i)TypeScript is a typed superset',
        r'(?i)Git is a version control',
        r'(?i)npm is a package manager',
        r'(?i)What is a component\?',
    ]

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.results = AuditResults()
        self.content = ""
        self.lines = []
        self.line_count = 0
        self.token_estimate = 0

    def analyze(self) -> AuditResults:
        """Run comprehensive analysis"""
        # Read file
        if not self._read_file():
            return self.results

        # Calculate metadata
        self._calculate_metadata()

        # Run all validators
        self._validate_security()
        self._validate_official_compliance()
        self._validate_best_practices()
        self._validate_research_optimization()
        self._validate_structure()
        self._validate_maintenance()

        # Calculate scores
        self.results.calculate_scores()

        return self.results

    def _read_file(self) -> bool:
        """Read and parse the CLAUDE.md file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
                self.line_count = len(self.lines)
            return True
        except Exception as e:
            self.results.add_finding(Finding(
                severity=Severity.CRITICAL,
                category=Category.OFFICIAL_COMPLIANCE,
                title="Cannot Read File",
                description=f"Failed to read {self.file_path}: {str(e)}",
                impact="Unable to validate CLAUDE.md configuration",
                remediation="Ensure file exists and is readable"
            ))
            return False

    def _calculate_metadata(self):
        """Calculate file metadata"""
        # Estimate tokens (rough: 1 token ≈ 4 characters for English)
        self.token_estimate = len(self.content) // 4

        # Calculate percentages of context window
        context_200k = (self.token_estimate / 200000) * 100
        context_1m = (self.token_estimate / 1000000) * 100

        self.results.metadata = {
            "file_path": str(self.file_path),
            "line_count": self.line_count,
            "character_count": len(self.content),
            "token_estimate": self.token_estimate,
            "context_usage_200k": round(context_200k, 2),
            "context_usage_1m": round(context_1m, 2),
            "tier": self._detect_tier(),
        }

    def _detect_tier(self) -> str:
        """Detect which memory tier this file belongs to"""
        path_str = str(self.file_path.absolute())

        if '/Library/Application Support/ClaudeCode/' in path_str or \
           '/etc/claude-code/' in path_str or \
           'C:\\ProgramData\\ClaudeCode\\' in path_str:
            return "Enterprise"
        elif str(self.file_path.name) == 'CLAUDE.md' and \
             (self.file_path.parent.name == '.claude' or \
              self.file_path.parent.name != Path.home().name):
            return "Project"
        elif Path.home() in self.file_path.parents:
            return "User"
        else:
            return "Unknown"

    # ========== SECURITY VALIDATION ==========

    def _validate_security(self):
        """CRITICAL: Check for secrets and sensitive information"""
        # Check for secrets
        for line_num, line in enumerate(self.lines, 1):
            for pattern, secret_type in self.SECRET_PATTERNS:
                if re.search(pattern, line):
                    self.results.add_finding(Finding(
                        severity=Severity.CRITICAL,
                        category=Category.SECURITY,
                        title=f"🚨 {secret_type} Detected",
                        description=f"Potential {secret_type.lower()} found in CLAUDE.md",
                        line_number=line_num,
                        code_snippet=self._redact_line(line),
                        impact="Security breach risk. Secrets may be exposed in git history, "
                               "logs, or backups. This violates security best practices.",
                        remediation=f"1. Remove the {secret_type.lower()} immediately\n"
                                   "2. Rotate the compromised credential\n"
                                   "3. Use environment variables or secret management\n"
                                   "4. Add to .gitignore if in separate file\n"
                                   "5. Clean git history if committed",
                        source="official"
                    ))

        # Check for internal URLs/IPs
        internal_ip_pattern = r'\b(10|172\.(1[6-9]|2[0-9]|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b'
        if re.search(internal_ip_pattern, self.content):
            self.results.add_finding(Finding(
                severity=Severity.CRITICAL,
                category=Category.SECURITY,
                title="Internal IP Address Exposed",
                description="Internal IP addresses found in CLAUDE.md",
                impact="Exposes internal infrastructure topology",
                remediation="Remove internal IPs. Reference documentation instead.",
                source="official"
            ))

    def _redact_line(self, line: str) -> str:
        """Redact sensitive parts of line for display"""
        for pattern, _ in self.SECRET_PATTERNS:
            line = re.sub(pattern, '[REDACTED]', line)
        return line[:100] + "..." if len(line) > 100 else line

    # ========== OFFICIAL COMPLIANCE VALIDATION ==========

    def _validate_official_compliance(self):
        """Validate against official Anthropic documentation"""
        # Check for excessive verbosity (> 500 lines)
        if self.line_count > 500:
            self.results.add_finding(Finding(
                severity=Severity.HIGH,
                category=Category.OFFICIAL_COMPLIANCE,
                title="File Exceeds Recommended Length",
                description=f"CLAUDE.md has {self.line_count} lines (recommended: < 300)",
                impact="Consumes excessive context window space. Official guidance: "
                       "'keep them lean as they take up context window space'",
                remediation="Reduce to under 300 lines. Use @imports for detailed documentation:\n"
                           "Example: @docs/architecture.md",
                source="official"
            ))

        # Check for generic programming content
        self._check_generic_content()

        # Validate import syntax and depth
        self._validate_imports()

        # Check for vague instructions
        self._check_vague_instructions()

        # Validate structure and formatting
        self._check_markdown_structure()

    def _check_generic_content(self):
        """Check for generic programming tutorials/documentation"""
        for line_num, line in enumerate(self.lines, 1):
            for pattern in self.GENERIC_PATTERNS:
                if re.search(pattern, line):
                    self.results.add_finding(Finding(
                        severity=Severity.HIGH,
                        category=Category.OFFICIAL_COMPLIANCE,
                        title="Generic Programming Content Detected",
                        description="File contains generic programming documentation",
                        line_number=line_num,
                        code_snippet=line[:100],
                        impact="Wastes context window. Official guidance: Don't include "
                               "'basic programming concepts Claude already understands'",
                        remediation="Remove generic content. Focus on project-specific standards.",
                        source="official"
                    ))
                    break  # One finding per line is enough

    def _validate_imports(self):
        """Validate @import statements"""
        import_pattern = r'^\s*@([^\s]+)'
        imports = []

        for line_num, line in enumerate(self.lines, 1):
            match = re.match(import_pattern, line)
            if match:
                import_path = match.group(1)
                imports.append((line_num, import_path))

                # Check if import path exists (if it's not a URL)
                if not import_path.startswith(('http://', 'https://')):
                    full_path = self.file_path.parent / import_path
                    if not full_path.exists():
                        self.results.add_finding(Finding(
                            severity=Severity.MEDIUM,
                            category=Category.MAINTENANCE,
                            title="Broken Import Path",
                            description=f"Import path does not exist: {import_path}",
                            line_number=line_num,
                            code_snippet=line,
                            impact="Imported documentation will not be loaded",
                            remediation=f"Fix import path or remove if no longer needed. "
                                       f"Expected: {full_path}",
                            source="official"
                        ))

        # Check for excessive imports (> 10 might be excessive)
        if len(imports) > 10:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.BEST_PRACTICES,
                title="Excessive Imports",
                description=f"Found {len(imports)} import statements",
                impact="Many imports may indicate poor organization",
                remediation="Consider consolidating related documentation",
                source="community"
            ))

        # TODO: Check for circular imports (requires traversing import graph)
        # TODO: Check import depth (max 5 hops)

    def _check_vague_instructions(self):
        """Detect vague or ambiguous instructions"""
        vague_phrases = [
            (r'\b(write|make|keep it|be)\s+(good|clean|simple|consistent|professional)\b', 'vague quality advice'),
            (r'\bfollow\s+best\s+practices\b', 'undefined best practices'),
            (r'\bdon\'t\s+be\s+clever\b', 'subjective advice'),
            (r'\bkeep\s+it\s+simple\b', 'vague simplicity advice'),
        ]

        for line_num, line in enumerate(self.lines, 1):
            for pattern, issue_type in vague_phrases:
                if re.search(pattern, line, re.IGNORECASE):
                    self.results.add_finding(Finding(
                        severity=Severity.HIGH,
                        category=Category.OFFICIAL_COMPLIANCE,
                        title="Vague or Ambiguous Instruction",
                        description=f"Line contains {issue_type}: not specific or measurable",
                        line_number=line_num,
                        code_snippet=line[:100],
                        impact="Not actionable. Claude won't know what this means in your context. "
                               "Official guidance: 'Be specific'",
                        remediation="Replace with measurable standards. Example:\n"
                                   "❌ 'Write good code'\n"
                                   "✅ 'Function length: max 50 lines, complexity: max 10'",
                        source="official"
                    ))

    def _check_markdown_structure(self):
        """Validate markdown structure and formatting"""
        # Check for at least one H1 header
        if not re.search(r'^#\s+', self.content, re.MULTILINE):
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.STRUCTURE,
                title="Missing Top-Level Header",
                description="No H1 header (#) found",
                impact="Poor document structure",
                remediation="Add H1 header with project name: # Project Name",
                source="community"
            ))

        # Check for consistent bullet style
        dash_bullets = len(re.findall(r'^\s*-\s+', self.content, re.MULTILINE))
        asterisk_bullets = len(re.findall(r'^\s*\*\s+', self.content, re.MULTILINE))

        if dash_bullets > 5 and asterisk_bullets > 5:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.STRUCTURE,
                title="Inconsistent Bullet Style",
                description=f"Mix of dash (-) and asterisk (*) bullets",
                impact="Inconsistent formatting reduces readability",
                remediation="Use consistent bullet style (recommend: dashes)",
                source="community"
            ))

    # ========== BEST PRACTICES VALIDATION ==========

    def _validate_best_practices(self):
        """Validate against community best practices"""
        # Check recommended size range (100-300 lines)
        if self.line_count < 50:
            self.results.add_finding(Finding(
                severity=Severity.INFO,
                category=Category.BEST_PRACTICES,
                title="File May Be Too Sparse",
                description=f"Only {self.line_count} lines (recommended: 100-300)",
                impact="May lack important project context",
                remediation="Consider adding: project overview, standards, common commands",
                source="community"
            ))
        elif 300 < self.line_count <= 500:
            self.results.add_finding(Finding(
                severity=Severity.MEDIUM,
                category=Category.BEST_PRACTICES,
                title="File Exceeds Optimal Length",
                description=f"{self.line_count} lines (recommended: 100-300)",
                impact="Community best practice: 200-line sweet spot for balance",
                remediation="Consider using imports for detailed documentation",
                source="community"
            ))

        # Check token usage percentage
        if self.token_estimate > 10000:  # > 5% of 200K context
            self.results.add_finding(Finding(
                severity=Severity.MEDIUM,
                category=Category.BEST_PRACTICES,
                title="High Token Usage",
                description=f"Estimated {self.token_estimate} tokens "
                           f"({self.results.metadata['context_usage_200k']}% of 200K window)",
                impact="Consumes significant context space (> 5%)",
                remediation="Aim for < 3,000 tokens (≈200 lines). Use imports for details.",
                source="community"
            ))

        # Check for organizational patterns
        self._check_organization()

        # Check for maintenance indicators
        self._check_update_dates()

    def _check_organization(self):
        """Check for good organizational patterns"""
        # Look for section markers
        sections = re.findall(r'^##\s+(.+)$', self.content, re.MULTILINE)

        if len(sections) < 3:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.STRUCTURE,
                title="Minimal Organization",
                description=f"Only {len(sections)} main sections found",
                impact="May lack clear structure",
                remediation="Organize into sections: Standards, Workflow, Commands, Reference",
                source="community"
            ))

        # Check for critical/important markers
        has_critical = bool(re.search(r'(?i)(critical|must|required|mandatory)', self.content))
        if not has_critical and self.line_count > 100:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.BEST_PRACTICES,
                title="No Priority Markers",
                description="No CRITICAL/MUST/REQUIRED emphasis found",
                impact="Hard to distinguish must-follow vs. nice-to-have standards",
                remediation="Add priority markers: CRITICAL, IMPORTANT, RECOMMENDED",
                source="community"
            ))

    def _check_update_dates(self):
        """Check for update dates/version information"""
        date_pattern = r'\b(20\d{2}[/-]\d{1,2}[/-]\d{1,2}|updated?:?\s*20\d{2})\b'
        has_date = bool(re.search(date_pattern, self.content, re.IGNORECASE))

        if not has_date and self.line_count > 100:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.MAINTENANCE,
                title="No Update Date",
                description="No last-updated date found",
                impact="Hard to know if information is current",
                remediation="Add update date: Updated: 2025-10-26",
                source="community"
            ))

    # ========== RESEARCH OPTIMIZATION VALIDATION ==========

    def _validate_research_optimization(self):
        """Validate against research-based optimizations"""
        # Check for positioning strategy (critical info at top/bottom)
        self._check_positioning_strategy()

        # Check for effective chunking
        self._check_chunking()

    def _check_positioning_strategy(self):
        """Check if critical information is positioned optimally"""
        # Analyze first 20% and last 20% for critical markers
        top_20_idx = max(1, self.line_count // 5)
        bottom_20_idx = self.line_count - top_20_idx

        top_content = '\n'.join(self.lines[:top_20_idx])
        bottom_content = '\n'.join(self.lines[bottom_20_idx:])
        middle_content = '\n'.join(self.lines[top_20_idx:bottom_20_idx])

        critical_markers = r'(?i)(critical|must|required|mandatory|never|always)'

        top_critical = len(re.findall(critical_markers, top_content))
        middle_critical = len(re.findall(critical_markers, middle_content))
        bottom_critical = len(re.findall(critical_markers, bottom_content))

        # If most critical content is in the middle, flag it
        total_critical = top_critical + middle_critical + bottom_critical
        if total_critical > 0 and middle_critical > (top_critical + bottom_critical):
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.RESEARCH_OPTIMIZATION,
                title="Critical Content in Middle Position",
                description="Most critical standards appear in middle section",
                impact="Research shows 'lost in the middle' attention pattern. "
                       "Critical info at top/bottom gets more attention.",
                remediation="Move must-follow standards to top section. "
                           "Move reference info to bottom. "
                           "Keep nice-to-have in middle.",
                source="research"
            ))

    def _check_chunking(self):
        """Check for effective information chunking"""
        # Look for clear section boundaries
        section_pattern = r'^#{1,3}\s+.+$'
        sections = re.findall(section_pattern, self.content, re.MULTILINE)

        if self.line_count > 100 and len(sections) < 5:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.RESEARCH_OPTIMIZATION,
                title="Large Unchunked Content",
                description=f"{self.line_count} lines with only {len(sections)} sections",
                impact="Large blocks of text harder to process. "
                       "Research suggests chunking improves comprehension.",
                remediation="Break into logical sections with clear headers",
                source="research"
            ))

    # ========== STRUCTURE & MAINTENANCE VALIDATION ==========

    def _validate_structure(self):
        """Validate document structure"""
        # Already covered in other validators
        pass

    def _validate_maintenance(self):
        """Validate maintenance indicators"""
        # Check for broken links (basic check)
        self._check_broken_links()

        # Check for duplicate sections
        self._check_duplicate_sections()

    def _check_broken_links(self):
        """Check for potentially broken file paths"""
        # Look for file path references
        path_pattern = r'[/\\][a-zA-Z0-9_\-]+[/\\][^\s\)]*'
        potential_paths = re.findall(path_pattern, self.content)

        broken_count = 0
        for path_str in potential_paths:
            # Clean up the path
            path_str = path_str.strip('`"\' ')
            if path_str.startswith('/'):
                # Check if path exists (relative to project root or absolute)
                check_path = self.file_path.parent / path_str.lstrip('/')
                if not check_path.exists() and not Path(path_str).exists():
                    broken_count += 1

        if broken_count > 0:
            self.results.add_finding(Finding(
                severity=Severity.MEDIUM,
                category=Category.MAINTENANCE,
                title="Potentially Broken File Paths",
                description=f"Found {broken_count} file paths that may not exist",
                impact="Broken paths mislead developers and indicate stale documentation",
                remediation="Verify all file paths and update or remove broken ones",
                source="community"
            ))

    def _check_duplicate_sections(self):
        """Check for duplicate section headers"""
        headers = re.findall(r'^#{1,6}\s+(.+)$', self.content, re.MULTILINE)
        header_counts = {}

        for header in headers:
            normalized = header.lower().strip()
            header_counts[normalized] = header_counts.get(normalized, 0) + 1

        duplicates = {h: c for h, c in header_counts.items() if c > 1}

        if duplicates:
            self.results.add_finding(Finding(
                severity=Severity.LOW,
                category=Category.STRUCTURE,
                title="Duplicate Section Headers",
                description=f"Found duplicate headers: {', '.join(duplicates.keys())}",
                impact="May indicate poor organization or conflicting information",
                remediation="Consolidate duplicate sections or rename for clarity",
                source="community"
            ))


def analyze_file(file_path: str) -> AuditResults:
    """Convenience function to analyze a CLAUDE.md file"""
    analyzer = CLAUDEMDAnalyzer(Path(file_path))
    return analyzer.analyze()


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <path-to-CLAUDE.md>")
        sys.exit(1)

    file_path = sys.argv[1]
    results = analyze_file(file_path)

    # Print summary
    print(f"\n{'='*60}")
    print(f"CLAUDE.md Audit Results: {file_path}")
    print(f"{'='*60}\n")

    print(f"Overall Health Score: {results.scores['overall']}/100")
    print(f"Security Score: {results.scores['security']}/100")
    print(f"Official Compliance Score: {results.scores['official_compliance']}/100")
    print(f"Best Practices Score: {results.scores['best_practices']}/100")
    print(f"Research Optimization Score: {results.scores['research_optimization']}/100")

    print(f"\n{'='*60}")
    print(f"Findings Summary:")
    print(f"  🚨 Critical: {results.scores['critical_count']}")
    print(f"  ⚠️  High: {results.scores['high_count']}")
    print(f"  📋 Medium: {results.scores['medium_count']}")
    print(f"  ℹ️  Low: {results.scores['low_count']}")
    print(f"{'='*60}\n")

    # Print findings
    for finding in results.findings:
        severity_emoji = {
            Severity.CRITICAL: "🚨",
            Severity.HIGH: "⚠️",
            Severity.MEDIUM: "📋",
            Severity.LOW: "ℹ️",
            Severity.INFO: "💡"
        }

        print(f"{severity_emoji.get(finding.severity, '•')} {finding.title}")
        print(f"   Category: {finding.category.value}")
        print(f"   {finding.description}")
        if finding.line_number:
            print(f"   Line: {finding.line_number}")
        if finding.remediation:
            print(f"   Fix: {finding.remediation}")
        print()
