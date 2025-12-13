# MCP Server Troubleshooting

## Error Handling Patterns

### Validation Errors

```typescript
if (!isValid(input)) {
  throw new Error("Invalid input: expected format X, got Y");
}
```

### API Errors

```typescript
try {
  const result = await externalAPI.call();
  return result;
} catch (error) {
  console.error("API error:", error);
  return {
    content: [{
      type: "text",
      text: `Error: ${error.message}. Please try again.`
    }]
  };
}
```

### Resource Not Found

```typescript
if (!resource) {
  throw new Error(`Resource not found: ${uri}`);
}
```

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Server not detected | Invalid path | Use absolute path, verify file exists |
| Tools don't appear | Build not run | Run `npm run build` |
| "Server error" | stdout logging | Remove console.log, use console.error |
| Connection timeout | Server crash | Check mcp-server-NAME.log for errors |
| Invalid config | JSON syntax | Validate JSON, check quotes/commas |

---

## Quick Reference Commands

### Check Claude Desktop Logs

```bash
tail -f ~/Library/Logs/Claude/mcp.log
tail -f ~/Library/Logs/Claude/mcp-server-[name].log
```

### Validate Config JSON

```bash
python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector [command] [args]
```

### Restart Claude Desktop

```bash
# macOS
osascript -e 'quit app "Claude"'
open -a Claude
```

---

## Transport-Specific Issues

### STDIO Transport

**Problem**: Server crashes with no error
**Cause**: Using console.log() which corrupts JSON-RPC
**Solution**: Use console.error() only

**Problem**: Server not responding
**Cause**: Blocking synchronous operation
**Solution**: Use async/await for all I/O

### HTTP Transport

**Problem**: Connection refused
**Cause**: Wrong port or server not running
**Solution**: Check PORT env var, verify server started

**Problem**: Authentication errors
**Cause**: Missing or invalid credentials
**Solution**: Configure auth headers/tokens
