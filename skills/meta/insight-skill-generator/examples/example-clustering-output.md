# Example: Clustering Analysis Output

This example shows what the clustering phase produces when analyzing a project's insights.

## Scenario

A project has been using the extract-explanatory-insights hook for 2 weeks, generating 12 insights across different categories.

---

## Phase 1: Discovery Summary

**Total Insights Found**: 12
**Date Range**: 2025-11-01 to 2025-11-14
**Unique Sessions**: 8
**Categories**:
- testing: 5 insights
- hooks-and-events: 3 insights
- architecture: 2 insights
- performance: 2 insights

**Preview**:
1. "Modern Testing Strategy with Testing Trophy" (testing, 2025-11-01)
2. "Hook Deduplication Session Management" (hooks-and-events, 2025-11-03)
3. "CPU Usage Prevention in Vitest" (testing, 2025-11-03)
4. "BSD awk Compatibility in Hook Scripts" (hooks-and-events, 2025-11-05)
5. "Semantic Query Priorities in React Testing Library" (testing, 2025-11-06)

---

## Phase 2: Clustering Analysis

### Cluster 1: Testing Strategy
**Size**: 3 insights
**Similarity Score**: 0.75 (high)
**Recommended Complexity**: Standard
**Recommended Pattern**: Validation

**Insights**:
1. "Modern Testing Strategy with Testing Trophy"
   - Keywords: testing, integration, unit, e2e, trophy, kent-c-dodds
   - Category: testing
   - Date: 2025-11-01
   - Length: 156 lines
   - Has code examples: Yes

2. "Semantic Query Priorities in React Testing Library"
   - Keywords: testing, react, semantic, query, getByRole, accessibility
   - Category: testing
   - Date: 2025-11-06
   - Length: 89 lines
   - Has code examples: Yes

3. "What NOT to Test - Brittle Patterns"
   - Keywords: testing, avoid, brittle, implementation-details, user-behavior
   - Category: testing
   - Date: 2025-11-08
   - Length: 67 lines
   - Has code examples: No

**Shared Keywords**: testing (3), react (2), user (2), behavior (2), semantic (2)

**Cluster Characteristics**:
- All in same category (testing)
- Temporal span: 7 days
- Common theme: User-focused testing approach
- Total code examples: 5 blocks
- Actionable items: 12

**Suggested Skill Name**: "user-focused-testing-guide"

**Suggested Description**: "Use PROACTIVELY when writing tests to ensure user-centric testing strategy following Testing Trophy methodology and React Testing Library best practices"

**Skill Structure Recommendation**:
```
SKILL.md sections:
- Overview (Testing Trophy philosophy)
- Phase 1: Query Selection (semantic queries)
- Phase 2: Test Writing (user workflows)
- Phase 3: Avoiding Brittle Tests
- Important Reminders (what NOT to test)
- Examples (from code blocks)
```

---

### Cluster 2: Hook Development
**Size**: 2 insights
**Similarity Score**: 0.68 (medium-high)
**Recommended Complexity**: Minimal to Standard
**Recommended Pattern**: Phase-based

**Insights**:
1. "Hook Deduplication Session Management"
   - Keywords: hook, deduplication, session, hash, state
   - Category: hooks-and-events
   - Date: 2025-11-03
   - Length: 124 lines
   - Has code examples: Yes (bash)

2. "BSD awk Compatibility in Hook Scripts"
   - Keywords: hook, awk, bsd, macos, compatibility, portable
   - Category: hooks-and-events
   - Date: 2025-11-05
   - Length: 78 lines
   - Has code examples: Yes (bash)

**Shared Keywords**: hook (2), bash (2), script (2), compatibility (2)

**Cluster Characteristics**:
- Same category (hooks-and-events)
- Temporal span: 2 days (high proximity)
- Common theme: Hook script development best practices
- Total code examples: 4 blocks (all bash)
- Actionable items: 8

**Suggested Skill Name**: "hook-script-development-guide"

**Suggested Description**: "Guides Claude Code hook script development with deduplication patterns and cross-platform compatibility best practices for macOS/Linux environments"

**Skill Structure Recommendation**:
```
SKILL.md sections:
- Overview (Hook development challenges)
- Phase 1: Deduplication Strategy (session vs content)
- Phase 2: Cross-Platform Compatibility (BSD awk)
- Phase 3: Testing and Validation
- Examples (bash scripts)
- Templates (hook-template.sh)
```

---

### Cluster 3: Performance Optimization
**Size**: 2 insights
**Similarity Score**: 0.62 (medium)
**Recommended Complexity**: Minimal
**Recommended Pattern**: Phase-based

**Insights**:
1. "CPU Usage Prevention in Vitest"
   - Keywords: vitest, cpu, performance, threads, watch-mode
   - Category: testing
   - Date: 2025-11-03
   - Length: 45 lines
   - Has code examples: Yes (npm scripts)

2. "Bundle Size Optimization"
   - Keywords: bundle, size, webpack, optimization, tree-shaking
   - Category: performance
   - Date: 2025-11-09
   - Length: 92 lines
   - Has code examples: Yes (webpack config)

**Shared Keywords**: performance (2), optimization (2), build (2)

**Cluster Characteristics**:
- Different categories (testing, performance)
- Temporal span: 6 days
- Common theme: Build/test performance
- Total code examples: 3 blocks
- Actionable items: 6

**Suggested Skill Name**: "build-performance-optimizer"

**Suggested Description**: "Analyzes build and test performance issues and generates optimization recommendations for Vitest test runs and webpack bundle sizes"

**Skill Structure Recommendation**:
```
SKILL.md sections:
- Overview (Performance impact on DX)
- Phase 1: Test Performance Analysis
- Phase 2: Bundle Size Analysis
- Phase 3: Optimization Implementation
- Important Reminders (check before test, monitor bundle)
- Examples (npm scripts, webpack config)
```

---

### Standalone Insights

#### Standalone 1: "Hook State Management Patterns"
**Quality Score**: 0.85 (high - qualifies for standalone skill)
**Category**: hooks-and-events
**Date**: 2025-11-07
**Length**: 134 lines
**Code Examples**: Yes (3 blocks)

**Why Standalone**:
- Doesn't cluster with other hook insights (different focus)
- High quality with comprehensive coverage
- Self-contained topic (state management)
- Multiple actionable patterns

**Suggested Skill Name**: "hook-state-manager"

**Suggested Description**: "Automates state management setup for Claude Code hooks with persistent storage, cleanup, and safe concurrency patterns"

---

#### Standalone 2: "Architecture Decision Records"
**Quality Score**: 0.82 (high - qualifies for standalone skill)
**Category**: architecture
**Date**: 2025-11-12
**Length**: 156 lines
**Code Examples**: Yes (template)

**Why Standalone**:
- Unique topic (no other architecture insights)
- High quality with complete template
- Valuable for documentation
- Industry best practice

**Suggested Skill Name**: "adr-documentation-helper"

**Suggested Description**: "Guides creation of Architecture Decision Records (ADRs) following industry standards with templates and integration with project documentation"

---

### Low-Quality Insights (Not Recommended for Skills)

#### "Git Branch Naming Convention"
**Quality Score**: 0.42 (low)
**Category**: version-control
**Reason for Exclusion**: Too simple, covered by existing conventions, no unique value

#### "TypeScript Strict Mode Benefits"
**Quality Score**: 0.38 (low)
**Category**: typescript
**Reason for Exclusion**: Common knowledge, well-documented elsewhere, not actionable enough

---

## User Decision Points

At this stage, the skill would present the following options to the user:

**Option 1: Generate All Recommended Skills** (5 skills)
- user-focused-testing-guide (Cluster 1)
- hook-script-development-guide (Cluster 2)
- build-performance-optimizer (Cluster 3)
- hook-state-manager (Standalone 1)
- adr-documentation-helper (Standalone 2)

**Option 2: Select Specific Skills**
- User picks which clusters/standalones to convert

**Option 3: Modify Clusters**
- Split large clusters
- Merge small clusters
- Recategorize insights
- Adjust complexity levels

**Option 4: Tune Thresholds and Retry**
- Increase cluster_minimum (0.6 → 0.7) for tighter clusters
- Decrease standalone_quality (0.8 → 0.7) for more standalone skills

---

## Proceeding to Phase 3

If user selects "user-focused-testing-guide" to generate, the skill would proceed to Phase 3: Interactive Skill Design with the following proposal:

**Skill Design Proposal**:
- Name: `user-focused-testing-guide`
- Description: "Use PROACTIVELY when writing tests to ensure user-centric testing strategy following Testing Trophy methodology and React Testing Library best practices"
- Complexity: Standard
- Pattern: Validation
- Structure:
  - SKILL.md with validation workflow
  - data/insights-reference.md with 3 source insights
  - examples/query-examples.md with semantic query patterns
  - templates/test-checklist.md with testing checklist

User can then customize before generation begins.

---

**This example demonstrates**:
1. How clustering groups related insights
2. What information is presented for each cluster
3. How standalone insights are identified
4. Why some insights are excluded
5. What decisions users can make
6. How the process flows into Phase 3
