# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Extreme Programming (XP) Principles (Universal)

**Purpose**: Guide decision-making between alternatives using XP's 16 principles (Kent Beck's 15 + Document Decisions).
**Source**: Kent Beck's "Extreme Programming Explained" (White Book)

---

## Principle Application

When choosing between alternatives, prefer the option that meets these principles more fully.

> "A principle is more concrete than values. Either you have rapid feedback or you don't." - Kent Beck

---

## Fundamental Principles (Always Apply)

### 1. Rapid Feedback
- Time between action and feedback is crucial
- Run tests on every change
- CI/CD feedback loops < 10 minutes
- Surface problems immediately, don't batch

### 2. Assume Simplicity
- Build for today, not hypothetical tomorrow
- "What is the simplest thing that could possibly work?"
- Follow YAGNI (You Ain't Gonna Need It)
- Refactor when needed, not preemptively

### 3. Incremental Change
- Small changes > big bang releases
- PRs should be reviewable in one sitting (<400 LOC preferred)
- Daily commits to main/trunk
- Feature flags for gradual rollout

### 4. Embracing Change
- Requirements change is opportunity, not threat
- Design for adaptability (low coupling, high cohesion)
- Conversations over contracts
- Welcome late-breaking requirements

### 5. Quality Work
- Never sacrifice quality for speed (it backfires)
- "Technical debt" is not a negotiating chip
- Definition of Done is non-negotiable
- Pride in craftsmanship

### 6. Document Decisions (ADRs)
- Record significant technical decisions in Architecture Decision Records
- Include context, decision, consequences, and alternatives considered
- ADRs are immutable - supersede with new ADR, don't edit old ones

### 7. Travel Light
- Just enough documentation - no more, no less
- Delete unused artifacts (orphan docs, stale diagrams)
- **Prioritize docs-in-code over markdown files** (JSDoc, docstrings, type annotations)
- Working software > comprehensive documentation
- README and CLAUDE.md are the exceptions - keep them current

---

## Further Principles (Apply Contextually)

### 8. Teach Learning
- Rotate pairs to spread knowledge
- Reduce bus factor through cross-training
- Share learnings in retrospectives

### 9. Small Initial Investment
- MVP first, enhance later
- Walking skeleton before full build
- Timeboxed spikes for unknowns
- Validate concepts before commitment

### 10. Play to Win
- Outcome-focused, not process-focused
- Cut meetings/processes that don't add value
- Empower team decisions
- Pursue excellence, not just compliance

### 11. Concrete Experiments
- Spike stories for technical uncertainty
- Prototype before committing to architecture
- Measure before and after changes
- Evidence-based decisions

### 12. Open, Honest Communication
- Blameless retrospectives
- Direct feedback in code reviews
- Transparent project status
- Psychological safety enables honesty

### 13. Work with People's Instincts
- Trust developer intuition
- Team chooses tools and approaches
- Avoid forcing unnatural processes
- Sustainable practices over heroics

### 14. Accepted Responsibility
- Responsibility is accepted, not assigned
- Self-assignment of tasks
- Ownership mindset for code areas
- Accountability without blame

### 15. Local Adaptation
- Adapt processes to context
- Retrospective-driven improvements
- Document local conventions
- Principles over rigid rules

### 16. Honest Measurement
- Measure outcomes, not outputs
- No vanity metrics
- Velocity is for planning, not performance
- Transparent, comprehensible metrics

---

## Quick Reference: Decision Checklist

When evaluating options, ask:

```
┌────────────────────────────────────────────────────────┐
│  XP PRINCIPLE CHECK                                    │
├────────────────────────────────────────────────────────┤
│  [ ] Does this give us faster feedback?                │
│  [ ] Is this the simplest solution that works?         │
│  [ ] Can we do this incrementally?                     │
│  [ ] Does this embrace or resist change?               │
│  [ ] Does this maintain quality standards?             │
│  [ ] Are we playing to win or not to lose?             │
│  [ ] Is this based on concrete experiments?            │
│  [ ] Are we traveling light or carrying baggage?       │
│  [ ] Can responsibility be genuinely accepted?         │
│  [ ] Are our measurements honest?                      │
└────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Violated Principle | Better Approach |
|--------------|-------------------|-----------------|
| Big bang releases | Incremental Change | Small, frequent releases |
| Speculative features | Assume Simplicity | Build when needed |
| "We'll test later" | Rapid Feedback | Test-first development |
| Assigned blame | Accepted Responsibility | Blameless post-mortems |
| Comprehensive upfront docs | Travel Light | Just-in-time documentation |
| Vanity metrics | Honest Measurement | Outcome-based metrics |
| Process for process' sake | Play to Win | Value-driven practices |
| "That's not my code" | Accepted Responsibility | Collective ownership |
