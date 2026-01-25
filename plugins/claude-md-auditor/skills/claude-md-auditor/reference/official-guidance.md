# Official Anthropic Guidance

Complete compilation of official documentation from docs.claude.com (verified 2025-10-26).

## Memory Hierarchy

**Precedence Order** (highest to lowest):
1. Enterprise policy (managed by admins)
2. Project instructions (.claude/CLAUDE.md)
3. User instructions (~/.claude/CLAUDE.md)

**Loading Behavior**:
- All tiers loaded and merged
- Higher precedence overrides conflicts
- Enterprise can restrict user/project capabilities

## File Locations

| Tier | Location | Scope |
|------|----------|-------|
| Enterprise | Managed centrally | Organization-wide |
| Project | `.claude/CLAUDE.md` or `CLAUDE.md` in project root | Per-repository |
| User | `~/.claude/CLAUDE.md` | All user sessions |

## Import Functionality

**Syntax**: `@path/to/file.md`

**Limitations**:
- Maximum 5 import hops
- Only markdown files
- Relative paths from CLAUDE.md location
- No circular imports

**Example**:
```markdown
## Coding Standards
@docs/coding-standards.md

## API Guidelines
@docs/api-guidelines.md
```

## Official Best Practices

### Keep Them Lean
- Avoid verbose documentation
- Focus on project-specific information
- Claude already knows general programming

### Be Specific
- Concrete examples over vague guidance
- Actual commands, not descriptions
- Real patterns from your codebase

### Use Structure
- Clear markdown headers
- Organized sections
- Priority markers for critical items

## What NOT to Include

### Security Risks
- API keys, tokens, secrets
- Database credentials
- Private keys
- Internal infrastructure details

### Redundant Content
- Generic programming best practices
- Language documentation
- Framework tutorials
- Content Claude already knows

### Problematic Content
- Conflicting instructions
- Vague guidance ("write good code")
- Outdated information

## Validation Methods

### /memory Command
Shows what Claude currently has loaded from all CLAUDE.md files.

### /init Command
Generates or updates CLAUDE.md based on project analysis.

## Official Documentation Links

- Memory Files: https://docs.claude.com/en/docs/memory
- Best Practices: https://docs.claude.com/en/docs/claude-md-best-practices
- Import Syntax: https://docs.claude.com/en/docs/imports
