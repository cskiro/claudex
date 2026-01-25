# Phase 4: Testing

**Objective**: Validate schema works with representative data

## Test Coverage

```python
import pytest

@pytest.fixture
def extractor():
    return ContactExtractor()

def test_complete_contact(extractor):
    """Test with all fields present."""
    text = "John Smith (john@example.com) interested in Enterprise plan, wants demo"
    result = extractor.extract(text)

    assert result.name == "John Smith"
    assert result.email == "john@example.com"
    assert result.plan_interest == "Enterprise"
    assert result.demo_requested is True

def test_minimal_contact(extractor):
    """Test with only required fields."""
    text = "Contact: jane@example.com"
    result = extractor.extract(text)

    assert result.email == "jane@example.com"
    assert result.name is not None  # Claude should infer or extract
    assert result.plan_interest is None  # Optional field
    assert result.demo_requested is False  # Default

def test_invalid_input(extractor):
    """Test with insufficient data."""
    text = "This has no contact information"
    # Depending on requirements, might raise or return partial data
    result = extractor.extract(text)
    # Define expected behavior

def test_refusal_scenario(extractor):
    """Test that refusals are handled."""
    # Test with potentially unsafe content
    # Verify graceful handling without crash
    pass

def test_token_limit(extractor):
    """Test with very long input."""
    text = "..." * 10000  # Very long text
    # Verify either succeeds or raises appropriate error
    pass
```

## Output

Comprehensive test suite covering edge cases.
