# Mode 2: Enterprise (Next.js + Full Tooling)

**Purpose**: Production-ready web applications with industry-standard tooling

**Setup Time**: ~60 seconds after `npm install`

## Tech Stack
- Next.js 14+ (App Router)
- React 18+
- TypeScript (strict mode)
- Vitest + React Testing Library
- ESLint + Prettier + Husky
- GitHub Actions CI/CD
- Conventional Commits

**Configuration Strategy**: 2-3 key questions, smart defaults

## Configuration Questions

1. "Include testing setup?" (default: yes)
2. "Include CI/CD workflows?" (default: yes)
3. "Use src/ directory?" (default: yes)

## Workflow Steps

### 1. Scaffold with Next.js
```bash
npx create-next-app@latest {project-name} \
  --typescript \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
cd {project-name}
```

### 2. Apply Connor's TypeScript Standards
- Update tsconfig.json with strict mode
- Configure path aliases
- Enable all type checking flags

### 3. Set Up Testing (if selected)
- Install Vitest, React Testing Library, jsdom
- Create vitest.config.ts with coverage settings (80% threshold)
- Add example test: `__tests__/page.test.tsx`
- Configure Testing Trophy approach
- Add test scripts:
  ```json
  "test": "vitest --run",
  "test:watch": "vitest",
  "test:coverage": "vitest --coverage",
  "test:low": "vitest --maxWorkers=2"
  ```

### 4. Configure Linting & Formatting
- Extend ESLint config with strict rules
- Add Prettier with Connor's preferences
- Install and configure Husky + lint-staged
- Set up pre-commit hook for:
  - Linting
  - Format checking
  - Type checking
  - Test running (on relevant files)

### 5. Set Up CI/CD (if selected)
- Create `.github/workflows/ci.yml`
- Configure on PR triggers
- Steps: install → lint → type-check → test → build
- Add status badge to README

### 6. Initialize Git with Standards
```bash
git init
git add .
git commit -m "feat: initial Next.js enterprise setup with testing and CI/CD"
```

### 7. Provide Next Steps

```markdown
## Your Enterprise React Project is Ready!

Start development:
  cd {project-name}
  npm install
  npm run dev

Project structure:
  src/
    ├── app/              # Next.js App Router
    │   ├── page.tsx      # Home page
    │   └── layout.tsx    # Root layout
    ├── components/       # React components
    ├── lib/              # Utility functions
    └── __tests__/        # Test files

Available commands:
  npm run dev              # Start dev server
  npm run build            # Production build
  npm run test             # Run tests (low CPU)
  npm run test:coverage    # Tests with coverage

Configured features:
  ✓ TypeScript strict mode
  ✓ Testing Trophy approach (Vitest + RTL)
  ✓ ESLint + Prettier + Husky
  ✓ GitHub Actions CI/CD
  ✓ 80% coverage threshold
  ✓ Pre-commit hooks
```

## When to Use

- Production web applications
- Team projects requiring standards
- Projects needing CI/CD from day one
- Full testing infrastructure needed
