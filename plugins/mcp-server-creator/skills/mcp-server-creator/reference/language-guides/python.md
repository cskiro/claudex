# Python MCP Server Best Practices (FastMCP)

## Setup

```bash
uv init mcp-server-name
uv add "mcp[cli]"
```

## Implementation

- ✓ Use type hints (FastMCP reads them!)
- ✓ Write detailed docstrings (becomes tool descriptions)
- ✓ Use async functions for I/O
- ✓ Handle exceptions gracefully
- ✓ Log to stderr only in STDIO mode

## Tool Definition

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-name")

@mcp.tool()
async def search_database(query: str, limit: int = 10) -> str:
    """
    Search the database for records matching the query.

    Args:
        query: Search terms to match against records
        limit: Maximum number of results to return (default: 10)

    Returns:
        JSON string of matching records
    """
    results = await db.search(query, limit=limit)
    return json.dumps(results)
```

## Resource Definition

```python
@mcp.resource("db://tables/{table_name}/schema")
async def get_table_schema(table_name: str) -> str:
    """Get the schema for a database table."""
    schema = await db.get_schema(table_name)
    return json.dumps(schema)
```

## Critical Rules

### STDIO Transport

```python
import sys

# WRONG - corrupts JSON-RPC
print("Debug info")

# CORRECT - safe for STDIO
print("Debug info", file=sys.stderr)

# Or use logging
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
```

### Error Handling

```python
@mcp.tool()
async def risky_operation(param: str) -> str:
    """Perform an operation that might fail."""
    try:
        result = await external_api.call(param)
        return str(result)
    except Exception as e:
        logging.error(f"Operation failed: {e}")
        raise ValueError(f"Operation failed: {e}")
```

## Run

```bash
# With uv
uv run main.py

# Direct
python main.py
```
