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
const hidden = `[...document.querySelectorAll('.rv .section-heading, .rv .card, .rv .person, .rv details.acc')].filter(e=>getComputedStyle(e).opacity==='0').length`;
const total  = `document.querySelectorAll('.rv .section-heading, .rv .card, .rv .person, .rv details.acc').length`;

await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:950,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:`${BASE}/index.html`});await sleep(1500);
console.log('on load        : rv active', await ev("document.documentElement.classList.contains('rv')"),
            '| hidden', await ev(hidden), 'of', await ev(total));
console.log('  hero revealed:', await ev("getComputedStyle(document.querySelector('.hero h1')).opacity"));
let r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/rv-top.png`,Buffer.from(r.result.data,'base64'));

await ev("window.scrollTo({top:1400,behavior:'instant'})"); await sleep(1200);
console.log('after scrolling : hidden', await ev(hidden), 'of', await ev(total));
r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/rv-mid.png`,Buffer.from(r.result.data,'base64'));

await ev("window.scrollTo({top:document.body.scrollHeight,behavior:'instant'})"); await sleep(1600);
console.log('at the bottom   : hidden', await ev(hidden), 'of', await ev(total));

// reduced motion must opt out entirely
await c.send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
await c.send('Page.navigate',{url:`${BASE}/built-industry.html`});await sleep(1500);
console.log('reduced motion  : rv active', await ev("document.documentElement.classList.contains('rv')"),
            '| hidden', await ev(hidden));
await c.send('Emulation.setEmulatedMedia',{features:[]});

// with scripting off nothing may hide
await c.send('Emulation.setScriptExecutionDisabled',{value:true});
await c.send('Page.navigate',{url:`${BASE}/use-cases.html`});await sleep(1400);
console.log('no javascript   : rv active', await ev("document.documentElement.classList.contains('rv')"));
await c.send('Emulation.setScriptExecutionDisabled',{value:false});
process.exit(0);
