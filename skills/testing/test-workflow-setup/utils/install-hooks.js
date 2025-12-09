#!/usr/bin/env node

/**
 * Hook Installer
 *
 * Installs git hooks and Claude hooks for TDD enforcement
 */

const fs = require('fs');
const path = require('path');

class HookInstaller {
  constructor(projectRoot, skillRoot) {
    this.projectRoot = projectRoot;
    this.skillRoot = skillRoot;
    this.gitHooksDir = path.join(projectRoot, '.git', 'hooks');
    this.claudeHooksDir = path.join(projectRoot, '.claude', 'hooks');
    this.tddAutomationDir = path.join(projectRoot, '.tdd-automation');
  }

  /**
   * Install all TDD hooks
   * @returns {object} Installation result
   */
  installAll() {
    const results = {
      success: true,
      installed: [],
      failed: [],
      skipped: []
    };

    // Create directories
    this.ensureDirectories();

    // Copy TDD automation files
    this.copyTddAutomationFiles(results);

    // Install git pre-commit hook
    this.installGitPreCommit(results);

    // Install Claude hooks (if Claude hooks directory exists)
    if (fs.existsSync(path.dirname(this.claudeHooksDir))) {
      this.installClaudeHooks(results);
    }

    results.success = results.failed.length === 0;
    return results;
  }

  /**
   * Ensure required directories exist
   */
  ensureDirectories() {
    const dirs = [
      this.tddAutomationDir,
      path.join(this.tddAutomationDir, 'scripts'),
      path.join(this.tddAutomationDir, 'templates'),
      path.join(this.tddAutomationDir, 'hooks')
    ];

    for (const dir of dirs) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }

    // Create Claude hooks directory if .claude exists
    if (fs.existsSync(path.join(this.projectRoot, '.claude'))) {
      if (!fs.existsSync(this.claudeHooksDir)) {
        fs.mkdirSync(this.claudeHooksDir, { recursive: true });
      }
    }
  }

  /**
   * Copy TDD automation files to project
   * @param {object} results - Results object to update
   */
  copyTddAutomationFiles(results) {
    const scriptsDir = path.join(this.skillRoot, 'scripts');
    const templatesDir = path.join(this.skillRoot, 'templates');
    const targetScriptsDir = path.join(this.tddAutomationDir, 'scripts');
    const targetTemplatesDir = path.join(this.tddAutomationDir, 'templates');

    try {
      // Copy scripts
      if (fs.existsSync(scriptsDir)) {
        this.copyDirectory(scriptsDir, targetScriptsDir);
        results.installed.push('TDD automation scripts');
      }

      // Copy templates
      if (fs.existsSync(templatesDir)) {
        this.copyDirectory(templatesDir, targetTemplatesDir);
        results.installed.push('TDD templates');
      }
    } catch (error) {
      results.failed.push(`Copy TDD files: ${error.message}`);
    }
  }

  /**
   * Install git pre-commit hook
   * @param {object} results - Results object to update
   */
  installGitPreCommit(results) {
    if (!fs.existsSync(this.gitHooksDir)) {
      results.skipped.push('Git pre-commit hook (no .git directory)');
      return;
    }

    const hookPath = path.join(this.gitHooksDir, 'pre-commit');
    const templatePath = path.join(this.skillRoot, 'templates', 'pre-commit.sh');

    try {
      // Check if hook already exists
      if (fs.existsSync(hookPath)) {
        const existing = fs.readFileSync(hookPath, 'utf-8');

        // Check if our TDD hook is already installed
        if (existing.includes('TDD_AUTOMATION')) {
          results.skipped.push('Git pre-commit hook (already installed)');
          return;
        }

        // Backup existing hook
        const backupPath = hookPath + '.backup';
        fs.copyFileSync(hookPath, backupPath);
        results.installed.push(`Git pre-commit hook backup (${backupPath})`);

        // Append our hook to existing
        const tddHook = fs.readFileSync(templatePath, 'utf-8');
        fs.appendFileSync(hookPath, '\n\n' + tddHook);
        results.installed.push('Git pre-commit hook (appended)');
      } else {
        // Install new hook
        fs.copyFileSync(templatePath, hookPath);
        fs.chmodSync(hookPath, '755');
        results.installed.push('Git pre-commit hook (new)');
      }
    } catch (error) {
      results.failed.push(`Git pre-commit hook: ${error.message}`);
    }
  }

  /**
   * Install Claude hooks
   * @param {object} results - Results object to update
   */
  installClaudeHooks(results) {
    const hooksToInstall = [
      {
        name: 'tdd-auto-enforcer.sh',
        description: 'TDD auto-enforcer hook'
      }
    ];

    for (const hook of hooksToInstall) {
      const sourcePath = path.join(this.skillRoot, 'templates', hook.name);
      const targetPath = path.join(this.claudeHooksDir, hook.name);

      try {
        if (fs.existsSync(targetPath)) {
          results.skipped.push(`${hook.description} (already exists)`);
          continue;
        }

        if (!fs.existsSync(sourcePath)) {
          results.failed.push(`${hook.description} (template not found)`);
          continue;
        }

        fs.copyFileSync(sourcePath, targetPath);
        fs.chmodSync(targetPath, '755');
        results.installed.push(hook.description);
      } catch (error) {
        results.failed.push(`${hook.description}: ${error.message}`);
      }
    }
  }

  /**
   * Copy directory recursively
   * @param {string} src - Source directory
   * @param {string} dest - Destination directory
   */
  copyDirectory(src, dest) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
      const srcPath = path.join(src, entry.name);
      const destPath = path.join(dest, entry.name);

      if (entry.isDirectory()) {
        this.copyDirectory(srcPath, destPath);
      } else {
        fs.copyFileSync(srcPath, destPath);

        // Make scripts executable
        if (entry.name.endsWith('.sh') || entry.name.endsWith('.js')) {
          try {
            fs.chmodSync(destPath, '755');
          } catch (error) {
            // Ignore chmod errors on systems that don't support it
          }
        }
      }
    }
  }

  /**
   * Uninstall all TDD hooks
   * @returns {object} Uninstallation result
   */
  uninstallAll() {
    const results = {
      success: true,
      removed: [],
      failed: []
    };

    // Remove git pre-commit hook (only our section)
    this.uninstallGitPreCommit(results);

    // Remove Claude hooks
    this.uninstallClaudeHooks(results);

    // Remove TDD automation directory
    if (fs.existsSync(this.tddAutomationDir)) {
      try {
        fs.rmSync(this.tddAutomationDir, { recursive: true, force: true });
        results.removed.push('.tdd-automation directory');
      } catch (error) {
        results.failed.push(`.tdd-automation directory: ${error.message}`);
      }
    }

    results.success = results.failed.length === 0;
    return results;
  }

  /**
   * Uninstall git pre-commit hook
   * @param {object} results - Results object to update
   */
  uninstallGitPreCommit(results) {
    const hookPath = path.join(this.gitHooksDir, 'pre-commit');

    if (!fs.existsSync(hookPath)) {
      return;
    }

    try {
      const content = fs.readFileSync(hookPath, 'utf-8');

      // Check if our hook is installed
      if (!content.includes('TDD_AUTOMATION')) {
        return;
      }

      // If the entire file is our hook, remove it
      if (content.trim().startsWith('#!/bin/bash') && content.includes('TDD_AUTOMATION')) {
        // Check if there's a backup
        const backupPath = hookPath + '.backup';
        if (fs.existsSync(backupPath)) {
          fs.copyFileSync(backupPath, hookPath);
          results.removed.push('Git pre-commit hook (restored from backup)');
        } else {
          fs.unlinkSync(hookPath);
          results.removed.push('Git pre-commit hook (removed)');
        }
      }
    } catch (error) {
      results.failed.push(`Git pre-commit hook: ${error.message}`);
    }
  }

  /**
   * Uninstall Claude hooks
   * @param {object} results - Results object to update
   */
  uninstallClaudeHooks(results) {
    const hooksToRemove = ['tdd-auto-enforcer.sh'];

    for (const hookName of hooksToRemove) {
      const hookPath = path.join(this.claudeHooksDir, hookName);

      if (fs.existsSync(hookPath)) {
        try {
          fs.unlinkSync(hookPath);
          results.removed.push(`Claude hook: ${hookName}`);
        } catch (error) {
          results.failed.push(`Claude hook ${hookName}: ${error.message}`);
        }
      }
    }
  }
}

module.exports = HookInstaller;
