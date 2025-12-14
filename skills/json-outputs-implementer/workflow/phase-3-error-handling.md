# Phase 3: Error Handling

**Objective**: Handle refusals, token limits, and validation errors

## Key Error Scenarios

### 1. Safety Refusals (`stop_reason: "refusal"`)

```python
if response.stop_reason == "refusal":
    logger.warning(f"Request refused: {input_text}")
    # Don't retry - respect safety boundaries
    return None  # or raise exception
```

### 2. Token Limit Reached (`stop_reason: "max_tokens"`)

```python
if response.stop_reason == "max_tokens":
    # Retry with higher limit
    return extract_with_higher_limit(text, max_tokens * 1.5)
```

### 3. Schema Validation Errors (SDK raises exception)

```python
from pydantic import ValidationError

try:
    result = response.parsed_output
except ValidationError as e:
    logger.error(f"Schema validation failed: {e}")
    # Should be rare - indicates schema mismatch
    raise
```

### 4. API Errors (400 - schema too complex)

```python
from anthropic import BadRequestError

try:
    response = client.beta.messages.parse(...)
except BadRequestError as e:
    if "too complex" in str(e).lower():
        # Simplify schema
        logger.error("Schema too complex, simplifying...")
    raise
```

## Output

Robust error handling for production deployments.
