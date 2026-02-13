---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

<!-- Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync -->

# TypeScript Standards

These rules apply **only when working with TypeScript files**.

---

## Type Safety (MANDATORY)

- **Strict mode enabled** - `"strict": true` in tsconfig.json
- **No `any` types** - Use `unknown` for truly unknown types
- **Explicit return types** for all public functions
- **Validate inputs at function boundaries** - Fail fast
- **Follow existing type patterns** - Match conventions already established in the codebase

**Example**:
```typescript
// GOOD
function getUser(userId: string): Promise<User | null> {
  if (!userId) {
    throw new Error('userId is required');
  }
  return db.users.findOne({ id: userId });
}

// BAD
function getUser(userId: any) {
  return db.users.findOne({ id: userId });
}
```

---

## Code Quality

- Format with **Prettier**
- Lint with **ESLint** (with TypeScript plugin)
- Type-check with `tsc --noEmit` before commits

---

## Naming Conventions

- Functions/variables: `camelCase`
- Classes/interfaces/types: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Type parameters: Single uppercase letter (`T`, `K`, `V`) or descriptive (`TItem`)
- Enum values: `PascalCase`

---

## React Components (TSX)

When working with `.tsx` files:

- Use **function components** with explicit props interfaces
- Define props interface **above** the component
- Use `React.FC<Props>` or explicit return type `JSX.Element`
- Hooks at the **top** of the component body

**Example**:
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export function Button({ label, onClick, disabled = false }: ButtonProps): JSX.Element {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

---

## Imports Organization

Group imports in this order (separated by blank lines):
1. External packages (`react`, `lodash`, etc.)
2. Internal packages (`@/components`, `@/utils`)
3. Relative imports (`./Button`, `../hooks`)
4. Type imports (`import type { ... }`)

---

## Error Handling

- Use **specific error types** (not generic `Error`)
- Always handle Promise rejections
- Use `unknown` for caught errors, then narrow

**Example**:
```typescript
// GOOD
try {
  await fetchUser();
} catch (error: unknown) {
  if (error instanceof ApiError) {
    logger.error('API error', { code: error.code });
  } else if (error instanceof Error) {
    logger.error('Unknown error', { message: error.message });
  }
  throw error;
}
```

---

## Utility Types (Use Built-ins)

- `Partial<T>` - Make all properties optional
- `Required<T>` - Make all properties required
- `Pick<T, K>` - Select specific properties
- `Omit<T, K>` - Remove specific properties
- `Record<K, V>` - Object with specific key/value types
