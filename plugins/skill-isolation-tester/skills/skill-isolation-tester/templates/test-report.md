# Skill Isolation Test Report: {{skill_name}}

**Generated**: {{timestamp}}
**Tester**: {{tester_name}}
**Environment**: {{environment}} ({{mode}})
**Duration**: {{duration}}

---

## Executive Summary

**Overall Status**: {{status}}
**Grade**: {{grade}}
**Ready for Release**: {{ready_for_release}}

### Quick Stats
- Execution Status: {{execution_status}}
- Side Effects: {{side_effects_count}} detected
- Dependencies: {{dependencies_count}} found
- Issues: {{issues_high}} HIGH, {{issues_medium}} MEDIUM, {{issues_low}} LOW

---

## Test Environment

**Isolation Mode**: {{mode}}
**Platform**: {{platform}}
**OS**: {{os_version}}
**Resources**: {{resources}}

{{#if mode_specific_details}}
### Mode-Specific Details
{{mode_specific_details}}
{{/if}}

---

## Execution Results

### Status
{{execution_status_icon}} **{{execution_status}}**

### Details
- **Start Time**: {{start_time}}
- **End Time**: {{end_time}}
- **Duration**: {{duration}}
- **Exit Code**: {{exit_code}}

### Output
```
{{skill_output}}
```

{{#if execution_errors}}
### Errors
```
{{execution_errors}}
```
{{/if}}

### Resource Usage
- **Peak CPU**: {{peak_cpu}}%
- **Peak Memory**: {{peak_memory}}
- **Disk I/O**: {{disk_io}}
- **Network**: {{network_usage}}

---

## Side Effects Analysis

### Filesystem Changes

#### Files Created: {{files_created_count}}
{{#each files_created}}
- `{{path}}` ({{size}}){{#if temporary}} - TEMPORARY{{/if}}{{#if cleanup_failed}} ⚠️ Not cleaned up{{/if}}
{{/each}}

{{#if files_created_count_zero}}
✅ No files created
{{/if}}

#### Files Modified: {{files_modified_count}}
{{#each files_modified}}
- `{{path}}`{{#if expected}} - Expected{{else}} ⚠️ Unexpected{{/if}}
{{/each}}

{{#if files_modified_count_zero}}
✅ No files modified
{{/if}}

#### Files Deleted: {{files_deleted_count}}
{{#each files_deleted}}
- `{{path}}`{{#if expected}} - Expected{{else}} ⚠️ Unexpected{{/if}}
{{/each}}

{{#if files_deleted_count_zero}}
✅ No files deleted
{{/if}}

### Process Management

#### Processes Created: {{processes_created_count}}
{{#each processes}}
- PID {{pid}}: `{{command}}`{{#if still_running}} ⚠️ Still running{{/if}}
{{/each}}

{{#if orphaned_processes}}
⚠️ **Orphaned Processes**: {{orphaned_processes_count}}
{{#each orphaned_processes}}
- PID {{pid}}: `{{command}}` ({{runtime}} running)
{{/each}}
{{/if}}

{{#if no_process_issues}}
✅ All processes completed successfully
{{/if}}

### System Configuration

#### Environment Variables
{{#if env_vars_changed}}
{{#each env_vars_changed}}
- `{{name}}`: {{before}} → {{after}}
{{/each}}
{{else}}
✅ No environment variable changes
{{/if}}

#### Services & Daemons
{{#if services_started}}
{{#each services_started}}
- `{{name}}` ({{status}}){{#if undocumented}} ⚠️ Undocumented{{/if}}
{{/each}}
{{else}}
✅ No services started
{{/if}}

#### Package Installations
{{#if packages_installed}}
{{#each packages_installed}}
- `{{name}}` ({{version}}){{#if undocumented}} ⚠️ Not documented{{/if}}
{{/each}}
{{else}}
✅ No packages installed
{{/if}}

### Network Activity

{{#if network_connections}}
**Connections**: {{network_connections_count}}
{{#each network_connections}}
- {{protocol}} to `{{destination}}:{{port}}`{{#if secure}} (HTTPS){{else}} ⚠️ (HTTP){{/if}}
{{/each}}

**Data Transmitted**: {{data_transmitted}}
{{else}}
✅ No network activity detected
{{/if}}

### Database Changes

{{#if database_changes}}
{{#each database_changes}}
- {{type}}: {{description}}
{{/each}}
{{else}}
✅ No database changes
{{/if}}

---

## Dependency Analysis

### System Packages Required
{{#if system_packages}}
{{#each system_packages}}
{{#if documented}}✅{{else}}⚠️{{/if}} `{{name}}`{{#if version}} ({{version}}){{/if}}{{#unless documented}} - **Not documented in README**{{/unless}}
{{/each}}
{{else}}
✅ No system package dependencies
{{/if}}

### Language Packages (npm/pip/gem)
{{#if language_packages}}
{{#each language_packages}}
{{#if documented}}✅{{else}}⚠️{{/if}} `{{name}}@{{version}}`{{#unless documented}} - **Not documented**{{/unless}}
{{/each}}
{{else}}
✅ No language package dependencies
{{/if}}

### Runtime Requirements
{{#if runtime_requirements}}
{{#each runtime_requirements}}
- {{name}}: {{requirement}}{{#if met}}✅{{else}}❌{{/if}}
{{/each}}
{{else}}
✅ No special runtime requirements
{{/if}}

---

## Code Quality Issues

### Hardcoded Paths Detected
{{#if hardcoded_paths}}
{{#each hardcoded_paths}}
⚠️ `{{path}}` in {{file}}:{{line}}
   → **Recommendation**: Use `$HOME` or relative path
{{/each}}
{{else}}
✅ No hardcoded paths detected
{{/if}}

### Security Concerns
{{#if security_issues}}
{{#each security_issues}}
{{severity_icon}} **{{severity}}**: {{description}}
   Location: {{file}}:{{line}}
   Recommendation: {{recommendation}}
{{/each}}
{{else}}
✅ No security issues detected
{{/if}}

### Performance Issues
{{#if performance_issues}}
{{#each performance_issues}}
⚠️ {{description}}
{{/each}}
{{else}}
✅ No performance issues detected
{{/if}}

---

## Portability Assessment

### Cross-Platform Compatibility
- **Linux**: {{linux_compatible}}
- **macOS**: {{macos_compatible}}
- **Windows**: {{windows_compatible}}

### Environment Dependencies
{{#if env_dependencies}}
{{#each env_dependencies}}
- {{name}}: {{status}}
{{/each}}
{{else}}
✅ No environment-specific dependencies
{{/if}}

### User-Specific Assumptions
{{#if user_assumptions}}
{{#each user_assumptions}}
⚠️ {{description}}
{{/each}}
{{else}}
✅ No user-specific assumptions
{{/if}}

---

## Issues Summary

### 🔴 HIGH Priority ({{issues_high_count}})
{{#each issues_high}}
{{index}}. **{{title}}**
   - Impact: {{impact}}
   - Location: {{location}}
   - Fix: {{fix_recommendation}}
{{/each}}

{{#if no_high_issues}}
✅ No HIGH priority issues
{{/if}}

### 🟡 MEDIUM Priority ({{issues_medium_count}})
{{#each issues_medium}}
{{index}}. **{{title}}**
   - Impact: {{impact}}
   - Location: {{location}}
   - Fix: {{fix_recommendation}}
{{/each}}

{{#if no_medium_issues}}
✅ No MEDIUM priority issues
{{/if}}

### 🟢 LOW Priority ({{issues_low_count}})
{{#each issues_low}}
{{index}}. **{{title}}**
   - Impact: {{impact}}
   - Fix: {{fix_recommendation}}
{{/each}}

{{#if no_low_issues}}
✅ No LOW priority issues
{{/if}}

---

## Recommendations

### Required Before Release
{{#each required_fixes}}
{{index}}. {{recommendation}}
{{/each}}

{{#if no_required_fixes}}
✅ No required fixes
{{/if}}

### Suggested Improvements
{{#each suggested_improvements}}
{{index}}. {{recommendation}}
{{/each}}

### Documentation Updates Needed
{{#each documentation_updates}}
- {{item}}
{{/each}}

---

## Scoring Breakdown

| Category | Score | Weight | Weighted Score |
|----------|-------|--------|----------------|
| **Execution** | {{execution_score}}/100 | 25% | {{execution_weighted}} |
| **Cleanliness** | {{cleanliness_score}}/100 | 25% | {{cleanliness_weighted}} |
| **Security** | {{security_score}}/100 | 30% | {{security_weighted}} |
| **Portability** | {{portability_score}}/100 | 10% | {{portability_weighted}} |
| **Documentation** | {{documentation_score}}/100 | 10% | {{documentation_weighted}} |
| **TOTAL** | | | **{{total_score}}/100** |

### Grade: {{grade}}

**Grading Scale:**
- A (90-100): Production ready
- B (80-89): Ready with minor fixes
- C (70-79): Significant improvements needed
- D (60-69): Major issues, not recommended
- F (0-59): Not safe to use

---

## Test Artifacts

### Snapshots
- Before: `{{snapshot_before_path}}`
- After: `{{snapshot_after_path}}`

### Logs
- Execution log: `{{execution_log_path}}`
- Side effects log: `{{side_effects_log_path}}`

### Isolation Environment
{{#if environment_preserved}}
✅ **Preserved for debugging**

Access instructions:
```bash
{{access_command}}
```
{{else}}
🗑️ **Cleaned up**
{{/if}}

---

## Final Verdict

### Status: {{final_status}}

{{#if approved}}
✅ **APPROVED for public release**

This skill has passed isolation testing with acceptable results. Address HIGH priority issues before release, and consider MEDIUM/LOW priority improvements in future versions.
{{/if}}

{{#if approved_with_fixes}}
⚠️ **APPROVED with required fixes**

This skill will be ready for public release after addressing the {{issues_high_count}} HIGH priority issue(s) listed above. Retest after fixes.
{{/if}}

{{#if not_approved}}
❌ **NOT APPROVED**

This skill has critical issues that must be addressed before public release. Major refactoring or fixes required. Retest after addressing all HIGH priority issues and reviewing MEDIUM priority items.
{{/if}}

### Next Steps

{{#each next_steps}}
{{index}}. {{step}}
{{/each}}

---

**Test Completed**: {{completion_time}}
**Report Version**: 1.0
**Tester**: {{tester_name}}

---

*This report was generated by skill-isolation-tester*
