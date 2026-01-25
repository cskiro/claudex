#!/bin/bash
# Full Cleanup of Claude Code Telemetry Stack
# WARNING: This removes all data including Docker volumes

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

# Navigate to telemetry directory
cd ~/.claude/telemetry || exit 1

# Stop and remove containers, networks, and volumes
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
