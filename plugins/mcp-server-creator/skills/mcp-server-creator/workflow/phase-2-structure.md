# Phase 2: Project Structure Generation

**Purpose**: Create proper project structure with SDK integration

## TypeScript Project Setup

```bash
# Create project directory
mkdir mcp-[server-name]
cd mcp-[server-name]

# Initialize npm project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk zod
npm install -D @types/node typescript
```

### TypeScript Configuration (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### Package.json Scripts

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc && node -e \"require('fs').chmodSync('build/index.js', '755')\"",
    "watch": "tsc --watch",
    "start": "node build/index.js"
  }
}
```

## Python Project Setup

```bash
# Create project with uv
uv init mcp-[server-name]
cd mcp-[server-name]

# Set up virtual environment
uv venv
source .venv/bin/activate

# Install MCP SDK
uv add "mcp[cli]"
```

## File Structure

```
mcp-server-name/
├── src/
│   └── index.ts (or main.py)
├── build/ (TypeScript only)
├── .env.example
├── .gitignore
├── package.json / pyproject.toml
├── tsconfig.json (TypeScript only)
└── README.md
```

## Output

Complete project structure with dependencies installed

## Transition

Proceed to Phase 3 (Server Implementation)
