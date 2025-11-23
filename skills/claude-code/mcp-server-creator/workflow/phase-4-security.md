# Phase 4: Environment & Security

**Purpose**: Secure secrets and configure environment

## Generate .env.example

```bash
# API Keys and Secrets
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Server Configuration
PORT=3000
LOG_LEVEL=info
```

## Generate .gitignore

```
# Dependencies
node_modules/
.venv/
__pycache__/

# Build outputs
build/
dist/
*.pyc

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

## Security Best Practices

- ✓ Never commit .env files
- ✓ Use environment variables for all secrets
- ✓ Validate all inputs with schemas
- ✓ Implement proper error handling (don't leak internals)
- ✓ Use HTTPS for HTTP transport servers

## Output

Secure configuration with secrets management

## Transition

Proceed to Phase 5 (Claude Desktop Integration)
