# CI/CD Integration Examples

Ready-to-use configurations for automated CLAUDE.md validation.

## Pre-Commit Hook

### Basic Validation

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q "CLAUDE.md"; then
  echo "Validating CLAUDE.md..."

  FILE=$(git diff --cached --name-only | grep "CLAUDE.md" | head -1)

  # Check file length
  LINES=$(wc -l < "$FILE")
  if [ "$LINES" -gt 500 ]; then
    echo "ERROR: CLAUDE.md is $LINES lines (max 500)"
    exit 1
  fi

  # Check for secrets
  if grep -qE "password|secret|token|api_key|-----BEGIN" "$FILE"; then
    echo "ERROR: Potential secrets detected in CLAUDE.md"
    echo "Run: grep -nE 'password|secret|token|api_key' $FILE"
    exit 1
  fi

  # Check for broken imports
  grep "^@" "$FILE" | while read -r import; do
    path="${import#@}"
    if [ ! -f "$path" ]; then
      echo "ERROR: Broken import: $import"
      exit 1
    fi
  done

  echo "CLAUDE.md validation passed"
fi
```

### Installation
```bash
chmod +x .git/hooks/pre-commit
```

## GitHub Actions

### Basic Workflow

```yaml
# .github/workflows/claude-md-audit.yml
name: CLAUDE.md Audit

on:
  pull_request:
    paths:
      - '**/CLAUDE.md'
      - '**/.claude/CLAUDE.md'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Find CLAUDE.md files
        id: find
        run: |
          files=$(find . -name "CLAUDE.md" -type f)
          echo "files=$files" >> $GITHUB_OUTPUT

      - name: Check file lengths
        run: |
          for file in ${{ steps.find.outputs.files }}; do
            lines=$(wc -l < "$file")
            if [ "$lines" -gt 500 ]; then
              echo "::error file=$file::File is $lines lines (max 500)"
              exit 1
            fi
            echo "OK: $file ($lines lines)"
          done

      - name: Check for secrets
        run: |
          for file in ${{ steps.find.outputs.files }}; do
            if grep -qE "password|secret|token|api_key|-----BEGIN" "$file"; then
              echo "::error file=$file::Potential secrets detected"
              grep -nE "password|secret|token|api_key" "$file" || true
              exit 1
            fi
          done
          echo "No secrets detected"

      - name: Check imports
        run: |
          for file in ${{ steps.find.outputs.files }}; do
            dir=$(dirname "$file")
            grep "^@" "$file" | while read -r import; do
              path="${import#@}"
              if [ ! -f "$dir/$path" ]; then
                echo "::error file=$file::Broken import: $import"
                exit 1
              fi
            done
          done
          echo "All imports valid"
```

### With PR Comment

```yaml
      - name: Post audit summary
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');

            // Collect results
            const results = {
              files: 0,
              passed: 0,
              failed: 0,
              warnings: []
            };

            // Post comment
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## CLAUDE.md Audit Results

              - Files checked: ${results.files}
              - Passed: ${results.passed}
              - Failed: ${results.failed}

              ${results.warnings.length > 0 ? '### Warnings\n' + results.warnings.join('\n') : ''}
              `
            });
```

## VS Code Task

### tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Audit CLAUDE.md",
      "type": "shell",
      "command": "bash",
      "args": [
        "-c",
        "echo 'Auditing CLAUDE.md...' && wc -l CLAUDE.md && grep -c '^##' CLAUDE.md && echo 'Done'"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "problemMatcher": []
    },
    {
      "label": "Check CLAUDE.md secrets",
      "type": "shell",
      "command": "bash",
      "args": [
        "-c",
        "if grep -qE 'password|secret|token|api_key' CLAUDE.md; then echo 'WARNING: Potential secrets found:' && grep -nE 'password|secret|token|api_key' CLAUDE.md; else echo 'No secrets detected'; fi"
      ],
      "group": "test",
      "problemMatcher": []
    }
  ]
}
```

### Keyboard Shortcut

```json
// keybindings.json
{
  "key": "ctrl+shift+a",
  "command": "workbench.action.tasks.runTask",
  "args": "Audit CLAUDE.md"
}
```

## Husky + lint-staged

### Installation

```bash
npm install -D husky lint-staged
npx husky init
```

### package.json

```json
{
  "lint-staged": {
    "**/CLAUDE.md": [
      "bash -c 'wc -l \"$0\" | awk \"{if (\\$1 > 500) {print \\\"ERROR: \\\" \\$1 \\\" lines\\\"; exit 1}}\"'",
      "bash -c 'grep -qE \"password|secret|token\" \"$0\" && exit 1 || true'"
    ]
  }
}
```

### .husky/pre-commit

```bash
npx lint-staged
```

## GitLab CI

```yaml
# .gitlab-ci.yml
claude-md-audit:
  stage: test
  rules:
    - changes:
        - "**/CLAUDE.md"
  script:
    - |
      for file in $(find . -name "CLAUDE.md"); do
        echo "Checking $file"
        lines=$(wc -l < "$file")
        if [ "$lines" -gt 500 ]; then
          echo "ERROR: $file is $lines lines"
          exit 1
        fi
      done
    - echo "CLAUDE.md audit passed"
```

## Makefile Target

```makefile
.PHONY: audit-claude-md

audit-claude-md:
	@echo "Auditing CLAUDE.md files..."
	@find . -name "CLAUDE.md" -exec sh -c '\
		lines=$$(wc -l < "{}"); \
		if [ "$$lines" -gt 500 ]; then \
			echo "ERROR: {} is $$lines lines"; \
			exit 1; \
		fi; \
		echo "OK: {} ($$lines lines)"' \;
	@echo "Checking for secrets..."
	@! grep -rE "password|secret|token|api_key" --include="CLAUDE.md" . || \
		(echo "ERROR: Secrets detected" && exit 1)
	@echo "Audit complete"
```

## Best Practices

1. **Fail fast**: Check secrets before anything else
2. **Clear errors**: Include file path and line numbers
3. **PR feedback**: Post results as comments
4. **Gradual adoption**: Start with warnings, then enforce
5. **Skip when needed**: Allow `[skip audit]` in commit message
