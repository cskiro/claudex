# Structured Outputs Best Practices

Production-ready patterns and recommendations for implementing structured outputs with Claude.

## Schema Design

### 1. Start Simple, Iterate

Begin with minimal schemas and expand based on real-world needs:

```python
# ✅ Phase 1: Start simple
class Contact(BaseModel):
    name: str
    email: str

# ✅ Phase 2: Add based on usage
class Contact(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None  # Added after finding it's sometimes available
    company: Optional[str] = None  # Added after customer feedback

# ❌ Don't start with everything
class Contact(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    fax: Optional[str] = None  # Rarely used
    pager: Optional[str] = None  # Never used
    # ... 20 more optional fields
```

### 2. Use Clear, Descriptive Names

Field names should be self-documenting:

```python
# ✅ Good: Clear and specific
class Invoice(BaseModel):
    invoice_number: str
    issue_date: str
    due_date: str
    total_amount_usd: float

# ❌ Poor: Ambiguous
class Invoice(BaseModel):
    num: str
    date: str  # Which date?
    date2: str  # Unclear
    amt: float  # What currency?
```

### 3. Add Comprehensive Descriptions

Descriptions help Claude understand what to extract:

```python
# ✅ Good: Detailed descriptions
class Product(BaseModel):
    sku: str = Field(description="Product SKU code (format: PROD-XXXXX)")
    name: str = Field(description="Product display name")
    price: float = Field(description="Price in USD before tax")
    category: str = Field(description="Product category (electronics, clothing, etc.)")

# ❌ Minimal: Not helpful
class Product(BaseModel):
    sku: str
    name: str
    price: float
    category: str
```

### 4. Use Enums for Constrained Values

Enums are better than free-text for known sets:

```python
# ✅ Good: Enum for known values
from enum import Enum

class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Ticket(BaseModel):
    priority: PriorityLevel

# ❌ Free text: Can produce unexpected values
class Ticket(BaseModel):
    priority: str  # Could be "Low", "HIGH", "urgent", "!!!", etc.
```

### 5. Make Required Fields Explicit

Only mark fields as required if they're truly mandatory:

```python
# ✅ Good: Clear required vs optional
class User(BaseModel):
    email: str  # Required - always present
    name: str  # Required - always present
    phone: Optional[str] = None  # Optional - might be missing
    company: Optional[str] = None  # Optional - might be missing

# ❌ Everything required: Will fail on missing data
class User(BaseModel):
    email: str
    name: str
    phone: str  # Fails if phone not in data
    company: str  # Fails if company not in data
```

---

## SDK Integration

### 1. Use `client.beta.messages.parse()` (Python)

Automatic validation and parsing:

```python
# ✅ Recommended: Automatic validation
response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    output_format=MyModel,
    messages=[...]
)
result = response.parsed_output  # Already validated

# ❌ Manual: More error-prone
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    output_format={"type": "json_schema", "schema": my_schema},
    messages=[...]
)
import json
result = json.loads(response.content[0].text)  # No validation
```

### 2. Use Zod/Pydantic Over Raw JSON

Type-safe schema definitions:

```typescript
// ✅ Good: Zod (TypeScript)
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string(),
  age: z.number().int().positive(),
  email: z.string().email(),
});

// ❌ Manual JSON: Error-prone
const userSchema = {
  type: "object",
  properties: {
    name: { type: "string" },
    age: { type: "integer" },  // Typo: "number" instead of "integer"?
    email: { type: "string" },
  },
  required: ["name", "age", "email"],
  additionalProperties: false  // Easy to forget
};
```

```python
# ✅ Good: Pydantic (Python)
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    age: int
    email: EmailStr

# ❌ Manual: Verbose and error-prone
user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age", "email"],
    "additionalProperties": False
}
```

### 3. Let SDKs Handle Transformation

Don't manually work around limitations:

```python
# ✅ Good: Let SDK transform
from pydantic import BaseModel, Field

class User(BaseModel):
    age: int = Field(ge=0, le=120)  # SDK adds to description

# ❌ Manual workaround: Unnecessary
class User(BaseModel):
    age: int = Field(description="Age (must be 0-120)")  # Manual constraint
```

---

## Error Handling

### 1. Handle All Stop Reasons

```python
response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    output_format=MyModel,
    messages=[...]
)

# ✅ Good: Handle all cases
if response.stop_reason == "refusal":
    logger.warning("Request refused for safety")
    return None  # Don't retry

elif response.stop_reason == "max_tokens":
    logger.warning("Response truncated")
    return retry_with_higher_max_tokens(messages)

elif response.stop_reason == "end_turn":
    return response.parsed_output

else:
    raise ValueError(f"Unexpected stop_reason: {response.stop_reason}")

# ❌ Assumes success
return response.parsed_output  # Breaks on refusal or max_tokens
```

### 2. Set Appropriate max_tokens

Different schemas need different token limits:

```python
# ✅ Good: Set based on expected output size
simple_extraction = client.beta.messages.parse(
    max_tokens=512,  # Small extraction
    output_format=ContactInfo,
    ...
)

complex_report = client.beta.messages.parse(
    max_tokens=4096,  # Large nested structure
    output_format=DetailedReport,
    ...
)

# ❌ Too low: Truncates responses
response = client.beta.messages.parse(
    max_tokens=100,  # Often too small
    output_format=LargeSchema,
    ...
)
```

### 3. Log Validation Failures

Track when schemas don't match expectations:

```python
from pydantic import ValidationError

try:
    result = response.parsed_output
except ValidationError as e:
    logger.error(
        "Schema validation failed",
        extra={
            "schema": MyModel.__name__,
            "errors": e.errors(),
            "response": response.content[0].text if response.content else None
        }
    )
    # Alert monitoring system
    metrics.increment("structured_output.validation_error")
    raise
```

---

## Performance Optimization

### 1. Minimize Schema Changes

Grammar compilation happens on schema changes:

```python
# ✅ Good: Stable schema, reused across requests
CONTACT_SCHEMA = ContactInfo

for email in emails:
    response = client.beta.messages.parse(
        output_format=CONTACT_SCHEMA,  # Same schema = cached grammar
        ...
    )

# ❌ Dynamic schemas: Cache miss every time
for email in emails:
    schema = create_dynamic_schema(email)  # Different each time
    response = client.beta.messages.parse(
        output_format=schema,  # Grammar recompiled
        ...
    )
```

### 2. Cache Hit Indicators

Monitor latency to detect cache misses:

```python
import time

start = time.time()
response = client.beta.messages.parse(...)
latency_ms = (time.time() - start) * 1000

if latency_ms > 1000:
    logger.warning(f"Slow request ({latency_ms}ms) - possible cache miss")
    metrics.histogram("structured_output.latency", latency_ms, tags=["cache:miss"])
else:
    metrics.histogram("structured_output.latency", latency_ms, tags=["cache:hit"])
```

### 3. Optimize Token Usage

Minimize unnecessary verbosity:

```python
# ✅ Good: Concise but clear
name: str = Field(description="Full name")

# ❌ Excessive: Wastes tokens
name: str = Field(
    description="The complete full name of the individual person including "
    "their first name, any middle names they may have, and their last name "
    "or surname, formatted as a single string value"
)
```

### 4. Batch When Possible

Use batch API for large-scale extraction:

```python
# ✅ Good: Batch processing (50% discount)
from anthropic import Anthropic

client = Anthropic()

# Create batch with structured outputs
requests = [
    {
        "custom_id": f"req_{i}",
        "params": {
            "model": "claude-sonnet-4-5",
            "max_tokens": 1024,
            "betas": ["structured-outputs-2025-11-13"],
            "messages": [{"role": "user", "content": text}],
            "output_format": {"type": "json_schema", "schema": my_schema}
        }
    }
    for i, text in enumerate(documents)
]

# Submit batch
batch = client.beta.messages.batches.create(requests=requests)

# ❌ Sequential API calls: Full price
for text in documents:
    response = client.beta.messages.parse(...)
```

---

## Production Monitoring

### 1. Track Key Metrics

```python
from dataclasses import dataclass
import time

@dataclass
class StructuredOutputMetrics:
    latency_ms: float
    input_tokens: int
    output_tokens: int
    stop_reason: str
    schema_name: str
    cache_hit: bool

def track_request(schema_name: str):
    start = time.time()

    response = client.beta.messages.parse(...)

    metrics = StructuredOutputMetrics(
        latency_ms=(time.time() - start) * 1000,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        stop_reason=response.stop_reason,
        schema_name=schema_name,
        cache_hit=(time.time() - start) < 0.5  # Heuristic
    )

    # Send to monitoring
    monitor.record(metrics)

    return response.parsed_output
```

### 2. Alert on Anomalies

```python
# Alert on high refusal rate
if refusal_rate > 0.05:  # >5% refusals
    alert("High refusal rate for structured outputs")

# Alert on validation failures
if validation_failure_rate > 0.01:  # >1% failures
    alert("Schema validation failures detected")

# Alert on slow requests
if p95_latency > 2000:  # >2s at P95
    alert("Slow structured output requests")
```

### 3. Cost Tracking

```python
# Track costs per schema type
cost_per_1k_tokens = {
    "input": 0.003,  # Sonnet 4.5 pricing
    "output": 0.015,
}

def calculate_cost(response):
    input_cost = (response.usage.input_tokens / 1000) * cost_per_1k_tokens["input"]
    output_cost = (response.usage.output_tokens / 1000) * cost_per_1k_tokens["output"]

    total_cost = input_cost + output_cost

    metrics.histogram(
        "structured_output.cost_usd",
        total_cost,
        tags=[f"schema:{schema_name}"]
    )

    return total_cost
```

---

## Testing

### 1. Test with Representative Data

```python
import pytest

@pytest.mark.parametrize("input_text,expected", [
    (
        "John Smith (john@example.com) wants Enterprise plan",
        {"name": "John Smith", "email": "john@example.com", "plan": "Enterprise"}
    ),
    (
        "Contact: jane@example.com",  # Missing name
        {"email": "jane@example.com"}
    ),
    (
        "Call me at 555-1234",  # No email
        None  # Should handle gracefully
    ),
])
def test_contact_extraction(input_text, expected):
    result = extract_contact(input_text)

    if expected is None:
        assert result is None
    else:
        for key, value in expected.items():
            assert getattr(result, key) == value
```

### 2. Test Edge Cases

```python
def test_empty_input():
    """Test with empty string."""
    result = extract_contact("")
    # Define expected behavior

def test_very_long_input():
    """Test with input exceeding context window."""
    long_text = "..." * 100000
    # Should handle or raise appropriate error

def test_malformed_data():
    """Test with unexpected format."""
    result = extract_contact("@#$%^&*()")
    # Should handle gracefully

def test_unicode_input():
    """Test with international characters."""
    result = extract_contact("名前: yamada@example.com")
    # Should handle correctly
```

### 3. Test Schema Evolution

```python
def test_schema_backward_compatible():
    """Ensure new schema handles old data."""

    # Old format
    old_data = '{"name": "John", "email": "john@example.com"}'

    # New schema with additional optional field
    class ContactV2(BaseModel):
        name: str
        email: str
        phone: Optional[str] = None  # New optional field

    # Should still work
    result = ContactV2.model_validate_json(old_data)
    assert result.name == "John"
    assert result.phone is None
```

---

## Common Pitfalls

### ❌ Pitfall 1: Forgetting `additionalProperties: false`

```python
# ❌ Will fail
schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"]
    # Missing: "additionalProperties": false
}

# ✅ Correct
schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
    "additionalProperties": false
}
```

### ❌ Pitfall 2: Using Complex Enums

```python
# ❌ Won't work
status: dict = Field(enum=[{"code": 200}, {"code": 404}])

# ✅ Use strings or simple types
status_code: int = Field(enum=[200, 404, 500])
```

### ❌ Pitfall 3: Not Handling Refusals

```python
# ❌ Assumes success
result = response.parsed_output  # Breaks on refusal

# ✅ Check stop_reason
if response.stop_reason == "refusal":
    handle_refusal()
else:
    result = response.parsed_output
```

### ❌ Pitfall 4: Recursive Schemas

```python
# ❌ Not supported
class Node(BaseModel):
    value: str
    children: List['Node']  # Recursive!

# ✅ Flatten to fixed depth
class Node(BaseModel):
    value: str
    children: List['NodeLevel2']

class NodeLevel2(BaseModel):
    value: str
    # No more nesting
```

---

## Quick Checklist

Before deploying to production:

- [ ] Schema uses only supported JSON Schema features
- [ ] All objects have `additionalProperties: false`
- [ ] Required fields are truly mandatory
- [ ] Enums used for constrained values
- [ ] Clear descriptions on all fields
- [ ] Error handling for all stop_reason values
- [ ] Appropriate `max_tokens` set
- [ ] Tested with representative data
- [ ] Edge cases covered in tests
- [ ] Monitoring/metrics in place
- [ ] Cost tracking configured
- [ ] Schema versioned and documented

---

**See Also:**
- [JSON Schema Limitations](./json-schema-limitations.md)
- [API Compatibility](./api-compatibility.md)
- [Official Documentation](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs)
