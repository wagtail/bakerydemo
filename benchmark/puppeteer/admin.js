import puppeteer from 'puppeteer';
import microtime from 'microtime';

(async () => {
    const browser = await puppeteer.launch({
      headless: true,
      executablePath: "/usr/bin/chromium-browser",
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    const page = await browser.newPage();
    page.setDefaultTimeout(5000);
    await page.setViewport({"width":1280,"height":1600});

    await page.goto(process.env.USAGE_SCENARIO_DOMAIN+"/admin/login/", { waitUntil: "networkidle0" });
    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    const id_username = await page.$('#id_username');
    await id_username.type('admin');
    const id_password = await page.$('#id_password');
    await id_password.type('changeme');
    const submit = await page.$('[type="submit"]');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      submit.press('Enter')
    ]);

    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      page.click('[href="/admin/pages/60/"]')
    ])
    console.log(microtime.now(), await page.title());

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      page.click('[href="/admin/pages/61/"]')
    ])
    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    await Promise.all([
      // Very heavy page that takes forever to load.
      page.waitForNavigation({ waitUntil: 'load', timeout: 15000 }),
      page.click('[href="/admin/pages/77/edit/"]')
    ])
    console.log(microtime.now(), await page.title());

    const id_title = await page.$('#id_title');
    await id_title.type('(new) ');

    const previewToggle = await page.waitForSelector('[aria-label="Toggle preview"]', { timeout: 10000 });

    await previewToggle.click();

    await page.waitForSelector('iframe[title="Preview"]', { visible: true });

    // I keep getting the error "Preview not available."
    // https://ibb.co/3CpLYZF
    //await page.waitForFunction(() => document.querySelector('iframe[title="Preview"]').contentDocument.querySelector('h1').innerText === '(new) Desserts with Benefits');

    // Un-comment to visually confirm the live preview panel’s appearance.
    // await page.screenshot({ path: 'admin.png' });

    await browser.close();
})().catch(err => {
    console.error(err);
    process.exit(1);
});
