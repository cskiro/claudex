# Claude Code Skill Anatomy

A comprehensive guide to understanding, creating, and optimizing Claude Code skills.

> **Sources**: This document synthesizes official Anthropic documentation from multiple sources. See [Documentation Sources](#documentation-sources) for details.

> **Claudex Note**: This marketplace uses a nested category structure: `skills/<category>/<skill-name>/SKILL.md`. All paths in this document reflect this structure.

## Table of Contents

1. [What is a Skill?](#what-is-a-skill)
2. [File Structure](#file-structure)
3. [SKILL.md Anatomy](#skillmd-anatomy)
4. [Frontmatter Specification](#frontmatter-specification)
5. [Discovery & Triggering](#discovery--triggering)
6. [Progressive Disclosure Pattern](#progressive-disclosure-pattern)
7. [Best Practices](#best-practices)
8. [Anti-Patterns](#anti-patterns)
9. [Tool Access Control](#tool-access-control)
10. [Testing & Validation](#testing--validation)
11. [Quality Checklist](#quality-checklist)
12. [Critical Insights (Repeated Across Sources)](#-critical-insights-repeated-across-sources)
13. [Gaps & Inconsistencies](#️-gaps--inconsistencies)
14. [Documentation Sources](#documentation-sources)

---

## What is a Skill?

A **skill** is a reusable capability package that Claude Code can discover and apply automatically based on context. Unlike slash commands (explicitly invoked with `/command`), skills are **model-invoked** — Claude autonomously decides when to use them based on semantic matching.

### The Core Distinction

> "**Projects say 'here's what you need to know.' Skills say 'here's how to do things.'**"
> — Anthropic Documentation

Skills are **portable expertise** — specialized training materials that teach Claude how to perform specific tasks. They work across any conversation and any project, unlike project-specific context.

### Skills vs Slash Commands

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| **Invocation** | Automatic (model-invoked) | Manual (`/command`) |
| **Structure** | Directory with SKILL.md + resources | Single `.md` file |
| **Discovery** | Semantic matching on description | Explicit typing |
| **Best for** | Complex workflows, team standards | Quick snippets, templates |
| **Context efficiency** | Files loaded on-demand | All content loaded at once |
| **Persistence** | Across conversations | Single conversation |

### Skills in the Claude Ecosystem

| Feature | Skills | Prompts | Projects | Subagents | MCP |
|---------|--------|---------|----------|-----------|-----|
| **Persistence** | Across conversations | Single conversation | Within project | Across sessions | Continuous |
| **When it loads** | Dynamically, as needed | Each turn | Always in project | When invoked | Always available |
| **Best for** | Specialized expertise | Quick requests | Centralized context | Specialized tasks | Data access |

**Key combinations:**
- **Skills + Subagents**: Specialized agents leverage portable expertise
- **Skills + Projects**: Persistent context with dynamic capabilities

### Skills vs CLAUDE.md

| Aspect | Skills | CLAUDE.md |
|--------|--------|-----------|
| **Scope** | Cross-repo, reusable knowledge | Project-specific guidance |
| **Loading** | Progressive/on-demand | Always loaded |
| **Platforms** | claude.ai, Claude Code, Claude API | Claude Code only |
| **Content** | Can include executable code + references | Markdown only |
| **Use cases** | Data schemas, company standards, domain expertise | Coding conventions, local workflows |

> "Skills let you encode institutional knowledge that works across teams and platforms."
> — Anthropic Documentation

### Storage Locations (Three Tiers)

| Location | Path | Scope |
|----------|------|-------|
| **Personal** | `~/.claude/skills/skill-name/` | Available across all projects |
| **Project** | `.claude/skills/skill-name/` | Shared with team via git |
| **Plugin/Marketplace** | `skills/<category>/<skill-name>/` | Auto-installed via marketplace |

---

## File Structure

### Minimal Skill (Single File)

```
skill-name/
└── SKILL.md                    # Required - main manifest
```

### Standard Skill

```
skill-name/
├── SKILL.md                    # Required - lean entry point (~100-200 lines)
├── README.md                   # Optional - user documentation
├── workflow/                   # Optional - step-by-step procedures
│   ├── phase-1-setup.md
│   └── phase-2-execution.md
├── reference/                  # Optional - detailed documentation
│   ├── api-reference.md
│   └── best-practices.md
└── examples/                   # Optional - concrete examples
    └── sample-output.md
```

### Complex Skill (Claudex Standard)

```
skill-name/
├── SKILL.md                    # Lean menu/router (~100-200 lines)
├── README.md                   # User documentation
├── CHANGELOG.md                # Version history (required for marketplace)
├── workflow/                   # Phased procedures
│   ├── phase-0-context.md
│   ├── phase-1-analysis.md
│   ├── phase-2-execution.md
│   └── phase-3-output.md
├── reference/                  # Deep documentation
│   ├── api-reference.md
│   ├── best-practices.md
│   └── troubleshooting.md
├── examples/                   # Sample outputs/usage
│   ├── example-1.md
│   └── example-2.md
├── templates/                  # Reusable templates
│   └── output-template.md
├── scripts/                    # Automation utilities
│   └── helper.sh
├── data/                       # Reference data
│   └── categories.yaml
└── modes/                      # Mode-specific workflows (for multi-mode skills)
    ├── quick-mode.md
    └── thorough-mode.md
```

**Note**: Claudex does NOT require `plugin.json` files in skill directories. The marketplace.json is the single source of truth.

---

## SKILL.md Anatomy

The SKILL.md file is the **only required file** and serves as the skill's entry point.

### Recommended Content Organization

| Section | Purpose | Content |
|---------|---------|---------|
| **Quick Start Workflow** | Step-by-step for common tasks | Numbered steps with decision points |
| **Standard Patterns** | Business logic, required filters | Rules that always apply |
| **Knowledge Base** | Pointers to reference files | Organized by category |

> "Information should live in either SKILL.md or reference files but not both, so keep SKILL.md lean."
> — Anthropic Documentation

### Structure Template

```markdown
---
name: skill-name
version: 0.1.0
description: Clear description of what AND when. Include trigger phrases and boundaries.
---

# Skill Name

Brief overview (2-3 sentences).

## When to Use

**Trigger Phrases**:
- "phrase that activates this skill"
- "another trigger phrase"

**Use Cases**:
- Specific use case 1
- Specific use case 2

**NOT for**:
- What this skill should not be used for
- Explicit boundaries

## Quick Reference

[Decision matrix or quick routing table]

## Workflow

| Phase | Purpose | Details |
|-------|---------|---------|
| 1 | Setup | → [workflow/phase-1.md](workflow/phase-1.md) |
| 2 | Execution | → [workflow/phase-2.md](workflow/phase-2.md) |

## Reference Materials

- [Best Practices](reference/best-practices.md)
- [Examples](examples/)

---

**Version**: 1.0.0 | **Author**: Name
```

---

## Frontmatter Specification

YAML frontmatter enclosed in `---` delimiters at the start of SKILL.md.

### Required Fields

| Field | Type | Max Length | Description |
|-------|------|------------|-------------|
| `name` | string | 64 chars | Unique identifier (lowercase, hyphens, numbers only) |
| `description` | string | 1024 chars (~100 words) | **CRITICAL** - What it does AND when to use it |

> "Claude maintains a lightweight index of available skills (names and descriptions, about 100 words each)."
> — Anthropic Documentation

**Official Spec Requirements** (from `anthropics/skills` repo):
- `name`: "hyphen-case, restricted to lowercase Unicode alphanumeric + hyphen"
- `name` **must align with the containing directory name**
- `description`: "Explains the skill's functionality and appropriate use cases for Claude"

**Guideline**: Aim for ~100 words for optimal indexing; hard limit is 1024 characters.

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Semantic version (e.g., "0.1.0") - **recommended for marketplace** |
| `author` | string | Skill creator |
| `created` | date | Creation date (YYYY-MM-DD) |
| `updated` | date | Last update date |
| `triggers` | list | Explicit trigger phrases (for documentation) |
| `allowed-tools` | string | Comma-separated tool restrictions (Claude Code only) |
| `license` | string | Licensing terms (keep concise) — **from official spec** |
| `metadata` | object | Key-value string pairs for additional properties — **from official spec** |

> **Note on `metadata`**: "Recommended to use reasonably unique keys to prevent conflicts" — Official Spec

### Example Frontmatter

```yaml
---
name: pdf-processor
version: 1.2.0
description: Extract text and tables from PDFs, fill form fields, merge documents. Use when working with PDF files, forms, document extraction, or batch PDF operations. NOT for simple viewing or format conversion.
author: Connor
created: 2025-01-15
updated: 2025-03-20
triggers:
  - extract PDF text
  - fill PDF form
  - merge PDFs
allowed-tools: Read, Grep, Glob, Bash
---
```

---

## Discovery & Triggering

### How Skills Are Discovered

Claude analyzes the `description` field to determine skill relevance. **The name and description are the ONLY parts that influence triggering.**

### Writing Effective Descriptions

**Bad** (too vague):
```yaml
description: Helps with documents
```

**Good** - Two valid patterns exist:

**Pattern A: Official Anthropic Style (Capability-First)**
```yaml
description: Comprehensive PDF manipulation toolkit for extracting text and
  tables, creating new PDFs, merging/splitting documents, and handling forms.
  When Claude needs to fill in a PDF form or programmatically process,
  generate, or analyze PDF documents at scale.
```

**Pattern B: Claudex Convention (Trigger-First)**
```yaml
description: Use PROACTIVELY when working with PDF files, forms, or document
  extraction. Extracts text and tables, fills form fields, merges documents.
  NOT for simple viewing or image-based PDFs without OCR.
```

> **Note**: Both patterns are valid. Pattern A follows Anthropic's production skills (pdf, docx, xlsx). Pattern B emphasizes proactive triggering for marketplace discovery.

### Description Components

1. **Capabilities** (verbs/actions): "Extract", "Generate", "Analyze"
2. **Trigger context** (when to activate): "When Claude needs to...", "Use when...", "Use PROACTIVELY when..."
3. **Domain specifics**: File types, frameworks, technologies
4. **Boundaries** (explicit): "NOT for...", "Not suitable for..."

### Testing Discovery

Ask questions that match your description:
```
# If description mentions "PDF files"
User: "Can you help me extract text from this PDF?"
# Claude should automatically activate the skill
```

---

## Progressive Disclosure Pattern

**Core Principle**: Keep SKILL.md lean (~100-200 lines) and load detailed content on-demand.

### Three-Tier Loading System

Skills use a **progressive disclosure mechanism** with three tiers:

| Tier | What Loads | Token Cost | When |
|------|------------|------------|------|
| **1. Metadata** | Name + description | ~100 tokens | Always (for discovery) |
| **2. Instructions** | SKILL.md content | <5k tokens | When skill is relevant |
| **3. Bundled files** | Reference docs, scripts | Variable | Only as needed |

> "You can have many Skills available without overwhelming Claude's context window."
> — Anthropic Documentation

### Why Progressive Disclosure?

| Approach | Context Usage | Performance |
|----------|---------------|-------------|
| Monolithic | 100% loaded always | Slow, wasteful |
| Progressive | ~15% loaded initially | Fast, efficient |

**RAG Support**: When knowledge approaches context limits, skills support RAG (Retrieval Augmented Generation), enabling capacity expansion **by up to 10x**.

### Implementation

**SKILL.md** acts as a **menu/router**:
```markdown
## Workflow

1. **Setup** - Install dependencies → [workflow/setup.md](workflow/setup.md)
2. **Analysis** - Run scans → [workflow/analysis.md](workflow/analysis.md)
3. **Reporting** - Generate output → [workflow/reporting.md](workflow/reporting.md)

## Reference

- [API Reference](reference/api.md)
- [Troubleshooting](reference/troubleshooting.md)
```

Claude reads linked files **only when needed** for the current task.

### Directory Conventions

| Directory | Purpose | Load Timing |
|-----------|---------|-------------|
| `workflow/` | Step-by-step procedures | When executing that phase |
| `reference/` | Detailed documentation | When deep-diving on topic |
| `examples/` | Concrete examples | When user needs examples |
| `templates/` | Reusable outputs | When generating output |
| `data/` | Reference data (YAML, JSON) | When data lookup needed |
| `scripts/` | Automation utilities | When executing automation |

### Reference File Content Categories

Organize reference files by these common categories:

| Category | Content | Example |
|----------|---------|---------|
| **Table schemas** | Column names, data types, descriptions | `references/tables.md` |
| **Standard filters** | WHERE clauses, conditions that always apply | `references/filters.md` |
| **Metric definitions** | Exact formulas with examples | `references/metrics.md` |
| **Query patterns** | SQL snippets, code templates | `references/queries.md` |
| **Edge cases** | Known quirks, decision trees | `references/edge-cases.md` |

---

## Best Practices

### 0. When to Create a Skill (The 5/10 Rule)

> "Don't write skills speculatively. Build them when you have real, repeated tasks."
> — Anthropic Documentation

**Threshold questions:**
- Have I done this task at least **5 times**?
- Will I do it at least **10 more times**?

If yes to both → create a skill.

**Good candidates:**
- Recurring prompts you type repeatedly across conversations
- Organizational standards (brand guidelines, compliance procedures)
- Domain expertise (Excel formulas, PDF manipulation)
- Document templates

**Candidate Skill Criteria** (from official docs):
- **Cross-repo relevant** — Applies across multiple projects
- **Multi-audience value** — Benefits both technical and non-technical users
- **Stable patterns** — Procedures unlikely to change frequently

### 1. One Skill = One Capability

**Good** (focused):
- "PDF form filling"
- "Git commit message generation"
- "WCAG accessibility auditing"

**Bad** (too broad):
- "Document processing" → split by document type
- "Code tools" → split by specific capability

### 2. Description is King

> "The description is the most critical component for skill discovery."

Include:
- Specific verbs (extract, generate, analyze, audit)
- Trigger phrases users actually say
- File types, frameworks, or domains
- Explicit "NOT for" boundaries

### 3. Use Decision Matrices

Help Claude route quickly:
```markdown
## Quick Decision Matrix

| User Request | Mode | Action |
|--------------|------|--------|
| "quick audit" | Fast | Automated scan only |
| "full audit" | Thorough | Manual + automated |
| "fix issues" | Remediation | Generate fixes |
```

### 4. Phase-Based Workflows

Structure complex skills with discrete phases:
```markdown
## Workflow

| Phase | Purpose | Output |
|-------|---------|--------|
| 0 | Context Analysis | Requirements summary |
| 1 | Execution | Raw results |
| 2 | Reporting | Formatted output |
```

Each phase should have:
- Clear inputs
- Defined outputs
- Common issues/troubleshooting

### 5. Include Mandatory Completion Criteria

For complex skills, add completion checklists:
```markdown
## Completion Checklist

- [ ] Phase 1 complete: data gathered
- [ ] Phase 2 complete: analysis run
- [ ] Output generated in correct format
- [ ] User offered integration options
```

### 6. Proactive Triggering Guidance

Document when Claude should offer the skill proactively:
```markdown
## Use PROACTIVELY When

- User creates a feature branch (`feature/*`)
- User asks "how should I structure..."
- User mentions "visualize" or "diagram"
```

### 7. Production Patterns (from Anthropic's docx skill)

**Decision Tree Routing** in SKILL.md:
```markdown
## Workflow Decision Tree

| Task | Workflow | Reference |
|------|----------|-----------|
| Reading/Analyzing | Text extraction | [extraction.md](extraction.md) |
| Creating New | docx-js workflow | [docx-js.md](docx-js.md) |
| Editing Existing | OOXML manipulation | [ooxml.md](ooxml.md) |
```

**Mandatory Documentation Review**:
```markdown
1. **MANDATORY - READ ENTIRE FILE**: Read [reference.md] without range limits
2. Create implementation based on documentation
3. Verify results
```

**Batching Strategy**: Organize changes into 3-10 logical batches for manageability

**Verification Pattern**: Always include verification steps (e.g., "Convert to markdown, grep for confirmation")

---

## Anti-Patterns

### ❌ Vague Descriptions

```yaml
# Bad
description: Helps with data
```
**Problem**: Won't trigger reliably

### ❌ Monolithic SKILL.md

```markdown
# Bad - 500+ lines in single file
## Phase 1
[300 lines of detailed steps...]
## Phase 2
[200 lines more...]
```
**Problem**: Wastes context window, slow loading

### ❌ Missing Boundaries

```yaml
# Bad - no "NOT for" section
description: Processes documents
```
**Problem**: Triggers inappropriately

### ❌ No Progressive Disclosure

```markdown
# Bad - everything inline
## API Reference
[100 lines of API docs]
## Examples
[50 lines of examples]
```
**Problem**: Loads everything even when not needed

### ❌ Undocumented Dependencies

```markdown
# Bad - no requirements listed
Just run the script...
```
**Problem**: Skill fails silently

### ❌ Inconsistent File Paths

```markdown
# Bad - Windows-style paths
See `workflow\phase-1.md`
```
**Problem**: Cross-platform issues. Always use forward slashes.

---

## Tool Access Control

Restrict which tools Claude can use without permission via `allowed-tools`.

### Syntax

```yaml
---
name: code-reviewer
description: Read-only code review and analysis
allowed-tools: Read, Grep, Glob
---
```

### Available Tools

| Tool | Purpose |
|------|---------|
| `Read` | View file contents |
| `Write` | Create new files |
| `Edit` | Modify existing files |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `Bash` | Execute shell commands |

### Use Cases for Restrictions

| Skill Type | Recommended Tools | Rationale |
|------------|-------------------|-----------|
| Auditing/Review | `Read, Grep, Glob` | Read-only, no modifications |
| Code Generation | `Read, Write, Grep, Glob` | Can create, not edit |
| Full Development | All tools | Complete access |

**Note**: `allowed-tools` only works in Claude Code Skills, not Agent SDK.

---

## Testing & Validation

### Testing Matrix (Three Scenarios)

| Scenario | Purpose | Expected Behavior |
|----------|---------|-------------------|
| **Normal operations** | Typical requests the skill should handle | Perfect execution |
| **Edge cases** | Incomplete or unusual inputs | Graceful degradation |
| **Out-of-scope requests** | Similar but shouldn't trigger | Skill stays inactive |

### Trigger Testing

Test both explicit and natural requests:

```
# Explicit (should trigger)
"Use the PDF skill to extract text"

# Natural (should also trigger if description is good)
"Can you help me get the text from this PDF?"

# Out-of-scope (should NOT trigger)
"Can you convert this image to PDF?" (if skill doesn't do conversion)
```

### Functional Testing

- [ ] Output consistency across multiple runs
- [ ] Usable by someone unfamiliar with the skill
- [ ] Documentation accuracy matches actual behavior
- [ ] Referenced files exist and are accessible

### Iterative Refinement

> "Monitor how your skill performs in real-world usage. Refine descriptions if triggering is inconsistent. Clarify instructions if outputs vary unexpectedly."
> — Anthropic Documentation

**Common fixes:**
- **Inconsistent triggering** → Improve description specificity
- **Unexpected outputs** → Clarify instructions, add examples
- **Wrong skill activates** → Add "NOT for" boundaries

### Validation Script

Run the claudex validation script:
```bash
# Validate all skills
python3 scripts/validate-skills.py

# Validate specific category
python3 scripts/validate-skills.py skills/analysis

# Verbose output
python3 scripts/validate-skills.py --verbose
```

---

## Quality Checklist

Before sharing or publishing a skill:

### Structure
- [ ] `name`: lowercase, hyphens only, ≤64 chars
- [ ] `name` matches containing directory name
- [ ] `description`: specific what + when + boundaries, ≤1024 chars
- [ ] SKILL.md: lean (100-200 lines)
- [ ] Progressive disclosure: detailed content in separate files
- [ ] File paths: Unix-style forward slashes

### Content
- [ ] "NOT for" section included
- [ ] At least 3 trigger phrases documented
- [ ] Decision matrix or quick reference present
- [ ] Workflow phases have clear I/O
- [ ] Dependencies documented

### Validation
- [ ] YAML frontmatter syntax valid
- [ ] All referenced files exist
- [ ] Scripts have execute permissions (`chmod +x`)
- [ ] Tested with actual trigger phrases
- [ ] Tested with team members

### Metadata (for marketplace)
- [ ] Version follows semver (start with 0.1.0)
- [ ] Author attributed
- [ ] CHANGELOG.md present
- [ ] Registered in marketplace.json

---

## Target Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| SKILL.md lines | 100-200 | Lean entry point |
| Initial context load | ~15% | Efficient discovery |
| "NOT for" section | 100% | Prevent misuse |
| Progressive disclosure | 100% | On-demand loading |
| Trigger phrases | ≥3 | Reliable discovery |

---

## Quick Reference Commands

```bash
# List skills by category
ls skills/*/

# View skill structure
tree skills/category/skill-name/

# Validate frontmatter
head -20 skills/category/skill-name/SKILL.md

# Check skill file count
find skills/category/skill-name/ -type f | wc -l

# Run validation
python3 scripts/validate-skills.py --verbose
```

---

## 🔑 Critical Insights (Repeated Across Sources)

These insights appear in **multiple official sources**, indicating highest importance:

### 1. Description is THE Most Critical Component ⭐⭐⭐⭐⭐

> Repeated in: ALL 5 sources (skills-explained, how-to-create-skills, building-skills-for-claude-code, Claude Code docs, **official spec**)

- **Only** the `name` and `description` influence triggering
- Content in workflow files does NOT affect discovery
- Write descriptions from Claude's perspective
- Include: capabilities, triggers, boundaries
- Claude maintains a "lightweight index" of ~100-word descriptions
- Official spec: "Explains the skill's functionality and appropriate use cases for Claude"

### 2. Progressive Disclosure is Non-Negotiable ⭐⭐⭐⭐⭐

> Repeated in: ALL 5 sources

- SKILL.md must be lean (100-200 lines)
- Use menu/router pattern
- Load detailed content on-demand
- Three-tier loading: metadata (~100 tokens) → instructions (<5k) → files (variable)
- "Detailed documentation loads only when needed during execution"

### 3. SKILL.md is THE Required Entrypoint ⭐⭐⭐⭐⭐

> Repeated in: ALL 5 sources, **confirmed by official spec**

- "A folder qualifies as a skill if it contains a `SKILL.md` file as its required entrypoint"
- No other file structure is mandatory
- Everything else (reference/, workflow/, etc.) is optional

### 4. Standard `---` Frontmatter Delimiters ⭐⭐⭐⭐

> Confirmed by: official spec, official template, building-skills-for-claude-code, production skills

- Use standard YAML `---` delimiters
- NOT `#---` (that was a documentation anomaly)

### 5. Avoid Bloating Context Window ⭐⭐⭐⭐

> Repeated in: ALL 5 sources

- Don't include unnecessary content
- Break content into chunks
- Let Claude select what's needed
- Referenced files don't need to be mutually exclusive

### 6. No Duplication Between SKILL.md and References ⭐⭐⭐

> Repeated in: building-skills-for-claude-code, how-to-create-skills

- "Information should live in either SKILL.md or reference files but not both"
- SKILL.md = high-level routing
- Reference files = detailed implementation

### 7. Explicit Boundaries Are Required ⭐⭐⭐

> Repeated in: how-to-create-skills, local principles.md, building-skills-for-claude-code

- Always include "NOT for" section
- Prevents inappropriate triggering
- Manages user expectations
- Vague descriptions = unreliable triggering

### 8. Name Must Match Directory ⭐⭐⭐

> Confirmed by: **official spec**

- `name` field "must align with the containing directory name"
- Use hyphen-case: "lowercase Unicode alphanumeric + hyphen"

### 9. Cross-Platform Portability ⭐⭐

> Repeated in: skills-explained, building-skills-for-claude-code, official repo

- Skills work across claude.ai, Claude Code, and Claude API
- "Encode institutional knowledge that works across teams and platforms"
- Unlike CLAUDE.md (Claude Code only)

---

## ⚠️ Gaps & Inconsistencies

Discrepancies found between official documentation sources:

### 1. Frontmatter Delimiter Format

| Source | Format |
|--------|--------|
| Claude Code docs | `---` (standard YAML) |
| how-to-create-skills blog | `#---` (commented variant) |
| building-skills-for-claude-code | `---` (standard YAML) |
| Claudex skills | `---` (standard YAML) |

**Resolution**: Use standard `---`. The `#---` appears to be a documentation typo or specific to claude.ai web interface.

### 2. `allowed-tools` Field

| Source | Status |
|--------|--------|
| Claude Code docs | Documented, supported |
| how-to-create-skills blog | **Not mentioned** |
| building-skills-for-claude-code | **Not mentioned** |

**Resolution**: Field exists in Claude Code but may not be documented in all sources. Use in Claude Code; may not work in claude.ai web.

### 3. `license` Field

| Source | Status |
|--------|--------|
| Claude Code docs | Not mentioned |
| how-to-create-skills blog | Listed as "required" |
| building-skills-for-claude-code | Not mentioned |
| **Official spec** | Listed as **optional** |

**Resolution**: Official spec confirms `license` is **optional**. The "required" claim was incorrect.

### 4. Storage Locations

| Source | Primary Path |
|--------|--------------|
| Claude Code docs | `~/.claude/skills/` or `.claude/skills/` |
| how-to-create-skills blog | `skills/` at project root |
| building-skills-for-claude-code | No specific path mentioned |

**Resolution**: Both are valid. Claude Code uses `.claude/skills/`; claude.ai web uses `skills/`.

### 5. Executable Code Support

| Source | Status |
|--------|--------|
| skills-explained | "Skills cannot include executable code in Claude.ai" |
| building-skills-for-claude-code | "Can include executable code + references" |
| Claude Code | Full script/executable support |

**Resolution**: Platform-dependent. Claude Code supports scripts; claude.ai web does not.

### 6. Multiple Skill Activation

| Source | Status |
|--------|--------|
| how-to-create-skills | "Multiple skills can activate simultaneously" |
| Other docs | Single skill focus implied |

**Resolution**: Multiple activation IS supported for complex tasks with different aspects.

### 7. Reference Directory Naming

| Source | Convention |
|--------|------------|
| Most docs | `reference/` (singular) |
| building-skills-for-claude-code | `references/` (plural) |

**Resolution**: Both work. Choose one convention and be consistent within your skill.

### 8. `metadata` Field (NEW from Official Spec)

| Source | Status |
|--------|--------|
| Official spec | Documented as optional |
| All other sources | **Not mentioned** |

**Resolution**: `metadata` is a valid optional field for key-value string pairs. Use unique keys to prevent conflicts.

### 9. Name-Directory Alignment (NEW from Official Spec)

| Source | Status |
|--------|--------|
| Official spec | `name` must match directory name |
| All other sources | **Not mentioned** |

**Resolution**: Official requirement — ensure your skill's `name` field matches its containing directory name.

### 10. Size Limits

| Source | Status |
|--------|--------|
| Official spec | **No limits specified** |
| Blog posts | ~100 words for description, 100-200 lines for SKILL.md |

**Resolution**: No hard limits in spec. Blog guidelines are best practices, not requirements.

---

## Documentation Sources

| Source | URL | Focus |
|--------|-----|-------|
| **Official Spec** | [github.com/anthropics/skills/spec](https://github.com/anthropics/skills/tree/main/spec) | **Authoritative** frontmatter schema, requirements |
| **Official Repo** | [github.com/anthropics/skills](https://github.com/anthropics/skills) | Production examples, templates |
| Skills Explained | [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained) | Conceptual overview, ecosystem context |
| How to Create Skills | [claude.com/blog/how-to-create-skills...](https://www.claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples) | Technical details, best practices |
| Building Skills for Claude Code | [claude.com/blog/building-skills-for-claude-code](https://www.claude.com/blog/building-skills-for-claude-code) | Claude Code specifics, SKILL.md structure |
| Claude Code Docs | [code.claude.com/docs/en/skills.md](https://code.claude.com/docs/en/skills.md) | CLI-specific implementation |
| Local Standards | [skill-structure.md](skill-structure.md) | Claudex-specific standards |

### Official Resources

- **Official Spec**: [github.com/anthropics/skills/spec/agent-skills-spec.md](https://github.com/anthropics/skills/tree/main/spec) (v1.0, 2025-10-16)
- **Skill Template**: [github.com/anthropics/skills/template](https://github.com/anthropics/skills/tree/main/template)
- **Production Examples**: docx, pdf, pptx, xlsx skills in official repo
- **Skills Cookbook**: Referenced in docs (API developers)
- **Community Marketplace**: [skillsmp.com](https://skillsmp.com/)

### Support Articles

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide)

### Distribution Options

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Zip file** | Quick informal sharing | Fast, simple | No versioning |
| **Internal repo** | Centralized approved versions | Controlled, auditable | Setup overhead |
| **Git repository** | Version control with history | Full history, collaboration | Requires git knowledge |
| **Plugin bundle** | Easy team distribution | One-click install | Packaging complexity |

---

**Last Updated**: 2025-12-05
