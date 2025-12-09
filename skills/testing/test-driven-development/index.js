#!/usr/bin/env node

/**
 * TDD Red-Green-Refactor Automation Skill
 *
 * Main orchestrator that installs TDD automation infrastructure in a project.
 * Configures CLAUDE.md, git hooks, npm scripts, and helper utilities to enforce
 * TDD workflow automatically for LLM-assisted development.
 *
 * @author Pattern Suggestion Pipeline
 * @version 0.2.0
 */

const fs = require('fs');
const path = require('path');

// Import utilities
const ClaudeMdValidator = require('./utils/validate-claude-md');
const ClaudeMdMerger = require('./utils/merge-claude-md');
const ProjectDetector = require('./utils/detect-project-type');
const PackageJsonUpdater = require('./utils/update-package-json');
const HookInstaller = require('./utils/install-hooks');

class TddAutomationSkill {
  constructor() {
    this.projectRoot = process.cwd();
    this.skillRoot = __dirname;
    this.version = '0.2.0';
  }

  /**
   * Main installation workflow
   */
  async install() {
    console.log('╔════════════════════════════════════════════════════════════════╗');
    console.log('║  TDD Red-Green-Refactor Automation                             ║');
    console.log('║  Version 0.2.0                                                 ║');
    console.log('╚════════════════════════════════════════════════════════════════╝\n');

    const results = {
      success: false,
      steps: [],
      errors: [],
      warnings: []
    };

    try {
      // Step 1: Detect project type
      console.log('🔍 Step 1: Detecting project configuration...\n');
      const projectInfo = await this.detectProject(results);

      // Step 2: Validate and backup CLAUDE.md
      console.log('\n🔍 Step 2: Validating CLAUDE.md...\n');
      const validation = await this.validateClaudeMd(results);

      if (validation.strategy === 'skip') {
        console.log('✅ TDD automation already installed');
        console.log('   No changes needed.\n');
        return results;
      }

      // Step 3: Install/merge CLAUDE.md configuration
      console.log('\n📝 Step 3: Configuring CLAUDE.md...\n');
      await this.configureClaudeMd(validation, results);

      // Step 4: Update package.json with TDD scripts
      console.log('\n📦 Step 4: Adding npm scripts...\n');
      await this.updatePackageJson(projectInfo, results);

      // Step 5: Install hooks
      console.log('\n🪝 Step 5: Installing hooks...\n');
      await this.installHooks(results);

      // Step 6: Verify installation
      console.log('\n✅ Step 6: Verifying installation...\n');
      await this.verifyInstallation(results);

      // Success summary
      results.success = results.errors.length === 0;
      this.printSummary(results, projectInfo);

    } catch (error) {
      console.error('\n❌ Installation failed:', error.message);
      console.error('\n   Stack trace:', error.stack);
      results.errors.push(error.message);
      results.success = false;
    }

    return results;
  }

  /**
   * Detect project type and configuration
   */
  async detectProject(results) {
    const detector = new ProjectDetector(this.projectRoot);
    const projectInfo = detector.detect();

    console.log(`   Project: ${projectInfo.projectName}`);
    console.log(`   Type: ${projectInfo.type}`);

    if (projectInfo.testFramework !== 'unknown') {
      console.log(`   Test Framework: ${projectInfo.testFramework}`);
    }

    if (projectInfo.hasTypeScript) {
      console.log('   Language: TypeScript');
    }

    if (projectInfo.hasGit) {
      console.log('   ✓ Git repository detected');
    } else {
      results.warnings.push('No git repository - git hooks will not be installed');
    }

    if (projectInfo.recommendations.length > 0) {
      console.log('\n   Recommendations:');
      projectInfo.recommendations.forEach(rec => {
        console.log(`   • ${rec}`);
        results.warnings.push(rec);
      });
    }

    results.steps.push('Project detection completed');
    return projectInfo;
  }

  /**
   * Validate CLAUDE.md state
   */
  async validateClaudeMd(results) {
    const validator = new ClaudeMdValidator(this.projectRoot);
    const validation = validator.validate();

    console.log(`   Location: ${validation.path}`);
    console.log(`   Exists: ${validation.exists ? 'Yes' : 'No'}`);

    if (validation.exists) {
      console.log(`   Size: ${this.formatBytes(validation.size)}`);
      console.log(`   Has Content: ${validation.hasExistingContent ? 'Yes' : 'No'}`);
    }

    console.log(`   Strategy: ${validation.strategy.toUpperCase()}`);

    if (validation.warnings.length > 0) {
      console.log('\n   Notes:');
      validation.warnings.forEach(warning => {
        console.log(`   • ${warning}`);
      });
    }

    results.steps.push(`CLAUDE.md validation: ${validation.strategy}`);
    return validation;
  }

  /**
   * Configure CLAUDE.md with TDD automation
   */
  async configureClaudeMd(validation, results) {
    const validator = new ClaudeMdValidator(this.projectRoot);

    if (validation.strategy === 'merge') {
      // Existing content - merge safely
      console.log('   Creating backup...');
      const backup = validator.createBackup();

      if (backup.success) {
        console.log(`   ✓ Backup created: ${path.basename(backup.path)}`);
        results.steps.push(`Backup created: ${backup.path}`);
      } else {
        throw new Error(`Backup failed: ${backup.reason}`);
      }

      // Read existing content
      const existingContent = fs.readFileSync(validator.claudeMdPath, 'utf-8');

      // Merge with TDD section
      console.log('   Merging TDD configuration...');
      const merger = new ClaudeMdMerger(existingContent);
      const mergedContent = merger.merge();

      // Write merged content
      fs.writeFileSync(validator.claudeMdPath, mergedContent, 'utf-8');

      const newSize = mergedContent.length;
      const added = newSize - validation.size;

      console.log(`   ✓ CLAUDE.md updated`);
      console.log(`     Original: ${this.formatBytes(validation.size)}`);
      console.log(`     New: ${this.formatBytes(newSize)} (+${this.formatBytes(added)})`);

      results.steps.push('CLAUDE.md merged with TDD configuration');

    } else {
      // No existing content or empty - create new
      console.log('   Creating new CLAUDE.md with TDD configuration...');

      const claudeDir = path.join(this.projectRoot, '.claude');
      if (!fs.existsSync(claudeDir)) {
        fs.mkdirSync(claudeDir, { recursive: true });
      }

      const content = ClaudeMdMerger.createNew();
      fs.writeFileSync(validator.claudeMdPath, content, 'utf-8');

      console.log(`   ✓ CLAUDE.md created`);
      console.log(`     Size: ${this.formatBytes(content.length)}`);

      results.steps.push('CLAUDE.md created with TDD configuration');
    }
  }

  /**
   * Update package.json with TDD scripts
   */
  async updatePackageJson(projectInfo, results) {
    if (!projectInfo.hasPackageJson) {
      console.log('   ⚠️  No package.json found - skipping npm scripts');
      results.warnings.push('No package.json - npm scripts not added');
      return;
    }

    const updater = new PackageJsonUpdater(this.projectRoot);

    // Check if already installed
    if (updater.hasTddScripts()) {
      console.log('   ✓ TDD scripts already installed');
      results.steps.push('TDD npm scripts already present');
      return;
    }

    // Determine test command based on project
    const testCommand = projectInfo.testFramework === 'vitest'
      ? 'vitest --run'
      : projectInfo.testFramework === 'jest'
      ? 'jest'
      : 'npm test';

    const result = updater.addTddScripts(testCommand);

    if (result.success) {
      console.log('   ✓ Added TDD scripts to package.json');

      if (result.added.length > 0) {
        console.log('\n   Scripts added:');
        result.added.forEach(script => {
          console.log(`   • ${script}`);
        });
      }

      if (result.skipped.length > 0) {
        console.log('\n   Scripts skipped (already exist):');
        result.skipped.forEach(script => {
          console.log(`   • ${script}`);
        });
      }

      results.steps.push(`Added ${result.added.length} npm scripts`);
    } else {
      results.warnings.push(`Failed to update package.json: ${result.reason}`);
    }
  }

  /**
   * Install git and Claude hooks
   */
  async installHooks(results) {
    const installer = new HookInstaller(this.projectRoot, this.skillRoot);
    const result = installer.installAll();

    if (result.installed.length > 0) {
      console.log('   Installed:');
      result.installed.forEach(item => {
        console.log(`   ✓ ${item}`);
      });
    }

    if (result.skipped.length > 0) {
      console.log('\n   Skipped:');
      result.skipped.forEach(item => {
        console.log(`   • ${item}`);
      });
    }

    if (result.failed.length > 0) {
      console.log('\n   Failed:');
      result.failed.forEach(item => {
        console.log(`   ✗ ${item}`);
        results.warnings.push(`Hook installation failed: ${item}`);
      });
    }

    results.steps.push(`Installed ${result.installed.length} hooks`);
  }

  /**
   * Verify installation was successful
   */
  async verifyInstallation(results) {
    const checks = [];

    // Check CLAUDE.md
    const claudeMdPath = path.join(this.projectRoot, '.claude', 'CLAUDE.md');
    if (fs.existsSync(claudeMdPath)) {
      const content = fs.readFileSync(claudeMdPath, 'utf-8');
      if (content.includes('TDD_AUTOMATION')) {
        checks.push('✓ CLAUDE.md configured');
      } else {
        checks.push('✗ CLAUDE.md missing TDD configuration');
      }
    } else {
      checks.push('✗ CLAUDE.md not found');
    }

    // Check .tdd-automation directory
    const tddDir = path.join(this.projectRoot, '.tdd-automation');
    if (fs.existsSync(tddDir)) {
      checks.push('✓ .tdd-automation directory created');
    }

    // Check package.json scripts
    const packageJsonPath = path.join(this.projectRoot, 'package.json');
    if (fs.existsSync(packageJsonPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
      if (packageJson.scripts && packageJson.scripts['test:tdd']) {
        checks.push('✓ npm scripts added');
      }
    }

    checks.forEach(check => console.log(`   ${check}`));
    results.steps.push('Installation verified');
  }

  /**
   * Print installation summary
   */
  printSummary(results, projectInfo) {
    console.log('\n╔════════════════════════════════════════════════════════════════╗');
    console.log('║  Installation Summary                                          ║');
    console.log('╚════════════════════════════════════════════════════════════════╝\n');

    if (results.success) {
      console.log('✅ TDD automation installed successfully!\n');
    } else {
      console.log('⚠️  TDD automation installed with warnings\n');
    }

    console.log('📦 What was installed:\n');
    console.log('   • CLAUDE.md: TDD workflow configuration for LLM');
    console.log('   • npm scripts: test:tdd, validate:tdd, generate:test');
    console.log('   • Git hooks: pre-commit TDD validation');
    console.log('   • Helper scripts: .tdd-automation/scripts/');
    console.log('   • Templates: Test file generators\n');

    console.log('🚀 Next steps:\n');
    console.log('   1. Test the automation:');
    console.log('      Say: "Implement user authentication"\n');
    console.log('   2. The LLM will automatically:');
    console.log('      • Follow TDD red-green-refactor workflow');
    console.log('      • Create tests BEFORE implementation');
    console.log('      • Run tests to verify each phase');
    console.log('      • Use TodoWrite to track progress\n');

    console.log('📚 Available commands:\n');
    console.log('   npm run test:tdd           # Run all tests');
    console.log('   npm run validate:tdd       # Check TDD compliance');
    console.log('   npm run generate:test <file>  # Create test template\n');

    console.log('🔧 Maintenance:\n');
    console.log('   node .tdd-automation/scripts/rollback-tdd.js');
    console.log('   node .tdd-automation/scripts/remove-tdd-section.js\n');

    if (results.warnings.length > 0) {
      console.log('⚠️  Warnings:\n');
      results.warnings.forEach(warning => {
        console.log(`   • ${warning}`);
      });
      console.log('');
    }

    console.log('═══════════════════════════════════════════════════════════════\n');
  }

  /**
   * Format bytes for display
   */
  formatBytes(bytes) {
    if (bytes < 1024) return `${bytes} bytes`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }
}

/**
 * Main entry point
 */
async function main() {
  const skill = new TddAutomationSkill();
  const results = await skill.install();

  if (!results.success && results.errors.length > 0) {
    console.error('Installation completed with errors');
    process.exit(1);
  }

  process.exit(0);
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = TddAutomationSkill;
