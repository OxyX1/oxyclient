const express = require('express');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const app = express();

  // Serve the XHTML file from the current directory (adjust the path as needed)
  app.use(express.static(path.join(__dirname)));

  // Serve index.xhtml at the root
  app.get('/', (req, res) => {
      res.sendFile(path.join(__dirname, 'index.xhtml'));
  });

  // Start the server
  const PORT = 3000;
  app.listen(PORT, () => {
      console.log(`Server running on http://localhost:${PORT}`);
  });

  // Function to scrape the input value and simulate button click with Puppeteer
  async function scrapeInput() {
      // Launch the browser in headless mode
      const browser = await puppeteer.launch({ headless: true });
      const page = await browser.newPage();

      // Navigate to the index.xhtml page hosted on the server
      await page.goto(`http://localhost:${PORT}/`);

      // Wait for the input field and button to be available
      await page.waitForSelector('#ipInput');
      await page.waitForSelector('#startButton');

      // Simulate entering a value into the input field
      await page.type('#ipInput', '192.168.1.1');  // Enter an IP address to ping

      // Click the button to start the pinging action
      await page.click('#startButton');

      // Wait for a moment to simulate the ping action (replace waitForTimeout with a custom delay)
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Get the value from the input field (the IP address)
      const ipValue = await page.$eval('#ipInput', (el) => el.value);
      console.log("IP entered for pinging:", ipValue);

      // Close the browser
      await browser.close();
  }

  await scrapeInput();
})();
