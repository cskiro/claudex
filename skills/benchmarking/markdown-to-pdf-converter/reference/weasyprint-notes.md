# WeasyPrint CSS Compatibility Notes

WeasyPrint doesn't support all CSS properties. This reference documents what works and what doesn't.

## Supported (Works)

### Layout
- `max-width`, `min-width` (but avoid min-width on images)
- `margin`, `padding`
- `display: block`, `display: inline-block`
- `text-align`
- `width`, `height` (with units)

### Typography
- `font-family`, `font-size`, `font-weight`, `font-style`
- `line-height`
- `color`

### Tables
- `border-collapse`
- `border` properties
- `padding` on cells

### Print/Page
- `@page { margin: ... }`
- `page-break-before`, `page-break-after`, `page-break-inside`
- `orphans`, `widows`

### Backgrounds
- `background-color`
- `background` (simple)

## NOT Supported (Ignored)

### Modern CSS
- `gap` (use margin instead)
- `overflow-x`, `overflow-y`
- CSS Grid layout
- Flexbox (limited support)
- CSS variables (`--custom-property`)
- `min()`, `max()`, `clamp()` functions

### Advanced Selectors
- `:has()` (limited)
- Complex pseudo-selectors

## Common Warnings

```
WARNING: Ignored `gap: min(4vw, 1.5em)` at X:Y, invalid value.
WARNING: Ignored `overflow-x: auto` at X:Y, unknown property.
```

These warnings are informational and don't affect the output. The CSS fallbacks handle them.

## Image Centering Pattern

WeasyPrint-compatible centering:

```html
<!-- This works -->
<figure style="margin: 2em auto; text-align: center;">
  <img style="max-width: 100%; display: inline-block;">
</figure>

<!-- This does NOT work reliably -->
<figure style="display: flex; justify-content: center;">
  <img>
</figure>
```

## Page Break Pattern

```html
<!-- Explicit page break -->
<div style="page-break-before: always;"></div>

<!-- Keep together -->
<div style="page-break-inside: avoid;">
  Content that should stay together
</div>
```
