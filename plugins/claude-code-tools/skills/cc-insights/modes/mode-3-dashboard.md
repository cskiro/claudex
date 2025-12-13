# Mode 3: Interactive Dashboard

**When to use**: Rich visual exploration and ongoing monitoring

## Trigger Phrases
- "Launch the insights dashboard"
- "Start the visualization server"
- "Show me the interactive insights"

## Process

1. User asks to start the dashboard
2. Skill launches Next.js dev server
3. Opens browser to http://localhost:3000
4. Provides real-time data from SQLite + ChromaDB

## Dashboard Pages

### Home
- Timeline of recent conversations
- Activity stats and quick metrics
- Summary cards

### Search
- Interactive semantic + keyword search interface
- Real-time results
- Filter by date, files, tools

### Insights
- Auto-generated reports with interactive charts
- Trend visualizations
- Pattern detection results

### Files
- File-centric view of all conversations
- Click to see all conversations touching a file
- Modification frequency heatmap

### Analytics
- Deep-dive into patterns and trends
- Tool usage statistics
- Activity patterns by time of day/week

## Tech Stack

- **Framework**: Next.js 15 with React Server Components
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Data**: SQLite + ChromaDB
- **URL**: http://localhost:3000

## Starting the Dashboard

```bash
# Navigate to dashboard directory
cd ~/.claude/skills/cc-insights/dashboard

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

The browser will automatically open to http://localhost:3000.

## Stopping the Dashboard

Press `Ctrl+C` in the terminal or close the terminal window.
