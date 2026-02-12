# Managed by swe-standards plugin — edits may be overwritten by /swe-standards:sync

# Vitest CPU Protection Standards (Universal)

## Problem Statement

Multiple concurrent Vitest instances can overwhelm CPU resources, causing:
- Thermal throttling (CPU reaches 100%)
- System instability
- Degraded development experience

**Root Cause:** Each Vitest instance spawns independent worker threads with no global coordination.

---

## Solution: Thread Limiting

### Environment Variables

Set in your shell config:

```bash
export VITEST_MAX_THREADS=4      # Max threads per instance
export VITEST_MIN_THREADS=1      # Min threads per instance
```

### Shell Wrapper (vtest)

Create a wrapper function that enforces limits:

```bash
vtest() {
  local running=$(pgrep -f "vitest" | wc -l)
  local max_threads=${VITEST_MAX_THREADS:-4}

  if [ "$running" -gt 1 ]; then
    max_threads=$((max_threads / running))
    echo "Warning: $running Vitest instances detected, reducing to $max_threads threads"
  fi

  npx vitest --pool=threads --poolOptions.threads.maxThreads="$max_threads" "$@"
}
```

### Status Monitor (vtest_status)

```bash
vtest_status() {
  echo "=== Vitest CPU Status ==="
  echo ""
  echo "Running instances: $(pgrep -f vitest | wc -l)"
  echo "Thread limit: ${VITEST_MAX_THREADS:-4}"
  echo ""
  echo "Processes:"
  ps aux | grep -E "[v]itest" | awk '{printf "  %s  %s%%  %s%%  %s\n", $2, $3, $4, $11}'
  echo ""
  echo "System:"
  echo "  CPUs: $(sysctl -n hw.ncpu 2>/dev/null || nproc)"
  echo "  Load: $(uptime | awk -F'load average:' '{print $2}')"
}
```

---

## Recommended Limits

| Scenario | Max Threads | Rationale |
|----------|-------------|-----------|
| Single instance | 4 | Fast feedback, leaves headroom |
| 2 concurrent instances | 3 each | Auto-reduced by wrapper |
| 3+ concurrent instances | 2 each | Prevents CPU thrashing |
| CI environment | 4-8 | Dedicated resources |

---

## CI Configuration

```typescript
// vitest.config.ts
poolOptions: {
  threads: {
    maxThreads: process.env.CI ? 8 : 4,
  },
}
```

---

## Troubleshooting

### Tests running slowly
```bash
VITEST_MAX_THREADS=6 vtest --run
```

### System still sluggish
```bash
vtest_status
pkill -f vitest  # Kill all Vitest instances if needed
```
