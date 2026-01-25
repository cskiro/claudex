# Mode 1: Local PoC Setup - Detailed Workflow

Complete step-by-step process for setting up a local OpenTelemetry stack for Claude Code telemetry.

---

## Overview

**Goal:** Create a complete local telemetry monitoring stack
**Time:** 5-7 minutes
**Prerequisites:** Docker Desktop, Claude Code, 2GB+ free disk space
**Output:** Running Grafana dashboard with Claude Code metrics

---

## Phase 0: Prerequisites Verification

### Step 0.1: Check Docker Installation

```bash
# Check if Docker is installed
docker --version

# Expected: Docker version 20.10.0 or higher
```

**If not installed:**
```
Docker is not installed. Please install Docker Desktop:
- Mac: https://docs.docker.com/desktop/install/mac-install/
- Linux: https://docs.docker.com/desktop/install/linux-install/
- Windows: https://docs.docker.com/desktop/install/windows-install/
```

**Stop if:** Docker not installed

### Step 0.2: Verify Docker is Running

```bash
# Check Docker daemon
docker ps

# Expected: List of containers (or empty list)
# Error: "Cannot connect to Docker daemon" means Docker isn't running
```

**If not running:**
```
Docker Desktop is not running. Please:
1. Open Docker Desktop application
2. Wait for the whale icon to be stable (not animated)
3. Try again
```

**Stop if:** Docker not running

### Step 0.3: Check Docker Compose

```bash
# Modern Docker includes compose
docker compose version

# Expected: Docker Compose version v2.x.x or higher
```

**Note:** We use `docker compose` (not `docker-compose`)

### Step 0.4: Check Available Ports

```bash
# Check if ports are available
lsof -i :3000 -i :4317 -i :4318 -i :8889 -i :9090 -i :3100

# Expected: No output (ports are free)
```

**If ports in use:**
```
The following ports are required but already in use:
- 3000: Grafana
- 4317: OTEL Collector (gRPC)
- 4318: OTEL Collector (HTTP)
- 8889: OTEL Collector (Prometheus exporter)
- 9090: Prometheus
- 3100: Loki

Options:
1. Stop services using these ports
2. Modify port mappings in docker-compose.yml (advanced)
```

**Stop if:** Critical ports (3000, 4317, 9090) are in use

### Step 0.5: Check Disk Space

```bash
# Check available disk space
df -h ~

# Minimum: 2GB free (for Docker images ~1.5GB + data volumes)
# Recommended: 5GB+ free for comfortable operation
```

**If low disk space:**
```
Low disk space detected. Setup requires:
- Initial: ~1.5GB for Docker images (OTEL, Prometheus, Grafana, Loki)
- Runtime: 500MB+ for data volumes (grows over time)
- Minimum: 2GB free disk space required

Please free up space before continuing.
```

---

## Phase 1: Directory Structure Creation

### Step 1.1: Create Base Directory

```bash
mkdir -p ~/.claude/telemetry/{dashboards,docs}
cd ~/.claude/telemetry
```

**Verify:**
```bash
ls -la ~/.claude/telemetry
# Should show: dashboards/ and docs/ directories
```

---

## Phase 2: Configuration File Generation

### Step 2.1: Create docker-compose.yml

**Template:** `templates/docker-compose-template.yml`

```yaml
services:
  # OpenTelemetry Collector - receives telemetry from Claude Code
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.115.1
    container_name: claude-otel-collector
    command: ["--config=/etc/otel-collector-config.yml"]
    volumes:
      - ./otel-collector-config.yml:/etc/otel-collector-config.yml
    ports:
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
      - "8889:8889"   # Prometheus metrics exporter
    networks:
      - claude-telemetry

  # Prometheus - stores metrics
  prometheus:
    image: prom/prometheus:v2.55.1
    container_name: claude-prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - claude-telemetry
    depends_on:
      - otel-collector

  # Loki - stores logs
  loki:
    image: grafana/loki:3.0.0
    container_name: claude-loki
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - loki-data:/loki
    networks:
      - claude-telemetry

  # Grafana - visualization dashboards
  grafana:
    image: grafana/grafana:11.3.0
    container_name: claude-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml
    networks:
      - claude-telemetry
    depends_on:
      - prometheus
      - loki

networks:
  claude-telemetry:
    driver: bridge

volumes:
  prometheus-data:
  loki-data:
  grafana-data:
```

**Write to:** `~/.claude/telemetry/docker-compose.yml`

**Note on Image Versions:**
- Versions are pinned to prevent breaking changes from upstream
- Current versions (tested and stable):
  - OTEL Collector: 0.115.1
  - Prometheus: v2.55.1
  - Loki: 3.0.0
  - Grafana: 11.3.0
- To update: Change version tags in docker-compose.yml and run `docker compose pull`

### Step 2.2: Create OTEL Collector Configuration

**Template:** `templates/otel-collector-config-template.yml`

**CRITICAL:** Use `debug` exporter, not deprecated `logging` exporter

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

  resource:
    attributes:
      - key: service.name
        value: claude-code
        action: upsert

  memory_limiter:
    check_interval: 1s
    limit_mib: 512

exporters:
  # Export metrics to Prometheus
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: claude_code
    const_labels:
      source: claude_code_telemetry

  # Export logs to Loki via OTLP HTTP
  otlphttp/loki:
    endpoint: http://loki:3100/otlp
    tls:
      insecure: true

  # Debug exporter (replaces deprecated logging exporter)
  debug:
    verbosity: normal

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch, resource]
      exporters: [prometheus, debug]

    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, resource]
      exporters: [otlphttp/loki, debug]

  telemetry:
    logs:
      level: info
```

**Write to:** `~/.claude/telemetry/otel-collector-config.yml`

### Step 2.3: Create Prometheus Configuration

**Template:** `templates/prometheus-config-template.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'otel-collector'
    static_configs:
      - targets: ['otel-collector:8889']
```

**Write to:** `~/.claude/telemetry/prometheus.yml`

### Step 2.4: Create Grafana Datasources Configuration

**Template:** `templates/grafana-datasources-template.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: true
```

**Write to:** `~/.claude/telemetry/grafana-datasources.yml`

### Step 2.5: Create Management Scripts

**Start Script:**

```bash
#!/bin/bash
# start-telemetry.sh

echo "🚀 Starting Claude Code Telemetry Stack..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

cd ~/.claude/telemetry || exit 1

# Start containers
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check container status
echo ""
echo "📊 Container Status:"
docker ps --filter "name=claude-" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "✅ Telemetry stack started!"
echo ""
echo "🌐 Access URLs:"
echo "   Grafana:    http://localhost:3000 (admin/admin)"
echo "   Prometheus: http://localhost:9090"
echo "   Loki:       http://localhost:3100"
echo ""
echo "📝 Next steps:"
echo "   1. Restart Claude Code to activate telemetry"
echo "   2. Import dashboards into Grafana"
echo "   3. Use Claude Code normally - metrics will appear in ~60 seconds"
```

**Write to:** `~/.claude/telemetry/start-telemetry.sh`

```bash
chmod +x ~/.claude/telemetry/start-telemetry.sh
```

**Stop Script:**

```bash
#!/bin/bash
# stop-telemetry.sh

echo "🛑 Stopping Claude Code Telemetry Stack..."

cd ~/.claude/telemetry || exit 1

docker compose down

echo "✅ Telemetry stack stopped"
echo ""
echo "Note: Data is preserved in Docker volumes."
echo "To start again: ./start-telemetry.sh"
echo "To completely remove all data: ./cleanup-telemetry.sh"
```

**Write to:** `~/.claude/telemetry/stop-telemetry.sh`

```bash
chmod +x ~/.claude/telemetry/stop-telemetry.sh
```

**Cleanup Script (Full Data Removal):**

```bash
#!/bin/bash
# cleanup-telemetry.sh

echo "⚠️  WARNING: This will remove ALL telemetry data including:"
echo "  - All containers"
echo "  - All Docker volumes (Grafana, Prometheus, Loki data)"
echo "  - Network configuration"
echo ""
read -p "Are you sure you want to proceed? (yes/no): " -r
echo

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Performing full cleanup of Claude Code telemetry stack..."

cd ~/.claude/telemetry || exit 1

docker compose down -v

echo ""
echo "✅ Full cleanup complete!"
echo ""
echo "Removed:"
echo "  ✓ All containers (otel-collector, prometheus, loki, grafana)"
echo "  ✓ All volumes (all historical data)"
echo "  ✓ Network configuration"
echo ""
echo "Preserved:"
echo "  ✓ Configuration files in ~/.claude/telemetry/"
echo "  ✓ Claude Code settings in ~/.claude/settings.json"
echo ""
echo "To start fresh: ./start-telemetry.sh"
```

**Write to:** `~/.claude/telemetry/cleanup-telemetry.sh`

```bash
chmod +x ~/.claude/telemetry/cleanup-telemetry.sh
```

---

## Phase 3: Start Docker Containers

### Step 3.1: Start All Services

```bash
cd ~/.claude/telemetry
docker compose up -d
```

**Expected output:**
```
[+] Running 5/5
 ✔ Network claude_claude-telemetry     Created
 ✔ Container claude-loki               Started
 ✔ Container claude-otel-collector     Started
 ✔ Container claude-prometheus         Started
 ✔ Container claude-grafana            Started
```

### Step 3.2: Verify Containers are Running

```bash
docker ps --filter "name=claude-" --format "table {{.Names}}\t{{.Status}}"
```

**Expected:** All 4 containers showing "Up X seconds/minutes"

**If OTEL Collector is not running:**
```bash
# Check logs
docker logs claude-otel-collector
```

**Common issue:** "logging exporter deprecated" error
**Solution:** Config file uses `debug` exporter (already fixed in template)

### Step 3.3: Wait for Services to be Healthy

```bash
# Give services time to initialize
sleep 10

# Test Prometheus
curl -s http://localhost:9090/-/healthy
# Expected: Prometheus is Healthy.

# Test Grafana
curl -s http://localhost:3000/api/health | jq
# Expected: {"database": "ok", ...}
```

---

## Phase 4: Update Claude Code Settings

### Step 4.1: Backup Existing Settings

```bash
cp ~/.claude/settings.json ~/.claude/settings.json.backup
```

### Step 4.2: Read Current Settings

```bash
# Read existing settings
cat ~/.claude/settings.json
```

### Step 4.3: Merge Telemetry Configuration

**Add to settings.json `env` section:**

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
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

**Template:** `templates/settings-env-template.json`

**Note:** Merge with existing env vars, don't replace entire settings file

### Step 4.4: Verify Settings Updated

```bash
cat ~/.claude/settings.json | grep CLAUDE_CODE_ENABLE_TELEMETRY
# Expected: "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
```

---

## Phase 5: Grafana Dashboard Import

### Step 5.1: Detect Prometheus Datasource UID

**Option A: Via Grafana API**

```bash
curl -s http://admin:admin@localhost:3000/api/datasources | \
  jq '.[] | select(.type=="prometheus") | {name, uid}'
```

**Expected:**
```json
{
  "name": "Prometheus",
  "uid": "PBFA97CFB590B2093"
}
```

**Option B: Manual Detection**
1. Open http://localhost:3000
2. Go to Connections → Data sources
3. Click Prometheus
4. Note the UID from the URL: `/datasources/edit/{UID}`

### Step 5.2: Fix Dashboard with Correct UID

**Read dashboard template:** `dashboards/claude-code-overview-template.json`

**Replace all instances of:**
```json
"datasource": {
  "type": "prometheus",
  "uid": "prometheus"
}
```

**With:**
```json
"datasource": {
  "type": "prometheus",
  "uid": "PBFA97CFB590B2093"
}
```

**Use detected UID from Step 5.1**

### Step 5.3: Verify Metric Names

**CRITICAL:** Claude Code metrics use double prefix: `claude_code_claude_code_*`

**Verify actual metric names:**
```bash
curl -s 'http://localhost:9090/api/v1/label/__name__/values' | \
  grep claude_code
```

**Expected metrics:**
- `claude_code_claude_code_active_time_seconds_total`
- `claude_code_claude_code_commit_count_total`
- `claude_code_claude_code_cost_usage_USD_total`
- `claude_code_claude_code_lines_of_code_count_total`
- `claude_code_claude_code_token_usage_tokens_total`

**Dashboard queries must use these exact names**

### Step 5.4: Save Corrected Dashboard

**Write to:** `~/.claude/telemetry/dashboards/claude-code-overview.json`

### Step 5.5: Import Dashboard

**Option A: Via Grafana UI**
1. Open http://localhost:3000 (admin/admin)
2. Dashboards → New → Import
3. Upload JSON file: `~/.claude/telemetry/dashboards/claude-code-overview.json`
4. Click Import

**Option B: Via API**
```bash
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @~/.claude/telemetry/dashboards/claude-code-overview.json
```

---

## Phase 6: Verification & Testing

### Step 6.1: Verify OTEL Collector Receiving Data

**Note:** Claude Code must be restarted for telemetry to activate!

```bash
# Check OTEL Collector logs for incoming data
docker logs claude-otel-collector --tail 50 | grep -i "received"
```

**Expected:** Messages about receiving OTLP data

**If no data:**
```
Reminder: You must restart Claude Code for telemetry to activate.
1. Exit current Claude Code session
2. Start new session: claude
3. Wait 60 seconds
4. Check again
```

### Step 6.2: Query Prometheus for Metrics

```bash
# Check if any claude_code metrics exist
curl -s 'http://localhost:9090/api/v1/label/__name__/values' | \
  jq '.data[] | select(. | startswith("claude_code"))'
```

**Expected:** List of claude_code metrics

**Sample query:**
```bash
curl -s 'http://localhost:9090/api/v1/query?query=claude_code_claude_code_lines_of_code_count_total' | \
  jq '.data.result'
```

**Expected:** Non-empty result array

### Step 6.3: Test Grafana Dashboard

1. Open http://localhost:3000
2. Navigate to imported dashboard
3. Check panels show data (or "No data" if Claude Code hasn't been used yet)

**If "No data":**
- Normal if Claude Code hasn't generated any activity yet
- Use Claude Code for 1-2 minutes
- Refresh dashboard

**If "Datasource not found":**
- UID mismatch - go back to Step 5.1

**If queries fail:**
- Metric name mismatch - verify double prefix

### Step 6.4: Generate Test Data

**To populate dashboard quickly:**
```
Use Claude Code to:
1. Ask a question (generates token usage)
2. Request a code modification (generates LOC metrics)
3. Have a conversation (generates active time)
```

**Wait 60 seconds, then refresh Grafana dashboard**

---

## Phase 7: Documentation & Quickstart Guide

### Step 7.1: Create Quickstart Guide

**Write to:** `~/.claude/telemetry/docs/quickstart.md`

**Include:**
- URLs and credentials
- Management commands (start/stop)
- What metrics are being collected
- How to access dashboards
- Troubleshooting quick reference

**Template:** `data/quickstart-template.md`

### Step 7.2: Provide User Summary

```
✅ Setup Complete!

📦 Installation:
   Location: ~/.claude/telemetry/
   Containers: 4 running (OTEL Collector, Prometheus, Loki, Grafana)

🌐 Access URLs:
   Grafana:    http://localhost:3000 (admin/admin)
   Prometheus: http://localhost:9090
   OTEL Collector: localhost:4317 (gRPC), localhost:4318 (HTTP)

📊 Dashboards Imported:
   ✓ Claude Code - Overview

📝 What's Being Collected:
   • Session counts and active time
   • Token usage (input/output/cached)
   • API costs by model
   • Lines of code modified
   • Commits and PRs created
   • Tool execution metrics

⚙️  Management:
   Start:   ~/.claude/telemetry/start-telemetry.sh
   Stop:    ~/.claude/telemetry/stop-telemetry.sh (preserves data)
   Cleanup: ~/.claude/telemetry/cleanup-telemetry.sh (removes all data)
   Logs:    docker logs claude-otel-collector

🚀 Next Steps:
   1. ✅ Restart Claude Code (telemetry activates on startup)
   2. Use Claude Code normally
   3. Check dashboard in ~60 seconds
   4. Review quickstart: ~/.claude/telemetry/docs/quickstart.md

📚 Documentation:
   - Quickstart: ~/.claude/telemetry/docs/quickstart.md
   - Metrics Reference: data/metrics-reference.md
   - Troubleshooting: data/troubleshooting.md
```

---

## Cleanup Instructions

### Remove Stack (Keep Data)
```bash
cd ~/.claude/telemetry
docker compose down
```

### Remove Stack and Data
```bash
cd ~/.claude/telemetry
docker compose down -v
```

### Remove Telemetry from Claude Code
Edit `~/.claude/settings.json` and remove the `env` section with telemetry variables, or set:
```json
"CLAUDE_CODE_ENABLE_TELEMETRY": "0"
```

Then restart Claude Code.

---

## Troubleshooting

See `data/troubleshooting.md` for detailed solutions to common issues.

**Quick fixes:**
- Container won't start → Check logs: `docker logs claude-otel-collector`
- No metrics → Restart Claude Code
- Dashboard broken → Verify datasource UID
- Wrong metric names → Use double prefix: `claude_code_claude_code_*`
