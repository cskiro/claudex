# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Core Principles (Universal)

These principles apply to ALL files and ALL projects.

---

## Fail Fast

- Validate inputs at function boundaries
- Never catch exceptions silently
- Return early on invalid state

## No Silent Failures

- Log errors with context (task_id, user_id, correlation_id)
- Use specific exception types, not generic `Exception`/`Error`

## Git Commits

Format: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `perf`

## Visual Communication

When explaining flows, architecture, comparisons, or state machines → **use ASCII diagrams**. See `visual-documentation.md` for patterns and best practices.

## Security (Always)

- NEVER hardcode secrets (use env vars)
- NEVER commit .env files
- Parameterized queries only (no SQL injection)

---

**For detailed standards**: See path-specific rules in your rules directory.
