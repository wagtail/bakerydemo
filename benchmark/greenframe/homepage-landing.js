async (page) => {
    await page.goto("", { waitUntil: "networkidle" });
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[href="/breads"]').click()
    ])
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[href="/breads/bolani/"]').click()
    ])
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');
}
