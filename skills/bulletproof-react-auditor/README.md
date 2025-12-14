# Bulletproof React Auditor Skill

> Comprehensive audit tool for React/TypeScript codebases based on Bulletproof React architecture principles

An Anthropic Skill that analyzes React applications for architectural issues, component anti-patterns, state management problems, and generates prioritized migration plans for adopting Bulletproof React patterns.

## Features

- **Progressive Disclosure**: Three-phase analysis (Discovery → Deep Analysis → Migration Plan)
- **React-Specific**: Tailored for React 16.8+ (hooks-based applications)
- **Comprehensive Analysis**:
  - Project Structure (feature-based vs flat)
  - Component Architecture (colocation, composition, size)
  - State Management (appropriate tools for each state type)
  - API Layer (centralized, type-safe patterns)
  - Testing Strategy (testing trophy compliance)
  - Styling Patterns (component libraries, utility CSS)
  - Error Handling (boundaries, interceptors, tracking)
  - Performance (code splitting, memoization, optimization)
  - Security (authentication, authorization, XSS prevention)
  - Standards Compliance (ESLint, TypeScript, naming conventions)
- **Multiple Report Formats**: Markdown, JSON, migration roadmaps
- **Prioritized Migration Plans**: P0-P3 severity with effort estimates
- **ASCII Structure Diagrams**: Visual before/after comparisons
- **Industry Standards**: Based on Bulletproof React best practices

## Installation

### Option 1: Claude Code (Recommended)

1. Clone or copy the `bulletproof-react-auditor` directory to your Claude skills directory
2. Ensure Python 3.8+ is installed
3. No additional dependencies required (uses Python standard library)

### Option 2: Manual Installation

```bash
cd ~/.claude/skills
git clone https://github.com/your-org/bulletproof-react-auditor.git
```

## Usage with Claude Code

### Basic Audit

```
Audit this React codebase using the bulletproof-react-auditor skill.
```

### Structure-Focused Audit

```
Run a structure audit on this React app against Bulletproof React patterns.
```

### Generate Migration Plan

```
Audit this React app and generate a migration plan to Bulletproof React architecture.
```

### Custom Scope

```
Audit this React codebase focusing on:
- Project structure and feature organization
- Component architecture patterns
- State management approach
```

## Direct Script Usage

```bash
# Full audit with Markdown report
python scripts/audit_engine.py /path/to/react-app --output audit.md

# Structure-focused audit
python scripts/audit_engine.py /path/to/react-app --scope structure,components --output report.md

# Generate migration plan
python scripts/audit_engine.py /path/to/react-app --migration-plan --output migration.md

# JSON output for CI/CD integration
python scripts/audit_engine.py /path/to/react-app --format json --output audit.json

# Quick health check only (Phase 1)
python scripts/audit_engine.py /path/to/react-app --phase quick
```

## Output Formats

### Markdown (Default)

Human-readable report with:
- ASCII structure diagrams (before/after)
- Detailed findings with code examples
- Step-by-step migration guidance
- Suitable for PRs, documentation, team reviews

### JSON

Machine-readable format for CI/CD integration:
```json
{
  "summary": {
    "compliance_score": 72,
    "grade": "C",
    "critical_issues": 3,
    "migration_effort_days": 15
  },
  "findings": [...],
  "metrics": {...},
  "migration_plan": [...]
}
```

### Migration Plan

Prioritized roadmap with:
- P0-P3 priority levels
- Effort estimates per task
- Dependency chains
- Before/after code examples
- ADR templates

## Audit Criteria

The skill audits based on 10 Bulletproof React categories:

### 1. Project Structure
- Feature-based organization (80%+ code in features/)
- Unidirectional dependencies (shared → features → app)
- No cross-feature imports
- Proper feature boundaries

### 2. Component Architecture
- Component colocation (near usage)
- Limited props (< 7-10 per component)
- No large components (< 300 LOC)
- No nested render functions
- Proper abstraction (identify repetition first)

### 3. State Management
- Appropriate tool for each state type
- Local state preferred over global
- Server cache separated (React Query/SWR)
- Form state managed (React Hook Form)
- URL state utilized

### 4. API Layer
- Centralized API client
- Type-safe request declarations
- Colocated in features/
- Data fetching hooks
- Error handling

### 5. Testing Strategy
- Testing trophy (70% integration, 20% unit, 10% E2E)
- Semantic queries (getByRole preferred)
- User behavior testing (not implementation)
- 80%+ coverage on critical paths

### 6. Styling Patterns
- Consistent approach (component library or utility CSS)
- Colocated styles
- Design system usage

### 7. Error Handling
- API error interceptors
- Multiple error boundaries
- Error tracking service
- User-friendly messages

### 8. Performance
- Code splitting at routes
- Memoization patterns
- State localization
- Image optimization
- Bundle size monitoring

### 9. Security
- JWT with HttpOnly cookies
- Authorization (RBAC/PBAC)
- Input sanitization
- XSS prevention

### 10. Standards Compliance
- ESLint configured
- TypeScript strict mode
- Prettier setup
- Git hooks (Husky)
- Absolute imports
- Kebab-case naming

See [`reference/audit_criteria.md`](reference/audit_criteria.md) for complete checklist.

## Severity Levels

- **Critical (P0)**: Fix immediately (within 24 hours)
  - Security vulnerabilities, breaking architectural patterns

- **High (P1)**: Fix this sprint (within 2 weeks)
  - Major architectural violations, significant refactoring needed

- **Medium (P2)**: Fix next quarter (within 3 months)
  - Component design issues, state management improvements

- **Low (P3)**: Backlog
  - Styling consistency, minor optimizations

See [`reference/severity_matrix.md`](reference/severity_matrix.md) for detailed criteria.

## Migration Approach

### Phase 1: Foundation (Week 1-2)
1. Create feature folders structure
2. Move shared utilities to proper locations
3. Set up absolute imports
4. Configure ESLint for architecture rules

### Phase 2: Feature Extraction (Week 3-6)
1. Identify feature boundaries
2. Move components to features/
3. Colocate API calls with features
4. Extract feature-specific state

### Phase 3: Refinement (Week 7-10)
1. Refactor large components
2. Implement proper state management
3. Add error boundaries
4. Optimize performance

### Phase 4: Polish (Week 11-12)
1. Improve test coverage
2. Add documentation
3. Implement remaining patterns
4. Final review

## Examples

See the [`examples/`](examples/) directory for:
- Sample audit report (React app before Bulletproof)
- Complete migration plan with timeline
- Before/after structure comparisons
- Code transformation examples

## Architecture

```
bulletproof-react-auditor/
├── SKILL.md                      # Skill definition (Claude loads this)
├── README.md                     # This file
├── scripts/
│   ├── audit_engine.py          # Core orchestrator
│   ├── analyzers/               # Specialized analyzers
│   │   ├── project_structure.py      # Folder organization
│   │   ├── component_architecture.py # Component patterns
│   │   ├── state_management.py       # State analysis
│   │   ├── api_layer.py              # API patterns
│   │   ├── testing_strategy.py       # Test quality
│   │   ├── styling_patterns.py       # Styling approach
│   │   ├── error_handling.py         # Error boundaries
│   │   ├── performance_patterns.py   # React performance
│   │   ├── security_practices.py     # React security
│   │   └── standards_compliance.py   # ESLint, TS, Prettier
│   ├── report_generator.py      # Multi-format reports
│   └── migration_planner.py     # Prioritized roadmaps
├── reference/
│   ├── bulletproof_principles.md # Complete BR guide
│   ├── audit_criteria.md         # Full checklist
│   ├── severity_matrix.md        # Issue prioritization
│   └── migration_patterns.md     # Common refactorings
└── examples/
    ├── sample_audit_report.md
    ├── migration_plan.md
    └── before_after_structure.md
```

## Extending the Skill

### Adding a New Analyzer

1. Create `scripts/analyzers/your_analyzer.py`
2. Implement `analyze(codebase_path, metadata)` function
3. Add to `ANALYZERS` dict in `audit_engine.py`

Example:
```python
def analyze(codebase_path: Path, metadata: Dict) -> List[Dict]:
    """Analyze specific Bulletproof React pattern."""
    findings = []

    # Your analysis logic here

    findings.append({
        'severity': 'high',
        'category': 'your_category',
        'title': 'Issue title',
        'current_state': 'What exists now',
        'target_state': 'Bulletproof recommendation',
        'migration_steps': ['Step 1', 'Step 2'],
        'effort': 'medium',
    })

    return findings
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Bulletproof React Audit

on: [pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Bulletproof Audit
        run: |
          python bulletproof-react-auditor/scripts/audit_engine.py . \
            --format json \
            --output audit-report.json
      - name: Check Compliance Score
        run: |
          SCORE=$(jq '.summary.compliance_score' audit-report.json)
          if [ "$SCORE" -lt 70 ]; then
            echo "❌ Compliance score $SCORE below threshold (70)"
            exit 1
          fi
```

## Best Practices

1. **Audit Before Major Refactoring**: Establish baseline before starting
2. **Incremental Migration**: Don't refactor everything at once
3. **Feature-by-Feature**: Migrate one feature at a time
4. **Test Coverage First**: Ensure tests before restructuring
5. **Team Alignment**: Share Bulletproof React principles with team
6. **Document Decisions**: Create ADRs for architectural changes
7. **Track Progress**: Re-run audits weekly to measure improvement

## Connor's Standards Integration

This skill enforces Connor's specific requirements:
- **TypeScript Strict Mode**: No `any` types allowed
- **Test Coverage**: 80%+ minimum on all code
- **Testing Trophy**: 70% integration, 20% unit, 10% E2E
- **Modern Testing**: Semantic queries (getByRole) preferred
- **No Brittle Tests**: Avoid testing implementation details
- **Code Quality**: No console.log, no `var`, strict equality
- **Git Standards**: Conventional commits, proper branch naming

## Limitations

- Static analysis only (no runtime profiling)
- React 16.8+ required (hooks-based)
- Best suited for SPA/SSG patterns
- Next.js apps may have additional patterns
- Large codebases may need scoped analysis
- Does not execute tests (analyzes test files)

## Version

**1.0.0** - Initial release

## Standards Compliance

Based on:
- Bulletproof React Official Guide
- Kent C. Dodds Testing Trophy
- React Best Practices 2024-25
- TypeScript Strict Mode Guidelines
- Connor's Development Standards

## License

Apache 2.0 (example skill for demonstration)

---

**Built with**: Python 3.8+
**Anthropic Skill Version**: 1.0
**Last Updated**: 2024-10-25
**Bulletproof React Version**: Based on v2024 guidelines
