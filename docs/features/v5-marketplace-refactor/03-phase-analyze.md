# Phase 3: Overlap Analysis

## Objective

Review all 23 skills for overlaps, redundancies, and reorganization opportunities.

## Skill Inventory (23 total)

### api-tools (3 skills)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| structured-outputs-advisor | JSON schema guidance | Low |
| json-outputs-implementer | JSON output implementation | Low |
| strict-tool-implementer | Strict tool use | Low |

### claude-code-tools (5 skills)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| cc-insights | Conversation analysis | Low |
| sub-agent-creator | Create subagents | Low |
| mcp-server-creator | MCP server scaffolding | Low |
| claude-md-auditor | CLAUDE.md validation | Low |
| otel-monitoring-setup | OpenTelemetry setup | Low |

### meta-tools (3 skills after restore)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| skill-creator | Create new skills | **Medium** |
| skill-isolation-tester | Test skills in isolation | Low |
| insight-skill-generator | Generate skills from insights | **High** (with skill-creator) |

### testing-tools (3 skills)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| e2e-testing | Playwright E2E testing | Low |
| test-driven-development | TDD workflow | Low |
| mutation-testing | Mutation test analysis | Low |

### devops-tools (3 skills)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| react-project-scaffolder | React project setup | Low |
| github-repo-setup | GitHub repo creation | Low |
| git-worktree-setup | Git worktree management | Low |

### analysis-tools (3 skills - restored)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| codebase-auditor | Code quality analysis | **Medium** (with code-quality-reviewer agent) |
| bulletproof-react-auditor | React best practices | Low |
| accessibility-audit | A11y compliance | **Medium** (with ui-ux-designer agent) |

### release-management (1 skill - restored)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| semantic-release-tagger | Automated versioning | Low |

### planning-tools (1 skill - restored)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| ascii-diagram-creator | ASCII diagram generation | **Low** (rules provide guidance only) |

### benchmarking (1 skill - restored)
| Skill | Purpose | Overlap Risk |
|-------|---------|--------------|
| benchmark-report-creator | Academic benchmark reports | Low |

### productivity-hooks (0 skills)
| Component | Purpose | Overlap Risk |
|-----------|---------|--------------|
| hooks.json | Event-driven automation | N/A |

---

## Identified Overlaps

### High Priority: skill-creator vs insight-skill-generator

**Overlap**: Both create skills from different inputs

**Recommendation**:
- Option A: Merge insight-skill-generator into skill-creator as a "mode"
- Option B: Keep separate with clearer differentiation in descriptions

**Decision**: TBD after implementation

### Medium Priority: codebase-auditor vs code-quality-reviewer agent

**Overlap**: Both perform code quality analysis

**Key Difference**:
- Skill: User-installed, semantic triggering, progressive disclosure
- Agent: Built-in, Task tool invocation, fixed behavior

**Recommendation**: Keep both - different invocation models serve different use cases

### Medium Priority: accessibility-audit vs ui-ux-designer agent

**Overlap**: Both cover accessibility

**Key Difference**:
- Skill: Focused audit workflow with checklist
- Agent: Broader UI/UX design scope

**Recommendation**: Keep both - skill provides structured audit workflow

---

## Reorganization Opportunities

### Single-Skill Plugins

Four plugins have only 1 skill:
- `release-management` (1)
- `planning-tools` (1)
- `benchmarking` (1)

**Options**:
1. Keep as-is (clear categorization)
2. Merge into broader categories (fewer plugins)

**Recommendation**: Keep as-is for v5.0.0, consider consolidation in v6.0.0

---

## Analysis Findings

| Finding | Severity | Action |
|---------|----------|--------|
| skill-creator/insight-skill-generator overlap | High | Document differentiation |
| Single-skill plugins | Low | Keep for now |
| Skill vs agent overlaps | Medium | Document as intentional |

## Next Steps

- [ ] Document skill differentiation in READMEs
- [ ] Add "NOT for" sections to overlapping skills
- [ ] Consider v6.0.0 consolidation roadmap
