# Phase 4: Testing Agent Workflows

**Objective**: Validate agent behavior with realistic scenarios

## Test Strategy

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_tool_functions():
    """Mock external tool functions."""
    return {
        "search_flights": Mock(return_value={"flights": [{"id": "F1", "price": 500}]}),
        "book_flight": Mock(return_value={"confirmation": "ABC123"}),
        "search_hotels": Mock(return_value={"hotels": [{"id": "H1", "price": 150}]}),
    }

def test_simple_flight_search(mock_tool_functions):
    """Test agent handles simple flight search."""
    with patch.dict('agent.TOOL_FUNCTIONS', mock_tool_functions):
        result = run_agent("Find flights from SF to LA on May 15 for 2 people")

        # Verify search_flights was called
        mock_tool_functions["search_flights"].assert_called_once()
        call_args = mock_tool_functions["search_flights"].call_args[1]

        # Strict mode guarantees these match schema
        assert call_args["origin"] == "San Francisco, CA"  # or similar
        assert call_args["destination"] == "Los Angeles, CA"
        assert call_args["travelers"] == 2
        assert "2024-05-15" in call_args["departure_date"]

def test_multi_step_booking(mock_tool_functions):
    """Test agent completes multi-step booking."""
    with patch.dict('agent.TOOL_FUNCTIONS', mock_tool_functions):
        result = run_agent(
            "Book a round trip from SF to Paris for 2 people, "
            "May 15-22, and find a hotel"
        )

        # Verify correct tool sequence
        assert mock_tool_functions["search_flights"].called
        assert mock_tool_functions["book_flight"].called
        assert mock_tool_functions["search_hotels"].called

def test_tool_failure_handling(mock_tool_functions):
    """Test agent handles tool failures gracefully."""
    mock_tool_functions["search_flights"].side_effect = Exception("API down")

    with patch.dict('agent.TOOL_FUNCTIONS', mock_tool_functions):
        result = run_agent("Find flights to Paris")

        # Should handle error gracefully
        assert "error" in result or "failed" in str(result).lower()

def test_parameter_validation():
    """Test that strict mode guarantees valid parameters."""
    # With strict mode, parameters are guaranteed to match schema
    # This test verifies the guarantee holds

    response = client.beta.messages.create(
        model="claude-sonnet-4-5",
        betas=["structured-outputs-2025-11-13"],
        messages=[{"role": "user", "content": "Search flights for 2 people"}],
        tools=TOOLS,
    )

    for block in response.content:
        if block.type == "tool_use":
            # These assertions should NEVER fail with strict mode
            assert isinstance(block.input, dict)
            assert "travelers" in block.input
            assert isinstance(block.input["travelers"], int)
            assert block.input["travelers"] in [1, 2, 3, 4, 5, 6]
```

## Output

Comprehensive test coverage for agent workflows.
