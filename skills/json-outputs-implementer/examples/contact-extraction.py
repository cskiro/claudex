"""
Contact Information Extraction Example

Extracts structured contact information from unstructured text (emails, messages, etc.)
using JSON outputs mode with Pydantic schema validation.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from anthropic import Anthropic
import os

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# Define schema with Pydantic
class ContactInfo(BaseModel):
    """Structured contact information extracted from text."""

    name: str = Field(description="Full name of the contact person")
    email: EmailStr = Field(description="Email address")
    phone: Optional[str] = Field(
        None, description="Phone number in any format"
    )
    company: Optional[str] = Field(
        None, description="Company or organization name"
    )
    plan_interest: Optional[str] = Field(
        None, description="Product plan or tier they're interested in"
    )
    demo_requested: bool = Field(
        False, description="Whether they requested a product demo"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Relevant tags or categories"
    )


def extract_contact(text: str) -> Optional[ContactInfo]:
    """
    Extract contact information from unstructured text.

    Args:
        text: Unstructured text containing contact information

    Returns:
        ContactInfo object with extracted data, or None if request refused
    """
    try:
        response = client.beta.messages.parse(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            betas=["structured-outputs-2025-11-13"],
            messages=[{
                "role": "user",
                "content": f"Extract contact information from the following text:\n\n{text}"
            }],
            output_format=ContactInfo,
        )

        # Handle different stop reasons
        if response.stop_reason == "refusal":
            print(f"⚠️  Request refused for safety reasons")
            return None

        if response.stop_reason == "max_tokens":
            print(f"⚠️  Response truncated - increase max_tokens")
            return None

        # Return validated contact info
        return response.parsed_output

    except Exception as e:
        print(f"❌ Error extracting contact: {e}")
        raise


def main():
    """Run contact extraction examples."""

    examples = [
        # Example 1: Complete contact info
        """
        Hi, I'm John Smith from Acme Corp. You can reach me at john.smith@acme.com
        or call me at (555) 123-4567. I'm interested in your Enterprise plan and
        would love to schedule a demo next week.
        """,

        # Example 2: Minimal info
        """
        Contact: jane.doe@example.com
        """,

        # Example 3: Informal message
        """
        Hey! Bob here. Email me at bob@startup.io if you want to chat about
        the Pro plan. Thanks!
        """,

        # Example 4: Multiple contacts (extracts first/primary)
        """
        From: alice@company.com
        CC: support@company.com

        Hi, I'm Alice Johnson, VP of Engineering at TechCo.
        We're evaluating your platform for our team of 50 developers.
        """,
    ]

    print("=" * 70)
    print("Contact Extraction Examples")
    print("=" * 70)

    for i, text in enumerate(examples, 1):
        print(f"\n📧 Example {i}:")
        print(f"Input: {text.strip()[:100]}...")

        contact = extract_contact(text)

        if contact:
            print(f"\n✅ Extracted Contact:")
            print(f"   Name: {contact.name}")
            print(f"   Email: {contact.email}")
            print(f"   Phone: {contact.phone or 'N/A'}")
            print(f"   Company: {contact.company or 'N/A'}")
            print(f"   Plan Interest: {contact.plan_interest or 'N/A'}")
            print(f"   Demo Requested: {contact.demo_requested}")
            print(f"   Tags: {', '.join(contact.tags) if contact.tags else 'None'}")
        else:
            print(f"\n❌ No contact extracted")

        print("-" * 70)


if __name__ == "__main__":
    main()
