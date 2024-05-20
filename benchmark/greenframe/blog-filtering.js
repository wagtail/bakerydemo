async (page) => {
    await page.goto("blog/", { waitUntil: "networkidle" });
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[aria-label="Filter by tag name dessert"]').click()
    ])
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[href="/blog/desserts-benefits/"]').click()
    ])
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');
}
