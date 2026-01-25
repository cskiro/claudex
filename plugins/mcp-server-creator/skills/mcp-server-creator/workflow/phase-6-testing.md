# Phase 6: Testing & Validation

**Purpose**: Verify server works correctly before deployment

## Testing Workflow

### 1. Build Check (TypeScript)

```bash
npm run build
# Should complete without errors
# Verify build/index.js exists
```

### 2. MCP Inspector Testing

```bash
# Install MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js

# Or for Python
npx @modelcontextprotocol/inspector uv run main.py
```

- Opens browser interface to test tools/resources
- Validates schemas and responses
- Great for debugging before Claude integration

### 3. Claude Desktop Integration Test

- Add to claude_desktop_config.json
- Completely restart Claude Desktop
- Check logs: `~/Library/Logs/Claude/mcp*.log`
- Look for server in "🔌" (attachments) menu

### 4. Functional Testing in Claude

Test with natural language queries:
- "Use [server-name] to [perform action]"
- "Can you [tool description]?"
- Verify tool appears in suggestions
- Check response accuracy

## Debugging Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Server not detected | Invalid path | Use absolute path, verify file exists |
| Tools don't appear | Build not run | Run `npm run build` |
| "Server error" | stdout logging | Remove console.log, use console.error |
| Connection timeout | Server crash | Check mcp-server-NAME.log for errors |
| Invalid config | JSON syntax | Validate JSON, check quotes/commas |

## Output

Validated, working MCP server with test results

## Transition

Proceed to Phase 7 (Documentation & Handoff)
