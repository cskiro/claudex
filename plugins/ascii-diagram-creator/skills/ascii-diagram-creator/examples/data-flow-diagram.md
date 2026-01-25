# Example: Data Flow Diagram

## Scenario

A user asks: "Illustrate how user authentication data flows through our system."

## Generated Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    USER AUTHENTICATION FLOW                              │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Browser    │
│  Login Form  │
└──────────────┘
       │
       │ 1. POST /auth/login
       │    { email, password }
       ▼
┌──────────────┐
│  API Gateway │
│  (Express)   │
└──────────────┘
       │
       │ 2. Route to auth service
       ▼
┌──────────────────────────────────────────────────────────────┐
│                      AUTH SERVICE                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  3. Validate credentials                                      │
│     ┌─────────────┐                                          │
│     │ Hash pwd    │──► Compare with stored hash              │
│     └─────────────┘                                          │
│            │                                                  │
│            ▼                                                  │
│  4. Query user database                                       │
│     ┌─────────────┐     ┌─────────────┐                      │
│     │ Users DB    │────►│ User record │                      │
│     │ (Postgres)  │     │ + roles     │                      │
│     └─────────────┘     └─────────────┘                      │
│            │                                                  │
│            ▼                                                  │
│  5. Generate tokens                                           │
│     ┌─────────────┐     ┌─────────────┐                      │
│     │ JWT Access  │     │ Refresh     │                      │
│     │ (15 min)    │     │ (7 days)    │                      │
│     └─────────────┘     └─────────────┘                      │
│            │                   │                              │
│            │                   ▼                              │
│            │            6. Store refresh token                │
│            │            ┌─────────────┐                       │
│            │            │   Redis     │                       │
│            │            │  Sessions   │                       │
│            │            └─────────────┘                       │
│            │                                                  │
└────────────┼──────────────────────────────────────────────────┘
             │
             │ 7. Return tokens
             ▼
┌──────────────┐
│  API Gateway │
└──────────────┘
       │
       │ 8. Set cookies & respond
       │    { accessToken, user }
       ▼
┌──────────────┐
│   Browser    │
│  Store JWT   │
└──────────────┘
       │
       │ 9. Subsequent requests
       │    Authorization: Bearer <token>
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  API Gateway │────►│  Middleware  │────►│  Protected   │
│              │     │  Verify JWT  │     │  Resources   │
└──────────────┘     └──────────────┘     └──────────────┘


TOKEN REFRESH FLOW:

Access Token Expired
       │
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser    │────►│ POST /auth/  │────►│    Redis     │
│  Refresh Req │     │   refresh    │     │  Validate    │
└──────────────┘     └──────────────┘     └──────────────┘
                            │                    │
                            │◄───────────────────┘
                            │  Valid? Issue new tokens
                            ▼
                     ┌──────────────┐
                     │  New Access  │
                     │   Token      │
                     └──────────────┘
```

## Explanation

This data flow diagram shows the complete authentication lifecycle:

1. **Initial login flow**: Steps 1-8 show credential validation and token generation
2. **Token storage**: Redis for refresh tokens, browser for access tokens
3. **Protected resource access**: JWT verification middleware
4. **Token refresh**: Separate flow for getting new access tokens

The nested structure within the Auth Service box shows internal processing details while maintaining flow clarity.

## Usage Suggestions

- Include in security documentation
- Add to API documentation for developers
- Reference during security audits
- Share with new team members during onboarding
