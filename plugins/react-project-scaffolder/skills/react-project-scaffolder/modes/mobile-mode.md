# Mobile Mode - Expo + React Native

## Mode Overview

**Purpose**: Cross-platform mobile applications with production-ready tooling

**Target Users**:
- Building iOS and Android apps from single codebase
- Mobile-first products and services
- Teams wanting native performance with React
- Startups needing fast mobile development
- Enterprise mobile applications

**Setup Time**: ~60 seconds (after npm install)

**Philosophy**: Native performance, React developer experience, production standards from day one.

---

## Tech Stack

```yaml
Framework:
  - Expo SDK 50+ (managed workflow)
  - React Native (latest stable)
  - TypeScript 5+ (strict mode)

Navigation:
  - Expo Router (file-based routing)
  - React Navigation (under the hood)

Testing:
  - Jest (React Native default)
  - React Native Testing Library
  - 80% coverage threshold

Code Quality:
  - ESLint (React Native rules)
  - Prettier (consistent formatting)
  - Husky (pre-commit hooks)
  - lint-staged (staged files only)

Build & Deploy:
  - EAS Build (cloud builds - optional)
  - EAS Submit (app store submission - optional)
  - OTA Updates (instant updates)

Standards:
  - Conventional Commits
  - TypeScript strict mode
  - Testing Trophy approach
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

# Check if Expo CLI is needed (will be installed via npx)
echo "Expo CLI will be used via npx"
```

**If validation fails**: Provide upgrade instructions

### Step 2: Ask Configuration Questions

Only essential questions with smart defaults:

**Question 1: Project Name**
- "What should I name your mobile project?"
- Validation: kebab-case or PascalCase, 3-50 chars
- Example: my-awesome-app or MyAwesomeApp

**Question 2: Navigation Setup**
- "Include Expo Router for navigation?"
- Default: YES
- Explain: "File-based routing like Next.js. Recommended for most apps."

**Question 3: Testing Setup**
- "Include testing infrastructure? (Jest + RN Testing Library)"
- Default: YES
- Explain: "Recommended for production apps. Connor's 80% coverage standard."

**Question 4: EAS Cloud Builds**
- "Set up EAS for cloud builds and app store submission?"
- Default: NO (can add later)
- Explain: "Requires Expo account. Can configure later when ready to deploy."

### Step 3: Scaffold with Expo

```bash
npx create-expo-app@latest {project-name} --template blank-typescript
cd {project-name}
```

**Why Expo?**
- Used by Instagram, Discord, Shopify
- Fastest mobile development experience
- Built-in access to native APIs
- Over-the-air (OTA) updates
- Managed workflow (easier) or bare workflow (more control)

### Step 4: Install Expo Router (if selected)

```bash
npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants expo-status-bar
```

Update `package.json`:

```json
{
  "main": "expo-router/entry"
}
```

Create `app/_layout.tsx`:

```typescript
import { Stack } from 'expo-router';

export default function RootLayout() {
  return <Stack />;
}
```

Create `app/index.tsx`:

```typescript
import { View, Text, StyleSheet } from 'react-native';

export default function Home() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to {project-name}</Text>
      <Text style={styles.subtitle}>
        Edit app/index.tsx to get started
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
});
```

Update `app.json`:

```json
{
  "expo": {
    "name": "{project-name}",
    "slug": "{project-name}",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "scheme": "{project-name}",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.{username}.{project-name}"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.{username}.{project-name}"
    },
    "web": {
      "bundler": "metro",
      "favicon": "./assets/favicon.png"
    },
    "plugins": ["expo-router"]
  }
}
```

### Step 5: Configure TypeScript (Strict Mode)

Update `tsconfig.json`:

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noImplicitOverride": true,
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"],
  "exclude": ["node_modules"]
}
```

### Step 6: Set Up Testing (if selected)

**6.1 Install Dependencies**

```bash
npm install -D jest jest-expo @testing-library/react-native @testing-library/jest-native @types/jest
```

**6.2 Create `jest.config.js`**

```javascript
module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: ['<rootDir>/__tests__/setup.ts'],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)',
  ],
  collectCoverageFrom: [
    '**/*.{ts,tsx}',
    '!**/coverage/**',
    '!**/node_modules/**',
    '!**/babel.config.js',
    '!**/jest.config.js',
    '!**/__tests__/**',
  ],
  coverageThreshold: {
    global: {
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
};
```

**6.3 Create Test Setup**

`__tests__/setup.ts`:

```typescript
import '@testing-library/jest-native/extend-expect';

// Mock Expo modules
jest.mock('expo-font');
jest.mock('expo-asset');

// Silence console warnings in tests
global.console = {
  ...console,
  warn: jest.fn(),
  error: jest.fn(),
};
```

**6.4 Create Example Test**

`__tests__/App.test.tsx`:

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react-native';
import Home from '../app/index';

describe('Home Screen', () => {
  it('should render welcome message when app loads', () => {
    render(<Home />);

    // Testing Trophy approach: Test user-visible behavior
    expect(screen.getByText(/welcome to/i)).toBeTruthy();
  });

  it('should display instructions for getting started', () => {
    render(<Home />);

    expect(screen.getByText(/edit app\/index.tsx/i)).toBeTruthy();
  });
});
```

**6.5 Update package.json Scripts**

```json
{
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "test": "jest --passWithNoTests",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint . --ext .ts,.tsx",
    "type-check": "tsc --noEmit"
  }
}
```

### Step 7: Configure Code Quality Tools

**7.1 Set Up ESLint**

```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-react eslint-plugin-react-native
```

Create `.eslintrc.js`:

```javascript
module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-native/all',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'react', 'react-native'],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  env: {
    'react-native/react-native': true,
  },
  rules: {
    // Connor's standards
    'no-console': 'warn',
    'no-var': 'error',
    'eqeqeq': ['error', 'always'],
    'prefer-const': 'error',
    '@typescript-eslint/no-unused-vars': [
      'error',
      { argsIgnorePattern: '^_' },
    ],
    '@typescript-eslint/no-explicit-any': 'error',
    'react/react-in-jsx-scope': 'off', // Not needed in React Native
    'react-native/no-inline-styles': 'warn',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

**7.2 Add Prettier**

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

Install Prettier:

```bash
npm install -D prettier eslint-config-prettier
```

**7.3 Set Up Husky + lint-staged**

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
    () => 'tsc --noEmit',
    'jest --bail --findRelatedTests --passWithNoTests',
  ],
  '*.{json,md}': ['prettier --write'],
};
```

### Step 8: Optional EAS Configuration (if selected)

```bash
# Install EAS CLI globally
npm install -g eas-cli

# Login to Expo
eas login

# Configure EAS Build
eas build:configure
```

This creates `eas.json`:

```json
{
  "cli": {
    "version": ">= 5.9.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {}
  }
}
```

### Step 9: Create Project Documentation

**Update README.md**:

```markdown
# {project-name}

Cross-platform mobile application built with Expo and React Native.

## Features

- 📱 React Native (iOS + Android from single codebase)
- ⚡ Expo SDK 50+ (managed workflow)
- 🧭 Expo Router (file-based navigation)
- 🔷 TypeScript (strict mode)
- 🧪 Testing Trophy approach (Jest + RN Testing Library)
- ✅ 80% test coverage threshold
- 🎨 ESLint + Prettier
- 🪝 Husky pre-commit hooks
- 🚀 EAS Build & Submit (optional)

## Getting Started

### Prerequisites

- Node.js 18+
- npm 9+
- iOS Simulator (Mac only) or Android Emulator
- Expo Go app on physical device (optional)

### Installation

\`\`\`bash
npm install
\`\`\`

### Development

\`\`\`bash
npm start
\`\`\`

This opens the Expo Dev Server. From there:

- Press **i** to open iOS simulator
- Press **a** to open Android emulator
- Scan QR code with Expo Go app on your phone

Or run directly:

\`\`\`bash
npm run ios       # iOS simulator
npm run android   # Android emulator
npm run web       # Web browser
\`\`\`

## Project Structure

\`\`\`
app/                        # Expo Router (file-based routing)
  ├── _layout.tsx           # Root layout
  ├── index.tsx             # Home screen
  └── (tabs)/               # Tab navigation (if using)
components/                 # Reusable components
  ├── ui/                   # UI components
  └── features/             # Feature components
__tests__/                  # Test files
  ├── setup.ts              # Test configuration
  └── App.test.tsx          # Example test
assets/                     # Images, fonts, etc.
  ├── icon.png
  ├── splash.png
  └── adaptive-icon.png
\`\`\`

## Available Commands

### Development
- \`npm start\` - Start Expo dev server
- \`npm run ios\` - Run on iOS simulator
- \`npm run android\` - Run on Android emulator
- \`npm run web\` - Run in web browser

### Code Quality
- \`npm run lint\` - Lint code with ESLint
- \`npm run type-check\` - Check TypeScript types

### Testing
- \`npm test\` - Run all tests
- \`npm run test:watch\` - Run tests in watch mode
- \`npm run test:coverage\` - Run tests with coverage report

### Build & Deploy (if EAS configured)
- \`eas build --platform ios\` - Build for iOS
- \`eas build --platform android\` - Build for Android
- \`eas build --platform all\` - Build for both platforms
- \`eas submit --platform ios\` - Submit to App Store
- \`eas submit --platform android\` - Submit to Play Store

## Testing Strategy

This project follows the **Testing Trophy** approach:

- **70% Integration Tests**: User workflows and component interactions
- **20% Unit Tests**: Complex business logic
- **10% E2E Tests**: Critical user journeys (use Detox or Maestro)

### Writing Tests

Test file naming: \`[component-name].test.tsx\`

\`\`\`typescript
import { render, screen, fireEvent } from '@testing-library/react-native';

describe('LoginScreen', () => {
  it('should submit form when user enters valid credentials', () => {
    const onSubmit = jest.fn();
    render(<LoginScreen onSubmit={onSubmit} />);

    fireEvent.changeText(screen.getByPlaceholderText('Email'), 'test@example.com');
    fireEvent.changeText(screen.getByPlaceholderText('Password'), 'password123');
    fireEvent.press(screen.getByText('Login'));

    expect(onSubmit).toHaveBeenCalled();
  });
});
\`\`\`

## Navigation with Expo Router

File-based routing like Next.js:

\`\`\`
app/
  ├── _layout.tsx          → Root layout
  ├── index.tsx            → / (home)
  ├── about.tsx            → /about
  ├── users/
  │   ├── [id].tsx         → /users/:id (dynamic)
  │   └── index.tsx        → /users
  └── (tabs)/              → Tab navigation group
      ├── _layout.tsx
      ├── home.tsx
      └── profile.tsx
\`\`\`

Navigate programmatically:

\`\`\`typescript
import { router } from 'expo-router';

router.push('/about');
router.replace('/login');
router.back();
\`\`\`

## Environment Variables

Create \`.env\`:

\`\`\`env
API_URL=https://api.example.com
\`\`\`

Install and configure:

\`\`\`bash
npm install react-native-dotenv
\`\`\`

## Building for Production

### With EAS (Recommended)

\`\`\`bash
# Build for iOS (requires Apple Developer account)
eas build --platform ios --profile production

# Build for Android (requires Google Play Console account)
eas build --platform android --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android
\`\`\`

### Local Builds

\`\`\`bash
# iOS (requires Mac + Xcode)
npx expo run:ios --configuration Release

# Android
npx expo run:android --variant release
\`\`\`

## Over-the-Air (OTA) Updates

Expo allows instant updates without app store review:

\`\`\`bash
# Publish update to production
eas update --branch production --message "Bug fixes"

# Users get update on next app restart
\`\`\`

## Deployment Checklist

- [ ] Update \`version\` in app.json
- [ ] Test on physical iOS device
- [ ] Test on physical Android device
- [ ] Run full test suite: \`npm run test:coverage\`
- [ ] Check bundle size: \`npx expo export\`
- [ ] Update app screenshots
- [ ] Build for production: \`eas build --platform all\`
- [ ] Test production builds
- [ ] Submit to stores: \`eas submit --platform all\`

## Common Issues

### Metro bundler cache issues
\`\`\`bash
npm start -- --clear
\`\`\`

### iOS simulator not opening
\`\`\`bash
sudo xcode-select -s /Applications/Xcode.app
\`\`\`

### Android emulator issues
- Ensure Android Studio is installed
- Check emulator is running: \`adb devices\`

## Resources

- [Expo Documentation](https://docs.expo.dev)
- [Expo Router](https://docs.expo.dev/router/introduction/)
- [React Native Testing Library](https://callstack.github.io/react-native-testing-library/)
- [EAS Build](https://docs.expo.dev/build/introduction/)

## License

MIT

---

Built with [react-project-scaffolder](https://github.com/yourusername/react-project-scaffolder)
```

### Step 10: Initialize Git

```bash
git init
git add .
git commit -m "feat: initial Expo + React Native setup with testing

- Expo SDK 50+ with managed workflow
- Expo Router for navigation
- TypeScript strict mode
- Jest + React Native Testing Library (80% coverage)
- ESLint + Prettier + Husky
- EAS configuration (optional)
- Comprehensive documentation"
```

Ensure `.gitignore` includes:

```
node_modules/
.expo/
dist/
npm-debug.*
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*
web-build/

# macOS
.DS_Store

# Environment
.env
.env.local

# Testing
coverage/
```

### Step 11: Verify Setup

```bash
# Verify all files
ls -la

# Check Expo installation
npx expo --version

# Verify tests run
npm test

# Start Expo dev server (verify it works)
npm start
```

### Step 12: Provide User Instructions

**Display to user**:

```markdown
✅ Mobile project "{project-name}" created successfully!

📁 Location: ./{project-name}

🚀 Next steps:

  1. cd {project-name}
  2. npm install
  3. npm start

Then:
  - Press 'i' for iOS simulator
  - Press 'a' for Android emulator
  - Scan QR code with Expo Go app on your phone

📚 What you have:
  ✓ Expo SDK 50+ (managed workflow)
  ✓ Expo Router (file-based navigation)
  ✓ TypeScript strict mode
  ✓ Jest + React Native Testing Library (80% coverage)
  ✓ ESLint + Prettier + Husky
  ✓ EAS Build configuration (if selected)
  ✓ OTA update support
  ✓ Comprehensive documentation

🧪 Test your setup:
  npm test           # Run all tests
  npm run lint       # Check code quality
  npm run type-check # Verify types

📱 Running on devices:
  - Install "Expo Go" app from App Store / Play Store
  - Scan QR code from terminal
  - See changes instantly with Fast Refresh

🔄 Pre-commit hooks active:
  - Linting (auto-fix)
  - Formatting (auto-format)
  - Type checking
  - Related tests run automatically

📦 Build for production (if EAS configured):
  eas build --platform all
  eas submit --platform all

💡 Tips:
  - Use Expo Router for navigation (like Next.js)
  - Test on physical devices early and often
  - Use EAS for cloud builds (no Xcode/Android Studio needed)
  - OTA updates allow instant bug fixes without app store review

📖 Documentation:
  - README.md - Complete guide with all commands
  - Expo docs: https://docs.expo.dev

🎯 Production-ready mobile development!
```

---

## File Structure Output

```
{project-name}/
├── .husky/
│   └── pre-commit              # Pre-commit hooks
├── app/
│   ├── _layout.tsx             # Root layout (Expo Router)
│   └── index.tsx               # Home screen
├── assets/
│   ├── icon.png                # App icon
│   ├── splash.png              # Splash screen
│   └── adaptive-icon.png       # Android adaptive icon
├── components/
│   ├── ui/                     # UI components
│   └── features/               # Feature components
├── __tests__/
│   ├── setup.ts                # Test setup
│   └── App.test.tsx            # Example test
├── .eslintrc.js                # ESLint config
├── .prettierrc                 # Prettier config
├── .gitignore                  # Git ignore
├── .lintstagedrc.js            # lint-staged config
├── jest.config.js              # Jest config
├── tsconfig.json               # TypeScript config
├── app.json                    # Expo config
├── package.json                # Dependencies
├── eas.json                    # EAS Build config (if configured)
└── README.md                   # Documentation
```

---

## Success Criteria

- [ ] Expo project scaffolded successfully
- [ ] Expo Router configured (if selected)
- [ ] TypeScript strict mode enabled
- [ ] Jest + RN Testing Library configured
- [ ] Example test passes
- [ ] ESLint + Prettier configured
- [ ] Husky pre-commit hooks working
- [ ] EAS configured (if selected)
- [ ] README generated
- [ ] Git initialized with commit
- [ ] `npm start` opens Expo Dev Server
- [ ] QR code displays for device testing
- [ ] Setup time < 90 seconds (excluding npm install)

---

## Troubleshooting

**Issue**: Expo CLI not found
**Solution**: Use npx: `npx expo start`

**Issue**: Metro bundler cache issues
**Solution**: Clear cache: `npm start -- --clear`

**Issue**: Tests fail with React Native module errors
**Solution**: Check jest.config.js transformIgnorePatterns

**Issue**: iOS simulator won't open
**Solution**: Set Xcode path: `sudo xcode-select -s /Applications/Xcode.app`

**Issue**: Android emulator not detected
**Solution**: Check ADB: `adb devices`, ensure emulator is running

**Issue**: EAS build fails
**Solution**: Check credentials and app config in app.json

---

## Why This Tech Stack?

**Expo over bare React Native**:
- Faster development (managed workflow)
- Built-in access to native APIs
- OTA updates (instant bug fixes)
- Used by Instagram, Discord, Shopify
- Easier for beginners, powerful for pros

**Expo Router over React Navigation**:
- File-based routing (like Next.js)
- Better TypeScript support
- Deep linking built-in
- Less boilerplate

**EAS Build over local builds**:
- No need for Xcode/Android Studio
- Cloud-based builds
- Consistent environments
- Easy team collaboration

---

**Remember**: This mode delivers native mobile performance with React developer experience. Production-ready with Connor's standards applied to mobile development.
