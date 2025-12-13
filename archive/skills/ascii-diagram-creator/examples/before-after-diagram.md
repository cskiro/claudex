# Example: Before/After Diagram

## Scenario

A user asks: "Show the directory structure before and after our TypeScript migration."

## Generated Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│               JAVASCRIPT TO TYPESCRIPT MIGRATION                         │
└─────────────────────────────────────────────────────────────────────────┘

BEFORE (JavaScript):                 AFTER (TypeScript):

src/                                 src/
├── components/                      ├── components/
│   ├── Button.js        ──►        │   ├── Button.tsx ✓
│   ├── Button.css       ──►        │   │   (CSS modules imported)
│   ├── Form.js          ──►        │   ├── Form.tsx ✓
│   ├── Form.css         ──►        │   │   (CSS modules imported)
│   └── Modal.js         ──►        │   └── Modal.tsx ✓
├── utils/                           ├── utils/
│   ├── helpers.js       ──►        │   ├── helpers.ts ✓
│   ├── constants.js     ──►        │   ├── constants.ts ✓
│   └── api.js           ──►        │   └── api.ts ✓
├── hooks/                           ├── hooks/
│   ├── useAuth.js       ──►        │   ├── useAuth.ts ✓
│   └── useForm.js       ──►        │   └── useForm.ts ✓
├── types/               NEW         ├── types/
│                                    │   ├── index.ts ✓
│                                    │   ├── api.d.ts ✓
│                                    │   └── components.d.ts ✓
├── App.js               ──►        ├── App.tsx ✓
├── index.js             ──►        ├── index.tsx ✓
└── .eslintrc.js         ──►        ├── .eslintrc.js (updated)
                                     └── tsconfig.json NEW

Configuration Files:
├── package.json         ──►        ├── package.json (updated deps)
├── jest.config.js       ──►        ├── jest.config.js (ts-jest)
└── .babelrc             ✗          └── (removed - using tsc)

Legend:
✓ = Conversion complete
──► = Transformed/updated
✗ = Removed
NEW = New file/directory
```

## Explanation

This before/after diagram shows the complete scope of a TypeScript migration:

- **File transformations**: .js → .tsx/.ts conversions
- **New additions**: types/ directory with type definitions
- **Removed files**: Babel config (replaced by TypeScript compiler)
- **Updated configs**: ESLint and Jest configurations

The parallel columns make it easy to trace each file's transformation.

## Usage Suggestions

- Include in migration PR description
- Add to project README as migration record
- Reference in team communication about changes
