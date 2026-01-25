# Phase 1: Choose Tag Naming Convention

**Purpose**: Select the optimal tag naming pattern based on repository structure and team conventions.

## Steps

### 1. Assess Repository Structure

- Ask: "Is this a monorepo with multiple independently-versioned components?"
- Single-component repo: Simpler flat tags work well
- Multi-component repo: Namespaced tags provide clarity

### 2. Understand Existing Conventions

- Check current tags: `git tag -l`
- If tags exist, recommend consistency with current pattern
- If no tags exist, choose based on best practices below

### 3. Choose Namespace Separator (for multi-component repos)

**Option A: Slash-based namespacing** (`component/vX.Y.Z`)
- Pros: Hierarchical, supports git tag filtering (`git tag -l "hook/*"`)
- Pros: CI/CD can trigger on patterns (`hook/*` vs `skill/*`)
- Cons: Can be confused with directory paths
- Example: `marketplace/v1.0.0`, `hook/extract-insights/v2.1.0`

**Option B: NPM-style @ separator** (`component@X.Y.Z`)
- Pros: Familiar to JavaScript developers (`@scope/package@version`)
- Pros: Cleaner URLs, semantic clarity, path-safe
- Pros: No confusion with directory separators
- Cons: Less common in non-JS ecosystems
- Note: `v` prefix optional with `@` (separator itself indicates version)
- Example: `marketplace@1.0.0`, `extract-insights@2.1.0`

**Option C: Flat tags with prefixes** (`vX.Y.Z`)
- Pros: Simple, universal, works everywhere
- Cons: Doesn't scale to multi-component repos
- Example: `v1.0.0`, `v2.1.0`

### 4. Recommend Based on Context

- **Monorepo with multiple components**: Use Option A or B
- **JavaScript/npm ecosystem**: Prefer Option B (`@` separator)
- **Single component**: Use Option C (flat `vX.Y.Z`)
- **Team familiarity**: If team uses npm daily, choose Option B

### 5. Document the Decision

Add tag convention to project README or CONTRIBUTING.md:

```markdown
## Versioning

We use namespaced semantic versioning with @ separator:
- Marketplace: `marketplace@X.Y.Z`
- Skills: `skill-name@X.Y.Z`
- Hooks: `hook-name@X.Y.Z`
```

## Output

Chosen tag naming convention documented and agreed upon.

## Common Issues

- **Mixing conventions**: Once chosen, stick to one convention
- **Forgetting namespace**: In monorepos, always include namespace even for "main" component
