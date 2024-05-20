async (page) => {
    await page.goto("contact-us/", { waitUntil: "networkidle" });
    console.log(await page.title());

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    const id_subject = await page.locator('#id_subject');
    await id_subject.type('Enquiring about bread');
    const id_your_name = await page.locator('#id_your_name');
    await id_your_name.type('Testing tester');
    const id_purpose = await page.locator('#id_purpose');
    await id_purpose.selectOption('Question');
    const id_body = await page.locator('#id_body');
    await id_body.type('Is this is for demo purposes only?');
    const submit = await page.locator('[type="submit"]');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      submit.press('Enter')
    ]);

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');

    console.log(await page.title());
    const intro = await page.locator('.index-header__body-introduction');
    console.log(await intro.evaluate((node) => node.innerText));

    await page.waitForTimeout(3000);
    await page.scrollToElement('footer');
    await page.waitForLoadState('networkidle');
}
