# Phase 3: Server Implementation

**Purpose**: Generate core server code with requested capabilities

## TypeScript Server Template

```typescript
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Initialize server
const server = new Server(
  {
    name: "server-name",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// Example Tool
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "tool_name",
      description: "What this tool does",
      inputSchema: {
        type: "object",
        properties: {
          param: { type: "string", description: "Parameter description" }
        },
        required: ["param"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "tool_name") {
    const { param } = request.params.arguments;
    const result = await performOperation(param);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2)
        }
      ]
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server with STDIO transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // CRITICAL: Never console.log() in STDIO mode!
  console.error("Server running on stdio");
}

main().catch(console.error);
```

## Python Server Template (FastMCP)

```python
#!/usr/bin/env python3

from mcp.server.fastmcp import FastMCP
import os

# Initialize server
mcp = FastMCP("server-name")

@mcp.tool()
async def tool_name(param: str) -> str:
    """
    Description of what this tool does.

    Args:
        param: Parameter description

    Returns:
        Result description
    """
    result = await perform_operation(param)
    return str(result)

@mcp.resource("resource://template/{id}")
async def get_resource(id: str) -> str:
    """Get resource by ID."""
    return f"Resource content for {id}"

if __name__ == "__main__":
    mcp.run()
```

## Key Implementation Patterns

### 1. Tool Definition
- Clear, descriptive names
- Comprehensive descriptions (AI uses this!)
- Strong typing with Zod/type hints
- Proper error handling

### 2. Resource Patterns
- URI templates for dynamic resources
- Efficient data fetching (avoid heavy computation)
- Proper MIME types

### 3. Logging Rules
- **STDIO servers**: NEVER use console.log/print (corrupts JSON-RPC)
- Use console.error / logging.error (stderr is safe)
- **HTTP servers**: stdout is safe

## Output

Fully implemented server with requested capabilities

## Transition

Proceed to Phase 4 (Environment & Security)
