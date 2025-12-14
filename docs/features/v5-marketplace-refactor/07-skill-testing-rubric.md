# v5.0.0 Skill Testing Rubric

Manual testing checklist for all 23 skills across 9 plugin categories.

## Testing Instructions

1. Open a **separate terminal** in `~/test-claudex-install`
2. Start Claude Code: `claude`
3. Test each skill by typing the trigger prompt
4. Verify the skill activates (check status line shows skill name)
5. Mark pass/fail in the checklist

---

## API Tools (3 skills)

### structured-outputs-advisor
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Help me with structured outputs" | Skill activates, asks clarifying questions | [ ] |
| Core function | "I need to extract structured data from customer emails" | Recommends JSON outputs, delegates to implementer | [ ] |

### json-outputs-implementer
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Implement JSON outputs for data extraction" | Skill activates | [ ] |
| Core function | "Create a Pydantic schema for user registration" | Generates SDK-ready schema | [ ] |

### strict-tool-implementer
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Implement strict tool use for my agent" | Skill activates | [ ] |
| Core function | "Create a validated tool schema for booking flights" | Generates strict tool definition | [ ] |

---

## Analysis Tools (3 skills) - RESTORED

### codebase-auditor
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Audit my codebase" | Skill activates | [ ] |
| Trigger alt | "Run a code quality audit" | Skill activates | [ ] |
| Core function | "Analyze this project for technical debt" | Starts audit workflow | [ ] |

### bulletproof-react-auditor
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Audit my React codebase" | Skill activates | [ ] |
| Trigger alt | "Check React best practices" | Skill activates | [ ] |
| Core function | "Analyze component architecture" | Starts React audit | [ ] |

### accessibility-audit
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Check accessibility" | Skill activates | [ ] |
| Trigger alt | "Run a11y audit" | Skill activates | [ ] |
| Core function | "Audit WCAG compliance" | Starts a11y workflow | [ ] |

---

## Claude Code Tools (5 skills)

### cc-insights
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Analyze my Claude Code conversations" | Skill activates | [ ] |
| Trigger alt | "Search past conversations" | Skill activates | [ ] |
| Core function | "Find conversations about testing" | Semantic search works | [ ] |

### sub-agent-creator
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create a sub-agent" | Skill activates | [ ] |
| Core function | "Generate a code review agent" | Creates agent YAML | [ ] |

### mcp-server-creator
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create an MCP server" | Skill activates | [ ] |
| Core function | "Scaffold an MCP server for database access" | Generates server code | [ ] |

### claude-md-auditor
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Audit my CLAUDE.md" | Skill activates | [ ] |
| Core function | "Validate CLAUDE.md against best practices" | Runs audit | [ ] |

### otel-monitoring-setup
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Set up OpenTelemetry monitoring" | Skill activates | [ ] |
| Core function | "Configure OTEL for Claude Code" | Provides setup guide | [ ] |

---

## Meta Tools (3 skills)

### skill-creator
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create a new skill" | Skill activates | [ ] |
| Core function | "Generate a skill for code formatting" | Scaffolds skill structure | [ ] |

### skill-isolation-tester
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Test my skill in isolation" | Skill activates | [ ] |
| Core function | "Run isolation tests on skill-creator" | Starts test workflow | [ ] |

### insight-skill-generator - RESTORED
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Generate a skill from insights" | Skill activates | [ ] |
| Core function | "Create skill from my lessons-learned patterns" | Analyzes insights | [ ] |

---

## Testing Tools (3 skills)

### e2e-testing
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Set up e2e testing" | Skill activates | [ ] |
| Trigger alt | "Configure Playwright" | Skill activates | [ ] |
| Core function | "Create e2e tests for login flow" | Generates test code | [ ] |

### test-driven-development
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Set up TDD" | Skill activates | [ ] |
| Trigger alt | "Enforce test-first development" | Skill activates | [ ] |
| Core function | "Configure TDD workflow" | Sets up TDD infrastructure | [ ] |

### mutation-testing
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Run mutation testing" | Skill activates | [ ] |
| Trigger alt | "Check test quality with mutations" | Skill activates | [ ] |
| Core function | "Analyze test suite effectiveness" | Starts mutation analysis | [ ] |

---

## DevOps Tools (3 skills)

### react-project-scaffolder
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create a new React project" | Skill activates | [ ] |
| Core function | "Scaffold enterprise React app" | Offers mode selection | [ ] |

### github-repo-setup
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create a GitHub repository" | Skill activates | [ ] |
| Core function | "Set up repo with CI/CD" | Offers setup modes | [ ] |

### git-worktree-setup
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Set up git worktrees" | Skill activates | [ ] |
| Core function | "Create parallel Claude Code sessions" | Creates worktrees | [ ] |

---

## Release Management (1 skill) - RESTORED

### semantic-release-tagger
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create a semantic release" | Skill activates | [ ] |
| Trigger alt | "Tag this release" | Skill activates | [ ] |
| Core function | "Analyze commits and suggest version" | Starts versioning workflow | [ ] |

---

## Planning Tools (1 skill) - RESTORED

### ascii-diagram-creator
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create an ASCII diagram" | Skill activates | [ ] |
| Trigger alt | "Draw architecture diagram" | Skill activates | [ ] |
| Core function | "Diagram the system architecture" | Generates ASCII art | [ ] |

---

## Benchmarking (1 skill) - RESTORED

### benchmark-report-creator
| Test | Prompt | Expected | Pass |
|------|--------|----------|------|
| Trigger | "Create a benchmark report" | Skill activates | [ ] |
| Core function | "Generate AI model comparison report" | Starts report workflow | [ ] |

---

## Quick Smoke Test (5 min)

For rapid validation, test these key skills:

| Plugin | Skill | Prompt | Pass |
|--------|-------|--------|------|
| analysis-tools | codebase-auditor | "Audit my codebase" | [ ] |
| analysis-tools | accessibility-audit | "Check accessibility" | [ ] |
| release-management | semantic-release-tagger | "Create semantic release" | [ ] |
| planning-tools | ascii-diagram-creator | "Create ASCII diagram" | [ ] |
| benchmarking | benchmark-report-creator | "Create benchmark report" | [ ] |
| meta-tools | skill-creator | "Create a new skill" | [ ] |
| testing-tools | e2e-testing | "Set up e2e testing" | [ ] |

---

## Results Summary

| Category | Total Skills | Passed | Failed |
|----------|--------------|--------|--------|
| API Tools | 3 | _ | _ |
| Analysis Tools | 3 | _ | _ |
| Claude Code Tools | 5 | _ | _ |
| Meta Tools | 3 | _ | _ |
| Testing Tools | 3 | _ | _ |
| DevOps Tools | 3 | _ | _ |
| Release Management | 1 | _ | _ |
| Planning Tools | 1 | _ | _ |
| Benchmarking | 1 | _ | _ |
| **TOTAL** | **23** | **_** | **_** |

---

## Notes

- If a skill doesn't trigger, check `/plugin` to verify it's installed
- Skills trigger based on semantic matching, not exact phrases
- Some skills may require specific project context to activate fully
