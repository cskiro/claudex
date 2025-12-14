#!/bin/bash
# Start Claude Code Telemetry Stack

echo "Starting Claude Code telemetry stack..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "❌ Error: Docker is not running. Please start Docker Desktop first."
  exit 1
fi

# Navigate to telemetry directory
cd ~/.claude/telemetry || exit 1

# Start containers
docker compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check container status
echo ""
echo "Container Status:"
docker compose ps

echo ""
echo "✅ Telemetry stack started!"
echo ""
echo "Access Points:"
echo "  - Grafana:   http://localhost:3000 (admin/admin)"
echo "  - Prometheus: http://localhost:9090"
echo "  - Loki:      http://localhost:3100"
echo ""
echo "OTEL Endpoints:"
echo "  - gRPC:      http://localhost:4317"
echo "  - HTTP:      http://localhost:4318"
echo ""
echo "Next: Restart Claude Code to start sending telemetry data"
