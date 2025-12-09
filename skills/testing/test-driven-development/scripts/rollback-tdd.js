#!/usr/bin/env node

/**
 * TDD Automation Rollback Utility
 *
 * Restores previous CLAUDE.md from backup and optionally removes all TDD automation.
 */

const fs = require('fs');
const path = require('path');

// Import utilities from parent directory
const projectRoot = process.cwd();
const skillRoot = path.join(__dirname, '..');

// Try to load ClaudeMdValidator from skill location
let ClaudeMdValidator;
try {
  ClaudeMdValidator = require(path.join(skillRoot, 'utils', 'validate-claude-md.js'));
} catch {
  // If skill utils not available, use local copy in .tdd-automation
  try {
    ClaudeMdValidator = require(path.join(projectRoot, '.tdd-automation', 'utils', 'validate-claude-md.js'));
  } catch {
    console.error('❌ Error: ClaudeMdValidator not found');
    console.error('   This script must be run from project root or .tdd-automation directory');
    process.exit(1);
  }
}

async function rollbackTddAutomation() {
  console.log('🔄 TDD Automation Rollback Utility\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const validator = new ClaudeMdValidator(projectRoot);

  // List available backups
  const backups = validator.listBackups();

  if (backups.length === 0) {
    console.log('❌ No backup files found');
    console.log('   Cannot rollback without backup');
    console.log('');
    console.log('   Backup files should be in: .claude/CLAUDE.md.backup.*');
    console.log('');
    process.exit(1);
  }

  console.log(`📋 Found ${backups.length} backup(s):\n`);

  backups.forEach((backup, i) => {
    const age = getTimeAgo(backup.created);
    console.log(`${i + 1}. ${backup.name}`);
    console.log(`   Created: ${backup.created.toISOString()} (${age})`);
    console.log(`   Size: ${formatBytes(backup.size)}\n`);
  });

  // Use most recent backup
  const latestBackup = backups[0];
  console.log(`🔄 Rolling back to most recent backup:\n`);
  console.log(`   ${latestBackup.name}`);
  console.log(`   Created: ${latestBackup.created.toISOString()}\n`);

  // Create backup of current state before rollback
  console.log('🔒 Creating safety backup of current state...');
  const currentBackup = validator.createBackup();

  if (currentBackup.success) {
    console.log(`✅ Current state backed up to:`);
    console.log(`   ${path.basename(currentBackup.path)}\n`);
  } else {
    console.log(`⚠️  Could not backup current state: ${currentBackup.reason}`);
    console.log(`   Proceeding with rollback anyway...\n`);
  }

  // Perform rollback
  console.log('🔄 Performing rollback...');
  const result = validator.rollback(latestBackup.path);

  if (result.success) {
    console.log('✅ Rollback successful!\n');
    console.log('   CLAUDE.md has been restored from:');
    console.log(`   ${path.basename(result.restoredFrom)}`);
    console.log(`   Size: ${formatBytes(result.size)}\n`);

    if (currentBackup.success) {
      console.log('   Your previous state was saved to:');
      console.log(`   ${path.basename(currentBackup.path)}\n`);
    }

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log('⚠️  TDD automation configuration has been removed from CLAUDE.md\n');
    console.log('   Other TDD automation components remain:');
    console.log('   • .tdd-automation/ directory');
    console.log('   • npm scripts (test:tdd, validate:tdd, etc.)');
    console.log('   • git hooks (.git/hooks/pre-commit)');
    console.log('   • Claude hooks (.claude/hooks/tdd-auto-enforcer.sh)\n');
    console.log('   To remove all TDD automation components:');
    console.log('   node .tdd-automation/scripts/uninstall-tdd.js\n');
    console.log('   To reinstall TDD automation:');
    console.log('   Run the tdd-automation skill again\n');
  } else {
    console.error('❌ Rollback failed:', result.reason);
    console.error('');
    console.error('   You may need to manually restore CLAUDE.md from backup');
    console.error(`   Backup location: ${latestBackup.path}`);
    console.error('');
    process.exit(1);
  }
}

function getTimeAgo(date) {
  const now = new Date();
  const diff = now - date;

  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  return `${seconds} second${seconds > 1 ? 's' : ''} ago`;
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} bytes`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// Run if called directly
if (require.main === module) {
  rollbackTddAutomation().catch(error => {
    console.error('❌ Unexpected error:', error.message);
    process.exit(1);
  });
}

module.exports = { rollbackTddAutomation };
