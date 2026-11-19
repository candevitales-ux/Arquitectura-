// node render.js memoria.html salida.pdf  (portada sin número de página)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(html));
  await p.pdf({ path: out + '.a.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await p.pdf({ path: out + '.b.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;font-size:9px;color:#888;font-family:Arial;text-align:right;padding-right:25mm"><span class="pageNumber"></span></div>' });
  await b.close();
})();
