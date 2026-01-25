# Phase 1: Tool Schema Design

**Objective**: Design validated tool schemas for your agent

## Steps

### 1. Identify Required Tools

Ask the user:
- "What actions should the agent be able to perform?"
- "What external systems will the agent interact with?"
- "What parameters does each tool need?"

**Example agent**: Travel booking
- `search_flights` - Find available flights
- `book_flight` - Reserve a flight
- `search_hotels` - Find hotels
- `book_hotel` - Reserve accommodation

### 2. Design Tool Schema with `strict: true`

**Template:**
```python
{
    "name": "tool_name",
    "description": "Clear description of what this tool does",
    "strict": True,  # ← Enables strict mode
    "input_schema": {
        "type": "object",
        "properties": {
            "param_name": {
                "type": "string",
                "description": "Clear parameter description"
            }
        },
        "required": ["param_name"],
        "additionalProperties": False  # ← Required
    }
}
```

**Example: Flight Search Tool**
```python
{
    "name": "search_flights",
    "description": "Search for available flights between two cities",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "Departure city (e.g., 'San Francisco, CA')"
            },
            "destination": {
                "type": "string",
                "description": "Arrival city (e.g., 'Paris, France')"
            },
            "departure_date": {
                "type": "string",
                "format": "date",
                "description": "Departure date in YYYY-MM-DD format"
            },
            "return_date": {
                "type": "string",
                "format": "date",
                "description": "Return date in YYYY-MM-DD format (optional)"
            },
            "travelers": {
                "type": "integer",
                "enum": [1, 2, 3, 4, 5, 6],
                "description": "Number of travelers"
            },
            "class": {
                "type": "string",
                "enum": ["economy", "premium", "business", "first"],
                "description": "Flight class preference"
            }
        },
        "required": ["origin", "destination", "departure_date", "travelers"],
        "additionalProperties": False
    }
}
```

### 3. Apply JSON Schema Limitations

**✅ Supported:**
- All basic types (object, array, string, integer, number, boolean)
- `enum` for constrained values
- `format` for strings (date, email, uri, uuid, etc.)
- Nested objects and arrays
- `required` fields
- `additionalProperties: false` (required!)

**❌ NOT Supported:**
- Recursive schemas
- Numerical constraints (minimum, maximum)
- String length constraints
- Complex regex patterns

### 4. Add Clear Descriptions

Good descriptions help Claude:
- Understand when to call the tool
- Know what values to provide
- Format parameters correctly

```python
# ✅ Good: Clear and specific
"origin": {
    "type": "string",
    "description": "Departure city and state/country (e.g., 'San Francisco, CA')"
}

# ❌ Vague: Not helpful
"origin": {
    "type": "string",
    "description": "Origin"
}
```

## Output

Well-designed tool schemas ready for implementation.
