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

    await page.goto(process.env.USAGE_SCENARIO_DOMAIN+"/contact-us/", { waitUntil: "networkidle0" });
    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    await page.waitForTimeout(3000);
    await page.evaluate(() => document.querySelector('footer').scrollIntoView());
    await page.waitForNetworkIdle();

    const id_subject = await page.$('#id_subject');
    await id_subject.type('Enquiring about bread');
    const id_your_name = await page.$('#id_your_name');
    await id_your_name.type('Testing tester');
    const id_purpose = await page.$('#id_purpose');
    await id_purpose.select('Question');
    const id_body = await page.$('#id_body');
    await id_body.type('Is this is for demo purposes only?');
    const submit = await page.$('[type="submit"]');

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      submit.press('Enter')
    ]);
    console.log("GMT_SCI_R=1");


    await page.waitForTimeout(3000);
    await page.evaluate(() => document.querySelector('footer').scrollIntoView());
    await page.waitForNetworkIdle();

    console.log(microtime.now(), await page.title());
    const intro = await page.$('.index-header__body-introduction');
    console.log(microtime.now(), (await intro.evaluate((node) => node.innerText)).replaceAll("\n", "--"));

    await page.waitForTimeout(3000);
    await page.evaluate(() => document.querySelector('footer').scrollIntoView());
    await page.waitForNetworkIdle();

    await browser.close();
})().catch(err => {
    console.error(err);
    process.exit(1);
});
