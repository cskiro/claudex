# Phase 2: Path Resolution

## Overview

Playwright's screenshot command requires properly formatted `file://` URLs. This phase covers path construction patterns.

## URL Format

Playwright requires URLs, not bare file paths:

```
file:// + absolute_path = valid URL
```

## Path Patterns

### From Current Directory

```bash
# Using $(pwd) for absolute path
playwright screenshot --full-page "file://$(pwd)/diagram.html" output.png
```

### From Absolute Path

```bash
# Direct absolute path
playwright screenshot --full-page "file:///Users/connor/project/diagram.html" output.png
```

### Handling Spaces in Paths

```bash
# Quote the entire URL
playwright screenshot --full-page "file://$(pwd)/my diagram.html" output.png
```

### Relative to Project Root

```bash
# Navigate from any subdirectory
playwright screenshot --full-page "file://$(git rev-parse --show-toplevel)/docs/diagram.html" output.png
```

## Path Validation

Before running conversion, verify the file exists:

```bash
# Check file exists
test -f "diagram.html" && echo "File found" || echo "File not found"

# List HTML files in current directory
ls -la *.html
```

## Anti-Patterns

| Wrong | Correct |
|-------|---------|
| `playwright screenshot diagram.html` | `playwright screenshot "file://$(pwd)/diagram.html"` |
| `playwright screenshot ./diagram.html` | `playwright screenshot "file://$(pwd)/diagram.html"` |
| `playwright screenshot file:diagram.html` | `playwright screenshot "file://$(pwd)/diagram.html"` |

## Next Phase

Once path is resolved, proceed to **Phase 3: Screenshot Capture**.
