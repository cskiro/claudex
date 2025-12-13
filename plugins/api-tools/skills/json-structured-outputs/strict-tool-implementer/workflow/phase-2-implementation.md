# Phase 2: Multi-Tool Agent Implementation

**Objective**: Implement agent with multiple validated tools

## Python Implementation

```python
from anthropic import Anthropic
from typing import Dict, Any, List

client = Anthropic()

# Define tools
TOOLS = [
    {
        "name": "search_flights",
        "description": "Search for available flights",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Departure city"},
                "destination": {"type": "string", "description": "Arrival city"},
                "departure_date": {"type": "string", "format": "date"},
                "travelers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6]}
            },
            "required": ["origin", "destination", "departure_date", "travelers"],
            "additionalProperties": False
        }
    },
    {
        "name": "book_flight",
        "description": "Book a selected flight",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "flight_id": {"type": "string", "description": "Flight identifier"},
                "passengers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "passport": {"type": "string"}
                        },
                        "required": ["name", "passport"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["flight_id", "passengers"],
            "additionalProperties": False
        }
    },
    {
        "name": "search_hotels",
        "description": "Search for hotels in a city",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
                "check_in": {"type": "string", "format": "date"},
                "check_out": {"type": "string", "format": "date"},
                "guests": {"type": "integer", "enum": [1, 2, 3, 4]}
            },
            "required": ["city", "check_in", "check_out", "guests"],
            "additionalProperties": False
        }
    }
]

# Tool execution functions
def search_flights(origin: str, destination: str, departure_date: str, travelers: int) -> Dict:
    """Execute flight search - calls actual API."""
    # Implementation here
    return {"flights": [...]}

def book_flight(flight_id: str, passengers: List[Dict]) -> Dict:
    """Book the flight - calls actual API."""
    # Implementation here
    return {"confirmation": "ABC123", "status": "confirmed"}

def search_hotels(city: str, check_in: str, check_out: str, guests: int) -> Dict:
    """Search hotels - calls actual API."""
    # Implementation here
    return {"hotels": [...]}

# Tool registry
TOOL_FUNCTIONS = {
    "search_flights": search_flights,
    "book_flight": book_flight,
    "search_hotels": search_hotels,
}

# Agent loop
def run_agent(user_request: str, max_turns: int = 10):
    """Run agent with tool validation."""
    messages = [{"role": "user", "content": user_request}]

    for turn in range(max_turns):
        response = client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            betas=["structured-outputs-2025-11-13"],
            messages=messages,
            tools=TOOLS,
        )

        # Process response
        if response.stop_reason == "end_turn":
            # Agent finished
            return extract_final_answer(response)

        if response.stop_reason == "tool_use":
            # Execute tools
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    # Tool input is GUARANTEED to match schema
                    tool_name = block.name
                    tool_input = block.input  # Already validated!

                    # Execute tool
                    tool_function = TOOL_FUNCTIONS[tool_name]
                    result = tool_function(**tool_input)  # Type-safe!

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            # Add assistant response and tool results to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        else:
            raise Exception(f"Unexpected stop reason: {response.stop_reason}")

    raise Exception("Max turns reached")

# Usage
result = run_agent("Book a flight from SF to Paris for 2 people, departing May 15")
print(result)
```

## TypeScript Implementation

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const TOOLS: Anthropic.Tool[] = [
  {
    name: "search_flights",
    description: "Search for available flights",
    strict: true,
    input_schema: {
      type: "object",
      properties: {
        origin: { type: "string", description: "Departure city" },
        destination: { type: "string", description: "Arrival city" },
        departure_date: { type: "string", format: "date" },
        travelers: { type: "integer", enum: [1, 2, 3, 4, 5, 6] }
      },
      required: ["origin", "destination", "departure_date", "travelers"],
      additionalProperties: false
    }
  },
  // ... other tools
];

async function runAgent(userRequest: string, maxTurns: number = 10) {
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: userRequest }
  ];

  for (let turn = 0; turn < maxTurns; turn++) {
    const response = await client.beta.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 2048,
      betas: ["structured-outputs-2025-11-13"],
      messages,
      tools: TOOLS,
    });

    if (response.stop_reason === "end_turn") {
      return extractFinalAnswer(response);
    }

    if (response.stop_reason === "tool_use") {
      const toolResults: Anthropic.ToolResultBlockParam[] = [];

      for (const block of response.content) {
        if (block.type === "tool_use") {
          // Input guaranteed to match schema!
          const result = await executeTool(block.name, block.input);

          toolResults.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: JSON.stringify(result)
          });
        }
      }

      messages.push({ role: "assistant", content: response.content });
      messages.push({ role: "user", content: toolResults });
    }
  }

  throw new Error("Max turns reached");
}
```

## Output

Working multi-tool agent with validated tool schemas.
