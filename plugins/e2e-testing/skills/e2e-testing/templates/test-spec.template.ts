import { test, expect } from '@playwright/test';
import { {{PAGE_OBJECT_CLASS}} } from '../pages/{{PAGE_OBJECT_FILE}}';
import { captureWithContext } from '../utils/screenshot-helper';

/**
 * {{TEST_SUITE_NAME}}
 *
 * Tests: {{TEST_DESCRIPTION}}
 * Generated: {{GENERATED_DATE}}
 */

test.describe('{{TEST_SUITE_NAME}}', () => {
  let page: {{PAGE_OBJECT_CLASS}};

  test.beforeEach(async ({ page: testPage }) => {
    page = new {{PAGE_OBJECT_CLASS}}(testPage);
    await page.goto();

    // Capture initial page load
    await captureWithContext(
      testPage,
      '{{TEST_SUITE_NAME_KEBAB}}-initial-load',
      'Page loaded successfully'
    );
  });

  {{#TESTS}}
  test('{{TEST_NAME}}', async ({ page: testPage }) => {
    // Arrange: {{ARRANGE_DESCRIPTION}}
    {{#ARRANGE_STEPS}}
    {{STEP}}
    {{/ARRANGE_STEPS}}

    // Capture pre-action state
    await captureWithContext(
      testPage,
      '{{TEST_SUITE_NAME_KEBAB}}-{{TEST_NAME_KEBAB}}-before',
      'Before {{ACTION_DESCRIPTION}}'
    );

    // Act: {{ACTION_DESCRIPTION}}
    {{ACTION_CODE}}

    // Capture post-action state
    await captureWithContext(
      testPage,
      '{{TEST_SUITE_NAME_KEBAB}}-{{TEST_NAME_KEBAB}}-after',
      'After {{ACTION_DESCRIPTION}}'
    );

    // Assert: {{ASSERT_DESCRIPTION}}
    {{#ASSERTIONS}}
    await expect({{SELECTOR}}).{{MATCHER}};
    {{/ASSERTIONS}}

    // Final state screenshot
    await captureWithContext(
      testPage,
      '{{TEST_SUITE_NAME_KEBAB}}-{{TEST_NAME_KEBAB}}-final',
      '{{FINAL_STATE_DESCRIPTION}}'
    );
  });

  {{/TESTS}}

  test('should not have accessibility violations', async ({ page: testPage }) => {
    // Run accessibility audit
    const AxeBuilder = (await import('@axe-core/playwright')).default;

    const accessibilityScanResults = await new AxeBuilder({ page: testPage })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    // Capture page with any violations highlighted
    await captureWithContext(
      testPage,
      '{{TEST_SUITE_NAME_KEBAB}}-accessibility-check',
      `Found ${accessibilityScanResults.violations.length} accessibility violations`
    );

    // Fail if there are critical violations
    const criticalViolations = accessibilityScanResults.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    expect(criticalViolations).toEqual([]);
  });

  test('should display correctly across viewports', async ({ page: testPage }) => {
    const viewports = [
      { name: 'desktop', width: 1280, height: 720 },
      { name: 'tablet', width: 768, height: 1024 },
      { name: 'mobile', width: 375, height: 667 },
    ];

    for (const viewport of viewports) {
      await testPage.setViewportSize(viewport);

      // Wait for any responsive changes to settle
      await testPage.waitForTimeout(500);

      // Capture screenshot for each viewport
      await captureWithContext(
        testPage,
        `{{TEST_SUITE_NAME_KEBAB}}-responsive-${viewport.name}`,
        `${viewport.width}x${viewport.height} viewport`
      );

      // Basic responsive checks
      await expect(testPage.locator('body')).toBeVisible();

      // No horizontal scroll on mobile/tablet
      if (viewport.name !== 'desktop') {
        const scrollWidth = await testPage.evaluate(() => document.body.scrollWidth);
        const clientWidth = await testPage.evaluate(() => document.body.clientWidth);
        expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 1); // Allow 1px tolerance
      }
    }
  });
});
