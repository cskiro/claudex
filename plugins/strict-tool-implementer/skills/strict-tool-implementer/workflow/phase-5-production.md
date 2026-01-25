# Phase 5: Production Agent Patterns

**Objective**: Production-ready agent architectures

## Pattern 1: Stateful Agent with Memory

```python
class StatefulTravelAgent:
    """Agent that maintains state across interactions."""

    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.booking_state: Dict[str, Any] = {}

    def chat(self, user_message: str) -> str:
        """Process user message and return response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = client.beta.messages.create(
            model="claude-sonnet-4-5",
            betas=["structured-outputs-2025-11-13"],
            max_tokens=2048,
            messages=self.conversation_history,
            tools=TOOLS,
        )

        # Process tools and update state
        final_response = self._process_response(response)

        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })

        return final_response

    def _process_response(self, response) -> str:
        """Process tool calls and maintain state."""
        # Implementation...
        pass

# Usage
agent = StatefulTravelAgent()
print(agent.chat("I want to go to Paris"))
print(agent.chat("For 2 people"))  # Remembers context
print(agent.chat("May 15 to May 22"))  # Continues booking
```

## Pattern 2: Tool Retry Logic

```python
def execute_tool_with_retry(
    tool_name: str,
    tool_input: Dict,
    max_retries: int = 3
) -> Dict:
    """Execute tool with exponential backoff retry."""
    import time

    for attempt in range(max_retries):
        try:
            tool_func = TOOL_FUNCTIONS[tool_name]
            result = tool_func(**tool_input)
            return {"success": True, "data": result}

        except Exception as e:
            if attempt == max_retries - 1:
                return {"success": False, "error": str(e)}

            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Tool {tool_name} failed, retrying in {wait_time}s")
            time.sleep(wait_time)
```

## Pattern 3: Tool Result Validation

```python
def validate_tool_result(tool_name: str, result: Any) -> bool:
    """Validate tool execution result."""
    validators = {
        "search_flights": lambda r: "flights" in r and len(r["flights"]) > 0,
        "book_flight": lambda r: "confirmation" in r,
        "search_hotels": lambda r: "hotels" in r,
    }

    validator = validators.get(tool_name)
    if validator:
        return validator(result)

    return True  # No validator = assume valid
```

## Output

Production-ready agent patterns with state management, retry logic, and validation.
