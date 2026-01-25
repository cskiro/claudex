"""
Invoice Data Extraction Example

Extracts structured invoice data from text using JSON outputs with nested schemas.
Demonstrates handling complex nested structures (line items, tax breakdown).
"""

from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# Nested schema for line items
class LineItem(BaseModel):
    """Individual line item on an invoice."""
    description: str = Field(description="Item description")
    quantity: int = Field(description="Quantity ordered")
    unit_price: float = Field(description="Price per unit in USD")
    total: float = Field(description="Total for this line (quantity * unit_price)")


class Invoice(BaseModel):
    """Complete invoice structure."""
    invoice_number: str = Field(description="Invoice ID (format: INV-XXXXX)")
    date: str = Field(description="Invoice date in YYYY-MM-DD format")
    due_date: str = Field(description="Payment due date in YYYY-MM-DD format")
    customer_name: str = Field(description="Customer or company name")
    customer_email: str = Field(description="Customer email address")

    line_items: List[LineItem] = Field(
        description="List of items on the invoice"
    )

    subtotal: float = Field(description="Subtotal before tax in USD")
    tax_rate: float = Field(description="Tax rate as decimal (e.g., 0.08 for 8%)")
    tax_amount: float = Field(description="Tax amount in USD")
    total_amount: float = Field(description="Final total amount in USD")

    notes: str = Field(
        default="",
        description="Additional notes or payment instructions"
    )


def extract_invoice(invoice_text: str) -> Optional[Invoice]:
    """Extract structured invoice data."""
    try:
        response = client.beta.messages.parse(
            model="claude-sonnet-4-5",
            max_tokens=2048,  # Higher for complex nested structures
            betas=["structured-outputs-2025-11-13"],
            messages=[{
                "role": "user",
                "content": f"Extract all invoice data from:\n\n{invoice_text}"
            }],
            output_format=Invoice,
        )

        if response.stop_reason != "end_turn":
            print(f"⚠️  Unexpected stop reason: {response.stop_reason}")
            return None

        return response.parsed_output

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def main():
    """Run invoice extraction example."""

    invoice_text = """
    INVOICE

    Invoice Number: INV-2024-00123
    Date: 2024-01-15
    Due Date: 2024-02-15

    Bill To:
    Acme Corporation
    John Smith, CFO
    john.smith@acme.com

    ITEMS:
    1. Cloud Hosting - Pro Plan (x3 servers)
       Quantity: 3
       Unit Price: $299.00
       Total: $897.00

    2. Database Storage - 500GB
       Quantity: 500
       Unit Price: $0.50
       Total: $250.00

    3. API Calls - Premium Tier
       Quantity: 1,000,000
       Unit Price: $0.001
       Total: $1,000.00

    4. Support - Enterprise Level
       Quantity: 1
       Unit Price: $500.00
       Total: $500.00

    Subtotal: $2,647.00
    Tax (8.5%): $224.99
    TOTAL: $2,871.99

    Payment Terms: Net 30
    Please remit payment to accounts@cloudprovider.com
    """

    print("=" * 70)
    print("Invoice Extraction Example")
    print("=" * 70)

    invoice = extract_invoice(invoice_text)

    if invoice:
        print(f"\n✅ Invoice Extracted Successfully\n")
        print(f"Invoice #: {invoice.invoice_number}")
        print(f"Customer: {invoice.customer_name} ({invoice.customer_email})")
        print(f"Date: {invoice.date}")
        print(f"Due: {invoice.due_date}")
        print(f"\nLine Items:")

        for i, item in enumerate(invoice.line_items, 1):
            print(f"  {i}. {item.description}")
            print(f"     Qty: {item.quantity} × ${item.unit_price:.2f} = ${item.total:.2f}")

        print(f"\nSubtotal: ${invoice.subtotal:.2f}")
        print(f"Tax ({invoice.tax_rate * 100:.1f}%): ${invoice.tax_amount:.2f}")
        print(f"TOTAL: ${invoice.total_amount:.2f}")

        if invoice.notes:
            print(f"\nNotes: {invoice.notes}")

        # Validation checks
        print(f"\n🔍 Validation:")
        calculated_subtotal = sum(item.total for item in invoice.line_items)
        print(f"   Subtotal matches: {abs(calculated_subtotal - invoice.subtotal) < 0.01}")

        calculated_tax = invoice.subtotal * invoice.tax_rate
        print(f"   Tax calculation matches: {abs(calculated_tax - invoice.tax_amount) < 0.01}")

        calculated_total = invoice.subtotal + invoice.tax_amount
        print(f"   Total matches: {abs(calculated_total - invoice.total_amount) < 0.01}")

    else:
        print("❌ Failed to extract invoice")


if __name__ == "__main__":
    from typing import Optional
    main()
