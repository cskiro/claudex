# Phase 3: Interactive Skill Design

**Purpose**: For each skill candidate, design the skill structure with user customization.

## Steps

### 1. Propose skill name
- Extract top keywords from cluster
- Apply naming heuristics:
  - Max 40 characters
  - Kebab-case
  - Remove filler words ("insight", "lesson", "the")
  - Add preferred suffix ("guide", "advisor", "helper")
- Example: "hook-deduplication-session-management" → "hook-deduplication-guide"
- Present to user with alternatives
- Allow user to customize

### 2. Generate description
- Use action verbs: "Use PROACTIVELY when", "Guides", "Analyzes"
- Include trigger context (what scenario)
- Include benefit (what outcome)
- Keep under 150 chars (soft limit, hard limit 1024)
- Present to user and allow editing

### 3. Assess complexity
Calculate based on:
- Number of insights (1 = minimal, 2-4 = standard, 5+ = complex)
- Total content length
- Presence of code examples
- Actionable items count

Recommend: minimal, standard, or complex
- Minimal: SKILL.md + README.md + plugin.json + CHANGELOG.md
- Standard: + data/insights-reference.md + examples/
- Complex: + templates/ + multiple examples/

### 4. Select skill pattern
Analyze insight content for pattern indicators:
- **Phase-based**: sequential steps, "first/then/finally"
- **Mode-based**: multiple approaches, "alternatively", "option"
- **Validation**: checking/auditing language, "ensure", "verify"
- **Data-processing**: parsing/transformation language

Recommend pattern with confidence level and explain trade-offs.

### 5. Map insights to skill structure
For each insight, identify content types:
- Problem description → Overview section
- Solution explanation → Workflow/Phases
- Code examples → examples/ directory
- Best practices → Important Reminders
- Checklists → templates/checklist.md
- Trade-offs → Decision Guide section
- Warnings → Important Reminders (high priority)

### 6. Define workflow phases (if phase-based)
For each phase:
- Generate phase name from insight content
- Extract purpose statement
- List steps (from insight action items or narrative)
- Define expected output
- Note common issues (from warnings in insights)

### 7. Preview the skill design
Show complete outline:
- Name, description, complexity
- Pattern and structure
- Section breakdown
- File structure

Ask for final confirmation or modifications.

## Output

Approved skill design specification ready for generation.

## Common Issues

- **User unsure about pattern**: Show examples from existing skills, offer recommendation
- **Naming conflicts**: Check ~/.claude/skills/ and .claude/skills/ for existing skills
- **Description too long**: Auto-trim and ask user to review
- **Unclear structure**: Fall back to default phase-based pattern
