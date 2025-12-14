# CLAUDE.md Anti-Patterns and Common Mistakes

> **Purpose**: Catalog of common mistakes, violations, and anti-patterns to avoid when creating CLAUDE.md files

This document identifies problematic patterns frequently found in CLAUDE.md files, explains why they're problematic, and provides better alternatives.

---

## Critical Violations (Security & Safety)

### 🚨 CRITICAL-01: Secrets in Memory Files

#### Problem
```markdown
# CLAUDE.md

## API Configuration
- API Key: sk-1234567890abcdefghijklmnop
- Database Password: MySecretPassword123
- AWS Secret: AKIAIOSFODNN7EXAMPLE
```

#### Why It's Dangerous
- ❌ CLAUDE.md files are typically committed to source control
- ❌ Exposes credentials to entire team and git history
- ❌ Can leak through PR comments, logs, or backups
- ❌ Violates security best practices

#### Correct Approach
```markdown
# CLAUDE.md

## API Configuration
- API keys stored in: .env (see .env.example for template)
- Database credentials: Use AWS Secrets Manager
- AWS credentials: Use IAM roles, never hardcode

## Environment Variables Required
- API_KEY (get from team lead)
- DB_PASSWORD (from 1Password vault)
- AWS_REGION (default: us-east-1)
```

**Severity**: CRITICAL
**Action**: Immediate removal + git history cleanup + key rotation

---

### 🚨 CRITICAL-02: Exposed Internal URLs/IPs

#### Problem
```markdown
## Production Servers
- Production Database: postgres://admin:pass@10.0.1.42:5432/proddb
- Internal API: https://internal-api.company.net/v1
- Admin Panel: https://admin.company.net (password: admin123)
```

#### Why It's Dangerous
- ❌ Exposes internal infrastructure
- ❌ Provides attack surface information
- ❌ May violate security policies

#### Correct Approach
```markdown
## Production Access
- Database: Use connection string from AWS Parameter Store
- API: See deployment documentation (requires VPN)
- Admin Panel: Contact DevOps for access (SSO required)
```

**Severity**: CRITICAL
**Action**: Remove immediately + security review

---

## High-Severity Issues

### ⚠️ HIGH-01: Generic Programming Advice

#### Problem
```markdown
## React Best Practices

React is a JavaScript library for building user interfaces. It was created
by Facebook in 2013. React uses a virtual DOM for efficient updates.

### What is a Component?
A component is a reusable piece of UI. Components can be class-based or
functional. Functional components are preferred in modern React...

[200 lines of React documentation]
```

#### Why It's Problematic
- ❌ Wastes context window space
- ❌ Claude already knows this information
- ❌ Not project-specific
- ❌ Duplicates official documentation

#### Correct Approach
```markdown
## React Standards (Project-Specific)

- Use functional components only (no class components)
- Custom hooks in: /src/hooks
- Component co-location pattern: Component + test + styles in same directory
- Props interface naming: [ComponentName]Props

Example:
/src/features/auth/LoginForm/
  ├── LoginForm.tsx
  ├── LoginForm.test.tsx
  ├── LoginForm.styles.ts
  └── index.ts
```

**Severity**: HIGH
**Action**: Remove generic content, keep only project-specific standards

---

### ⚠️ HIGH-02: Excessive Verbosity

#### Problem
```markdown
# CLAUDE.md (1,200 lines)

## Introduction
Welcome to our project. This document contains comprehensive information...
[50 lines of introduction]

## History
This project started in 2019 when our founder...
[100 lines of history]

## Git Basics
To use git, first you need to understand version control...
[200 lines of git tutorial]

## TypeScript Fundamentals
TypeScript is a typed superset of JavaScript...
[300 lines of TypeScript basics]

[500 more lines of generic information]
```

#### Why It's Problematic
- ❌ Consumes excessive context (> 18,000 tokens ≈ 9% of 200K window)
- ❌ "Lost in the middle" degradation
- ❌ Difficult to maintain
- ❌ Hard to find relevant information

#### Correct Approach
```markdown
# CLAUDE.md (250 lines)

## Project: MyApp
Enterprise CRM built with React + TypeScript + PostgreSQL

## CRITICAL STANDARDS
[20 lines of must-follow rules]

## Architecture
[30 lines of project-specific architecture]

## Development Workflow
[40 lines of team process]

## Code Standards
[50 lines of project-specific rules]

## Common Tasks
[40 lines of commands and workflows]

## Detailed Documentation (Imports)
@docs/architecture.md
@docs/git-workflow.md
@docs/typescript-conventions.md
```

**Severity**: HIGH
**Action**: Reduce to < 300 lines, use imports for detailed docs

---

### ⚠️ HIGH-03: Vague or Ambiguous Instructions

#### Problem
```markdown
## Code Quality
- Write good code
- Make it clean
- Follow best practices
- Be consistent
- Keep it simple
- Don't be clever
```

#### Why It's Problematic
- ❌ Not actionable
- ❌ Subjective interpretation
- ❌ Doesn't provide measurable criteria
- ❌ Claude won't know what "good" means in your context

#### Correct Approach
```markdown
## Code Quality Standards (Measurable)

- Function length: Maximum 50 lines (warning) / 100 lines (error)
- Cyclomatic complexity: Maximum 10 (warning) / 20 (error)
- Test coverage: Minimum 80% for new code
- No `console.log` in src/ directory (use /src/lib/logger.ts)
- No `any` types (use `unknown` if type truly unknown)
- TypeScript strict mode: Enabled (no opt-outs)
```

**Severity**: HIGH
**Action**: Replace vague advice with specific, measurable standards

---

## Medium-Severity Issues

### ⚠️ MEDIUM-01: Outdated Information

#### Problem
```markdown
## Build Process
- Use Webpack 4 for bundling
- Node 12 required
- Run tests with Jest 25

## Deployment
- Deploy to Heroku using git push
- Use MongoDB 3.6
```

#### Why It's Problematic
- ❌ Misleads developers
- ❌ May cause build failures
- ❌ Indicates unmaintained documentation
- ❌ Conflicts with actual setup

#### Correct Approach
```markdown
## Build Process (Updated 2025-10-26)
- Vite 5.0 for bundling (migrated from Webpack)
- Node 20 LTS required
- Run tests with Vitest 2.0

## Deployment (Updated 2025-10-26)
- Deploy to AWS ECS using GitHub Actions
- Use PostgreSQL 16

## Update History
- 2025-10-26: Migrated to Vite, PostgreSQL
- 2024-05-15: Upgraded to Node 20
```

**Severity**: MEDIUM
**Action**: Regular audits, include update dates

---

### ⚠️ MEDIUM-02: Duplicate or Conflicting Information

#### Problem
```markdown
## Code Style (Line 50)
- Use 2-space indentation
- Prefer single quotes

## TypeScript Standards (Line 150)
- Use 4-space indentation
- Prefer double quotes

## React Guidelines (Line 250)
- Indentation: Use tabs
- Quotes: Use backticks for strings
```

#### Why It's Problematic
- ❌ Conflicting instructions
- ❌ Claude may follow the wrong standard
- ❌ Team confusion
- ❌ Indicates poor maintenance

#### Correct Approach
```markdown
## Code Style (Single Source of Truth)

### Formatting (Enforced by Prettier)
- Indentation: 2 spaces
- Quotes: Single quotes for strings, backticks for templates
- Line length: 100 characters
- Trailing commas: Always

### Config Location
- .prettierrc.json (root directory)
- Auto-format on save (VS Code: editor.formatOnSave)
```

**Severity**: MEDIUM
**Action**: Consolidate all style rules in one section

---

### ⚠️ MEDIUM-03: Missing Context for Standards

#### Problem
```markdown
## Standards
- Never use `useState` hook
- All API calls must use POST method
- No files over 200 lines
- Must use Redux for all state
```

#### Why It's Problematic
- ❌ Standards seem arbitrary without context
- ❌ May be outdated after architecture changes
- ❌ Hard to question or update
- ❌ New team members don't understand "why"

#### Correct Approach
```markdown
## State Management Standards

### useState Hook (Avoid for Complex State)
- ❌ DON'T: Use useState for complex/shared state
- ✅ DO: Use useState for simple local UI state (toggles, input values)
- ✅ DO: Use Zustand for shared application state
- WHY: useState causes prop drilling; Zustand avoids this

### API Call Methods
- Use POST for: Mutations, large request bodies
- Use GET for: Queries, cached responses
- WHY: RESTful conventions, better caching

### File Length (Soft Limit: 200 Lines)
- Preference: Keep files under 200 lines
- Exception: Generated files, large data structures
- WHY: Maintainability, easier code review
```

**Severity**: MEDIUM
**Action**: Add context/rationale for standards

---

## Low-Severity Issues

### ⚠️ LOW-01: Poor Organization

#### Problem
```markdown
# CLAUDE.md

Random information...
## Testing
More random stuff...
### Security
Back to testing...
## API
### More Security
## Testing Again
```

#### Why It's Problematic
- ❌ Hard to navigate
- ❌ Information scattered
- ❌ Difficult to maintain
- ❌ Poor user experience

#### Correct Approach
```markdown
# Project Name

## 1. CRITICAL STANDARDS
[Must-follow rules]

## 2. PROJECT OVERVIEW
[Context and architecture]

## 3. DEVELOPMENT WORKFLOW
[Git, PRs, deployment]

## 4. CODE STANDARDS
[Language/framework specific]

## 5. TESTING REQUIREMENTS
[Coverage, strategies]

## 6. SECURITY REQUIREMENTS
[Authentication, data protection]

## 7. COMMON TASKS
[Commands, workflows]

## 8. REFERENCE
[File locations, links]
```

**Severity**: LOW
**Action**: Reorganize with clear hierarchy

---

### ⚠️ LOW-02: Broken Links and Paths

#### Problem
```markdown
## Documentation
- See architecture docs: /docs/arch.md (404)
- Import types from: /src/old-types/index.ts (moved)
- Run deploy script: ./scripts/deploy.sh (deleted)
```

#### Why It's Problematic
- ❌ Misleads developers
- ❌ Causes frustration
- ❌ Indicates stale documentation

#### Correct Approach
```markdown
## Documentation (Verified 2025-10-26)
- Architecture: /docs/architecture/system-design.md ✅
- Types: /src/types/index.ts ✅
- Deployment: npm run deploy (see package.json scripts) ✅

## Validation
Links verified: 2025-10-26
Next check: 2026-01-26
```

**Severity**: LOW
**Action**: Periodic validation, date stamps

---

### ⚠️ LOW-03: Inconsistent Formatting

#### Problem
```markdown
## Code Standards
some bullet points without dashes
* Others with asterisks
- Some with dashes
  - Inconsistent indentation
    * Mixed styles

Headers in Title Case
Headers in sentence case
Headers in SCREAMING CASE
```

#### Why It's Problematic
- ❌ Unprofessional appearance
- ❌ Harder to parse
- ❌ May affect rendering
- ❌ Poor user experience

#### Correct Approach
```markdown
## Code Standards

### Formatting Rules
- Consistent bullet style (dashes)
- 2-space indentation for nested lists
- Title Case for H2 headers
- Sentence case for H3 headers

### Example List
- First item
  - Nested item A
  - Nested item B
- Second item
  - Nested item C
```

**Severity**: LOW
**Action**: Adopt consistent markdown style guide

---

## Structural Anti-Patterns

### 📋 STRUCTURE-01: No Section Hierarchy

#### Problem
```markdown
# CLAUDE.md
Everything at the top level
No organization
No hierarchy
Just a wall of text
```

#### Correct Approach
```markdown
# Project Name

## Section 1
### Subsection 1.1
### Subsection 1.2

## Section 2
### Subsection 2.1
```

---

### 📋 STRUCTURE-02: Circular Imports

#### Problem
```markdown
# CLAUDE.md
@docs/standards.md

# docs/standards.md
@docs/guidelines.md

# docs/guidelines.md
@CLAUDE.md
```

#### Correct Approach
- Maintain acyclic import graph
- Use unidirectional imports
- CLAUDE.md → detailed docs (not reverse)

---

### 📋 STRUCTURE-03: Deep Import Nesting

#### Problem
```markdown
# CLAUDE.md
@docs/level1.md
  @docs/level2.md
    @docs/level3.md
      @docs/level4.md
        @docs/level5.md
          @docs/level6.md (exceeds 5-hop limit)
```

#### Correct Approach
- Maximum 5 import hops
- Flatten structure when possible
- Use fewer, comprehensive documents

---

## Detection and Prevention

### Automated Checks

```markdown
## Checklist for CLAUDE.md Quality

### Security (CRITICAL)
- [ ] No API keys, tokens, or passwords
- [ ] No database credentials
- [ ] No internal URLs or IPs
- [ ] No private keys
- [ ] Git history clean

### Content Quality (HIGH)
- [ ] No generic programming tutorials
- [ ] Under 300 lines (or using imports)
- [ ] Specific, actionable instructions
- [ ] No vague advice ("write good code")
- [ ] Project-specific context

### Maintainability (MEDIUM)
- [ ] No outdated information
- [ ] No conflicting instructions
- [ ] Context provided for standards
- [ ] All links functional
- [ ] Last update date present

### Structure (LOW)
- [ ] Clear section hierarchy
- [ ] Consistent formatting
- [ ] No circular imports
- [ ] Import depth ≤ 5 hops
- [ ] Logical organization
```

---

## Anti-Pattern Summary Table

| ID | Anti-Pattern | Severity | Impact | Fix Effort |
|----|-------------|----------|---------|------------|
| CRITICAL-01 | Secrets in memory files | 🚨 CRITICAL | Security breach | Immediate |
| CRITICAL-02 | Exposed internal infrastructure | 🚨 CRITICAL | Security risk | Immediate |
| HIGH-01 | Generic programming advice | ⚠️ HIGH | Context waste | High |
| HIGH-02 | Excessive verbosity | ⚠️ HIGH | Context waste | High |
| HIGH-03 | Vague instructions | ⚠️ HIGH | Ineffective | Medium |
| MEDIUM-01 | Outdated information | ⚠️ MEDIUM | Misleading | Medium |
| MEDIUM-02 | Duplicate/conflicting info | ⚠️ MEDIUM | Confusion | Medium |
| MEDIUM-03 | Missing context for standards | ⚠️ MEDIUM | Poor adoption | Low |
| LOW-01 | Poor organization | ⚠️ LOW | UX issue | Low |
| LOW-02 | Broken links/paths | ⚠️ LOW | Frustration | Low |
| LOW-03 | Inconsistent formatting | ⚠️ LOW | Unprofessional | Low |
| STRUCTURE-01 | No section hierarchy | 📋 STRUCTURAL | Poor navigation | Low |
| STRUCTURE-02 | Circular imports | 📋 STRUCTURAL | Load failure | Medium |
| STRUCTURE-03 | Deep import nesting | 📋 STRUCTURAL | Complexity | Low |

---

## Real-World Examples

### Example 1: The "Documentation Dump"

**Before** (Anti-Pattern):
```markdown
# CLAUDE.md (2,500 lines)

[Complete React documentation copy-pasted]
[Complete TypeScript handbook]
[Complete git tutorial]
[Complete testing library docs]
```

**After** (Fixed):
```markdown
# CLAUDE.md (200 lines)

## Project-Specific React Standards
- Functional components only
- Co-location pattern
- Custom hooks in /src/hooks

## TypeScript Standards
- Strict mode enabled
- No `any` types
- Explicit return types

@docs/react-architecture.md
@docs/typescript-conventions.md
```

---

### Example 2: The "Secret Leaker"

**Before** (Anti-Pattern):
```markdown
## API Configuration
API_KEY=sk-1234567890
DB_PASSWORD=MySecret123
```

**After** (Fixed):
```markdown
## API Configuration
- Use .env file (see .env.example)
- API_KEY: Get from team lead
- DB_PASSWORD: In 1Password vault
```

---

### Example 3: The "Vague Advisor"

**Before** (Anti-Pattern):
```markdown
## Standards
- Write clean code
- Be professional
- Follow best practices
```

**After** (Fixed):
```markdown
## Code Quality Standards
- Max function length: 50 lines
- Max cyclomatic complexity: 10
- Min test coverage: 80%
- No console.log in production
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-26
**Purpose**: Anti-pattern catalog for CLAUDE.md auditing
**Status**: Comprehensive reference for audit validation
