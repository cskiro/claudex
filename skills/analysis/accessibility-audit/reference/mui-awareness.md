# MUI Framework Awareness

MUI components have built-in accessibility features. Audit rules MUST account for framework defaults to avoid false positives.

## Component Defaults

### SvgIcon
- **Behavior**: Automatically adds `aria-hidden="true"` when `titleAccess` prop is undefined
- **Source**: `node_modules/@mui/material/SvgIcon/SvgIcon.js`

**Rule**: Do NOT flag MUI icons as missing aria-hidden unless titleAccess is set

```tsx
// Only flag if titleAccess is set (should have aria-label or be visible):
<SvgIcon titleAccess="Icon name" />

// Do NOT flag (auto aria-hidden):
<SearchIcon />
<Timeline />
```

### Alert
- **Behavior**: Defaults to `role="alert"` (assertive live region)

**Rule**: Do NOT recommend adding `role="alert"` - it's already there

```tsx
// Only suggest role="status" if polite announcement is more appropriate:
<Alert severity="success" role="status">Item saved</Alert>
```

### Button
- **Behavior**: Has minimum 36.5px height by default

**Rule**: Usually meets 24x24px target size requirement

```tsx
// Only flag if size="small" or custom sx reduces below 24px:
<Button size="small" sx={{ minHeight: '20px' }} /> // Flag this
<Button>Normal</Button> // Don't flag
```

### TextField
- **Behavior**: Automatically associates label with input via id

**Rule**: Do NOT flag as missing label if `label` prop is provided

```tsx
// This is accessible (auto-associated):
<TextField label="Email" />

// Only flag if no label and no aria-label:
<TextField /> // Flag this
```

### Autocomplete
- **Behavior**: Manages `aria-expanded`, `aria-controls`, `aria-activedescendant`

**Rule**: Do NOT flag ARIA attributes - they're managed by component

```tsx
// All ARIA is handled internally:
<Autocomplete options={options} renderInput={(params) => <TextField {...params} />} />
```

## False Positive Checklist

Before flagging a MUI component violation:

1. [ ] Check if MUI provides default accessibility behavior
2. [ ] Verify the violation exists in rendered output (use browser DevTools)
3. [ ] Test with actual screen reader to confirm issue
4. [ ] Check MUI documentation for accessibility notes

## Common False Positives

| Automated Finding | Why It's False | Reality |
|-------------------|----------------|---------|
| "Icon missing aria-hidden" | MUI adds it automatically | Check rendered HTML |
| "Alert missing role" | Default is role="alert" | Only change if polite needed |
| "Button too small" | 36.5px default height | Check actual rendered size |
| "Input missing label" | TextField manages labels | Check for label prop |
| "Missing aria-expanded" | Autocomplete manages it | Check rendered state |
