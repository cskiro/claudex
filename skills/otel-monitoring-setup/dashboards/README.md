# Grafana Dashboard Templates

This directory contains pre-configured Grafana dashboards for Claude Code telemetry.

## Available Dashboards

### 1. claude-code-overview.json
**Comprehensive dashboard with all key metrics**

**Panels:**
- Total Lines of Code (all-time counter)
- Total Cost (24h rolling window)
- Total Tokens (24h rolling window)
- Active Time (24h rolling window)
- Cost Over Time (per hour rate)
- Token Usage by Type (stacked timeseries)
- Lines of Code Modified (bar chart)
- Commits Created (24h counter)

**Metrics Used:**
- `claude_code_claude_code_lines_of_code_count_total`
- `claude_code_claude_code_cost_usage_USD_total`
- `claude_code_claude_code_token_usage_tokens_total`
- `claude_code_claude_code_active_time_seconds_total`
- `claude_code_claude_code_commit_count_total`

**Note:** This dashboard uses the correct double-prefix metric names.

### 2. claude-code-simple.json
**Simplified dashboard for quick overview**

**Panels:**
- Active Sessions
- Total Cost (24h)
- Total Tokens (24h)
- Active Time (24h)
- Cost Over Time
- Token Usage by Type

**Use Case:** Lightweight dashboard for basic monitoring without detailed breakdowns.

## Importing Dashboards

### Method 1: Grafana UI (Recommended)

1. Access Grafana: http://localhost:3000
2. Login with admin/admin
3. Go to: Dashboards → New → Import
4. Click "Upload JSON file"
5. Select the dashboard JSON file
6. Click "Import"

### Method 2: Grafana API

```bash
# Get the datasource UID first
DATASOURCE_UID=$(curl -s -u admin:admin http://localhost:3000/api/datasources | jq -r '.[] | select(.type=="prometheus") | .uid')

# Update dashboard with correct UID
cat claude-code-overview.json | jq --arg uid "$DATASOURCE_UID" '
  walk(if type == "object" and .datasource.type == "prometheus" then .datasource.uid = $uid else . end)
' > dashboard-updated.json

# Import dashboard
curl -X POST http://localhost:3000/api/dashboards/db \
  -u admin:admin \
  -H "Content-Type: application/json" \
  -d @dashboard-updated.json
```

## Datasource UID Configuration

**Important:** The dashboards have a hardcoded Prometheus datasource UID: `PBFA97CFB590B2093`

If your Grafana instance has a different UID, you need to replace it:

```bash
# Find your datasource UID
curl -s -u admin:admin http://localhost:3000/api/datasources | jq '.[] | select(.type=="prometheus") | {name, uid}'

# Replace UID in dashboard
YOUR_UID="YOUR_ACTUAL_UID_HERE"
cat claude-code-overview.json | sed "s/PBFA97CFB590B2093/$YOUR_UID/g" > claude-code-overview-fixed.json

# Import the fixed version
```

The skill handles this automatically during Mode 1 setup!

## Customizing Dashboards

### Adding Custom Panels

Use these PromQL queries as templates:

**Total Tokens by Model:**
```promql
sum by (model) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))
```

**Cost per Session:**
```promql
increase(claude_code_claude_code_cost_usage_USD_total[24h])
/
increase(claude_code_claude_code_session_count_total[24h])
```

**Lines of Code per Hour:**
```promql
rate(claude_code_claude_code_lines_of_code_count_total[5m]) * 3600
```

**Average Session Duration:**
```promql
increase(claude_code_claude_code_active_time_seconds_total[24h])
/
increase(claude_code_claude_code_session_count_total[24h])
```

### Time Range Recommendations

- **Real-time monitoring:** Last 15 minutes, 30s refresh
- **Daily review:** Last 24 hours, 1m refresh
- **Weekly analysis:** Last 7 days, 5m refresh
- **Monthly reports:** Last 30 days, 15m refresh

## Troubleshooting

### Dashboard Shows "No Data"

1. **Check data source connection:**
   ```bash
   curl -s http://localhost:3000/api/health | jq .
   ```

2. **Verify Prometheus has data:**
   ```bash
   curl -s 'http://localhost:9090/api/v1/label/__name__/values' | jq . | grep claude_code
   ```

3. **Check metric naming:**
   - Ensure queries use double prefix: `claude_code_claude_code_*`
   - Not single prefix: `claude_code_*`

### Dashboard Shows "Datasource Not Found"

- Your datasource UID doesn't match the dashboard
- Follow the "Datasource UID Configuration" section above

### Panels Show Different Time Ranges

- Set dashboard time range at top-right
- Individual panels inherit from dashboard unless overridden
- Check panel settings: Edit → Query Options → Time Range

## Additional Resources

- **Metric Reference:** See `../data/metrics-reference.md`
- **PromQL Queries:** See `../data/prometheus-queries.md`
- **Grafana Docs:** https://grafana.com/docs/grafana/latest/
