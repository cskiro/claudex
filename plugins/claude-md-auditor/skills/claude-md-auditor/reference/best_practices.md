# Community Best Practices for CLAUDE.md Configuration

> **Source**: Community wisdom, practitioner experience, and field-tested recommendations (not official Anthropic guidance)

This document contains best practices derived from the Claude Code community, real-world usage, and practical experience. While not officially mandated by Anthropic, these practices have proven effective across many projects.

---

## Size Recommendations

### Target Length: 100-300 Lines

**Rationale**:
- Represents approximately 1,500-4,500 tokens
- Accounts for roughly 1-2.5% of a 200K context window
- Small enough to avoid attention issues
- Large enough to be comprehensive
- Balances detail with context efficiency

**Community Consensus**:
- ✅ **Under 100 lines**: Potentially too sparse, may miss important context
- ✅ **100-300 lines**: Sweet spot for most projects
- ⚠️ **300-500 lines**: Acceptable for complex projects, but consider splitting
- ❌ **Over 500 lines**: Too verbose, consider using imports

**Note**: This is community-derived guidance, not an official Anthropic recommendation. Official guidance simply says "keep them lean."

### Token Budget Analysis

| CLAUDE.md Size | Tokens | % of 200K Context | Recommendation |
|----------------|--------|-------------------|----------------|
| 50 lines | ~750 | 0.4% | Too sparse |
| 100 lines | ~1,500 | 0.75% | Minimum viable |
| 200 lines | ~3,000 | 1.5% | Ideal |
| 300 lines | ~4,500 | 2.25% | Maximum recommended |
| 500 lines | ~7,500 | 3.75% | Consider splitting |
| 1000 lines | ~15,000 | 7.5% | Excessive |

---

## Content Organization

### Priority Positioning Strategy

Based on LLM research (not official Anthropic guidance), organize content by priority:

#### TOP Section (Highest Attention)
Place **mission-critical** standards here:
```markdown
# CRITICAL STANDARDS

## Security Requirements (MUST FOLLOW)
- Never commit secrets or API keys
- All authentication must use MFA
- Input validation required for all user inputs

## Code Quality Gates (MUST PASS)
- TypeScript strict mode enforced
- 80% test coverage minimum before PR merge
- No console.log in production code
```

#### MIDDLE Section (Lower Attention)
Place **nice-to-have** context and supporting information:
```markdown
## Nice-to-Have Practices
- Prefer functional components over class components
- Use meaningful variable names
- Keep functions under 50 lines when possible
```

#### BOTTOM Section (High Attention)
Place **important reference** information:
```markdown
## Key Commands (REFERENCE)
- npm run build: Build production bundle
- npm test: Run test suite
- npm run lint: Run linter

## Critical File Locations
- Config: /config/app.config.ts
- Types: /src/types/global.d.ts
```

**Rationale**: "Lost in the middle" research shows LLMs have U-shaped attention curves, with highest attention at the start and end of context.

---

## The 80/20 Rule for CLAUDE.md

### 80% Essential, 20% Supporting

**Essential (80%)** - Must-have information:
- Project-specific development standards
- Security requirements
- Testing requirements
- Critical file locations
- Common commands
- Non-obvious architectural decisions

**Supporting (20%)** - Nice-to-have context:
- Historical context
- Optional style preferences
- General best practices
- Team conventions

### Example Structure (200-line CLAUDE.md)

```markdown
# Project: MyApp

## CRITICAL STANDARDS (30 lines)
- Security requirements
- Must-follow coding standards
- Quality gates

## PROJECT CONTEXT (40 lines)
- Tech stack overview
- Architecture patterns
- Key dependencies

## DEVELOPMENT WORKFLOW (40 lines)
- Git workflow
- Testing requirements
- Deployment process

## CODE STANDARDS (30 lines)
- Language-specific rules
- Framework conventions
- Naming patterns

## COMMON ISSUES & SOLUTIONS (20 lines)
- Known gotchas
- Troubleshooting tips

## REFERENCE (40 lines)
- Common commands
- File locations
- Useful links
```

---

## Import Strategy

### When to Use Imports

#### Use Imports For:
- ✅ Lengthy architecture documentation (> 100 lines)
- ✅ Detailed API documentation
- ✅ Testing strategy documentation
- ✅ Deployment procedures
- ✅ Historical ADRs (Architecture Decision Records)

#### Keep in Main CLAUDE.md:
- ✅ Critical standards that must always be in context
- ✅ Common commands and workflows
- ✅ Project overview and tech stack
- ✅ Essential file locations

### Example Import Structure

```markdown
# CLAUDE.md (main file - 200 lines)

## Critical Standards (always in context)
- Security requirements
- Quality gates
- Testing requirements

## Project Overview
- Tech stack summary
- Architecture pattern

## Import Detailed Documentation
@docs/architecture/system-design.md
@docs/testing/testing-strategy.md
@docs/deployment/deployment-guide.md
@docs/api/api-documentation.md
@~/.claude/personal-preferences.md
```

**Benefits**:
- Keeps main CLAUDE.md lean
- Loads additional context on demand
- Easier to maintain separate documents
- Can reference external documentation

---

## Category Organization

### Recommended Section Structure

#### 1. Header & Overview (5-10 lines)
```markdown
# Project Name
Brief description of the project
Tech stack: React, TypeScript, Node.js, PostgreSQL
```

#### 2. Critical Standards (20-30 lines)
```markdown
## MUST-FOLLOW STANDARDS
- Security requirements
- Quality gates
- Non-negotiable practices
```

#### 3. Architecture (20-40 lines)
```markdown
## Architecture
- Patterns used
- Key decisions
- Module structure
```

#### 4. Development Workflow (20-30 lines)
```markdown
## Development Workflow
- Git branching strategy
- Commit conventions
- PR requirements
```

#### 5. Code Standards (30-50 lines)
```markdown
## Code Standards
- Language-specific rules
- Framework conventions
- Testing requirements
```

#### 6. Common Tasks (20-30 lines)
```markdown
## Common Tasks
- Build commands
- Test commands
- Deployment commands
```

#### 7. Reference Information (20-40 lines)
```markdown
## Reference
- File locations
- Environment setup
- Troubleshooting
```

---

## Version Control Best Practices

### Project-Level CLAUDE.md

#### Commit to Source Control
- ✅ **DO** commit `./CLAUDE.md` or `./.claude/CLAUDE.md` to git
- ✅ **DO** include in code reviews
- ✅ **DO** update alongside code changes
- ✅ **DO** document major changes in commit messages

#### Review Standards
```markdown
## PR Checklist for CLAUDE.md Changes
- [ ] Removed outdated information
- [ ] Added context for new features/patterns
- [ ] Updated commands if changed
- [ ] Verified no secrets committed
- [ ] Kept file under 300 lines
- [ ] Used imports for lengthy docs
```

### User-Level CLAUDE.md

#### Keep Personal Preferences Separate
- ✅ **DO** use `~/.claude/CLAUDE.md` for personal preferences
- ✅ **DO NOT** commit user-level files to project repos
- ✅ **DO** share useful patterns with team (move to project-level)

---

## Naming Conventions

### Section Headers

Use clear, action-oriented headers:

#### Good Examples:
```markdown
## MUST FOLLOW: Security Requirements
## How to Build and Deploy
## Common Troubleshooting Solutions
## File Structure Overview
```

#### Avoid:
```markdown
## Miscellaneous
## Other
## Notes
## TODO
```

### Emphasis Techniques

Use consistent emphasis for priority levels:

```markdown
## CRITICAL: [thing that must never be violated]
## IMPORTANT: [thing that should be followed]
## RECOMMENDED: [thing that's nice to have]
## REFERENCE: [lookup information]
```

---

## Maintenance Cadence

### When to Update CLAUDE.md

#### Update Immediately:
- New critical security requirements
- Major architecture changes
- New must-follow standards
- Breaking changes in workflow

#### Update During Sprint Planning:
- New features that introduce patterns
- Updated dependencies with new conventions
- Deprecated practices to remove

#### Update Quarterly:
- Remove outdated information
- Consolidate duplicate guidance
- Optimize length and structure
- Review for clarity

### Staleness Detection

Signs your CLAUDE.md needs updating:
- ⚠️ References to deprecated tools or frameworks
- ⚠️ Outdated command examples
- ⚠️ Broken file paths
- ⚠️ Conflicting instructions
- ⚠️ Information duplicated in multiple sections

---

## Multi-Project Strategies

### User-Level Patterns

For developers working across multiple projects:

```markdown
# ~/.claude/CLAUDE.md

## Personal Development Standards
- TDD approach required
- Write tests before implementation
- No console.log statements

## Preferred Tools
- Use Vitest for testing
- Use ESLint with recommended config
- Use Prettier with 2-space indent

## Communication Style
- Be concise and direct
- Provide context for decisions
- Flag breaking changes prominently
```

### Project-Level Focus

Each project's CLAUDE.md should:
- ✅ Override user-level preferences where needed
- ✅ Add project-specific context
- ✅ Define team-wide standards
- ❌ Avoid duplicating user-level preferences

---

## Testing Your CLAUDE.md

### Validation Checklist

#### Structure Test
- [ ] Under 300 lines (or using imports)
- [ ] Clear section headers
- [ ] Bullet points for lists
- [ ] Code blocks formatted correctly

#### Content Test
- [ ] No secrets or sensitive information
- [ ] Specific instructions (not generic)
- [ ] Project-specific context
- [ ] No outdated information
- [ ] No broken file paths

#### Effectiveness Test
- [ ] Start a new Claude Code session
- [ ] Verify standards are followed without re-stating
- [ ] Test that Claude references CLAUDE.md correctly
- [ ] Confirm critical standards enforced

---

## Advanced Techniques

### Conditional Instructions

Use clear conditions for context-specific guidance:

```markdown
## Testing Standards

### For New Features
- Write tests BEFORE implementation (TDD)
- Integration tests required for API endpoints
- Accessibility tests for UI components

### For Bug Fixes
- Add regression test that would have caught the bug
- Update existing tests if behavior changed
- Ensure fix doesn't break other tests
```

### Progressive Disclosure

Organize from high-level to detailed:

```markdown
## Architecture

### Overview
- Clean Architecture pattern
- Feature-based modules
- Hexagonal architecture for API layer

### Module Structure
├── features/           # Feature modules
│   ├── auth/          # Authentication feature
│   ├── dashboard/     # Dashboard feature
│   └── settings/      # Settings feature
├── lib/               # Shared libraries
└── infrastructure/    # Infrastructure layer

### Detailed Patterns
(Include or import detailed documentation)
```

---

## Anti-Patterns to Avoid

### Common Mistakes

#### ❌ Copy-Paste from Documentation
```markdown
## React Hooks
React Hooks allow you to use state and other React features
without writing a class...
[200 lines of React documentation]
```
**Problem**: Claude already knows this. Wastes context.

#### ❌ Excessive Detail
```markdown
## Git Workflow
1. First, open your terminal
2. Navigate to the project directory using cd
3. Type git status to see your changes
4. Type git add to stage files...
[50 lines of basic git commands]
```
**Problem**: Claude knows git. Be specific about YOUR workflow only.

#### ❌ Vague Instructions
```markdown
## Code Quality
- Write good code
- Make it clean
- Follow best practices
```
**Problem**: Not actionable. Be specific.

#### ✅ Better Approach
```markdown
## Code Quality Standards
- TypeScript strict mode: no `any` types
- Function length: max 50 lines
- Cyclomatic complexity: max 10
- Test coverage: minimum 80%
- No console.log in src/ directory (use logger instead)
```

---

## Success Metrics

### How to Know Your CLAUDE.md is Effective

#### Good Signs:
- ✅ Claude consistently follows your standards without prompting
- ✅ New team members onboard faster
- ✅ Fewer "why did Claude do that?" moments
- ✅ Code reviews show consistent patterns
- ✅ Standards violations caught early

#### Bad Signs:
- ❌ Constantly repeating yourself in prompts
- ❌ Claude ignores your standards
- ❌ Instructions are ambiguous
- ❌ Team members confused about standards
- ❌ CLAUDE.md conflicts with actual practices

---

## Real-World Examples

### Startup/Small Team (150 lines)
- Focus on essential standards
- Include critical workflows
- Prioritize speed over perfection

### Enterprise Project (250 lines + imports)
- Comprehensive security standards
- Detailed compliance requirements
- Links to additional documentation
- Multi-environment considerations

### Open Source Project (200 lines)
- Contribution guidelines
- Code review process
- Community standards
- Documentation requirements

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-26
**Status**: Community best practices (not official Anthropic guidance)
**Confidence**: Based on field experience and practitioner reports
