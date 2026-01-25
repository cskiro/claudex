# Diagram Type Templates

Ready-to-use templates for each diagram type.

## 1. Architecture Diagram

**Purpose**: Show system components and their relationships.

### Basic Template

```
┌─────────────────────────────────┐
│     COMPONENT NAME              │
├─────────────────────────────────┤
│ • Feature 1                     │
│ • Feature 2                     │
│ • Feature 3                     │
└─────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   CONNECTED COMPONENT           │
└─────────────────────────────────┘
```

### Multi-Component Template

```
┌───────────────┐     ┌───────────────┐
│   Frontend    │     │   Backend     │
├───────────────┤     ├───────────────┤
│ • React       │────►│ • Node.js     │
│ • Redux       │     │ • Express     │
└───────────────┘     └───────────────┘
                              │
                              ▼
                      ┌───────────────┐
                      │   Database    │
                      ├───────────────┤
                      │ • PostgreSQL  │
                      └───────────────┘
```

### When to Use

- Documenting service architecture
- Explaining module relationships
- Showing system overview
- Onboarding new team members

---

## 2. Before/After Diagram

**Purpose**: Compare current vs proposed state.

### Basic Template

```
BEFORE:                    AFTER:
old/structure/      ──►    new/structure/
├── file1          KEPT    ├── file1
├── file2          MOVED   ├── relocated/
│                          │   └── file2
└── file3          DELETED
```

### With Status Indicators

```
CURRENT STATE:              TARGET STATE:
src/                        src/
├── components/      ✓      ├── components/
│   ├── old.js      ──►     │   └── new.tsx
│   └── legacy.js   ✗       ├── features/
├── utils/          🔄      │   └── auth/
│   └── helpers.js  ──►     └── shared/
└── tests/          ✓           └── utils/
```

### File Transformation

```
BEFORE:                         AFTER:
src/                            src/
├── Button.js          ──►      ├── Button.tsx ✓
├── Button.css         ──►      │   (styles included)
├── Form.js            ──►      ├── Form.tsx ✓
├── Form.css           ──►      │   (styles included)
└── utils.js           ──►      └── utils.ts ✓

Legend: ✓ = TypeScript conversion complete
```

### When to Use

- Planning directory restructuring
- Showing migration scope
- Documenting refactoring changes
- Creating PR descriptions

---

## 3. Phased Migration Diagram

**Purpose**: Show step-by-step progression with status.

### Basic Template

```
┌────────────────────────────────┐
│  PHASE 1: Description          │
│  Status: COMPLETE ✓            │
│  Action: Specific task         │
└────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────┐
│  PHASE 2: Description          │
│  Status: IN PROGRESS ⏳        │
│  Action: Specific task         │
└────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────┐
│  PHASE 3: Description          │
│  Status: PENDING               │
│  Action: Specific task         │
└────────────────────────────────┘
```

### Detailed Migration Plan

```
┌─────────────────────────────────────────────────────────┐
│                SYSTEM CONSOLIDATION PLAN                 │
└─────────────────────────────────────────────────────────┘

PHASE 1: Analysis ✓
┌──────────────────┐
│ Current State    │──► Identify duplicates
│ 11 directories   │──► Find dependencies
│ 3 systems        │──► Check references
└──────────────────┘
         │
         ▼
PHASE 2: Migration ⏳
┌──────────────────┐
│ Moving Data      │
│ ✓ Memory files   │
│ ✓ Pattern files  │
│ ⏳ Script updates │
└──────────────────┘
         │
         ▼
PHASE 3: Validation
┌──────────────────┐
│ Final State      │
│ 2 directories    │──► All tests passing
│ 1 unified system │──► No duplicates
└──────────────────┘
```

### When to Use

- Tracking multi-phase projects
- Showing progress through stages
- Planning sequential changes
- Sprint/milestone planning

---

## 4. Data Flow Diagram

**Purpose**: Illustrate how data moves through the system.

### Basic Template

```
Input ──► Process ──► Output
   ▲         │          │
   │         ▼          ▼
Feedback  Storage   Display
```

### API Request Flow

```
┌────────┐     ┌────────────┐     ┌──────────┐
│ Client │────►│ API Gateway│────►│ Service  │
└────────┘     └────────────┘     └──────────┘
    ▲                                   │
    │                                   ▼
    │                            ┌──────────┐
    └────────────────────────────│ Database │
         Response with data      └──────────┘
```

### Authentication Flow

```
User Input
    │
    ▼
┌──────────────┐
│ Login Form   │
└──────────────┘
    │
    ▼
┌──────────────┐     ┌──────────────┐
│ Auth Service │────►│ Token Store  │
└──────────────┘     └──────────────┘
    │                       │
    ▼                       │
┌──────────────┐            │
│ JWT Token    │◄───────────┘
└──────────────┘
    │
    ▼
Protected Resources
```

### Data Pipeline

```
Raw Data ──► Validate ──► Transform ──► Store ──► Display
               │              │          │
               ▼              ▼          ▼
            Errors         Logs      Analytics
```

### When to Use

- Explaining API request/response flow
- Documenting data pipelines
- Showing processing steps
- Illustrating system integrations
