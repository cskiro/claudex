import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/home.page';
import { captureWithContext } from '../utils/screenshot-helper';

/**
 * Example Playwright Test for React + Vite Application
 *
 * This demonstrates best practices for e2e testing with screenshot capture
 */

test.describe('Homepage', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.goto();

    // Capture initial page load
    await captureWithContext(page, 'homepage-initial-load', 'Homepage loaded successfully');
  });

  test('should display welcome message', async ({ page }) => {
    // Arrange: Page is already loaded in beforeEach

    // Act: No action needed, just checking initial state
    await captureWithContext(page, 'homepage-welcome-check', 'Checking for welcome message');

    // Assert: Welcome message is visible
    await expect(homePage.welcomeMessage).toBeVisible();
    await expect(homePage.welcomeMessage).toContainText('Welcome');
  });

  test('should navigate to about page when clicking About link', async ({ page }) => {
    // Arrange: Page loaded
    await captureWithContext(page, 'homepage-before-nav', 'Before clicking About link');

    // Act: Click About link
    await homePage.aboutLink.click();

    // Capture after navigation
    await page.waitForURL('**/about');
    await captureWithContext(page, 'about-page-loaded', 'About page after navigation');

    // Assert: URL changed and about page content visible
    expect(page.url()).toContain('/about');
    await expect(page.getByRole('heading', { name: 'About' })).toBeVisible();
  });

  test('should submit contact form successfully', async ({ page }) => {
    // Arrange: Navigate to contact page
    await page.goto('/contact');
    await captureWithContext(page, 'contact-form-initial', 'Contact form initial state');

    // Act: Fill out form
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john@example.com');
    await page.getByLabel('Message').fill('This is a test message');

    await captureWithContext(page, 'contact-form-filled', 'Form filled before submission');

    await page.getByRole('button', { name: 'Send Message' }).click();

    // Wait for success message
    await page.waitForSelector('[data-testid="success-message"]', { state: 'visible' });

    await captureWithContext(page, 'contact-form-success', 'Success message displayed');

    // Assert: Success message appears
    await expect(page.getByTestId('success-message')).toBeVisible();
    await expect(page.getByTestId('success-message')).toContainText('Message sent successfully');
  });

  test('should validate required fields', async ({ page }) => {
    // Arrange: Navigate to contact page
    await page.goto('/contact');
    await captureWithContext(page, 'contact-form-validation-init', 'Before validation check');

    // Act: Try to submit empty form
    await page.getByRole('button', { name: 'Send Message' }).click();

    await captureWithContext(page, 'contact-form-validation-errors', 'Validation errors displayed');

    // Assert: Error messages appear
    await expect(page.getByText('Name is required')).toBeVisible();
    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Message is required')).toBeVisible();
  });

  test('should not have accessibility violations', async ({ page }) => {
    const AxeBuilder = (await import('@axe-core/playwright')).default;

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    await captureWithContext(
      page,
      'homepage-accessibility-check',
      `Found ${accessibilityScanResults.violations.length} accessibility violations`
    );

    // Log violations for review
    if (accessibilityScanResults.violations.length > 0) {
      console.log('\n⚠️  Accessibility Violations:');
      accessibilityScanResults.violations.forEach((violation) => {
        console.log(`\n- ${violation.id}: ${violation.description}`);
        console.log(`  Impact: ${violation.impact}`);
        console.log(`  Nodes: ${violation.nodes.length}`);
      });
    }

    // Fail on critical violations only (for this example)
    const criticalViolations = accessibilityScanResults.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    expect(criticalViolations).toEqual([]);
  });

  test('should display correctly across viewports', async ({ page }) => {
    const viewports = [
      { name: 'desktop', width: 1280, height: 720 },
      { name: 'tablet', width: 768, height: 1024 },
      { name: 'mobile', width: 375, height: 667 },
    ];

    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(500); // Let responsive changes settle

      await captureWithContext(
        page,
        `homepage-responsive-${viewport.name}`,
        `${viewport.width}x${viewport.height} viewport`
      );

      // Verify no horizontal scroll on mobile/tablet
      if (viewport.name !== 'desktop') {
        const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
        const clientWidth = await page.evaluate(() => document.body.clientWidth);
        expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 1); // Allow 1px tolerance
      }

      // Verify main navigation is accessible
      const nav = page.getByRole('navigation');
      await expect(nav).toBeVisible();
    }
  });
});
