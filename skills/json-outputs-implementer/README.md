# JSON Outputs Implementer

Specialized skill for implementing JSON outputs mode with guaranteed schema compliance.

## Purpose

This skill handles **end-to-end implementation** of JSON outputs mode (`output_format`), ensuring Claude's responses strictly match your JSON schema. Covers schema design, SDK integration, testing, and production deployment.

## Use Cases

- **Data Extraction**: Pull structured info from text/images
- **Classification**: Categorize content with guaranteed output format
- **API Formatting**: Generate API-ready JSON responses
- **Report Generation**: Create structured reports
- **Database Operations**: Ensure type-safe inserts/updates

## Prerequisites

- Routed here by `structured-outputs-advisor`
- Model: Claude Sonnet 4.5 or Opus 4.1
- Beta header: `structured-outputs-2025-11-13`

## Quick Start

**Python with Pydantic:**
```python
from pydantic import BaseModel
from anthropic import Anthropic

class Contact(BaseModel):
    name: str
    email: str

client = Anthropic()
response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": "Extract contact..."}],
    output_format=Contact,
)

contact = response.parsed_output  # Guaranteed valid
```

**TypeScript with Zod:**
```typescript
import { z } from 'zod';

const ContactSchema = z.object({
  name: z.string(),
  email: z.string().email(),
});

const response = await client.beta.messages.parse({
  model: "claude-sonnet-4-5",
  betas: ["structured-outputs-2025-11-13"],
  output_format: betaZodOutputFormat(ContactSchema),
  messages: [...]
});
```

## What You'll Learn

1. **Schema Design** - Respecting JSON Schema limitations
2. **SDK Integration** - Pydantic/Zod helpers
3. **Error Handling** - Refusals, token limits, validation
4. **Production Optimization** - Caching, monitoring, cost tracking
5. **Testing** - Comprehensive validation strategies

## Examples

- [contact-extraction.py](./examples/contact-extraction.py) - Extract contact info
- [invoice-extraction.py](./examples/invoice-extraction.py) - Complex nested schemas

## Related Skills

- [`structured-outputs-advisor`](../structured-outputs-advisor/) - Choose the right mode
- [`strict-tool-implementer`](../strict-tool-implementer/) - For tool validation

## Reference Materials

- [JSON Schema Limitations](../structured-outputs-advisor/reference/json-schema-limitations.md)
- [Best Practices](../structured-outputs-advisor/reference/best-practices.md)
- [API Compatibility](../structured-outputs-advisor/reference/api-compatibility.md)

## Version

Current version: 0.1.0

See [CHANGELOG.md](./CHANGELOG.md) for version history.
