#!/usr/bin/env node

/**
 * Package.json Updater
 *
 * Safely adds TDD-related npm scripts to package.json
 */

const fs = require('fs');
const path = require('path');

class PackageJsonUpdater {
  constructor(projectRoot) {
    this.projectRoot = projectRoot;
    this.packageJsonPath = path.join(projectRoot, 'package.json');
  }

  /**
   * Add TDD scripts to package.json
   * @param {string} testCommand - Base test command (e.g., 'vitest --run')
   * @returns {object} Update result
   */
  addTddScripts(testCommand = 'vitest --run') {
    if (!fs.existsSync(this.packageJsonPath)) {
      return {
        success: false,
        reason: 'package.json not found'
      };
    }

    try {
      // Create backup
      const backupPath = this.packageJsonPath + '.backup';
      fs.copyFileSync(this.packageJsonPath, backupPath);

      // Read and parse package.json
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf-8'));

      // Ensure scripts object exists
      if (!packageJson.scripts) {
        packageJson.scripts = {};
      }

      // Define TDD scripts
      const tddScripts = {
        'test:tdd': testCommand,
        'test:tdd:watch': testCommand.replace('--run', '').trim(),
        'test:red': `${testCommand} --reporter=verbose`,
        'test:green': `${testCommand} --reporter=verbose`,
        'validate:tdd': 'node .tdd-automation/scripts/validate-tdd.js',
        'generate:test': 'node .tdd-automation/scripts/generate-test.js'
      };

      // Track what was added
      const added = [];
      const skipped = [];

      // Add scripts that don't exist
      for (const [key, value] of Object.entries(tddScripts)) {
        if (!packageJson.scripts[key]) {
          packageJson.scripts[key] = value;
          added.push(key);
        } else {
          skipped.push(key);
        }
      }

      // Write updated package.json with pretty formatting
      fs.writeFileSync(
        this.packageJsonPath,
        JSON.stringify(packageJson, null, 2) + '\n',
        'utf-8'
      );

      return {
        success: true,
        added,
        skipped,
        backup: backupPath
      };

    } catch (error) {
      return {
        success: false,
        reason: error.message
      };
    }
  }

  /**
   * Remove TDD scripts from package.json
   * @returns {object} Removal result
   */
  removeTddScripts() {
    if (!fs.existsSync(this.packageJsonPath)) {
      return {
        success: false,
        reason: 'package.json not found'
      };
    }

    try {
      // Create backup
      const backupPath = this.packageJsonPath + '.backup';
      fs.copyFileSync(this.packageJsonPath, backupPath);

      // Read and parse package.json
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf-8'));

      if (!packageJson.scripts) {
        return {
          success: true,
          removed: [],
          backup: backupPath
        };
      }

      // Define TDD script keys to remove
      const tddScriptKeys = [
        'test:tdd',
        'test:tdd:watch',
        'test:red',
        'test:green',
        'validate:tdd',
        'generate:test'
      ];

      // Track what was removed
      const removed = [];

      // Remove TDD scripts
      for (const key of tddScriptKeys) {
        if (packageJson.scripts[key]) {
          delete packageJson.scripts[key];
          removed.push(key);
        }
      }

      // Write updated package.json
      fs.writeFileSync(
        this.packageJsonPath,
        JSON.stringify(packageJson, null, 2) + '\n',
        'utf-8'
      );

      return {
        success: true,
        removed,
        backup: backupPath
      };

    } catch (error) {
      return {
        success: false,
        reason: error.message
      };
    }
  }

  /**
   * Check if TDD scripts are already installed
   * @returns {boolean} True if TDD scripts exist
   */
  hasTddScripts() {
    if (!fs.existsSync(this.packageJsonPath)) {
      return false;
    }

    try {
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf-8'));

      if (!packageJson.scripts) {
        return false;
      }

      // Check if any TDD scripts exist
      const tddScriptKeys = ['test:tdd', 'validate:tdd', 'generate:test'];
      return tddScriptKeys.some(key => packageJson.scripts[key]);

    } catch (error) {
      return false;
    }
  }
}

module.exports = PackageJsonUpdater;
