---
name: ascii-diagram-creator
version: 0.4.0
description: Use PROACTIVELY when user asks for ASCII diagrams, text diagrams, or visual representations of systems, workflows, or relationships. Triggers on "ascii diagram", "text diagram", "visualize", "show how X connects/synergizes", "diagram the flow/phases", or "illustrate relationships". Generates terminal-compatible diagrams using box-drawing characters. Supports architecture, before/after, phased migration, data flow, and relationship/synergy diagrams. Not for image generation or graphical output.
---

# ASCII Diagram Creator

## Overview

This skill is a **visual generator agent** that creates clear, terminal-compatible ASCII diagrams to communicate system changes, migrations, and architectural decisions. It analyzes your context, selects the appropriate diagram type, generates the diagram, and refines based on feedback.

**Key Capabilities**:
- **Codebase auto-discovery**: Automatically scan project structure, detect architecture patterns, and populate diagrams
- **Project-type templates**: Pre-built templates for Bulletproof React, Next.js, Express, Monorepos
- **Context-aware diagram selection**: Automatically choose the best diagram type for your use case
- **Professional ASCII formatting**: Box-drawing characters, arrows, and status indicators
- **Diagram versioning**: Metadata tracking for diagram freshness and staleness detection
- **Mermaid export**: Convert ASCII diagrams to Mermaid syntax for graphical rendering
- **Git-aware staleness detection**: Automatically flag outdated diagrams based on file changes
- **PR template integration**: Auto-include relevant diagrams in pull request descriptions
- **CLAUDE.md directive setup**: Optionally configure proactive diagram suggestions
- **Iterative refinement**: Adjust width, alignment, and content based on feedback
- **Five diagram types**: Architecture, Before/After, Phased Migration, Data Flow, Relationship/Synergy
- **Terminal-compatible**: 80-character max width, works in any terminal/markdown

## When to Use This Skill

**Trigger Phrases**:
- "create an ascii diagram" / "make a text diagram"
- "create a diagram showing..."
- "visualize this architecture"
- "show how X connects/synergizes/relates"
- "diagram the workflow/phases/flow"
- "illustrate the relationships between"
- "show before and after"

**Use PROACTIVELY when**:
- User is planning a major refactoring or migration
- User is restructuring directories or file organization
- User needs to communicate system changes in a PR description
- User is explaining architecture to team members
- User mentions "show me", "visualize", or "diagram"

**Do NOT use when**:
- User wants graphical/image output (use Mermaid or external tools)
- User needs flowcharts with complex branching (consider Mermaid)
- User is asking about code, not structure or flow
- Simple lists would suffice instead of visual diagrams

## Response Style

**Visual Generator Agent**: Analyze context to determine what needs visualization, select appropriate diagram type, generate ASCII diagram, and refine through iteration.

**Execution Pattern**:
1. **Analyze context**: Understand what the user wants to visualize
2. **Select diagram type**: Choose Architecture, Before/After, Phased, or Data Flow
3. **Generate diagram**: Create initial diagram with proper formatting
4. **Present with explanation**: Show diagram and explain visual elements
5. **Refine on request**: Adjust based on user feedback ("make it wider", "add status")
6. **MANDATORY - Output & Integration**: Execute Phase 4 completely:
   - Offer Mermaid export for graphical rendering
   - Run staleness detection if existing diagrams found
   - Offer PR integration if user is working on a PR
   - **Ask about CLAUDE.md directive setup**
   - Output completion checklist (see below)

**CRITICAL**: The skill is NOT complete until the Completion Checklist is output.

## Workflow

| Phase | Description | Details |
|-------|-------------|---------|
| 0 | Context Analysis | → [workflow/phase-0-context-analysis.md](workflow/phase-0-context-analysis.md) |
| 1 | Diagram Type Selection | → [workflow/phase-1-diagram-selection.md](workflow/phase-1-diagram-selection.md) |
| 2 | Diagram Generation | → [workflow/phase-2-generation.md](workflow/phase-2-generation.md) |
| 3 | Iterative Refinement | → [workflow/phase-3-refinement.md](workflow/phase-3-refinement.md) |
| **4** | **Output & Integration (MANDATORY)** | → [workflow/phase-4-output-integration.md](workflow/phase-4-output-integration.md) |

> **⚠️ IMPORTANT**: Phase 4 must ALWAYS be executed. Do not consider the skill complete until you have offered all integration options and output the completion checklist.

## Quick Reference

### Diagram Types

| Type | Purpose | Best For |
|------|---------|----------|
| Architecture | System components and relationships | Showing how modules connect |
| Before/After | Compare current vs proposed state | Migration plans, refactoring |
| Phased Migration | Step-by-step progression | Multi-phase projects |
| Data Flow | How data moves through system | API flows, pipelines |
| Relationship/Synergy | How elements interact or complement | SDLC phases, skill workflows, team structures |

### Visual Elements

| Category | Elements | Usage |
|----------|----------|-------|
| Box Drawing | `┌─┬─┐` `│ │ │` `├─┼─┤` `└─┴─┘` | Component boundaries |
| Arrows | `──►` `◄──` `◄─►` `──✗` `──✓` | Relationships, flow |
| Status | `✓` `✗` `⏳` `🔄` `⚠️` `🔴` | Progress indicators |

### Formatting Rules

| Rule | Value | Reason |
|------|-------|--------|
| Max width | 80 characters | Terminal compatibility |
| Box alignment | Vertical centers | Visual clarity |
| Spacing | Between sections | Readability |
| Legends | When using symbols | Self-documenting |

## Diagram Versioning

Add metadata to track diagram freshness and enable staleness detection:

```markdown
<!-- diagram-meta
  type: architecture
  created: 2025-01-23
  last-verified: 2025-01-23
  source-patterns: [src/features/*, src/app/routes/*]
  stale-after: 30d
-->
```

**Metadata Fields**:
| Field | Purpose |
|-------|---------|
| `type` | Diagram type (architecture, data-flow, etc.) |
| `created` | Initial creation date |
| `last-verified` | Last time diagram was confirmed accurate |
| `source-patterns` | Glob patterns of directories diagram represents |
| `stale-after` | Days until diagram should be re-verified |

**Staleness Detection**: When files matching `source-patterns` are modified after `stale-after` days from `last-verified`, the diagram should be re-verified.

## Reference Materials

- [Visual Elements Reference](reference/visual-elements.md)
- [Best Practices](reference/best-practices.md)
- [Diagram Type Templates](reference/diagram-types.md)
- [Project-Type Templates](reference/project-templates.md)
- [Mermaid Export Guide](reference/mermaid-export.md)

## Workflow Automation

This skill can be integrated into your workflow automatically. See the README for:
- Hook-based auto-triggers when creating feature branches
- CLAUDE.md directives for proactive diagram suggestions
- Sub-agent integration for feature planning workflows

## Mandatory Completion Checklist

**You MUST output this checklist before the skill is complete.** This ensures all integration options are offered.

```markdown
## Diagram Generation Complete

### Outputs
- [ ] ASCII diagram generated (80-char width)
- [ ] Diagram metadata added (if saving to file)

### Integration Options Offered (Phase 4)
- [ ] Mermaid export: [offered/accepted/declined/not applicable]
- [ ] PR integration: [offered/accepted/declined/not applicable]
- [ ] CLAUDE.md directive: [offered/accepted/declined/already configured]

### Next Steps
- Recommended save location: [path]
- Staleness tracking: [enabled/disabled]
```

**Example completed checklist:**
```markdown
## Diagram Generation Complete

### Outputs
- [x] ASCII diagram generated (80-char width)
- [x] Diagram metadata added

### Integration Options Offered (Phase 4)
- [x] Mermaid export: offered, user declined
- [x] PR integration: accepted, added to PR description
- [x] CLAUDE.md directive: offered, user accepted (added to ~/.claude/CLAUDE.md)

### Next Steps
- Recommended save location: docs/architecture/auth-flow.md
- Staleness tracking: enabled (30 days)
```

## Metadata

**Category**: planning
**Source**: Protocol conversion from `~/.claude/protocols/ASCII_DIAGRAM_PROTOCOL.yaml`
**Version**: 0.3.1
