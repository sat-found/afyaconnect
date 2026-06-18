/**
 * Capture AfyaConnect UI screenshots for README documentation.
 * Requires: npx playwright (installed on first run).
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const BASE_URL = process.env.AFYA_URL || 'http://localhost:8091';
const OUT_DIR = path.join(__dirname, '..', 'docs', 'screenshots');

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.screenshot({
    path: path.join(OUT_DIR, '01-login.png'),
    fullPage: false,
  });

  const database = page.locator('#database');
  if (await database.isVisible().catch(() => false)) {
    const tag = await database.evaluate((el) => el.tagName.toLowerCase());
    if (tag === 'select') {
      await database.selectOption('health');
    } else {
      await database.fill('health');
    }
  }
  await page.locator('#login').fill('admin');
  await page.getByRole('button', { name: /login/i }).click();

  const passwordField = page.locator('#ask-dialog-entry');
  await passwordField.waitFor({ state: 'visible', timeout: 15000 });
  await passwordField.fill('gnusolidario');
  await page.locator('.ask-dialog .btn-primary').click();

  await page.waitForSelector('#menu .panel, #tablist li', { timeout: 60000 });
  await page.waitForTimeout(3000);

  const configWizard = page.locator('.modal.in:visible .btn-primary, .modal.show .btn-primary').first();
  if (await configWizard.count()) {
    await configWizard.click();
    await page.waitForTimeout(1500);
  }

  await page.screenshot({
    path: path.join(OUT_DIR, '02-dashboard.png'),
    fullPage: false,
  });

  const triageLink = page.locator('#menu').getByText('Triage Sessions', { exact: true });
  if (await triageLink.count()) {
    await triageLink.click({ force: true });
    await page.waitForTimeout(3000);
    await page.screenshot({
      path: path.join(OUT_DIR, '03-triage-sessions.png'),
      fullPage: false,
    });
  }

  const configLink = page.locator('#menu').getByText('AfyaConnect Configuration', { exact: true });
  if (await configLink.count()) {
    await configLink.click({ force: true });
    await page.waitForTimeout(2500);
    await page.screenshot({
      path: path.join(OUT_DIR, '04-afyaconnect-config.png'),
      fullPage: false,
    });
  }

  await browser.close();
  console.log('Screenshots saved to', OUT_DIR);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
