# Phase 4: Manual Validation

These checks CANNOT be automated and require human judgment.

## 1. Color Contrast Validation

**Tool**: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Process
1. Extract all colors from theme configuration
2. Calculate contrast ratios for each text/background pair
3. Document results in gap report

### Requirements
| Element Type | Minimum Ratio |
|--------------|---------------|
| Normal text (< 18pt) | 4.5:1 |
| Large text (>= 18pt or 14pt bold) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

### Severity by Element
- Primary CTA button low contrast = **CRITICAL**
- Body text low contrast = **HIGH**
- Footer link low contrast = **MEDIUM**
- Decorative text low contrast = **LOW**

## 2. Keyboard Navigation Testing

### Basic Test
1. Start at top of page
2. Press Tab repeatedly through all interactive elements
3. Verify:
   - [ ] Logical order (left-to-right, top-to-bottom)
   - [ ] No keyboard traps (can always Tab away)
   - [ ] All functionality accessible
   - [ ] Focus indicator visible on every element

### Key Combinations to Test
| Key | Expected Behavior |
|-----|-------------------|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous focusable element |
| Enter | Activate buttons/links |
| Space | Activate buttons, toggle checkboxes |
| Escape | Close modals/menus |
| Arrow keys | Navigate within components (menus, tabs) |

### Common Keyboard Traps
- Modal dialogs without Escape handling
- Date pickers without keyboard support
- Custom dropdowns that don't cycle

## 3. Screen Reader Testing

### Recommended Tools
- **Mac**: VoiceOver (built-in, Cmd+F5)
- **Windows**: NVDA (free), JAWS (paid)
- **iOS**: VoiceOver (built-in)
- **Android**: TalkBack (built-in)

### What to Test
1. **Landmarks**: Header, nav, main, footer announced
2. **Headings**: Logical hierarchy (h1 → h2 → h3)
3. **Forms**: Labels announced, errors read
4. **Dynamic content**: Status messages announced
5. **Images**: Alt text read appropriately

### VoiceOver Commands (Mac)
| Command | Action |
|---------|--------|
| VO + Right Arrow | Next element |
| VO + Left Arrow | Previous element |
| VO + U | Open rotor (landmarks, headings, links) |
| VO + Space | Activate |

## 4. Zoom and Reflow Testing

### 200% Zoom Test
1. Browser zoom to 200%
2. Verify:
   - [ ] No horizontal scrolling
   - [ ] No text truncation
   - [ ] No overlapping elements
   - [ ] All functionality accessible

### 320px Width Test (Mobile Reflow)
1. Resize browser to 320px width
2. Verify:
   - [ ] Content reflows to single column
   - [ ] No horizontal scroll
   - [ ] Touch targets still accessible
   - [ ] Text remains readable

## 5. WCAG Interpretation Decisions

Some criteria require human judgment:

### 2.4.5 Multiple Ways
- **Question**: Is this a "set of Web pages"?
- **If < 3 pages**: Likely exempt
- **If >= 3 pages**: Need 2+ navigation methods

### 3.2.6 Consistent Help
- **Question**: Does a help mechanism exist?
- **If no help exists**: Compliant (no requirement)
- **If help exists**: Must be consistently placed

### 1.3.5 Identify Input Purpose
- **Question**: Is this collecting user data from the 53 specified purposes?
- Search inputs: **NOT** in scope
- User email/phone: **IN** scope

## Checklist

- [ ] All color combinations checked against contrast requirements
- [ ] Full keyboard navigation test completed
- [ ] Screen reader testing with at least one tool
- [ ] 200% zoom test passed
- [ ] 320px reflow test passed
- [ ] Applicability decisions documented

## Next Step

Proceed to [Report Generation](reporting.md)
