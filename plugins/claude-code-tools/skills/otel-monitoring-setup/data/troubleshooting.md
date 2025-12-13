# Troubleshooting Guide

Common issues and solutions for Claude Code OpenTelemetry setup.

---

## Container Issues

### Docker Not Running

**Symptom:** `Cannot connect to the Docker daemon`

**Diagnosis:**
```bash
docker info
```

**Solutions:**
1. Start Docker Desktop application
2. Wait for Docker to fully initialize
3. Check system tray for Docker icon
4. Verify Docker daemon is running: `ps aux | grep docker`

---

### Containers Won't Start

**Symptom:** Containers exit immediately after `docker compose up`

**Diagnosis:**
```bash
# Check container logs
docker compose logs

# Check specific service
docker compose logs otel-collector
docker compose logs prometheus
```

**Common Causes:**

**1. OTEL Collector Configuration Error**
```bash
# Check for errors
docker compose logs otel-collector | grep -i error

# Common issues:
# - Deprecated logging exporter
# - Deprecated 'address' field in telemetry.metrics
```

**Solution A - Deprecated logging exporter:**
Update `otel-collector-config.yml`:
```yaml
exporters:
  debug:
    verbosity: normal
  # NOT:
  # logging:
  #   loglevel: info
```

**Solution B - Deprecated 'address' field (v0.123.0+):**

If logs show: `'address' has invalid keys` or similar error:

Update `otel-collector-config.yml`:
```yaml
service:
  telemetry:
    metrics:
      level: detailed
      # REMOVE this line (deprecated in v0.123.0+):
      # address: ":8888"
```

The `address` field in `service.telemetry.metrics` is deprecated in newer OTEL Collector versions. Simply remove it - the collector will use default internal metrics endpoint.

**2. Port Already in Use**
```bash
# Check which ports are in use
lsof -i :3000  # Grafana
lsof -i :4317  # OTEL gRPC
lsof -i :4318  # OTEL HTTP
lsof -i :8889  # OTEL Prometheus exporter
lsof -i :9090  # Prometheus
lsof -i :3100  # Loki
```

**Solution:**
- Stop conflicting service
- Or change port in docker-compose.yml

**3. Volume Permission Issues**
```bash
# Check volume permissions
docker volume ls
docker volume inspect claude-telemetry_prometheus-data
```

**Solution:**
```bash
# Remove and recreate volumes
docker compose down -v
docker compose up -d
```

---

### Containers Keep Restarting

**Symptom:** Container status shows "Restarting"

**Diagnosis:**
```bash
docker compose ps
docker compose logs --tail=50 <service-name>
```

**Solutions:**
1. Check memory limits: Increase memory_limiter in OTEL config
2. Check disk space: `df -h`
3. Check for configuration errors in logs
4. Restart Docker Desktop

---

## Claude Code Settings Issues

### 🚨 CRITICAL: Telemetry Not Sending (Most Common Issue)

**Symptom:** No metrics appearing in Prometheus after Claude Code restart

**ROOT CAUSE (90% of cases):** Missing required exporter environment variables

Even when `CLAUDE_CODE_ENABLE_TELEMETRY=1` is set, telemetry **will not send** without explicit exporter configuration. This is the #1 most common issue.

**Diagnosis Checklist:**

**1. Check REQUIRED exporters (MOST IMPORTANT):**
```bash
jq '.env.OTEL_METRICS_EXPORTER' ~/.claude/settings.json
# Must return: "otlp" (NOT null, NOT missing)

jq '.env.OTEL_LOGS_EXPORTER' ~/.claude/settings.json
# Should return: "otlp" (recommended for event tracking)
```

**If either returns `null` or is missing, this is your problem!**

**2. Verify telemetry is enabled:**
```bash
jq '.env.CLAUDE_CODE_ENABLE_TELEMETRY' ~/.claude/settings.json
# Should return: "1"
```

**3. Check OTEL endpoint:**
```bash
jq '.env.OTEL_EXPORTER_OTLP_ENDPOINT' ~/.claude/settings.json
# Should return: "http://localhost:4317" (for local setup)
```

**3. Verify JSON is valid:**
```bash
jq empty ~/.claude/settings.json
# No output = valid JSON
```

**4. Check if Claude Code was restarted:**
```bash
# Telemetry config only loads at startup!
# Must quit and restart Claude Code completely
```

**5. Test OTEL endpoint connectivity:**
```bash
nc -zv localhost 4317
# Should show: Connection to localhost port 4317 [tcp/*] succeeded!
```

**Solutions:**

**If exporters are missing (MOST COMMON):**

Add these REQUIRED settings to ~/.claude/settings.json:
```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc"
  }
}
```

Then **MUST restart Claude Code** (settings only load at startup).

**If endpoint unreachable:**
- Verify OTEL Collector container is running
- Check firewall settings
- Try HTTP endpoint instead: `http://localhost:4318`

**If still no data:**
- Check OTEL Collector logs for incoming connections
- Verify Claude Code is running (not just idle)
- Wait 60 seconds (default export interval)

---

### Settings.json Syntax Errors

**Symptom:** Claude Code won't start or shows errors

**Diagnosis:**
```bash
# Validate JSON
jq empty ~/.claude/settings.json

# Pretty-print to find issues
jq . ~/.claude/settings.json
```

**Common Issues:**
- Missing commas between properties
- Trailing commas before closing braces
- Unescaped quotes in strings
- Incorrect nesting

**Solution:**
```bash
# Restore backup
cp ~/.claude/settings.json.backup ~/.claude/settings.json

# Or fix JSON manually with editor
```

---

## Grafana Issues

### Can't Access Grafana

**Symptom:** `localhost:3000` doesn't load

**Diagnosis:**
```bash
# Check if Grafana is running
docker ps | grep grafana

# Check Grafana logs
docker compose logs grafana

# Check port availability
lsof -i :3000
```

**Solutions:**
1. Verify container is running: `docker compose up -d grafana`
2. Wait 30 seconds for Grafana to initialize
3. Try `http://127.0.0.1:3000` instead
4. Check Docker network: `docker network inspect claude-telemetry`

---

### Dashboard Shows "Datasource Not Found"

**Symptom:** Dashboard panels show "datasource prometheus not found"

**Cause:** Dashboard has hardcoded datasource UID that doesn't match your Grafana instance

**Diagnosis:**
1. Go to: http://localhost:3000/connections/datasources
2. Click on Prometheus datasource
3. Note the UID from URL (e.g., `PBFA97CFB590B2093`)

**Solution:**
```bash
# Get your datasource UID
DATASOURCE_UID=$(curl -s -u admin:admin http://localhost:3000/api/datasources | jq -r '.[] | select(.type=="prometheus") | .uid')

echo "Your Prometheus datasource UID: $DATASOURCE_UID"

# Update dashboard JSON
cd ~/.claude/telemetry/dashboards
cat claude-code-overview.json | sed "s/PBFA97CFB590B2093/$DATASOURCE_UID/g" > claude-code-overview-fixed.json

# Re-import the fixed dashboard
```

---

### Dashboard Shows "No Data"

**Symptom:** Dashboard loads but all panels show "No data"

**Diagnosis Steps:**

**1. Check Prometheus has data:**
```bash
# Query Prometheus directly
curl -s 'http://localhost:9090/api/v1/label/__name__/values' | jq . | grep claude_code

# Should see metrics like:
# "claude_code_claude_code_session_count_total"
# "claude_code_claude_code_cost_usage_USD_total"
```

**2. Check datasource connection:**
- Go to: http://localhost:3000/connections/datasources
- Click Prometheus
- Click "Save & Test"
- Should show: "Successfully queried the Prometheus API"

**3. Verify metric names in queries:**
```bash
# Check if metrics use double prefix
curl -s 'http://localhost:9090/api/v1/query?query=claude_code_claude_code_session_count_total' | jq .
```

**Solutions:**

**If metrics don't exist:**
- Claude Code hasn't sent data yet (wait 60 seconds)
- OTEL Collector isn't receiving data (check container logs)
- Settings.json wasn't configured correctly

**If metrics exist but dashboard shows no data:**
- Dashboard queries use wrong metric names
- Update queries to use double prefix: `claude_code_claude_code_*`
- Check time range (top-right corner of Grafana)

**If single prefix metrics exist (`claude_code_*`):**
Your setup uses old naming. Update dashboard:
```bash
# Replace double prefix with single
sed 's/claude_code_claude_code_/claude_code_/g' dashboard.json > dashboard-fixed.json
```

---

## Prometheus Issues

### Prometheus Shows No Targets

**Symptom:** Prometheus UI (localhost:9090) → Status → Targets shows no targets or DOWN status

**Diagnosis:**
```bash
# Check Prometheus config
cat ~/.claude/telemetry/prometheus.yml

# Check if OTEL Collector is reachable from Prometheus
docker exec -it claude-prometheus ping otel-collector
```

**Solutions:**
1. Verify `prometheus.yml` has correct scrape_configs
2. Ensure OTEL Collector is running
3. Check Docker network connectivity
4. Restart Prometheus: `docker compose restart prometheus`

---

### Prometheus Can't Scrape OTEL Collector

**Symptom:** Target shows as DOWN with error "context deadline exceeded"

**Diagnosis:**
```bash
# Check if OTEL Collector is exposing metrics
curl http://localhost:8889/metrics

# Check OTEL Collector logs
docker compose logs otel-collector
```

**Solutions:**
1. Verify OTEL Collector prometheus exporter is configured
2. Check port 8889 is exposed in docker-compose.yml
3. Restart OTEL Collector: `docker compose restart otel-collector`

---

## Metric Issues

### Metrics Have Double Prefix

**Symptom:** Metrics are named `claude_code_claude_code_*` instead of `claude_code_*`

**Explanation:** This is expected behavior with the current OTEL Collector configuration:
- First `claude_code` = Prometheus exporter namespace
- Second `claude_code` = Original metric name

**Solutions:**

**Option 1: Accept it (Recommended)**
- Update dashboard queries to use double prefix
- This is the standard configuration

**Option 2: Remove namespace prefix**
Update `otel-collector-config.yml`:
```yaml
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: ""  # Remove namespace
```

Then restart: `docker compose restart otel-collector`

---

### Old Metrics Still Showing

**Symptom:** After changing configuration, old metrics still appear

**Cause:** Prometheus retains metrics until retention period expires

**Solutions:**

**Quick fix: Delete Prometheus data:**
```bash
docker compose down
docker volume rm claude-telemetry_prometheus-data
docker compose up -d
```

**Proper fix: Wait for retention:**
- Default retention is 15 days
- Old metrics will automatically disappear
- New metrics will coexist temporarily

---

## Network Issues

### Can't Reach OTEL Endpoint from Claude Code

**Symptom:** Claude Code can't connect to `localhost:4317`

**Diagnosis:**
```bash
# Test gRPC endpoint
nc -zv localhost 4317

# Test HTTP endpoint
curl -v http://localhost:4318/v1/metrics -d '{}'
```

**Solutions:**

**If connection refused:**
1. Check OTEL Collector is running
2. Verify ports are exposed in docker-compose.yml
3. Check firewall/antivirus blocking localhost connections

**If timeout:**
1. Increase export timeout in settings.json
2. Try HTTP protocol instead of gRPC

**macOS-specific:**
- Use `http://host.docker.internal:4317` instead of `localhost:4317`
- Or use bridge network mode

---

### Enterprise Endpoint Unreachable

**Symptom:** Can't connect to company OTEL endpoint

**Diagnosis:**
```bash
# Test connectivity
ping otel.company.com

# Test port
nc -zv otel.company.com 4317

# Test with VPN
# (Ensure corporate VPN is connected)
```

**Solutions:**
1. Connect to corporate VPN
2. Check firewall allows outbound connections
3. Verify endpoint URL is correct
4. Try HTTP endpoint (port 4318) instead of gRPC
5. Contact platform team to verify endpoint is accessible

---

## Performance Issues

### High Memory Usage

**Symptom:** OTEL Collector or Prometheus using excessive memory

**Diagnosis:**
```bash
# Check container resource usage
docker stats

# Check Prometheus TSDB size
du -sh ~/.claude/telemetry/prometheus-data
```

**Solutions:**

**OTEL Collector:**
Reduce memory_limiter in `otel-collector-config.yml`:
```yaml
processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 256  # Reduce from 512
```

**Prometheus:**
Reduce retention:
```yaml
command:
  - '--storage.tsdb.retention.time=7d'  # Reduce from 15d
  - '--storage.tsdb.retention.size=1GB'
```

---

### Slow Grafana Dashboards

**Symptom:** Dashboards take long time to load or timeout

**Diagnosis:**
```bash
# Check query performance in Prometheus
# Go to: http://localhost:9090/graph
# Run expensive queries like: sum by (account_uuid, model, type) (...)
```

**Solutions:**
1. Reduce dashboard time range (use 6h instead of 7d)
2. Increase dashboard refresh interval (1m → 5m)
3. Use recording rules for complex queries
4. Reduce number of panels
5. Use simpler aggregations

---

## Data Quality Issues

### Unexpected Cost Values

**Symptom:** Cost metrics seem incorrect

**Diagnosis:**
```bash
# Check raw cost values
curl -s 'http://localhost:9090/api/v1/query?query=claude_code_claude_code_cost_usage_USD_total' | jq .

# Check token usage
curl -s 'http://localhost:9090/api/v1/query?query=claude_code_claude_code_token_usage_tokens_total' | jq .
```

**Causes:**
- Cost is cumulative counter (not reset between sessions)
- Dashboard may be using wrong time range
- Model pricing may have changed

**Solutions:**
- Use `increase([24h])` not raw counter values
- Verify pricing in metrics reference
- Check Claude Code version (pricing may vary)

---

### Missing Sessions

**Symptom:** Some Claude Code sessions not recorded

**Causes:**
1. Claude Code wasn't restarted after settings update
2. OTEL Collector was down during session
3. Export interval hadn't elapsed yet (60 seconds default)
4. Network issue prevented export

**Solutions:**
- Always restart Claude Code after settings changes
- Monitor OTEL Collector uptime
- Check OTEL Collector logs for export errors
- Reduce export interval if real-time data needed

---

## Getting Help

### Collect Debug Information

When asking for help, provide:

```bash
# 1. Container status
docker compose ps

# 2. Container logs (last 50 lines)
docker compose logs --tail=50

# 3. Configuration files
cat ~/.claude/telemetry/otel-collector-config.yml
cat ~/.claude/telemetry/prometheus.yml

# 4. Claude Code settings (redact sensitive info!)
jq '.env | with_entries(select(.key | startswith("OTEL_")))' ~/.claude/settings.json

# 5. Prometheus metrics list
curl -s 'http://localhost:9090/api/v1/label/__name__/values' | jq . | grep claude_code

# 6. System info
docker --version
docker compose version
uname -a
```

### Enable Debug Logging

**OTEL Collector:**
```yaml
exporters:
  debug:
    verbosity: detailed  # Change from 'normal'

service:
  telemetry:
    logs:
      level: debug  # Change from 'info'
```

**Claude Code:**
Add to settings.json:
```json
"env": {
  "OTEL_LOG_LEVEL": "debug"
}
```

Then check logs:
```bash
docker compose logs -f otel-collector
```

---

## Additional Resources

- **OTEL Collector Docs:** https://opentelemetry.io/docs/collector/
- **Prometheus Troubleshooting:** https://prometheus.io/docs/prometheus/latest/troubleshooting/
- **Grafana Troubleshooting:** https://grafana.com/docs/grafana/latest/troubleshooting/
- **Docker Compose Docs:** https://docs.docker.com/compose/
