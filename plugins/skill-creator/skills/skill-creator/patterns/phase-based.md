# Phase-Based Skill Pattern

Use this pattern when your skill follows **sequential phases** that build on each other.

## When to Use

- Skill has a linear workflow with clear stages
- Each phase depends on the previous phase
- Progressive disclosure of complexity
- Examples: codebase-auditor (discovery → analysis → reporting → remediation)

## Structure

### Phase Overview

Define clear phases with dependencies:

```
Phase 1: Discovery
  ↓
Phase 2: Analysis
  ↓
Phase 3: Reporting
  ↓
Phase 4: Action/Remediation
```

### Phase Workflow Template

```markdown
## Workflow

### Phase 1: [Name]

**Purpose**: [What this phase accomplishes]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Output**: [What information is produced]

**Transition**: [When to move to next phase]

### Phase 2: [Name]

**Purpose**: [What this phase accomplishes]

**Inputs**: [Required from previous phase]

**Steps:**
1. [Step 1]
2. [Step 2]

**Output**: [What information is produced]
```

## Example: Codebase Auditor

**Phase 1: Initial Assessment** (Progressive Disclosure)
- Lightweight scan to understand codebase
- Identify tech stack and structure
- Quick health check
- **Output**: Project profile and initial findings

**Phase 2: Deep Analysis** (Load on Demand)
- Based on Phase 1, perform targeted analysis
- Code quality, security, testing, etc.
- **Output**: Detailed findings with severity

**Phase 3: Report Generation**
- Aggregate findings from Phase 2
- Calculate scores and metrics
- **Output**: Comprehensive audit report

**Phase 4: Remediation Planning**
- Prioritize findings by severity
- Generate action plan
- **Output**: Prioritized task list

## Best Practices

1. **Progressive Disclosure**: Start lightweight, go deep only when needed
2. **Clear Transitions**: Explicitly state when moving between phases
3. **Phase Independence**: Each phase should have clear inputs/outputs
4. **Checkpoint Validation**: Verify prerequisites before advancing
5. **Early Exit**: Allow stopping after any phase if user only needs partial analysis
6. **Incremental Value**: Each phase should provide standalone value

## Phase Characteristics

### Discovery Phase
- Fast and lightweight
- Gather context and identify scope
- No expensive operations
- Output guides subsequent phases

### Analysis Phase
- Deep dive based on discovery
- Resource-intensive operations
- Parallel processing when possible
- Structured output for reporting

### Reporting Phase
- Aggregate and synthesize data
- Calculate metrics and scores
- Generate human-readable output
- Support multiple formats

### Action Phase
- Provide recommendations
- Generate implementation guidance
- Offer to perform actions
- Track completion
