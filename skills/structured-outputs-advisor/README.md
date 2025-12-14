# Structured Outputs Advisor

Expert advisor skill for choosing between JSON outputs and strict tool use modes in Anthropic's structured outputs feature.

## Purpose

This skill serves as the **entry point** for implementing structured outputs. It analyzes your requirements and recommends the right mode:

- **JSON Outputs** (`output_format`) - For data extraction, classification, API formatting
- **Strict Tool Use** (`strict: true`) - For agentic workflows, validated tool parameters

Then delegates to specialized implementation skills.

## When to Use

Invoke this skill when you need:
- Guaranteed JSON schema compliance
- Validated tool input parameters
- Structured data extraction
- Type-safe API responses
- Reliable agentic workflows

## Quick Start

**Trigger phrases:**
- "implement structured outputs"
- "need guaranteed JSON schema"
- "extract structured data from..."
- "build reliable agent with validated tools"

The advisor will ask questions to understand your use case and recommend the appropriate mode.

## Workflow

1. **Requirements gathering** - Understand what you're building
2. **Mode selection** - JSON outputs vs strict tool use
3. **Delegation** - Hand off to specialized skill for implementation

## Related Skills

- [`json-outputs-implementer`](../json-outputs-implementer/) - Implements JSON outputs mode
- [`strict-tool-implementer`](../strict-tool-implementer/) - Implements strict tool use mode

## Examples

See [mode-selection-examples.md](./examples/mode-selection-examples.md) for detailed scenarios.

## Documentation

- [Official Structured Outputs Docs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs)
- [JSON Schema Limitations](./reference/json-schema-limitations.md)
- [Best Practices](./reference/best-practices.md)
- [API Compatibility](./reference/api-compatibility.md)

## Version

Current version: 0.1.0

See [CHANGELOG.md](./CHANGELOG.md) for version history.
