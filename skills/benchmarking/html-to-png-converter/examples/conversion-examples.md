# Conversion Examples

## Example 1: Academic Diagram

Converting an architecture diagram for a research paper.

**Context**: You have `docs/architecture_diagram.html` and need `docs/architecture_diagram.png`.

```bash
# Navigate to project root
cd /path/to/project

# Convert with full-page capture
playwright screenshot --full-page "file://$(pwd)/docs/architecture_diagram.html" docs/architecture_diagram.png

# Verify dimensions
sips -g pixelHeight -g pixelWidth docs/architecture_diagram.png
```

## Example 2: Bar Chart

Converting a bar chart visualization.

**Context**: You have `docs/loophole_rate_diagram.html` showing experimental results.

```bash
# High-resolution output for publication
playwright screenshot --full-page --scale=2 "file://$(pwd)/docs/loophole_rate_diagram.html" docs/loophole_rate_diagram.png
```

## Example 3: Batch Conversion

Converting all HTML files in a directory.

**Context**: Multiple diagrams in `docs/figures/`.

```bash
# Create output directory
mkdir -p docs/figures/png

# Batch convert all HTML files
for f in docs/figures/*.html; do
  filename=$(basename "$f" .html)
  playwright screenshot --full-page "file://$(pwd)/$f" "docs/figures/png/${filename}.png"
  echo "Converted: $f"
done
```

## Example 4: Dark Mode Variant

Creating light and dark mode versions of a diagram.

```bash
# Light mode (default)
playwright screenshot --full-page "file://$(pwd)/diagram.html" diagram-light.png

# Dark mode
playwright screenshot --full-page --color-scheme=dark "file://$(pwd)/diagram.html" diagram-dark.png
```

## Example 5: From Empathy Experiment

Real example from paralleLLM project:

```bash
# Convert the loophole rate bar chart
playwright screenshot --full-page "file://$(pwd)/docs/loophole_rate_diagram.html" docs/loophole_rate_diagram.png

# Convert architecture pipeline diagram
playwright screenshot --full-page "file://$(pwd)/docs/architecture_diagram_v2.html" docs/architecture_diagram_v2.png
```

## Example 6: With Wait for Animations

When HTML has CSS transitions or animations:

```bash
# Wait 1 second for animations to complete
playwright screenshot --full-page --wait-for-timeout=1000 "file://$(pwd)/animated-diagram.html" output.png
```

## Shell Script for Project Integration

Create a reusable script `scripts/html-to-png.sh`:

```bash
#!/bin/bash
# html-to-png.sh - Convert HTML diagrams to PNG
# Usage: ./scripts/html-to-png.sh <input.html> [output.png]

set -e

INPUT="$1"
OUTPUT="${2:-${INPUT%.html}.png}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <input.html> [output.png]"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT"
  exit 1
fi

echo "Converting: $INPUT -> $OUTPUT"
playwright screenshot --full-page "file://$(pwd)/$INPUT" "$OUTPUT"
echo "Done! Dimensions:"
sips -g pixelHeight -g pixelWidth "$OUTPUT"
```

Make executable:
```bash
chmod +x scripts/html-to-png.sh
```

Use:
```bash
./scripts/html-to-png.sh docs/diagram.html docs/diagram.png
```
