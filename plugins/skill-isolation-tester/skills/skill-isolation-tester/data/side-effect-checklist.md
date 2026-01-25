# Side Effect Detection Checklist

## Overview

This checklist helps identify all side effects caused by skill execution. Side effects are any changes to the system state beyond the skill's primary output. Proper detection ensures skills are well-behaved and clean up after themselves.

## Why Side Effects Matter

**Portability:** Skills with untracked side effects may not work for other users

**Cleanliness:** Leftover files and processes waste resources

**Security:** Unexpected system modifications are security risks

**Documentation:** Users need to know what a skill changes

## Categories of Side Effects

## 1. Filesystem Changes

### Files Created

**What to Check:**
- Files in skill directory
- Files in /tmp/ or /var/tmp/
- Files in user home directory (~/)
- Files in system directories (/usr/local/, /opt/)
- Hidden files (.*) and cache directories (.cache/)
- Lock files (.lock, .pid)

**How to Detect:**
```bash
# Before execution
find /path -type f > /tmp/before-files.txt

# After execution
find /path -type f > /tmp/after-files.txt

# Compare
diff /tmp/before-files.txt /tmp/after-files.txt | grep "^>" | sed 's/^> //'
```

**Expected Behavior:**
- ✅ Temporary files in /tmp cleaned up before exit
- ✅ Output files in current directory or specified location
- ✅ Cache files in ~/.cache/skill-name/ (acceptable)
- ❌ Random files scattered across filesystem
- ❌ Files in system directories without explicit permission

**Severity:**
- **LOW**: Cache files in proper location
- **MEDIUM**: Temp files not cleaned up
- **HIGH**: Files in system directories
- **CRITICAL**: Files overwriting existing user data

### Files Modified

**What to Check:**
- Project files (package.json, tsconfig.json, etc.)
- Configuration files (.env, .config/)
- System configs (/etc/*)
- User configs (~/.bashrc, ~/.zshrc)
- Git repository files (.git/)

**How to Detect:**
```bash
# Take checksums before
find /path -type f -exec md5sum {} \; > /tmp/before-checksums.txt

# After execution
find /path -type f -exec md5sum {} \; > /tmp/after-checksums.txt

# Find modified files
diff /tmp/before-checksums.txt /tmp/after-checksums.txt
```

**Expected Behavior:**
- ✅ Only files explicitly in skill's scope modified
- ✅ Backup created before modifying important files
- ✅ Modifications clearly documented in output
- ❌ Configuration files modified without notice
- ❌ Git repository modified unexpectedly
- ❌ System files changed

**Severity:**
- **LOW**: Intended file modifications (skill's purpose)
- **MEDIUM**: Unintended project file changes
- **HIGH**: User config modifications without consent
- **CRITICAL**: System file modifications

### Files Deleted

**What to Check:**
- Files in skill scope (expected deletions)
- Temp files created by skill
- User files outside skill scope
- System files

**How to Detect:**
```bash
# Compare before/after file lists
diff /tmp/before-files.txt /tmp/after-files.txt | grep "^<" | sed 's/^< //'
```

**Expected Behavior:**
- ✅ Only temporary files created by skill deleted
- ✅ Deletions are part of skill's documented purpose
- ❌ User files deleted without explicit permission
- ❌ Project files deleted accidentally
- ❌ System files deleted

**Severity:**
- **LOW**: Skill's own temp files deleted (cleanup)
- **MEDIUM**: Unexpected file deletions in project
- **HIGH**: User files deleted
- **CRITICAL**: System files or important data deleted

### Directory Changes

**What to Check:**
- New directories created
- Working directory changed
- Directories removed

**How to Detect:**
```bash
# List directories before/after
find /path -type d > /tmp/before-dirs.txt
find /path -type d > /tmp/after-dirs.txt
diff /tmp/before-dirs.txt /tmp/after-dirs.txt
```

**Expected Behavior:**
- ✅ Directories created for skill output
- ✅ Temp directories in /tmp
- ✅ Working directory restored after operations
- ❌ Empty directories left behind
- ❌ Directories created in unexpected locations

## 2. Process Management

### Processes Created

**What to Check:**
- Foreground processes (should complete)
- Background processes (daemons, services)
- Child processes (spawned by skill)
- Zombie processes

**How to Detect:**
```bash
# Before execution
ps aux > /tmp/before-processes.txt

# After execution (wait 30 seconds)
sleep 30
ps aux > /tmp/after-processes.txt

# Find new processes
diff /tmp/before-processes.txt /tmp/after-processes.txt | grep "^>"
```

**Expected Behavior:**
- ✅ All skill processes complete and exit
- ✅ No orphaned child processes
- ✅ Background services documented if needed
- ❌ Processes still running after skill exits
- ❌ Zombie processes
- ❌ High CPU/memory usage processes

**Severity:**
- **LOW**: Short-lived child processes that exit cleanly
- **MEDIUM**: Background processes that should have been stopped
- **HIGH**: Orphaned processes consuming resources
- **CRITICAL**: Runaway processes (infinite loops, memory leaks)

### Process Resource Usage

**What to Check:**
- CPU usage during and after execution
- Memory consumption
- Disk I/O
- Network I/O

**How to Detect:**
```bash
# Monitor during execution
top -b -n 1 > /tmp/resource-usage.txt

# Or use htop, ps aux, etc.
```

**Expected Behavior:**
- ✅ Reasonable resource usage for task
- ✅ Resources released after completion
- ❌ 100% CPU for extended time
- ❌ Memory leaks (growing usage)
- ❌ Excessive disk I/O

**Severity:**
- **LOW**: Temporary spike during execution
- **MEDIUM**: Higher than expected but acceptable
- **HIGH**: Excessive usage (> 80% CPU, > 1GB RAM)
- **CRITICAL**: Resource exhaustion (OOM, disk full)

## 3. System Configuration

### Environment Variables

**What to Check:**
- New environment variables set
- Modified PATH, HOME, etc.
- Shell configuration changes

**How to Detect:**
```bash
# Before
env | sort > /tmp/before-env.txt

# After
env | sort > /tmp/after-env.txt

# Compare
diff /tmp/before-env.txt /tmp/after-env.txt
```

**Expected Behavior:**
- ✅ No permanent environment changes
- ✅ Temporary env vars for skill only
- ❌ PATH modified globally
- ❌ System env vars changed

**Severity:**
- **LOW**: Temporary env vars in skill scope
- **MEDIUM**: PATH modified in current shell
- **HIGH**: .bashrc/.zshrc modified
- **CRITICAL**: System-wide env changes

### System Services

**What to Check:**
- Systemd services started
- Cron jobs created
- Launch agents/daemons (macOS)

**How to Detect:**
```bash
# Linux
systemctl list-units --type=service > /tmp/before-services.txt
# After
systemctl list-units --type=service > /tmp/after-services.txt
diff /tmp/before-services.txt /tmp/after-services.txt

# Cron jobs
crontab -l > /tmp/before-cron.txt
# After
crontab -l > /tmp/after-cron.txt
```

**Expected Behavior:**
- ✅ No services unless explicitly documented
- ✅ Services stopped after skill exits
- ❌ Services left running
- ❌ Cron jobs created without consent

**Severity:**
- **MEDIUM**: Services that should have been stopped
- **HIGH**: Unexpected service installations
- **CRITICAL**: System services modified

### Package Installations

**What to Check:**
- NPM packages (global)
- Python packages (pip)
- System packages (apt, brew)
- Ruby gems, Go modules, etc.

**How to Detect:**
```bash
# NPM global packages
npm list -g --depth=0 > /tmp/before-npm.txt
# After
npm list -g --depth=0 > /tmp/after-npm.txt
diff /tmp/before-npm.txt /tmp/after-npm.txt

# System packages (Debian/Ubuntu)
dpkg -l > /tmp/before-packages.txt
# After
dpkg -l > /tmp/after-packages.txt
```

**Expected Behavior:**
- ✅ All dependencies documented in README
- ✅ Local installations (in project directory)
- ❌ Global package installations without notice
- ❌ System package changes

**Severity:**
- **LOW**: Local project dependencies
- **MEDIUM**: Global NPM packages (if documented)
- **HIGH**: System packages installed
- **CRITICAL**: Conflicting package versions

## 4. Network Activity

### Connections Established

**What to Check:**
- HTTP/HTTPS requests
- WebSocket connections
- Database connections
- SSH connections

**How to Detect:**
```bash
# Monitor network during execution
# macOS
lsof -i -n -P | grep <skill-process>

# Linux
netstat -tupn | grep <skill-process>

# Or use tcpdump, wireshark for detailed analysis
```

**Expected Behavior:**
- ✅ All network requests documented
- ✅ HTTPS used for sensitive data
- ✅ Connections properly closed
- ❌ Unexpected outbound connections
- ❌ Data sent to unknown servers
- ❌ Connections left open

**Severity:**
- **LOW**: Documented API calls (HTTPS)
- **MEDIUM**: HTTP requests (not HTTPS)
- **HIGH**: Unexpected network destinations
- **CRITICAL**: Data exfiltration attempts

### Data Transmitted

**What to Check:**
- API payloads
- File uploads/downloads
- Metrics/telemetry data

**Expected Behavior:**
- ✅ Clear documentation of what's sent
- ✅ User consent for data transmission
- ✅ No sensitive data in plaintext
- ❌ Telemetry without consent
- ❌ Credentials sent over HTTP

## 5. Database & State

### Database Changes

**What to Check:**
- Tables created/dropped
- Records inserted/updated/deleted
- Schema migrations
- Indexes created

**How to Detect:**
```sql
-- Before (SQLite example)
SELECT * FROM sqlite_master WHERE type='table';

-- After
SELECT * FROM sqlite_master WHERE type='table';

-- Record counts
SELECT COUNT(*) FROM each_table;
```

**Expected Behavior:**
- ✅ Changes are part of skill's purpose
- ✅ Backup created before modifications
- ✅ Transactions used (rollback on error)
- ❌ Unexpected table drops
- ❌ Data loss without backup
- ❌ Schema changes without migration docs

### Cache & Session State

**What to Check:**
- Redis/Memcached keys
- Session files
- Browser storage (if skill uses web UI)

**Expected Behavior:**
- ✅ Cache properly namespaced
- ✅ Expired sessions cleaned up
- ❌ Cache pollution
- ❌ Stale session files

## 6. Permissions & Security

### File Permissions

**What to Check:**
- File permission changes (chmod)
- Ownership changes (chown)
- ACL modifications

**How to Detect:**
```bash
# Before
ls -la /path > /tmp/before-perms.txt

# After
ls -la /path > /tmp/after-perms.txt
diff /tmp/before-perms.txt /tmp/after-perms.txt
```

**Expected Behavior:**
- ✅ Appropriate permissions for created files
- ✅ No overly permissive files (777)
- ❌ Permissions changed on existing files
- ❌ World-writable files created

**Severity:**
- **MEDIUM**: Overly restrictive permissions
- **HIGH**: Overly permissive permissions (777)
- **CRITICAL**: System file permission changes

### Security Credentials

**What to Check:**
- API keys in files or logs
- Passwords in plaintext
- Certificates/keys created
- SSH keys modified

**Expected Behavior:**
- ✅ Credentials stored securely (keychain, vault)
- ✅ No credentials in logs or temp files
- ❌ API keys in plaintext files
- ❌ Passwords in shell history
- ❌ Private keys with wrong permissions

**Severity:**
- **HIGH**: Credentials in files
- **CRITICAL**: Credentials exposed to other users

## Automated Detection Script

```bash
#!/bin/bash
# side-effect-detector.sh

BEFORE_DIR="/tmp/skill-test-before"
AFTER_DIR="/tmp/skill-test-after"

mkdir -p "$BEFORE_DIR" "$AFTER_DIR"

# Capture before state
capture_state() {
  local DIR="$1"
  find /tmp -type f > "$DIR/tmp-files.txt"
  ps aux > "$DIR/processes.txt"
  env | sort > "$DIR/env.txt"
  npm list -g --depth=0 > "$DIR/npm-global.txt" 2>/dev/null
  netstat -tupn > "$DIR/network.txt" 2>/dev/null
  # Add more as needed
}

# Before
capture_state "$BEFORE_DIR"

# Run skill
echo "Execute skill now..."
read -p "Press enter when skill completes..."

# After
capture_state "$AFTER_DIR"

# Compare
echo "=== Side Effects Detected ==="
echo ""
echo "Files in /tmp:"
diff "$BEFORE_DIR/tmp-files.txt" "$AFTER_DIR/tmp-files.txt" | grep "^>" | wc -l

echo "Processes:"
diff "$BEFORE_DIR/processes.txt" "$AFTER_DIR/processes.txt" | grep "^>" | head -5

echo "Environment variables:"
diff "$BEFORE_DIR/env.txt" "$AFTER_DIR/env.txt"

echo "NPM global packages:"
diff "$BEFORE_DIR/npm-global.txt" "$AFTER_DIR/npm-global.txt"

# Detailed reports
echo ""
echo "Full reports in: $BEFORE_DIR and $AFTER_DIR"
```

## Reporting Template

```markdown
## Side Effects Report

### Filesystem Changes
- **Files Created**: X files
  - /tmp/skill-temp-123.log (5KB)
  - ~/.cache/skill-name/data.json (15KB)
- **Files Modified**: Y files
  - package.json (version updated)
- **Files Deleted**: Z files
  - /tmp/old-cache.json

### Process Management
- **Processes Created**: N
- **Orphaned Processes**: M (list if > 0)
- **Resource Usage**: Peak 45% CPU, 128MB RAM

### System Configuration
- **Env Vars Changed**: None
- **Services Started**: None
- **Packages Installed**: jq (1.6)

### Network Activity
- **Connections**: 3 HTTPS requests to api.example.com
- **Data Transmitted**: 1.2KB (API calls)

### Database Changes
- **Tables**: 1 created (skill_cache)
- **Records**: 15 inserted

### Security
- **Permissions**: All files 644 (appropriate)
- **Credentials**: No sensitive data detected

### Overall Assessment
✅ Cleanup: Mostly clean (3 temp files remaining)
⚠️  Documentation: Missing jq dependency in README
✅ Security: No issues
```

---

**Remember:** The goal is not zero side effects (that's impossible for useful skills), but **documented, intentional, and cleaned-up** side effects. Every side effect should be either part of the skill's purpose or properly cleaned up on exit.
