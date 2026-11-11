// uso: node render.js build/unifilar.html build/ESQUEMA_UNIFILAR_A3   (genera .pdf A3 apaisado y .png)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [, , inp, out] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.round(420 * 96 / 25.4), height: Math.round(297 * 96 / 25.4) }, deviceScaleFactor: 3 });
  await p.goto('file://' + path.resolve(inp));
  await p.waitForFunction('window.READY === true');
  await p.pdf({ path: out + '.pdf', width: '420mm', height: '297mm', printBackground: true, pageRanges: '1' });
  await p.screenshot({ path: out + '.png' });
  await b.close();
})();
