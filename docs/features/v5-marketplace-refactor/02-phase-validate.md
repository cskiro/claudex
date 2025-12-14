# Phase 2: Validation & Testing

## Objective

Update `marketplace.json` with restored plugin definitions and validate the marketplace configuration.

## Plugin Definitions to Add

### analysis-tools
```json
{
  "name": "analysis-tools",
  "description": "Code quality, security, and architecture analysis tools for comprehensive codebase auditing",
  "source": "./",
  "strict": false,
  "skills": [
    "./skills/codebase-auditor",
    "./skills/bulletproof-react-auditor",
    "./skills/accessibility-audit"
  ]
}
```

### release-management
```json
{
  "name": "release-management",
  "description": "Automated release workflows, versioning, and deployment readiness tools",
  "source": "./",
  "strict": false,
  "skills": [
    "./skills/semantic-release-tagger"
  ]
}
```

### planning-tools
```json
{
  "name": "planning-tools",
  "description": "Visual planning and documentation tools including ASCII diagrams",
  "source": "./",
  "strict": false,
  "skills": [
    "./skills/ascii-diagram-creator"
  ]
}
```

### benchmarking
```json
{
  "name": "benchmarking",
  "description": "Benchmark report creation with diagrams and PDF export for AI/ML research",
  "source": "./",
  "strict": false,
  "skills": [
    "./skills/benchmark-report-creator"
  ]
}
```

### meta-tools (update)
Add `insight-skill-generator` to existing meta-tools:
```json
"skills": [
  "./skills/skill-creator",
  "./skills/skill-isolation-tester",
  "./skills/insight-skill-generator"
]
```

## Validation Steps

1. [ ] Update `marketplace.json` with plugin definitions
2. [ ] Bump version to `5.0.0`
3. [ ] Run validation script:
   ```bash
   python3 scripts/validate-marketplace.py
   ```
4. [ ] Verify all skill paths resolve correctly

## Expected Output

```
Marketplace validation passed!
- 10 plugins found
- 23 skills registered
- All paths valid
```

## Test Plugin Installation

```bash
# Clear cache
rm -rf ~/.claude/plugins/cache/claudex

# Reinstall marketplace
/plugin marketplace remove claudex
/plugin marketplace add cskiro/claudex

# Install all plugins
/plugin install analysis-tools@claudex
/plugin install release-management@claudex
/plugin install planning-tools@claudex
/plugin install benchmarking@claudex
```

## Success Criteria

- [ ] `validate-marketplace.py` passes with exit code 0
- [ ] All 10 plugins install without errors
- [ ] No "Plugin not found" errors in /plugin menu
