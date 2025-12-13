# Claude Code Metrics Reference

Complete reference for all Claude Code OpenTelemetry metrics.

**Important:** All metrics use a double prefix: `claude_code_claude_code_*`

---

## Metric Categories

1. **Usage Metrics** - Session counts, active time
2. **Token Metrics** - Input, output, cached tokens
3. **Cost Metrics** - API costs by model
4. **Productivity Metrics** - LOC, commits, PRs
5. **Error Metrics** - Failures, retries

---

## Usage Metrics

### claude_code_claude_code_session_count_total

**Type:** Counter
**Description:** Total number of Claude Code sessions started
**Labels:**
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version (e.g., "1.2.3")

**Example Query:**
```promql
# Total sessions across all users
sum(claude_code_claude_code_session_count_total)

# Sessions by version
sum by (version) (claude_code_claude_code_session_count_total)

# New sessions in last 24h
increase(claude_code_claude_code_session_count_total[24h])
```

---

### claude_code_claude_code_active_time_seconds_total

**Type:** Counter
**Description:** Total active time spent in Claude Code sessions (in seconds)
**Labels:**
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version

**Example Query:**
```promql
# Total active hours
sum(claude_code_claude_code_active_time_seconds_total) / 3600

# Active hours per day
increase(claude_code_claude_code_active_time_seconds_total[24h]) / 3600

# Average session duration
increase(claude_code_claude_code_active_time_seconds_total[24h])
/
increase(claude_code_claude_code_session_count_total[24h])
```

**Note:** "Active time" means time when Claude Code is actively processing or responding to user input.

---

## Token Metrics

### claude_code_claude_code_token_usage_tokens_total

**Type:** Counter
**Description:** Total tokens consumed by Claude Code API calls
**Labels:**
- `type` - Token type: `input`, `output`, `cache_creation`, `cache_read`
- `model` - Model name (e.g., "claude-sonnet-4-5-20250929", "claude-opus-4-20250514")
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version

**Token Types Explained:**
- **input:** User messages and tool results sent to Claude
- **output:** Claude's responses (text and tool calls)
- **cache_creation:** Tokens written to prompt cache (billed at input rate)
- **cache_read:** Tokens read from prompt cache (billed at 10% of input rate)

**Example Query:**
```promql
# Total tokens by type (24h)
sum by (type) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))

# Tokens by model (24h)
sum by (model) (increase(claude_code_claude_code_token_usage_tokens_total[24h]))

# Cache hit rate
sum(increase(claude_code_claude_code_token_usage_tokens_total{type="cache_read"}[24h]))
/
sum(increase(claude_code_claude_code_token_usage_tokens_total{type=~"input|cache_creation|cache_read"}[24h]))

# Token usage rate (per minute)
rate(claude_code_claude_code_token_usage_tokens_total[5m]) * 60
```

---

## Cost Metrics

### claude_code_claude_code_cost_usage_USD_total

**Type:** Counter
**Description:** Total API costs in USD
**Labels:**
- `model` - Model name
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version

**Pricing Reference (as of Jan 2025):**
- **Claude Sonnet 4.5:** $3/MTok input, $15/MTok output
- **Claude Opus 4:** $15/MTok input, $75/MTok output
- **Cache read:** 10% of input price
- **Cache write:** Same as input price

**Example Query:**
```promql
# Total cost (24h)
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))

# Cost by model (24h)
sum by (model) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))

# Cost per hour
rate(claude_code_claude_code_cost_usage_USD_total[5m]) * 3600

# Average cost per session
increase(claude_code_claude_code_cost_usage_USD_total[24h])
/
increase(claude_code_claude_code_session_count_total[24h])

# Cumulative cost over time
sum(claude_code_claude_code_cost_usage_USD_total)
```

---

## Productivity Metrics

### claude_code_claude_code_lines_of_code_count_total

**Type:** Counter
**Description:** Total lines of code modified (added + changed + deleted)
**Labels:**
- `type` - Modification type: `added`, `changed`, `deleted`
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version

**Example Query:**
```promql
# Total LOC modified
sum(claude_code_claude_code_lines_of_code_count_total)

# LOC by type (24h)
sum by (type) (increase(claude_code_claude_code_lines_of_code_count_total[24h]))

# LOC per hour
rate(claude_code_claude_code_lines_of_code_count_total[5m]) * 3600

# Lines per dollar
sum(increase(claude_code_claude_code_lines_of_code_count_total[24h]))
/
sum(increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

---

### claude_code_claude_code_commit_count_total

**Type:** Counter
**Description:** Total git commits created by Claude Code
**Labels:**
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version

**Example Query:**
```promql
# Total commits
sum(claude_code_claude_code_commit_count_total)

# Commits per day
increase(claude_code_claude_code_commit_count_total[24h])

# Commits per session
increase(claude_code_claude_code_commit_count_total[24h])
/
increase(claude_code_claude_code_session_count_total[24h])
```

---

### claude_code_claude_code_pr_count_total

**Type:** Counter
**Description:** Total pull requests created by Claude Code
**Labels:**
- `account_uuid` - Anonymous user identifier
- `version` - Claude Code version

**Example Query:**
```promql
# Total PRs
sum(claude_code_claude_code_pr_count_total)

# PRs per week
increase(claude_code_claude_code_pr_count_total[7d])
```

---

## Cardinality and Resource Attributes

### Resource Attributes

All metrics include these resource attributes (configured in settings.json):

```json
"OTEL_RESOURCE_ATTRIBUTES": "environment=local,deployment=poc,team=platform"
```

**Common Attributes:**
- `service.name` = "claude-code" (set by OTEL Collector)
- `environment` - Deployment environment (local, dev, staging, prod)
- `deployment` - Deployment type (poc, enterprise)
- `team` - Team identifier
- `department` - Department identifier
- `project` - Project identifier

**Querying with Resource Attributes:**
```promql
# Filter by environment
sum(claude_code_claude_code_cost_usage_USD_total{environment="production"})

# Aggregate by team
sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[24h]))
```

---

## Metric Naming Convention

**Format:** `claude_code_claude_code_<metric_name>_<unit>_<type>`

**Why double prefix?**
- First `claude_code` comes from Prometheus exporter namespace in OTEL Collector config
- Second `claude_code` comes from the original metric name in Claude Code
- This is expected behavior with the current configuration

**Components:**
- `<metric_name>`: Descriptive name (e.g., `token_usage`, `cost_usage`)
- `<unit>`: Unit of measurement (e.g., `tokens`, `USD`, `seconds`, `count`)
- `<type>`: Metric type (always `total` for counters)

---

## Querying Best Practices

### Use increase() for Counters

Counters are cumulative, so use `increase()` for time windows:

```promql
# ✅ Correct - Shows cost in last 24h
increase(claude_code_claude_code_cost_usage_USD_total[24h])

# ❌ Wrong - Shows cumulative cost since start
claude_code_claude_code_cost_usage_USD_total
```

### Use rate() for Rates

Calculate per-second rate, then multiply for desired unit:

```promql
# Cost per hour
rate(claude_code_claude_code_cost_usage_USD_total[5m]) * 3600

# Tokens per minute
rate(claude_code_claude_code_token_usage_tokens_total[5m]) * 60
```

### Aggregate with sum()

Combine metrics across labels:

```promql
# Total tokens (all types)
sum(claude_code_claude_code_token_usage_tokens_total)

# Total tokens by type
sum by (type) (claude_code_claude_code_token_usage_tokens_total)

# Total cost across all models
sum(claude_code_claude_code_cost_usage_USD_total)
```

---

## Example Dashboards

### Executive Summary (single values)

```promql
# Total cost this month
sum(increase(claude_code_claude_code_cost_usage_USD_total[30d]))

# Total LOC this month
sum(increase(claude_code_claude_code_lines_of_code_count_total[30d]))

# Active users (unique account_uuids)
count(count by (account_uuid) (claude_code_claude_code_session_count_total))

# Average session cost
sum(increase(claude_code_claude_code_cost_usage_USD_total[30d]))
/
sum(increase(claude_code_claude_code_session_count_total[30d]))
```

### Cost Tracking

```promql
# Daily cost trend
sum(increase(claude_code_claude_code_cost_usage_USD_total[1d]))

# Cost by model (pie chart)
sum by (model) (increase(claude_code_claude_code_cost_usage_USD_total[7d]))

# Cost by team (bar chart)
sum by (team) (increase(claude_code_claude_code_cost_usage_USD_total[7d]))
```

### Productivity Tracking

```promql
# LOC per day
sum(increase(claude_code_claude_code_lines_of_code_count_total[1d]))

# Commits per week
sum(increase(claude_code_claude_code_commit_count_total[7d]))

# Efficiency: LOC per dollar
sum(increase(claude_code_claude_code_lines_of_code_count_total[30d]))
/
sum(increase(claude_code_claude_code_cost_usage_USD_total[30d]))
```

---

## Retention and Storage

**Default Prometheus Retention:** 15 days

**Adjust retention:**
```yaml
# In prometheus.yml or docker-compose.yml
command:
  - '--storage.tsdb.retention.time=90d'
  - '--storage.tsdb.retention.size=50GB'
```

**Disk usage estimation:**
- ~1-2 MB per day per active user
- ~30-60 MB per month per active user
- ~360-720 MB per year per active user

**For long-term storage:** Consider using Prometheus remote write to send data to a time-series database like VictoriaMetrics, Cortex, or Thanos.

---

## Additional Resources

- **Official OTEL Docs:** https://opentelemetry.io/docs/
- **Prometheus Query Docs:** https://prometheus.io/docs/prometheus/latest/querying/basics/
- **PromQL Examples:** See `prometheus-queries.md`
