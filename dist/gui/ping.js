const express = require('express');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const app = express();

  app.use(express.static(path.join(__dirname)));

  app.get('/', (req, res) => {
      res.sendFile(path.join(__dirname, 'index.xhtml'));
  });

  const PORT = 3000;
  app.listen(PORT, () => {
      console.log(`Server running on http://localhost:${PORT}`);
  });

  async function scrapeInput() {
      const browser = await puppeteer.launch({ headless: true });
      const page = await browser.newPage();

      await page.goto(`http://localhost:${PORT}/`);

      await page.waitForSelector('#ipInput');
      await page.waitForSelector('#startButton');

      await page.type('#ipInput', '192.168.1.1');

      await page.click('#startButton');

      await new Promise(resolve => setTimeout(resolve, 1000));

      const ipValue = await page.$eval('#ipInput', (el) => el.value);
      console.log("IP entered for pinging:", ipValue);

      await browser.close();
  }

  await scrapeInput();
})();
