# Mermaid Export Guide

Convert ASCII diagrams to Mermaid syntax for graphical rendering in GitHub, GitLab, Notion, and other platforms that support Mermaid.

## When to Use Mermaid Export

- Documentation that will be viewed in GitHub/GitLab (renders automatically)
- Presentations where graphical output is preferred
- Teams that prefer visual diagrams over text-based
- When you need to iterate on diagrams in a visual editor

## Conversion Rules

### Basic Elements

| ASCII Element | Mermaid Syntax | Example |
|---------------|----------------|---------|
| `┌─────┐` Box | `[Label]` | `A[Component]` |
| `(( ))` Circle | `((Label))` | `A((Start))` |
| `{ }` Diamond | `{Label}` | `A{Decision}` |
| `──►` Arrow | `-->` | `A --> B` |
| `◄──` Reverse | `<--` | `A <-- B` |
| `◄─►` Bidirectional | `<-->` | `A <--> B` |
| `──✗` Blocked | `-.-x` | `A -.-x B` |
| Text on arrow | `-- text -->` | `A -- calls --> B` |

### Container Elements

| ASCII Pattern | Mermaid Equivalent |
|--------------|-------------------|
| Nested boxes | `subgraph` |
| Grouped components | `subgraph "Name"` |
| Layers | Multiple subgraphs |

### Status Indicators

Use Mermaid classes for status styling:

```mermaid
graph TD
    A[Complete]:::done
    B[In Progress]:::pending
    C[Blocked]:::blocked

    classDef done fill:#90EE90
    classDef pending fill:#FFE4B5
    classDef blocked fill:#FFB6C1
```

---

## Conversion Examples

### Architecture Diagram

**ASCII Input**:
```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │   app/      │     │  features/  │     │   shared/   │   │
│  │  (routes)   │────►│  (domains)  │────►│  (common)   │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Mermaid Output**:
```mermaid
graph LR
    subgraph "Application Architecture"
        A[app/<br/>routes] --> B[features/<br/>domains]
        B --> C[shared/<br/>common]
    end
```

### Before/After Diagram

**ASCII Input**:
```
BEFORE                          AFTER
┌──────────────┐               ┌──────────────┐
│  Monolith    │               │   Service A  │
│  All-in-one  │      ──►      ├──────────────┤
│              │               │   Service B  │
└──────────────┘               └──────────────┘
```

**Mermaid Output**:
```mermaid
graph LR
    subgraph Before
        A[Monolith<br/>All-in-one]
    end

    subgraph After
        B[Service A]
        C[Service B]
    end

    A -.-> B
    A -.-> C
```

### Phased Migration Diagram

**ASCII Input**:
```
PHASE 1: Analysis        PHASE 2: Migration       PHASE 3: Validation
┌──────────────┐        ┌──────────────┐         ┌──────────────┐
│ ✓ Complete   │───────►│ ⏳ In Progress│────────►│ ○ Pending    │
└──────────────┘        └──────────────┘         └──────────────┘
```

**Mermaid Output**:
```mermaid
graph LR
    A[Phase 1<br/>Analysis]:::done --> B[Phase 2<br/>Migration]:::pending
    B --> C[Phase 3<br/>Validation]:::future

    classDef done fill:#90EE90,stroke:#228B22
    classDef pending fill:#FFE4B5,stroke:#FF8C00
    classDef future fill:#E0E0E0,stroke:#808080
```

### Data Flow Diagram

**ASCII Input**:
```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────►│   API   │────►│ Service │────►│   DB    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
      ▲                                              │
      └──────────────────────────────────────────────┘
```

**Mermaid Output**:
```mermaid
graph LR
    A[User] --> B[API]
    B --> C[Service]
    C --> D[DB]
    D --> A
```

---

## Direction Options

Choose the flow direction based on diagram type:

| Direction | Syntax | Best For |
|-----------|--------|----------|
| Left to Right | `graph LR` | Data flows, pipelines |
| Top to Bottom | `graph TD` | Hierarchies, architecture |
| Bottom to Top | `graph BT` | Bottom-up structures |
| Right to Left | `graph RL` | Reverse flows |

---

## Advanced Features

### Subgraph Nesting

```mermaid
graph TD
    subgraph "Frontend"
        subgraph "Components"
            A[Button]
            B[Form]
        end
        subgraph "Pages"
            C[Home]
            D[Dashboard]
        end
    end

    C --> A
    D --> B
```

### Click Events (for interactive diagrams)

```mermaid
graph TD
    A[Component]
    click A "https://github.com/repo/component" "View source"
```

### Notes and Comments

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]

    %% This is a comment
    %% Comments don't render
```

---

## Platform Support

| Platform | Support | Notes |
|----------|---------|-------|
| GitHub | ✓ Native | Renders in markdown files and issues |
| GitLab | ✓ Native | Renders in markdown |
| Notion | ✓ Native | Use `/mermaid` block |
| VS Code | ✓ Extension | Mermaid Preview extension |
| Obsidian | ✓ Native | Built-in support |
| Confluence | ⚠️ Plugin | Requires Mermaid plugin |

---

## Conversion Tips

1. **Keep it simple**: ASCII diagrams with many nested elements may not convert cleanly
2. **Use subgraphs sparingly**: More than 2-3 levels of nesting gets hard to read
3. **Add line breaks**: Use `<br/>` in node labels for multi-line text
4. **Test rendering**: Preview in GitHub/GitLab before committing
5. **Preserve ASCII version**: Keep both formats for different use cases

---

## Quick Conversion Checklist

- [ ] Identify all boxes → Convert to nodes `[Label]`
- [ ] Identify all arrows → Convert to connections `-->`
- [ ] Identify groupings → Convert to `subgraph`
- [ ] Identify status indicators → Add `classDef` styles
- [ ] Choose direction (`LR` vs `TD`)
- [ ] Test rendering in target platform
