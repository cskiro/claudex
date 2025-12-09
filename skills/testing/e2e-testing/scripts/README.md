# Helper Scripts

These scripts provide reference implementations for automating Playwright e2e testing workflows. They are meant to guide LLM implementation, not to be executed directly.

## Script Overview

### 1. `setup-playwright.sh`
**Purpose**: Automate Playwright installation and initial configuration

**What it does**:
- Checks Node.js version compatibility
- Installs Playwright via npm
- Installs browser binaries (Chromium, Firefox, WebKit)
- Generates initial playwright.config.ts
- Creates test directory structure

**Usage Pattern** (for LLM to implement):
```bash
#!/bin/bash
# Detect if Playwright is already installed
# If not, run: npm init playwright@latest -- --yes
# Create directory structure
# Generate config based on detected framework
```

### 2. `detect-framework.ts`
**Purpose**: Identify application framework and configuration

**What it does**:
- Reads package.json dependencies
- Checks for config files (vite.config.ts, next.config.js, etc.)
- Determines dev server command and port
- Returns framework metadata for test generation

**Usage Pattern**:
```typescript
// Read package.json
// Match against patterns in framework-detection-patterns.yaml
// Return framework object with baseURL, devCommand, etc.
```

### 3. `generate-tests.ts`
**Purpose**: Generate Playwright test specifications from templates

**What it does**:
- Takes framework metadata and user journeys as input
- Populates test templates with appropriate selectors
- Adds screenshot capture points
- Generates Page Object Models
- Creates test helper utilities

**Usage Pattern**:
```typescript
// Load templates from ../templates/
// Populate with framework-specific values
// Generate .spec.ts files in tests/specs/
// Generate .page.ts files in tests/pages/
```

### 4. `capture-screenshots.ts`
**Purpose**: Execute tests and capture organized screenshots

**What it does**:
- Runs Playwright test suite
- Captures screenshots at defined points
- Organizes by test name, viewport, timestamp
- Generates metadata JSON for each screenshot

**Usage Pattern**:
```typescript
// Run: npx playwright test
// Hook into test lifecycle to capture screenshots
// Save to screenshots/current/{test-name}-{viewport}-{state}-{timestamp}.png
// Generate screenshots/metadata.json
```

### 5. `analyze-visual.ts`
**Purpose**: LLM-powered visual analysis of screenshots

**What it does**:
- Reads all screenshots from current run
- Sends each to LLM vision API with analysis prompts
- Categorizes findings (UI bugs, accessibility, layout)
- Generates structured issue reports
- Assigns severity levels

**Usage Pattern**:
```typescript
// Read screenshots/current/*.png
// For each screenshot:
//   - Send to LLM with prompts from ../data/common-ui-bugs.md
//   - Extract identified issues
//   - Categorize and rate severity
// Generate visual-analysis-report.md
```

### 6. `compare-regression.ts`
**Purpose**: Compare current screenshots with baselines

**What it does**:
- Loads baseline screenshots
- Performs pixel-level comparison with current screenshots
- Generates diff images highlighting changes
// Calculates difference percentages
- Classifies changes (expected, suspicious, critical)

**Usage Pattern**:
```typescript
// Load screenshots/baselines/*.png
// Load screenshots/current/*.png
// Use Playwright's comparison utilities
// Generate screenshots/diffs/*.png
// Create regression-report.md
```

### 7. `generate-fixes.ts`
**Purpose**: Generate code fix recommendations from visual issues

**What it does**:
- Takes visual analysis results as input
- Maps issues to source code locations
- Generates specific fix recommendations
- Provides before/after code snippets
- Prioritizes by severity

**Usage Pattern**:
```typescript
// Read visual-analysis-report.md
// For each issue:
//   - Infer likely source file (component, styles)
//   - Generate fix recommendation
//   - Provide file:line reference
//   - Create code snippet
// Generate fix-recommendations.md
```

### 8. `export-test-suite.ts`
**Purpose**: Package test suite for production use

**What it does**:
- Copies generated tests to project's tests/ directory
- Adds npm scripts to package.json
- Generates README with usage instructions
- Creates CI/CD workflow examples
- Validates everything works

**Usage Pattern**:
```typescript
// Copy tests/specs/ to project/tests/e2e/
// Copy tests/pages/ to project/tests/e2e/pages/
// Update project/package.json with test scripts
// Generate project/tests/e2e/README.md
// Validate: run tests to ensure they work
```

## Implementation Guidelines

### For LLMs Implementing These Scripts

**Don't execute scripts directly** - Instead, implement the logic inline:

```typescript
// Example: Instead of calling setup-playwright.sh
// Implement the logic directly in your response:

async function setupPlaywright() {
  // 1. Check Node version
  const nodeVersion = await execCommand('node --version');
  if (!nodeVersion.startsWith('v16') && !nodeVersion.startsWith('v18')) {
    throw new Error('Node 16+ required');
  }

  // 2. Install Playwright
  await execCommand('npm init playwright@latest -- --yes');

  // 3. Create directory structure
  await createDirectories([
    'tests/setup',
    'tests/pages',
    'tests/specs',
    'tests/utils',
    'screenshots/baselines',
    'screenshots/current',
    'screenshots/diffs',
  ]);

  // 4. Generate config (using templates)
  const config = await generatePlaywrightConfig(framework);
  await writeFile('playwright.config.ts', config);
}
```

### Script Dependencies

All scripts should be standalone reference implementations:
- No external dependencies beyond Playwright
- Clear, commented code
- Error handling included
- TypeScript for type safety

### Data Flow Between Scripts

```
1. detect-framework.ts
   ↓ (framework metadata)
2. setup-playwright.sh
   ↓ (Playwright installed, config generated)
3. generate-tests.ts
   ↓ (test files created)
4. capture-screenshots.ts
   ↓ (screenshots captured)
5. analyze-visual.ts
   ↓ (issues identified)
6. compare-regression.ts
   ↓ (regressions detected)
7. generate-fixes.ts
   ↓ (fix recommendations created)
8. export-test-suite.ts
   ↓ (production-ready test suite)
```

## Testing the Scripts

To validate script logic (for human developers):

```bash
# 1. Framework detection
npx ts-node scripts/detect-framework.ts
# Should output: { framework: 'react_vite', baseURL: 'http://localhost:5173', ... }

# 2. Test generation
npx ts-node scripts/generate-tests.ts --framework react_vite
# Should create: tests/specs/*.spec.ts

# 3. Screenshot capture
npx ts-node scripts/capture-screenshots.ts
# Should create: screenshots/current/*.png

# 4. Visual analysis
npx ts-node scripts/analyze-visual.ts
# Should create: visual-analysis-report.md

# 5. Regression comparison
npx ts-node scripts/compare-regression.ts
# Should create: screenshots/diffs/*.png, regression-report.md

# 6. Fix generation
npx ts-node scripts/generate-fixes.ts
# Should create: fix-recommendations.md

# 7. Export
npx ts-node scripts/export-test-suite.ts
# Should copy files to project/tests/e2e/
```

## Error Handling

All scripts should handle common errors:

```typescript
try {
  // Script logic
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error('File not found. Check paths.');
  } else if (error.message.includes('npm')) {
    console.error('npm command failed. Check if npm is installed.');
  } else {
    console.error('Unexpected error:', error.message);
  }
  process.exit(1);
}
```

## Performance Considerations

- **Parallel execution**: Run tests in parallel where possible
- **Incremental screenshots**: Only capture screenshots for changed tests
- **Caching**: Cache framework detection results
- **Batch processing**: Process multiple screenshots in batches for LLM analysis

## Future Enhancements

Potential scripts to add:

- `update-baselines.ts` - Interactive baseline approval
- `optimize-selectors.ts` - Suggest better selectors
- `generate-performance-tests.ts` - Add Core Web Vitals checks
- `create-ci-config.ts` - Generate GitHub Actions workflow
- `analyze-flaky-tests.ts` - Detect and fix flaky tests

---

**Remember**: These are reference implementations to guide LLM development. The actual execution happens through LLM-generated code, not by running these scripts directly.
