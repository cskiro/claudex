# Phase 5: Claude Desktop Integration

**Purpose**: Configure server in Claude Desktop for immediate use

## Configuration Location

- **macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## TypeScript Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-server-name/build/index.js"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Python Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server-name",
        "run",
        "main.py"
      ],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Critical Requirements

- ✅ **Use ABSOLUTE paths** (not relative like `./` or `~/`)
- ✅ Run `npm run build` before testing (TypeScript)
- ✅ Completely restart Claude Desktop (Cmd+Q on macOS)
- ✅ Valid JSON syntax (check with `python -m json.tool`)

## Output

Complete Claude Desktop configuration with restart instructions

## Transition

Proceed to Phase 6 (Testing & Validation)
