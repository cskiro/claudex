#!/usr/bin/env node

/**
 * CLAUDE.md Validator
 *
 * Validates and manages CLAUDE.md files with backup and rollback capabilities.
 * Ensures safe installation of TDD automation without data loss.
 */

const fs = require('fs');
const path = require('path');

class ClaudeMdValidator {
  constructor(projectRoot) {
    this.projectRoot = projectRoot;
    this.claudeDir = path.join(projectRoot, '.claude');
    this.claudeMdPath = path.join(this.claudeDir, 'CLAUDE.md');
  }

  /**
   * Validate current CLAUDE.md state and determine installation strategy
   * @returns {object} Validation result with strategy recommendation
   */
  validate() {
    const result = {
      exists: false,
      hasExistingContent: false,
      hasTddSection: false,
      needsBackup: false,
      strategy: 'create', // create | merge | skip | abort
      warnings: [],
      size: 0,
      path: this.claudeMdPath
    };

    // Check if CLAUDE.md exists
    if (!fs.existsSync(this.claudeMdPath)) {
      result.strategy = 'create';
      result.warnings.push('No CLAUDE.md found - will create new file');
      return result;
    }

    result.exists = true;
    const content = fs.readFileSync(this.claudeMdPath, 'utf-8');
    result.size = content.length;

    // Check if file has meaningful content (not just empty or whitespace)
    if (content.trim().length > 0) {
      result.hasExistingContent = true;
      result.needsBackup = true;
    }

    // Check if TDD automation is already installed
    if (this.detectTddSection(content)) {
      result.hasTddSection = true;
      result.strategy = 'skip';
      result.warnings.push('TDD automation already installed in CLAUDE.md');
      return result;
    }

    // Determine merge strategy
    if (result.hasExistingContent) {
      result.strategy = 'merge';
      result.warnings.push(`Existing CLAUDE.md found (${result.size} bytes) - will merge`);
    } else {
      result.strategy = 'create';
      result.warnings.push('Empty CLAUDE.md found - will replace');
    }

    return result;
  }

  /**
   * Detect if TDD automation section exists in content
   * @param {string} content - CLAUDE.md content to check
   * @returns {boolean} True if TDD section detected
   */
  detectTddSection(content) {
    const markers = [
      '<!-- TDD_AUTOMATION_START -->',
      'TDD Red-Green-Refactor Automation (Auto-Installed)',
      'tdd-automation-version:'
    ];

    return markers.some(marker => content.includes(marker));
  }

  /**
   * Create timestamped backup of current CLAUDE.md
   * @returns {object} Backup result with success status and path
   */
  createBackup() {
    if (!fs.existsSync(this.claudeMdPath)) {
      return {
        success: false,
        reason: 'No file to backup',
        path: null
      };
    }

    // Ensure .claude directory exists
    if (!fs.existsSync(this.claudeDir)) {
      fs.mkdirSync(this.claudeDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(
      this.claudeDir,
      `CLAUDE.md.backup.${timestamp}`
    );

    try {
      fs.copyFileSync(this.claudeMdPath, backupPath);
      const originalSize = fs.statSync(this.claudeMdPath).size;

      return {
        success: true,
        path: backupPath,
        originalSize,
        timestamp
      };
    } catch (error) {
      return {
        success: false,
        reason: error.message,
        path: null
      };
    }
  }

  /**
   * List all backup files sorted by date (newest first)
   * @returns {array} Array of backup file info objects
   */
  listBackups() {
    if (!fs.existsSync(this.claudeDir)) {
      return [];
    }

    try {
      return fs.readdirSync(this.claudeDir)
        .filter(f => f.startsWith('CLAUDE.md.backup'))
        .map(f => ({
          name: f,
          path: path.join(this.claudeDir, f),
          created: fs.statSync(path.join(this.claudeDir, f)).mtime,
          size: fs.statSync(path.join(this.claudeDir, f)).size
        }))
        .sort((a, b) => b.created - a.created);
    } catch (error) {
      console.error('Error listing backups:', error.message);
      return [];
    }
  }

  /**
   * Restore CLAUDE.md from backup file
   * @param {string} backupPath - Path to backup file
   * @returns {object} Rollback result with success status
   */
  rollback(backupPath) {
    if (!fs.existsSync(backupPath)) {
      return {
        success: false,
        reason: 'Backup file not found',
        path: backupPath
      };
    }

    try {
      // Ensure .claude directory exists
      if (!fs.existsSync(this.claudeDir)) {
        fs.mkdirSync(this.claudeDir, { recursive: true });
      }

      fs.copyFileSync(backupPath, this.claudeMdPath);

      return {
        success: true,
        restoredFrom: backupPath,
        size: fs.statSync(this.claudeMdPath).size
      };
    } catch (error) {
      return {
        success: false,
        reason: error.message,
        path: backupPath
      };
    }
  }

  /**
   * Remove TDD section from CLAUDE.md
   * @returns {object} Removal result with success status
   */
  removeTddSection() {
    if (!fs.existsSync(this.claudeMdPath)) {
      return {
        success: false,
        reason: 'CLAUDE.md not found'
      };
    }

    const content = fs.readFileSync(this.claudeMdPath, 'utf-8');

    // Check if TDD section exists
    if (!this.detectTddSection(content)) {
      return {
        success: false,
        reason: 'No TDD section found in CLAUDE.md'
      };
    }

    // Create backup before removal
    const backup = this.createBackup();
    if (!backup.success) {
      return {
        success: false,
        reason: `Backup failed: ${backup.reason}`
      };
    }

    // Remove TDD section using markers
    const startMarker = '<!-- TDD_AUTOMATION_START -->';
    const endMarker = '<!-- TDD_AUTOMATION_END -->';

    const startIdx = content.indexOf(startMarker);
    const endIdx = content.indexOf(endMarker);

    if (startIdx === -1 || endIdx === -1) {
      return {
        success: false,
        reason: 'Could not find section markers for clean removal'
      };
    }

    // Remove section and clean up extra whitespace
    const beforeSection = content.substring(0, startIdx).trimEnd();
    const afterSection = content.substring(endIdx + endMarker.length).trimStart();

    const cleanedContent = beforeSection + (afterSection ? '\n\n' + afterSection : '');

    try {
      fs.writeFileSync(this.claudeMdPath, cleanedContent, 'utf-8');

      const originalSize = content.length;
      const newSize = cleanedContent.length;

      return {
        success: true,
        backup: backup.path,
        originalSize,
        newSize,
        removed: originalSize - newSize
      };
    } catch (error) {
      // Rollback on error
      this.rollback(backup.path);
      return {
        success: false,
        reason: `Write failed: ${error.message}`
      };
    }
  }
}

module.exports = ClaudeMdValidator;
