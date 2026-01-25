#!/bin/bash
# Stop Claude Code Telemetry Stack

echo "Stopping Claude Code telemetry stack..."

# Navigate to telemetry directory
cd ~/.claude/telemetry || exit 1

# Stop containers
docker compose down

echo "✅ Telemetry stack stopped!"
echo ""
echo "Note: Data is preserved in Docker volumes."
echo "To start again: ./start-telemetry.sh"
echo "To completely remove all data: ./cleanup-telemetry.sh"
