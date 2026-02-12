# Profile Matrix

Which rules belong to which profiles. Core is always included.

## Matrix

| Rule File | Core | TypeScript | Python | Testing | Quality | Security |
|-----------|:----:|:----------:|:------:|:-------:|:-------:|:--------:|
| `core/core.md` | x | | | | | |
| `core/xp-principles.md` | x | | | | | |
| `methodology/git-branching.md` | x | | | | | |
| `methodology/git-flow-narrative.md` | x | | | | | |
| `domain/visual-documentation.md` | x | | | | | |
| `language/typescript.md` | | x | | | | |
| `language/python.md` | | | x | | | |
| `methodology/testing.md` | | | | x | | |
| `quality/pr-review-toolkit-workflow.md` | | | | | x | |
| `quality/code-simplifier-workflow.md` | | | | | x | |
| `quality/docs-check-workflow.md` | | | | | x | |
| `quality/vitest-cpu-protection.md` | | x | | x | | |
| `domain/security.md` | | | | | | x |

## Profile Descriptions

### Core (always included)
Foundation rules that apply to every project: fail-fast principles, XP methodology, git branching conventions, narrative commit templates, and visual documentation standards.

### TypeScript
Language-specific standards for TypeScript/React projects: strict types, naming conventions, React component patterns, import organization. Includes Vitest CPU protection.

### Python
Language-specific standards for Python projects: type hints, Black/Ruff/mypy toolchain, Google-style docstrings, functional patterns, Pydantic configuration.

### Testing
TDD workflow and Testing Trophy methodology: red-green-refactor cycle, AAA pattern, coverage requirements, mocking best practices. Includes Vitest CPU protection.

### Quality
Pre-PR quality gates: PR review toolkit workflow (6 specialized agents), code simplifier workflow, documentation freshness checks.

### Security
OWASP Top 10 prevention, authentication patterns, secrets management, security headers. Path-scoped to load only for security-related files.

## Recommended Combinations

| Project Type | Profiles |
|-------------|----------|
| TypeScript web app | Core + TypeScript + Testing + Quality |
| Python backend | Core + Python + Testing + Quality |
| Full-stack TypeScript | Core + TypeScript + Testing + Quality + Security |
| Full-stack Python | Core + Python + Testing + Quality + Security |
| Polyglot | Core + TypeScript + Python + Testing + Quality + Security |
