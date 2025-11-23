# Mode 1: Sandbox (Vite + React + TypeScript)

**Purpose**: Lightning-fast React setup for experiments and learning

**Setup Time**: ~15 seconds after `npm install`

## Tech Stack
- Vite 5+ (fastest dev server, HMR in <50ms)
- React 18+
- TypeScript (strict mode)
- ESLint + Prettier (minimal config)

**Configuration Strategy**: Fully automated, zero questions

## Workflow Steps

### 1. Scaffold with Vite
```bash
npm create vite@latest {project-name} -- --template react-ts
cd {project-name}
```

### 2. Configure TypeScript Strict Mode
- Update tsconfig.json with Connor's strict settings
- Enable all strict flags
- Configure path aliases

### 3. Set Up Linting
- Install ESLint + Prettier
- Apply minimal config (no overkill for sandbox)
- Add format script to package.json

### 4. Initialize Git
```bash
git init
git add .
git commit -m "feat: initial Vite + React + TypeScript setup"
```

### 5. Provide Next Steps

```markdown
## Your Sandbox is Ready!

Start development:
  cd {project-name}
  npm install
  npm run dev

Project structure:
  src/
    ├── App.tsx          # Main component
    ├── main.tsx         # Entry point
    └── vite-env.d.ts    # Vite types

Available commands:
  npm run dev          # Start dev server (http://localhost:5173)
  npm run build        # Build for production
  npm run preview      # Preview production build
  npm run lint         # Check code quality
```

## When to Use

- Quick experiments and prototypes
- Learning React concepts
- Testing ideas before enterprise implementation
- Minimal overhead needed
