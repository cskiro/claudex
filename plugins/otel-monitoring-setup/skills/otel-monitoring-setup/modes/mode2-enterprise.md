# Mode 2: Enterprise Setup (Connect to Existing Infrastructure)

**Goal:** Configure Claude Code to send telemetry to centralized company infrastructure

**When to use:**
- Company has centralized OTEL Collector endpoint
- Team rollout scenario
- Want aggregated team metrics
- Privacy/compliance requires centralized control
- No need for local Grafana dashboards

**Prerequisites:**
- OTEL Collector endpoint URL (e.g., `https://otel.company.com:4317`)
- Authentication credentials (API key or mTLS certificates)
- Optional: Team/department identifiers
- Write access to `~/.claude/settings.json`

**Estimated Time:** 2-3 minutes

---

## Phase 0: Gather Requirements

### Step 0.1: Collect endpoint information from user

Ask the user for the following details:

1. **OTEL Collector Endpoint URL**
   - Format: `https://otel.company.com:4317` or `http://otel.company.com:4318`
   - Protocol: gRPC (port 4317) or HTTP (port 4318)

2. **Authentication Method**
   - API Key/Bearer Token
   - mTLS certificates
   - Basic Auth
   - No authentication (internal network)

3. **Team/Environment Identifiers**
   - Team name (e.g., `team=platform`)
   - Environment (e.g., `environment=production`)
   - Department (e.g., `department=engineering`)
   - Any other custom attributes

4. **Optional: Protocol Preferences**
   - Default: gRPC (more efficient)
   - Alternative: HTTP (better firewall compatibility)

**Example Questions:**

```
To configure enterprise telemetry, I need a few details:

1. **Endpoint:** What is your OTEL Collector endpoint URL?
   (e.g., https://otel.company.com:4317)

2. **Protocol:** HTTPS or HTTP? gRPC or HTTP/protobuf?

3. **Authentication:** Do you have an API key, certificate, or other credentials?

4. **Team identifier:** What team/department should metrics be tagged with?
   (e.g., team=platform, department=engineering)
```

---

## Phase 1: Backup Existing Settings

### Step 1.1: Backup settings.json

**Always backup before modifying!**

```bash
# Check if settings.json exists
if [ -f ~/.claude/settings.json ]; then
  cp ~/.claude/settings.json ~/.claude/settings.json.backup.$(date +%Y%m%d-%H%M%S)
  echo "✅ Backup created: ~/.claude/settings.json.backup.$(date +%Y%m%d-%H%M%S)"
else
  echo "⚠️  No existing settings.json found - will create new one"
fi
```

### Step 1.2: Read existing settings

```bash
# Check current settings
cat ~/.claude/settings.json
```

**Important:** Preserve all existing settings when adding telemetry configuration!

---

## Phase 2: Update Claude Code Settings

### Step 2.1: Determine configuration based on authentication method

**Scenario A: API Key Authentication**

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer YOUR_API_KEY_HERE",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production,deployment=enterprise"
  }
}
```

**Scenario B: mTLS Certificate Authentication**

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.company.com:4317",
    "OTEL_EXPORTER_OTLP_CERTIFICATE": "/path/to/client-cert.pem",
    "OTEL_EXPORTER_OTLP_CLIENT_KEY": "/path/to/client-key.pem",
    "OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE": "/path/to/ca-cert.pem",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production,deployment=enterprise"
  }
}
```

**Scenario C: HTTP Protocol (Port 4318)**

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.company.com:4318",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer YOUR_API_KEY_HERE",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production,deployment=enterprise"
  }
}
```

**Scenario D: No Authentication (Internal Network)**

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://otel.internal.company.com:4317",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production,deployment=enterprise"
  }
}
```

### Step 2.2: Update settings.json

**Method 1: Manual Update (Safest)**

1. Open `~/.claude/settings.json` in editor
2. Merge the telemetry configuration into existing `env` object
3. Preserve all other settings
4. Save file

**Method 2: Programmatic Update (Use with Caution)**

```bash
# Read existing settings
existing_settings=$(cat ~/.claude/settings.json)

# Create merged settings (requires jq)
cat ~/.claude/settings.json | jq '. + {
  "env": (.env // {} | . + {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer YOUR_API_KEY_HERE",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production,deployment=enterprise"
  })
}' > ~/.claude/settings.json.new

# Validate JSON
if jq empty ~/.claude/settings.json.new 2>/dev/null; then
  mv ~/.claude/settings.json.new ~/.claude/settings.json
  echo "✅ Settings updated successfully"
else
  echo "❌ Invalid JSON - restoring backup"
  rm ~/.claude/settings.json.new
fi
```

### Step 2.3: Validate configuration

```bash
# Check that settings.json is valid JSON
jq empty ~/.claude/settings.json

# Display telemetry configuration
jq '.env | with_entries(select(.key | startswith("OTEL_") or . == "CLAUDE_CODE_ENABLE_TELEMETRY"))' ~/.claude/settings.json
```

---

## Phase 3: Test Connectivity (Optional)

### Step 3.1: Test OTEL endpoint reachability

```bash
# Test gRPC endpoint (port 4317)
nc -zv otel.company.com 4317

# Test HTTP endpoint (port 4318)
curl -v https://otel.company.com:4318/v1/metrics -d '{}' -H "Content-Type: application/json"
```

### Step 3.2: Validate authentication

```bash
# Test with API key
curl -v https://otel.company.com:4318/v1/metrics \
  -H "Authorization: Bearer YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{}'

# Expected: 200 or 401/403 (tells us auth is working)
# Unexpected: Connection refused, timeout (network issue)
```

---

## Phase 4: User Instructions

### Step 4.1: Provide restart instructions

**Display to user:**

```
✅ Configuration complete!

**Important Next Steps:**

1. **Restart Claude Code** for telemetry to take effect
   - Telemetry configuration is only loaded at startup
   - Close all Claude Code sessions and restart

2. **Verify with your platform team** that they see metrics
   - Metrics should appear within 60 seconds of restart
   - Tagged with: team=platform, environment=production
   - Metric prefix: claude_code_claude_code_*

3. **Dashboard access**
   - Contact your platform team for Grafana/dashboard URLs
   - Dashboards should be centrally managed

**Troubleshooting:**

If metrics don't appear:
- Check network connectivity to OTEL endpoint
- Verify authentication credentials are correct
- Check firewall rules allow outbound connections
- Review OTEL Collector logs on backend (platform team)
- Verify OTEL_EXPORTER_OTLP_ENDPOINT is correct

**Rollback:**

If you need to disable telemetry:
- Restore backup: cp ~/.claude/settings.json.backup.TIMESTAMP ~/.claude/settings.json
- Or set: "CLAUDE_CODE_ENABLE_TELEMETRY": "0"
```

---

## Phase 5: Create Team Rollout Documentation

### Step 5.1: Generate rollout guide for team distribution

**Create file: `claude-code-telemetry-setup-guide.md`**

```markdown
# Claude Code Telemetry Setup Guide

**For:** [Team Name] Team Members
**Last Updated:** [Date]

## Overview

We're collecting Claude Code usage telemetry to:
- Track API costs and optimize spending
- Measure productivity metrics (LOC, commits, PRs)
- Understand token usage patterns
- Identify high-value use cases

**Privacy:** All metrics are aggregated and anonymized at the team level.

## Setup Instructions

### Step 1: Backup Your Settings

```bash
cp ~/.claude/settings.json ~/.claude/settings.json.backup
```

### Step 2: Update Configuration

Add the following to your `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer [PROVIDED_BY_PLATFORM_TEAM]",
    "OTEL_METRIC_EXPORT_INTERVAL": "60000",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000",
    "OTEL_LOG_USER_PROMPTS": "1",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "true",
    "OTEL_METRICS_INCLUDE_VERSION": "true",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "true",
    "OTEL_RESOURCE_ATTRIBUTES": "team=[TEAM_NAME],environment=production"
  }
}
```

**Important:** Replace `[PROVIDED_BY_PLATFORM_TEAM]` with your API key.

### Step 3: Restart Claude Code

Close all Claude Code sessions and restart for changes to take effect.

### Step 4: Verify Setup

After 5 minutes of usage:
1. Check team dashboard: [DASHBOARD_URL]
2. Verify your metrics appear in the team aggregation
3. Contact [TEAM_CONTACT] if you have issues

## What's Being Collected?

**Metrics:**
- Session counts and active time
- Token usage (input, output, cached)
- API costs by model
- Lines of code modified
- Commits and PRs created

**Events/Logs:**
- User prompts (anonymized)
- Tool executions
- API requests

**NOT Collected:**
- Source code content
- File names or paths
- Personal identifiers (beyond account UUID for deduplication)

## Dashboard Access

**Team Dashboard:** [URL]
**Login:** Use your company SSO

## Support

**Issues?** Contact [TEAM_CONTACT] or #claude-code-telemetry Slack channel

**Opt-Out:** Contact [TEAM_CONTACT] if you need to opt out for specific projects
```

---

## Phase 6: Success Criteria

### Checklist for Mode 2 completion:

- ✅ Backed up existing settings.json
- ✅ Updated settings with correct OTEL endpoint
- ✅ Added authentication (API key or certificates)
- ✅ Set team/environment resource attributes
- ✅ Validated JSON configuration
- ✅ Tested connectivity (optional)
- ✅ Provided restart instructions to user
- ✅ Created team rollout documentation (if applicable)

**Expected outcome:**
- Claude Code sends telemetry to central endpoint within 60 seconds of restart
- Platform team can see metrics tagged with team identifier
- User has clear instructions for verification and troubleshooting

---

## Troubleshooting

### Issue 1: Connection Refused

**Symptoms:** Claude Code can't reach OTEL endpoint

**Checks:**
```bash
# Test network connectivity
ping otel.company.com

# Test port access
nc -zv otel.company.com 4317

# Check corporate VPN/proxy
echo $HTTPS_PROXY
```

**Solutions:**
- Connect to corporate VPN
- Use HTTP proxy if required: `HTTPS_PROXY=http://proxy.company.com:8080`
- Try HTTP protocol (port 4318) instead of gRPC
- Contact network team to allow outbound connections

### Issue 2: Authentication Failed

**Symptoms:** 401 or 403 errors in logs

**Checks:**
```bash
# Verify API key format
jq '.env.OTEL_EXPORTER_OTLP_HEADERS' ~/.claude/settings.json

# Test manually
curl -v https://otel.company.com:4318/v1/metrics \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{}'
```

**Solutions:**
- Verify API key is correct and not expired
- Check header format: `Authorization=Bearer TOKEN` (no quotes, equals sign)
- Confirm permissions with platform team
- Try rotating API key

### Issue 3: Metrics Not Appearing

**Symptoms:** Platform team doesn't see metrics after 5 minutes

**Checks:**
```bash
# Verify telemetry is enabled
jq '.env.CLAUDE_CODE_ENABLE_TELEMETRY' ~/.claude/settings.json

# Check endpoint configuration
jq '.env.OTEL_EXPORTER_OTLP_ENDPOINT' ~/.claude/settings.json

# Confirm Claude Code was restarted
ps aux | grep claude
```

**Solutions:**
- Restart Claude Code (telemetry loads at startup only)
- Verify endpoint URL has correct protocol and port
- Check with platform team if OTEL Collector is receiving data
- Review OTEL Collector logs for errors
- Verify resource attributes match expected format

### Issue 4: Certificate Errors (mTLS)

**Symptoms:** SSL/TLS handshake errors

**Checks:**
```bash
# Verify certificate paths
ls -la /path/to/client-cert.pem
ls -la /path/to/client-key.pem
ls -la /path/to/ca-cert.pem

# Check certificate validity
openssl x509 -in /path/to/client-cert.pem -noout -dates
```

**Solutions:**
- Ensure certificate files are readable
- Verify certificates haven't expired
- Check certificate chain is complete
- Confirm CA certificate matches server
- Contact platform team for new certificates if needed

---

## Enterprise Configuration Examples

### Example 1: Multi-Environment Setup

**Development:**
```json
"OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=development,user=john.doe"
```

**Staging:**
```json
"OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=staging,user=john.doe"
```

**Production:**
```json
"OTEL_RESOURCE_ATTRIBUTES": "team=platform,environment=production,user=john.doe"
```

### Example 2: Department-Level Aggregation

```json
"OTEL_RESOURCE_ATTRIBUTES": "department=engineering,team=platform,squad=backend,environment=production"
```

Enables queries like:
- Cost by department
- Usage by team within department
- Squad-level productivity metrics

### Example 3: Project-Based Tagging

```json
"OTEL_RESOURCE_ATTRIBUTES": "team=platform,project=api-v2-migration,environment=production"
```

Track costs and effort for specific initiatives.

---

## Additional Resources

- **OTEL Specification:** https://opentelemetry.io/docs/specs/otel/
- **Claude Code Metrics Reference:** See `data/metrics-reference.md`
- **Enterprise Architecture:** See `data/enterprise-architecture.md`
- **Team Dashboard Queries:** See `data/prometheus-queries.md`

---

**Mode 2 Complete!** ✅
