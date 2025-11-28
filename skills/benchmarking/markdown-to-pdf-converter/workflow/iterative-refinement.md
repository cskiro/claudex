# Iterative PDF Refinement Workflow

Step-by-step process for tuning page breaks and layout in complex documents.

## Phase 1: Initial Conversion

```bash
# Generate HTML with CSS
pandoc document.md -o document.html --standalone --css=pdf-style.css

# Generate PDF
weasyprint document.html document.pdf
```

## Phase 2: Review PDF

Open the PDF and check for:

1. **Orphaned headings** - Heading at bottom of page, content on next
2. **Split tables** - Table breaks across pages
3. **Cut-off images** - Image doesn't fit, gets cropped
4. **Excessive whitespace** - Large gaps from unnecessary page breaks
5. **Off-center figures** - Images aligned left instead of center

## Phase 3: Fix Issues

### Orphaned Headings
CSS already handles this with `page-break-after: avoid`. If still occurring, add manual page break BEFORE the heading:

```html
<div style="page-break-before: always;"></div>

### Section Title
```

### Split Tables
Add to the table's container:
```html
<div style="page-break-inside: avoid;">

| Column 1 | Column 2 |
|----------|----------|
| data     | data     |

</div>
```

### Cut-off Images
Remove any `min-width` constraints. Use only:
```html
<img style="max-width: 100%; height: auto;">
```

### Excessive Whitespace
Remove unnecessary `<div style="page-break-before: always;">` tags. Let content flow naturally and only add page breaks where truly needed.

### Off-center Figures
Use the full figure pattern:
```html
<figure style="margin: 2em auto; page-break-inside: avoid; text-align: center;">
  <img src="image.png" style="max-width: 100%; height: auto; display: inline-block;">
  <figcaption style="text-align: center; font-style: italic; margin-top: 1em;">
    Figure N: Caption
  </figcaption>
</figure>
```

## Phase 4: Regenerate and Verify

```bash
# Regenerate after each fix
pandoc document.md -o document.html --standalone --css=pdf-style.css
weasyprint document.html document.pdf
```

Repeat until all issues resolved.

## Tips

1. **Work section by section** - Don't try to fix everything at once
2. **Check page count** - Unnecessary page breaks inflate page count
3. **Test at actual print size** - View at 100% zoom
4. **Version your PDFs** - Keep v1.0, v1.1, etc. during refinement
