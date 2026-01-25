# Common Use Cases

## Use Case 1: Data Extraction

**Scenario**: Extract invoice data from text/images

```python
from pydantic import BaseModel
from typing import List

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str
    date: str
    customer_name: str
    line_items: List[LineItem]
    subtotal: float
    tax: float
    total_amount: float

response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    max_tokens=2048,
    messages=[{"role": "user", "content": f"Extract invoice:\n{invoice_text}"}],
    output_format=Invoice,
)

invoice = response.parsed_output
# Insert into database with guaranteed types
db.insert_invoice(invoice.model_dump())
```

## Use Case 2: Classification

**Scenario**: Classify support tickets

```python
class TicketClassification(BaseModel):
    category: str  # "billing", "technical", "sales"
    priority: str  # "low", "medium", "high", "critical"
    confidence: float
    requires_human: bool
    suggested_assignee: Optional[str] = None
    tags: List[str]

response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": f"Classify:\n{ticket}"}],
    output_format=TicketClassification,
)

classification = response.parsed_output
if classification.requires_human or classification.confidence < 0.7:
    route_to_human(ticket)
else:
    auto_assign(ticket, classification.category)
```

## Use Case 3: API Response Formatting

**Scenario**: Generate API-ready responses

```python
class APIResponse(BaseModel):
    status: str  # "success" or "error"
    data: dict
    errors: Optional[List[dict]] = None
    metadata: dict

response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": f"Process: {request}"}],
    output_format=APIResponse,
)

# Directly return as JSON API response
return jsonify(response.parsed_output.model_dump())
```
