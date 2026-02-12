# Rule Catalog

Summary of every rule included in the swe-standards plugin.

---

## Core Rules

### core.md
**Profile**: Core
**Scope**: Universal (all files)

Foundation principles: fail fast (validate inputs at boundaries), no silent failures (log errors with context), conventional commit format, visual communication via ASCII diagrams, and security basics (no hardcoded secrets, parameterized queries).

### xp-principles.md
**Profile**: Core
**Scope**: Universal

Kent Beck's 16 XP principles for decision-making: Rapid Feedback, Assume Simplicity, Incremental Change, Embracing Change, Quality Work, Document Decisions (ADRs), Travel Light, plus 9 contextual principles. Includes decision checklist and anti-pattern table.

---

## Methodology Rules

### git-branching.md
**Profile**: Core
**Scope**: Universal

Branch naming (`<type>/<descriptive-name>`), one branch per scope, never commit to protected branches, merge via PR. Enforces descriptive names over opaque identifiers.

### git-flow-narrative.md
**Profile**: Core
**Scope**: Universal

Narrative commit templates (Intent/Interpretation/Action/Insight), PR description template (The Ask/Journey/Architecture/Outcome/Lessons), co-author attribution, commit flow that reads like chapters.

### testing.md
**Profile**: Testing
**Scope**: Universal

TDD red-green-refactor-audit cycle, Testing Trophy (70% integration, 20% unit, 10% E2E), AAA pattern, `should [behavior] when [condition]` naming, 80% coverage minimum, mocking best practices, anti-patterns table.

---

## Domain Rules

### security.md
**Profile**: Security
**Scope**: Path-scoped (`**/auth/**`, `**/security/**`, `**/middleware/**`, `**/*.env*`, etc.)

OWASP Top 10 prevention table, auth patterns (OAuth 2.0, short-lived tokens, bcrypt/argon2), data protection (AES-256, TLS 1.2+, PII redaction), secrets management, secure coding examples (SQL, paths, passwords), security headers, pre-production checklist.

### visual-documentation.md
**Profile**: Core
**Scope**: Universal

ASCII diagram patterns (system context, flow, decision, status table, layer architecture), box-drawing character reference, when-to-use decision table, best practices for diagram clarity.

---

## Language Rules

### typescript.md
**Profile**: TypeScript
**Scope**: Path-scoped (`**/*.ts`, `**/*.tsx`)

Strict mode required, no `any` types, explicit return types, Prettier + ESLint, naming conventions (camelCase functions, PascalCase types), React component patterns (function components, props interfaces), import organization, error handling with `unknown`, utility types.

### python.md
**Profile**: Python
**Scope**: Path-scoped (`**/*.py`)

Type hints mandatory, mypy strict, Black + Ruff toolchain, snake_case naming, Google-style docstrings, error handling (specific exceptions, context logging), import organization with isort, functional patterns preferred, Pydantic for configuration.

---

## Quality Rules

### pr-review-toolkit-workflow.md
**Profile**: Quality
**Scope**: Universal

6 specialized review agents (code-reviewer, code-simplifier, comment-analyzer, pr-test-analyzer, silent-failure-hunter, type-design-analyzer), decision matrix by task type, parallel vs sequential execution guide, pre-PR checklist.

### code-simplifier-workflow.md
**Profile**: Quality
**Scope**: Universal

Final quality gate before PR: extract named functions, simplify array operations, improve cleanup patterns, enhance variable naming. Preserves security fixes and API contracts. Run after all other reviews.

### docs-check-workflow.md
**Profile**: Quality
**Scope**: Universal

Documentation freshness checks: CLAUDE.md, README.md, CHANGELOG.md, architecture diagrams, ADRs. Trigger table mapping change types to required doc updates. Anti-patterns (stale docs, orphan docs).

### vitest-cpu-protection.md
**Profile**: TypeScript, Testing
**Scope**: Universal

CPU protection for Vitest: thread limiting (4 max per instance), shell wrapper (`vtest`), status monitor (`vtest_status`), recommended limits table, CI configuration.
