# Phase 5: Production Optimization

**Objective**: Optimize for performance, cost, and reliability

## 1. Grammar Caching Strategy

The first request compiles a grammar from your schema (~extra latency). Subsequent requests use cached grammar (24-hour TTL).

**Cache Invalidation Triggers:**
- Schema structure changes
- Tool set changes (if using tools + JSON outputs together)
- 24 hours of non-use

**Best Practices:**
```python
# ✅ Good: Finalize schema before production
CONTACT_SCHEMA = ContactInfo  # Reuse same schema

# ❌ Bad: Dynamic schema generation
def get_schema(include_phone: bool):  # Different schemas = cache misses
    if include_phone:
        class Contact(BaseModel):
            phone: str
            ...
    ...
```

## 2. Token Cost Management

Structured outputs add tokens via system prompt:
```python
# Monitor token usage
response = client.beta.messages.parse(...)
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")

# Optimize descriptions for token efficiency
# ✅ Good: Concise but clear
name: str = Field(description="Full name")

# ❌ Excessive: Too verbose
name: str = Field(description="The complete full name of the person including first name, middle name if available, and last name")
```

## 3. Monitoring

```python
import time
from dataclasses import dataclass

@dataclass
class StructuredOutputMetrics:
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cache_hit: bool  # Infer from latency
    stop_reason: str

def track_metrics(response, start_time) -> StructuredOutputMetrics:
    latency = (time.time() - start_time) * 1000

    return StructuredOutputMetrics(
        latency_ms=latency,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        cache_hit=latency < 500,  # Heuristic: fast = cache hit
        stop_reason=response.stop_reason,
    )

# Track in production
metrics = track_metrics(response, start_time)
if metrics.latency_ms > 1000:
    logger.warning(f"Slow structured output: {metrics.latency_ms}ms")
```

## Output

Production-optimized implementation with caching and monitoring.
