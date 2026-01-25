"""
Travel Booking Agent Example

Multi-tool agent using strict tool use mode for guaranteed parameter validation.
Demonstrates validated tool inputs in agentic workflows.
"""

from anthropic import Anthropic
from typing import Dict, Any, List
import json
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# Define tools with strict mode
TOOLS = [
    {
        "name": "search_flights",
        "description": "Search for available flights between two cities",
        "strict": True,  # Enable strict parameter validation
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Departure city (e.g., 'San Francisco, CA')"
                },
                "destination": {
                    "type": "string",
                    "description": "Arrival city (e.g., 'Paris, France')"
                },
                "departure_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Departure date in YYYY-MM-DD format"
                },
                "return_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Return date in YYYY-MM-DD format (optional for one-way)"
                },
                "travelers": {
                    "type": "integer",
                    "enum": [1, 2, 3, 4, 5, 6],
                    "description": "Number of travelers"
                }
            },
            "required": ["origin", "destination", "departure_date", "travelers"],
            "additionalProperties": False  # Required for strict mode
        }
    },
    {
        "name": "book_flight",
        "description": "Book a selected flight",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "flight_id": {
                    "type": "string",
                    "description": "Flight identifier from search results"
                },
                "passenger_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Full names of all passengers"
                },
                "contact_email": {
                    "type": "string",
                    "format": "email",
                    "description": "Contact email for booking confirmation"
                }
            },
            "required": ["flight_id", "passenger_names", "contact_email"],
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
                "city": {
                    "type": "string",
                    "description": "City name"
                },
                "check_in": {
                    "type": "string",
                    "format": "date",
                    "description": "Check-in date in YYYY-MM-DD format"
                },
                "check_out": {
                    "type": "string",
                    "format": "date",
                    "description": "Check-out date in YYYY-MM-DD format"
                },
                "guests": {
                    "type": "integer",
                    "enum": [1, 2, 3, 4],
                    "description": "Number of guests"
                }
            },
            "required": ["city", "check_in", "check_out", "guests"],
            "additionalProperties": False
        }
    }
]


# Mock tool implementations
def search_flights(origin: str, destination: str, departure_date: str,
                   travelers: int, return_date: str = None) -> Dict:
    """Mock flight search - would call real API."""
    print(f"🔍 Searching flights: {origin} → {destination}")
    print(f"   Departure: {departure_date}, Travelers: {travelers}")

    return {
        "flights": [
            {
                "id": "FL123",
                "airline": "Air France",
                "departure": f"{departure_date} 10:00",
                "arrival": f"{departure_date} 23:00",
                "price": 850.00,
                "class": "Economy"
            },
            {
                "id": "FL456",
                "airline": "United",
                "departure": f"{departure_date} 14:30",
                "arrival": f"{departure_date} 03:30+1",
                "price": 920.00,
                "class": "Economy"
            }
        ]
    }


def book_flight(flight_id: str, passenger_names: List[str],
                contact_email: str) -> Dict:
    """Mock flight booking - would call real API."""
    print(f"✈️  Booking flight {flight_id}")
    print(f"   Passengers: {', '.join(passenger_names)}")
    print(f"   Email: {contact_email}")

    return {
        "confirmation": "ABC123XYZ",
        "status": "confirmed",
        "total_price": 850.00 * len(passenger_names)
    }


def search_hotels(city: str, check_in: str, check_out: str, guests: int) -> Dict:
    """Mock hotel search - would call real API."""
    print(f"🏨 Searching hotels in {city}")
    print(f"   Check-in: {check_in}, Check-out: {check_out}, Guests: {guests}")

    return {
        "hotels": [
            {
                "id": "HTL789",
                "name": "Grand Hotel Paris",
                "rating": 4.5,
                "price_per_night": 200.00,
                "amenities": ["WiFi", "Breakfast", "Gym"]
            },
            {
                "id": "HTL101",
                "name": "Budget Inn",
                "rating": 3.5,
                "price_per_night": 80.00,
                "amenities": ["WiFi"]
            }
        ]
    }


# Tool registry
TOOL_FUNCTIONS = {
    "search_flights": search_flights,
    "book_flight": book_flight,
    "search_hotels": search_hotels,
}


def run_travel_agent(user_request: str, max_turns: int = 10):
    """
    Run travel booking agent with strict tool validation.

    With strict mode enabled, all tool inputs are GUARANTEED to match
    the schema - no validation needed in tool functions!
    """
    messages = [{"role": "user", "content": user_request}]

    print("=" * 70)
    print(f"User Request: {user_request}")
    print("=" * 70)

    for turn in range(max_turns):
        print(f"\n🤖 Agent Turn {turn + 1}")

        response = client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            betas=["structured-outputs-2025-11-13"],
            messages=messages,
            tools=TOOLS,
        )

        # Check stop reason
        if response.stop_reason == "end_turn":
            # Agent finished
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text

            print(f"\n✅ Agent Complete:")
            print(f"{final_text}")
            return final_text

        if response.stop_reason == "tool_use":
            # Execute tools
            tool_results = []

            for block in response.content:
                if block.type == "text":
                    print(f"\n💭 Agent: {block.text}")

                elif block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input  # GUARANTEED to match schema!

                    print(f"\n🔧 Tool Call: {tool_name}")
                    print(f"   Input: {json.dumps(tool_input, indent=2)}")

                    # Execute tool with validated inputs
                    tool_function = TOOL_FUNCTIONS[tool_name]
                    result = tool_function(**tool_input)  # Type-safe!

                    print(f"   Result: {json.dumps(result, indent=2)}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })

            # Add to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        else:
            print(f"⚠️  Unexpected stop reason: {response.stop_reason}")
            break

    print("\n⚠️  Max turns reached without completion")
    return None


def main():
    """Run travel agent examples."""

    examples = [
        "Book a round trip from San Francisco to Paris for 2 people, "
        "departing May 15, 2024 and returning May 22, 2024. "
        "Passengers are John Smith and Jane Doe. "
        "Email confirmation to john.smith@example.com. "
        "Also find a hotel in Paris for those dates.",

        "Find flights from New York to London for 1 traveler on June 1, 2024.",

        "Search for hotels in Tokyo for 2 guests, checking in July 10 "
        "and checking out July 15.",
    ]

    for i, request in enumerate(examples, 1):
        print(f"\n\n{'='*70}")
        print(f"EXAMPLE {i}")
        print(f"{'='*70}")

        run_travel_agent(request)


if __name__ == "__main__":
    main()
