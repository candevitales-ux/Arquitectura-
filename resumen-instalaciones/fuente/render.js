const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const d=process.argv[2];
await p.goto('file://'+d+'/cover.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:d+'/cover.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
await p.goto('file://'+d+'/resumen.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:d+'/body.pdf',format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,
 headerTemplate:'<div></div>',
 footerTemplate:'<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5pt;color:#8a8aa0;padding:0 14mm;display:flex;justify-content:space-between"><span>Resumen Instalaciones</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'});
await b.close();})();
