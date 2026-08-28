import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
async function ev(x){const r=await c.send('Runtime.evaluate',{expression:x,returnByValue:true});return r.result.result?r.result.result.value:null;}
const vis=`[...document.querySelectorAll('#ucgrid .uc')].filter(c=>c.style.display!=='none').length`;

await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:`${BASE}/use-cases.html`});await sleep(2200);
console.log('start                     :', await ev(vis), '|', await ev("document.getElementById('uccount').textContent"));
await ev(`[...document.querySelectorAll('.uc-filter')].find(b=>b.dataset.dim==='area'&&b.textContent.trim()==='Construction and Professional Services').click()`);
await sleep(200);
console.log('area = Construction       :', await ev(vis));
await ev(`[...document.querySelectorAll('.uc-filter')].find(b=>b.dataset.dim==='group'&&b.textContent.trim()==='Project and delivery').click()`);
await sleep(200);
console.log('  + group = Project        :', await ev(vis), '| clear button shown:', await ev("!document.getElementById('ucclear').hidden"));
await ev(`document.getElementById('ucclear').click()`); await sleep(200);
console.log('after clear               :', await ev(vis));
await ev(`[...document.querySelectorAll('.uc-filter')].find(b=>b.dataset.dim==='group'&&b.textContent.trim()==='Asset and facility').click()`);
await sleep(200);
console.log('group = Asset and facility:', await ev(vis));
await c.send('Runtime.evaluate',{expression:"document.querySelector('.uc-filterset').scrollIntoView({block:'start'})"});
await sleep(500);
let r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/uc-filters.png`,Buffer.from(r.result.data,'base64'));

// deep link from a capability group
await c.send('Page.navigate',{url:`${BASE}/use-cases.html#uc-estimating-quantity-take-offs-and-materials`});
await sleep(2400);
console.log('deep link target found    :', await ev("!!document.getElementById('uc-estimating-quantity-take-offs-and-materials')"));
console.log('  filters reset by jump    :', await ev(vis));
r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/uc-deeplink.png`,Buffer.from(r.result.data,'base64'));

// the capabilities side
await c.send('Page.navigate',{url:`${BASE}/capabilities.html`});await sleep(2200);
await ev("document.querySelectorAll('details.acc')[0].open=true");
await sleep(400);
console.log('capability group links    :', await ev("document.querySelectorAll('details.acc')[0].querySelectorAll('.acc-rel a').length"));
await ev("document.querySelectorAll('details.acc')[0].scrollIntoView({block:'start'})");
await sleep(500);
r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/cap-links.png`,Buffer.from(r.result.data,'base64'));
console.log('doc/vw', await ev('document.documentElement.scrollWidth'), await ev('innerWidth'));
process.exit(0);
