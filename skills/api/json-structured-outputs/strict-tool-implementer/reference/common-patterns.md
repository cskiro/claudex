# Common Agentic Patterns

## Pattern 1: Sequential Workflow

Tools execute in sequence (search → book → confirm):

```python
# User: "Book a flight to Paris"
# Agent executes:
1. search_flights(origin="SF", destination="Paris", ...)
2. book_flight(flight_id="F1", passengers=[...])
3. send_confirmation(confirmation_id="ABC123")
```

## Pattern 2: Parallel Tool Execution

Multiple independent tools (flights + hotels):

```python
# User: "Find flights and hotels for Paris trip"
# Agent can call in parallel (if your implementation supports it):
1. search_flights(destination="Paris", ...)
2. search_hotels(city="Paris", ...)
```

## Pattern 3: Conditional Branching

Tool selection based on context:

```python
# User: "Plan my trip"
# Agent decides which tools to call based on conversation:
if budget_conscious:
    search_flights(class="economy")
else:
    search_flights(class="business")
```

## Important Reminders

1. **Always set `strict: true`** - This enables validation
2. **Require `additionalProperties: false`** - Enforced by strict mode
3. **Use enums for constrained values** - Better than free text
4. **Clear descriptions matter** - Claude uses these to decide when to call tools
5. **Tool inputs are guaranteed valid** - No validation needed in tool functions
6. **Handle tool execution failures** - External APIs can fail
7. **Test multi-step workflows** - Edge cases appear in tool composition
8. **Monitor agent behavior** - Track tool usage patterns and failures
