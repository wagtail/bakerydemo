import { expect, test } from '@playwright/test';

test.describe('fixture-backed pages', () => {
  test('home page renders demo content', async ({ page }) => {
    await page.goto('/');

    await expect(
      page.getByRole('heading', { name: 'Welcome to the Wagtail Bakery!' }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Learn more about Wagtail' }),
    ).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Breads' })).toBeVisible();
  });

  test('desktop search returns fixture content', async ({ page }) => {
    await page.goto('/');

    await page.locator('#search-input').fill('Anadama');
    await page.locator('#search-input').press('Enter');

    await expect(page).toHaveURL(/\/search\/\?q=Anadama/);
    await expect(
      page.getByRole('heading', { name: 'Search results' }),
    ).toBeVisible();
    await expect(page.getByRole('link', { name: /Anadama/ })).toBeVisible();
  });
});
