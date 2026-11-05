/** Local-only documentation renderer. Tool dependencies live outside the product. */
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { architectureSvg } from './architecture-layout.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const toolRoot = process.env.OX_DOC_TOOLS || '/tmp/ox-doc-visual-tools';
process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.join(toolRoot, 'browsers');
const require = createRequire(path.join(toolRoot, 'package.json'));
const { chromium } = require('playwright');
const MarkdownIt = require('markdown-it');
const md = new MarkdownIt({ html: true });
const base = path.join(root, 'docs/validation/documentation-visuals-20261104');
const output = path.join(base, 'render');
await fs.mkdir(output, { recursive: true });
const config = JSON.parse(await fs.readFile(path.join(root, 'docs/assets/mermaid.json')));
const targets = ['README.md', 'application/README.md', 'docs/README.md',
 'docs/architecture/application.md', 'docs/architecture/contracts.md',
 'docs/development/governance.md', 'docs/development/sharing.md'];
const style = `body{margin:0;background:#fff;color:#172554;font:16px/1.6 Arial,sans-serif}
main{max-width:960px;padding:32px;margin:auto;overflow-wrap:break-word}h1{font-size:36px;line-height:1.2}h2{font-size:28px;border-bottom:1px solid #cbd5e1;padding-bottom:8px;margin-top:40px}h3{font-size:20px;margin-top:32px}a{color:#4338ca}img{display:block;max-width:100%;height:auto;border-radius:8px}pre{background:#f1f5f9;padding:16px;overflow:auto;border-radius:8px}code{font-family:monospace;font-size:.9em}blockquote{border-left:4px solid #6366f1;margin:24px 0;padding:1px 20px;background:#eef2ff}table{border-collapse:collapse;display:block;overflow:auto;font-size:14px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #cbd5e1}th{background:#eef2ff}summary{cursor:pointer;color:#4338ca}details{margin:16px 0}hr{border:0;border-top:1px solid #cbd5e1;margin:32px 0}
body.dark{background:#111827;color:#e2e8f0}body.dark a,body.dark summary{color:#c7d2fe}body.dark pre{background:#1e293b}body.dark blockquote,body.dark th{background:#1e293b}body.dark img[src$=".svg"]{background:white}body.zoom{zoom:2}
@media(max-width:600px){main{padding:20px}h1{font-size:32px}h2{font-size:25px}}`;
function headingId(title) { return title.toLowerCase().replace(/[^\p{L}\p{N}_\- ]/gu, '').replace(/ /g, '-'); }
md.renderer.rules.heading_open = (tokens, i) => `<${tokens[i].tag} id="${headingId(tokens[i+1].content)}">`;
const renderHtml = (name, theme, zoom) => `<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${name} — revisão local</title><style>${style}</style><body class="${theme} ${zoom?'zoom':''}"><main>${md.render(''+contents[name])}</main></body></html>`;
const contents = Object.fromEntries(await Promise.all(targets.map(async n => [n, await fs.readFile(path.join(root, n), 'utf8')])));
const mime = {'.svg':'image/svg+xml','.png':'image/png','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.md':'text/plain'};
const server = http.createServer(async (req,res) => {
 try {
  const url = new URL(req.url, 'http://127.0.0.1');
  if (url.pathname === '/__render') {res.setHeader('content-type','text/html');res.end('<!doctype html><html><body><script type="module">import mermaid from "/_tools/node_modules/mermaid/dist/mermaid.esm.min.mjs";window.mermaid=mermaid;</script></body></html>');return;}
  if (url.searchParams.has('preview')) {
   const name = decodeURIComponent(url.pathname.slice(1));
   if (!targets.includes(name)) throw new Error('Unknown preview');
   res.setHeader('content-type','text/html');res.end(renderHtml(name,url.searchParams.get('theme')||'light',url.searchParams.has('zoom')));return;
  }
  const tools = url.pathname.startsWith('/_tools/');
  const folder = tools ? toolRoot : root;
  const relative = decodeURIComponent(url.pathname.slice(tools?8:1));
  const file = path.resolve(folder, relative);
  if (!file.startsWith(folder + path.sep)) throw new Error('Path outside allowed root');
  res.setHeader('content-type',mime[path.extname(file)]||'application/octet-stream');
  res.end(await fs.readFile(file));
 } catch(e) {res.statusCode=404;res.end(String(e));}
});
let browser;
try {
 await new Promise((resolve,reject) => {server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
 const origin = `http://127.0.0.1:${server.address().port}`;
 browser = await chromium.launch({headless:true, ...(process.env.OX_DOC_CHROMIUM ? {executablePath:process.env.OX_DOC_CHROMIUM} : {})});
 const page = await browser.newPage();
 await page.goto(origin+'/__render');
 await page.waitForFunction(() => window.mermaid);
 const pack = JSON.parse(await fs.readFile(path.join(root,'docs/assets/vendor/lucide/icons.json')));
 await page.evaluate(({config,pack}) => {window.mermaid.initialize(config);window.mermaid.registerIconPacks([{name:'lucide',icons:pack}]);},{config,pack});
 const diagrams = [];
 for (const name of (await fs.readdir(path.join(root,'docs/assets/diagrams'))).filter(n=>n.endsWith('.mmd')).sort()) {
  const source = await fs.readFile(path.join(root,'docs/assets/diagrams',name),'utf8');
  const svg = await page.evaluate(async ({source,id}) => {
   await window.mermaid.parse(source);
   const {svg} = await window.mermaid.render(id,source);
   const container = document.createElement('div');
   container.innerHTML = svg;
   const node = container.querySelector('svg');
   const doc = document;
   container.style.visibility='hidden';
   document.body.appendChild(container);
   for (const label of node.querySelectorAll('.edgeLabel .label')) {
    const b=label.getBBox();
    if(b.width>0) {
     const bg=document.createElementNS('http://www.w3.org/2000/svg','rect');
     for(const [k,v] of Object.entries({x:b.x-4,y:b.y-3,width:b.width+8,height:b.height+6,fill:'#ffffff',opacity:1}))bg.setAttribute(k,''+v);
     bg.setAttribute('style','fill:#ffffff;opacity:1;stroke:none');
     label.insertBefore(bg,label.firstChild);
    }
   }
   const [x,y,w,h]=node.getAttribute('viewBox').split(/[ ,]+/).map(Number);
   const rect=doc.createElementNS('http://www.w3.org/2000/svg','rect');
   for (const [k,v] of Object.entries({x,y,width:w,height:h,fill:'#ffffff'}))rect.setAttribute(k,''+v);
   node.insertBefore(rect,node.firstChild);
   const serialized=new XMLSerializer().serializeToString(node);
   container.remove();
   return serialized;
  },{source,id:'ox_'+name.replaceAll(/[^a-z]/g,'_')});
  const asset='docs/assets/'+name.replace('.mmd',name==='architecture.mmd'?'-mermaid.svg':'.svg');
  await fs.writeFile(path.join(root,asset),svg+'\n');
  diagrams.push({source:'docs/assets/diagrams/'+name,asset,bytes:svg.length});
 }
 await fs.writeFile(path.join(root,'docs/assets/architecture.svg'),architectureSvg(pack));
 const preview = await browser.newPage();
 const figureMetrics = [];
 for (const asset of [...diagrams.map(d=>d.asset), 'docs/assets/ox-overview.svg', 'docs/assets/architecture.svg']) {
  await preview.setViewportSize({width:1100,height:900});
  await preview.goto(origin+'/'+asset);
  const metrics=await preview.evaluate(()=>{
   const svg=document.querySelector('svg');
   const bounds=svg.getBoundingClientRect();
   const text=[...svg.querySelectorAll('text,foreignObject p')].map(t=>{
    const b=t.getBoundingClientRect(),style=getComputedStyle(t);
    return {text:t.textContent,font:style.fontSize,color:style.fill||style.color,box:{x:b.x,y:b.y,width:b.width,height:b.height},outside:b.width>0&&(b.x<bounds.x-2||b.y<bounds.y-2||b.right>bounds.right+2||b.bottom>bounds.bottom+2)};
   });
   return {viewBox:svg.getAttribute('viewBox'),display:{width:bounds.width,height:bounds.height},text,externalRefs:[...svg.querySelectorAll('[href],[src]')].map(e=>e.getAttribute('href')||e.getAttribute('src')).filter(x=>/^(https?:|\/\/)/.test(x)),title:svg.querySelector('title')?.textContent,description:svg.querySelector('desc')?.textContent};
  });
  const capture='figure-'+path.basename(asset,'.svg')+'.png';
  await preview.goto(origin+'/__render');
  await preview.setContent(`<html><body style="margin:0;background:white"><img alt="figure" style="display:block;width:1100px;height:auto" src="${origin}/${asset}"></body></html>`);
  await preview.evaluate(async()=>Promise.all([...document.images].map(i=>i.decode())));
  await preview.screenshot({path:path.join(output,capture),fullPage:true,timeout:60000});
  figureMetrics.push({asset,capture,...metrics});
 }
 const matrix = [];
 for (const name of targets) {
  for (const width of [360,768,1280]) for (const theme of ['light','dark']) {
   await preview.setViewportSize({width,height:960});
   await preview.goto(`${origin}/${name}?preview&theme=${theme}`);
   await preview.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
   const metrics=await preview.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({src:i.getAttribute('src'),width:i.width,height:i.height,loaded:i.complete&&i.naturalWidth>0})),headings:[...document.querySelectorAll('h1,h2,h3')].map(h=>({level:h.tagName,text:h.textContent})),fonts:getComputedStyle(document.body).fontFamily}));
   const id=name.replaceAll('/','_').replace('.md','')+'-'+width+'-'+theme;
   await preview.screenshot({path:path.join(output,id+'.png'),fullPage:true});
   if(name==='README.md' && width===1280)await preview.screenshot({path:path.join(output,'README-above-fold-'+theme+'.png')});
   matrix.push({document:name,theme,...metrics,capture:id+'.png'});
  }
  await preview.setViewportSize({width:1280,height:960});
  await preview.goto(`${origin}/${name}?preview&zoom`);
  await preview.evaluate(async()=>Promise.all([...document.images].map(i=>i.decode())));
  const id=name.replaceAll('/','_').replace('.md','')+'-zoom200';
  await preview.screenshot({path:path.join(output,id+'.png'),fullPage:true});
  matrix.push({document:name,theme:'light',zoom:'200% complete document CSS zoom, equivalent layout inspection rather than browser UI zoom',capture:id+'.png'});
 }
 const result={renderer:'Mermaid '+require('mermaid/package.json').version,browser:browser.version(),playwright:require('playwright/package.json').version,markdownIt:require('markdown-it/package.json').version,iconPack:'@iconify-json/lucide 1.2.74, selected offline subset',config:'docs/assets/mermaid.json',diagrams,figureMetrics,matrix,limits:'Local Markdown preview with declared CSS, not the actual VS Code webview. SVG exports are primary delivery; native Mermaid source uses renderer-dependent theme. Zoom inspection uses CSS zoom:2 for the complete document, not browser UI zoom or physical display scaling.'};
 await fs.writeFile(path.join(base,'render-results.json'),JSON.stringify(result,null,2)+'\n');
 console.log(`Rendered ${diagrams.length} diagrams and ${matrix.length} document views with ${result.renderer}.`);
 if (matrix.some(m=>m.images?.some(i=>!i.loaded)||m.scrollWidth>m.width))throw new Error('Broken image or document overflow in matrix');
} finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
