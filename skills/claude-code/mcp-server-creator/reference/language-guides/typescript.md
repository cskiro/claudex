# TypeScript MCP Server Best Practices

## Configuration

- ✓ Use strict mode in tsconfig.json
- ✓ Target ES2022 or later
- ✓ Use Node16 module resolution

## Implementation

- ✓ Leverage Zod for runtime validation
- ✓ Export types for reusability
- ✓ Use async/await consistently
- ✓ Handle errors with try/catch
- ✓ Build before testing!

## Critical Rules

### STDIO Transport
```typescript
// WRONG - corrupts JSON-RPC
console.log("Debug info");

// CORRECT - safe for STDIO
console.error("Debug info");
```

### Tool Schemas

```typescript
import { z } from "zod";

const ToolInputSchema = z.object({
  query: z.string().describe("Search query"),
  limit: z.number().optional().default(10).describe("Max results"),
});

// Validate in handler
const input = ToolInputSchema.parse(request.params.arguments);
```

### Error Handling

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const result = await performOperation(request.params);
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  } catch (error) {
    console.error("Tool error:", error);
    return {
      content: [{
        type: "text",
        text: `Error: ${error.message}`
      }],
      isError: true
    };
  }
});
```

## Build & Run

```bash
# Development
npm run watch

# Production
npm run build
node build/index.js
```
