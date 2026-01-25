# Common UI Bugs - Visual Analysis Guide

Patterns and indicators for identifying UI bugs from screenshots during LLM-powered visual analysis.

## Layout Issues

### 1. Overlapping Elements

**Visual Indicators:**
- Text overlapping other text
- Buttons overlapping images or other buttons
- Content extending beyond container boundaries
- Z-index issues causing incorrect stacking

**Examples:**
```
❌ Modal dialog overlapped by dropdown menu
❌ Footer content overlapping main content
❌ Notification banner covering navigation
❌ Search results hidden behind fixed header
```

**Screenshot Analysis:**
- Look for any elements that appear on top of others unexpectedly
- Check if all content is fully visible and not obscured
- Verify layering makes sense (modals on top, backgrounds behind)

### 2. Text Truncation / Overflow

**Visual Indicators:**
- Text cut off mid-word or mid-letter
- Ellipsis (...) in unexpected places
- Content extending outside visible area
- Horizontal scrollbars on text containers

**Examples:**
```
❌ Button text: "Continue to Chec..." (truncated on mobile)
❌ Table header: "Customer N..." instead of "Customer Name"
❌ Card title cut off at viewport edge
❌ Long email addresses broken into random positions
```

**Screenshot Analysis:**
- Check if all text is fully visible
- Look for truncation indicators (...)
- Verify important text isn't cut off
- Check if text wraps properly on smaller viewports

### 3. Broken Grid/Flexbox Layouts

**Visual Indicators:**
- Cards or items with inconsistent sizes
- Uneven spacing between elements
- Elements not aligned in columns/rows
- One element significantly larger/smaller than siblings

**Examples:**
```
❌ Product grid: 3 cards same height, 1 card twice as tall
❌ Navigation items: uneven spacing (10px, 20px, 15px)
❌ Form inputs: labels misaligned with inputs
❌ Cards: some with images, some without, causing height mismatch
```

**Screenshot Analysis:**
- Check if grid items are evenly sized
- Verify consistent spacing between elements
- Look for alignment issues in rows/columns
- Identify items breaking out of grid structure

### 4. Responsive Breakpoint Issues

**Visual Indicators (comparing viewport sizes):**
- Desktop layout on mobile (very small text, horizontal scroll)
- Mobile layout on desktop (everything too large, wasted space)
- Sudden jumps in layout between similar viewport sizes
- Media queries not triggering at expected breakpoints

**Examples:**
```
❌ Desktop: 3-column layout → Mobile: Still 3 columns (too cramped)
✅ Desktop: 3-column layout → Tablet: 2 columns → Mobile: 1 column

❌ Desktop: 16px text → Mobile: 16px text (too small on small screen)
✅ Desktop: 16px text → Mobile: 14px text with increased line height

❌ Fixed sidebar pushes main content off screen on tablet
✅ Sidebar collapses to hamburger menu on tablet
```

**Screenshot Analysis:**
- Compare same page across desktop (1280px+), tablet (768px), mobile (375px)
- Check if layout adapts appropriately at each size
- Verify no horizontal scrolling on mobile
- Ensure touch targets are 44x44px minimum on mobile

## Component-Specific Issues

### 5. Form Validation Problems

**Visual Indicators:**
- Error messages in wrong location (far from input)
- No visible error state (input looks normal despite error)
- Success state not clearly indicated
- Disabled buttons without indication why

**Examples:**
```
❌ Error message at top of page, input in middle (hard to associate)
✅ Error message directly below relevant input

❌ Invalid input: red border only (color-blind users miss it)
✅ Invalid input: red border + error icon + error text

❌ Submit button disabled, no explanation why
✅ Submit button disabled with tooltip "Complete required fields"

❌ Multiple validation errors shown as one generic message
✅ Each field shows its specific error message
```

**Screenshot Analysis:**
- Check if error states are clearly visible
- Verify error messages are near their inputs
- Look for validation indicators beyond just color
- Confirm required fields are clearly marked

### 6. Button States

**Visual Indicators:**
- Active/hover/focus states indistinguishable
- Disabled buttons look clickable
- Primary vs secondary buttons unclear
- Loading/submitting state not indicated

**Examples:**
```
❌ Disabled button: gray text on light gray (looks clickable)
✅ Disabled button: clear visual indication (opacity, cursor, label)

❌ Primary and secondary buttons identical appearance
✅ Primary: bold color, secondary: outline only

❌ Button clicked but no loading indicator (looks broken)
✅ Button shows spinner or "Loading..." text when clicked

❌ Hover state same as default state (no feedback)
✅ Hover state: darker background or subtle animation
```

**Screenshot Analysis:**
- Verify different button states are visually distinct
- Check if disabled buttons clearly look non-interactive
- Look for visual feedback on interactive states
- Ensure primary actions are visually prominent

### 7. Image Loading Issues

**Visual Indicators:**
- Broken image icons (usually a small icon or alt text)
- Missing images (blank space where image should be)
- Images with wrong aspect ratio (stretched/squashed)
- Low-resolution images appearing pixelated

**Examples:**
```
❌ Product image slot shows broken image icon
❌ Profile picture area: empty circle (image failed to load)
❌ Banner image: 16:9 image stretched to 1:1 (distorted)
❌ Thumbnail: tiny image scaled up 3x (pixelated)
```

**Screenshot Analysis:**
- Look for broken image indicators
- Check if all images loaded successfully
- Verify images maintain proper aspect ratios
- Identify pixelated or low-quality images

### 8. Table/List Issues

**Visual Indicators:**
- Headers not aligned with columns
- Inconsistent row heights
- Text overflow in cells
- Missing borders or inconsistent borders
- Poor mobile table handling (horizontal scroll)

**Examples:**
```
❌ Table headers offset from column data
❌ One row 2x height of others (content wrapping differently)
❌ Cell content: "john.doe@verylongemailaddr..." (truncated)
❌ Mobile table: requires horizontal scroll to see all columns
```

**Screenshot Analysis:**
- Verify column headers align with data
- Check for consistent row heights
- Look for text overflow in cells
- Ensure tables are readable on mobile (responsive design)

## Content Issues

### 9. Missing Content

**Visual Indicators:**
- Empty sections (just headers, no content)
- Placeholder text in production ("Lorem ipsum", "TBD", "Coming soon")
- Missing images or icons where expected
- Incomplete sentences or paragraphs

**Examples:**
```
❌ Section header "Latest Articles" with no articles below
❌ Product description: "Lorem ipsum dolor sit amet..."
❌ Icon placeholder: gray square instead of actual icon
❌ Bio section: ends mid-sentence
```

**Screenshot Analysis:**
- Identify any placeholder content
- Look for empty sections or containers
- Check if all expected content is present
- Verify no incomplete text

### 10. Inconsistent Spacing/Padding

**Visual Indicators:**
- Uneven margins between sections
- Inconsistent padding inside containers
- Elements touching edges (no breathing room)
- Random spacing that doesn't follow a system

**Examples:**
```
❌ Section 1: 40px margin → Section 2: 25px margin → Section 3: 35px
✅ All sections: consistent 40px margin

❌ Card padding: 16px top, 20px right, 14px bottom, 18px left
✅ Card padding: 16px all sides

❌ Button text touching button edge (no padding)
✅ Button: 12px vertical, 20px horizontal padding
```

**Screenshot Analysis:**
- Check for consistent spacing throughout page
- Verify elements have appropriate padding
- Look for crowded areas with insufficient spacing
- Identify spacing that breaks visual rhythm

## Typography Issues

### 11. Font Rendering Problems

**Visual Indicators:**
- Jagged or pixelated text
- Text weight too thin (hard to read)
- Inconsistent font families
- Line height too tight or too loose

**Examples:**
```
❌ Body text: font-weight 100 (barely visible)
✅ Body text: font-weight 400 (readable)

❌ Headings: Arial → Body: Times New Roman (inconsistent)
✅ All text: consistent font family

❌ Long paragraph: line-height 1.0 (text touching)
✅ Long paragraph: line-height 1.5 (readable spacing)
```

**Screenshot Analysis:**
- Check if text is crisp and readable
- Verify consistent font families
- Look for appropriate line height (1.4-1.6 for body text)
- Ensure font weights are accessible

### 12. Text Alignment Issues

**Visual Indicators:**
- Center-aligned paragraphs (hard to read)
- Inconsistent alignment within a section
- Right-aligned text in LTR layout without reason
- Justified text with large gaps

**Examples:**
```
❌ Long paragraph: center-aligned (hard to follow)
✅ Long paragraph: left-aligned

❌ Form: labels left-aligned, some center-aligned randomly
✅ Form: all labels consistently left-aligned

❌ Justified text: large gaps between words ("rivers")
✅ Left-aligned text with ragged right edge
```

**Screenshot Analysis:**
- Check if alignment aids readability
- Verify consistent alignment within sections
- Look for awkward gaps in justified text
- Ensure alignment makes sense for content type

## Interactive Element Issues

### 13. Hover/Focus States Missing

**Note:** Only detectable if screenshot captures focused/hovered state

**Visual Indicators:**
- Link looks identical to surrounding text (no underline, same color)
- Focused input indistinguishable from unfocused
- Hovered button shows no change
- Dropdown menu items don't highlight on hover

**Examples:**
```
❌ Link: blue text, no underline, same as normal text
✅ Link: blue text with underline, or different color

❌ Input focused: looks identical to unfocused state
✅ Input focused: blue border or outline appears

❌ Menu item hovered: no visual change
✅ Menu item hovered: background color change
```

**Screenshot Analysis (if interactive state captured):**
- Verify interactive elements show visual feedback
- Check if focused element has clear indicator
- Look for hover states that provide feedback
- Ensure keyboard focus is visible

### 14. Icon Issues

**Visual Indicators:**
- Icons misaligned with text
- Icons wrong size (too large or too small)
- Icons wrong color (low contrast, invisible)
- Icon-only buttons without labels or tooltips

**Examples:**
```
❌ Icon button: 16x16px icon in 48x48px button (looks lost)
✅ Icon button: 24x24px icon in 48x48px button (balanced)

❌ Icon: white on light gray background (barely visible)
✅ Icon: dark gray on light gray (clear contrast)

❌ Icon: baseline-aligned with text (appears raised)
✅ Icon: center-aligned with text

❌ Icon-only button with no label (unclear purpose)
✅ Icon button with aria-label or visible text label
```

**Screenshot Analysis:**
- Check if icons are appropriately sized
- Verify icons have sufficient contrast
- Look for proper alignment with adjacent text
- Ensure icon buttons have clear purpose

## Color and Theme Issues

### 15. Dark Mode Issues

**Visual Indicators (when comparing light/dark screenshots):**
- White text on light background (inverted incorrectly)
- Hard-coded colors not switching with theme
- Images/logos with wrong theme variant
- Insufficient contrast in dark mode

**Examples:**
```
❌ Dark mode: #333 text on #000 background (low contrast)
✅ Dark mode: #E0E0E0 text on #1A1A1A background

❌ Light mode logo on dark background (invisible)
✅ Dark mode variant logo displayed

❌ Input background: white in both modes (wrong in dark)
✅ Input background: white in light, #2A2A2A in dark
```

**Screenshot Analysis (compare light/dark if available):**
- Verify all colors invert appropriately
- Check contrast ratios in both modes
- Look for hard-coded colors that don't adapt
- Ensure images/logos have correct variants

### 16. Brand Color Misuse

**Visual Indicators:**
- Too many competing colors
- Brand colors used incorrectly (primary for everything)
- Status colors confusing (green for error, red for success)
- Inaccessible color combinations

**Examples:**
```
❌ All buttons primary color (no hierarchy)
✅ Primary button: brand color, secondary: gray/outline

❌ Success message in red, error in green (confusing)
✅ Success in green, error in red, warning in amber

❌ 8 different colors used on one page (chaotic)
✅ Consistent color palette: 2-3 main colors + neutrals
```

**Screenshot Analysis:**
- Check if color usage is consistent and meaningful
- Verify status colors match conventions (green=success, red=error)
- Look for excessive color variety
- Ensure brand colors used appropriately

## Animation and Transition Issues

**Note:** Difficult to detect from static screenshots, but can infer

### 17. Loading States

**Visual Indicators:**
- Content area completely empty (no skeleton/spinner)
- "Loading..." text with no visual indicator
- Sudden content appearance (jarring)
- Infinite loading (screenshot shows spinner forever)

**Examples:**
```
❌ Empty white space while loading (looks broken)
✅ Skeleton UI placeholders during load

❌ Just text "Loading..." (static, looks stuck)
✅ Animated spinner + "Loading..." text

❌ Screenshot from 30 seconds ago: still loading (timeout issue)
✅ Content loads within reasonable time (< 3 seconds)
```

**Screenshot Analysis:**
- Look for loading indicators
- Check if empty states have placeholders
- Identify potential timeout issues (loading too long)

## Mobile-Specific Issues

### 18. Fixed Positioning Problems

**Visual Indicators:**
- Fixed header covering content (not enough top padding)
- Fixed footer hiding interactive elements
- Input fields hidden behind keyboard (inferred)
- Fixed elements overlapping each other

**Examples:**
```
❌ Fixed header: covers first line of content
✅ Content has top padding equal to header height

❌ Fixed "Chat with us" button: covers form submit button
✅ Fixed button repositions when other content appears

❌ Input field: likely behind keyboard when focused
✅ Page scrolls input into view above keyboard
```

**Screenshot Analysis (mobile viewports):**
- Check if fixed headers leave room for content
- Verify fixed elements don't overlap important content
- Look for sufficient padding to account for fixed elements

### 19. Orientation Issues

**Visual Indicators (portrait vs landscape):**
- Content cut off in landscape mode
- Poor use of available space in landscape
- Fixed height elements that don't adapt
- Horizontal layout forced into vertical space

**Examples:**
```
❌ Portrait: shows full content → Landscape: content cut off
✅ Both orientations show full content

❌ Landscape: wide empty margins, cramped center content
✅ Landscape: content uses available width appropriately
```

**Screenshot Analysis (if both orientations available):**
- Compare same page in portrait and landscape
- Verify content adapts to available space
- Check if all content remains accessible

## Analysis Priority

When analyzing screenshots, prioritize issues by impact:

### Critical (Stop immediately)
1. Content completely missing or invisible
2. Major layout breaks (overlapping, off-screen)
3. Severe contrast violations (< 3:1)
4. Broken images or core UI elements

### High (Fix soon)
1. Text truncation losing important info
2. Form validation not visible
3. Responsive breakpoint failures
4. Touch targets too small (< 44px)

### Medium (Fix in next iteration)
1. Inconsistent spacing
2. Minor alignment issues
3. Missing hover/focus states
4. Moderate contrast issues (3:1-4.4:1)

### Low (Polish)
1. Minor typography inconsistencies
2. Slight spacing irregularities
3. Non-critical icon sizing
4. Subtle animation issues

## Generating Bug Reports

For each issue found, provide:

```markdown
### [Issue Title]

**Severity**: Critical | High | Medium | Low

**Location**: [Specific page/component where visible]

**Screenshot**: `path/to/screenshot.png` (timestamp: YYYY-MM-DD HH:MM:SS)

**Viewport**: Desktop 1280x720 | Tablet 768x1024 | Mobile 375x667

**Description**: [Clear description of what's wrong]

**Expected Behavior**: [What should appear instead]

**Likely Cause**: [Technical reason, e.g., "Missing max-width constraint", "Improper flexbox configuration"]

**Recommended Fix**:
- **File**: `src/components/Button.tsx`
- **Line**: 45
- **Current**: \`className="px-4 text-xl"\`
- **Fixed**: \`className="px-4 text-sm sm:text-base md:text-xl max-w-full"\`
- **Reasoning**: Text size needs responsive scaling and max-width to prevent overflow on mobile
```

---

**Remember**: Focus on bugs that impact **usability** and **accessibility**. Not every minor imperfection is critical. Prioritize issues that prevent users from completing tasks or accessing content.
