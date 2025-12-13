# MCP Server Creator Skill

Automated tool for creating production-ready Model Context Protocol (MCP) servers with TypeScript or Python SDKs.

## What This Skill Does

The MCP Server Creator skill streamlines the entire process of building MCP servers by:

1. **Gathering requirements** through interactive questions about your server's purpose
2. **Selecting the right SDK** (TypeScript, Python, Java, Kotlin, or C#)
3. **Generating project structure** with proper dependencies and build configuration
4. **Creating server implementation** with tools, resources, and prompts
5. **Configuring Claude Desktop** integration with proper paths and environment
6. **Providing testing guidance** with MCP Inspector and validation steps

## When to Use

Use this skill when you want to:

- Connect Claude to your data sources (databases, APIs, files)
- Expose custom tools for AI to call
- Build workflow automation servers
- Create enterprise integrations
- Learn MCP development patterns

## Trigger Phrases

- "create an MCP server for [purpose]"
- "build a Model Context Protocol server"
- "set up MCP integration with [data source]"
- "help me create a server for Claude Desktop"
- "scaffold an MCP server"

## What Gets Generated

### Project Structure

```
mcp-server-name/
├── src/
│   └── index.ts (or main.py)
├── build/ (TypeScript only)
├── package.json / pyproject.toml
├── tsconfig.json (TypeScript only)
├── .env.example
├── .gitignore
└── README.md
```

### Key Features

- ✅ Full TypeScript or Python server implementation
- ✅ Proper SDK integration with error handling
- ✅ Tool definitions with Zod schemas or type hints
- ✅ Resource and prompt handlers (if needed)
- ✅ Claude Desktop configuration
- ✅ Environment variable management
- ✅ Security best practices (.gitignore, input validation)
- ✅ Comprehensive documentation
- ✅ Testing instructions with MCP Inspector

## Example Usage

### Simple Tool Server

**You:** "Create an MCP server that can search my local documents"

**Skill generates:**
- File search tool with glob patterns
- Content search tool using grep
- Resource handlers for file contents
- Claude Desktop configuration
- Security validations (path traversal prevention)

### Database Integration

**You:** "Build an MCP server to query my PostgreSQL database"

**Skill generates:**
- Database query tool with SQL validation
- Schema inspection tools
- Connection pooling setup
- Environment variable configuration
- Read-only query enforcement

### API Wrapper

**You:** "Create a server that wraps the GitHub API"

**Skill generates:**
- GitHub API client setup
- Tools for common operations (search, issues, PRs)
- Authentication configuration
- Rate limiting handling
- Response formatting for AI consumption

## Supported Languages

| Language | SDK | Best For |
|----------|-----|----------|
| **TypeScript** | `@modelcontextprotocol/sdk` | Web APIs, JS ecosystem |
| **Python** | `mcp[cli]` (FastMCP) | Data processing, ML |
| **Java** | Spring AI MCP | Enterprise Java apps |
| **Kotlin** | Kotlin SDK | Android/JVM apps |
| **C#** | ModelContextProtocol NuGet | Windows/Azure apps |

## Common Patterns Included

The skill includes templates and guidance for:

- **Database Integration**: PostgreSQL, MySQL, MongoDB
- **API Wrappers**: REST APIs, GraphQL
- **File System Access**: Secure file operations
- **Search Integration**: Elasticsearch, vector search
- **Workflow Automation**: CI/CD, deployments
- **Notification Systems**: Email, Slack, SMS
- **Data Processing**: ETL, analytics pipelines
- **Authentication**: Token validation, permissions

## Testing Your Server

The skill provides three testing approaches:

1. **MCP Inspector** (recommended first)
   ```bash
   npx @modelcontextprotocol/inspector node build/index.js
   ```
   - Browser-based testing interface
   - Validates schemas and responses
   - No Claude Desktop required

2. **Claude Desktop Integration**
   - Add to `claude_desktop_config.json`
   - Restart Claude Desktop
   - Test with natural language

3. **Custom Client**
   - Build your own MCP client
   - Use in other AI applications

## Files Included

### Templates
- `typescript-server.ts.template` - Full TypeScript server template
- `python-server.py.template` - Full Python server template
- `package.json.template` - npm configuration
- `tsconfig.json.template` - TypeScript configuration

### Data Files
- `common-patterns.yaml` - 8 common server patterns with dependencies
- `tool-examples.yaml` - Example tool definitions for common use cases

## Security Features

Every generated server includes:

- ✅ Environment variable management (never commit secrets)
- ✅ Input validation with schemas
- ✅ Proper error handling (don't leak internals)
- ✅ .gitignore configuration
- ✅ Logging best practices (stderr only for STDIO)
- ✅ Path traversal prevention (file servers)
- ✅ SQL injection prevention (database servers)

## Next Steps After Generation

1. Review generated code and customize tool implementations
2. Add your API keys/credentials to `.env`
3. Build the project (`npm run build` for TypeScript)
4. Test with MCP Inspector
5. Add to Claude Desktop configuration
6. Test with natural language queries
7. Iterate and enhance based on usage

## Troubleshooting

The skill includes debugging guidance for:

- Server not detected in Claude Desktop
- Tools not appearing
- Connection timeouts
- Build errors
- STDIO logging issues
- Configuration syntax errors

Check `~/Library/Logs/Claude/mcp*.log` for detailed error messages.

## Learn More

- [MCP Documentation](https://modelcontextprotocol.io)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Example Servers](https://github.com/modelcontextprotocol/servers)

---

**Created by**: Connor
**Version**: 0.1.0
**License**: MIT
