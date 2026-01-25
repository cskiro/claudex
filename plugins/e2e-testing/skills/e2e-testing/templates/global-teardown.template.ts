import { FullConfig } from '@playwright/test';
import { generateManifest } from '../utils/screenshot-helper';

/**
 * Global Teardown
 * Runs once after all tests complete
 *
 * Responsibilities:
 * - Generate screenshot manifest
 * - Clean up temporary files (if needed)
 * - Generate summary report
 * - Perform any cleanup tasks
 */

async function globalTeardown(config: FullConfig) {
  console.log('\n🏁 Starting global teardown...\n');

  // 1. Generate screenshot manifest
  try {
    generateManifest();
  } catch (error) {
    console.error('⚠️  Failed to generate screenshot manifest:', error);
  }

  // 2. Generate test summary
  generateSummary();

  // 3. Optional: Clean up temporary files
  // cleanupTempFiles();

  console.log('\n✅ Global teardown complete\n');
}

/**
 * Generate test execution summary
 */
function generateSummary() {
  console.log('\n📊 Test Execution Summary:');
  console.log('─'.repeat(50));

  // Test results are available through Playwright's built-in reporters
  // This is just a placeholder for custom summary logic

  console.log('✅ Check playwright-report/ for detailed results');
  console.log('✅ Screenshots available in screenshots/current/');
  console.log('✅ Test results available in test-results/');

  console.log('\n💡 Next steps:');
  console.log('   1. Review screenshots for visual issues');
  console.log('   2. Compare with baselines if available');
  console.log('   3. Run visual analysis: npm run analyze:visual');
  console.log('   4. Generate fix recommendations if issues found');
}

/**
 * Optional: Clean up temporary files
 */
function cleanupTempFiles() {
  // Add cleanup logic here if needed
  // For example: remove old screenshots, clear cache, etc.
  console.log('🧹 Cleaning up temporary files...');
}

export default globalTeardown;
