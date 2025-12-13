# CLAUDE.md Anti-Patterns

Catalog of common mistakes organized by severity.

## Critical Violations (Fix Immediately)

### Exposed Secrets
```markdown
# BAD - Never do this
API_KEY=sk-abc123...
DATABASE_URL=postgres://user:password@host:5432/db
```

**Detection patterns**:
- `password`, `secret`, `token`, `api_key`
- `postgres://`, `mysql://`, `mongodb://`
- `-----BEGIN.*PRIVATE KEY-----`
- `sk-`, `pk_`, `AKIA` (API key prefixes)

**Fix**: Remove immediately, rotate credentials, clean git history

### Exposed Infrastructure
```markdown
# BAD
Internal API: http://192.168.1.100:8080
Database: 10.0.0.50:5432
```

**Fix**: Use environment variables or secrets management

## High Severity (Fix This Sprint)

### Generic Content
```markdown
# BAD - Claude already knows this
## JavaScript Best Practices
- Use const instead of var
- Prefer arrow functions
- Use async/await over callbacks
```

**Fix**: Remove generic content, keep only project-specific deviations

### Excessive Verbosity
```markdown
# BAD - Too wordy
When you are writing code for this project, it is important that you
remember to always consider the implications of your changes and how
they might affect other parts of the system...
```

**Fix**: Be direct and concise
```markdown
# GOOD
Check integration test impacts before modifying shared utilities.
```

### Vague Instructions
```markdown
# BAD
Write good, clean code following best practices.
```

**Fix**: Be specific
```markdown
# GOOD
- Max function length: 50 lines
- Max file length: 300 lines
- All public functions need JSDoc
```

### Conflicting Guidance
```markdown
# BAD - Contradictory
## Testing
Always write tests first (TDD).

## Development Speed
Skip tests for quick prototypes.
```

**Fix**: Resolve conflicts, specify when each applies

## Medium Severity (Schedule for Next Quarter)

### Outdated Information
```markdown
# BAD
Run: npm run test (uses Jest)  # Actually switched to Vitest 6 months ago
```

**Fix**: Regular audits, add last-updated dates

### Duplicated Content
```markdown
# BAD - Same info twice
## Build Commands
npm run build

## Getting Started
Run `npm run build` to build the project.
```

**Fix**: Single source of truth, reference don't repeat

### Missing Context
```markdown
# BAD - Why this pattern?
Always use repository pattern for data access.
```

**Fix**: Explain reasoning
```markdown
# GOOD
Use repository pattern for data access (enables testing with mocks,
required for our caching layer).
```

### Broken Import Paths
```markdown
# BAD
@docs/old-standards.md  # File was moved/deleted
```

**Fix**: Validate imports exist, update or remove stale references

## Low Severity (Backlog)

### Poor Organization
```markdown
# BAD - No structure
Here's how to build. npm run build. Tests use vitest. We use TypeScript.
The API is REST. Database is Postgres. Deploy with Docker.
```

**Fix**: Use headers, lists, logical grouping

### Inconsistent Formatting
```markdown
# BAD - Mixed styles
## Build Commands
- npm run build

## Testing
Run `npm test` for unit tests
npm run test:e2e runs e2e tests
```

**Fix**: Consistent formatting throughout

### Missing Priority Markers
```markdown
# BAD - What's critical vs nice-to-have?
Use TypeScript strict mode.
Add JSDoc to public functions.
Never use any type.
Format with Prettier.
```

**Fix**: Add priority markers
```markdown
# GOOD
**CRITICAL**: Never use `any` type
**IMPORTANT**: TypeScript strict mode enabled
**RECOMMENDED**: JSDoc on public functions
```

## Structural Anti-Patterns

### Circular Imports
```
CLAUDE.md -> @a.md -> @b.md -> @CLAUDE.md  # Infinite loop
```

**Fix**: Flatten structure, avoid circular references

### Deep Nesting
```
CLAUDE.md -> @a.md -> @b.md -> @c.md -> @d.md -> @e.md  # 5 hops max!
```

**Fix**: Maximum 3 levels recommended, 5 is hard limit

### Monolithic Files
```markdown
# BAD - 800 lines in one file
[Everything crammed together]
```

**Fix**: Split into imports by category
```markdown
# GOOD
@standards/typescript.md
@standards/testing.md
@patterns/api.md
```

## Detection Commands

```bash
# Check for secrets
grep -rE "password|secret|token|api_key" CLAUDE.md

# Check file length
wc -l CLAUDE.md  # Should be < 300

# Check for broken imports
grep "^@" CLAUDE.md | while read import; do
  path="${import#@}"
  [ ! -f "$path" ] && echo "Broken: $import"
done

# Check for vague words
grep -iE "good|clean|proper|best|appropriate" CLAUDE.md
```
