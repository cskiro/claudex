/**
 * High-Resolution Diagram Capture Script
 *
 * Converts HTML diagrams to retina-quality PNGs using Playwright API.
 *
 * IMPORTANT: This script exists because Playwright CLI does NOT support
 * --device-scale-factor flag. The CLI approach fails for hi-res capture.
 *
 * Usage:
 *   node capture-diagram.js <html-file> <output-png>
 *   node capture-diagram.js diagram.html figures/figure-1.png
 *   node capture-diagram.js  # Batch: all *diagram*.html in current dir
 *
 * Prerequisites:
 *   npm install playwright
 *   npx playwright install chromium
 *
 * Based on: paralleLLM empathy-experiment v1.0/v2.0 pipeline
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Configuration - optimized for publication quality
const CONFIG = {
  deviceScaleFactor: 2,         // 2x for retina quality (CRITICAL)
  selector: '.diagram-container', // Default container selector
  timeout: 30000,               // 30s timeout for complex diagrams
};

/**
 * Capture a single HTML file to high-res PNG
 *
 * @param {string} htmlPath - Path to HTML file
 * @param {string} pngPath - Output PNG path
 * @param {string} selector - CSS selector for element to capture
 */
async function captureScreenshot(htmlPath, pngPath, selector = CONFIG.selector) {
  const browser = await chromium.launch();

  // CRITICAL: deviceScaleFactor must be set in context, NOT in screenshot()
  const context = await browser.newContext({
    deviceScaleFactor: CONFIG.deviceScaleFactor,
  });
  const page = await context.newPage();

  const absoluteHtmlPath = path.resolve(htmlPath);

  // Verify file exists
  if (!fs.existsSync(absoluteHtmlPath)) {
    console.error(`Error: File not found: ${absoluteHtmlPath}`);
    await browser.close();
    process.exit(1);
  }

  console.log(`Capturing ${htmlPath} at ${CONFIG.deviceScaleFactor}x resolution...`);

  await page.goto(`file://${absoluteHtmlPath}`, {
    waitUntil: 'networkidle',
    timeout: CONFIG.timeout
  });

  // Try to find the selector, fall back to full page if not found
  let element;
  try {
    element = await page.locator(selector);
    const count = await element.count();
    if (count === 0) {
      console.warn(`  Warning: Selector "${selector}" not found, capturing full page`);
      await page.screenshot({ path: pngPath, type: 'png', fullPage: true });
    } else {
      await element.screenshot({ path: pngPath, type: 'png' });
    }
  } catch (error) {
    console.warn(`  Warning: ${error.message}, capturing full page`);
    await page.screenshot({ path: pngPath, type: 'png', fullPage: true });
  }

  // Verify output was created
  if (fs.existsSync(pngPath)) {
    const stats = fs.statSync(pngPath);
    console.log(`  ✓ Saved to ${pngPath} (${Math.round(stats.size / 1024)}KB)`);
  } else {
    console.error(`  ✗ Failed to create ${pngPath}`);
  }

  await browser.close();
}

/**
 * Batch capture all diagram HTML files in a directory
 *
 * @param {string} directory - Directory to scan
 */
async function captureAllDiagrams(directory = '.') {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: CONFIG.deviceScaleFactor,
  });
  const page = await context.newPage();

  // Find all *diagram*.html files
  const files = fs.readdirSync(directory)
    .filter(f => f.endsWith('.html') && f.toLowerCase().includes('diagram'));

  if (files.length === 0) {
    console.log('No diagram HTML files found (*diagram*.html pattern)');
    console.log('Tip: Name your files like "pipeline-diagram.html" or "architecture_diagram.html"');
    await browser.close();
    return;
  }

  console.log(`Found ${files.length} diagram(s) to capture at ${CONFIG.deviceScaleFactor}x resolution:\n`);

  let successCount = 0;
  for (const htmlFile of files) {
    const htmlPath = path.join(directory, htmlFile);
    const pngPath = htmlPath.replace('.html', '.png');

    console.log(`Capturing ${htmlFile}...`);
    await page.goto(`file://${path.resolve(htmlPath)}`, {
      waitUntil: 'networkidle',
      timeout: CONFIG.timeout
    });

    try {
      const element = await page.locator(CONFIG.selector);
      const count = await element.count();

      if (count === 0) {
        await page.screenshot({ path: pngPath, type: 'png', fullPage: true });
        console.log(`  ✓ ${path.basename(pngPath)} (full page - no ${CONFIG.selector})`);
      } else {
        await element.screenshot({ path: pngPath, type: 'png' });
        console.log(`  ✓ ${path.basename(pngPath)}`);
      }
      successCount++;
    } catch (error) {
      console.log(`  ✗ Failed: ${error.message}`);
    }
  }

  await browser.close();
  console.log(`\nCompleted: ${successCount}/${files.length} diagrams captured`);
}

/**
 * Display usage information
 */
function showUsage() {
  console.log(`
Benchmark Report Diagram Capture Tool
=====================================

Usage:
  node capture-diagram.js <html-file> <output-png>   # Single file
  node capture-diagram.js <directory>                 # Batch capture
  node capture-diagram.js                             # Batch in current dir

Examples:
  node capture-diagram.js diagram.html figure-1.png
  node capture-diagram.js ./docs
  node capture-diagram.js

Configuration:
  Resolution:  ${CONFIG.deviceScaleFactor}x (retina quality)
  Selector:    ${CONFIG.selector}
  Timeout:     ${CONFIG.timeout / 1000}s

Note: This script uses Playwright API because the CLI does NOT support
      --device-scale-factor for high-resolution captures.
`);
}

// Main execution
async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    showUsage();
    return;
  }

  if (args.length === 2) {
    // Single file mode: node capture-diagram.js input.html output.png
    await captureScreenshot(args[0], args[1]);
  } else if (args.length === 1) {
    // Could be directory or single HTML file
    if (fs.existsSync(args[0]) && fs.statSync(args[0]).isDirectory()) {
      await captureAllDiagrams(args[0]);
    } else if (args[0].endsWith('.html')) {
      // Single HTML, auto-generate PNG name
      const pngPath = args[0].replace('.html', '.png');
      await captureScreenshot(args[0], pngPath);
    } else {
      console.error(`Error: "${args[0]}" is not a valid directory or HTML file`);
      process.exit(1);
    }
  } else {
    // Default: capture all diagrams in current directory
    await captureAllDiagrams('.');
  }
}

main().catch(error => {
  console.error('Fatal error:', error.message);
  process.exit(1);
});
