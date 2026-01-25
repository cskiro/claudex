# Example: Architecture Diagram

## Scenario

A user asks: "Show me how our e-commerce platform components are connected."

## Generated Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      E-COMMERCE PLATFORM ARCHITECTURE                    │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────────┐                           ┌───────────────────┐
│   Web Frontend    │                           │  Mobile Frontend  │
├───────────────────┤                           ├───────────────────┤
│ • React SPA       │                           │ • React Native    │
│ • Redux state     │                           │ • Offline sync    │
│ • Tailwind CSS    │                           │ • Push notifs     │
└───────────────────┘                           └───────────────────┘
          │                                               │
          └───────────────────┬───────────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   API Gateway     │
                    ├───────────────────┤
                    │ • Rate limiting   │
                    │ • Auth validation │
                    │ • Request routing │
                    └───────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Auth Service   │ │ Product Service │ │  Order Service  │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • JWT tokens    │ │ • Catalog CRUD  │ │ • Cart mgmt     │
│ • OAuth 2.0     │ │ • Search/filter │ │ • Checkout flow │
│ • Session mgmt  │ │ • Inventory     │ │ • Payment proc  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Users DB      │ │  Products DB    │ │   Orders DB     │
│   (PostgreSQL)  │ │  (PostgreSQL)   │ │   (PostgreSQL)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Explanation

This architecture diagram shows the three-tier structure of the e-commerce platform:

1. **Presentation Layer**: Web and mobile frontends
2. **API Layer**: Gateway with routing to microservices
3. **Data Layer**: Dedicated databases per service

The vertical flow clearly shows how requests travel from clients through the gateway to specific services and their databases.

## Usage Suggestions

- Include in architecture documentation
- Add to README for new developer onboarding
- Reference in technical design documents
