# Visual Elements Reference

Complete reference for all ASCII diagram visual elements.

## Box Drawing Characters

### Basic Box

```
┌─────────────────┐
│   Content       │
└─────────────────┘
```

### Box with Header

```
┌─────────────────┐
│   HEADER        │
├─────────────────┤
│   Content       │
└─────────────────┘
```

### Box with Multiple Sections

```
┌─────────────────┐
│   Section 1     │
├─────────────────┤
│   Section 2     │
├─────────────────┤
│   Section 3     │
└─────────────────┘
```

### Character Reference

| Character | Name | Usage |
|-----------|------|-------|
| `┌` | Top-left corner | Start of box |
| `┐` | Top-right corner | End of top border |
| `└` | Bottom-left corner | Start of bottom border |
| `┘` | Bottom-right corner | End of box |
| `─` | Horizontal line | Top/bottom borders |
| `│` | Vertical line | Side borders |
| `├` | Left T-junction | Left side divider |
| `┤` | Right T-junction | Right side divider |
| `┬` | Top T-junction | Top divider |
| `┴` | Bottom T-junction | Bottom divider |
| `┼` | Cross junction | Grid intersection |

## Arrows

### Directional Arrows

| Arrow | Name | Meaning |
|-------|------|---------|
| `──►` | Right arrow | Forward flow, transformation |
| `◄──` | Left arrow | Reverse flow, feedback |
| `◄─►` | Bidirectional | Two-way communication |
| `│` + `▼` | Down arrow | Vertical flow downward |
| `│` + `▲` | Up arrow | Vertical flow upward |

### Status Arrows

| Arrow | Meaning | Example Use |
|-------|---------|-------------|
| `──✓` | Approved/kept | Retained items in migration |
| `──✗` | Blocked/removed | Deleted items |

### Creating Vertical Flow

```
┌─────────┐
│ Step 1  │
└─────────┘
     │
     ▼
┌─────────┐
│ Step 2  │
└─────────┘
```

## Status Indicators

### Progress Symbols

| Symbol | Meaning | When to Use |
|--------|---------|-------------|
| `✓` | Complete/done | Finished tasks, kept items |
| `✗` | Removed/failed | Deleted items, blocked tasks |
| `⏳` | In progress | Currently active work |
| `🔄` | Migrated/moved | Relocated items |

### Alert Symbols

| Symbol | Meaning | When to Use |
|--------|---------|-------------|
| `⚠️` | Warning | Needs attention |
| `🔴` | Critical | Urgent issue |

### Using Status in Diagrams

```
┌──────────────────┐
│ Migration Status │
├──────────────────┤
│ ✓ Database       │
│ ✓ API endpoints  │
│ ⏳ Frontend      │
│ ✗ Legacy cleanup │
└──────────────────┘
```

## Tree Structures

### Directory Tree

```
project/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   └── Form.tsx
│   └── utils/
│       └── helpers.ts
└── tests/
    └── unit/
```

### Tree Characters

| Character | Usage |
|-----------|-------|
| `├──` | Branch with more siblings below |
| `└──` | Last branch (no more siblings) |
| `│` | Vertical continuation |

## Combining Elements

### Architecture with Status

```
┌─────────────────────┐
│   API Gateway ✓     │
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   Auth Service ⏳   │
└─────────────────────┘
```

### Before/After with Arrows

```
BEFORE:              AFTER:
├── old.js    ──►    ├── new.ts ✓
├── temp.js   ──✗    └── utils.ts ✓
└── legacy.js ──✗
```
