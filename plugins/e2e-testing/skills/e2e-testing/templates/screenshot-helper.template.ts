import { Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Screenshot Helper Utilities
 * Provides consistent screenshot capture with metadata
 */

export interface ScreenshotMetadata {
  path: string;
  context: string;
  timestamp: string;
  viewport: {
    width: number;
    height: number;
  };
  url: string;
  testName?: string;
}

/**
 * Capture screenshot with context metadata
 *
 * @param page - Playwright page object
 * @param name - Screenshot name (will be kebab-cased)
 * @param context - Description of what the screenshot shows
 * @returns Metadata about the captured screenshot
 */
export async function captureWithContext(
  page: Page,
  name: string,
  context: string
): Promise<ScreenshotMetadata> {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const viewport = page.viewportSize() || { width: 1280, height: 720 };
  const url = page.url();

  // Ensure screenshots directory exists
  const screenshotDir = path.join(process.cwd(), 'screenshots', 'current');
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  // Generate filename
  const filename = `${name}-${timestamp}.png`;
  const screenshotPath = path.join(screenshotDir, filename);

  // Wait for network idle before capturing
  await page.waitForLoadState('networkidle');

  // Capture screenshot
  await page.screenshot({
    path: screenshotPath,
    fullPage: true,
  });

  // Create metadata
  const metadata: ScreenshotMetadata = {
    path: screenshotPath,
    context,
    timestamp: new Date().toISOString(),
    viewport,
    url,
    testName: process.env.PLAYWRIGHT_TEST_NAME,
  };

  // Save metadata alongside screenshot
  const metadataPath = screenshotPath.replace('.png', '.json');
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

  console.log(`📸 Screenshot captured: ${filename}`);
  console.log(`   Context: ${context}`);

  return metadata;
}

/**
 * Capture element screenshot with context
 *
 * @param page - Playwright page object
 * @param selector - Element selector
 * @param name - Screenshot name
 * @param context - Description
 */
export async function captureElement(
  page: Page,
  selector: string,
  name: string,
  context: string
): Promise<ScreenshotMetadata> {
  const element = page.locator(selector);
  await element.waitFor({ state: 'visible' });

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const viewport = page.viewportSize() || { width: 1280, height: 720 };
  const url = page.url();

  const screenshotDir = path.join(process.cwd(), 'screenshots', 'current');
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  const filename = `${name}-element-${timestamp}.png`;
  const screenshotPath = path.join(screenshotDir, filename);

  await element.screenshot({
    path: screenshotPath,
  });

  const metadata: ScreenshotMetadata = {
    path: screenshotPath,
    context: `${context} (element: ${selector})`,
    timestamp: new Date().toISOString(),
    viewport,
    url,
    testName: process.env.PLAYWRIGHT_TEST_NAME,
  };

  const metadataPath = screenshotPath.replace('.png', '.json');
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

  console.log(`📸 Element screenshot captured: ${filename}`);

  return metadata;
}

/**
 * Capture comparison screenshots (before/after)
 *
 * @param page - Playwright page object
 * @param name - Base name for screenshots
 * @param actionCallback - Action to perform between screenshots
 */
export async function captureComparison(
  page: Page,
  name: string,
  actionCallback: () => Promise<void>
): Promise<{ before: ScreenshotMetadata; after: ScreenshotMetadata }> {
  const before = await captureWithContext(page, `${name}-before`, 'State before action');

  await actionCallback();

  const after = await captureWithContext(page, `${name}-after`, 'State after action');

  return { before, after };
}

/**
 * Capture screenshots across multiple viewports
 *
 * @param page - Playwright page object
 * @param name - Base name for screenshots
 * @param viewports - Array of viewport configurations
 */
export async function captureViewports(
  page: Page,
  name: string,
  viewports: Array<{ name: string; width: number; height: number }>
): Promise<ScreenshotMetadata[]> {
  const screenshots: ScreenshotMetadata[] = [];

  for (const viewport of viewports) {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });

    // Wait for responsive changes to settle
    await page.waitForTimeout(500);

    const metadata = await captureWithContext(
      page,
      `${name}-${viewport.name}`,
      `${viewport.width}x${viewport.height} viewport`
    );

    screenshots.push(metadata);
  }

  return screenshots;
}

/**
 * Generate screenshot manifest
 * Collects all screenshots and their metadata into a single manifest file
 */
export function generateManifest(): void {
  const screenshotDir = path.join(process.cwd(), 'screenshots', 'current');

  if (!fs.existsSync(screenshotDir)) {
    console.log('No screenshots directory found');
    return;
  }

  const files = fs.readdirSync(screenshotDir);
  const metadataFiles = files.filter((f) => f.endsWith('.json'));

  const manifest = metadataFiles.map((file) => {
    const content = fs.readFileSync(path.join(screenshotDir, file), 'utf-8');
    return JSON.parse(content);
  });

  const manifestPath = path.join(screenshotDir, 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  console.log(`\n📋 Screenshot manifest generated: ${manifestPath}`);
  console.log(`   Total screenshots: ${manifest.length}`);
}

/**
 * Compare screenshot with baseline
 *
 * @param currentPath - Path to current screenshot
 * @param baselinePath - Path to baseline screenshot
 * @param diffPath - Path to save diff image
 * @param threshold - Difference threshold (0-1, default 0.2 = 20%)
 */
export async function compareWithBaseline(
  currentPath: string,
  baselinePath: string,
  diffPath: string,
  threshold: number = 0.2
): Promise<{ match: boolean; diffPercentage: number }> {
  // Note: This requires pixelmatch or Playwright's built-in comparison
  // For now, this is a placeholder showing the interface

  console.log(`🔍 Comparing screenshots:`);
  console.log(`   Current: ${currentPath}`);
  console.log(`   Baseline: ${baselinePath}`);

  // Implementation would use Playwright's toHaveScreenshot comparison
  // or a library like pixelmatch for pixel-level comparison

  return {
    match: true,
    diffPercentage: 0,
  };
}
