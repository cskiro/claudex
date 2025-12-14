# Known Issues & Fixes

Common problems and solutions for Claude Code OpenTelemetry setup.

## Issue 1: Missing OTEL Exporters (Most Common)

**Problem**: Claude Code not sending telemetry even with `CLAUDE_CODE_ENABLE_TELEMETRY=1`

**Cause**: Missing required exporter settings

**Symptoms**:
- No metrics in Prometheus after restart
- OTEL Collector logs show no incoming connections
- Dashboard shows "No data"

**Fix**: Add to settings.json:
```json
{
  "env": {
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp"
  }
}
```

**Important**: Restart Claude Code after adding!

## Issue 2: OTEL Collector Deprecated 'address' Field

**Problem**: OTEL Collector crashes with "'address' has invalid keys" error

**Cause**: The `address` field in `service.telemetry.metrics` is deprecated in v0.123.0+

**Fix**: Remove the address field:
```yaml
service:
  telemetry:
    metrics:
      level: detailed
      # REMOVE: address: ":8888"
```

## Issue 3: OTEL Collector Deprecated Exporter

**Problem**: OTEL Collector fails with "logging exporter has been deprecated"

**Fix**: Use `debug` exporter instead:
```yaml
exporters:
  debug:
    verbosity: normal

service:
  pipelines:
    metrics:
      exporters: [prometheus, debug]
```

## Issue 4: Dashboard Datasource Not Found

**Problem**: Grafana dashboard shows "datasource prometheus not found"

**Cause**: Dashboard has hardcoded UID that doesn't match your setup

**Fix**:

1. Detect your actual UID:
```bash
curl -s http://admin:admin@localhost:3000/api/datasources | jq '.[0].uid'
```

2. Replace all occurrences in dashboard JSON:
```bash
sed -i '' 's/"uid": "prometheus"/"uid": "YOUR_ACTUAL_UID"/g' dashboard.json
```

3. Re-import the dashboard

## Issue 5: Metric Names Double Prefix

**Problem**: Dashboard queries fail because metrics have format `claude_code_claude_code_*`

**Cause**: Claude Code adds prefix, OTEL Collector adds another

**Affected Metrics**:
- `claude_code_claude_code_lines_of_code_count_total`
- `claude_code_claude_code_cost_usage_USD_total`
- `claude_code_claude_code_token_usage_tokens_total`
- `claude_code_claude_code_active_time_seconds_total`
- `claude_code_claude_code_commit_count_total`

**Fix**: Update dashboard queries to use actual metric names

**Verify actual names**:
```bash
curl -s http://localhost:9090/api/v1/label/__name__/values | jq '.data[]' | grep claude
```

## Issue 6: No Data in Prometheus

**Diagnostic Steps**:

1. **Check containers running**:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

2. **Check OTEL Collector logs**:
```bash
docker logs otel-collector 2>&1 | tail -50
```

3. **Query Prometheus directly**:
```bash
curl -s 'http://localhost:9090/api/v1/query?query=up' | jq '.data.result'
```

4. **Verify Claude Code settings**:
```bash
cat ~/.claude/settings.json | jq '.env'
```

**Common Causes**:
- Claude Code not restarted after settings change
- Missing OTEL_METRICS_EXPORTER setting
- Wrong endpoint (should be localhost:4317 for local)
- Firewall blocking ports

## Issue 7: Port Conflicts

**Problem**: Container fails to start due to port already in use

**Check ports**:
```bash
for port in 3000 4317 4318 8889 9090; do
  lsof -i :$port && echo "Port $port in use"
done
```

**Solutions**:
- Stop conflicting service
- Change port in docker-compose.yml
- Use different port mapping

## Issue 8: Docker Not Running

**Problem**: Commands fail with "Cannot connect to Docker daemon"

**Fix**:
1. Start Docker Desktop application
2. Wait for it to fully initialize
3. Verify: `docker info`

## Issue 9: Insufficient Disk Space

**Problem**: Containers fail to start or crash

**Required**: Minimum 2GB free

**Check**:
```bash
df -h ~/.claude
```

**Solutions**:
- Clean Docker: `docker system prune`
- Remove old images: `docker image prune -a`
- Clear telemetry volumes: `~/.claude/telemetry/cleanup-telemetry.sh`

## Issue 10: Grafana Dashboard Empty After Import

**Diagnostic Steps**:

1. Check time range (upper right) - data might be outside range
2. Verify datasource is connected (green checkmark in settings)
3. Run test query in Explore view
4. Check metric names match actual names in Prometheus

## Debugging Commands

```bash
# Full container status
docker compose -f ~/.claude/telemetry/docker-compose.yml ps

# OTEL Collector config validation
docker exec otel-collector cat /etc/otel/config.yaml

# Prometheus targets
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets'

# Grafana datasources
curl -s http://admin:admin@localhost:3000/api/datasources | jq '.'

# All available metrics
curl -s http://localhost:9090/api/v1/label/__name__/values | jq '.data | length'
```

## Getting Help

If issues persist:

1. Collect diagnostics:
```bash
docker compose -f ~/.claude/telemetry/docker-compose.yml logs > telemetry-logs.txt
cat ~/.claude/settings.json | jq '.env' > settings-env.txt
```

2. Check versions:
```bash
docker --version
docker compose version
```

3. Provide: logs, settings, versions, and exact error message
