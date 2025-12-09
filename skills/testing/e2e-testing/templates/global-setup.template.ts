import { chromium, FullConfig } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Global Setup
 * Runs once before all tests
 *
 * Responsibilities:
 * - Ensure dev server is ready
 * - Create screenshot directories
 * - Perform any global authentication
 * - Set up test database (if needed)
 */

async function globalSetup(config: FullConfig) {
  console.log('\n🚀 Starting global setup...\n');

  // 1. Create screenshot directories
  createScreenshotDirectories();

  // 2. Verify dev server is accessible (webServer config handles startup)
  const baseURL = config.projects[0].use.baseURL || 'http://localhost:{{PORT}}';
  await verifyServer(baseURL);

  // 3. Optional: Perform global authentication
  // await performAuthentication(config);

  console.log('✅ Global setup complete\n');
}

/**
 * Create necessary screenshot directories
 */
function createScreenshotDirectories() {
  const directories = [
    'screenshots/current',
    'screenshots/baselines',
    'screenshots/diffs',
    'test-results',
  ];

  for (const dir of directories) {
    const dirPath = path.join(process.cwd(), dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
      console.log(`📁 Created directory: ${dir}`);
    }
  }
}

/**
 * Verify dev server is accessible
 */
async function verifyServer(baseURL: string, maxRetries = 30) {
  console.log(`🔍 Verifying server at ${baseURL}...`);

  for (let i = 0; i < maxRetries; i++) {
    try {
      const browser = await chromium.launch();
      const page = await browser.newPage();

      const response = await page.goto(baseURL, { timeout: 5000 });

      if (response && response.ok()) {
        console.log(`✅ Server is ready at ${baseURL}`);
        await browser.close();
        return;
      }

      await browser.close();
    } catch (error) {
      // Server not ready yet, wait and retry
      if (i < maxRetries - 1) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      } else {
        throw new Error(
          `Server at ${baseURL} is not accessible after ${maxRetries} attempts`
        );
      }
    }
  }
}

/**
 * Optional: Perform global authentication
 * Saves authentication state to be reused across all tests
 */
async function performAuthentication(config: FullConfig) {
  // Only run if authentication is needed
  if (!process.env.AUTH_USERNAME || !process.env.AUTH_PASSWORD) {
    console.log('⏭️  Skipping authentication (no credentials provided)');
    return;
  }

  console.log('🔐 Performing global authentication...');

  const baseURL = config.projects[0].use.baseURL || 'http://localhost:{{PORT}}';
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to login page
    await page.goto(`${baseURL}/login`);

    // Fill in credentials
    await page.getByLabel('Username').fill(process.env.AUTH_USERNAME);
    await page.getByLabel('Password').fill(process.env.AUTH_PASSWORD);
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Wait for successful login (adjust selector as needed)
    await page.waitForURL(`${baseURL}/dashboard`, { timeout: 10000 });

    // Save authentication state
    await context.storageState({ path: 'auth.json' });

    console.log('✅ Authentication successful, state saved to auth.json');
  } catch (error) {
    console.error('❌ Authentication failed:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

export default globalSetup;
