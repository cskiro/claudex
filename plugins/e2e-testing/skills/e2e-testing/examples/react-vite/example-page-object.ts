import { Page, Locator } from '@playwright/test';

/**
 * HomePage Page Object Model
 *
 * Example POM for a React + Vite application homepage
 * Demonstrates best practices for locator selection
 */

export class HomePage {
  readonly page: Page;

  // Locators - Using semantic selectors (priority: getByRole > getByLabel > getByText > getByTestId)
  readonly welcomeMessage: Locator;
  readonly aboutLink: Locator;
  readonly contactLink: Locator;
  readonly navbar: Locator;
  readonly heroSection: Locator;
  readonly ctaButton: Locator;
  readonly featureCards: Locator;

  constructor(page: Page) {
    this.page = page;

    // Initialize locators with semantic selectors
    this.navbar = page.getByRole('navigation');
    this.welcomeMessage = page.getByRole('heading', { name: /welcome/i });
    this.aboutLink = page.getByRole('link', { name: /about/i });
    this.contactLink = page.getByRole('link', { name: /contact/i });
    this.heroSection = page.getByRole('banner');
    this.ctaButton = page.getByRole('button', { name: /get started/i });
    this.featureCards = page.getByRole('article');
  }

  /**
   * Navigate to homepage
   */
  async goto() {
    await this.page.goto('/');
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Wait for page to be fully loaded and ready
   */
  async waitForReady() {
    await this.welcomeMessage.waitFor({ state: 'visible' });
    await this.navbar.waitFor({ state: 'visible' });
  }

  /**
   * Navigate to About page
   */
  async goToAbout() {
    await this.aboutLink.click();
    await this.page.waitForURL('**/about');
  }

  /**
   * Navigate to Contact page
   */
  async goToContact() {
    await this.contactLink.click();
    await this.page.waitForURL('**/contact');
  }

  /**
   * Click the main CTA button
   */
  async clickCTA() {
    await this.ctaButton.click();
  }

  /**
   * Get count of feature cards
   */
  async getFeatureCardCount(): Promise<number> {
    return await this.featureCards.count();
  }

  /**
   * Take screenshot of homepage
   */
  async screenshot(name: string = 'homepage') {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    await this.page.screenshot({
      path: `screenshots/current/${name}-${timestamp}.png`,
      fullPage: true,
    });
  }
}
