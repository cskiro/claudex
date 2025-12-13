# Complex Skill Structure Example

This example shows the structure for skills with multiple operating modes or data processing capabilities.

## Directory Structure

### Mode-Based Complex Skill

```
complex-skill/
├── SKILL.md           # Agent manifest with mode detection (required)
├── README.md          # User documentation (required)
├── plugin.json        # Marketplace metadata (required)
├── CHANGELOG.md       # Version history (required)
├── modes/             # Mode-specific workflows (required for mode-based)
│   ├── mode1-name.md
│   ├── mode2-name.md
│   └── mode3-name.md
├── data/              # Reference materials (optional)
│   ├── best-practices.md
│   └── troubleshooting.md
├── examples/          # Sample outputs per mode (optional)
│   ├── mode1-example.md
│   └── mode2-example.md
└── templates/         # Reusable templates (optional)
    └── output-template.md
```

### Data Processing Complex Skill

```
complex-skill/
├── SKILL.md           # Agent manifest (required)
├── README.md          # User documentation (required)
├── plugin.json        # Marketplace metadata (required)
├── CHANGELOG.md       # Version history (required)
├── scripts/           # Processing scripts (required for data processing)
│   ├── processor.py
│   ├── indexer.py
│   ├── query.py
│   └── generator.py
├── data/              # Reference materials (optional)
│   └── config-defaults.yaml
├── examples/          # Sample outputs (optional)
│   └── sample-report.md
└── templates/         # Report templates (optional)
    └── report-template.md.j2
```

## When to Use Complex Structure

Use this structure when:

### Mode-Based:
- Multiple distinct operating modes based on user intent
- Each mode has its own workflow
- Different outputs per mode
- Clear mode detection logic needed
- Example: git-worktree-setup (single/batch/cleanup/list modes)

### Data Processing:
- Processes data from files or APIs
- Performs analysis or transformation
- Generates insights or reports
- Needs helper scripts for processing
- Example: cc-insights (conversation analysis)

## Characteristics

- **Complexity**: High
- **Files**: 4 required + 4+ optional directories
- **Pattern**: Mode-based or data-processing
- **Modes**: Multiple distinct modes OR data pipeline
- **Scripts**: Often needed for data processing
- **Dependencies**: May have Python/Node dependencies

## SKILL.md Template (Mode-Based)

```markdown
---
name: skill-name
version: 0.1.0
description: Multi-mode skill that handles X, Y, and Z
author: Your Name
---

# Skill Name

## Overview

This skill operates in multiple modes based on user intent.

## When to Use This Skill

**Trigger Phrases:**
- "mode 1 trigger"
- "mode 2 trigger"
- "mode 3 trigger"

**Use Cases:**
- Mode 1: Use case
- Mode 2: Use case
- Mode 3: Use case

## Quick Decision Matrix

\`\`\`
User Request              → Mode      → Action
─────────────────────────────────────────────────
"trigger 1"               → Mode 1    → Action 1
"trigger 2"               → Mode 2    → Action 2
"trigger 3"               → Mode 3    → Action 3
\`\`\`

## Mode Detection Logic

\`\`\`javascript
// Mode 1: Description
if (userMentions("keyword1")) {
  return "mode1-name";
}

// Mode 2: Description
if (userMentions("keyword2")) {
  return "mode2-name";
}

// Mode 3: Description
if (userMentions("keyword3")) {
  return "mode3-name";
}

// Ambiguous - ask user
return askForClarification();
\`\`\`

## Core Responsibilities

### Shared Prerequisites
- ✓ Prerequisite 1 (all modes)
- ✓ Prerequisite 2 (all modes)

### Mode-Specific Workflows
See detailed workflows in:
- \`modes/mode1-name.md\` - Mode 1 complete workflow
- \`modes/mode2-name.md\` - Mode 2 complete workflow
- \`modes/mode3-name.md\` - Mode 3 complete workflow

## Success Criteria

Varies by mode - see individual mode documentation.
```

## SKILL.md Template (Data Processing)

```markdown
---
name: skill-name
version: 0.1.0
description: Processes X data to generate Y insights
author: Your Name
---

# Skill Name

## Overview

Automatically processes data from [source] to provide [capabilities].

## When to Use This Skill

**Trigger Phrases:**
- "search for X"
- "generate Y report"
- "analyze Z data"

**Use Cases:**
- Search and find
- Generate insights
- Track patterns

## Architecture

\`\`\`
Input → Processing → Storage → Query/Analysis → Output
\`\`\`

## Workflow

### Phase 1: Data Ingestion
- Discover data sources
- Validate format
- Process incrementally

### Phase 2: Processing
- Extract features
- Generate embeddings (if semantic)
- Store in database

### Phase 3: Query/Analysis
- Search interface
- Pattern detection
- Generate reports

## Scripts

See \`scripts/\` directory:
- \`processor.py\` - Main data processing
- \`indexer.py\` - Build indexes
- \`query.py\` - Query interface
- \`generator.py\` - Report generation

## Performance

- Initial processing: [time estimate]
- Incremental updates: [time estimate]
- Search latency: [time estimate]
- Memory usage: [estimate]
```

## Directory Purposes

### modes/
For mode-based skills, each file documents one mode:
- Complete workflow for that mode
- Mode-specific prerequisites
- Mode-specific outputs
- Mode-specific error handling

### scripts/
For data processing skills:
- Python/Node scripts for heavy processing
- CLI interfaces for user interaction
- Batch processors
- Report generators

## Best Practices

### Mode-Based Skills:
1. **Clear mode boundaries**: Each mode is distinct
2. **Explicit detection**: Unambiguous mode selection
3. **Shared prerequisites**: Extract common validation
4. **Mode independence**: Each mode works standalone
5. **Detailed documentation**: Each mode has its own guide

### Data Processing Skills:
1. **Incremental processing**: Don't reprocess everything
2. **State tracking**: Know what's been processed
3. **Progress indicators**: Show progress for long operations
4. **Error recovery**: Handle failures gracefully
5. **Performance docs**: Document expected performance
6. **Script documentation**: Each script has clear --help

## Examples of Complex Skills

### Mode-Based:
- **git-worktree-setup**: Single/Batch/Cleanup/List modes
- **Multi-format converter**: Different output formats
- **Environment manager**: Create/Update/Delete/List

### Data Processing:
- **cc-insights**: Conversation analysis with RAG search
- **Log analyzer**: Parse logs, detect patterns, generate reports
- **Metrics aggregator**: Collect data, analyze trends, visualize

## When NOT to Use Complex Structure

Avoid over-engineering:
- Don't create modes if phases suffice
- Don't add scripts if pure LLM can handle it
- Don't add directories you won't populate
- Start minimal, grow as needed
