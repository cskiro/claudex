# Severity Rubric

## Core Principle

**Severity = Impact x Likelihood**, NOT WCAG conformance level.

- Level A vs AA is a *conformance tier*, not a risk rating
- A Level A failure can be LOW severity (decorative image missing alt)
- A Level AA failure can be CRITICAL (focus outline removed)

## Severity Levels

### Critical
- **Description**: Completely blocks access for users with disabilities
- **Impact**: Prevents task completion
- **Examples**:
  - Keyboard trap preventing navigation (2.1.2, Level A)
  - Missing alt text on primary action image (1.1.1, Level A)
  - Form submission inaccessible via keyboard (2.1.1, Level A)
  - Focus outline removed from focusable elements (2.4.7, Level AA)

### High
- **Description**: Significantly degrades experience or blocks common workflows
- **Impact**: Makes tasks difficult or requires workarounds
- **Examples**:
  - No skip navigation on complex site (2.4.1, Level A)
  - Poor contrast on primary CTA button (1.4.3, Level AA)
  - Missing error suggestions on required form (3.3.3, Level AA)
  - Touch targets too small on mobile (2.5.8, Level AA)

### Medium
- **Description**: Minor usability impact, affects subset of users
- **Impact**: Causes confusion or requires extra effort
- **Examples**:
  - Decorative icon not hidden but in acceptable context (1.1.1, Level A)
  - Link text needs slight improvement for clarity (2.4.4, Level A)
  - Missing autocomplete on optional field (1.3.5, Level AA)

### Low
- **Description**: Best practice enhancement, minimal user impact
- **Impact**: Nice-to-have improvement
- **Examples**:
  - Could add tooltips for better UX (not required)
  - Page title could be more descriptive (2.4.2, Level A - but functional)

## Calculation Guide

### Impact Assessment
| Level | Description | Severity Modifier |
|-------|-------------|-------------------|
| Blocker | Prevents access | Critical/High |
| Degraded | Makes difficult | High/Medium |
| Friction | Adds effort | Medium/Low |
| Minor | Barely noticeable | Low |

### Likelihood Assessment
| Level | Description | Severity Modifier |
|-------|-------------|-------------------|
| Core flow | All users hit it | Increase severity |
| Common | Many users hit it | Base severity |
| Edge case | Few users hit it | Decrease severity |
| Rare | Almost never | Low |

## Examples

### Same Criterion, Different Severity

**Missing alt text (1.1.1, Level A)**:
- Hero image: Impact=Blocker, Likelihood=All users → **CRITICAL**
- Decorative footer icon: Impact=Minor, Likelihood=Rare → **LOW**

**No skip link (2.4.1, Level A)**:
- 3-item navigation: Impact=Friction, Likelihood=Common → **MEDIUM**
- 50-item navigation: Impact=Degraded, Likelihood=All users → **HIGH**

**Poor contrast (1.4.3, Level AA)**:
- Primary CTA button: **CRITICAL**
- Body text: **HIGH**
- Footer link: **MEDIUM**
- Decorative text: **LOW**
