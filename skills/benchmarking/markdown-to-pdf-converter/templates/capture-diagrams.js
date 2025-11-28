/**
 * Diagram Capture Script
 * Converts HTML diagrams to high-resolution PNGs using Playwright
 *
 * Usage:
 *   node capture-diagrams.js [html-file] [output-png]
 *   node capture-diagrams.js  # Captures all diagrams in current directory
 *
 * Prerequisites:
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Configuration
const CONFIG = {
  deviceScaleFactor: 2,  // 2x for retina quality
  selector: '.diagram-container',  // Default container selector
};

/**
 * Capture a single HTML file to PNG
 */
async function captureScreenshot(htmlPath, pngPath, selector = CONFIG.selector) {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: CONFIG.deviceScaleFactor,
  });
  const page = await context.newPage();

  const absoluteHtmlPath = path.resolve(htmlPath);
  console.log(`Capturing ${htmlPath}...`);

  await page.goto(`file://${absoluteHtmlPath}`);

  const element = await page.locator(selector);
  await element.screenshot({
    path: pngPath,
    type: 'png',
  });

  console.log(`  → Saved to ${pngPath}`);
  await browser.close();
}

/**
 * Capture all HTML diagrams in a directory
 */
async function captureAllDiagrams(directory = '.') {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: CONFIG.deviceScaleFactor,
  });
  const page = await context.newPage();

  // Find all *_diagram*.html files
  const files = fs.readdirSync(directory)
    .filter(f => f.endsWith('.html') && f.includes('diagram'));

  if (files.length === 0) {
    console.log('No diagram HTML files found in directory');
    await browser.close();
    return;
  }

  for (const htmlFile of files) {
    const htmlPath = path.join(directory, htmlFile);
    const pngPath = htmlPath.replace('.html', '.png');

    console.log(`Capturing ${htmlFile}...`);
    await page.goto(`file://${path.resolve(htmlPath)}`);

    try {
      const element = await page.locator(CONFIG.selector);
      await element.screenshot({ path: pngPath, type: 'png' });
      console.log(`  → Saved to ${path.basename(pngPath)}`);
    } catch (error) {
      console.log(`  ✗ Failed: ${error.message}`);
    }
  }

  await browser.close();
  console.log('\nAll diagrams captured successfully!');
}

// Main execution
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 2) {
    // Single file mode: node capture-diagrams.js input.html output.png
    await captureScreenshot(args[0], args[1]);
  } else if (args.length === 1) {
    // Directory mode: node capture-diagrams.js ./docs
    await captureAllDiagrams(args[0]);
  } else {
    // Default: capture all diagrams in current directory
    await captureAllDiagrams('.');
  }
}

main().catch(console.error);
