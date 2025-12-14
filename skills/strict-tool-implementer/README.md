# Strict Tool Implementer

Specialized skill for implementing strict tool use mode with guaranteed parameter validation.

## Purpose

This skill handles **end-to-end implementation** of strict tool use mode (`strict: true`), ensuring tool input parameters strictly follow your schema. Essential for building reliable agentic workflows with type-safe tool execution.

## Use Cases

- **Multi-Tool Agents**: Travel booking, research assistants, etc.
- **Validated Function Calls**: Ensure parameters match expected types
- **Complex Tool Schemas**: Tools with nested properties
- **Critical Operations**: Financial transactions, booking systems
- **Tool Composition**: Sequential and parallel tool execution

## Prerequisites

- Routed here by `structured-outputs-advisor`
- Model: Claude Sonnet 4.5 or Opus 4.1
- Beta header: `structured-outputs-2025-11-13`

## Quick Start

**Python:**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": "Search for flights..."}],
    tools=[{
        "name": "search_flights",
        "description": "Search for available flights",
        "strict": True,  # Enable strict validation
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string"},
                "destination": {"type": "string"},
                "travelers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6]}
            },
            "required": ["origin", "destination", "travelers"],
            "additionalProperties": False
        }
    }]
)

# Tool inputs GUARANTEED to match schema
for block in response.content:
    if block.type == "tool_use":
        execute_tool(block.name, block.input)  # Type-safe!
```

## What You'll Learn

1. **Tool Schema Design** - With `strict: true` and proper validation
2. **Multi-Tool Workflows** - Sequential and parallel tool execution
3. **Agent Patterns** - Stateful agents, retry logic, validation
4. **Error Handling** - Tool failures, refusals, edge cases
5. **Production Deployment** - Monitoring, testing, reliability

## Examples

- [travel-booking-agent.py](./examples/travel-booking-agent.py) - Multi-tool agent workflow

## Related Skills

- [`structured-outputs-advisor`](../structured-outputs-advisor/) - Choose the right mode
- [`json-outputs-implementer`](../json-outputs-implementer/) - For data extraction

## Reference Materials

- [JSON Schema Limitations](../reference/json-schema-limitations.md)
- [Best Practices](../reference/best-practices.md)
- [API Compatibility](../reference/api-compatibility.md)

## Version

Current version: 0.1.0

See [CHANGELOG.md](./CHANGELOG.md) for version history.
