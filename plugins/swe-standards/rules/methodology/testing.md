# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Testing Standards (Universal)

**Purpose**: Enforce TDD red-green-refactor and Kent C. Dodds' Testing Trophy across all code — tests AND implementation.

---

## Core Philosophy

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

- **Test behavior and outcomes**, not implementation details
- **Test pure functionality** — given input X, expect output Y
- **Test user behavior** — what does the consumer of this code actually do?
- **Never test _how_ something works** — test _what_ it produces

---

## TDD Workflow (MANDATORY)

**RED-GREEN-REFACTOR is NON-NEGOTIABLE** — for new features AND refactors.

```
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌─────────┐
│   RED   │────▶│  GREEN  │────▶│ REFACTOR  │────▶│  AUDIT  │──╮
│  (Fail) │     │ (Pass)  │     │ (Improve) │     │ (Prune) │  │
└─────────┘     └─────────┘     └───────────┘     └─────────┘  │
     ▲                                                          │
     └──────────────────────────────────────────────────────────╯
```

1. **RED**: Write a failing test that describes the desired behavior
2. **GREEN**: Write the _minimum_ code to make it pass
3. **REFACTOR**: Improve structure while keeping tests green
4. **AUDIT**: After refactor, honestly evaluate the test suite (see Test Audit below)
5. **Repeat** for the next behavior

### Test Audit (Post-Refactor)

After every REFACTOR phase, ask yourself:

> "Be very honest — which of our tests are not actually protecting us?"

Make a list of tests that should be:
- **Refactored** — tests that assert implementation details instead of behavior
- **Deleted** — tests that add maintenance burden without catching real bugs

---

## Testing Trophy Balance

```
          /\
         /  \
        / E2E\           10%
       /──────\
      /        \
     /Integration\       70%  ← the bulk of your tests
    /──────────────\
   /                \
  /      Unit        \   20%
 /────────────────────\
```

| Layer | % | What to test | How |
|-------|---|-------------|-----|
| **E2E** | 10% | Critical user journeys | Real system, real I/O |
| **Integration** | 70% | Module interactions, data flow, contracts | Real dependencies where feasible |
| **Unit** | 20% | Pure functions, algorithms, edge cases | Isolated, fast, no I/O |

---

## What to Test vs What NOT to Test

### Test This (Behavior / Functionality)
- Given input X, function returns Y
- Given invalid input, function throws/rejects with specific error
- Given event A, system produces side effect B (file written, trace appended)
- Edge cases: empty input, boundary values, malformed data

### Never Test This (Implementation Details)
- Internal variable names or intermediate state
- Number of times a function was called
- Specific DOM element counts or CSS classes
- Execution order of internal steps
- That a private helper exists or was invoked

---

## Test Structure

### AAA Pattern (Arrange-Act-Assert)

```typescript
it('should calculate total correctly', () => {
  // Arrange - Set up test data
  const items = [
    { price: 10, quantity: 2 },
    { price: 5, quantity: 3 },
  ];

  // Act - Execute the code under test
  const total = calculateTotal(items);

  // Assert - Verify the result
  expect(total).toBe(35);
});
```

### Naming Convention

Pattern: `should [behavior] when [condition]`

**Good:**
- `it('should return user when found')`
- `it('should throw NotFoundError when id is invalid')`
- `it('should append trace to JSONL when input is valid')`

**Bad:**
- `it('works')` — what works?
- `it('test_get_user')` — too vague
- `it('calls createTrace')` — testing implementation, not behavior

---

## Coverage Requirements

- **Minimum 80%** overall
- **100% for critical paths** (hook contract, data integrity, auth)
- **Coverage decreases = CI failure**

---

## Mocking Best Practices

- Mock **external dependencies** (APIs, databases, file system) — not code you own
- Prefer **dependency injection** over global mocks
- Use **factories** for test data generation
- For integration tests, prefer **real dependencies** where feasible

```typescript
// GOOD - Inject dependency
const service = new UserService(mockDatabase);

// BAD - Global mock that hides real behavior
jest.mock('../database');
```

---

## Test Anti-Patterns (AVOID)

| Anti-Pattern | Why | Do Instead |
|--------------|-----|-----------|
| Testing implementation details | Brittle, breaks on refactor | Test inputs → outputs |
| Snapshot testing for logic | False confidence, rubber-stamped updates | Assert specific values |
| Tests without assertions | Pass vacuously | Every test asserts something |
| Multiple behaviors per test | Hard to diagnose failures | One behavior per `it()` block |
| Order-dependent tests | Flaky, non-deterministic | Each test sets up its own state |
| Mocking what you own | Hides real bugs | Use real code, mock boundaries |

---

## TDD Commit Flow

```bash
# RED phase — test describes desired behavior
git commit -m "test(scope): add tests for [behavior] (RED)"

# GREEN phase — minimal implementation passes
git commit -m "feat(scope): implement [behavior] (GREEN)"

# REFACTOR phase — improve without changing behavior
git commit -m "refactor(scope): simplify [what changed]"

# AUDIT phase — prune/refactor tests that don't earn their keep
git commit -m "test(scope): remove/refactor [what] — tests implementation not behavior"
```
