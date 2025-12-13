# Enterprise Mode - Next.js + Full Tooling

## Mode Overview

**Purpose**: Production-ready web applications with comprehensive tooling and testing

**Target Users**:
- Building SaaS products
- Enterprise dashboards and admin panels
- Content-heavy websites with SEO needs
- Applications requiring server-side rendering
- Teams needing consistent standards

**Setup Time**: ~60 seconds (after npm install)

**Philosophy**: Production-ready from day one. Industry-standard tooling with Connor's quality standards built in.

---

## Tech Stack

```yaml
Framework:
  - Next.js 14+ (App Router, React Server Components)
  - React 18+
  - TypeScript 5+ (strict mode)

Testing:
  - Vitest (Testing Trophy approach)
  - React Testing Library
  - jsdom (DOM simulation)
  - 80% coverage threshold

Code Quality:
  - ESLint (Next.js config + strict rules)
  - Prettier (consistent formatting)
  - Husky (pre-commit hooks)
  - lint-staged (staged files only)

CI/CD:
  - GitHub Actions
  - Automated testing on PR
  - Build validation
  - Type checking

Standards:
  - Conventional Commits
  - Branch naming conventions
  - Comprehensive documentation
```

---

## Workflow

### Step 1: Validate Prerequisites

```bash
# Check Node.js version (>= 18)
node --version

# Check npm version (>= 9)
npm --version

# Check git is installed
git --version
```

**If validation fails**: Provide clear upgrade instructions with links

### Step 2: Ask Configuration Questions

Only ask essential questions with smart defaults:

**Question 1: Project Name**
- "What should I name your project?"
- Validation: kebab-case, 3-50 chars, no existing directory
- Example: my-awesome-app

**Question 2: Testing Setup**
- "Include testing infrastructure? (Vitest + React Testing Library)"
- Default: YES
- Explain: "Recommended for production apps. Adds ~30s to setup."

**Question 3: CI/CD Workflows**
- "Include GitHub Actions CI/CD?"
- Default: YES
- Explain: "Automated testing on every PR. Requires GitHub repository."

**Question 4: Source Directory**
- "Use src/ directory for better organization?"
- Default: YES
- Explain: "Keeps root clean. Next.js best practice."

### Step 3: Scaffold with Next.js

```bash
npx create-next-app@latest {project-name} \
  --typescript \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-tailwind

cd {project-name}
```

**Why these flags?**
- `--typescript`: Connor requires TypeScript
- `--eslint`: Linting from start
- `--app`: Use App Router (modern approach)
- `--src-dir`: Clean project structure
- `--import-alias`: Absolute imports with @/
- `--no-tailwind`: Let user choose styling (can add later)

### Step 4: Apply Connor's TypeScript Standards

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    },

    /* Connor's Strict Mode Additions */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noImplicitOverride": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Step 5: Set Up Testing (if selected)

**5.1 Install Dependencies**

```bash
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event @vitest/coverage-v8
```

**5.2 Create `vitest.config.ts`**

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/__tests__/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/__tests__/',
        '**/*.config.ts',
        '**/*.config.js',
        '.next/',
      ],
      // Connor's 80% threshold
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**5.3 Create Test Setup File**

`src/__tests__/setup.ts`:

```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

**5.4 Create Example Test**

`src/__tests__/page.test.tsx`:

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Page from '@/app/page';

describe('Home Page', () => {
  it('should render welcome message when page loads', () => {
    render(<Page />);

    // Testing Trophy approach: Test user-visible behavior
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
  });

  it('should have semantic HTML structure for accessibility', () => {
    const { container } = render(<Page />);

    // Check for main landmark
    const main = container.querySelector('main');
    expect(main).toBeInTheDocument();
  });
});
```

**5.5 Update package.json Scripts**

Add to `scripts`:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "vitest --run",
    "test:watch": "vitest",
    "test:coverage": "vitest --coverage",
    "test:low": "vitest --maxWorkers=2 --run",
    "test:ui": "vitest --ui"
  }
}
```

### Step 6: Configure Code Quality Tools

**6.1 Extend ESLint Configuration**

Update `.eslintrc.json`:

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "no-console": "warn",
    "no-var": "error",
    "eqeqeq": ["error", "always"],
    "prefer-const": "error",
    "@typescript-eslint/no-unused-vars": [
      "error",
      { "argsIgnorePattern": "^_" }
    ],
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

**6.2 Add Prettier**

Create `.prettierrc`:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

Create `.prettierignore`:

```
node_modules
.next
out
build
dist
coverage
*.lock
```

Install Prettier:

```bash
npm install -D prettier eslint-config-prettier
```

Update `.eslintrc.json` to include Prettier:

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ]
}
```

**6.3 Set Up Husky + lint-staged**

```bash
npx husky-init && npm install
npm install -D lint-staged
```

Update `.husky/pre-commit`:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

Create `.lintstagedrc.js`:

```javascript
module.exports = {
  '*.{ts,tsx}': [
    'eslint --fix',
    'prettier --write',
    () => 'tsc --noEmit', // Type check
  ],
  '*.{json,md}': ['prettier --write'],
};
```

Update `package.json`:

```json
{
  "scripts": {
    "prepare": "husky install"
  }
}
```

### Step 7: Set Up CI/CD (if selected)

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.node-version == '20.x'
        with:
          file: ./coverage/coverage-final.json
          flags: unittests

      - name: Build project
        run: npm run build
        env:
          NODE_ENV: production
```

### Step 8: Create Project Documentation

**8.1 Update README.md**

```markdown
# {project-name}

Production-ready Next.js application with comprehensive testing and tooling.

## Features

- ⚡ Next.js 14+ with App Router
- 🔷 TypeScript (strict mode)
- 🧪 Testing Trophy approach (Vitest + RTL)
- ✅ 80% test coverage threshold
- 🎨 ESLint + Prettier
- 🪝 Husky pre-commit hooks
- 🔄 GitHub Actions CI/CD
- 📝 Conventional Commits

## Getting Started

### Prerequisites

- Node.js 18+
- npm 9+

### Installation

\`\`\`bash
npm install
\`\`\`

### Development

\`\`\`bash
npm run dev
\`\`\`

Visit [http://localhost:3000](http://localhost:3000)

## Project Structure

\`\`\`
src/
├── app/                    # Next.js App Router
│   ├── page.tsx            # Home page
│   ├── layout.tsx          # Root layout
│   └── globals.css         # Global styles
├── components/             # React components
│   ├── ui/                 # UI components
│   └── features/           # Feature components
├── lib/                    # Utility functions
│   └── utils.ts
└── __tests__/              # Test files
    ├── setup.ts            # Test configuration
    └── page.test.tsx       # Example test
\`\`\`

## Available Commands

### Development
- \`npm run dev\` - Start dev server (http://localhost:3000)
- \`npm run build\` - Build for production
- \`npm run start\` - Start production server

### Code Quality
- \`npm run lint\` - Lint code with ESLint
- \`npm run type-check\` - Check TypeScript types

### Testing
- \`npm run test\` - Run all tests
- \`npm run test:watch\` - Run tests in watch mode
- \`npm run test:coverage\` - Run tests with coverage report
- \`npm run test:low\` - Run tests (low CPU usage)

## Testing Strategy

This project follows the **Testing Trophy** approach:

- **70% Integration Tests**: User workflows and component interactions
- **20% Unit Tests**: Complex business logic
- **10% E2E Tests**: Critical user journeys

### Writing Tests

Test file naming: \`[component-name].test.tsx\`

Test structure:
\`\`\`typescript
describe('Component Name', () => {
  it('should [behavior] when [condition]', () => {
    // Arrange, Act, Assert
  });
});
\`\`\`

Use semantic queries (React Testing Library):
1. \`getByRole()\` - Most preferred
2. \`getByLabelText()\` - Form elements
3. \`getByText()\` - User-visible content
4. \`getByTestId()\` - Last resort only

### Coverage Requirements

Minimum 80% coverage for:
- Lines
- Functions
- Branches
- Statements

## Git Workflow

### Branch Naming

- \`feature/description\` - New features
- \`bugfix/description\` - Bug fixes
- \`chore/description\` - Maintenance tasks

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

\`\`\`
feat: add user authentication
fix: resolve login redirect issue
test: add tests for auth flow
docs: update API documentation
chore: update dependencies
\`\`\`

### Pre-commit Checks

Husky automatically runs before each commit:
- ESLint (auto-fix enabled)
- Prettier (auto-format)
- TypeScript type checking
- Staged files only (fast)

## Deployment

### Vercel (Recommended)

\`\`\`bash
npm install -g vercel
vercel
\`\`\`

### Docker

\`\`\`bash
docker build -t {project-name} .
docker run -p 3000:3000 {project-name}
\`\`\`

## Environment Variables

Create \`.env.local\`:

\`\`\`env
# Example variables
NEXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgresql://...
\`\`\`

## CI/CD

GitHub Actions runs on every PR:
1. Install dependencies
2. Lint code
3. Type check
4. Run tests with coverage
5. Build project

## Tech Stack Details

### Why Next.js?
- Server-side rendering for SEO
- API routes for backend logic
- Optimized image handling
- Industry standard (Netflix, TikTok)

### Why Vitest?
- 10x faster than Jest
- Compatible with Vite
- Great TypeScript support
- Modern testing features

## Contributing

1. Create a feature branch
2. Make changes with tests
3. Ensure all checks pass
4. Submit PR with description

## License

MIT

---

Built with [react-project-scaffolder](https://github.com/yourusername/react-project-scaffolder)
```

**8.2 Create CONTRIBUTING.md**

```markdown
# Contributing Guidelines

## Development Standards

### Code Quality
- TypeScript strict mode (all flags enabled)
- No \`console.log\` in production code
- No \`any\` types
- Explicit return types for functions

### Testing
- Write tests for new features
- Maintain 80% coverage minimum
- Follow Testing Trophy approach
- Use semantic queries in tests

### Commits
- Follow Conventional Commits format
- Keep commits atomic and focused
- Write descriptive commit messages

## Development Workflow

1. **Create branch**: \`git checkout -b feature/your-feature\`
2. **Make changes**: Edit code + add tests
3. **Run checks**: \`npm run lint && npm run test\`
4. **Commit**: \`git commit -m "feat: your feature"\`
5. **Push**: \`git push origin feature/your-feature\`
6. **Create PR**: Submit for review

## Pre-commit Checks

Husky runs these automatically:
- ESLint (fixes issues automatically)
- Prettier (formats code)
- TypeScript (type checking)

If checks fail, fix issues before committing.

## Testing Guidelines

### What to Test
- User-visible behavior
- Business logic
- Error handling
- Edge cases

### What NOT to Test
- Implementation details
- External libraries
- Trivial functions

### Example Test

\`\`\`typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should submit form when user enters valid credentials', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});
\`\`\`

## Questions?

Open an issue or reach out to the maintainers.
```

### Step 9: Initialize Git

```bash
git init
git add .
git commit -m "feat: initial Next.js enterprise setup with testing and CI/CD

- Next.js 14 with App Router
- TypeScript strict mode
- Vitest + React Testing Library (80% coverage)
- ESLint + Prettier + Husky
- GitHub Actions CI/CD
- Comprehensive documentation"
```

### Step 10: Verify Setup

```bash
# Verify all files
ls -la

# Check dependencies installed
npm list --depth=0

# Verify TypeScript config
cat tsconfig.json | grep "strict"

# Verify tests can run
npm run test

# Verify build works
npm run build
```

### Step 11: Provide User Instructions

**Display to user**:

```markdown
✅ Enterprise project "{project-name}" created successfully!

📁 Location: ./{project-name}

🚀 Next steps:

  1. cd {project-name}
  2. npm install
  3. npm run dev

Your dev server will start at http://localhost:3000

📚 What you have:
  ✓ Next.js 14 with App Router
  ✓ TypeScript strict mode
  ✓ Vitest + React Testing Library (80% coverage)
  ✓ ESLint + Prettier + Husky
  ✓ GitHub Actions CI/CD
  ✓ Testing Trophy approach
  ✓ Comprehensive documentation

🧪 Test your setup:
  npm run test           # Run all tests
  npm run lint           # Check code quality
  npm run type-check     # Verify types

📋 Pre-commit hooks active:
  - Linting (auto-fix)
  - Formatting (auto-format)
  - Type checking

🔄 CI/CD ready:
  - Push to GitHub to activate workflows
  - Automated testing on every PR

💡 Tips:
  - Follow Testing Trophy: 70% integration, 20% unit, 10% e2e
  - Use semantic queries: getByRole() > getByLabelText() > getByText()
  - Write tests alongside features (TDD approach)
  - Keep commits following Conventional Commits format

📖 Documentation:
  - README.md - Project overview and commands
  - CONTRIBUTING.md - Development guidelines

🎯 Production-ready from day one!
```

---

## File Structure Output

```
{project-name}/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── .husky/
│   └── pre-commit              # Pre-commit hooks
├── .vscode/ (optional)
│   └── settings.json           # Editor config
├── src/
│   ├── app/
│   │   ├── page.tsx            # Home page
│   │   ├── layout.tsx          # Root layout
│   │   ├── globals.css         # Global styles
│   │   └── favicon.ico         # Favicon
│   ├── components/
│   │   ├── ui/                 # UI components
│   │   └── features/           # Feature components
│   ├── lib/
│   │   └── utils.ts            # Utilities
│   └── __tests__/
│       ├── setup.ts            # Test setup
│       └── page.test.tsx       # Example test
├── public/                     # Static files
├── .eslintrc.json              # ESLint config
├── .prettierrc                 # Prettier config
├── .prettierignore             # Prettier ignore
├── .gitignore                  # Git ignore
├── .lintstagedrc.js            # lint-staged config
├── vitest.config.ts            # Vitest config
├── tsconfig.json               # TypeScript config
├── next.config.js              # Next.js config
├── package.json                # Dependencies
├── README.md                   # Documentation
└── CONTRIBUTING.md             # Guidelines
```

---

## Success Criteria

- [ ] Next.js project scaffolded with App Router
- [ ] TypeScript strict mode enabled (all flags)
- [ ] Vitest + RTL configured with 80% threshold
- [ ] Example test passes
- [ ] ESLint + Prettier configured
- [ ] Husky pre-commit hooks working
- [ ] GitHub Actions workflow created
- [ ] README and CONTRIBUTING.md generated
- [ ] Git initialized with commit
- [ ] `npm run dev` starts successfully
- [ ] `npm run test` passes
- [ ] `npm run build` completes
- [ ] Setup time < 90 seconds (excluding npm install)

---

## Troubleshooting

**Issue**: Husky pre-commit hook fails
**Solution**: Run `npm run lint -- --fix` to auto-fix issues

**Issue**: Tests fail with module resolution errors
**Solution**: Check vitest.config.ts has correct path aliases

**Issue**: Type errors in strict mode
**Solution**: This shouldn't happen - review generated code

**Issue**: Build fails
**Solution**: Run `npm run type-check` to see TypeScript errors

**Issue**: Coverage below 80%
**Solution**: Add more tests or adjust threshold temporarily

---

## Why This Tech Stack?

**Next.js over Vite**:
- Server-side rendering for SEO
- Built-in routing
- API routes for backend
- Image optimization
- Battle-tested at scale (Netflix, Uber)

**Vitest over Jest**:
- 10x faster test execution
- Better TypeScript support
- Modern ESM support
- Compatible with Vite ecosystem

**Husky + lint-staged**:
- Catch issues before commit
- Fast (only staged files)
- Team consistency
- Industry standard

**GitHub Actions**:
- Free for public repos
- Integrated with GitHub
- Easy to configure
- Extensive marketplace

---

**Remember**: This mode is production-ready. Every tool included is standard in industry and aligned with Connor's "production-ready from day one" philosophy.
