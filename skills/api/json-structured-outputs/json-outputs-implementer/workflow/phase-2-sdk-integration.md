# Phase 2: SDK Integration

**Objective**: Implement using SDK helpers for automatic validation

## Python Implementation

**Recommended: Use `client.beta.messages.parse()`**

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from anthropic import Anthropic

class ContactInfo(BaseModel):
    name: str = Field(description="Full name of the contact")
    email: str = Field(description="Email address")
    plan_interest: Optional[str] = Field(
        None, description="Plan tier they're interested in"
    )
    demo_requested: bool = Field(
        False, description="Whether they requested a demo"
    )

client = Anthropic()

def extract_contact(text: str) -> ContactInfo:
    """Extract contact information from text."""
    response = client.beta.messages.parse(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        betas=["structured-outputs-2025-11-13"],
        messages=[{
            "role": "user",
            "content": f"Extract contact information from: {text}"
        }],
        output_format=ContactInfo,
    )

    # Handle edge cases
    if response.stop_reason == "refusal":
        raise ValueError("Claude refused the request")

    if response.stop_reason == "max_tokens":
        raise ValueError("Response truncated - increase max_tokens")

    # Automatically validated
    return response.parsed_output

# Usage
contact = extract_contact("John Smith (john@example.com) wants Enterprise plan")
print(contact.name, contact.email)  # Type-safe access
```

## TypeScript Implementation

```typescript
import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';
import { betaZodOutputFormat } from '@anthropic-ai/sdk/helpers/beta/zod';

const ContactInfoSchema = z.object({
  name: z.string().describe("Full name of the contact"),
  email: z.string().email().describe("Email address"),
  plan_interest: z.string().optional().describe("Plan tier interested in"),
  demo_requested: z.boolean().default(false).describe("Demo requested"),
});

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function extractContact(text: string) {
  const response = await client.beta.messages.parse({
    model: "claude-sonnet-4-5",
    max_tokens: 1024,
    betas: ["structured-outputs-2025-11-13"],
    messages: [{
      role: "user",
      content: `Extract contact information from: ${text}`
    }],
    output_format: betaZodOutputFormat(ContactInfoSchema),
  });

  if (response.stop_reason === "refusal") {
    throw new Error("Claude refused the request");
  }

  if (response.stop_reason === "max_tokens") {
    throw new Error("Response truncated - increase max_tokens");
  }

  return response.parsed_output;
}

// Usage
const contact = await extractContact("John Smith (john@example.com)...");
console.log(contact.name, contact.email);  // Fully typed
```

## Output

Working implementation with SDK validation.
