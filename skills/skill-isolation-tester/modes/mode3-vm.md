# Mode 3: VM (Virtual Machine) Isolation

## When to Use

**Best for:**
- High-risk skills that modify system configurations
- Skills that require kernel modules or system services
- Testing skills that interact with VMs themselves
- Maximum isolation and security
- Skills from untrusted sources

**Not suitable for:**
- Quick iteration during development (too slow)
- Skills that are obviously safe and read-only
- Situations where speed is more important than isolation

**Risk Level**: Medium to high complexity skills

## Advantages

- 🔒 **Complete Isolation**: Separate kernel, OS, and all resources
- 🛡️ **Maximum Security**: Host system is completely protected
- 🖥️ **Real OS Environment**: Test on actual Linux/macOS distributions
- 📸 **Snapshots**: Easy rollback to clean state
- 🧪 **Destructive Testing**: Safe to test potentially dangerous operations

## Limitations

- 🐌 **Slow**: Minutes to provision, slower execution
- 💾 **Disk Space**: 10-20GB per VM
- 💰 **Resource Intensive**: Requires significant RAM and CPU
- 🔧 **Complex Setup**: More moving parts to configure
- ⏱️ **Longer Feedback Loop**: Not ideal for rapid iteration

## Prerequisites

1. Virtualization software installed:
   - **macOS**: UTM, Parallels, or VMware Fusion
   - **Linux**: QEMU/KVM, VirtualBox, or virt-manager
   - **Windows**: VirtualBox, Hyper-V, or VMware Workstation

2. Base VM image or ISO:
   - Ubuntu 22.04 LTS (recommended)
   - Debian 12
   - Fedora 39

3. System resources:
   - 8GB+ host RAM (allocate 2-4GB to VM)
   - 20GB+ disk space
   - CPU virtualization enabled (VT-x/AMD-V)

4. Command-line tools:
   - **macOS with UTM**: `utmctl` or use UI
   - **Linux**: `virsh` (libvirt) or `vboxmanage` (VirtualBox)
   - **Multipass**: `multipass` (cross-platform, recommended)

## Recommended: Use Multipass

Multipass is the easiest option for cross-platform VM management:

```bash
# Install Multipass
# macOS:
brew install multipass

# Linux:
sudo snap install multipass

# Windows:
# Download from https://multipass.run/
```

## Workflow

### Step 1: Validate Virtualization Environment

```bash
# Check virtualization is enabled (Linux)
grep -E 'vmx|svm' /proc/cpuinfo

# Check Multipass is installed
command -v multipass || { echo "Install Multipass"; exit 1; }

# Check available resources
multipass info || echo "First time setup needed"
```

### Step 2: Create Base VM

**Launch clean Ubuntu VM:**
```bash
VM_NAME="skill-test-$(date +%s)"

# Launch VM with Multipass
multipass launch \
  --name "$VM_NAME" \
  --cpus 2 \
  --memory 2G \
  --disk 10G \
  22.04

# Wait for VM to be ready
multipass exec "$VM_NAME" -- cloud-init status --wait
```

**Or use UTM (macOS GUI):**
1. Download Ubuntu 22.04 ARM64 ISO
2. Create new VM with 2GB RAM, 10GB disk
3. Install Ubuntu and setup user
4. Note VM name for scripts

**Or use virsh (Linux CLI):**
```bash
# Download cloud image
wget https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-amd64.img

# Create VM
virt-install \
  --name "$VM_NAME" \
  --memory 2048 \
  --vcpus 2 \
  --disk ubuntu-22.04-server-cloudimg-amd64.img \
  --import \
  --os-variant ubuntu22.04
```

### Step 3: Install Claude Code in VM

```bash
# Install system dependencies
multipass exec "$VM_NAME" -- sudo apt-get update
multipass exec "$VM_NAME" -- sudo apt-get install -y \
  curl \
  git \
  nodejs \
  npm

# Install Claude Code
multipass exec "$VM_NAME" -- npm install -g @anthropic/claude-code

# Verify installation
multipass exec "$VM_NAME" -- which claude
```

### Step 4: Copy Skill to VM

```bash
# Create directory structure
multipass exec "$VM_NAME" -- mkdir -p /home/ubuntu/.claude/skills

# Copy skill to VM
multipass transfer \
  ~/.claude/skills/[skill-name] \
  "$VM_NAME":/home/ubuntu/.claude/skills/

# Verify copy
multipass exec "$VM_NAME" -- ls -la /home/ubuntu/.claude/skills/[skill-name]
```

### Step 5: Take VM Snapshot

**With Multipass:**
```bash
# Multipass doesn't support snapshots directly
# Instead, we'll capture filesystem state
multipass exec "$VM_NAME" -- find /home/ubuntu -type f > /tmp/before-files.txt
multipass exec "$VM_NAME" -- dpkg -l > /tmp/before-packages.txt
multipass exec "$VM_NAME" -- ps aux > /tmp/before-processes.txt
```

**With UTM (macOS):**
```bash
# Take snapshot via UI or CLI if available
utmctl snapshot "$VM_NAME" --name "before-skill-test"
```

**With virsh (Linux):**
```bash
virsh snapshot-create-as "$VM_NAME" before-skill-test "Before skill test"
```

### Step 6: Execute Skill in VM

**Start Claude Code session in VM:**
```bash
# Interactive session
multipass shell "$VM_NAME"

# Then inside VM:
claude

# Run skill with trigger phrase
```

**Or execute non-interactively:**
```bash
# If skill has test command
multipass exec "$VM_NAME" -- \
  bash -c "claude skill run [skill-name] --test"
```

**Monitor from host:**
```bash
# Watch resource usage
multipass info "$VM_NAME" --format json | jq '.info[] | {memory_usage, cpu_usage}'

# Tail logs
multipass exec "$VM_NAME" -- tail -f /var/log/syslog
```

### Step 7: Take Post-Execution Snapshot

```bash
# Capture filesystem state
multipass exec "$VM_NAME" -- find /home/ubuntu -type f > /tmp/after-files.txt
multipass exec "$VM_NAME" -- dpkg -l > /tmp/after-packages.txt
multipass exec "$VM_NAME" -- ps aux > /tmp/after-processes.txt

# Compare
diff /tmp/before-files.txt /tmp/after-files.txt > /tmp/file-changes.txt
diff /tmp/before-packages.txt /tmp/after-packages.txt > /tmp/package-changes.txt
diff /tmp/before-processes.txt /tmp/after-processes.txt > /tmp/process-changes.txt
```

**Snapshot VM state:**
```bash
# virsh
virsh snapshot-create-as "$VM_NAME" after-skill-test "After skill test"

# UTM (macOS)
utmctl snapshot "$VM_NAME" --name "after-skill-test"
```

### Step 8: Analyze Results

**Extract execution logs:**
```bash
# Copy Claude Code logs from VM
multipass transfer \
  "$VM_NAME":/home/ubuntu/.claude/logs/ \
  /tmp/skill-test-logs/

# Analyze logs
grep -i "error\|warning\|fail" /tmp/skill-test-logs/*.log
```

**Check filesystem changes:**
```bash
echo "Files added: $(grep ">" /tmp/file-changes.txt | wc -l)"
echo "Files removed: $(grep "<" /tmp/file-changes.txt | wc -l)"

# Check for unexpected modifications
grep ">/etc/" /tmp/file-changes.txt  # System config changes
grep ">/usr/local/" /tmp/file-changes.txt  # Global installs
```

**Check package changes:**
```bash
# List newly installed packages
grep ">" /tmp/package-changes.txt

# Check for removed packages
grep "<" /tmp/package-changes.txt
```

**Check for orphaned processes:**
```bash
# Processes still running after skill completion
grep ">" /tmp/process-changes.txt | grep -v "ps\|grep\|ssh"
```

**System modifications:**
```bash
# Check for systemd services
multipass exec "$VM_NAME" -- systemctl list-units --type=service --state=running

# Check for cron jobs
multipass exec "$VM_NAME" -- crontab -l

# Check for environment modifications
multipass exec "$VM_NAME" -- cat /etc/environment
```

### Step 9: Generate Comprehensive Report

```markdown
# VM Isolation Test Report: [skill-name]

## Environment
**VM Platform**: Multipass / UTM / virsh
**OS**: Ubuntu 22.04 LTS
**VM Name**: $VM_NAME
**Resources**: 2 vCPU, 2GB RAM, 10GB disk

## Execution Results
**Status**: ✅ Completed successfully
**Duration**: 45 seconds
**Exit Code**: 0

## Filesystem Changes
**Files Added**: 12
- `/home/ubuntu/.claude/cache/skill-data.json` (15KB)
- `/tmp/skill-temp-*.log` (3 files, 45KB total)
- `/home/ubuntu/.cache/skill-assets/` (8 files, 120KB)

**Files Modified**: 2
- `/home/ubuntu/.claude/config.json` (updated skill registry)
- `/home/ubuntu/.bash_history` (normal)

**Files Deleted**: 0

## Package Changes
**Installed Packages**: 2
- `jq` (1.6-2.1ubuntu3)
- `tree` (2.0.2-1)

**Removed Packages**: 0

## System Modifications
✅ No systemd services added
✅ No cron jobs created
✅ No environment variables modified
⚠️  Found leftover temp files in /tmp

## Process Analysis
**Orphaned Processes**: 0
**Background Jobs**: 0
**Network Connections**: 0

## Security Assessment
✅ No unauthorized file access attempts
✅ No privilege escalation attempts
✅ No suspicious network activity
✅ All operations within user home directory

## Dependency Analysis
**System Packages Required**:
- `jq` (for JSON processing) - Not documented in README
- `tree` (for directory visualization) - Optional

**NPM Packages Required**: None beyond Claude Code

**Hardcoded Paths Detected**:
⚠️  `/home/ubuntu/.claude/cache` (line 67)
→  Should use `$HOME/.claude/cache` or `~/.claude/cache`

## Recommendations
1. **CRITICAL**: Document `jq` dependency in README.md
2. **HIGH**: Fix hardcoded path on line 67
3. **MEDIUM**: Clean up /tmp files before skill exits
4. **LOW**: Consider making `tree` dependency optional

## Overall Grade: B (READY with minor fixes)

**Portability**: 85/100
**Cleanliness**: 75/100
**Security**: 100/100
**Documentation**: 70/100

**Final Status**: ✅ **APPROVED** for public release after addressing CRITICAL and HIGH priority items
```

### Step 10: Cleanup or Preserve

**Ask user:**
```
Test complete. VM: $VM_NAME

Options:
1. Keep VM for manual inspection
   Command: multipass shell $VM_NAME

2. Stop VM (can restart later)
   Command: multipass stop $VM_NAME

3. Delete VM and snapshots (full cleanup)
   Command: multipass delete $VM_NAME && multipass purge

4. Rollback to "before" snapshot and retest
   (virsh/UTM only)

Your choice?
```

**Cleanup commands:**
```bash
# Option 2: Stop VM
multipass stop "$VM_NAME"

# Option 3: Full cleanup
multipass delete "$VM_NAME"
multipass purge

# Cleanup temp files
rm -rf /tmp/skill-test-logs
rm /tmp/before-*.txt /tmp/after-*.txt /tmp/*-changes.txt
```

## Interpreting Results

### ✅ **PASS** - Production Ready
- VM still bootable after test
- Skill completed successfully
- No unauthorized system modifications
- All dependencies documented
- No security issues detected
- Clean cleanup (no orphaned resources)

### ⚠️ **WARNING** - Needs Review
- Skill works but left system modifications
- Installed undocumented packages
- Modified system configs (needs user consent)
- Performance issues (high resource usage)

### ❌ **FAIL** - Not Safe
- VM corrupted or unbootable
- Skill crashed or hung indefinitely
- Unauthorized privilege escalation
- Malicious behavior detected
- Critical undocumented dependencies
- Data exfiltration attempts

## Common Issues

### Issue: "Multipass not found"
**Fix**:
```bash
# macOS
brew install multipass

# Linux
sudo snap install multipass
```

### Issue: "Virtualization not enabled"
**Cause**: VT-x/AMD-V disabled in BIOS
**Fix**: Enable virtualization in BIOS/UEFI settings

### Issue: "Failed to launch VM"
**Cause**: Insufficient resources
**Fix**:
```bash
# Reduce VM resources
multipass launch --cpus 1 --memory 1G --disk 5G
```

### Issue: "VM network not working"
**Cause**: Network bridge issues
**Fix**:
```bash
# Restart Multipass daemon
# macOS
sudo launchctl kickstart -k system/com.canonical.multipassd

# Linux
sudo systemctl restart snap.multipass.multipassd
```

### Issue: "Can't copy files to VM"
**Cause**: SSH/sftp issues
**Fix**:
```bash
# Mount host directory instead
multipass mount ~/.claude/skills "$VM_NAME":/mnt/skills
```

## Advanced Techniques

### Automated Testing Pipeline

```bash
#!/bin/bash
# test-skill-vm.sh

SKILL_NAME="$1"
VM_NAME="skill-test-$SKILL_NAME-$(date +%s)"

# Launch VM
multipass launch --name "$VM_NAME" 22.04

# Setup
multipass exec "$VM_NAME" -- bash -c "
  sudo apt-get update
  sudo apt-get install -y nodejs npm
  npm install -g @anthropic/claude-code
"

# Copy skill
multipass transfer ~/.claude/skills/$SKILL_NAME "$VM_NAME":/home/ubuntu/.claude/skills/

# Run test
multipass exec "$VM_NAME" -- claude skill test $SKILL_NAME

# Cleanup
multipass delete "$VM_NAME"
multipass purge
```

### Testing on Multiple OS Versions

```bash
# Test on Ubuntu 20.04, 22.04, and 24.04
for version in 20.04 22.04 24.04; do
  VM="skill-test-ubuntu-${version}"
  multipass launch --name "$VM" $version
  # ... run tests ...
  multipass delete "$VM"
done
```

### Network Isolation Testing

```bash
# Create VM without internet access (if supported by hypervisor)
# Then test if skill fails gracefully without network
```

## Best Practices

1. **Always take snapshots** before running skills
2. **Test on clean VMs** - don't reuse VMs between tests
3. **Monitor resource usage** - catch runaway processes
4. **Check system logs** (`/var/log/syslog`) for warnings
5. **Test rollback** - ensure VM can be restored
6. **Document all system dependencies** found
7. **Use minimal VM resources** to catch resource issues
8. **Archive test results** before destroying VMs

## Quick Command Reference

```bash
# Launch VM
multipass launch --name test-vm 22.04

# List VMs
multipass list

# Shell into VM
multipass shell test-vm

# Execute command in VM
multipass exec test-vm -- <command>

# Copy file to VM
multipass transfer local-file test-vm:/remote/path

# Copy file from VM
multipass transfer test-vm:/remote/path local-file

# Stop VM
multipass stop test-vm

# Start VM
multipass start test-vm

# Delete VM
multipass delete test-vm && multipass purge

# VM info
multipass info test-vm
```

---

**Remember:** VM isolation is the gold standard for testing high-risk skills. It's slower but provides complete security and accurate testing of system-level behaviors. Use for skills from untrusted sources or skills that modify system state.
