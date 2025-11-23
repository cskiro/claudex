# Phase 7: Documentation & Handoff

**Purpose**: Provide user with complete documentation and next steps

## Generate README.md

```markdown
# MCP Server: [Name]

## Description
[What this server does and why it's useful]

## Capabilities

### Tools
- **tool_name**: Description of what it does
  - Parameters: param1 (type) - description
  - Returns: description

### Resources
- **resource://pattern/{id}**: Description

### Prompts
- **prompt_name**: Description

## Setup

### Prerequisites
- Node.js 18+ / Python 3.10+
- Claude Desktop or MCP-compatible client

### Installation

1. Clone/download this server
2. Install dependencies:
   ```bash
   npm install && npm run build
   # OR
   uv sync
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. Add to Claude Desktop config (see Phase 5)

5. Restart Claude Desktop completely

## Usage Examples

### Example 1: [Use Case]
Query: "[Natural language query]"
Expected: [What happens]

## Development

### Running Locally
```bash
npm run watch  # Auto-rebuild on changes
```

### Testing with MCP Inspector
```bash
npx @modelcontextprotocol/inspector node build/index.js
```

### Debugging
Logs location: `~/Library/Logs/Claude/mcp-server-[name].log`

## Security Notes
- Never commit .env file
- Rotate API keys regularly
- Validate all inputs
```

## Provide Next Steps

```markdown
## Next Steps

1. ✅ Server code generated at: [path]
2. ⬜ Review and customize tool implementations
3. ⬜ Add your API keys to .env
4. ⬜ Run build: `npm run build` or test with `uv run`
5. ⬜ Test with MCP Inspector
6. ⬜ Add to Claude Desktop config
7. ⬜ Restart Claude Desktop
8. ⬜ Test with natural language queries
9. ⬜ Iterate and enhance based on usage
```

## Output

Complete documentation and clear path to production use
