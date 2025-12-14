import { Page, Locator } from '@playwright/test';

/**
 * {{PAGE_NAME}} Page Object Model
 *
 * Represents: {{PAGE_DESCRIPTION}}
 * URL: {{PAGE_URL}}
 * Generated: {{GENERATED_DATE}}
 */

export class {{PAGE_CLASS_NAME}} {
  readonly page: Page;

  // Locators - Using semantic selectors (getByRole, getByLabel, getByText)
  {{#LOCATORS}}
  readonly {{LOCATOR_NAME}}: Locator;
  {{/LOCATORS}}

  constructor(page: Page) {
    this.page = page;

    // Initialize locators
    {{#LOCATORS}}
    this.{{LOCATOR_NAME}} = page.{{SELECTOR}};
    {{/LOCATORS}}
  }

  /**
   * Navigate to this page
   */
  async goto() {
    await this.page.goto('{{PAGE_URL}}');
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Wait for page to be ready
   */
  async waitForReady() {
    await this.page.waitForLoadState('domcontentloaded');
    {{#READY_INDICATORS}}
    await this.{{INDICATOR}}.waitFor({ state: 'visible' });
    {{/READY_INDICATORS}}
  }

  {{#METHODS}}
  /**
   * {{METHOD_DESCRIPTION}}
   {{#PARAMS}}
   * @param {{PARAM_NAME}} - {{PARAM_DESCRIPTION}}
   {{/PARAMS}}
   */
  async {{METHOD_NAME}}({{PARAMS_SIGNATURE}}) {
    {{METHOD_BODY}}
  }

  {{/METHODS}}

  /**
   * Get page title
   */
  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  /**
   * Get current URL
   */
  async getCurrentUrl(): Promise<string> {
    return this.page.url();
  }

  /**
   * Take screenshot of this page
   * @param name - Screenshot filename
   */
  async screenshot(name: string) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    await this.page.screenshot({
      path: `screenshots/current/{{PAGE_NAME_KEBAB}}-${name}-${timestamp}.png`,
      fullPage: true,
    });
  }
}
