# Phase 0: Context Analysis

**Purpose**: Understand what the user wants to visualize and gather necessary information to create an effective diagram.

**Execute immediately when skill activates.**

## 1. Auto-Discovery Mode (NEW)

**Run these discovery steps automatically** to reduce manual exploration:

### Project Type Detection

Execute in parallel to detect project architecture:

```bash
# React/Frontend detection
glob: "src/features/**" OR "src/app/**" OR "pages/**"

# Package detection
read: package.json → extract dependencies, scripts

# Config file detection
glob: "{next,vite,webpack}.config.*" OR "tsconfig.json"
```

### Architecture Scanning

```bash
# Feature boundaries (Bulletproof React)
glob: "src/features/*/index.{ts,tsx}"

# Route structure
glob: "src/app/**/page.{ts,tsx}" OR "pages/**/*.{ts,tsx}"

# API layer
grep: "export.*function.*fetch|api|query" --type ts

# Cross-feature dependencies
grep: "import.*from '@/features" OR "from '../features"
```

### Output Summary

After auto-discovery, report:

```
Project Type: [bulletproof-react | next-app-router | express-api | monorepo | generic]
Features Found: [list of feature directories]
Routes Found: [list of route patterns]
Key Dependencies: [from package.json]
Architecture Pattern: [detected pattern]
```

This auto-discovery reduces 50% of manual codebase exploration.

---

## 2. Identify Visualization Target

Determine what needs to be diagrammed:

- **System architecture**: Components, modules, services
- **File/directory structure**: Current or proposed organization
- **Process flow**: Steps, phases, stages
- **Data movement**: Input, processing, output

## 3. Extract Key Information

From the user's request or **auto-discovery results**:

- Component names and relationships
- Current vs desired state (for migrations)
- Number of phases/steps (for phased diagrams)
- Data sources and destinations (for flow diagrams)

## 4. Assess Complexity

Evaluate scope to determine diagram approach:

| Complexity | Characteristics | Approach |
|------------|-----------------|----------|
| Simple | 2-4 components, linear flow | Single compact diagram |
| Medium | 5-10 components, some branches | Standard diagram with sections |
| Complex | 10+ components, multiple flows | Multiple diagrams or layered view |

## Output

Context summary ready for diagram type selection:
- **What**: Clear description of visualization target
- **Scope**: Number of components/phases
- **Purpose**: How the diagram will be used (PR, docs, presentation)
- **Constraints**: Any specific requirements (width, detail level)

## Common Issues

**Vague requests**: Ask for clarification
- "What specifically would you like to see in the diagram?"
- "Should this show the current state, proposed state, or both?"

**Missing information**: Gather from codebase if possible
- Run `ls` or `tree` for directory structures
- Check existing docs for architecture info
