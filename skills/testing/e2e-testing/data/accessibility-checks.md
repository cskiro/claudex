# Accessibility Checks for Visual Analysis

WCAG 2.1 AA compliance criteria for LLM-powered screenshot analysis.

## Overview

When analyzing screenshots, check for these accessibility violations. This guide follows WCAG 2.1 Level AA standards.

## 1. Color Contrast

### Minimum Contrast Ratios

**Text:**
- Normal text (< 18pt or < 14pt bold): **4.5:1**
- Large text (≥ 18pt or ≥ 14pt bold): **3:1**

**UI Components:**
- Form inputs, buttons, icons: **3:1** against background

### Common Violations in Screenshots

```
❌ Light gray text on white background (2:1 ratio)
✅ Dark gray #595959 on white #FFFFFF (7:1 ratio)

❌ Blue link #4A90E2 on light blue #E8F4FF (1.8:1 ratio)
✅ Blue link #0066CC on white #FFFFFF (8.2:1 ratio)

❌ Gray placeholder text #CCCCCC on white (1.6:1 ratio)
✅ Gray placeholder text #757575 on white (4.6:1 ratio)
```

### Visual Indicators

When analyzing screenshots, look for:
- Pale or faded text that's hard to read
- Low-contrast buttons that don't stand out
- Links that blend into surrounding text
- Disabled states that are barely distinguishable

## 2. Text Size and Readability

### Minimum Font Sizes

- Body text: **16px** minimum (1rem)
- Small text acceptable: **14px** for secondary content
- Avoid: Text smaller than **12px** (fails WCAG)

### Common Violations

```
❌ Body text at 12px - too small for many users
✅ Body text at 16px or larger

❌ Mobile text at 10px - illegible on small screens
✅ Mobile text at 14px minimum

❌ Long paragraphs with no line height spacing
✅ Line height 1.5x for body text (e.g., 16px text with 24px line height)
```

### Visual Indicators

- Text that appears squished or compressed
- Long lines of text with minimal spacing
- Tiny labels on buttons or form fields

## 3. Focus Indicators

### Requirements

All interactive elements must have **visible focus indicators**:
- Minimum **2px** outline or border
- Contrast ratio of **3:1** against background
- Clearly visible when tabbing through interface

### Common Violations

```
❌ No visible outline when button is focused
✅ Blue 2px outline appears on focus

❌ Focus outline same color as background (invisible)
✅ High-contrast focus outline (e.g., black on white)

❌ Focus state only indicated by subtle background color change
✅ Focus state with outline + background color change
```

### Visual Indicators in Screenshots

Look for:
- Focused element (if screenshot captures tab state)
- Absence of visible outline or border
- Focus indicator that's too subtle or low-contrast

## 4. Form Labels and Instructions

### Requirements

- Every form input must have a visible **<label>** or aria-label
- Labels must be **adjacent** to their inputs
- Required fields must be clearly indicated
- Error messages must be **visible and associated** with inputs

### Common Violations

```
❌ Input with only placeholder text (disappears when typing)
✅ Input with persistent label above or beside it

❌ Label far away from input (hard to associate)
✅ Label immediately adjacent to input

❌ Required field marked only with color (red border)
✅ Required field marked with * and "Required" text

❌ Error message in different part of page
✅ Error message directly below input field
```

### Visual Indicators

- Inputs without visible labels
- Placeholder text used as labels (disappears on focus)
- Required fields indicated only by color
- Error states without clear error text

## 5. Heading Hierarchy

### Requirements

- Headings must follow logical order: **H1 → H2 → H3** (no skipping)
- Page should have exactly **one H1** (page title)
- Headings should be **visually distinct** from body text

### Common Violations

```
❌ Page with H1 → H4 (skips H2, H3)
✅ Page with H1 → H2 → H3

❌ Multiple H1 headings on same page
✅ Single H1 for page title, H2s for sections

❌ Heading text same size as body text
✅ Headings progressively larger: H3 < H2 < H1
```

### Visual Indicators in Screenshots

- Headings that don't look like headings (same size as body)
- Missing visual hierarchy (all headings same size)
- Text that looks like headings but isn't (bold body text)

## 6. Alternative Text for Images

### Requirements

- Decorative images: Empty alt="" or aria-hidden="true"
- Informative images: Descriptive alt text
- Complex images (charts, graphs): Detailed description

### Common Violations

**Note:** Can't always detect from screenshots alone, but can identify likely issues:

```
❌ Icon buttons with no visible text label (likely missing aria-label)
✅ Icon buttons with visible text label or tooltip

❌ Charts/graphs with no accompanying data table or description
✅ Charts with descriptive caption or linked data table

❌ Images that convey important info but might lack alt text
✅ Important info also available in visible text
```

### Visual Indicators

- Icon-only buttons without text labels
- Charts/infographics without textual explanations
- Images that appear to contain important information

## 7. Keyboard Navigation

### Requirements

- All interactive elements accessible via keyboard
- Logical tab order (top to bottom, left to right)
- No keyboard traps
- Skip links for navigation

### Visual Analysis Cues

**Can identify potential issues from screenshots:**

```
❌ Custom dropdown without visible keyboard focus states
✅ Standard HTML select or custom with clear focus indicators

❌ Modal dialog with no visible close button (might trap keyboard)
✅ Modal with visible, accessible close button

❌ Navigation menu requiring hover (might be keyboard inaccessible)
✅ Navigation menu that works on click/enter
```

## 8. Touch Target Size

### Minimum Sizes (Mobile)

- Interactive elements: **44x44 CSS pixels** minimum
- Adequate spacing between targets: **8px** minimum

### Common Violations

```
❌ Mobile buttons at 32x32px (too small)
✅ Mobile buttons at 48x48px

❌ Links in mobile menu spaced 4px apart (accidental taps)
✅ Links spaced 12px apart

❌ Checkbox at 16x16px on mobile (hard to tap)
✅ Checkbox with expanded tap area 44x44px
```

### Visual Indicators in Mobile Screenshots

- Tiny buttons that would be hard to tap accurately
- Densely packed clickable elements
- Links or buttons too close together

## 9. Responsive Design

### Requirements

- Content readable without horizontal scrolling
- No text truncation
- Proper scaling on different viewports
- No overlapping content

### Common Violations

```
❌ Desktop layout on mobile with horizontal scroll
✅ Mobile-optimized layout with no horizontal scroll

❌ Text cut off at viewport edge
✅ Text wraps properly within viewport

❌ Fixed-width elements overflow on small screens
✅ Flexible/responsive elements scale to screen size

❌ Overlapping elements on mobile (buttons on top of text)
✅ Elements stack vertically with proper spacing
```

### Visual Indicators Across Viewports

When comparing desktop/tablet/mobile screenshots:
- Text that gets cut off on smaller screens
- Overlapping or compressed elements
- Horizontal scrollbars on mobile
- Unreadable small text on mobile

## 10. Color Not Sole Indicator

### Requirements

- Information must not rely on **color alone**
- Use patterns, icons, or text in addition to color

### Common Violations

```
❌ Required fields indicated only by red border
✅ Required fields with red border + "*" icon + "Required" text

❌ Success/error only shown by green/red color
✅ Success/error shown by color + icon + text message

❌ Chart legend with only colored boxes
✅ Chart legend with colored boxes + patterns + labels

❌ Form validation using only red/green highlighting
✅ Form validation with color + icons + error text
```

### Visual Indicators

- Status indicators using only color
- Charts relying solely on color to differentiate data
- Form states indicated only by color changes
- Links distinguished only by color (not underline)

## Visual Analysis Workflow

When analyzing a screenshot for accessibility:

### Step 1: Text and Contrast
1. Check all text for sufficient contrast (4.5:1 for body, 3:1 for large)
2. Verify text is large enough (16px minimum)
3. Check line height and spacing for readability

### Step 2: Interactive Elements
1. Identify all buttons, links, form inputs
2. Verify they have sufficient size (44x44px on mobile)
3. Check for visible focus indicators (if focus state captured)
4. Ensure adequate spacing between targets

### Step 3: Form Elements
1. Check each input has visible label
2. Verify required fields clearly marked (not just color)
3. Look for error messages (should be near inputs)

### Step 4: Structure
1. Check heading hierarchy (visual size progression)
2. Verify logical content flow
3. Look for proper spacing and organization

### Step 5: Responsive Issues
1. Check for text truncation or cutoff
2. Look for overlapping elements
3. Verify no horizontal scroll
4. Ensure touch targets appropriate for viewport

### Step 6: Color Usage
1. Identify any color-only indicators
2. Verify status messages use icons or text too
3. Check charts/graphs have non-color differentiation

## Severity Levels

When reporting accessibility issues from screenshots:

### Critical (P0)
- Contrast ratio < 3:1 for any text
- Missing form labels
- Keyboard trap (if detectable)
- Content not accessible without horizontal scroll

### High (P1)
- Contrast ratio 3:1-4.4:1 for normal text
- Touch targets < 44x44px on mobile
- Heading hierarchy violations
- Color as sole indicator for critical info

### Medium (P2)
- Text size < 14px for body content
- Insufficient spacing between touch targets (< 8px)
- Inconsistent focus indicators
- Minor responsive issues

### Low (P3)
- Line height < 1.4 for long text blocks
- Decorative images possibly missing alt (can't confirm from screenshot)
- Minor visual hierarchy inconsistencies

## Example Analysis Output

```markdown
## Accessibility Issues Found

### Critical (1)
1. **Insufficient color contrast on form labels**
   - Location: Contact form, all input labels
   - Issue: Light gray #AAAAAA on white #FFFFFF (2.6:1 ratio)
   - Requirement: 4.5:1 for normal text
   - Fix: Use darker gray #595959 (7:1 ratio)

### High (2)
1. **Missing visible labels on inputs**
   - Location: Email and password fields
   - Issue: Only placeholder text, no persistent label
   - Fix: Add visible <label> elements above inputs

2. **Touch targets too small on mobile**
   - Location: Social media icons in footer
   - Issue: Icons are 24x24px (below 44x44px minimum)
   - Fix: Increase tap area to 44x44px with padding

### Medium (1)
1. **Body text too small**
   - Location: Article content
   - Issue: 14px font size (recommended 16px minimum)
   - Fix: Increase base font size to 16px
```

## Tools for Automated Checking

While visual analysis is manual, recommend these tools for comprehensive checks:

```typescript
// Integrate axe-core in Playwright tests
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should not have accessibility violations', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

---

**References:**
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Axe DevTools](https://www.deque.com/axe/devtools/)
