// node render.js <html> <pdf> <png>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(html));
  await p.pdf({ path: pdf, format: 'A4', landscape: true, printBackground: true });
  await p.screenshot({ path: png });
  await b.close();
})();
