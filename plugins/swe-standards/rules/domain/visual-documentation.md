# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Visual Documentation Standards (Universal)

---

## ASCII Diagram Patterns

### System Context
```
┌─────────────────────────────────────────────────────────────────┐
│                         SYSTEM NAME                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐     ┌─────────────┐     ┌─────────┐              │
│  │  User   │────▶│   System    │────▶│   DB    │              │
│  └─────────┘     └─────────────┘     └─────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### Flow Diagram
```
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│  Step  │──▶│  Step  │──▶│  Step  │──▶│  Done  │
└────────┘   └────────┘   └────────┘   └────────┘
```

### Decision Flow
```
         ┌─────────────┐
         │  Condition? │
         └──────┬──────┘
    Yes ◄───────┼───────► No
```

### Status Table
```
┌────────────────┬────────┬─────────┐
│  Service       │ Status │ Latency │
├────────────────┼────────┼─────────┤
│  api-gateway   │   OK   │  45ms   │
│  auth-service  │  WARN  │ 156ms   │
└────────────────┴────────┴─────────┘
```

### Layer Architecture
```
┌─────────────────────────────────────┐
│           Presentation              │
├─────────────────────────────────────┤
│           Application               │
├─────────────────────────────────────┤
│             Domain                  │
├─────────────────────────────────────┤
│          Infrastructure             │
└─────────────────────────────────────┘
```

---

## Box-Drawing Characters

```
Corners: ┌ ┐ └ ┘    T-joins: ├ ┤ ┬ ┴    Cross: ┼
Lines:   │ ─        Arrows:  ▶ ◀ ▲ ▼ → ←
Double:  ║ ═ ╔ ╗ ╚ ╝
```

---

## When to Use Diagrams

| Concept | Use Diagram |
|---------|-------------|
| Flows (data, process) | Yes |
| Architecture | Yes |
| Comparisons | Table |
| State machines | Yes |
| Simple answers | No |
| Before/after changes | Yes |
| Dependencies | Yes |

---

## Diagram Best Practices

- Keep diagrams **simple** - max 5-7 elements per level
- Use **consistent box sizes** for similar elements
- Add **labels** to arrows when meaning isn't obvious
- Include a **title** or context for complex diagrams
- Prefer **horizontal flow** (left-to-right) for sequences
- Use **vertical flow** (top-to-bottom) for hierarchies
