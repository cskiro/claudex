# Official Anthropic Guidance for CLAUDE.md Configuration

> **Source**: Official Anthropic documentation from docs.claude.com (verified 2025-10-26)

This document compiles all official guidance from Anthropic for creating and maintaining CLAUDE.md memory files in Claude Code.

## Memory Hierarchy

### Three-Tier System

Claude Code uses a hierarchical memory system with clear precedence:

1. **Enterprise Policy Memory** (Highest Priority)
   - **Locations**:
     - macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
     - Linux: `/etc/claude-code/CLAUDE.md`
     - Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`
   - **Purpose**: Organization-wide instructions managed by IT/DevOps
   - **Access**: Typically managed centrally, not by individual developers

2. **Project Memory** (Medium Priority)
   - **Locations**:
     - `./CLAUDE.md` (project root)
     - `./.claude/CLAUDE.md` (hidden directory in project root)
   - **Purpose**: Team-shared project instructions committed to source control
   - **Access**: All team members can edit, checked into git

3. **User Memory** (Lowest Priority)
   - **Location**: `~/.claude/CLAUDE.md`
   - **Purpose**: Personal preferences that apply across all projects
   - **Access**: Individual developer only

### Precedence Rules

- **Higher-level memories load first** and provide a foundation that more specific memories build upon
- **Settings are merged**: More specific settings add to or override broader ones
- **Recursive discovery**: Claude Code starts in the current working directory and recurses up to (but not including) the root directory, reading any CLAUDE.md files it finds

**Source**: [Memory Management Documentation](https://docs.claude.com/en/docs/claude-code/memory)

---

## File Loading Behavior

### Launch-Time Loading

- **CLAUDE.md files are loaded at startup** when Claude Code is launched
- Memory files in **parent directories** are loaded at startup
- Memories in **subdirectories** load dynamically when Claude accesses files in those locations
- This loading happens **separately from conversation history**

**Source**: [Memory Lookup Documentation](https://docs.claude.com/en/docs/claude-code/memory)

---

## Import Functionality

### Syntax

CLAUDE.md files can import additional files using the `@path/to/import` syntax:

```markdown
# Project Standards
@docs/coding-standards.md
@docs/testing-guidelines.md
@~/.claude/my-personal-preferences.md
```

### Limitations

- **Maximum import depth**: 5 hops
- **Prevents circular imports**: Claude Code detects and prevents infinite loops
- **Purpose**: Allows you to include documentation without bloating the main memory file

**Source**: [Memory Imports Documentation](https://docs.claude.com/en/docs/claude-code/memory)

---

## Official Best Practices

### Keep Memory Files Lean

> "Memory files are read at the beginning of each coding session, which is why it's important to keep them lean as they take up context window space."

**Key Principle**: Concise and human-readable

### Be Specific

- ✅ **Good**: "Use 2-space indentation"
- ❌ **Bad**: "Format code properly"

**Rationale**: Specific instructions are more actionable and less ambiguous

### Use Structure to Organize

- **Format**: Each individual memory as a bullet point
- **Group**: Related memories under descriptive headings
- **Example**:
  ```markdown
  ## Code Style
  - Use 2-space indentation
  - Use ES modules syntax
  - Destructure imports when possible

  ## Testing
  - Run tests with: npm test
  - Minimum 80% coverage required
  ```

### Strike a Balance

- Avoid wasting tokens on too many details
- Don't include generic information Claude already understands
- Focus on project-specific context and requirements

**Source**: [Memory Best Practices Documentation](https://docs.claude.com/en/docs/claude-code/memory), [Best Practices Blog](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## What NOT to Include

### ❌ Basic Programming Concepts

Claude already understands fundamental programming principles. Don't include:
- Language syntax basics
- Common design patterns
- Standard library documentation
- General programming advice

### ❌ Information Covered in Official Documentation

Don't duplicate content from official docs that Claude has been trained on:
- Framework documentation (React, Vue, etc.)
- Language specifications (JavaScript, TypeScript, etc.)
- Standard tool documentation (npm, git, etc.)

### ❌ Changing Details

Avoid information that changes frequently:
- Current sprint tasks (use issue trackers instead)
- Temporary project status
- Time-sensitive information
- Specific bug references

### ❌ Secret Information

**Never include**:
- API keys or tokens
- Passwords or credentials
- Private keys
- Connection strings
- Any sensitive information

**Note**: .env files should be in .gitignore, and CLAUDE.md should never contain secrets

**Source**: [Memory Best Practices](https://docs.claude.com/en/docs/claude-code/memory), [Security Standards](https://docs.claude.com/en/docs/claude-code/settings)

---

## Context Management

### Auto-Compaction

- **Behavior**: "Your context window will be automatically compacted as it approaches its limit"
- **Purpose**: Allows you to continue working indefinitely
- **Customization**: You can add summary instructions to CLAUDE.md to customize compaction behavior
- **Hook**: PreCompact hook runs before compaction operation

### Memory Persistence Across Sessions

- CLAUDE.md files persist across sessions (loaded at launch)
- Memory files maintain their content through compaction
- You can customize how compaction summarizes conversations via CLAUDE.md

**Source**: [Cost Management Documentation](https://docs.claude.com/en/docs/claude-code/costs), [Hooks Reference](https://docs.claude.com/en/docs/claude-code/hooks)

---

## Validation Methods

### Official Commands

#### `/memory` Command
- **Purpose**: View and edit CLAUDE.md memory files
- **Usage**: Type `/memory` in Claude Code to see all loaded memory files
- **Features**:
  - Shows file paths for each memory location
  - Allows direct editing of memory files
  - Confirms which files are loaded

#### `/init` Command
- **Purpose**: Bootstrap CLAUDE.md file for your project
- **Usage**: Run `/init` in a new project
- **Features**:
  - Analyzes your codebase
  - Generates initial CLAUDE.md with project information
  - Includes conventions and frequently used commands

**Source**: [Slash Commands Reference](https://docs.claude.com/en/docs/claude-code/slash-commands)

### CLI Debug Flags

While there is no `/debug` slash command, Claude Code offers CLI flags:

- `--debug`: Enable debug mode with detailed output
- `--mcp-debug`: Debug MCP server connections
- `--verbose`: Enable verbose logging

**Source**: Claude Code CLI documentation

---

## Content Recommendations

### What TO Include

#### Project-Specific Context
```markdown
# Project Overview
- Monorepo using npm workspaces
- TypeScript strict mode enforced
- Testing with Vitest

## Architecture
- Feature-based folder structure
- Clean Architecture pattern
- API layer in /src/api
```

#### Development Standards
```markdown
## Code Quality
- TypeScript strict mode required
- No `any` types allowed
- 80% test coverage minimum
- No console.log in production code

## Git Workflow
- Branch pattern: feature/{name}
- Conventional commit messages
- Pre-commit hooks enforced
```

#### Common Commands
```markdown
## Bash Commands
- npm run build: Build the project
- npm test: Run tests with coverage
- npm run typecheck: Run TypeScript compiler checks
```

#### Important File Locations
```markdown
## Key Files
- Config: /config/app.config.ts
- Constants: /src/constants/index.ts
- Types: /src/types/global.d.ts
```

**Source**: [Best Practices Blog](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## Integration with Settings

### Relationship to settings.json

While CLAUDE.md provides instructions and context, `settings.json` provides programmatic control:

#### Settings Hierarchy
1. Enterprise managed policies (highest)
2. Command line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

#### Complementary Usage
- **CLAUDE.md**: Instructions, context, standards, preferences
- **settings.json**: Permissions, hooks, tool access, environment variables

**Example** of settings.json:
```json
{
  "permissions": {
    "allow": ["Bash(npm run test:*)"],
    "deny": ["Write(./.env)", "Write(./production.config.*)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write(*.py)",
        "hooks": [{"type": "command", "command": "python -m black $file"}]
      }
    ]
  }
}
```

**Source**: [Settings Documentation](https://docs.claude.com/en/docs/claude-code/settings)

---

## Iterative Improvement

### Living Document Philosophy

- **Use `#` shortcut**: Quickly add instructions during conversations
- **Iterate and refine**: Test what produces the best instruction following
- **Share with team**: Commit improvements to source control
- **Add emphasis**: Use keywords like "IMPORTANT" or "YOU MUST" for critical standards

### Optimization Techniques

Consider using a "prompt improver" to enhance instructions:
- Make vague instructions more specific
- Add context where needed
- Improve clarity and organization

**Source**: [Best Practices Blog](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## Summary of Official Guidelines

### ✅ DO

1. Keep CLAUDE.md files **lean and concise**
2. Be **specific** in instructions (not generic)
3. Use **structured markdown** with headings and bullets
4. Use **imports** for large documentation
5. Focus on **project-specific** context
6. **Iterate and refine** based on effectiveness
7. Use **hierarchy** appropriately (Enterprise → Project → User)

### ❌ DON'T

1. Include basic programming concepts
2. Duplicate official documentation
3. Add changing/temporary information
4. Include secrets or sensitive information
5. Make memory files excessively long
6. Use vague or generic instructions
7. Create circular import loops

---

## Validation Checklist

When auditing a CLAUDE.md file, verify:

- [ ] Proper file location (Enterprise/Project/User tier)
- [ ] No secrets or sensitive information
- [ ] Specific (not generic) instructions
- [ ] Structured with headings and bullets
- [ ] No duplicated official documentation
- [ ] Import syntax correct (if used)
- [ ] Maximum 5-hop import depth
- [ ] No circular imports
- [ ] Lean and concise (not excessively verbose)
- [ ] Project-specific context (not generic advice)
- [ ] Can be validated via `/memory` command

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-26
**Based On**: Official Anthropic documentation from docs.claude.com
**Verification Status**: All claims verified against official sources
