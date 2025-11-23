# Phase 1: Schema Design

**Objective**: Create a production-ready JSON schema respecting all limitations

## Steps

### 1. Define Output Structure

Ask the user:
- "What fields do you need in the output?"
- "Which fields are required vs. optional?"
- "What are the data types for each field?"
- "Are there nested objects or arrays?"

### 2. Choose Schema Approach

**Option A: Pydantic (Python) - Recommended**
```python
from pydantic import BaseModel
from typing import List, Optional

class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: Optional[str] = None
    demo_requested: bool = False
    tags: List[str] = []
```

**Option B: Zod (TypeScript) - Recommended**
```typescript
import { z } from 'zod';

const ContactInfoSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  plan_interest: z.string().optional(),
  demo_requested: z.boolean().default(false),
  tags: z.array(z.string()).default([]),
});
```

**Option C: Raw JSON Schema**
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string", "description": "Full name"},
    "email": {"type": "string", "description": "Email address"},
    "plan_interest": {"type": "string", "description": "Interested plan"},
    "demo_requested": {"type": "boolean"},
    "tags": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["name", "email", "demo_requested"],
  "additionalProperties": false
}
```

### 3. Apply JSON Schema Limitations

**✅ Supported Features:**
- All basic types: object, array, string, integer, number, boolean, null
- `enum` (strings, numbers, bools, nulls only)
- `const`
- `anyOf` and `allOf` (limited)
- `$ref`, `$def`, `definitions` (local only)
- `required` and `additionalProperties: false`
- String formats: date-time, time, date, email, uri, uuid, ipv4, ipv6
- Array `minItems` (0 or 1 only)

**❌ NOT Supported (SDK can transform these):**
- Recursive schemas
- Numerical constraints (minimum, maximum)
- String constraints (minLength, maxLength)
- Complex array constraints
- External `$ref`

### 4. Add AI-Friendly Descriptions

```python
class Invoice(BaseModel):
    invoice_number: str  # Field(description="Invoice ID, format: INV-XXXXX")
    date: str  # Field(description="Invoice date in YYYY-MM-DD format")
    total: float  # Field(description="Total amount in USD")
    items: List[LineItem]  # Field(description="Line items on the invoice")
```

Good descriptions help Claude understand what to extract.

## Output

Production-ready schema following Anthropic's limitations.
