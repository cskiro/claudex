# Phase 4: Screenshot Capture & Execution

**Purpose**: Run tests and capture comprehensive visual data

## Steps

### 1. Execute test suite

```bash
npx playwright test --project=chromium --headed=false
```

### 2. Capture screenshots systematically

- Full-page screenshots for layout analysis
- Element-specific screenshots for component testing
- Different viewports (desktop, tablet, mobile)
- Different states (hover, focus, active, disabled)

### 3. Organize screenshot artifacts

- Group by test name
- Add timestamp and viewport metadata
- Generate index file for easy navigation

### 4. Handle failures gracefully

On test failure:
- Capture additional debug screenshots
- Save page HTML snapshot
- Record network activity
- Generate Playwright trace for replay

## Output

Organized screenshot directory with metadata:

```
screenshots/
├── current/
│   ├── home-page-load-2024-01-15T10-30-00.png
│   ├── home-page-after-click-2024-01-15T10-30-05.png
│   └── index.json (metadata)
└── ...
```

## Performance

~30-60 seconds for typical app (5-10 tests)

## Common Issues

**Screenshot capture fails**
- Increase timeout
- Add explicit waits
- Capture partial screenshot on failure

**Tests timeout**
- Check dev server is running
- Increase test timeout
- Add explicit wait conditions

## Transition

Proceed to Phase 5 (Visual Analysis)
