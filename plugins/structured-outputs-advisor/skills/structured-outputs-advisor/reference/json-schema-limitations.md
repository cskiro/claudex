# JSON Schema Limitations Reference

Complete reference for JSON Schema support in Anthropic's structured outputs feature (both JSON outputs and strict tool use modes).

## Supported Features

### Basic Types ✅

All basic JSON Schema types are fully supported:

- `object`
- `array`
- `string`
- `integer`
- `number`
- `boolean`
- `null`

**Example:**
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "score": {"type": "number"},
    "active": {"type": "boolean"},
    "metadata": {"type": "null"}
  }
}
```

### Enumerations ✅

`enum` is supported for primitive types only (strings, numbers, booleans, nulls).

**✅ Supported:**
```json
{
  "status": {
    "type": "string",
    "enum": ["pending", "approved", "rejected"]
  },
  "priority": {
    "type": "integer",
    "enum": [1, 2, 3, 4, 5]
  },
  "enabled": {
    "type": "boolean",
    "enum": [true, false]
  }
}
```

**❌ NOT Supported:**
```json
{
  "config": {
    "enum": [
      {"mode": "fast"},
      {"mode": "accurate"}
    ]
  }
}
```
*Reason: Complex types in enum not supported*

### Constants ✅

`const` is fully supported:

```json
{
  "api_version": {
    "type": "string",
    "const": "v1.0"
  }
}
```

### Composition ✅ (Limited)

**Supported:**
- `anyOf` - Choose one of multiple schemas
- `allOf` - Must match all schemas (limited - see below)

**✅ anyOf Example:**
```json
{
  "contact": {
    "anyOf": [
      {"type": "string", "format": "email"},
      {"type": "string", "format": "uri"}
    ]
  }
}
```

**⚠️ allOf Limitations:**
```json
// ✅ Simple allOf works
{
  "allOf": [
    {"type": "object", "properties": {"name": {"type": "string"}}},
    {"type": "object", "properties": {"age": {"type": "integer"}}}
  ]
}

// ❌ allOf with $ref not supported
{
  "allOf": [
    {"$ref": "#/definitions/Base"},
    {"properties": {"extra": {"type": "string"}}}
  ]
}
```

### References ✅ (Local Only)

**Supported:**
- `$ref` - Local references only
- `$def` - Definitions
- `definitions` - Legacy definitions syntax

**✅ Local References:**
```json
{
  "definitions": {
    "Address": {
      "type": "object",
      "properties": {
        "street": {"type": "string"},
        "city": {"type": "string"}
      }
    }
  },
  "properties": {
    "billing": {"$ref": "#/definitions/Address"},
    "shipping": {"$ref": "#/definitions/Address"}
  }
}
```

**❌ External References:**
```json
{
  "$ref": "https://example.com/schemas/address.json"
}
```
*Reason: External $ref not supported*

### Object Properties ✅

**Supported:**
- `properties` - Define object properties
- `required` - List required fields
- `additionalProperties: false` - **REQUIRED** for structured outputs

**Example:**
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "email": {"type": "string"}
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

**⚠️ Important:**
- `additionalProperties` MUST be set to `false`
- `additionalProperties: true` or `additionalProperties: {...}` NOT supported

### String Formats ✅

**Supported Formats:**
- `date-time` - ISO 8601 date-time
- `time` - Time only
- `date` - Date only (YYYY-MM-DD)
- `duration` - ISO 8601 duration
- `email` - Email address
- `hostname` - Valid hostname
- `uri` - URI
- `ipv4` - IPv4 address
- `ipv6` - IPv6 address
- `uuid` - UUID

**Example:**
```json
{
  "created_at": {"type": "string", "format": "date-time"},
  "birthday": {"type": "string", "format": "date"},
  "email": {"type": "string", "format": "email"},
  "website": {"type": "string", "format": "uri"},
  "id": {"type": "string", "format": "uuid"}
}
```

**❌ Unsupported Formats:**
Any format not in the list above will be ignored.

### Array Constraints ✅ (Very Limited)

**Supported:**
- `minItems: 0` - Array can be empty
- `minItems: 1` - Array must have at least one item

**✅ Example:**
```json
{
  "tags": {
    "type": "array",
    "items": {"type": "string"},
    "minItems": 1
  }
}
```

**❌ NOT Supported:**
- `minItems` > 1
- `maxItems`
- `uniqueItems`
- `contains`

### Default Values ✅

`default` is supported for all types:

```json
{
  "status": {
    "type": "string",
    "default": "pending"
  },
  "priority": {
    "type": "integer",
    "default": 3
  },
  "tags": {
    "type": "array",
    "items": {"type": "string"},
    "default": []
  }
}
```

---

## NOT Supported Features

### Recursive Schemas ❌

**Not Allowed:**
```json
{
  "definitions": {
    "Node": {
      "type": "object",
      "properties": {
        "value": {"type": "string"},
        "children": {
          "type": "array",
          "items": {"$ref": "#/definitions/Node"}
        }
      }
    }
  }
}
```

**Workaround:** Flatten to fixed depth:
```json
{
  "definitions": {
    "Node": {
      "type": "object",
      "properties": {
        "value": {"type": "string"},
        "children": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "value": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

### Numerical Constraints ❌

**NOT Supported:**
- `minimum` / `exclusiveMinimum`
- `maximum` / `exclusiveMaximum`
- `multipleOf`

**Example (Will Fail):**
```json
{
  "age": {
    "type": "integer",
    "minimum": 0,
    "maximum": 120
  }
}
```

**SDK Transformation:**
Python/TypeScript SDKs will:
1. Remove the constraint
2. Add to description: "Must be between 0 and 120"
3. Validate response against original constraint

**Manual Workaround:**
```json
{
  "age": {
    "type": "integer",
    "description": "Age in years (must be between 0 and 120)"
  }
}
```
Then validate in application code.

### String Constraints ❌

**NOT Supported:**
- `minLength` / `maxLength`
- Complex `pattern` (regex)

**Example (Will Fail):**
```json
{
  "username": {
    "type": "string",
    "minLength": 3,
    "maxLength": 20,
    "pattern": "^[a-zA-Z0-9_]+$"
  }
}
```

**SDK Transformation:**
Adds to description: "Must be 3-20 characters, alphanumeric with underscores"

**Manual Approach:**
```json
{
  "username": {
    "type": "string",
    "description": "Username (3-20 characters, alphanumeric and underscores only)"
  }
}
```

### Pattern (Regex) ⚠️ (Limited Support)

**✅ Simple Patterns Work:**
- Basic quantifiers: `*`, `+`, `?`, `{n,m}` (simple cases)
- Character classes: `[]`, `.`, `\d`, `\w`, `\s`
- Groups: `(...)`
- Anchors: `^`, `$`

**❌ NOT Supported:**
- Backreferences: `\1`, `\2`
- Lookahead/lookbehind: `(?=...)`, `(?!...)`, `(?<=...)`, `(?<!...)`
- Word boundaries: `\b`, `\B`
- Complex quantifiers: `{100,500}`

**✅ Example (Works):**
```json
{
  "phone": {
    "type": "string",
    "pattern": "^\\d{3}-\\d{3}-\\d{4}$"
  }
}
```

**❌ Example (Fails):**
```json
{
  "repeated": {
    "type": "string",
    "pattern": "^(\\w+)\\s+\\1$"
  }
}
```

### Array Constraints (Beyond minItems) ❌

**NOT Supported:**
- `maxItems`
- `minItems` > 1
- `uniqueItems`
- `contains`
- Tuple validation (fixed-length arrays with different types)

### Additional Properties ❌

**Required:**
```json
{
  "additionalProperties": false
}
```

**NOT Supported:**
- `additionalProperties: true`
- `additionalProperties: {...}` (schema for additional properties)

### Dependencies ❌

**NOT Supported:**
- `dependencies`
- `dependentSchemas`
- `dependentRequired`

---

## SDK Transformation

### How SDKs Handle Unsupported Features

Both Python (`anthropic`) and TypeScript (`@anthropic-ai/sdk`) SDKs automatically transform schemas:

**Transformation Steps:**
1. **Remove** unsupported constraints (minimum, maximum, minLength, maxLength, etc.)
2. **Update descriptions** to include constraint information
3. **Add** `additionalProperties: false` to all objects
4. **Filter** string formats to supported list only
5. **Validate** responses against original schema (with all constraints)

**Example:**

**Original Pydantic Model:**
```python
class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=0, le=120)
    email: str
```

**Sent to API (Transformed):**
```json
{
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "description": "Must be at least 3 characters and at most 20 characters"
    },
    "age": {
      "type": "integer",
      "description": "Must be greater than or equal to 0 and less than or equal to 120"
    },
    "email": {"type": "string"}
  },
  "required": ["username", "age", "email"],
  "additionalProperties": false
}
```

**Response Validation:**
SDK validates response against original constraints (min_length, max_length, ge, le).

---

## Error Messages

### Common Schema Validation Errors

**"Too many recursive definitions in schema"**
- **Cause:** Schema has cyclic recursive definitions
- **Solution:** Remove recursion or flatten to fixed depth

**"Schema is too complex"**
- **Cause:** Schema exceeds complexity limits
- **Solution:** Simplify structure, reduce nesting, or reduce number of `strict: true` tools

**"Unsupported schema feature: [feature]"**
- **Cause:** Using feature not supported by structured outputs
- **Solution:** Review limitations, remove feature, or use SDK transformation

**"additionalProperties must be false"**
- **Cause:** `additionalProperties` not set to `false`
- **Solution:** Add `"additionalProperties": false` to all objects

---

## Best Practices

### 1. Design for Constraints

Since numerical/string constraints aren't supported natively, design schemas to minimize validation needs:

```python
# ✅ Good: Use enums for bounded ranges
priority: int = Field(enum=[1, 2, 3, 4, 5])

# ❌ Requires SDK transformation
priority: int = Field(ge=1, le=5)
```

### 2. Use SDK Helpers

Let SDKs handle transformation automatically:

```python
# Python
from anthropic import Anthropic

response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    output_format=MyPydanticModel,  # SDK transforms automatically
)
```

### 3. Test Schema Complexity

Before production, test that your schema compiles:

```python
try:
    response = client.beta.messages.create(
        model="claude-sonnet-4-5",
        betas=["structured-outputs-2025-11-13"],
        messages=[{"role": "user", "content": "test"}],
        output_format={"type": "json_schema", "schema": my_schema}
    )
except anthropic.BadRequestError as e:
    print(f"Schema too complex: {e}")
```

### 4. Avoid Deep Nesting

Deeply nested schemas increase complexity:

```python
# ✅ Good: Moderate nesting (2-3 levels)
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address

# ⚠️ Risky: Deep nesting (4+ levels)
class A(BaseModel):
    b: 'B'

class B(BaseModel):
    c: 'C'

class C(BaseModel):
    d: 'D'
```

---

## Quick Reference

| Feature | Supported | Notes |
|---------|-----------|-------|
| Basic types | ✅ | object, array, string, integer, number, boolean, null |
| enum | ✅ | Primitives only (no objects/arrays) |
| const | ✅ | Fully supported |
| anyOf | ✅ | Fully supported |
| allOf | ⚠️ | Simple cases only, no $ref |
| $ref (local) | ✅ | #/definitions/... only |
| $ref (external) | ❌ | http://... not supported |
| required | ✅ | Fully supported |
| additionalProperties: false | ✅ | **Required** |
| additionalProperties: true | ❌ | Not supported |
| String formats | ✅ | date-time, date, time, email, uri, uuid, ipv4, ipv6 |
| pattern (simple) | ✅ | Basic regex only |
| pattern (complex) | ❌ | Backreferences, lookahead not supported |
| minimum/maximum | ❌ | Use SDK transformation |
| minLength/maxLength | ❌ | Use SDK transformation |
| minItems (0 or 1) | ✅ | Supported |
| minItems (>1) | ❌ | Not supported |
| maxItems | ❌ | Not supported |
| uniqueItems | ❌ | Not supported |
| Recursive schemas | ❌ | Not supported |
| default | ✅ | All types |

---

**Official Documentation:** https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
