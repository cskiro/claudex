# React Project Scaffolder

Automated React project scaffolding with three production-ready modes: sandbox, enterprise, and mobile.

## Overview

This skill helps you quickly spin up React projects with the right tooling for your use case. Instead of manually configuring TypeScript, testing, linting, and other tools, this skill provides opinionated, production-ready setups that follow industry standards and Connor's development philosophy.

## Three Modes

### 1. Sandbox Mode (Vite + React + TypeScript)
**Best for**: Quick experiments, prototyping, learning

**Setup time**: ~15 seconds

**What you get**:
- ⚡ Vite (fastest dev server)
- ⚛️ React 18+
- 🔷 TypeScript (strict mode)
- 🎨 ESLint + Prettier (minimal config)
- 📦 Minimal dependencies

**Trigger phrases**:
- "create a React sandbox"
- "quick React setup for testing"
- "React experiment project"

### 2. Enterprise Mode (Next.js + Full Tooling)
**Best for**: Production web apps, SaaS products, enterprise dashboards

**Setup time**: ~60 seconds

**What you get**:
- ⚡ Next.js 14+ (App Router)
- ⚛️ React 18+
- 🔷 TypeScript (strict mode)
- 🧪 Vitest + React Testing Library (80% coverage)
- 🎨 ESLint + Prettier + Husky
- 🔄 GitHub Actions CI/CD
- 📚 Comprehensive documentation
- 🏆 Testing Trophy approach

**Trigger phrases**:
- "create an enterprise React project"
- "production React app with testing"
- "Next.js project with full tooling"

### 3. Mobile Mode (Expo + React Native)
**Best for**: Cross-platform mobile apps (iOS + Android)

**Setup time**: ~60 seconds

**What you get**:
- 📱 Expo SDK 50+ (managed workflow)
- 🧭 Expo Router (file-based navigation)
- 🔷 TypeScript (strict mode)
- 🧪 Jest + React Native Testing Library (80% coverage)
- 🎨 ESLint + Prettier + Husky
- 🚀 EAS Build & Submit (optional)
- 📚 Comprehensive documentation

**Trigger phrases**:
- "create a mobile React project"
- "React Native project with Expo"
- "cross-platform mobile app"

## Quick Start

Simply ask Claude Code to create a React project:

```
You: "Create a React sandbox for testing"
```

Claude will:
1. Detect the mode (sandbox, enterprise, or mobile)
2. Validate your environment (Node.js, npm)
3. Ask essential configuration questions (if needed)
4. Scaffold the complete project
5. Provide next steps and usage instructions

## Usage Examples

### Example 1: Quick Sandbox
```
You: "I need a quick React sandbox to test a feature"

Claude: "I'll create a Vite + React + TypeScript sandbox for you..."
[15 seconds later]
Claude: "✅ Done! Run: cd react-sandbox && npm install && npm run dev"
```

### Example 2: Enterprise Project
```
You: "Create an enterprise React project called my-dashboard"

Claude: "I'll set up Next.js with full tooling. Quick questions:
  - Include testing? (yes)
  - Include CI/CD? (yes)"

[60 seconds later]
Claude: "✅ Done! Your production-ready Next.js project is ready with:
  - TypeScript strict mode
  - Vitest + RTL (80% coverage)
  - ESLint + Prettier + Husky
  - GitHub Actions CI/CD"
```

### Example 3: Mobile App
```
You: "Build a mobile React app with navigation"

Claude: "I'll create an Expo project with Expo Router. Quick questions:
  - Include Expo Router for navigation? (yes)
  - Include testing? (yes)
  - Set up EAS for cloud builds? (no)"

[60 seconds later]
Claude: "✅ Done! Your Expo project is ready.
  Run: cd my-app && npm install && npm start
  Then scan the QR code with Expo Go on your phone!"
```

## What Makes This Different?

### Connor's Standards Baked In
- TypeScript strict mode (all flags enabled)
- Testing Trophy approach (70% integration, 20% unit, 10% e2e)
- 80% test coverage threshold
- No `console.log` in production code
- Pre-commit hooks for quality
- Conventional commits

### Industry Best Practices
- **Vite** for sandboxes (fastest dev experience)
- **Next.js** for enterprise (used by Netflix, TikTok)
- **Expo** for mobile (used by Instagram, Discord)
- Modern testing with Vitest/Jest + RTL
- Automated CI/CD with GitHub Actions

### Smart Automation
- Minimal questions (smart defaults)
- Fast setup (sandbox in 15s, others in 60s)
- Production-ready from day one
- Comprehensive documentation generated
- Git initialized with proper commits

## Project Structure

Each mode creates a well-organized project:

### Sandbox Structure
```
project-name/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── tsconfig.json (strict mode)
├── vite.config.ts
├── .eslintrc.cjs
└── README.md
```

### Enterprise Structure
```
project-name/
├── src/
│   ├── app/              # Next.js App Router
│   ├── components/       # React components
│   ├── lib/              # Utilities
│   └── __tests__/        # Test files
├── .github/workflows/    # CI/CD
├── .husky/               # Pre-commit hooks
├── package.json
├── tsconfig.json (strict mode)
├── vitest.config.ts
└── README.md
```

### Mobile Structure
```
project-name/
├── app/                  # Expo Router
├── components/           # React components
├── assets/               # Images, fonts
├── __tests__/            # Test files
├── package.json
├── tsconfig.json (strict mode)
├── app.json
└── README.md
```

## Configuration

The skill follows these conventions:

### TypeScript
- Strict mode enabled (all flags)
- Path aliases configured (`@/` for imports)
- Explicit return types preferred
- No `any` types allowed

### Testing
- Testing Trophy approach
- 80% coverage minimum
- Semantic queries (getByRole > getByTestId)
- Test naming: "should [behavior] when [condition]"

### Code Quality
- ESLint with strict rules
- Prettier with consistent formatting
- Husky pre-commit hooks (enterprise/mobile)
- Lint-staged (only changed files)

### Git
- Conventional commits
- Branch naming: feature/, bugfix/, chore/
- Proper .gitignore for each mode

## Prerequisites

- **Node.js**: 18.x or higher (20.x recommended)
- **npm**: 9.x or higher (10.x recommended)
- **git**: Latest version (optional but recommended)

For mobile mode:
- **iOS**: macOS with Xcode (for simulator)
- **Android**: Android Studio with emulator

## Troubleshooting

### Environment validation fails
Run the validation script manually:
```bash
~/.claude/skills/react-project-scaffolder/scripts/validate-environment.sh
```

### Node.js version too old
Update using nvm:
```bash
nvm install 18
nvm use 18
```

Or download from: https://nodejs.org/

### npm install fails
Clear cache and retry:
```bash
npm cache clean --force
npm install
```

### Expo QR code won't scan (mobile)
- Ensure phone is on same WiFi network
- Install "Expo Go" app from App Store / Play Store
- Try using tunnel mode: `npm start -- --tunnel`

## Examples

See the `examples/` directory for sample projects created with each mode:
- `examples/sandbox-output/` - Sandbox project example
- `examples/enterprise-output/` - Enterprise project example
- `examples/mobile-output/` - Mobile project example

## Technical Details

### Mode Detection
The skill uses natural language processing to detect which mode you want:
- Keywords: "sandbox", "quick", "test" → Sandbox
- Keywords: "enterprise", "production", "testing" → Enterprise
- Keywords: "mobile", "native", "ios", "android" → Mobile

### Hybrid Approach
- **Sandbox**: Fully automated (no questions)
- **Enterprise/Mobile**: 2-3 key questions with smart defaults

### Templates + Scripts
- Configuration files stored in `templates/`
- Scaffolding logic in mode definitions (`modes/`)
- Validation scripts in `scripts/`
- Dependencies reference in `data/`

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

This skill is part of Connor's personal skill collection. If you find issues or have suggestions:
1. Test the skill thoroughly
2. Document the issue with examples
3. Suggest improvements with reasoning

## License

MIT

## Credits

Built by Connor using the skill-creator skill.

Inspired by:
- Vite team (lightning-fast dev server)
- Next.js team at Vercel (production-ready React)
- Expo team (best mobile developer experience)
- Kent C. Dodds (Testing Trophy methodology)
- Connor's development standards (production-ready from day one)

---

**Ready to scaffold?** Just ask Claude Code to create a React project!
