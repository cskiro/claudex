# Mode 1: Search Conversations

**When to use**: Find specific past conversations

## Trigger Phrases
- "Find conversations about React performance optimization"
- "Search for times I fixed authentication bugs"
- "Show me conversations that modified Auth.tsx"
- "What conversations mention TypeScript strict mode?"

## Process

1. User asks to search for a topic or file
2. Skill performs RAG semantic search
3. Returns ranked results with context snippets
4. Optionally show full conversation details

## Search Types

### Semantic Search (by meaning)
```
User: "Find conversations about fixing bugs related to user authentication"

Skill: [Performs RAG search]
Found 3 conversations:
1. "Debug JWT token expiration" (Oct 24)
2. "Fix OAuth redirect loop" (Oct 20)
3. "Implement session timeout handling" (Oct 18)
```

### Metadata Search (by files/tools)
```
User: "Show conversations that modified src/auth/token.ts"

Skill: [Queries SQLite metadata]
Found 5 conversations touching src/auth/token.ts:
1. "Implement token refresh logic" (Oct 25)
2. "Add token validation" (Oct 22)
...
```

### Time-based Search
```
User: "What did I work on last week?"

Skill: [Queries by date range]
Last week (Oct 19-25) you had 12 conversations:
- 5 about authentication features
- 3 about bug fixes
- 2 about testing
- 2 about refactoring
```

## Output Format

```
Found 5 conversations about "React performance optimization":

1. [Similarity: 0.89] "Optimize UserProfile re-renders" (Oct 25, 2025)
   Files: src/components/UserProfile.tsx, src/hooks/useUser.ts
   Snippet: "...implemented useMemo to prevent unnecessary re-renders..."

2. [Similarity: 0.82] "Fix dashboard performance issues" (Oct 20, 2025)
   Files: src/pages/Dashboard.tsx
   Snippet: "...React.memo wrapper reduced render count by 60%..."

[View full conversations? Type the number]
```
