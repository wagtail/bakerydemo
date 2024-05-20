async (page) => {
    await page.goto("", { waitUntil: "networkidle" });
    console.log(await page.title());

    await page.waitForTimeout(10000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    const search = await page.locator('#search-input');
    await search.type('bread');
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      search.press('Enter')
    ]);

    console.log(await page.title());

    await page.waitForTimeout(10000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[href="/blog/icelandic-baking/"]').click()
    ])

    await page.waitForTimeout(30000);

    console.log(await page.title());
}
