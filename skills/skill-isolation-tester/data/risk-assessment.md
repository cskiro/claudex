# Skill Risk Assessment Guide

## Overview

This guide helps you assess the risk level of a skill to determine the appropriate isolation environment for testing. Risk assessment prevents over-isolation (wasting time) and under-isolation (security issues).

## Risk Levels

### Low Risk → Git Worktree

**Characteristics:**
- Read-only operations on existing files
- No system commands (bash, npm, apt, etc.)
- No file creation outside skill directory
- No network requests
- Pure data processing or analysis
- File reading and reporting only

**Examples:**
- Code analyzer that reads files and generates reports
- Configuration validator that checks syntax
- Documentation generator from code comments
- Markdown formatter or linter
- Log file parser

**Appropriate Environment:** Git Worktree (fast, lightweight)

### Medium Risk → Docker

**Characteristics:**
- File creation in user directories
- NPM/pip package installation
- Bash commands for file operations
- Git operations (clone, commit, etc.)
- Network requests (API calls, downloads)
- Environment variable reads
- Temporary file creation
- Database connections (local)

**Examples:**
- Code generator that creates new files
- Package installer or dependency manager
- API integration that fetches remote data
- Build tool that compiles code
- Test runner that executes tests
- Migration tool that updates files

**Appropriate Environment:** Docker (OS isolation, reproducible)

### High Risk → VM

**Characteristics:**
- System configuration changes (/etc/ modifications)
- Service installation (systemd, cron)
- Kernel module loading
- VM or container operations
- Database schema migrations (production)
- Destructive operations (file deletion, disk formatting)
- Privilege escalation (sudo commands)
- Unknown or untrusted source

**Examples:**
- System setup automation
- Infrastructure provisioning
- VM management tools
- Security testing tools
- Experimental or unreviewed skills
- Skills from external repositories

**Appropriate Environment:** VM (complete isolation, safest)

## Assessment Checklist

### Step 1: Parse Skill Manifest (SKILL.md)

Read the skill's SKILL.md and look for these keywords:

**Low Risk Indicators:**
- "analyze", "read", "parse", "validate", "check", "lint", "format"
- "generate report", "calculate", "summarize"
- Read-only file operations
- No system commands mentioned

**Medium Risk Indicators:**
- "install", "create", "write", "modify", "update", "build", "compile"
- "npm install", "pip install", "git clone"
- "fetch", "download", "API call"
- File creation mentioned
- Bash commands for file operations

**High Risk Indicators:**
- "sudo", "systemctl", "cron", "service"
- "configure system", "modify /etc"
- "VM", "docker run", "container"
- "delete", "remove", "format"
- "root access", "privilege"

### Step 2: Scan Skill Code

If skill includes scripts or code files, scan for:

**Red Flags (High Risk):**
```bash
# In bash scripts
sudo
systemctl
/etc/
chmod 777
rm -rf /
dd if=
mkfs
usermod
passwd
```

```javascript
// In JavaScript/Node
require('child_process').exec('sudo')
fs.rmdirSync('/', { recursive: true })
process.setuid(0)
```

```python
# In Python
os.system('sudo')
import subprocess
subprocess.run(['sudo', ...])
```

**Medium Risk Patterns:**
```bash
npm install
git clone
curl | bash
apt-get install
brew install
pip install
mkdir -p
touch
echo > file
```

**Low Risk Patterns:**
```bash
cat file.txt
grep pattern
find . -name
ls -la
echo "message"
```

### Step 3: Check Dependencies

Review plugin.json or README for dependencies:

**Low Risk:**
- No external dependencies
- Pure JavaScript/Python/Ruby standard library
- Read-only CLI tools (cat, grep, jq for reading only)

**Medium Risk:**
- NPM packages listed
- Python packages (via requirements.txt)
- Common CLI tools (git, curl, wget)
- Database connections (read/write)

**High Risk:**
- System packages (apt, yum, brew)
- Kernel modules
- Root-level dependencies
- Unsigned binaries
- External scripts from unknown sources

### Step 4: Review File Operations

Check what directories the skill accesses:

**Low Risk:**
- Reads from current directory only
- Reads from specified input files
- Writes reports to current directory

**Medium Risk:**
- Reads/writes to ~/.claude/
- Reads/writes to /tmp/
- Creates files in user directories
- Modifies project files

**High Risk:**
- Accesses /etc/
- Accesses /usr/ or /usr/local/
- Accesses /sys/ or /proc/
- Modifies system binaries
- Accesses /var/log/

### Step 5: Network Activity Assessment

**Low Risk:**
- No network activity
- Reads from local cache only

**Medium Risk:**
- HTTP GET requests to public APIs
- Documented API endpoints
- Read-only data fetching
- HTTPS only

**High Risk:**
- HTTP POST with sensitive data
- Unclear network destinations
- Raw socket operations
- Arbitrary URL from user input
- Self-updating mechanism

## Automatic Risk Scoring

Use this scoring system:

```javascript
function assessSkillRisk(skill) {
  let score = 0;

  // File operations
  if (mentions(skill, "read", "parse", "analyze")) score += 1;
  if (mentions(skill, "write", "create", "modify")) score += 3;
  if (mentions(skill, "delete", "remove", "rm -rf")) score += 8;

  // System operations
  if (mentions(skill, "npm install", "pip install")) score += 3;
  if (mentions(skill, "apt-get", "brew install")) score += 5;
  if (mentions(skill, "sudo", "systemctl", "service")) score += 10;

  // File paths
  if (accesses(skill, "~/", "/tmp/")) score += 2;
  if (accesses(skill, "/etc/", "/usr/")) score += 8;

  // Network
  if (mentions(skill, "fetch", "API", "curl")) score += 2;
  if (mentions(skill, "download", "wget")) score += 3;

  // Process operations
  if (mentions(skill, "exec", "spawn", "child_process")) score += 4;

  // Determine risk level
  if (score <= 3) return "low";      // Worktree
  if (score <= 10) return "medium";  // Docker
  return "high";                     // VM
}
```

**Scoring Reference:**
- 0-3: Low Risk → Git Worktree
- 4-10: Medium Risk → Docker
- 11+: High Risk → VM

## Special Cases

### Unknown or Unreviewed Skills

**Default:** High Risk (VM isolation)

Even if skill appears low risk, use VM for first test of:
- Skills from external repositories
- Skills without documentation
- Skills with obfuscated code
- Skills from untrusted authors

### Skills in Active Development

**Recommendation:** Medium Risk (Docker)

For your own skills during development:
- Start with Git Worktree for speed
- Use Docker before committing
- Use VM before public release

### Skills from Marketplace

**Recommendation:** Follow listed risk level

Trusted marketplace skills can use their documented risk level.

## Override Cases

User can always override automatic detection:

```
test skill low-risk-skill in vm     # More isolation than needed (safe but slow)
test skill high-risk-skill in docker # Less isolation (not recommended)
```

**Warn user if choosing lower isolation than recommended.**

## Risk Re-assessment

Re-assess risk if skill is updated:
- Major version changes
- New dependencies added
- New file operations
- Expanded scope

## Decision Tree

```
Start
  |
  ├─ Does skill read files only?
  |    └─ YES → Low Risk (Worktree)
  |    └─ NO → Continue
  |
  ├─ Does skill install packages or modify files?
  |    └─ YES → Medium Risk (Docker)
  |    └─ NO → Continue
  |
  ├─ Does skill modify system configs or use sudo?
  |    └─ YES → High Risk (VM)
  |    └─ NO → Continue
  |
  └─ Is skill from untrusted source?
       └─ YES → High Risk (VM)
       └─ NO → Medium Risk (Docker)
```

## Example Assessments

### Example 1: "code-formatter"

**Description:** Formats JavaScript/TypeScript files using prettier

**Analysis:**
- Reads files: Yes (score: +1)
- Writes files: Yes (score: +3)
- System commands: No
- Dependencies: prettier (npm package) (score: +3)
- File paths: Current directory only

**Total Score:** 7
**Risk Level:** Medium → Docker

**Reasoning:** Modifies files but limited to project directory. Docker provides adequate isolation.

### Example 2: "log-analyzer"

**Description:** Parses log files and generates HTML report

**Analysis:**
- Reads files: Yes (score: +1)
- Writes files: Yes (HTML report) (score: +3)
- System commands: No
- Dependencies: None
- File paths: Current directory + /tmp for temp files (score: +2)

**Total Score:** 6
**Risk Level:** Medium → Docker

**Reasoning:** Safe operations but creates files. Docker ensures clean testing.

### Example 3: "system-auditor"

**Description:** Audits system security configuration

**Analysis:**
- Reads files: Yes, including /etc/ (score: +1 + 8)
- System commands: Runs systemctl, checks services (score: +10)
- Dependencies: System tools
- File paths: /etc/, /var/log/ (score: +8)

**Total Score:** 27
**Risk Level:** High → VM

**Reasoning:** Accesses sensitive system directories and uses system commands. VM required.

### Example 4: "markdown-linter"

**Description:** Checks markdown files for style violations

**Analysis:**
- Reads files: Yes (score: +1)
- Writes files: No (only stdout)
- System commands: No
- Dependencies: None
- File paths: Current directory only

**Total Score:** 1
**Risk Level:** Low → Git Worktree

**Reasoning:** Pure read-only analysis. Worktree is sufficient and fast.

---

**Remember:** When in doubt, choose higher isolation. It's better to be safe than to clean up a compromised system. Speed is secondary to security.
