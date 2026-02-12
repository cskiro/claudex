# Setup & Adoption Guide

Step-by-step guide for adopting swe-standards in your projects.

---

## Prerequisites

- Claude Code installed
- swe-standards plugin installed (`/plugin install swe-standards@claudex`)

## Step 1: Run Init

```
/swe-standards:init
```

This will:
1. Detect your project type (TypeScript, Python, or both)
2. Recommend profiles based on detected tooling
3. Let you select which profiles to install
4. Scaffold rules to `~/.claude/rules/swe-standards/`
5. Write a manifest for tracking versions and changes

## Step 2: Verify Installation

```
/swe-standards:check
```

Confirms all selected rules are present and healthy.

## Step 3: Test Integration

Start a new Claude Code session. The rules will auto-load based on file context:
- Universal rules load for every file
- Path-scoped rules load only for matching files (e.g., `typescript.md` for `.ts` files)

Try these to verify:
- Open a `.ts` file → TypeScript standards should influence suggestions
- Ask about git branching → narrative templates should apply
- Write a test → TDD workflow should be enforced

## Step 4: Customize (Optional)

Rules are scaffolded as real files. You can:
- **Edit** any rule to match your team's conventions
- **Delete** rules you don't want
- **Add** custom rules alongside swe-standards rules

Note: Edited files will be flagged as "modified" by `/swe-standards:sync` and won't be overwritten without your confirmation.

---

## Incremental Adoption

You don't have to adopt everything at once:

### Week 1: Core Only
Start with Core profile (git branching, commit templates, fail-fast principles).

### Week 2: Add Language Profile
Add TypeScript or Python profile based on your stack.

### Week 3: Add Testing
Adopt TDD workflow and Testing Trophy methodology.

### Week 4: Add Quality
Enable PR review toolkit and code simplifier workflows.

### When Ready: Add Security
Install security standards for production-grade protection.

---

## Dependencies

| Plugin | Source | Why | Install |
|--------|--------|-----|---------|
| `pr-review-toolkit` | Anthropic marketplace (external) | Quality profile's 6 review agents | Install from Anthropic's plugin marketplace |
| `adr-generator` | claudex marketplace | XP principles reference ADR creation | `/plugin install adr-generator@claudex` |
| `ascii-diagram-creator` | claudex marketplace | Visual documentation standards | `/plugin install ascii-diagram-creator@claudex` |

The `/swe-standards:init` and `/swe-standards:check` commands will detect missing dependencies and prompt you to install them.

---

## Troubleshooting

### Rules not loading
- Check `~/.claude/rules/swe-standards/` exists and contains files
- Run `/swe-standards:check` to verify
- Restart Claude Code session (rules load at session start)

### Path-scoped rules not activating
- Verify the file you're editing matches the rule's `paths:` frontmatter
- Example: `typescript.md` only loads for `**/*.ts` and `**/*.tsx` files

### Want to start over
- Delete `~/.claude/rules/swe-standards/`
- Delete `~/.claude/swe-standards.json`
- Run `/swe-standards:init` again
