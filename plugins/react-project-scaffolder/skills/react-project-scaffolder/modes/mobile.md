# Mode 3: Mobile (Expo + React Native)

**Purpose**: Cross-platform mobile apps with production-ready tooling

**Setup Time**: ~60 seconds after `npm install`

## Tech Stack
- Expo SDK 50+ (managed workflow)
- React Native (latest stable)
- TypeScript (strict mode)
- Jest + React Native Testing Library
- ESLint + Prettier + Husky
- EAS Build (optional)

**Configuration Strategy**: 2-3 key questions, smart defaults

## Configuration Questions

1. "Include testing setup?" (default: yes)
2. "Include CI/CD for EAS?" (default: no)
3. "Navigation library?" (default: Expo Router)

## Workflow Steps

### 1. Scaffold with Expo
```bash
npx create-expo-app {project-name} --template expo-template-blank-typescript
cd {project-name}
```

### 2. Apply TypeScript Strict Mode
- Update tsconfig.json with strict settings
- Configure path aliases for React Native
- Enable all type checking flags

### 3. Set Up Testing (if selected)
- Install Jest, React Native Testing Library
- Create jest.config.js for React Native
- Add example test
- Configure 80% coverage threshold
- Add test scripts:
  ```json
  "test": "jest --maxWorkers=2",
  "test:watch": "jest --watch",
  "test:coverage": "jest --coverage"
  ```

### 4. Configure Linting & Formatting
- Install ESLint with React Native rules
- Add Prettier configuration
- Set up Husky + lint-staged
- Configure pre-commit hooks

### 5. Set Up Navigation (Expo Router)
```bash
npx expo install expo-router
```
- Create app/ directory structure
- Set up root layout
- Add example screens

### 6. Initialize Git
```bash
git init
git add .
git commit -m "feat: initial Expo + React Native setup"
```

### 7. Provide Next Steps

```markdown
## Your Mobile Project is Ready!

Start development:
  cd {project-name}
  npm install
  npx expo start

Project structure:
  app/
    ├── _layout.tsx       # Root layout
    ├── index.tsx         # Home screen
    └── [screen].tsx      # Dynamic routes
  components/             # Reusable components
  __tests__/              # Test files

Available commands:
  npx expo start         # Start development
  npx expo start --ios   # iOS simulator
  npx expo start --android  # Android emulator
  npm run test           # Run tests
  npm run lint           # Lint code

Configured features:
  ✓ TypeScript strict mode
  ✓ Expo Router navigation
  ✓ Jest + RNTL testing
  ✓ ESLint + Prettier
  ✓ 80% coverage threshold

Next steps:
  1. Run on device: npx expo start --tunnel
  2. Add more screens in app/
  3. Configure app.json for store submission
  4. Set up EAS Build for production
```

## When to Use

- Cross-platform iOS/Android apps
- Quick mobile prototypes
- Apps using Expo managed workflow
- Teams familiar with React wanting mobile
