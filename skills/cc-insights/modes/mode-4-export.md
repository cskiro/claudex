# Mode 4: Export and Integration

**When to use**: Share insights or integrate with other tools

## Trigger Phrases
- "Export weekly insights as markdown"
- "Save conversation metadata as JSON"
- "Generate HTML report for sharing"

## Process

1. User asks to export in a specific format
2. Skill generates formatted output
3. Saves to specified location

## Export Formats

### Markdown
Human-readable reports with formatting.

```bash
Export location: ./insights/weekly-report.md
```

### JSON
Machine-readable data for integration with other tools.

```json
{
  "period": "2025-10-19 to 2025-10-25",
  "conversations": 12,
  "files_modified": 23,
  "tool_uses": 45,
  "top_files": [
    {"path": "src/auth/token.ts", "count": 5},
    {"path": "src/components/Login.tsx", "count": 3}
  ],
  "topics": ["authentication", "testing", "bug fixes"]
}
```

### CSV
Activity data for spreadsheets.

```csv
date,conversation_count,files_modified,tool_uses
2025-10-19,4,8,12
2025-10-20,3,6,9
...
```

### HTML
Standalone report with styling for sharing.

```html
<!-- Self-contained report with inline CSS -->
<!-- Can be opened in any browser -->
```

## Example Usage

```
User: "Export this month's insights as JSON for my dashboard"

Skill: [Generates JSON report]
Exported to: ./insights/october-2025.json
Contains: 45 conversations, 89 files, 156 tool uses
```
