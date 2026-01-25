# Sandbox Mode - Vite + React + TypeScript

## Mode Overview

**Purpose**: Lightning-fast React setup for experiments, prototyping, and learning

**Target Users**:
- Developers testing React concepts
- Quick proof-of-concept implementations
- Learning React fundamentals
- Isolating bug reproductions

**Setup Time**: ~15 seconds (after npm install)

**Philosophy**: Minimal configuration, maximum speed. Zero questions asked.

---

## Tech Stack

```yaml
Core:
  - Vite 5+ (fastest dev server, HMR in <50ms)
  - React 18+
  - TypeScript 5+ (strict mode)

Development:
  - ESLint (minimal rules, quick feedback)
  - Prettier (automatic formatting)

Excluded (intentionally):
  - Testing frameworks (add if needed)
  - Pre-commit hooks (keep it light)
  - CI/CD (not needed for sandboxes)
  - Additional tooling (KISS principle)
```

---

## Workflow

### Step 1: Validate Prerequisites

```bash
# Check Node.js version (>= 18)
node --version

# Check npm version (>= 9)
npm --version
```

**If validation fails**: Show clear error with upgrade instructions

### Step 2: Get Project Name

**Ask user**: "What should I name your sandbox project?"

**Validation**:
- No spaces (suggest kebab-case)
- Valid directory name
- Not already existing
- Length 3-50 characters

**Auto-suggest**: If empty, suggest `react-sandbox-{timestamp}`

### Step 3: Scaffold with Vite

```bash
npm create vite@latest {project-name} -- --template react-ts
```

**Why Vite?**
- Fastest dev server (instant HMR)
- Native ES modules (no bundling in dev)
- Minimal config out of box
- Production builds with Rollup

### Step 4: Configure TypeScript (Strict Mode)

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Connor's Strict Mode Settings */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noImplicitOverride": true,

    /* Path Aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Step 5: Set Up Minimal Linting

Create `.eslintrc.cjs`:

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    // Connor's standards
    'no-console': 'warn',
    'no-var': 'error',
    'eqeqeq': ['error', 'always'],
  },
}
```

Create `.prettierrc`:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### Step 6: Update package.json Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx}\"",
    "preview": "vite preview"
  }
}
```

### Step 7: Initialize Git

```bash
cd {project-name}
git init
git add .
git commit -m "feat: initial Vite + React + TypeScript sandbox setup"
```

Ensure `.gitignore` includes:
```
# Dependencies
node_modules/

# Build output
dist/
dist-ssr/

# Environment
.env
.env.local
.env.*.local

# Editor
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### Step 8: Generate README

Create `README.md`:

```markdown
# {project-name}

Quick React sandbox created with Vite + TypeScript.

## Getting Started

Install dependencies:
\`\`\`bash
npm install
\`\`\`

Start development server:
\`\`\`bash
npm run dev
\`\`\`

Visit http://localhost:5173 in your browser.

## Project Structure

\`\`\`
src/
  ├── App.tsx          # Main React component
  ├── App.css          # Component styles
  ├── main.tsx         # Application entry point
  ├── index.css        # Global styles
  └── vite-env.d.ts    # Vite type definitions
\`\`\`

## Available Commands

- \`npm run dev\` - Start development server with HMR
- \`npm run build\` - Build for production
- \`npm run preview\` - Preview production build locally
- \`npm run lint\` - Check code quality
- \`npm run format\` - Format code with Prettier

## Tech Stack

- ⚡ Vite - Next generation frontend tooling
- ⚛️ React 18 - UI library
- 🔷 TypeScript - Type safety
- 🎨 ESLint + Prettier - Code quality

## Next Steps

This is a minimal sandbox. Add what you need:

- **Testing**: \`npm install -D vitest @testing-library/react jsdom\`
- **Routing**: \`npm install react-router-dom\`
- **State**: \`npm install zustand\` or \`npm install @tanstack/react-query\`
- **Styling**: \`npm install -D tailwindcss\`

## Configuration

- TypeScript strict mode is enabled
- ESLint checks for common issues
- Prettier formats on save (if editor configured)

---

Built with [react-project-scaffolder](https://github.com/yourusername/react-project-scaffolder)
```

### Step 9: Verify Setup

```bash
# Check all files were created
ls -la

# Verify package.json is valid
cat package.json | grep "vite"

# Check TypeScript config
cat tsconfig.json | grep "strict"
```

### Step 10: Provide User Instructions

**Display to user**:

```markdown
✅ Sandbox project "{project-name}" created successfully!

📁 Location: ./{project-name}

🚀 Next steps:

  1. cd {project-name}
  2. npm install
  3. npm run dev

Your dev server will start at http://localhost:5173

📚 What you have:
  ✓ Vite + React 18 + TypeScript (strict mode)
  ✓ ESLint + Prettier configured
  ✓ Git initialized with first commit
  ✓ Minimal dependencies for fast experiments

⚡ Lightning fast HMR - changes reflect instantly!

💡 Tips:
  - Edit src/App.tsx to start building
  - Add dependencies as needed
  - Run 'npm run lint' to check code quality
  - Run 'npm run format' to auto-format

🎯 This is a sandbox - keep it simple and experiment freely!
```

---

## File Structure Output

```
{project-name}/
├── .git/                   # Git repository
├── .gitignore              # Git ignore rules
├── .eslintrc.cjs           # ESLint configuration
├── .prettierrc             # Prettier configuration
├── index.html              # HTML entry point
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript config (strict)
├── tsconfig.node.json      # TypeScript for Node
├── vite.config.ts          # Vite configuration
├── README.md               # Project documentation
├── public/                 # Static assets
└── src/
    ├── App.tsx             # Main component
    ├── App.css             # Component styles
    ├── main.tsx            # Entry point
    ├── index.css           # Global styles
    ├── vite-env.d.ts       # Vite types
    └── assets/             # Images, etc.
```

---

## Success Criteria

- [ ] Vite project scaffolded successfully
- [ ] TypeScript strict mode enabled
- [ ] ESLint + Prettier configured
- [ ] Git initialized with commit
- [ ] README generated
- [ ] All files present in expected locations
- [ ] No errors in console
- [ ] Setup time < 20 seconds (excluding npm install)

---

## Troubleshooting

**Issue**: npm create vite fails
**Solution**: Update npm to latest version: `npm install -g npm@latest`

**Issue**: TypeScript errors on import
**Solution**: Check tsconfig.json has correct paths configuration

**Issue**: ESLint not working
**Solution**: Ensure .eslintrc.cjs is in root directory

**Issue**: Port 5173 already in use
**Solution**: Kill process on port or Vite will auto-increment to 5174

---

## Why This Tech Stack?

**Vite over Create React App**:
- 10-100x faster dev server startup
- Instant HMR (< 50ms)
- CRA is no longer maintained by React team
- Smaller bundle sizes
- Better TypeScript experience

**TypeScript over JavaScript**:
- Catch errors before runtime
- Better IDE autocomplete
- Connor's standard (required)
- Minimal overhead in sandbox

**ESLint + Prettier**:
- Consistent code style
- Catch common mistakes
- Quick feedback loop
- Industry standard

---

**Remember**: This mode prioritizes speed over features. Get users coding in <15 seconds!
