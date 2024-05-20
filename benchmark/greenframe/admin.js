async (page) => {
    await page.goto("admin/login/", { waitUntil: "networkidle" });
    console.log(await page.title());

    const id_username = await page.locator('#id_username');
    await id_username.type('admin');
    const id_password = await page.locator('#id_password');
    await id_password.type('changeme');
    const submit = await page.locator('[type="submit"]');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      submit.press('Enter')
    ]);

    console.log(await page.title());

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[href="/admin/pages/60/"]').first().click()
    ])
    console.log(await page.title());

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[href="/admin/pages/61/"]').first().click()
    ])
    console.log(await page.title());

    await Promise.all([
      // Very heavy page that takes forever to load.
      page.waitForNavigation({ waitUntil: 'load', timeout: 15000 }),
      page.locator('[href="/admin/pages/77/edit/"]').first().click()
    ])
    console.log(await page.title());

    const id_title = await page.locator('#id_title');
    await id_title.type('(new) ');

    const previewToggle = await page.waitForSelector('[aria-label="Toggle preview"]', { timeout: 10000 });

    await previewToggle.click();

    await page.waitForSelector('iframe[title="Preview"]', { visible: true });
    await page.waitForFunction(() => document.querySelector('iframe[title="Preview"]').contentDocument.querySelector('h1').innerText === '(new) Desserts with Benefits');

    // Un-comment to visually confirm the live preview panel’s appearance.
    // await page.screenshot({ path: 'admin.png' });
}
