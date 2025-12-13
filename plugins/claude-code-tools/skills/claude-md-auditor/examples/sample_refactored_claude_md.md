# CLAUDE.md

<!-- Refactored: 2025-10-26 09:32:18 -->
<!-- Based on official Anthropic guidelines and best practices -->

<!-- Tier: Project -->

# Claude Configuration v4.4.0

## 🚨 CRITICAL: Must-Follow Standards

<!-- Place non-negotiable standards here (top position = highest attention) -->

- [Add critical security requirements]
- [Add critical quality gates]
- [Add critical workflow requirements]

## 📋 Project Overview

**Tech Stack**: [List technologies]
**Architecture**: [Architecture pattern]
**Purpose**: [Project purpose]

## 🔧 Development Workflow

### Git Workflow
- Branch pattern: `feature/{name}`, `bugfix/{name}`
- Conventional commit messages required
- PRs require: tests + review + passing CI

## 📝 Code Standards

### TypeScript/JavaScript
- TypeScript strict mode: enabled
- No `any` types (use `unknown` if needed)
- Explicit return types required

### Testing
- Minimum coverage: 80%
- Testing trophy: 70% integration, 20% unit, 10% E2E
- Test naming: 'should [behavior] when [condition]'

## 📌 REFERENCE: Common Tasks

<!-- Bottom position = recency attention, good for frequently accessed info -->

### Build & Test
```bash
npm run build        # Build production
npm test            # Run tests
npm run lint        # Run linter
```

### Key File Locations
- Config: `/config/app.config.ts`
- Types: `/src/types/index.ts`
- Utils: `/src/utils/index.ts`

## 📚 Detailed Documentation (Imports)

<!-- Use imports to keep this file lean (<300 lines) -->

<!-- Example:
@docs/architecture.md
@docs/testing-strategy.md
@docs/deployment.md
-->


---

**Last Updated**: 2025-10-26
**Maintained By**: [Team/Owner]

<!-- Follow official guidance: Keep lean, be specific, use structure -->
