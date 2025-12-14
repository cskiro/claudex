# Bulletproof React Audit Criteria

Complete checklist for auditing React/TypeScript applications against Bulletproof React architecture principles.

## 1. Project Structure

### Feature-Based Organization
- [ ] 80%+ of code organized in src/features/
- [ ] Each feature has its own directory
- [ ] Features are independent (no cross-feature imports)
- [ ] Feature subdirectories: api/, components/, hooks/, stores/, types/, utils/

### Top-Level Directories
- [ ] src/app/ exists (application layer)
- [ ] src/features/ exists and contains features
- [ ] src/components/ for truly shared components only
- [ ] src/hooks/ for shared custom hooks
- [ ] src/lib/ for third-party configurations
- [ ] src/utils/ for shared utilities
- [ ] src/types/ for shared TypeScript types
- [ ] src/stores/ for global state (if needed)

### Unidirectional Dependencies
- [ ] No cross-feature imports
- [ ] Shared code imported into features (not vice versa)
- [ ] App layer imports from features
- [ ] Clean dependency flow: shared → features → app

## 2. Component Architecture

### Component Design
- [ ] Components < 300 lines of code
- [ ] No large components (> 500 LOC)
- [ ] Components accept < 7-10 props
- [ ] No nested render functions
- [ ] Component colocation (near where used)
- [ ] Proper use of composition over excessive props

### File Organization
- [ ] Kebab-case file naming
- [ ] Components colocated with tests
- [ ] Styles colocated with components
- [ ] Feature-specific components in features/
- [ ] Only truly shared components in src/components/

### Abstraction
- [ ] No premature abstractions
- [ ] Repetition identified before creating abstractions
- [ ] Components are focused and single-purpose

## 3. State Management

### State Categories
- [ ] Component state with useState/useReducer
- [ ] Global state with Context, Zustand, or Jotai
- [ ] Server cache state with React Query or SWR
- [ ] Form state with React Hook Form or Formik
- [ ] URL state with React Router

### State Localization
- [ ] State as local as possible
- [ ] Global state only when necessary
- [ ] No single massive global state object
- [ ] Context split into multiple focused providers

### Server State
- [ ] React Query or SWR for API data
- [ ] Proper caching configuration
- [ ] No manual loading/error state for API calls
- [ ] Optimistic updates where appropriate

## 4. API Layer

### Centralized Configuration
- [ ] Single API client instance
- [ ] Configured in src/lib/
- [ ] Base URL configuration
- [ ] Request/response interceptors
- [ ] Error handling interceptors

### Request Organization
- [ ] API calls colocated in features/*/api/
- [ ] Type-safe request declarations
- [ ] Custom hooks for each endpoint
- [ ] Validation schemas with types
- [ ] Proper error handling

## 5. Testing Strategy

### Coverage
- [ ] 80%+ line coverage
- [ ] 75%+ branch coverage
- [ ] 100% coverage on critical paths
- [ ] Coverage reports generated

### Testing Trophy Distribution
- [ ] ~70% integration tests
- [ ] ~20% unit tests
- [ ] ~10% E2E tests

### Test Quality
- [ ] Tests named "should X when Y"
- [ ] Semantic queries (getByRole, getByLabelText)
- [ ] Testing user behavior, not implementation
- [ ] No brittle tests (exact counts, element ordering)
- [ ] Tests isolated and independent
- [ ] No flaky tests

### Testing Tools
- [ ] Vitest or Jest configured
- [ ] @testing-library/react installed
- [ ] @testing-library/jest-dom for assertions
- [ ] Playwright or Cypress for E2E (optional)

## 6. Styling Patterns

### Styling Approach
- [ ] Consistent styling method chosen
- [ ] Component library (Chakra, Radix, MUI) OR
- [ ] Utility CSS (Tailwind) OR
- [ ] CSS-in-JS (Emotion, styled-components)
- [ ] Styles colocated with components

### Design System
- [ ] Design tokens defined
- [ ] Color palette established
- [ ] Typography scale defined
- [ ] Spacing system consistent

## 7. Error Handling

### Error Boundaries
- [ ] Multiple error boundaries at strategic locations
- [ ] Route-level error boundaries
- [ ] Feature-level error boundaries
- [ ] User-friendly error messages
- [ ] Error recovery mechanisms

### API Errors
- [ ] API error interceptors configured
- [ ] User notifications for errors
- [ ] Automatic retry logic where appropriate
- [ ] Unauthorized user logout

### Error Tracking
- [ ] Sentry or similar service configured
- [ ] User context added to errors
- [ ] Environment-specific error handling
- [ ] Source maps configured for production

## 8. Performance

### Code Splitting
- [ ] React.lazy() for route components
- [ ] Suspense boundaries with loading states
- [ ] Large features split into chunks
- [ ] Bundle size monitored and optimized

### React Performance
- [ ] State localized to prevent re-renders
- [ ] React.memo for expensive components
- [ ] useMemo for expensive calculations
- [ ] useCallback for stable function references
- [ ] Children prop optimization patterns

### Asset Optimization
- [ ] Images lazy loaded
- [ ] Images in modern formats (WebP)
- [ ] Responsive images with srcset
- [ ] Images < 500KB
- [ ] Videos lazy loaded or streamed

## 9. Security

### Authentication
- [ ] JWT stored in HttpOnly cookies (not localStorage)
- [ ] Secure session management
- [ ] Token refresh logic
- [ ] Logout functionality

### Authorization
- [ ] RBAC or PBAC implemented
- [ ] Protected routes
- [ ] Permission checks on actions
- [ ] API-level authorization

### XSS Prevention
- [ ] Input sanitization (DOMPurify)
- [ ] No dangerouslySetInnerHTML without sanitization
- [ ] Output encoding
- [ ] Content Security Policy

### CSRF Protection
- [ ] CSRF tokens for state-changing requests
- [ ] SameSite cookie attribute
- [ ] Verify origin headers

## 10. Standards Compliance

### ESLint
- [ ] .eslintrc or eslint.config.js configured
- [ ] React rules enabled
- [ ] TypeScript rules enabled
- [ ] Accessibility rules (jsx-a11y)
- [ ] Architectural rules (import restrictions)

### TypeScript
- [ ] strict: true in tsconfig.json
- [ ] No `any` types
- [ ] Explicit return types
- [ ] Type definitions for third-party libraries
- [ ] Types colocated with features

### Prettier
- [ ] Prettier configured
- [ ] Format on save enabled
- [ ] Consistent code style
- [ ] .prettierrc configuration

### Git Hooks
- [ ] Husky configured
- [ ] Pre-commit linting
- [ ] Pre-commit type checking
- [ ] Pre-commit tests (optional)

### File Naming
- [ ] Kebab-case for files and directories
- [ ] Consistent naming conventions
- [ ] ESLint rule to enforce naming

### Absolute Imports
- [ ] TypeScript paths configured (@/ prefix)
- [ ] Imports use @/ instead of relative paths
- [ ] Easier refactoring and moving files

## Compliance Scoring

### Grade Scale
- **A (90-100)**: Excellent Bulletproof React compliance
- **B (80-89)**: Good compliance, minor improvements needed
- **C (70-79)**: Moderate compliance, significant refactoring recommended
- **D (60-69)**: Poor compliance, major architectural changes needed
- **F (<60)**: Non-compliant, complete restructuring required

### Category Weights
All categories weighted equally for overall score.

---

**Note**: This checklist represents the ideal Bulletproof React architecture. Adapt based on your project's specific needs and constraints while maintaining the core principles.
