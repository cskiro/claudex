# Research-Based Optimization

Academic findings on LLM context utilization and attention patterns.

## Lost in the Middle Phenomenon

**Source**: Liu et al., 2023 - "Lost in the Middle: How Language Models Use Long Contexts"

### Key Finding
LLMs perform best when relevant information is positioned at the **beginning or end** of context, not the middle.

### Performance Curve
```
Performance
    ^
100%|*                              *
    |  *                          *
 75%|    *                      *
    |      *                  *
 50%|        *    ****    *
    |          **      **
    +----------------------------> Position
    Start    Middle         End
```

### Implications for CLAUDE.md
- **Critical information**: First 20% of file
- **Reference material**: Last 20% of file
- **Supporting details**: Middle sections

## Optimal Structure

Based on research findings:

```markdown
# Project Name

## CRITICAL (Top 20%)
- Build commands
- Breaking patterns to avoid
- Security requirements

## IMPORTANT (Next 30%)
- Core architecture
- Main conventions
- Testing requirements

## SUPPORTING (Middle 30%)
- Detailed patterns
- Edge cases
- Historical context

## REFERENCE (Bottom 20%)
- Links and resources
- Version history
- Maintenance notes
```

## Token Efficiency Research

### Context Window Utilization
- **Diminishing returns** after ~4K tokens of instructions
- **Optimal range**: 1,500-3,000 tokens
- **Beyond 5K**: Consider splitting into imports

### Information Density
- Prefer lists over paragraphs (better attention)
- Use code blocks (higher signal-to-noise)
- Avoid redundancy (wastes attention budget)

## Attention Calibration (MIT/Google Cloud AI, 2024)

### Finding
Recent models (Claude 3.5+) show improved but not eliminated middle-position degradation.

### Recommendations
1. **Chunking**: Group related information together
2. **Explicit markers**: Use headers and formatting
3. **Repetition**: Critical items can appear twice (top and bottom)

## Claude-Specific Performance Data

### Context Awareness in Claude 4/4.5
- Better at tracking multiple requirements
- Still benefits from positional optimization
- Explicit priority markers help attention allocation

### Effective Markers
```markdown
**CRITICAL**: Must follow exactly
**IMPORTANT**: Strongly recommended
**NOTE**: Additional context
```

## Practical Applications

### Audit Criteria Based on Research

**Check positioning of**:
- Security requirements (should be top)
- Build commands (should be top)
- Error-prone patterns (should be top or bottom)
- Reference links (should be bottom)

**Flag as issues**:
- Critical info buried in middle
- Long unstructured paragraphs
- Missing headers/structure
- No priority markers

## References

- Liu et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts"
- MIT/Google Cloud AI (2024). "Attention Calibration in Large Language Models"
- Anthropic (2024). "Claude's Context Window Behavior"
