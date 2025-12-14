# Project-Type Templates

Pre-built architecture diagram templates for common project types. Use these as starting points after auto-discovery detects the project type.

## Template Selection

| Project Type | Detection Signals | Template |
|--------------|-------------------|----------|
| Bulletproof React | `src/features/*`, eslint-plugin-import | [bulletproof-react](#bulletproof-react) |
| Next.js App Router | `src/app/**/page.tsx`, next.config.* | [next-app-router](#nextjs-app-router) |
| Express API | express in deps, `routes/*` or `controllers/*` | [express-api](#express-api) |
| Monorepo (Nx/Turborepo) | `packages/*` or `apps/*`, workspace config | [monorepo](#monorepo) |
| Generic Full-Stack | Mixed patterns | [generic-fullstack](#generic-full-stack) |

---

## Bulletproof React

**Detection**: `src/features/*/index.{ts,tsx}` + eslint-plugin-import

```
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │
│  │   app/      │     │  features/  │     │   shared/   │        │
│  │  (routes)   │────►│  (domains)  │────►│  (common)   │        │
│  └─────────────┘     └─────────────┘     └─────────────┘        │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │
│  │   routes/   │     │ components/ │     │    lib/     │        │
│  │   layouts/  │     │   hooks/    │     │   types/    │        │
│  │             │     │    api/     │     │   utils/    │        │
│  └─────────────┘     └─────────────┘     └─────────────┘        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Import Rules: app → features → shared (unidirectional)         │
└─────────────────────────────────────────────────────────────────┘
```

**Populate with**:
- Features from `glob: src/features/*/index.ts`
- Routes from `glob: src/app/**`
- Cross-feature deps from `grep: import.*from '@/features`

---

## Next.js App Router

**Detection**: `app/**/page.tsx` + `next.config.*`

```
┌─────────────────────────────────────────────────────────────────┐
│                     NEXT.JS APP STRUCTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                     app/                              │       │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │       │
│  │  │ layout  │  │  page   │  │ loading │  │  error  │  │       │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │       │
│  │       │            │                                  │       │
│  │       ▼            ▼                                  │       │
│  │  ┌─────────────────────────────────────────────┐     │       │
│  │  │              Route Groups                    │     │       │
│  │  │   (auth)/   (dashboard)/   (public)/        │     │       │
│  │  └─────────────────────────────────────────────┘     │       │
│  └──────────────────────────────────────────────────────┘       │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │
│  │ components/ │     │    lib/     │     │   types/    │        │
│  │   (UI)      │     │  (server)   │     │  (shared)   │        │
│  └─────────────┘     └─────────────┘     └─────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Populate with**:
- Route groups from `glob: src/app/(*)/`
- Dynamic routes from `glob: src/app/**/[*]`
- Server actions from `grep: "use server"`

---

## Express API

**Detection**: `express` in dependencies + `routes/*` or `controllers/*`

```
┌─────────────────────────────────────────────────────────────────┐
│                      EXPRESS API LAYERS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request ──►  ┌──────────────────────────────────┐              │
│               │         Middleware Layer          │              │
│               │  auth │ validation │ rate-limit   │              │
│               └──────────────┬───────────────────┘              │
│                              │                                   │
│                              ▼                                   │
│               ┌──────────────────────────────────┐              │
│               │          Routes Layer             │              │
│               │   /api/users  │  /api/products   │              │
│               └──────────────┬───────────────────┘              │
│                              │                                   │
│                              ▼                                   │
│               ┌──────────────────────────────────┐              │
│               │        Controllers Layer          │              │
│               │   userController │ productCtrl   │              │
│               └──────────────┬───────────────────┘              │
│                              │                                   │
│                              ▼                                   │
│               ┌──────────────────────────────────┐              │
│               │         Services Layer            │              │
│               │   userService │ productService   │              │
│               └──────────────┬───────────────────┘              │
│                              │                                   │
│                              ▼                                   │
│               ┌──────────────────────────────────┐              │
│               │           Data Layer              │              │
│               │    models │ repositories │ db    │              │
│               └──────────────────────────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Populate with**:
- Routes from `glob: routes/*.js` or `grep: router\.(get|post|put|delete)`
- Controllers from `glob: controllers/*.js`
- Models from `glob: models/*.js`

---

## Monorepo

**Detection**: `packages/*` or `apps/*` + workspace config (nx.json, turbo.json, pnpm-workspace.yaml)

```
┌─────────────────────────────────────────────────────────────────┐
│                     MONOREPO STRUCTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                      apps/                           │        │
│  │   ┌─────────┐   ┌─────────┐   ┌─────────┐           │        │
│  │   │   web   │   │  admin  │   │   api   │           │        │
│  │   └────┬────┘   └────┬────┘   └────┬────┘           │        │
│  └────────┼─────────────┼────────────┼──────────────────┘        │
│           │             │            │                           │
│           └─────────────┼────────────┘                           │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                   packages/                          │        │
│  │   ┌─────────┐   ┌─────────┐   ┌─────────┐           │        │
│  │   │   ui    │   │  utils  │   │  types  │           │        │
│  │   └─────────┘   └─────────┘   └─────────┘           │        │
│  │   ┌─────────┐   ┌─────────┐   ┌─────────┐           │        │
│  │   │  config │   │   api   │   │  eslint │           │        │
│  │   └─────────┘   └─────────┘   └─────────┘           │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Dependency Flow: apps → packages (unidirectional)              │
└─────────────────────────────────────────────────────────────────┘
```

**Populate with**:
- Apps from `glob: apps/*/package.json`
- Packages from `glob: packages/*/package.json`
- Internal deps from each package.json dependencies

---

## Generic Full-Stack

**Detection**: Mixed patterns or undetected project type

```
┌─────────────────────────────────────────────────────────────────┐
│                    FULL-STACK APPLICATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐     ┌─────────────────────┐            │
│  │      Frontend       │     │       Backend       │            │
│  │   ┌───────────┐     │     │   ┌───────────┐     │            │
│  │   │    UI     │     │     │   │    API    │     │            │
│  │   │Components │     │ ──► │   │  Routes   │     │            │
│  │   └───────────┘     │     │   └───────────┘     │            │
│  │   ┌───────────┐     │     │   ┌───────────┐     │            │
│  │   │   State   │     │     │   │  Services │     │            │
│  │   │Management │     │     │   │  Business │     │            │
│  │   └───────────┘     │     │   └───────────┘     │            │
│  │   ┌───────────┐     │     │   ┌───────────┐     │            │
│  │   │    API    │     │     │   │    Data   │     │            │
│  │   │   Client  │     │     │   │   Layer   │     │            │
│  │   └───────────┘     │     │   └───────────┘     │            │
│  └─────────────────────┘     └─────────────────────┘            │
│                                      │                           │
│                                      ▼                           │
│                         ┌─────────────────────┐                  │
│                         │      Database       │                  │
│                         └─────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Populate with**:
- Manual discovery based on directory structure
- `ls src/` or `tree -L 2` for structure overview

---

## Usage Instructions

1. **Auto-detect project type** using Phase 0 discovery commands
2. **Select matching template** from this reference
3. **Run populate commands** to fill in actual component names
4. **Customize** by adding/removing boxes based on actual architecture
5. **Add diagram metadata** for versioning (see below)

### Adding Diagram Metadata

Include this comment block at the top of generated diagrams:

```markdown
<!-- diagram-meta
  type: [template-name]
  created: YYYY-MM-DD
  last-verified: YYYY-MM-DD
  source-patterns: [glob patterns used]
  stale-after: 30d
-->
```

This enables automated staleness detection when the codebase structure changes.
