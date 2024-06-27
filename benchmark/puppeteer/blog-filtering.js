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
    await page.setViewport({"width":1280,"height":800});

    await page.goto(process.env.USAGE_SCENARIO_DOMAIN+"/blog/", { waitUntil: "networkidle0" });
    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    await page.waitForTimeout(3000);
    await page.evaluate(() => document.querySelector('footer').scrollIntoView());
    await page.waitForNetworkIdle();

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      page.click('[href="/blog/tags/dessert/"]')
    ])
    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    await page.waitForTimeout(3000);
    await page.evaluate(() => document.querySelector('footer').scrollIntoView());
    await page.waitForNetworkIdle();

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      page.click('[href="/blog/desserts-benefits/"]')
    ])
    console.log(microtime.now(), await page.title());
    console.log("GMT_SCI_R=1");

    await page.waitForTimeout(3000);
    await page.evaluate(() => document.querySelector('footer').scrollIntoView());
    await page.waitForNetworkIdle();

    await browser.close();
})().catch(err => {
    console.error(err);
    process.exit(1);
});
