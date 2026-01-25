# Phase 1: Diagram Type Selection

**Purpose**: Choose the most appropriate diagram type based on context analysis.

## Decision Matrix

| User Wants To... | Diagram Type | Key Indicator |
|------------------|--------------|---------------|
| Show how things connect | Architecture | "components", "modules", "relationships" |
| Compare states | Before/After | "current vs", "migration", "restructuring" |
| Show progression | Phased Migration | "phases", "steps", "stages", "timeline" |
| Explain movement | Data Flow | "flow", "pipeline", "process", "how data" |

## 1. Architecture Diagram

**Best for**: System components and their relationships

**Use when**:
- Explaining how modules connect
- Documenting service architecture
- Showing dependencies between components

**Example context**: "Show how our auth module connects to the database"

## 2. Before/After Diagram

**Best for**: Comparing current vs proposed state

**Use when**:
- Planning directory restructuring
- Showing migration changes
- Documenting refactoring scope

**Example context**: "Show the file structure before and after cleanup"

## 3. Phased Migration Diagram

**Best for**: Step-by-step progression with status

**Use when**:
- Tracking multi-phase projects
- Showing progress through stages
- Planning sequential changes

**Example context**: "Diagram our three-phase migration plan"

## 4. Data Flow Diagram

**Best for**: How data moves through the system

**Use when**:
- Explaining API request/response flow
- Documenting data pipelines
- Showing processing steps

**Example context**: "Illustrate how user data flows from signup to storage"

## Output

Selected diagram type with rationale:
- **Type**: Which of the four diagram types
- **Rationale**: Why this type fits best
- **Key elements**: Main components to include
- **Optional elements**: Status indicators, legends, etc.

## Hybrid Approaches

Sometimes multiple types work. Consider:
- **Architecture + Status**: Show components with progress indicators
- **Before/After + Phases**: Show transformation in stages
- **Data Flow + Architecture**: Show data movement between components
