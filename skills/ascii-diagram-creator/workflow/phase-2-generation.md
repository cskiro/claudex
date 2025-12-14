# Phase 2: Diagram Generation

**Purpose**: Create the ASCII diagram using proper visual elements and formatting.

## 1. Apply Formatting Rules

Before generating, ensure compliance:

- **Maximum width**: 80 characters
- **Box alignment**: Vertical centers aligned
- **Spacing**: Clear separation between sections
- **Legends**: Include when using status indicators

## 2. Select Visual Elements

### Box Drawing Characters

```
┌─────────────────┐    Top border
│   Content       │    Side borders with padding
├─────────────────┤    Section divider
│   More content  │
└─────────────────┘    Bottom border
```

### Arrow Types

| Arrow | Meaning | Usage |
|-------|---------|-------|
| `──►` | Transformation/flow | Data movement, process flow |
| `◄──` | Reverse flow | Feedback loops |
| `◄─►` | Bidirectional | Two-way communication |
| `──✓` | Approved/kept | Retained items |
| `──✗` | Removed/blocked | Deleted items |

### Status Indicators

| Symbol | Meaning |
|--------|---------|
| `✓` | Complete/kept |
| `✗` | Removed/deleted |
| `⏳` | In progress |
| `🔄` | Migrated/moved |
| `⚠️` | Warning |
| `🔴` | Critical |

## 3. Generate Diagram

Follow the template for the selected type:

### Architecture Template
```
┌─────────────────────────────────┐
│     COMPONENT NAME              │
├─────────────────────────────────┤
│ • Feature 1                     │
│ • Feature 2                     │
└─────────────────────────────────┘
             │
             ▼
    [Connected Component]
```

### Before/After Template
```
BEFORE:                    AFTER:
old/structure/      ──►    new/structure/
├── file1          KEPT    ├── file1
├── file2          MOVED   └── newfile
└── file3          DELETED
```

### Phased Migration Template
```
┌────────────────────────────────┐
│  PHASE 1: Description          │
│  Status: IN PROGRESS           │
│  Action: Specific task         │
└────────────────────────────────┘
                  │
                  ▼
[Next Phase]
```

### Data Flow Template
```
Input ──► Process ──► Output
   ▲         │          │
   │         ▼          ▼
Feedback  Storage   Display
```

## 4. Add Context

Include with the diagram:
- Brief explanation of what it shows
- Legend for any symbols used
- Suggested usage (PR, docs, README)

## Output

Complete ASCII diagram with:
- Proper formatting (80-char max)
- Appropriate visual elements
- Clear labels and structure
- Explanatory context
