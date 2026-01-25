# API Compatibility Reference

Complete compatibility matrix for structured outputs with other Claude API features.

## Feature Availability

### Supported Models

| Model | JSON Outputs | Strict Tool Use | Notes |
|-------|--------------|-----------------|-------|
| Claude Sonnet 4.5 (`claude-sonnet-4-5`) | ✅ | ✅ | Recommended - best performance |
| Claude Opus 4.1 (`claude-opus-4-1`) | ✅ | ✅ | Maximum capability |
| Claude 3.5 Sonnet (legacy) | ❌ | ❌ | Not supported |
| Claude 3 Opus (legacy) | ❌ | ❌ | Not supported |
| Claude 3 Haiku | ❌ | ❌ | Not supported |

**Requirements:**
- Beta header: `anthropic-beta: structured-outputs-2025-11-13`
- Model must be Sonnet 4.5 or Opus 4.1

---

## Compatible Features

### ✅ Batch Processing

Structured outputs work with batch API for 50% cost savings:

```python
from anthropic import Anthropic

client = Anthropic()

# Create batch with structured outputs
batch_requests = [
    {
        "custom_id": f"extraction_{i}",
        "params": {
            "model": "claude-sonnet-4-5",
            "max_tokens": 1024,
            "betas": ["structured-outputs-2025-11-13"],
            "messages": [{"role": "user", "content": document}],
            "output_format": {
                "type": "json_schema",
                "schema": extraction_schema
            }
        }
    }
    for i, document in enumerate(documents)
]

# Submit batch
batch = client.beta.messages.batches.create(requests=batch_requests)

# Poll for completion
while batch.processing_status != "ended":
    time.sleep(60)
    batch = client.beta.messages.batches.retrieve(batch.id)

# Retrieve results
for result in batch.results:
    parsed_output = json.loads(result.result.content[0].text)
```

**Benefits:**
- 50% cost reduction
- Ideal for large-scale data extraction
- Structured outputs guarantee schema compliance even in batch mode

---

### ✅ Token Counting

Count tokens before making requests:

```python
# Count tokens for structured output request
token_count = client.beta.messages.count_tokens(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": "Extract contact info..."}],
    output_format={"type": "json_schema", "schema": contact_schema},
)

print(f"Input tokens (including system prompt): {token_count.input_tokens}")

# Estimate cost
input_cost = (token_count.input_tokens / 1000) * 0.003  # Sonnet 4.5 pricing
print(f"Estimated input cost: ${input_cost:.4f}")
```

**Note:**
- Token counting includes the injected system prompt for structured outputs
- Output tokens can't be precisely counted beforehand (depends on Claude's response)

---

### ✅ Streaming

Stream structured outputs as they're generated:

```python
# Stream JSON outputs
stream = client.beta.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": "Extract data..."}],
    output_format={"type": "json_schema", "schema": my_schema},
)

with stream as s:
    for text in s.text_stream:
        print(text, end="", flush=True)

# Final response
final_response = stream.get_final_message()
parsed_output = json.loads(final_response.content[0].text)
```

**Notes:**
- Streamed content is still guaranteed to match schema
- Grammar constraints apply throughout streaming
- Final assembled response is validated

---

### ✅ Combined JSON Outputs + Strict Tool Use

Use both modes in the same request:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    max_tokens=2048,
    messages=[{"role": "user", "content": "Analyze this data and search for related info"}],

    # JSON outputs for final response
    output_format={
        "type": "json_schema",
        "schema": analysis_schema
    },

    # Strict tool use for tool calls
    tools=[{
        "name": "search_database",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }]
)

# Tool calls have validated inputs
# Final response matches analysis_schema
```

**Use Cases:**
- Agent gathers data via tools (strict mode)
- Agent returns analysis in structured format (JSON outputs)

**Important:**
- Changing either schema OR tool set invalidates grammar cache
- More complex than using one mode alone

---

## Incompatible Features

### ❌ Citations

Citations cannot be used with JSON outputs:

```python
# ❌ This will fail with 400 error
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13", "pdfs-2024-09-25"],
    messages=[...],
    output_format={"type": "json_schema", "schema": my_schema},  # Incompatible!
)
```

**Reason:**
Citations require interleaving citation blocks with text, which conflicts with strict JSON schema constraints.

**Workaround:**
Choose one:
1. Use citations without `output_format` (no schema guarantee)
2. Use `output_format` without citations (schema guaranteed, no citations)

---

### ❌ Message Prefilling (with JSON Outputs)

Message prefilling is incompatible with JSON outputs:

```python
# ❌ This may not work as expected
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[
        {"role": "user", "content": "Extract contact info"},
        {"role": "assistant", "content": "{"}  # Prefill
    ],
    output_format={"type": "json_schema", "schema": contact_schema},
)
```

**Reason:**
Grammar constraints start fresh and don't account for prefilled content.

**Workaround:**
Don't use prefilling with JSON outputs - let Claude generate complete response.

---

## Grammar Scope

### What Grammar Applies To

Grammars constrain:
- ✅ Claude's direct text output (when using JSON outputs)
- ✅ Tool `input` values (when using strict tool use)

Grammars do NOT constrain:
- ❌ Tool use `name` field (validated separately)
- ❌ Tool results (your application's output)
- ❌ Thinking tags (when using Extended Thinking)

**Example with Extended Thinking:**

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    thinking={
        "type": "enabled",
        "budget_tokens": 1024
    },
    messages=[{"role": "user", "content": "Extract and analyze..."}],
    output_format={"type": "json_schema", "schema": analysis_schema},
)

# Response structure:
# [
#   {"type": "thinking", "thinking": "..."},  # Free-form thinking (NO grammar)
#   {"type": "text", "text": "{...}"}  # Structured output (grammar applied)
# ]
```

**Grammar resets** between sections, allowing free-form thinking while guaranteeing structured final output.

---

## Prompt Caching Interaction

### Cache Invalidation

Changing `output_format` invalidates prompt cache:

```python
# First request - sets cache
response1 = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13", "prompt-caching-2024-07-31"],
    messages=[
        {
            "role": "user",
            "content": large_document,
            "cache_control": {"type": "ephemeral"}
        },
        {"role": "user", "content": "Extract contacts"}
    ],
    output_format=contact_schema,
)

# Second request - CACHE MISS if schema changes
response2 = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13", "prompt-caching-2024-07-31"],
    messages=[
        {
            "role": "user",
            "content": large_document,  # Same cached content
            "cache_control": {"type": "ephemeral"}
        },
        {"role": "user", "content": "Extract contacts"}
    ],
    output_format=invoice_schema,  # Different schema = cache invalidated
)
```

**Best Practice:**
Keep schemas stable when using prompt caching for multi-turn conversations.

---

## Performance Considerations

### Grammar Compilation

**First Request (Cold Start):**
- Grammar compilation adds latency (~500-1500ms)
- One-time cost per unique schema
- Cached for 24 hours

**Subsequent Requests (Warm):**
- Use cached grammar
- Fast response (~200-500ms baseline)

**Cache Invalidation:**
- Schema structure changes
- Tool set changes (when using both structured outputs + tools)
- 24-hour timeout

### Token Overhead

Structured outputs add token costs:

```python
# Without structured outputs
base_input_tokens = 150

# With structured outputs
structured_input_tokens = 150 + ~50  # System prompt injection

# Additional cost
extra_cost = (50 / 1000) * 0.003  # ~$0.00015 per request
```

**Optimization:**
- Minimize schema complexity to reduce system prompt size
- Reuse schemas across requests for grammar caching

---

## Quick Reference Matrix

| Feature | JSON Outputs | Strict Tool Use | Notes |
|---------|--------------|-----------------|-------|
| Batch Processing | ✅ | ✅ | 50% discount applies |
| Token Counting | ✅ | ✅ | Includes system prompt |
| Streaming | ✅ | ✅ | Schema guaranteed during stream |
| Citations | ❌ | ✅ | Citations incompatible with JSON outputs only |
| Message Prefilling | ❌ | ✅ | Prefilling incompatible with JSON outputs only |
| Prompt Caching | ✅ | ✅ | Schema changes invalidate cache |
| Extended Thinking | ✅ | ✅ | Grammar doesn't apply to thinking blocks |
| Combined Modes | ✅ | ✅ | Can use both in same request |
| Multi-turn Conversations | ✅ | ✅ | Fully supported |

---

## Migration Path

### From Regular API to Structured Outputs

**Before (No guarantees):**
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{
        "role": "user",
        "content": "Extract contact info as JSON: " + text
    }]
)

# Parse and validate manually
try:
    data = json.loads(response.content[0].text)
    contact = ContactInfo(**data)  # Might fail
except (json.JSONDecodeError, ValidationError):
    # Handle errors, retry, etc.
    pass
```

**After (Guaranteed):**
```python
response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": text}],
    output_format=ContactInfo,
)

contact = response.parsed_output  # Guaranteed valid
```

**Benefits:**
- No JSON parsing errors
- No schema validation errors
- No retry logic needed for schema violations
- Cleaner code

---

**See Also:**
- [JSON Schema Limitations](./json-schema-limitations.md)
- [Best Practices](./best-practices.md)
- [Official Documentation](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs)
