// uso: node src/c2/render_a4.js build/c2/laminas.html build/c2/salida.pdf build/c2/png_prefix N
// Imprime un HTML con N páginas A4 verticales (una <svg> por página) a un PDF vectorial y una PNG por página.
const { chromium } = require('playwright-core');
const path = require('path');
(async () => {
  const [,, inp, outPdf, pngPrefix, n] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: Math.round(210 * 96 / 25.4), height: Math.round(297 * 96 / 25.4) }, deviceScaleFactor: 2.5 });
  await p.goto('file://' + path.resolve(inp));
  await p.pdf({ path: outPdf, width: '210mm', height: '297mm', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  for (let i = 0; i < +n; i++) {
    const el = await p.$('#pg' + (i + 1));
    await el.screenshot({ path: `${pngPrefix}${String(i + 1).padStart(2, '0')}.png` });
  }
  await b.close();
})();
