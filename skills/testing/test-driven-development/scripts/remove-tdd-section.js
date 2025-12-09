#!/usr/bin/env node

/**
 * TDD Section Removal Utility
 *
 * Cleanly removes only the TDD automation section from CLAUDE.md
 * while preserving all other content.
 */

const fs = require('fs');
const path = require('path');

// Import utilities
const projectRoot = process.cwd();
const skillRoot = path.join(__dirname, '..');

// Try to load ClaudeMdValidator
let ClaudeMdValidator;
try {
  ClaudeMdValidator = require(path.join(skillRoot, 'utils', 'validate-claude-md.js'));
} catch {
  try {
    ClaudeMdValidator = require(path.join(projectRoot, '.tdd-automation', 'utils', 'validate-claude-md.js'));
  } catch {
    console.error('❌ Error: ClaudeMdValidator not found');
    process.exit(1);
  }
}

async function removeTddSection() {
  console.log('🗑️  TDD Section Removal Utility\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const validator = new ClaudeMdValidator(projectRoot);

  // Check if CLAUDE.md exists
  if (!fs.existsSync(validator.claudeMdPath)) {
    console.log('❌ CLAUDE.md not found');
    console.log(`   Expected location: ${validator.claudeMdPath}`);
    console.log('');
    process.exit(1);
  }

  // Check if TDD section exists
  const content = fs.readFileSync(validator.claudeMdPath, 'utf-8');

  if (!validator.detectTddSection(content)) {
    console.log('✅ No TDD section found in CLAUDE.md');
    console.log('   Nothing to remove');
    console.log('');
    process.exit(0);
  }

  console.log('🔍 TDD section detected in CLAUDE.md\n');

  // Show what will be removed
  const startMarker = '<!-- TDD_AUTOMATION_START -->';
  const endMarker = '<!-- TDD_AUTOMATION_END -->';
  const startIdx = content.indexOf(startMarker);
  const endIdx = content.indexOf(endMarker);

  if (startIdx !== -1 && endIdx !== -1) {
    const sectionSize = endIdx - startIdx + endMarker.length;
    console.log(`   Section size: ${formatBytes(sectionSize)}`);
    console.log(`   Total file size: ${formatBytes(content.length)}`);
    console.log(`   After removal: ${formatBytes(content.length - sectionSize)}\n`);
  }

  // Perform removal
  console.log('🔒 Creating backup before removal...');
  const result = validator.removeTddSection();

  if (result.success) {
    console.log(`✅ Backup created: ${path.basename(result.backup)}\n`);
    console.log('✅ TDD section removed successfully!\n');
    console.log('   Statistics:');
    console.log(`   • Original size: ${formatBytes(result.originalSize)}`);
    console.log(`   • New size: ${formatBytes(result.newSize)}`);
    console.log(`   • Removed: ${formatBytes(result.removed)}\n`);
    console.log('   Backup available at:');
    console.log(`   ${result.backup}\n`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log('⚠️  TDD automation configuration removed from CLAUDE.md\n');
    console.log('   Other TDD automation components remain:');
    console.log('   • .tdd-automation/ directory');
    console.log('   • npm scripts (test:tdd, validate:tdd, etc.)');
    console.log('   • git hooks (.git/hooks/pre-commit)');
    console.log('   • Claude hooks (.claude/hooks/tdd-auto-enforcer.sh)\n');
    console.log('   To remove all components:');
    console.log('   node .tdd-automation/scripts/uninstall-tdd.js\n');
    console.log('   To restore this section:');
    console.log(`   node .tdd-automation/scripts/rollback-tdd.js\n`);
  } else {
    console.error('❌ Removal failed:', result.reason);
    console.error('');
    console.error('   Possible issues:');
    console.error('   • Section markers not found (manual edit may be needed)');
    console.error('   • File permissions issue');
    console.error('   • Disk space issue');
    console.error('');
    console.error('   Manual removal:');
    console.error('   1. Open .claude/CLAUDE.md in editor');
    console.error('   2. Find <!-- TDD_AUTOMATION_START -->');
    console.error('   3. Delete everything until <!-- TDD_AUTOMATION_END -->');
    console.error('   4. Save file');
    console.error('');
    process.exit(1);
  }
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} bytes`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// Run if called directly
if (require.main === module) {
  removeTddSection().catch(error => {
    console.error('❌ Unexpected error:', error.message);
    process.exit(1);
  });
}

module.exports = { removeTddSection };
