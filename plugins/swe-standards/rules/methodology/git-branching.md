# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Git Branching (Universal)

**Purpose**: All work in git-tracked projects must happen on feature branches. Never commit directly to main, master, or develop.

---

## Rules

1. **Always branch off main** before starting work:
   ```bash
   git checkout main && git pull && git checkout -b <type>/<descriptive-name>
   ```

2. **Never commit directly to protected branches** (main, master, develop).

3. **Branch naming** follows `<type>/<concise-description>`:

   **Types:**
   - `feat/` — New features
   - `fix/` — Bug fixes
   - `hotfix/` — Production hotfixes
   - `refactor/` — Code refactoring
   - `docs/` — Documentation
   - `chore/` — Maintenance tasks

   **Template:** `<type>/<verb-or-noun-phrase>` — 2-4 words, kebab-case, describes _what_ changes.

   **Good:** `feat/enable-sso`, `fix/login-redirect-loop`, `refactor/extract-api-client`, `chore/update-planning-docs`

   **Bad (never use):**
   - `feat/phase-1`, `chore/batch-2`, `fix/round-3` — opaque milestone/phase markers
   - `fix/issues-84-88`, `feat/various-improvements` — bundles multiple scopes
   - `fix/github-issue-123`, `chore/issue-83` — numeric issue refs without description
   - `chore/updates`, `chore/cleanup` — too vague (cleanup _what_?)

4. **One branch = one scope**: Each branch addresses exactly one feature or issue. No bundling unrelated changes.

5. **Merge via PR**: Feature branches merge to main through pull requests with code review.

## Emergency Override

If a direct commit to main is truly necessary, document the reason in the commit message.
