# Mode 2: Generate Insights

**When to use**: Understand patterns and trends

## Trigger Phrases
- "Generate weekly insights report"
- "Show me my most active files this month"
- "What patterns do you see in my conversations?"
- "Create a project summary report"

## Process

1. User asks for insights on a timeframe
2. Skill analyzes metadata and patterns
3. Creates markdown report with visualizations
4. Offers to save report to file

## Report Sections

- **Executive Summary**: Key metrics
- **Activity Timeline**: Conversations over time
- **File Hotspots**: Most modified files
- **Tool Usage Breakdown**: Which tools you use most
- **Topic Clusters**: Recurring themes
- **Knowledge Highlights**: Key solutions and learnings

## Example Output

```markdown
# Weekly Insights (Oct 19-25, 2025)

## Overview
- 12 conversations
- 8 active days
- 23 files modified
- 45 tool uses

## Top Files
1. src/auth/token.ts (5 modifications)
2. src/components/Login.tsx (3 modifications)
3. src/api/auth.ts (3 modifications)

## Activity Pattern
Mon: ████████ 4 conversations
Tue: ██████ 3 conversations
Wed: ██████ 3 conversations
Thu: ████ 2 conversations
Fri: ████ 2 conversations

## Key Topics
- Authentication (6 conversations)
- Testing (3 conversations)
- Bug fixes (2 conversations)

## Knowledge Highlights
- Implemented JWT refresh token pattern
- Added React Testing Library for auth components
- Fixed OAuth redirect edge case

[Save report to file? Y/n]
```

## File-Centric Analysis

```
# File Hotspots (All Time)

🔥🔥🔥 src/auth/token.ts (15 conversations)
🔥🔥 src/components/Login.tsx (9 conversations)
🔥🔥 src/api/auth.ts (8 conversations)
🔥 src/hooks/useAuth.ts (6 conversations)

Insight: Authentication module is your most active area.
Consider: Review token.ts for refactoring opportunities.
```
