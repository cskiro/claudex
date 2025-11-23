# Phase 1: Application Discovery & Version Detection

**Purpose**: Understand the application architecture, detect framework versions, and determine optimal Playwright setup

## Steps

### 1. Detect application type and versions
- Read package.json to identify frameworks (React, Vite, Next.js, Express, etc.)
- Check for common files (vite.config.ts, next.config.js, app.js, index.html)
- Identify build tools and dev server configuration
- Extract installed package versions for version-aware configuration

### 2. Consult version compatibility database
- Load `data/framework-versions.yaml` compatibility rules
- Match installed versions against version ranges using semver
- Determine appropriate templates for each framework version
- Identify potential breaking changes or incompatibilities
- **Example**: Tailwind v4 detected → use `@import` syntax, not `@tailwind`

### 3. Validate application access
- Check if dev server is running (ports 3000, 5173, 8080, etc.)
- If not running, determine how to start it (npm run dev, npm start, etc.)
- Verify application loads successfully

### 4. Map critical user journeys
- Identify key pages/routes from routing configuration
- Detect authentication flows
- Find form submissions and interactive elements
- Locate API integrations

## Version Detection Logic

```typescript
// Load compatibility database
const versionDb = parseYAML('data/framework-versions.yaml');

// Detect versions
const detectedVersions = {
  tailwind: detectVersion(deps.tailwindcss, versionDb.tailwindcss),
  react: detectVersion(deps.react, versionDb.react),
  vite: detectVersion(deps.vite, versionDb.vite),
};

// Select appropriate templates
const templates = {
  css: detectedVersions.tailwind?.templates.css || 'templates/css/vanilla.css',
  postcss: detectedVersions.tailwind?.templates.postcss_config,
  playwright: 'templates/playwright.config.template.ts',
};
```

## Output

Application profile with:
- Framework type and versions
- URLs and ports
- Test targets
- Selected templates

## Common Issues

**Unrecognized framework**
- Ask user to specify app type and dev server command manually
- Use generic static site configuration as fallback

**Missing package.json**
- Check for other indicators (index.html, etc.)
- Prompt user for application details

## Transition

Proceed to Phase 2 (Playwright Installation) with version-aware configuration
