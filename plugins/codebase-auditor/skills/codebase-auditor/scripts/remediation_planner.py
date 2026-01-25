#!/usr/bin/env python3
"""
Remediation Planner

Generates prioritized action plans based on audit findings.
Uses severity, impact, frequency, and effort to prioritize issues.
"""

from typing import Dict, List
from datetime import datetime, timedelta


def generate_remediation_plan(findings: Dict[str, List[Dict]], metadata: Dict) -> str:
    """
    Generate a prioritized remediation plan.

    Args:
        findings: All findings organized by category
        metadata: Project metadata

    Returns:
        Markdown-formatted remediation plan
    """
    plan = []

    # Header
    plan.append("# Codebase Remediation Plan")
    plan.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    plan.append(f"**Codebase**: `{metadata.get('path', 'Unknown')}`")
    plan.append("\n---\n")

    # Flatten and prioritize all findings
    all_findings = []
    for category, category_findings in findings.items():
        for finding in category_findings:
            finding['category'] = category
            all_findings.append(finding)

    # Calculate priority scores
    for finding in all_findings:
        finding['priority_score'] = calculate_priority_score(finding)

    # Sort by priority score (highest first)
    all_findings.sort(key=lambda x: x['priority_score'], reverse=True)

    # Group by priority level
    p0_issues = [f for f in all_findings if f['severity'] == 'critical']
    p1_issues = [f for f in all_findings if f['severity'] == 'high']
    p2_issues = [f for f in all_findings if f['severity'] == 'medium']
    p3_issues = [f for f in all_findings if f['severity'] == 'low']

    # Priority 0: Critical Issues (Fix Immediately)
    if p0_issues:
        plan.append("## Priority 0: Critical Issues (Fix Immediately ⚡)")
        plan.append("\n**Timeline**: Within 24 hours")
        plan.append("**Impact**: Security vulnerabilities, production-breaking bugs, data loss risks\n")

        for i, finding in enumerate(p0_issues, 1):
            plan.append(f"### {i}. {finding.get('title', 'Untitled')}")
            plan.append(f"**Category**: {finding.get('category', 'Unknown').replace('_', ' ').title()}")
            plan.append(f"**Location**: `{finding.get('file', 'Unknown')}`")
            plan.append(f"**Effort**: {finding.get('effort', 'unknown').upper()}")
            plan.append(f"\n**Issue**: {finding.get('description', 'No description')}")
            plan.append(f"\n**Impact**: {finding.get('impact', 'Unknown impact')}")
            plan.append(f"\n**Action**: {finding.get('remediation', 'No remediation suggested')}\n")
            plan.append("---\n")

    # Priority 1: High Issues (Fix This Sprint)
    if p1_issues:
        plan.append("## Priority 1: High Issues (Fix This Sprint 📅)")
        plan.append("\n**Timeline**: Within current sprint (2 weeks)")
        plan.append("**Impact**: Significant quality, security, or user experience issues\n")

        for i, finding in enumerate(p1_issues[:10], 1):  # Top 10
            plan.append(f"### {i}. {finding.get('title', 'Untitled')}")
            plan.append(f"**Category**: {finding.get('category', 'Unknown').replace('_', ' ').title()}")
            plan.append(f"**Effort**: {finding.get('effort', 'unknown').upper()}")
            plan.append(f"\n**Action**: {finding.get('remediation', 'No remediation suggested')}\n")

        if len(p1_issues) > 10:
            plan.append(f"\n*...and {len(p1_issues) - 10} more high-priority issues*\n")

        plan.append("---\n")

    # Priority 2: Medium Issues (Fix Next Quarter)
    if p2_issues:
        plan.append("## Priority 2: Medium Issues (Fix Next Quarter 📆)")
        plan.append("\n**Timeline**: Within 3 months")
        plan.append("**Impact**: Code maintainability, developer productivity\n")
        plan.append(f"**Total Issues**: {len(p2_issues)}\n")

        # Group by subcategory
        subcategories = {}
        for finding in p2_issues:
            subcat = finding.get('subcategory', 'Other')
            if subcat not in subcategories:
                subcategories[subcat] = []
            subcategories[subcat].append(finding)

        plan.append("**Grouped by Type**:\n")
        for subcat, subcat_findings in subcategories.items():
            plan.append(f"- {subcat.replace('_', ' ').title()}: {len(subcat_findings)} issues")

        plan.append("\n---\n")

    # Priority 3: Low Issues (Backlog)
    if p3_issues:
        plan.append("## Priority 3: Low Issues (Backlog 📋)")
        plan.append("\n**Timeline**: When time permits")
        plan.append("**Impact**: Minor improvements, stylistic issues\n")
        plan.append(f"**Total Issues**: {len(p3_issues)}\n")
        plan.append("*Address during dedicated tech debt sprints or slow periods*\n")
        plan.append("---\n")

    # Implementation Timeline
    plan.append("## Suggested Timeline\n")

    today = datetime.now()

    if p0_issues:
        deadline = today + timedelta(days=1)
        plan.append(f"- **{deadline.strftime('%Y-%m-%d')}**: All P0 issues resolved")

    if p1_issues:
        deadline = today + timedelta(weeks=2)
        plan.append(f"- **{deadline.strftime('%Y-%m-%d')}**: P1 issues addressed (end of sprint)")

    if p2_issues:
        deadline = today + timedelta(weeks=12)
        plan.append(f"- **{deadline.strftime('%Y-%m-%d')}**: P2 issues resolved (end of quarter)")

    # Effort Summary
    plan.append("\n## Effort Summary\n")

    effort_estimates = calculate_effort_summary(all_findings)
    plan.append(f"**Total Estimated Effort**: {effort_estimates['total']} person-days")
    plan.append(f"- Critical/High: {effort_estimates['critical_high']} days")
    plan.append(f"- Medium: {effort_estimates['medium']} days")
    plan.append(f"- Low: {effort_estimates['low']} days")

    # Team Assignment Suggestions
    plan.append("\n## Team Assignment Suggestions\n")
    plan.append("- **Security Team**: All P0 security issues, P1 vulnerabilities")
    plan.append("- **QA/Testing**: Test coverage improvements, test quality issues")
    plan.append("- **Infrastructure**: CI/CD improvements, build performance")
    plan.append("- **Development Team**: Code quality refactoring, complexity reduction")

    # Footer
    plan.append("\n---\n")
    plan.append("*Remediation plan generated by Codebase Auditor Skill*")
    plan.append("\n*Priority scoring based on: Impact × 10 + Frequency × 5 - Effort × 2*")

    return '\n'.join(plan)


def calculate_priority_score(finding: Dict) -> int:
    """
    Calculate priority score for a finding.

    Formula: (Impact × 10) + (Frequency × 5) - (Effort × 2)

    Args:
        finding: Individual finding

    Returns:
        Priority score (higher = more urgent)
    """
    # Map severity to impact (1-10)
    severity_impact = {
        'critical': 10,
        'high': 7,
        'medium': 4,
        'low': 2,
    }
    impact = severity_impact.get(finding.get('severity', 'low'), 1)

    # Estimate frequency (1-10) based on category
    # Security/testing issues affect everything
    category = finding.get('category', '')
    if category in ['security', 'testing']:
        frequency = 10
    elif category in ['quality', 'performance']:
        frequency = 6
    else:
        frequency = 3

    # Map effort to numeric value (1-10)
    effort_values = {
        'low': 2,
        'medium': 5,
        'high': 8,
    }
    effort = effort_values.get(finding.get('effort', 'medium'), 5)

    # Calculate score
    score = (impact * 10) + (frequency * 5) - (effort * 2)

    return max(0, score)  # Never negative


def calculate_effort_summary(findings: List[Dict]) -> Dict[str, int]:
    """
    Calculate total effort estimates.

    Args:
        findings: All findings

    Returns:
        Dictionary with effort estimates in person-days
    """
    # Map effort levels to days
    effort_days = {
        'low': 0.5,
        'medium': 2,
        'high': 5,
    }

    critical_high_days = sum(
        effort_days.get(f.get('effort', 'medium'), 2)
        for f in findings
        if f.get('severity') in ['critical', 'high']
    )

    medium_days = sum(
        effort_days.get(f.get('effort', 'medium'), 2)
        for f in findings
        if f.get('severity') == 'medium'
    )

    low_days = sum(
        effort_days.get(f.get('effort', 'medium'), 2)
        for f in findings
        if f.get('severity') == 'low'
    )

    return {
        'critical_high': round(critical_high_days, 1),
        'medium': round(medium_days, 1),
        'low': round(low_days, 1),
        'total': round(critical_high_days + medium_days + low_days, 1),
    }
