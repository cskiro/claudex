---
paths:
  - "**/*.py"
---

<!-- Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync -->

# Python Standards

These rules apply **only when working with Python files**.

---

## Type Safety (MANDATORY)

- **All public functions MUST have type hints**
- **mypy strict mode enforced**
- **Use `from __future__ import annotations`** for forward references
- **Validate inputs at function boundaries** - Fail fast

**Example**:
```python
from __future__ import annotations

# GOOD
def get_user(user_id: str) -> User | None:
    if not user_id:
        raise ValueError("user_id is required")
    return db.query(User).filter_by(id=user_id).first()

# BAD
def get_user(user_id):
    return db.query(User).filter_by(id=user_id).first()
```

---

## Code Quality (MANDATORY)

- Format with **Black** (line length 88)
- Lint with **Ruff**
- Type-check with **mypy** after EVERY file change

**Commands**:
```bash
black src/
ruff check src/
mypy src/
```

---

## Naming Conventions

- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods/attributes: `_single_underscore`
- "Truly private": `__double_underscore` (name mangling)

---

## Docstrings (Google Style)

Use Google-style docstrings for all public functions:

```python
def calculate_score(
    items: list[Item],
    weights: dict[str, float],
    normalize: bool = True,
) -> float:
    """Calculate weighted score from items.

    Args:
        items: List of items to score.
        weights: Weight factors by item type.
        normalize: Whether to normalize to 0-1 range.

    Returns:
        Calculated score value.

    Raises:
        ValueError: If items is empty.
        KeyError: If weight not found for item type.
    """
```

---

## Error Handling

- **Never catch exceptions silently**
- Use **specific exception types**
- Log with context (correlation ID, user ID, etc.)

**Example**:
```python
# GOOD
try:
    user = await get_user(user_id)
except UserNotFoundError:
    logger.warning("User not found", extra={"user_id": user_id})
    raise
except DatabaseError as e:
    logger.error("Database error", extra={"user_id": user_id, "error": str(e)})
    raise ServiceUnavailableError("Database temporarily unavailable") from e

# BAD
try:
    user = await get_user(user_id)
except:
    return None  # Silent failure!
```

---

## Imports Organization

Group imports in this order (separated by blank lines):
1. Standard library (`os`, `sys`, `typing`)
2. Third-party packages (`fastapi`, `pydantic`)
3. Local imports (`from .models import User`)

**Use `isort`** to auto-format imports.

---

## Functional Patterns (PREFERRED)

- Pure functions (no side effects)
- Immutable data structures
- List/dict comprehensions over loops
- Avoid global state mutation

**Example**:
```python
# GOOD - Pure function
def calculate_total(items: list[Item]) -> Decimal:
    return sum(item.price * item.quantity for item in items)

# BAD - Side effect
total = Decimal(0)
def add_to_total(item: Item) -> None:
    global total
    total += item.price * item.quantity
```

---

## Configuration (Pydantic)

Use Pydantic for configuration validation:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```
