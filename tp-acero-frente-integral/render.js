// uso: node render.js entrada.html salida(sin ext) landscape|portrait
const { chromium } = require('playwright-core');
(async () => {
  const [,, inp, out, orient] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'] });
  const land = orient === 'landscape';
  const W = land ? 420 : 297, H = land ? 297 : 420;
  const p = await b.newPage({ viewport: { width: Math.round(W*96/25.4), height: Math.round(H*96/25.4) }, deviceScaleFactor: 4 });
  p.on('console', m => console.log('console:', m.text(), JSON.stringify(m.location())));
  p.on('pageerror', e => console.log('ERR:', e.message, e.stack));
  const http=require('http'),fs=require('fs'),path=require('path');
  const root=process.cwd();
  const srv=http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));
    fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);r.end();return;}
    const t={'.js':'text/javascript','.html':'text/html','.svg':'image/svg+xml'}[path.extname(f)]||'application/octet-stream';
    r.writeHead(200,{'Content-Type':t});r.end(d);});}).listen(8765);
  await p.goto('http://localhost:8765/' + inp);
  await p.waitForFunction('window.READY === true', { timeout: 240000 });
  if (process.argv[5]) require('fs').writeFileSync(process.argv[5], JSON.stringify(await p.evaluate(() => window.EXPORT)));
  if (process.argv[6]) require('fs').writeFileSync(process.argv[6], JSON.stringify(await p.evaluate(() => ({ VEC2D: window.VEC2D || [], OVERLAY: window.OVERLAY || '' }))));
  await p.pdf({ path: out + '.pdf', width: W+'mm', height: H+'mm', printBackground: true, pageRanges:'1' });
  await p.screenshot({ path: out + '.png', fullPage: false });
  await b.close(); srv.close();
})();
