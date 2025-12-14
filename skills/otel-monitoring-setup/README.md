# Claude Code OpenTelemetry Setup Skill

Automated workflow for setting up OpenTelemetry telemetry collection for Claude Code usage monitoring, cost tracking, and productivity analytics.

**Version:** 1.0.0
**Author:** Prometheus Team

---

## Features

- **Mode 1: Local PoC Setup** - Full Docker stack with Grafana dashboards
- **Mode 2: Enterprise Setup** - Connect to centralized infrastructure
- Automated configuration file generation
- Dashboard import with UID detection
- Verification and testing procedures
- Comprehensive troubleshooting guides

---

## Quick Start

### Prerequisites

**For Mode 1 (Local PoC):**
- Docker Desktop installed and running
- Claude Code installed
- Write access to `~/.claude/settings.json`

**For Mode 2 (Enterprise):**
- OTEL Collector endpoint URL
- Authentication credentials
- Write access to `~/.claude/settings.json`

### Installation

This skill is designed to be invoked by Claude Code. No manual installation required.

### Usage

**Mode 1 - Local PoC Setup:**
```
"Set up Claude Code telemetry locally"
"I want to try OpenTelemetry with Claude Code"
"Create a local telemetry stack for me"
```

**Mode 2 - Enterprise Setup:**
```
"Connect Claude Code to our company OTEL endpoint at otel.company.com:4317"
"Set up telemetry for team rollout"
"Configure enterprise telemetry"
```

---

## What Gets Collected?

### Metrics
- **Session counts and active time** - How much you use Claude Code
- **Token usage** - Input, output, cached tokens by model
- **API costs** - Spend tracking by model and time
- **Lines of code** - Code modifications (added, changed, deleted)
- **Commits and PRs** - Git activity tracking

### Events/Logs
- User prompts (if enabled)
- Tool executions
- API requests
- Session lifecycle

**Privacy:** Metrics are anonymized. Source code content is never collected.

---

## Directory Structure

```
claude-code-otel-setup/
├── SKILL.md                  # Main skill definition
├── README.md                 # This file
├── modes/
│   ├── mode1-poc-setup.md    # Detailed local setup workflow
│   └── mode2-enterprise.md   # Detailed enterprise setup workflow
├── templates/
│   ├── docker-compose.yml    # Docker Compose configuration
│   ├── otel-collector-config.yml  # OTEL Collector configuration
│   ├── prometheus.yml        # Prometheus scrape configuration
│   ├── grafana-datasources.yml    # Grafana datasource provisioning
│   ├── settings.json.local   # Local telemetry settings template
│   ├── settings.json.enterprise  # Enterprise settings template
│   ├── start-telemetry.sh    # Start script
│   └── stop-telemetry.sh     # Stop script
├── dashboards/
│   ├── README.md             # Dashboard import guide
│   ├── claude-code-overview.json  # Comprehensive dashboard
│   └── claude-code-simple.json    # Simplified dashboard
└── data/
    ├── metrics-reference.md  # Complete metrics documentation
    ├── prometheus-queries.md # Useful PromQL queries
    └── troubleshooting.md    # Common issues and solutions
```

---

## Mode 1: Local PoC Setup

**What it does:**
- Creates `~/.claude/telemetry/` directory
- Generates Docker Compose configuration
- Starts 4 containers: OTEL Collector, Prometheus, Loki, Grafana
- Updates Claude Code settings.json
- Imports Grafana dashboards
- Verifies data flow

**Time:** 5-7 minutes

**Output:**
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Working dashboards with real data

**Detailed workflow:** See `modes/mode1-poc-setup.md`

---

## Mode 2: Enterprise Setup

**What it does:**
- Collects enterprise OTEL endpoint details
- Updates Claude Code settings.json with endpoint and auth
- Adds team/environment resource attributes
- Tests connectivity (optional)
- Provides team rollout documentation

**Time:** 2-3 minutes

**Output:**
- Claude Code configured to send to central endpoint
- Connectivity verified
- Team rollout guide generated

**Detailed workflow:** See `modes/mode2-enterprise.md`

---

## Example Dashboards

### Overview Dashboard

Includes:
- Total Lines of Code (all-time)
- Total Cost (24h)
- Total Tokens (24h)
- Active Time (24h)
- Cost Over Time (timeseries)
- Token Usage by Type (stacked)
- Lines of Code Modified (bar chart)
- Commits Created (24h)

### Custom Queries

See `data/prometheus-queries.md` for 50+ ready-to-use PromQL queries:
- Cost analysis
- Token usage
- Productivity metrics
- Team aggregation
- Model comparison
- Alerting rules

---

## Common Use Cases

### Individual Developer

**Goal:** Track personal Claude Code usage and costs

**Setup:**
```
Mode 1 (Local PoC)
```

**Access:**
- Personal Grafana dashboard at localhost:3000
- All data stays local

---

### Team Pilot (5-10 Users)

**Goal:** Aggregate metrics across pilot users

**Setup:**
```
Mode 2 (Enterprise)
```

**Architecture:**
- Centralized OTEL Collector
- Team-level Prometheus/Grafana
- Aggregated dashboards

---

### Enterprise Rollout (100+ Users)

**Goal:** Organization-wide cost tracking and productivity analytics

**Setup:**
```
Mode 2 (Enterprise) + Managed Infrastructure
```

**Features:**
- Department/team/project attribution
- Chargeback reporting
- Executive dashboards
- Trend analysis

---

## Troubleshooting

### Quick Checks

**Containers not starting:**
```bash
docker compose logs
```

**No metrics in Prometheus:**
1. Restart Claude Code (telemetry loads at startup)
2. Wait 60 seconds (export interval)
3. Check OTEL Collector logs: `docker compose logs otel-collector`

**Dashboard shows "No data":**
1. Verify metric names use double prefix: `claude_code_claude_code_*`
2. Check time range (top-right corner)
3. Verify datasource UID matches

**Full troubleshooting guide:** See `data/troubleshooting.md`

---

## Known Issues

### Issue 1: 🚨 CRITICAL - Missing OTEL Exporters

**Description:** Claude Code not sending telemetry even with `CLAUDE_CODE_ENABLE_TELEMETRY=1`

**Cause:** Missing required `OTEL_METRICS_EXPORTER` and `OTEL_LOGS_EXPORTER` settings

**Solution:** The skill templates include these by default. **Always verify** they're present in settings.json. See Configuration Reference for details.

---

### Issue 2: OTEL Collector Deprecated 'address' Field

**Description:** Collector crashes with "'address' has invalid keys" error

**Cause:** The `address` field in `service.telemetry.metrics` is deprecated in collector v0.123.0+

**Solution:** Skill templates have this removed. If using custom config, remove the deprecated field.

---

### Issue 3: Metric Double Prefix

**Description:** Metrics are named `claude_code_claude_code_*` instead of `claude_code_*`

**Cause:** OTEL Collector Prometheus exporter adds namespace prefix

**Solution:** This is expected. Dashboards use correct naming.

---

### Issue 4: Dashboard Datasource UID Mismatch

**Description:** Dashboard shows "datasource prometheus not found"

**Cause:** Dashboard has hardcoded UID that doesn't match your Grafana

**Solution:** Skill automatically detects and fixes UID during import

---

### Issue 5: OTEL Collector Deprecated Exporter

**Description:** Container fails with "logging exporter has been deprecated"

**Cause:** Old OTEL configuration

**Solution:** Skill uses `debug` exporter (not deprecated `logging`)

---

## Configuration Reference

### Settings.json (Local)

**🚨 CRITICAL REQUIREMENTS:**

The following settings are **REQUIRED** (not optional) for telemetry to work:
- `CLAUDE_CODE_ENABLE_TELEMETRY: "1"` - Enables telemetry system
- `OTEL_METRICS_EXPORTER: "otlp"` - **REQUIRED** to send metrics (most common missing setting!)
- `OTEL_LOGS_EXPORTER: "otlp"` - **REQUIRED** to send events/logs

Without `OTEL_METRICS_EXPORTER` and `OTEL_LOGS_EXPORTER`, telemetry will not send even if `CLAUDE_CODE_ENABLE_TELEMETRY=1` is set.

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",           // REQUIRED!
    "OTEL_LOGS_EXPORTER": "otlp",              // REQUIRED!
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "environment=local,deployment=poc"
  }
}
```

### Settings.json (Enterprise)

**Same CRITICAL requirements apply:**
- `OTEL_METRICS_EXPORTER: "otlp"` - **REQUIRED!**
- `OTEL_LOGS_EXPORTER: "otlp"` - **REQUIRED!**

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",           // REQUIRED!
    "OTEL_LOGS_EXPORTER": "otlp",              // REQUIRED!
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer YOUR_API_KEY",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production"
  }
}
```

---

## Management

### Start Telemetry Stack (Mode 1)

```bash
~/.claude/telemetry/start-telemetry.sh
```

### Stop Telemetry Stack (Mode 1)

```bash
~/.claude/telemetry/stop-telemetry.sh
```

### Check Status

```bash
docker compose ps
```

### View Logs

```bash
docker compose logs -f
```

### Restart Services

```bash
docker compose restart
```

---

## Data Retention

**Default:** 15 days in Prometheus

**Adjust retention:**
Edit `docker-compose.yml` or `prometheus.yml`:
```yaml
command:
  - '--storage.tsdb.retention.time=90d'
  - '--storage.tsdb.retention.size=50GB'
```

**Disk usage:** ~1-2 MB per day per active user

---

## Security Considerations

### Local Setup (Mode 1)

- Grafana accessible only on localhost
- Default credentials: admin/admin (change after first login)
- No external network exposure
- Data stored in Docker volumes

### Enterprise Setup (Mode 2)

- Use HTTPS endpoints
- Store API keys securely (environment variables, secrets manager)
- Enable mTLS for production
- Tag metrics with team/project for proper attribution

---

## Performance Tuning

### Reduce OTEL Collector Memory

Edit `otel-collector-config.yml`:
```yaml
processors:
  memory_limiter:
    limit_mib: 256  # Reduce from default
```

### Reduce Prometheus Retention

Edit `docker-compose.yml`:
```yaml
command:
  - '--storage.tsdb.retention.time=7d'  # Reduce from 15d
```

### Optimize Dashboard Queries

- Use recording rules for expensive queries
- Reduce dashboard time ranges
- Increase refresh intervals

See `data/prometheus-queries.md` for recording rule examples

---

## Integration Examples

### Cost Alerts (PagerDuty/Slack)

```yaml
# alertmanager.yml
groups:
  - name: claude_code_cost
    rules:
      - alert: HighDailyCost
        expr: sum(increase(claude_code_claude_code_cost_usage_USD_total[24h])) > 100
        annotations:
          summary: "Claude Code daily cost exceeded $100"
```

### Weekly Cost Reports (Email)

Use Grafana Reporting:
1. Create dashboard with cost panels
2. Set up email delivery
3. Schedule weekly reports

### Chargeback Integration

Export metrics to data warehouse:
```yaml
# Use Prometheus remote write
remote_write:
  - url: "https://datawarehouse.company.com/prometheus"
```

---

## Contributing

This skill is maintained by the Prometheus Team.

**Feedback:** Open an issue or contact the team

**Improvements:** Submit pull requests with enhancements

---

## Changelog

### Version 1.1.0 (2025-11-01)

**Critical Updates from Production Testing:**
- 🚨 **CRITICAL FIX**: Documented missing OTEL_METRICS_EXPORTER/OTEL_LOGS_EXPORTER as #1 cause of "telemetry not working"
- ✅ Added deprecated `address` field fix for OTEL Collector v0.123.0+
- ✅ Enhanced troubleshooting with prominent exporter configuration section
- ✅ Updated all documentation with CRITICAL warnings for required settings
- ✅ Added comprehensive Known Issues section covering production scenarios
- ✅ Verified templates have correct exporter configuration

**What Changed:**
- Troubleshooting guide now prioritizes missing exporters as root cause
- Known Issues expanded from 3 to 6 issues with production learnings
- Configuration Reference includes prominent CRITICAL requirements callout
- SKILL.md Important Reminders section updated with exporter warnings

### Version 1.0.0 (2025-10-31)

**Initial Release:**
- Mode 1: Local PoC setup with full Docker stack
- Mode 2: Enterprise setup with centralized endpoint
- Comprehensive documentation and troubleshooting
- Dashboard templates with correct metric naming
- Automated UID detection and replacement

**Known Issues Fixed:**
- ✅ OTEL Collector deprecated logging exporter
- ✅ Dashboard datasource UID mismatch
- ✅ Metric double prefix handling
- ✅ Loki exporter configuration

---

## Additional Resources

- **Claude Code Monitoring Docs:** https://docs.claude.com/claude-code/monitoring
- **OpenTelemetry Docs:** https://opentelemetry.io/docs/
- **Prometheus Docs:** https://prometheus.io/docs/
- **Grafana Docs:** https://grafana.com/docs/

---

## License

Internal use within Elsevier organization.

---

## Support

**Issues?** Check `data/troubleshooting.md` first

**Questions?** Contact Prometheus Team or #claude-code-telemetry channel

**Emergency?** Rollback with: `cp ~/.claude/settings.json.backup ~/.claude/settings.json`

---

**Ready to monitor your Claude Code usage!** 🚀
