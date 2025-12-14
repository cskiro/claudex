# Codebase Audit Criteria Checklist

This document provides a comprehensive checklist for auditing codebases based on modern software engineering best practices (2024-25).

## 1. Code Quality

### Complexity Metrics
- [ ] Cyclomatic complexity measured for all functions/methods
- [ ] Functions with complexity > 10 flagged as warnings
- [ ] Functions with complexity > 20 flagged as critical
- [ ] Cognitive complexity analyzed
- [ ] Maximum nesting depth < 4 levels
- [ ] Function/method length < 50 LOC (recommendation)
- [ ] File length < 500 LOC (recommendation)

### Code Duplication
- [ ] Duplication analysis performed (minimum 6-line blocks)
- [ ] Overall duplication < 5%
- [ ] Duplicate blocks identified with locations
- [ ] Opportunities for abstraction documented

### Code Smells
- [ ] God objects/classes identified (> 10 public methods)
- [ ] Feature envy detected (high coupling to other classes)
- [ ] Dead code identified (unused imports, variables, functions)
- [ ] Magic numbers replaced with named constants
- [ ] Hard-coded values moved to configuration
- [ ] Naming conventions consistent
- [ ] Error handling comprehensive
- [ ] No console.log in production code
- [ ] No commented-out code blocks

### Language-Specific (TypeScript/JavaScript)
- [ ] No use of `any` type (strict mode)
- [ ] No use of `var` keyword
- [ ] Strict equality (`===`) used consistently
- [ ] Return type annotations present for functions
- [ ] Non-null assertions justified with comments
- [ ] Async/await preferred over Promise chains
- [ ] No implicit any returns

## 2. Testing & Coverage

### Coverage Metrics
- [ ] Line coverage >= 80%
- [ ] Branch coverage >= 75%
- [ ] Function coverage >= 90%
- [ ] Critical paths have 100% coverage (auth, payment, data processing)
- [ ] Coverage reports generated and accessible

### Testing Trophy Distribution
- [ ] Integration tests: ~70% of total tests
- [ ] Unit tests: ~20% of total tests
- [ ] E2E tests: ~10% of total tests
- [ ] Actual distribution documented

### Test Quality
- [ ] Tests follow "should X when Y" naming pattern
- [ ] Tests are isolated and independent
- [ ] No tests of implementation details (brittle tests)
- [ ] Single assertion per test (or grouped related assertions)
- [ ] Edge cases covered
- [ ] No flaky tests
- [ ] Tests use semantic queries (getByRole, getByLabelText)
- [ ] Avoid testing emoji presence, exact DOM counts, element ordering

### Test Performance
- [ ] Tests complete in < 30 seconds (unit/integration)
- [ ] CPU usage monitored (use `npm run test:low -- --run`)
- [ ] No runaway test processes
- [ ] Tests run in parallel where possible
- [ ] Max threads limited to prevent CPU overload

## 3. Security

### Dependency Vulnerabilities
- [ ] No critical CVEs in dependencies
- [ ] No high-severity CVEs in dependencies
- [ ] All dependencies using supported versions
- [ ] No dependencies unmaintained for > 2 years
- [ ] License compliance verified
- [ ] No dependency confusion risks

### OWASP Top 10 (2024)
- [ ] Access control properly implemented
- [ ] Sensitive data encrypted at rest and in transit
- [ ] Input validation prevents injection attacks
- [ ] Security design patterns followed
- [ ] Security configuration reviewed (no defaults)
- [ ] All components up-to-date
- [ ] Authentication robust (MFA, rate limiting)
- [ ] Software integrity verified (SRI, signatures)
- [ ] Security logging and monitoring enabled
- [ ] SSRF protections in place

### Secrets Management
- [ ] No API keys in code
- [ ] No tokens in code
- [ ] No passwords in code
- [ ] No private keys committed
- [ ] Environment variables properly used
- [ ] No secrets in client-side code
- [ ] .env files in .gitignore
- [ ] Git history clean of secrets

### Security Best Practices
- [ ] Input validation on all user inputs
- [ ] Output encoding prevents XSS
- [ ] CSRF tokens implemented
- [ ] Secure session management
- [ ] HTTPS enforced
- [ ] CSP headers configured
- [ ] Rate limiting on APIs
- [ ] SQL prepared statements used

## 4. Architecture & Design

### SOLID Principles
- [ ] Single Responsibility: Classes/modules have one reason to change
- [ ] Open/Closed: Open for extension, closed for modification
- [ ] Liskov Substitution: Subtypes are substitutable for base types
- [ ] Interface Segregation: Clients not forced to depend on unused methods
- [ ] Dependency Inversion: Depend on abstractions, not concretions

### Design Patterns
- [ ] Appropriate patterns used (Factory, Strategy, Observer, etc.)
- [ ] No anti-patterns (Singleton abuse, God Object, etc.)
- [ ] Not over-engineered
- [ ] Not under-engineered

### Modularity
- [ ] Low coupling between modules
- [ ] High cohesion within modules
- [ ] No circular dependencies
- [ ] Proper separation of concerns
- [ ] Clean public APIs
- [ ] Internal implementation details hidden

## 5. Performance

### Build Performance
- [ ] Build time < 2 minutes for typical project
- [ ] Bundle size documented and optimized
- [ ] Code splitting implemented
- [ ] Tree-shaking enabled
- [ ] Source maps configured correctly
- [ ] Production build optimized

### Runtime Performance
- [ ] No memory leaks
- [ ] Algorithms efficient (avoid O(n²) where possible)
- [ ] No excessive re-renders (React/Vue)
- [ ] Computations memoized where appropriate
- [ ] Images optimized (< 200KB)
- [ ] Videos optimized or lazy-loaded
- [ ] Lazy loading for large components

### CI/CD Performance
- [ ] Pipeline runs in < 10 minutes
- [ ] Deployment frequency documented
- [ ] Test execution time < 5 minutes
- [ ] Docker images < 500MB (if applicable)

## 6. Documentation

### Code Documentation
- [ ] Public APIs documented (JSDoc/TSDoc)
- [ ] Complex logic has inline comments
- [ ] README.md comprehensive
- [ ] Architecture Decision Records (ADRs) present
- [ ] API documentation available
- [ ] CONTRIBUTING.md exists
- [ ] CODE_OF_CONDUCT.md exists

### Documentation Maintenance
- [ ] No outdated documentation
- [ ] No broken links
- [ ] All sections complete
- [ ] Code examples work correctly
- [ ] Changelog maintained

## 7. DevOps & CI/CD

### CI/CD Maturity
- [ ] Automated testing in pipeline
- [ ] Automated deployment configured
- [ ] Development/staging/production environments
- [ ] Rollback capability exists
- [ ] Feature flags used for risky changes
- [ ] Blue-green or canary deployments

### DORA 4 Metrics
- [ ] Deployment frequency measured
  - Elite: Multiple times per day
  - High: Once per day to once per week
  - Medium: Once per week to once per month
  - Low: Less than once per month
- [ ] Lead time for changes measured
  - Elite: Less than 1 hour
  - High: 1 day to 1 week
  - Medium: 1 week to 1 month
  - Low: More than 1 month
- [ ] Change failure rate measured
  - Elite: < 1%
  - High: 1-5%
  - Medium: 5-15%
  - Low: > 15%
- [ ] Time to restore service measured
  - Elite: < 1 hour
  - High: < 1 day
  - Medium: 1 day to 1 week
  - Low: > 1 week

### Infrastructure as Code
- [ ] Configuration managed as code
- [ ] Infrastructure versioned
- [ ] Secrets managed securely (Vault, AWS Secrets Manager)
- [ ] Environment variables documented

## 8. Accessibility (WCAG 2.1 AA)

### Semantic HTML
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] ARIA labels where needed
- [ ] Form labels associated with inputs
- [ ] Landmark regions defined (header, nav, main, footer)

### Keyboard Navigation
- [ ] All interactive elements keyboard accessible
- [ ] Focus management implemented
- [ ] Tab order logical
- [ ] Focus indicators visible

### Screen Reader Support
- [ ] Images have alt text
- [ ] ARIA live regions for dynamic content
- [ ] Links have descriptive text
- [ ] Form errors announced

### Color & Contrast
- [ ] Text contrast >= 4.5:1 (normal text)
- [ ] Text contrast >= 3:1 (large text 18pt+)
- [ ] UI components contrast >= 3:1
- [ ] Color not sole means of conveying information

## 9. Technical Debt

### SQALE Rating
- [ ] Technical debt quantified in person-days
- [ ] Rating assigned (A-E)
  - A: <= 5% of development time
  - B: 6-10%
  - C: 11-20%
  - D: 21-50%
  - E: > 50%

### Debt Categories
- [ ] Code smell debt identified
- [ ] Test debt quantified
- [ ] Documentation debt listed
- [ ] Security debt prioritized
- [ ] Performance debt noted
- [ ] Architecture debt evaluated

## 10. Project-Specific Standards

### Connor's Global Standards
- [ ] TypeScript strict mode enabled
- [ ] No `any` types
- [ ] Explicit return types
- [ ] Comprehensive error handling
- [ ] 80%+ test coverage
- [ ] No console.log statements
- [ ] No `var` keyword
- [ ] No loose equality (`==`)
- [ ] Conventional commits format
- [ ] Branch naming follows pattern: (feature|bugfix|chore)/{component-name}

## Audit Completion

### Final Checks
- [ ] All critical issues identified
- [ ] All high-severity issues documented
- [ ] Severity assigned to each finding
- [ ] Remediation effort estimated
- [ ] Report generated
- [ ] Remediation plan created
- [ ] Stakeholders notified

---

**Note**: This checklist is based on industry best practices as of 2024-25. Adjust severity thresholds and criteria based on your project's maturity stage and business context.
