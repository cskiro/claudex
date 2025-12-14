#!/usr/bin/env node

/**
 * TDD Compliance Validator
 *
 * Validates that project follows TDD best practices:
 * - All implementation files have corresponding tests
 * - Test coverage meets minimum threshold
 * - Tests are properly structured
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

async function validateTdd() {
  console.log('🔍 TDD Compliance Validation\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const results = {
    passed: [],
    failed: [],
    warnings: []
  };

  // Check 1: Verify test files exist for implementation files
  console.log('📋 Check 1: Test file coverage...');
  await checkTestFileCoverage(results);

  // Check 2: Verify test framework is installed
  console.log('\n📋 Check 2: Test framework installation...');
  await checkTestFramework(results);

  // Check 3: Verify TDD npm scripts exist
  console.log('\n📋 Check 3: TDD npm scripts...');
  await checkNpmScripts(results);

  // Check 4: Verify git hooks installed
  console.log('\n📋 Check 4: Git hooks...');
  await checkGitHooks(results);

  // Check 5: Verify CLAUDE.md has TDD configuration
  console.log('\n📋 Check 5: CLAUDE.md configuration...');
  await checkClaudeMd(results);

  // Summary
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log('📊 Validation Summary\n');

  if (results.passed.length > 0) {
    console.log(`✅ Passed: ${results.passed.length}`);
    results.passed.forEach(msg => console.log(`   • ${msg}`));
    console.log('');
  }

  if (results.warnings.length > 0) {
    console.log(`⚠️  Warnings: ${results.warnings.length}`);
    results.warnings.forEach(msg => console.log(`   • ${msg}`));
    console.log('');
  }

  if (results.failed.length > 0) {
    console.log(`❌ Failed: ${results.failed.length}`);
    results.failed.forEach(msg => console.log(`   • ${msg}`));
    console.log('');
  }

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  if (results.failed.length > 0) {
    console.log('❌ TDD compliance validation FAILED\n');
    console.log('   Please address the failed checks above');
    console.log('   Run: npm run generate:test <file> to create missing tests\n');
    process.exit(1);
  } else if (results.warnings.length > 0) {
    console.log('⚠️  TDD compliance validation PASSED with warnings\n');
    console.log('   Consider addressing the warnings above\n');
    process.exit(0);
  } else {
    console.log('✅ TDD compliance validation PASSED\n');
    console.log('   All checks passed successfully!\n');
    process.exit(0);
  }
}

async function checkTestFileCoverage(results) {
  const srcDir = path.join(process.cwd(), 'src');

  if (!fs.existsSync(srcDir)) {
    results.warnings.push('No src/ directory found - skipping test coverage check');
    return;
  }

  const implFiles = findImplementationFiles(srcDir);
  const testFiles = findTestFiles(srcDir);

  let missing = 0;
  let covered = 0;

  for (const implFile of implFiles) {
    const testFile = findCorrespondingTest(implFile, testFiles);

    if (!testFile) {
      missing++;
      if (missing <= 5) {  // Only show first 5 to avoid spam
        results.failed.push(`Missing test for: ${path.relative(process.cwd(), implFile)}`);
      }
    } else {
      covered++;
    }
  }

  if (missing > 5) {
    results.failed.push(`... and ${missing - 5} more files without tests`);
  }

  const totalFiles = implFiles.length;
  const coverage = totalFiles > 0 ? ((covered / totalFiles) * 100).toFixed(1) : 100;

  if (missing === 0 && totalFiles > 0) {
    results.passed.push(`All ${totalFiles} implementation files have tests (100%)`);
  } else if (coverage >= 80) {
    results.warnings.push(`Test file coverage: ${coverage}% (${covered}/${totalFiles}) - below 100%`);
  } else if (totalFiles === 0) {
    results.warnings.push('No implementation files found in src/');
  }
}

async function checkTestFramework(results) {
  const packageJsonPath = path.join(process.cwd(), 'package.json');

  if (!fs.existsSync(packageJsonPath)) {
    results.failed.push('package.json not found');
    return;
  }

  try {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    const allDeps = {
      ...packageJson.dependencies,
      ...packageJson.devDependencies
    };

    const testFrameworks = ['vitest', 'jest', '@jest/globals', 'mocha', 'ava'];
    const installed = testFrameworks.find(fw => allDeps[fw]);

    if (installed) {
      results.passed.push(`Test framework installed: ${installed}`);
    } else {
      results.failed.push('No test framework found (install vitest, jest, or mocha)');
    }
  } catch (error) {
    results.failed.push(`Error reading package.json: ${error.message}`);
  }
}

async function checkNpmScripts(results) {
  const packageJsonPath = path.join(process.cwd(), 'package.json');

  if (!fs.existsSync(packageJsonPath)) {
    return; // Already reported in previous check
  }

  try {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    const scripts = packageJson.scripts || {};

    const requiredScripts = ['test:tdd', 'validate:tdd', 'generate:test'];
    const missingScripts = requiredScripts.filter(script => !scripts[script]);

    if (missingScripts.length === 0) {
      results.passed.push('All TDD npm scripts installed');
    } else {
      missingScripts.forEach(script => {
        results.warnings.push(`Missing npm script: ${script}`);
      });
    }
  } catch (error) {
    results.failed.push(`Error checking npm scripts: ${error.message}`);
  }
}

async function checkGitHooks(results) {
  const preCommitPath = path.join(process.cwd(), '.git', 'hooks', 'pre-commit');

  if (!fs.existsSync(path.join(process.cwd(), '.git'))) {
    results.warnings.push('Not a git repository - no git hooks checked');
    return;
  }

  if (!fs.existsSync(preCommitPath)) {
    results.warnings.push('Git pre-commit hook not installed');
    return;
  }

  const content = fs.readFileSync(preCommitPath, 'utf-8');

  if (content.includes('TDD_AUTOMATION') || content.includes('TDD Validation')) {
    results.passed.push('Git pre-commit hook installed for TDD validation');
  } else {
    results.warnings.push('Git pre-commit hook exists but may not have TDD validation');
  }
}

async function checkClaudeMd(results) {
  const claudeMdPath = path.join(process.cwd(), '.claude', 'CLAUDE.md');

  if (!fs.existsSync(claudeMdPath)) {
    results.warnings.push('No .claude/CLAUDE.md found');
    return;
  }

  const content = fs.readFileSync(claudeMdPath, 'utf-8');

  const tddMarkers = [
    'TDD Red-Green-Refactor',
    'tdd-automation-version',
    '<!-- TDD_AUTOMATION_START -->'
  ];

  const hasTddConfig = tddMarkers.some(marker => content.includes(marker));

  if (hasTddConfig) {
    results.passed.push('CLAUDE.md has TDD configuration');
  } else {
    results.warnings.push('CLAUDE.md exists but missing TDD configuration');
  }
}

function findImplementationFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // Skip node_modules, dist, build, etc.
      if (!['node_modules', 'dist', 'build', '.git', 'coverage'].includes(entry.name)) {
        findImplementationFiles(fullPath, files);
      }
    } else if (entry.isFile()) {
      // Include .ts, .js, .tsx, .jsx files but exclude test files
      if (/\.(ts|js|tsx|jsx)$/.test(entry.name) && !/\.(test|spec)\./.test(entry.name)) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

function findTestFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      if (!['node_modules', 'dist', 'build', '.git', 'coverage'].includes(entry.name)) {
        findTestFiles(fullPath, files);
      }
    } else if (entry.isFile()) {
      if (/\.(test|spec)\.(ts|js|tsx|jsx)$/.test(entry.name)) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

function findCorrespondingTest(implFile, testFiles) {
  const dir = path.dirname(implFile);
  const filename = path.basename(implFile);
  const base = filename.replace(/\.(ts|js|tsx|jsx)$/, '');

  // Try multiple test file patterns
  const patterns = [
    path.join(dir, `${base}.test.ts`),
    path.join(dir, `${base}.test.js`),
    path.join(dir, `${base}.test.tsx`),
    path.join(dir, `${base}.test.jsx`),
    path.join(dir, `${base}.spec.ts`),
    path.join(dir, `${base}.spec.js`),
    path.join(dir, `${base}.spec.tsx`),
    path.join(dir, `${base}.spec.jsx`)
  ];

  return testFiles.find(testFile => patterns.includes(testFile));
}

// Run if called directly
if (require.main === module) {
  validateTdd().catch(error => {
    console.error('❌ Unexpected error:', error.message);
    process.exit(1);
  });
}

module.exports = { validateTdd };
