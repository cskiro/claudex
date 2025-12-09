-- Audit History Database Schema
-- SQLite schema for tracking audit results over time

-- ============================================================================
-- TABLES
-- ============================================================================

-- Audit execution history
CREATE TABLE IF NOT EXISTS audit_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT UNIQUE NOT NULL,           -- UUID for this run
    started_at DATETIME NOT NULL,
    completed_at DATETIME,
    status TEXT CHECK(status IN ('running', 'completed', 'failed', 'cancelled')),
    scope TEXT,                             -- Directory/files audited
    trigger TEXT,                           -- 'manual', 'pr', 'scheduled', 'ci'
    commit_sha TEXT,
    branch TEXT,
    total_files INTEGER,
    total_findings INTEGER,
    quality_score REAL,
    security_score REAL,
    config_hash TEXT,                       -- Hash of audit config used
    metadata JSON                           -- Additional run metadata
);

-- Individual findings from audits
CREATE TABLE IF NOT EXISTS audit_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL REFERENCES audit_runs(run_id),
    finding_hash TEXT NOT NULL,             -- Hash for deduplication
    rule_id TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('critical', 'high', 'medium', 'low', 'info')),
    category TEXT,                          -- 'security', 'quality', 'performance', etc.
    file_path TEXT NOT NULL,
    line_number INTEGER,
    column_number INTEGER,
    message TEXT NOT NULL,
    suggestion TEXT,
    effort_minutes INTEGER,                 -- Estimated fix time
    first_seen_run TEXT,                    -- Run ID when first detected
    status TEXT DEFAULT 'open' CHECK(status IN ('open', 'fixed', 'wontfix', 'false_positive')),
    resolved_at DATETIME,
    resolved_by TEXT,
    metadata JSON
);

-- Quantitative metrics over time
CREATE TABLE IF NOT EXISTS audit_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL REFERENCES audit_runs(run_id),
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    unit TEXT,                              -- 'percent', 'count', 'minutes', etc.
    threshold_warning REAL,
    threshold_critical REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Pre-computed trend data for dashboards
CREATE TABLE IF NOT EXISTS audit_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    metric_name TEXT NOT NULL,
    value REAL NOT NULL,
    delta_day REAL,                         -- Change from previous day
    delta_week REAL,                        -- Change from previous week
    UNIQUE(date, metric_name)
);

-- File-level audit tracking
CREATE TABLE IF NOT EXISTS audit_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL REFERENCES audit_runs(run_id),
    file_path TEXT NOT NULL,
    file_hash TEXT,                         -- Content hash for change detection
    last_modified DATETIME,
    loc INTEGER,                            -- Lines of code
    complexity_avg REAL,
    finding_count INTEGER DEFAULT 0,
    needs_reaudit BOOLEAN DEFAULT FALSE,
    UNIQUE(run_id, file_path)
);

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_findings_run ON audit_findings(run_id);
CREATE INDEX IF NOT EXISTS idx_findings_severity ON audit_findings(severity);
CREATE INDEX IF NOT EXISTS idx_findings_status ON audit_findings(status);
CREATE INDEX IF NOT EXISTS idx_findings_file ON audit_findings(file_path);
CREATE INDEX IF NOT EXISTS idx_findings_hash ON audit_findings(finding_hash);
CREATE INDEX IF NOT EXISTS idx_metrics_run ON audit_metrics(run_id);
CREATE INDEX IF NOT EXISTS idx_metrics_name ON audit_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_trends_date ON audit_trends(date);
CREATE INDEX IF NOT EXISTS idx_files_path ON audit_files(file_path);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- Current open findings (most recent status per finding_hash)
CREATE VIEW IF NOT EXISTS v_open_findings AS
SELECT
    f.*,
    r.branch,
    r.commit_sha
FROM audit_findings f
JOIN audit_runs r ON f.run_id = r.run_id
WHERE f.status = 'open'
  AND f.run_id = (
      SELECT run_id FROM audit_runs
      WHERE status = 'completed'
      ORDER BY completed_at DESC
      LIMIT 1
  );

-- Quality score trend (last 30 days)
CREATE VIEW IF NOT EXISTS v_score_trend AS
SELECT
    DATE(r.completed_at) as date,
    AVG(r.quality_score) as avg_quality,
    AVG(r.security_score) as avg_security,
    SUM(r.total_findings) as total_findings,
    COUNT(*) as audit_count
FROM audit_runs r
WHERE r.status = 'completed'
  AND r.completed_at >= DATE('now', '-30 days')
GROUP BY DATE(r.completed_at)
ORDER BY date DESC;

-- Files needing re-audit (changed since last audit or high finding count)
CREATE VIEW IF NOT EXISTS v_stale_files AS
SELECT DISTINCT
    af.file_path,
    af.last_modified,
    af.finding_count,
    af.complexity_avg,
    r.completed_at as last_audit
FROM audit_files af
JOIN audit_runs r ON af.run_id = r.run_id
WHERE af.needs_reaudit = TRUE
   OR af.finding_count > 5
   OR r.completed_at < DATE('now', '-7 days');

-- Finding resolution rate
CREATE VIEW IF NOT EXISTS v_resolution_stats AS
SELECT
    category,
    severity,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'fixed' THEN 1 ELSE 0 END) as fixed,
    SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open,
    ROUND(100.0 * SUM(CASE WHEN status = 'fixed' THEN 1 ELSE 0 END) / COUNT(*), 1) as fix_rate
FROM audit_findings
GROUP BY category, severity;

-- Technical debt summary
CREATE VIEW IF NOT EXISTS v_debt_summary AS
SELECT
    category,
    COUNT(*) as finding_count,
    SUM(effort_minutes) as total_effort_minutes,
    ROUND(SUM(effort_minutes) / 60.0, 1) as total_effort_hours,
    AVG(effort_minutes) as avg_effort_minutes
FROM audit_findings
WHERE status = 'open'
GROUP BY category
ORDER BY total_effort_minutes DESC;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Auto-update finding status when resolved
CREATE TRIGGER IF NOT EXISTS trg_finding_resolved
AFTER UPDATE ON audit_findings
WHEN NEW.status IN ('fixed', 'wontfix', 'false_positive') AND OLD.status = 'open'
BEGIN
    UPDATE audit_findings
    SET resolved_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id AND resolved_at IS NULL;
END;

-- Auto-mark file for re-audit when findings added
CREATE TRIGGER IF NOT EXISTS trg_file_needs_reaudit
AFTER INSERT ON audit_findings
BEGIN
    UPDATE audit_files
    SET needs_reaudit = TRUE,
        finding_count = finding_count + 1
    WHERE file_path = NEW.file_path
      AND run_id = NEW.run_id;
END;

-- ============================================================================
-- MAINTENANCE PROCEDURES
-- ============================================================================

-- Cleanup old runs (keep last 90 days)
-- Run periodically: DELETE FROM audit_runs WHERE completed_at < DATE('now', '-90 days');

-- Vacuum database (run after large deletions)
-- VACUUM;

-- Analyze tables for query optimization
-- ANALYZE;

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

/*
-- Get finding trend for last 7 days
SELECT
    DATE(r.completed_at) as date,
    f.severity,
    COUNT(*) as count
FROM audit_findings f
JOIN audit_runs r ON f.run_id = r.run_id
WHERE r.completed_at >= DATE('now', '-7 days')
GROUP BY DATE(r.completed_at), f.severity
ORDER BY date, f.severity;

-- Find recurring issues (same finding in multiple runs)
SELECT
    finding_hash,
    rule_id,
    file_path,
    COUNT(DISTINCT run_id) as occurrence_count
FROM audit_findings
GROUP BY finding_hash
HAVING occurrence_count > 3
ORDER BY occurrence_count DESC;

-- Calculate MTTR (Mean Time To Resolve) by severity
SELECT
    severity,
    AVG(JULIANDAY(resolved_at) - JULIANDAY(
        (SELECT MIN(r.completed_at) FROM audit_runs r WHERE r.run_id = audit_findings.first_seen_run)
    )) as avg_days_to_resolve
FROM audit_findings
WHERE status = 'fixed' AND resolved_at IS NOT NULL
GROUP BY severity;
*/
