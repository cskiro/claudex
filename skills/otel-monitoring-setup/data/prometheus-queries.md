# Useful Prometheus Queries (PromQL)

Collection of useful PromQL queries for Claude Code telemetry analysis.

**Note:** All queries use the double prefix: `claude_code_claude_code_*`

---

## Cost Analysis

### Daily Cost Trend
```promql
sum(increase(claude_code_claude_code_cost_usage_USD_total[1d]))
```

### Cost by Model
```promql
sum by (model) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

### Cost per Hour (Rate)
```promql
rate(claude_code_claude_code_cost_usage_USD_total[5m]) * 3600
```

### Average Cost per Session
```promql
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))
/
sum(increase(claude_code_claude_code_session_count_total[24h]))
```

### Cumulative Monthly Cost
```promql
sum(increase(claude_code_claude_code_cost_usage_USD_total[30d]))
```

### Cost by Team
```promql
sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

### Projected Monthly Cost (based on last 7 days)
```promql
(sum(increase(claude_code_claude_code_cost_usage_USD_total[7d])) / 7) * 30
```

---

## Token Usage

### Total Tokens by Type
```promql
sum by (type) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))
```

### Tokens by Model
```promql
sum by (model) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))
```

### Cache Hit Rate
```promql
sum(increase(claude_code_claude_code_token_usage_tokens_total{type="cache_read"}[24h]))
/
sum(increase(claude_code_claude_code_token_usage_tokens_total{type=~"input|cache_creation|cache_read"}[24h]))
* 100
```

### Input vs Output Token Ratio
```promql
sum(increase(claude_code_claude_code_token_usage_tokens_total{type="input"}[24h]))
/
sum(increase(claude_code_claude_code_token_usage_tokens_total{type="output"}[24h]))
```

### Token Usage Rate (per minute)
```promql
sum by (type) (rate(claude_code_claude_code_token_usage_tokens_total[5m]) * 60)
```

### Total Tokens (All Time)
```promql
sum(claude_code_claude_code_token_usage_tokens_total)
```

---

## Productivity Metrics

### Total Lines of Code Modified
```promql
sum(claude_code_claude_code_lines_of_code_count_total)
```

### LOC by Type (Added, Changed, Deleted)
```promql
sum by (type) (increase(claude_code_claude_code_lines_of_code_count_total[24h]))
```

### LOC per Hour
```promql
rate(claude_code_claude_code_lines_of_code_count_total[5m]) * 3600
```

### Lines per Dollar (Efficiency)
```promql
sum(increase(claude_code_claude_code_lines_of_code_count_total[24h]))
/
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

### Commits per Day
```promql
increase(claude_code_claude_code_commit_count_total[24h])
```

### PRs per Week
```promql
increase(claude_code_claude_code_pr_count_total[7d])
```

### LOC per Commit
```promql
sum(increase(claude_code_claude_code_lines_of_code_count_total[24h]))
/
sum(increase(claude_code_claude_code_commit_count_total[24h]))
```

---

## Session Analytics

### Total Sessions
```promql
sum(claude_code_claude_code_session_count_total)
```

### New Sessions (24h)
```promql
increase(claude_code_claude_code_session_count_total[24h])
```

### Active Users (Unique account_uuids)
```promql
count(count by (account_uuid) (claude_code_claude_code_session_count_total))
```

### Average Session Duration
```promql
sum(increase(claude_code_claude_code_active_time_seconds_total[24h]))
/
sum(increase(claude_code_claude_code_session_count_total[24h]))
/ 60
```
*Result in minutes*

### Total Active Hours (24h)
```promql
sum(increase(claude_code_claude_code_active_time_seconds_total[24h])) / 3600
```

### Sessions by Version
```promql
sum by (version) (increase(claude_code_claude_code_session_count_total[24h]))
```

---

## Team Aggregation

### Cost by Team (Last 24h)
```promql
sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

### LOC by Team (Last 24h)
```promql
sum by (team) (increase(claude_code_claude_code_lines_of_code_count_total[24h]))
```

### Active Users per Team
```promql
count by (team) (count by (team, account_uuid) (claude_code_claude_code_session_count_total))
```

### Team Efficiency (LOC per Dollar)
```promql
sum by (team) (increase(claude_code_claude_code_lines_of_code_count_total[24h]))
/
sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

### Top Spending Teams (Last 7 days)
```promql
topk(5, sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[7d])))
```

---

## Model Comparison

### Cost by Model (Pie Chart)
```promql
sum by (model) (increase(claude_code_claude_code_cost_usage_USD_total[7d]))
```

### Token Efficiency by Model (Tokens per Dollar)
```promql
sum by (model) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))
/
sum by (model) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

### Most Used Model
```promql
topk(1, sum by (model) (increase(claude_code_claude_code_token_usage_tokens_total[24h])))
```

### Model Usage Distribution (%)
```promql
sum by (model) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))
/
sum(increase(claude_code_claude_code_token_usage_tokens_total[24h]))
* 100
```

---

## Alerting Queries

### High Daily Cost Alert (> $50)
```promql
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h])) > 50
```

### Cost Spike Alert (50% increase compared to yesterday)
```promql
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))
/
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h] offset 24h))
> 1.5
```

### No Activity Alert (no sessions in last hour)
```promql
increase(claude_code_claude_code_session_count_total[1h]) == 0
```

### Low Cache Hit Rate Alert (< 20%)
```promql
(
  sum(increase(claude_code_claude_code_token_usage_tokens_total{type="cache_read"}[1h]))
  /
  sum(increase(claude_code_claude_code_token_usage_tokens_total{type=~"input|cache_creation|cache_read"}[1h]))
  * 100
) < 20
```

---

## Forecasting

### Projected Monthly Cost (based on last 7 days)
```promql
(sum(increase(claude_code_claude_code_cost_usage_USD_total[7d])) / 7) * 30
```

### Projected Annual Cost (based on last 30 days)
```promql
(sum(increase(claude_code_claude_code_cost_usage_USD_total[30d])) / 30) * 365
```

### Average Daily Cost (Last 30 days)
```promql
sum(increase(claude_code_claude_code_cost_usage_USD_total[30d])) / 30
```

### Growth Rate (Week over Week)
```promql
(
  sum(increase(claude_code_claude_code_cost_usage_USD_total[7d]))
  -
  sum(increase(claude_code_claude_code_cost_usage_USD_total[7d] offset 7d))
)
/
sum(increase(claude_code_claude_code_cost_usage_USD_total[7d] offset 7d))
* 100
```
*Result as percentage*

---

## Debugging Queries

### Check if Metrics Exist
```promql
claude_code_claude_code_session_count_total
```

### List All Claude Code Metrics
```
# Use Prometheus UI or API
curl -s 'http://localhost:9090/api/v1/label/__name__/values' | jq . | grep claude_code
```

### Check Metric Labels
```promql
# Returns all label combinations
count by (account_uuid, version, team, environment) (claude_code_claude_code_session_count_total)
```

### Latest Value for All Metrics
```promql
# Session count
claude_code_claude_code_session_count_total

# Cost
claude_code_claude_code_cost_usage_USD_total

# Tokens
claude_code_claude_code_token_usage_tokens_total

# LOC
claude_code_claude_code_lines_of_code_count_total
```

### Metrics Cardinality (Number of Time Series)
```promql
count(claude_code_claude_code_token_usage_tokens_total)
```

---

## Recording Rules

Save these as Prometheus recording rules for faster dashboard queries:

```yaml
groups:
  - name: claude_code_aggregations
    interval: 1m
    rules:
      # Daily cost
      - record: claude_code:cost_usd:daily
        expr: sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))

      # Cost by team
      - record: claude_code:cost_usd:daily:by_team
        expr: sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))

      # Cache hit rate
      - record: claude_code:cache_hit_rate:daily
        expr: |
          sum(increase(claude_code_claude_code_token_usage_tokens_total{type="cache_read"}[24h]))
          /
          sum(increase(claude_code_claude_code_token_usage_tokens_total{type=~"input|cache_creation|cache_read"}[24h]))
          * 100

      # LOC efficiency
      - record: claude_code:loc_per_dollar:daily
        expr: |
          sum(increase(claude_code_claude_code_lines_of_code_count_total[24h]))
          /
          sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

Then use simplified queries:
```promql
# Instead of complex query, just use:
claude_code:cost_usd:daily
claude_code:cost_usd:daily:by_team
```

---

## Visualization Tips

### Time Series Panel
- Use `rate()` for smooth trends
- Set legend to `{{label_name}}` for clarity
- Enable "Lines" draw style with opacity

### Stat Panel
- Use `lastNotNull` for counters
- Use `increase([24h])` for daily totals
- Add thresholds for color coding

### Bar Chart
- Use `sum by (label)` for grouping
- Sort by value descending
- Limit to top 10 with `topk(10, ...)`

### Pie Chart
- Calculate percentages with division
- Use `sum by (label)` for segments
- Limit to top categories

---

## Additional Resources

- **Prometheus Query Docs:** https://prometheus.io/docs/prometheus/latest/querying/basics/
- **PromQL Examples:** https://prometheus.io/docs/prometheus/latest/querying/examples/
- **Grafana Query Editor:** https://grafana.com/docs/grafana/latest/datasources/prometheus/
